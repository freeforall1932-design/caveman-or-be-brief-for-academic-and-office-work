#!/usr/bin/env python3
"""
Build the one skill.

Everything the merged skill contains is declared in ``sources.json``. This script
turns that declaration into files; nothing in ``dist/`` is hand-written.

    python one-skill/build.py sync            # vendor upstream sources into upstream/
    python one-skill/build.py build           # sources.json + core/ + upstream/ -> dist/skill/
    python one-skill/build.py install         # mirror dist/skill/ into every install path
    python one-skill/build.py all             # build + install
    python one-skill/build.py check           # rebuild in a temp dir, fail if dist/ is stale

Adding a repository later
-------------------------
``sources.json`` is the only file to edit. Give the new source an ``origin`` of
``{"kind": "github", "repo": "owner/name", "ref": "HEAD"}`` plus a ``sync.include``
list, then one entry per skill it contributes with a ``bucket``, an ``order``, a
``title``, a ``when`` and its ``entry`` path. Then ``sync`` and ``all``.

Design
------
*   Upstream bodies are carried in **verbatim**, modulo three mechanical
    normalisations the merge requires: frontmatter stripped, one stale section
    list dropped (``strip_sections``), headings demoted one level so they nest
    under the section that names them.
*   The judgement lives in ``core/`` — the always-on rules, the precedence order
    and the router. That layer is the merge; ``dist/skill/SKILL.md`` is core/ with
    generated tables substituted in.
*   Buckets are destinations, not origins. Two skills from different repos that
    govern the same destination sit adjacent in the same reference file, which is
    where a contradiction is visible instead of being smuggled past the reader.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent          # one-skill/
REPO = ROOT.parent                              # repository root
MANIFEST_PATH = ROOT / "sources.json"
CORE_DIR = ROOT / "core"
UPSTREAM_DIR = ROOT / "upstream"
# `dist/` is a scratch tree, not a deliverable: the repository's .gitignore keeps
# generated `dist/` out of git, and the tracked artifacts are the install mirrors.
# Comparing against a mirror instead would mean trusting a copy to verify itself.
DIST_DIR = ROOT / "dist"
SKILL_DIR = DIST_DIR / "skill"
CACHE_DIR = ROOT / ".cache"
PROVENANCE = UPSTREAM_DIR / "PROVENANCE.json"

ALWAYS_ON_BUDGET = 2400   # words in SKILL.md: it rides in every request

SKIP_NAMES = {"README.md", "LICENSE", "CONTRIBUTING.md", "CHANGELOG.md", "agents", "zips"}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def die(msg: str) -> "NoReturn":
    raise SystemExit(f"build.py: {msg}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def slugify(text: str) -> str:
    """GitHub-flavoured heading anchor."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text).strip("-")


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter key -> raw value, body). A YAML subset is parsed:
    scalars, quoted strings, block scalars and inline lists."""
    meta: dict[str, str] = {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return meta, text
    raw, body = m.group(1), text[m.end():]
    key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line[0] not in " \t-" and ":" in line:
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            if val in (">", ">", "|", "|-"):
                meta[key] = ""
                continue
            meta[key] = val.strip().strip('"').strip("'")
        elif key:
            meta[key] = (meta.get(key, "") + " " + line.strip()).strip()
    for k, v in list(meta.items()):
        if v.startswith("[") and v.endswith("]"):
            meta[k] = ", ".join(x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip())
    return meta, body.strip() + "\n"


def strip_named_sections(body: str, names: list[str]) -> tuple[str, list[str]]:
    """Drop every heading whose text matches one of ``names``, plus its content,
    up to the next heading of the same or higher rank."""
    dropped: list[str] = []
    lines = body.splitlines()
    out: list[str] = []
    skip_rank = 0
    wanted = {n.strip().lower() for n in names}
    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            rank = len(m.group(1))
            title = m.group(2).strip().lower().strip("*# ").strip()
            if skip_rank and rank <= skip_rank:
                skip_rank = 0
            if title in wanted or any(title.startswith(w) for w in wanted if len(w) > 6):
                skip_rank = rank
                dropped.append(m.group(2).strip())
                continue
        if skip_rank:
            continue
        out.append(line)
    return "\n".join(out).strip() + "\n", dropped


def demote(body: str, levels: int = 1) -> str:
    """Push headings down ``levels`` levels, dropping a leading single H1 (the
    section heading the manifest supplies)."""
    lines = body.splitlines()
    if lines and re.match(r"^#\s+\S", lines[0]):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    out = []
    for line in lines:
        m = re.match(r"^(#{1,6})(\s+)(.*)$", line)
        if m:
            rank = min(6, len(m.group(1)) + levels)
            out.append("#" * rank + m.group(2) + m.group(3))
        else:
            out.append(line)
    return "\n".join(out).strip() + "\n"


# --------------------------------------------------------------------------- #
# manifest
# --------------------------------------------------------------------------- #
@dataclass
class Skill:
    cfg: dict
    source_slug: str
    source_title: str
    body: str = ""
    docs: list[tuple[str, str]] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    meta: dict = field(default_factory=dict)
    dropped: list[str] = field(default_factory=list)
    edited: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return self.cfg["id"]

    @property
    def title(self) -> str:
        return self.cfg["title"]

    @property
    def anchor(self) -> str:
        return slugify(self.title)

    @property
    def is_command(self) -> bool:
        return bool(self.cfg.get("command")) or self.meta.get("disable-model-invocation") == "true"


class Manifest:
    def __init__(self, path: Path):
        self.data = json.loads(read(path))
        self.skill = self.data["skill"]
        self.buckets = {b["id"]: b for b in self.data["buckets"]}
        self.sources = self.data["sources"]

    def entries(self) -> list[tuple[dict, dict]]:
        for src in self.sources:
            for cfg in src.get("skills", []):
                yield src, cfg

    def load(self) -> list[Skill]:
        out: list[Skill] = []
        for src, cfg in self.entries():
            entry = ROOT / cfg["entry"]
            if not entry.exists():
                die(f"{cfg['id']}: entry file missing: {cfg['entry']} (run `python one-skill/build.py sync`)")
            meta, body = split_frontmatter(read(entry))
            body, dropped = strip_named_sections(body, cfg.get("strip_sections", []))
            if cfg.get("keep_sections"):
                body, kept_dropped = keep_only_sections(body, cfg["keep_sections"])
                dropped = dropped + kept_dropped
            if cfg.get("markup"):
                body = markup_transforms(body, cfg["markup"])
            sk = Skill(cfg=cfg, source_slug=src["slug"], source_title=src["title"],
                       meta=meta, body=body, dropped=dropped)
            wanted = {w.strip().lower() for w in cfg.get("strip_sections", [])}
            got = {d.strip().lower() for d in dropped}
            for w in sorted(wanted - got):
                if not any(g.startswith(w) or w in g for g in got):
                    die(f"{cfg['id']}: strip_sections names a heading that is not in the "
                        f"source ({w!r}); the upstream section was renamed or the strip is "
                        f"stale. Update sources.json rather than shipping a dead rule.")
            for doc in cfg.get("docs", []):
                if not isinstance(doc, dict) or "path" not in doc or "label" not in doc:
                    die(f"{cfg['id']}: every doc needs {{label, path}}; got {doc!r}")
                p = ROOT / doc["path"]
                if not p.exists():
                    die(f"{cfg['id']}: doc missing: {doc['path']}")
                _, db = split_frontmatter(read(p))
                sk.docs.append({"label": doc["label"], "path": doc["path"],
                                "body": db.strip(),
                                "anchor": slugify(f"{doc['label']} ({cfg['id']})")})
            for s in cfg.get("scripts", []):
                if (ROOT / s).exists():
                    sk.scripts.append(s)
            out.append(sk)
        return out


# --------------------------------------------------------------------------- #
# sync — vendor upstream sources into upstream/
# --------------------------------------------------------------------------- #
def resolve_checkout(src: dict) -> tuple[Path, str]:
    """Local path for a source's files, cloning GitHub sources into .cache/."""
    origin = src.get("origin", {})
    if origin.get("kind") == "local":
        return REPO, git_rev(REPO)
    repo = origin["repo"]
    dest = CACHE_DIR / src["slug"]
    ref = origin.get("ref", "HEAD")
    if not (dest / ".git").exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            dest.mkdir()
        print(f"  cloning {repo} …")
        subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                        f"https://github.com/{repo}.git", str(dest)], check=True)
    if ref and ref != "HEAD":
        subprocess.run(["git", "-C", str(dest), "fetch", "--quiet", "--depth", "1", "origin", ref], check=False)
        subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", ref], check=False)
    return dest, git_rev(dest)


def git_rev(path: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        return "unversioned"


def copy_entry(base: Path, rel: str, dest: Path, skip: set[str],
               only: list[str] | None = None) -> int:
    src = base / rel
    if not src.exists():
        print(f"  ! missing: {rel}", file=sys.stderr)
        return 0
    n = 0
    if src.is_dir():
        for p in sorted(src.rglob("*")):
            if not p.is_file() or any(part in skip for part in p.relative_to(src).parts):
                continue
            if p.suffix not in {".md", ".py", ".sh", ".json", ".txt"}:
                continue
            # Some upstream skills are a SKILL.md plus a pile of SDK docs and helper
            # scripts. Vendoring the pile would put files in the bundle that nothing
            # routes to; `only` keeps the unit the merge actually works on.
            if only and not any(fnmatch(p.name, pat) for pat in only):
                continue
            target = dest / p.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)
            n += 1
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest if dest.suffix else dest / src.name)
        n = 1
    return n


def repo_hint(src: dict) -> str:
    origin = src.get("origin", {})
    return origin.get("repo") or "this repository"


def cmd_sync(man: Manifest, only: str | None = None) -> dict:
    print("sync — vendoring upstream sources")
    prov: dict = {}
    for src in man.sources:
        if only and src["slug"] != only:
            continue
        sync = src.get("sync")
        if not sync or not sync.get("include"):
            continue
        base, rev = resolve_checkout(src)
        skip = set(SKIP_NAMES) | set()
        n = 0
        missing: list[str] = []
        for item in sync["include"]:
            skip |= set(item.get("skip", []))
            dest = ROOT / item["to"]
            if not (base / item["from"]).exists():
                # a missing source is a hard error, and above all not a reason to
                # wipe: an earlier build silently deleted a whole vendored tree
                # this way when a path moved in the source repo
                missing.append(item["from"])
                continue
            if dest.exists() and dest.is_dir() and not dest.exists():
                shutil.rmtree(dest)
            n += copy_entry(base, item["from"], dest, skip, item.get("only"))
        if missing:
            die(f"{src['slug']}: sync found nothing at {missing} in {base} — the path moved "
                "in the source repo or the ref is wrong; the vendored tree was left untouched")
        discovered: list[str] = []
        for rel_dir in src.get("discover", []):
            root = base / rel_dir
            if not root.exists():
                die(f"{src['slug']}: discover path {rel_dir!r} is not in {repo_hint(src)} at "
                    f"{rev[:10]} — upstream moved, so the account of what exists there is wrong")
            for q in sorted(root.rglob("SKILL.md")):
                discovered.append(q.parent.name if q.name == "SKILL.md" else q.stem)
        if n == 0 and not discovered:
            die(f"{src['slug']}: sync copied 0 files")
        print(f"  {src['slug']}: {n} files, {len(discovered)} skills upstream "
              f"({rev[:10]})")
        prov[src["slug"]] = {
            "discovered_upstream": sorted(set(discovered)),
            "title": src["title"],
            "attribution": src.get("attribution", ""),
            "license": src.get("license", ""),
            "origin": src.get("origin", {}),
            "revision": rev,
            "files": n,
        }
    existing = {}
    if PROVENANCE.exists():
        existing = json.loads(read(PROVENANCE))
    existing.update(prov)
    write(PROVENANCE, json.dumps(existing, indent=2, sort_keys=True) + "\n")
    return existing


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #
LINK_SPAN_RE = re.compile(r"\[[^\[\]]*\]\([^)\s]+(?:\s+\"[^\"]*\")?\)")


def rewire_script_mentions(body: str, scripts: list[str]) -> str:
    """Point prose and shell examples at the carried copy of a script. Links are
    masked first: a link target is rewrite_links' business, and touching it twice
    is how `](../scripts/x.py)` becomes `](../scripts${CLAUDE_SKILL_DIR}/…)`.

    A bash example cannot use a file-relative path, because the agent's cwd is the
    project, not this skill's references directory; `${CLAUDE_SKILL_DIR}` is what
    resolves from anywhere."""
    if not scripts:
        return body
    spans: list[str] = []

    def stash(m: re.Match) -> str:
        spans.append(m.group(0))
        return f"\x00LINK{len(spans) - 1}\x00"

    masked = LINK_SPAN_RE.sub(stash, body)
    for script in scripts:
        name = Path(script).name
        # only a runtime path reference: `$VAR/name` or `./name`. A bare filename in
        # prose can be the *destination* the author is telling the agent to create,
        # and rewriting that would corrupt the instruction instead of the link.
        masked = re.sub(rf"\$\{{[A-Z_]+\}}/{re.escape(name)}",
                        f"${{CLAUDE_SKILL_DIR}}/scripts/{name}", masked)
        masked = re.sub(rf"(?<![\w./-])\./{re.escape(name)}",
                        f"../scripts/{name}", masked)
    for i, original in enumerate(spans):
        masked = masked.replace(f"\x00LINK{i}\x00", original)
    return masked


def section_anchor(sk: Skill) -> str:
    return slugify(sk.title)


def validate_records(man: Manifest) -> None:
    """A thing left out without a reason is a thing nobody decided to leave out."""
    for src in man.sources:
        for x in src.get("not_merged", []) + src.get("not_routed", []) + src.get("not_vendored", []):
            key = x.get("skill") or x.get("path") or x.get("what")
            if not isinstance(x, dict) or "reason" not in x:
                die(f"{src['slug']}: {key} is cast aside without a recorded reason")
            if not (x["reason"] or "").strip():
                die(f"{src['slug']}: {key} has an empty reason; say what is missing and "
                    "who would need it")
            if isinstance(key, dict):
                die(f"{src['slug']}: a cast-aside record needs 'skill', 'path' or 'what'")


def skill_name(src: dict, vendored: str) -> str | None:
    """Which upstream *skill* a vendored path came from. A source may vendor one file
    per skill under its own name (this repo's `legacy/` tree does), so the vendored
    directory is not always the identity; the include map is what says where a file
    actually came from."""
    for inc in src.get("sync", {}).get("include", []):
        to, frm = PurePosixPath(inc["to"]), PurePosixPath(inc["from"])
        v = PurePosixPath(vendored)
        if v == to:
            return frm.parent.name if frm.name == "SKILL.md" else None
    parent = PurePosixPath(vendored).parent.name
    return parent or None


def prov_for(man: Manifest, slug: str) -> list[str]:
    """The skill names this source was found to contain when it was last synced."""
    if not PROVENANCE.exists():
        return []
    data = json.loads(read(PROVENANCE))
    return (data.get(slug) or {}).get("discovered_upstream", [])


def inventory(man: Manifest) -> list[str]:
    """Every SKILL.md vendored from a source must be either merged or recorded as
    cast aside, with a reason. This is the difference between 'I merged what
    mattered' and 'I quietly skipped what was inconvenient': upstream grows, and a
    new skill that nobody looked at would otherwise stay invisible."""
    routed: dict[str, set[str]] = {}
    excused: dict[str, set[str]] = {}
    for src, cfg in man.entries():
        routed.setdefault(src["slug"], set()).add(skill_name(src, cfg["entry"]) or "")
    for src in man.sources:
        excused.setdefault(src["slug"], set()).update(
            n for n in (skill_name(src, x["path"]) for x in src.get("not_routed", [])) if n)
    problems: list[str] = []
    for src in man.sources:
        slug = src["slug"]
        up = UPSTREAM_DIR / slug if (UPSTREAM_DIR / slug).exists() else None
        if up is None:
            continue
        declared = {x["skill"] for x in src.get("not_merged", [])}
        missing_reason = [x["skill"] for x in src.get("not_merged", []) if not x.get("reason")]
        for r in missing_reason:
            problems.append(f"{slug}: not_merged entry {r!r} has no reason")
        found = {p.parent.name for p in up.rglob("SKILL.md")}
        # the vendored set is not the upstream set: a source may vendor one file per
        # skill under other names, and upstream may have grown a skill nobody copied
        # down at all. PROVENANCE.json records what the source held at the pinned
        # revision, and that list is what has to be accounted for.
        found |= set(prov_for(man, slug))
        seen = routed.get(slug, set()) | declared | excused.get(slug, set())
        for name in sorted(found - seen):
            problems.append(f"{slug}: vendored skill {name!r} is neither routed nor in not_merged")
        for name in sorted(declared - found):
            if not any(name == skill_name(src, cfg["entry"]) for _s, cfg in man.entries()):
                problems.append(f"{slug}: not_merged names {name!r}, which is not vendored "
                                "and not in what the source held at its pinned revision "
                                "(upstream moved or renamed it — re-check the inventory)")
    return problems


def orphans(man: Manifest) -> list[str]:
    """A vendored file that no skill routes to is a skill that silently did not get
    merged. Either route it or record it in `not_routed` with a reason."""
    routed: set[str] = set()
    for _src, cfg in man.entries():
        routed.add(cfg["entry"])
        for d in cfg.get("docs", []):
            routed.add(d["path"])
        for s in cfg.get("scripts", []):
            routed.add(s)
    allowed = {x["path"] for src in man.sources for x in src.get("not_routed", [])}
    # a file vendored under a skill that the source records as cast aside is not an
    # unmerged skill: the record is the point, and inventory() is what checks it
    cast: dict[str, set[str]] = {}
    for src in man.sources:
        cast[src["slug"]] = {x["skill"] for x in src.get("not_merged", [])}
    out: list[str] = []
    for p in sorted(UPSTREAM_DIR.rglob("*")):
        if not p.is_file() or p.name == "PROVENANCE.json":
            continue
        rel = str(p.relative_to(ROOT))
        up_parts = p.relative_to(UPSTREAM_DIR).parts
        slug = up_parts[0] if up_parts else ""
        excused = bool(set(up_parts[1:-1]) & cast.get(slug, set()))
        if rel not in routed and rel not in allowed and not excused:
            out.append(rel)
    return out


def build_registry(man: Manifest, skills: list[Skill]) -> dict[Path, tuple[str, str | None]]:
    """abs path of every carried file -> (reference file that holds it, anchor).
    Scripts carry no anchor; they land in ``scripts/``. The registry is what makes
    a link resolvable in both directions: a sibling that joined the same reference
    file becomes an in-page anchor, a sibling that went to another bucket becomes a
    link to that file. Upstream never had to distinguish the two."""
    reg: dict[Path, tuple[str, str | None]] = {}
    for sk in skills:
        bfile = Path(man.buckets[sk.cfg["bucket"]]["file"]).name
        reg[(ROOT / sk.cfg["entry"]).resolve()] = (bfile, section_anchor(sk))
        for d in sk.docs:
            reg[(ROOT / d["path"]).resolve()] = (bfile, d["anchor"])
        for s in sk.scripts:
            reg[(ROOT / s).resolve()] = ("__script__", Path(s).name)
    return reg


LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def rewrite_links(text: str, base_dir: Path, mapping, mine: str = "") -> str:
    """Repoint a relative link at the in-file section (or the carried script) that
    now holds its target. Sub-anchors survive: heading text is preserved through
    demotion, so the upstream fragment still resolves inside the merged file."""
    def repl(mm: re.Match) -> str:
        label, target = mm.group(1), mm.group(2)
        head, _, frag = target.partition("#")
        if not head or head.startswith(("/", "http", "mailto:")):
            return mm.group(0)
        resolved = (base_dir / head).resolve()
        if resolved not in mapping:
            return mm.group(0)
        holder, anchor = mapping[resolved]
        frag_suffix = f"#{frag}" if frag else ""
        if holder == "__script__":
            return f"[{label}](../scripts/{anchor}{frag_suffix})"
        if holder and holder != mine:
            return f"[{label}]({holder}#{frag or anchor})"
        return f"[{label}](#{frag or anchor})"

    return LINK_RE.sub(repl, text)


def apply_replaces(text: str, sk: Skill) -> tuple[str, list[str]]:
    """Literal, declared substitutions. Each one is recorded in SOURCES.md, so an
    edit that keeps the merged skill from lying about its own layout is auditable
    instead of being a silent rewrite of someone's text."""
    # A needle may live in the entry or in any sibling doc, so "found" is decided
    # across the whole skill, not per text: see render_skill's check at the end.
    applied: list[str] = []
    for item in sk.cfg.get("replace", []):
        if not isinstance(item, dict) or "from" not in item or "to" not in item:
            die(f"{sk.id}: every replace needs {{from, to, reason?}}; got {item!r}")
        needle, replacement = item["from"], item["to"]
        if needle in text:
            text = text.replace(needle, replacement)
            applied.append(needle)
    return text, applied


def _heading_lines(body: str):
    """Yield (line_index, rank, normalized_title, raw_title) for every heading."""
    out = []
    for i, line in enumerate(body.splitlines()):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            raw = m.group(2).strip()
            norm = re.sub(r"\[|\]|\(#[^)]*\)", "", raw).strip().lower()
            out.append((i, len(m.group(1)), norm, raw))
    return out


def _section_span(heads, idx: int, lines_n: int) -> tuple[int, int]:
    """Half-open line range of the section that starts at heads[idx]: up to the
    next heading of the same rank or shallower."""
    rank = heads[idx][1]
    for j in range(idx + 1, len(heads)):
        if heads[j][1] <= rank:
            return heads[idx][0], heads[j][0]
    return heads[idx][0], lines_n


PRECEDENCE_SCOPE_NOTE = (
    "Rows below name layers this fragment does not carry. They stay so the ruling is\n"
    "visible; do not invent what an absent layer would have said.")


def family_scope_note(man: Manifest, family: dict) -> str:
    """A fragment must say what it left out, or a model reading only this tree
    assumes the rules it cannot see do not exist."""
    held = set(family["buckets"])
    routed = {cfg["bucket"] for _src, cfg in man.entries()}
    missing = [f"{man.buckets[b]['heading'].split(' — ')[0]} (`{Path(man.buckets[b]['file']).name}`)"
               for b in man.buckets if b not in held and b in routed]
    lines = [
        "## Scope of this fragment",
        "",
        f"This is the **{family['title']}** fragment: {family['summary']}",
        "",
        f"It is a subset of `{man.skill['name']}`, built from the same manifest, and it is",
        f"**a fallback, not the default**. Install it instead of the full skill, never",
        "beside it: the always-on rules would load twice.",
    ]
    if missing:
        lines += ["", "Not included here — if the task turns into one of these, say so and",
                  "stop guessing from the rules that are present:", ""]
        lines += [f"- {m}" for m in missing]
    return "\n".join(lines)


def keep_only_sections(body: str, names: list[str]) -> tuple[str, list[str]]:
    """The inverse of strip_named_sections, for a skill that is mostly a driver for
    a tool this bundle does not ship: carry the sections that work without it, drop
    the rest by name. Keeping it this way is auditable; paraphrasing the rest into
    a tool-free version would not be. A name matching nothing fails the build."""
    wanted = {n.strip().lower().lstrip("#").strip() for n in names}
    lines = body.splitlines()
    heads = _heading_lines(body)
    keep: set[int] = set()
    matched: set[str] = set()
    for idx, (start, rank, norm, raw) in enumerate(heads):
        hit = norm in wanted or any(norm.startswith(w) for w in wanted if len(w) > 6)
        if not hit:
            continue
        matched.add(next(w for w in wanted if norm == w or norm.startswith(w)))
        a, b = _section_span(heads, idx, len(lines))
        keep.update(range(a, b))
    # a heading inside a kept section is kept, not dropped; only a section that
    # starts a discarded span counts as dropped, or the report lies about the cut
    # a leading H1 is dropped by the merge for every skill, so it is not a "cut section"
    dropped = [raw for i, rank, norm, raw in heads if i not in keep and rank > 1]
    missing = wanted - matched
    if missing:
        die(f"keep_sections names a heading that is not in the source: {sorted(missing)}")
    # text before the first heading is the skill's own framing; keep it with the
    # first kept section, or a kept section loses the sentence saying what applies
    first_head = heads[0][0] if heads else 0
    if keep:
        keep.update(range(0, first_head))
    out = [lines[i] for i in range(len(lines)) if i in keep]
    return "\n".join(out).strip() + "\n", dropped


def markup_transforms(body: str, kinds: list[str]) -> str:
    """Markup-only cleanups for sources whose text is a website or a generator
    template. Words are never changed: HTML wrapper lines go, and an
    anchor-in-heading becomes a plain heading. Both are recorded as normalisations."""
    for kind in kinds:
        if kind == "strip-html-lines":
            body = "\n".join(l for l in body.splitlines()
                              if not re.match(r"^\s*</?(div|a|img|small|h1|br|p|span|figure|script|style|iframe)\b", l)) + "\n"
        elif kind == "unwrap-heading-anchors":
            # two shapes the site generator leaves behind:
            #   ## <a name="x"></a>[Title](#x)      (anchor then self-link)
            #   ## <a name="x">[Title](#x)</a>      (link wrapped in the anchor)
            body = re.sub(r"<a name=\"[^\"]*\"></a>\s*", "", body)
            body = re.sub(r"^(#{1,6})\s*(?:<a name=\"[^\"]*\">\s*)?\[([^\]]+)\]\(#[^)]*\)\s*(?:</a>)?\s*$",
                          r"\1 \2", body, flags=re.M)
            body = re.sub(r"^(#{1,6})\s*<a name=\"[^\"]*\">(.*?)</a>\s*$", r"\1 \2", body, flags=re.M)
        elif kind == "strip-inline-html":
            body = re.sub(r"</?(?:br|small|big|em2|center|sup|sub|wbr)\s*/?>", "", body)
        elif kind == "drop-bookmark-blocks":
            body = re.sub(r"<a name=\"[^\"]*\"></a>", "", body)
            body = re.sub(r"\s{2,}$", "", body, flags=re.M)
        else:
            die(f"unknown markup transform {kind!r}")
    return body.strip() + "\n"


def render_skill(sk: Skill, registry: dict, mine: str) -> str:
    """One upstream skill -> one section of a bucket file, verbatim body."""
    parts = [f"## {sk.title}", ""]
    prov = f"`{sk.source_slug}` / `{sk.id}`"
    when = sk.cfg.get("when", "")
    parts.append(f"> {prov} / {when}" if when else f"> {prov}")
    parts.append("")
    note = sk.cfg.get("note")
    if note:
        parts.append(f"> **Merge note.** {note}")
        parts.append("")
    if sk.dropped:
        parts.append(f"> *(not carried here: {', '.join(sk.dropped)}. "
                     f"{sk.cfg.get('strip_reason', 'Upstream-only content; nothing to fetch inside a merged skill.')})*")
        parts.append("")

    entry_dir = (ROOT / sk.cfg["entry"]).resolve().parent
    body, sk.edited = apply_replaces(sk.body, sk)
    body = rewire_script_mentions(body, sk.scripts)
    body = rewrite_links(body, entry_dir, registry, mine)
    parts.append(demote(body, 1).rstrip())
    parts.append("")
    for doc in sk.docs:
        parts.append(f"### {doc['label']} ({sk.id})")
        parts.append("")
        parts.append(f"> carried verbatim from `{doc['path']}`, the same upstream "
                     f"directory as `{sk.id}`.")
        parts.append("")
        doc_dir = (ROOT / doc["path"]).resolve().parent
        doc_text, more = apply_replaces(doc["body"], sk)
        sk.edited = sorted(set(sk.edited) | set(more))
        parts.append(demote(rewrite_links(doc_text, doc_dir, registry, mine), 1).rstrip())
        parts.append("")
    # A replace that matched nothing is worse than no replace: the record in
    # SOURCES.md would describe an edit that never happened, and the misleading
    # upstream sentence stays in the shipped skill.
    unmatched = [i["from"] for i in sk.cfg.get("replace", []) if i["from"] not in sk.edited]
    if unmatched:
        die(f"{sk.id}: a declared replace matches nothing in the source any more: "
            f"{unmatched[0][:70]!r} — upstream moved, so update sources.json instead of "
            "shipping an edit that never happened")
    return "\n".join(parts).rstrip() + "\n"


def carried_files(registry: dict) -> set[Path]:
    """Every file the merge actually carries, so the audit can tell a link the
    builder was supposed to fix from a path that was never a real file."""
    return set(registry)


def audit(registry: dict, out: Path) -> list[str]:
    """Links and anchors inside the generated package must resolve. A relative
    link is only a failure if its target was something this skill ships; upstream
    prose about a repo that does not exist here is left alone."""
    problems: list[str] = []
    anchors: dict[Path, set[str]] = {}
    for p in out.rglob("*.md"):
        anchors[p] = {slugify(m.group(1)) for m in re.finditer(r"^#{1,6}\s+(.*)$", read(p), re.M)}
    for p in sorted(out.rglob("*.md")):
        raw = read(p)
        # A link inside a code span is an *example* of a link, not one: SOURCES.md
        # quotes the exact text it replaced, so without this the audit blames the
        # record for the crime.
        text = re.sub(r"`[^`\n]*`", "", re.sub(r"```.*?```", "", raw, flags=re.S))
        well_formed = {m.span() for m in re.finditer(r"\[[^\[\]]*\]\(", text)}
        covered = set()
        for start, _end in well_formed:
            covered.add(start)
        for m in re.finditer(r"\]\(", text):
            label = text[:m.start()].rfind("[")
            close = text[:m.start()].rfind("]")
            if label == -1 or (close != -1 and close > label):
                problems.append(f"{p.relative_to(out)}: link with no label at offset {m.start()}")
        for label, target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                if target[1:] and target[1:] not in anchors[p]:
                    problems.append(f"{p.relative_to(out)}: dead anchor {target} (link text: {label!r})")
                continue
            head = target.partition("#")[0]
            if not head:
                continue
            resolved = (p.parent / head).resolve()
            if resolved.exists():
                continue
            if resolved.suffix not in {".md", ".py", ".sh", ".json", ".txt"}:
                continue
            # a target the *builder* wrote (references/… is our own layout) has no
            # excuse for missing: upstream never links that way, so if one appears
            # it is a rewire that pointed at a file this bundle does not carry
            if head.startswith("references/") or head.startswith("./references/"):
                problems.append(f"{p.relative_to(out)}: link into the bundle that goes nowhere: {target}")
                continue
            if any(c.name == Path(head).name for c in carried_files(registry)):
                problems.append(f"{p.relative_to(out)}: unrewritten link {target} (link text: {label!r})")
    return problems


def assemble(man: Manifest, out: Path, family: dict | None = None) -> dict:
    """Build one skill tree. `family` is None for the unified bundle, or an entry
    from the manifest's `families` list, in which case exactly those buckets are
    assembled and the scope note says what was left behind."""
    validate_records(man)          # before writing: a broken record must not be
    if not family:                  # discoverable only in the output it produced
        problems = inventory(man)
        for msg in problems:
            print(f"  inventory: {msg}", file=sys.stderr)
        if problems:
            die(f"{len(problems)} upstream skill(s) are unaccounted for: merge them or record "
                "them under the source's not_merged with a reason")
    skills = man.load()
    if family:
        wanted = set(family["buckets"])
        unknown = wanted - set(man.buckets)
        if unknown:
            die(f"family {family['id']} names unknown buckets: {sorted(unknown)}")
        bucket_ids = [b for b in man.buckets if b in wanted]
        skills = [s for s in skills if s.cfg["bucket"] in wanted]
    else:
        bucket_ids = list(man.buckets)
    if out.exists():
        shutil.rmtree(out)

    stats = {"skills": 0, "words": 0, "references": 0, "stripped": []}
    registry = build_registry(man, skills)

    # --- references -------------------------------------------------------- #
    for bid in bucket_ids:
        bucket = man.buckets[bid]
        members = sorted(
            [s for s in skills if s.cfg["bucket"] == bid],
            key=lambda s: (s.cfg.get("order", 50), s.id),
        )
        if not members:
            continue
        head = [
            f"# {bucket['heading']}",
            "",
            f"**Read this when:** {bucket['when']}",
            "",
            f"**Layer:** {bucket['layer']}",
            "",
            "Loaded on demand: the always-on rules live in the skill's `SKILL.md`. The",
            "bodies below are upstream text carried verbatim, with the per-section",
            "provenance and every declared edit listed in `SOURCES.md` beside this file.",
            "",
            "| section | from | load |",
            "|---|---|---|",
        ]
        for s in members:
            head.append(f"| [{s.title}](#{s.anchor}) | `{s.source_slug}` | {'command' if s.is_command else 'always'} |")
        head.append("")
        bfile = Path(bucket["file"]).name
        body = "\n".join([render_skill(s, registry, bfile) for s in members])
        text = "\n".join(head).rstrip() + "\n\n---\n\n" + body
        write(out / bucket["file"], text)
        stats["references"] += 1
        stats["words"] += len(text.split())
        stats["skills"] += len(members)

    # --- scripts ----------------------------------------------------------- #
    seen_scripts: set[str] = set()
    for s in skills:
        for script in s.scripts:
            name = Path(script).name
            if name in seen_scripts:
                continue
            seen_scripts.add(name)
            src = ROOT / script
            write(out / "scripts" / name, read(src))
            (out / "scripts" / name).chmod(0o755)

    # --- SKILL.md ---------------------------------------------------------- #
    router = ["| If the task is… | Read |", "|---|---|"]
    for bid in bucket_ids:
        bucket = man.buckets[bid]
        members = [s for s in skills if s.cfg["bucket"] == bid]
        if not members:
            continue
        fname = bucket["file"].split("/")[-1]
        rows = "1 section" if len(members) == 1 else f"{len(members)} sections"
        router.append(
            f"| {bucket['when']} | [`{fname}`](references/{fname}) ({rows}) |"
        )
    commands = ["| Say | Read | What it is |", "|---|---|---|"]
    for s in sorted([x for x in skills if x.is_command], key=lambda x: (x.cfg["bucket"], x.id)):
        bucket = man.buckets[s.cfg["bucket"]]
        # A hint, not the whole `when`: this table rides in every request, and each
        # reference file opens with a full index of its sections.
        hint = s.cfg.get("hint") or re.split(r"[.;]", s.cfg.get("when", ""))[0]
        commands.append(f"| `{s.id}` | [`{bucket['file'].split('/')[-1]}`](references/{bucket['file'].split('/')[-1]}) | {hint.strip().rstrip(',')} |")

    sources_rows = ["| Source | Skills in here | License |", "|---|---|---|"]
    for src in man.sources:
        n = len([s for s in skills if s.source_slug == src["slug"]])
        sources_rows.append(f"| {src['title']} | {n} | {src.get('license', '')} |")

    tokens = {
        "ROUTER_TABLE": "\n".join(router),
        "COMMANDS_TABLE": "\n".join(commands),
        "SOURCES_TABLE": "\n".join(sources_rows),
        "SKILL_COUNT": str(len(skills)),
        "SOURCE_COUNT": str(len({s.source_slug for s in skills})),
        "FAMILY_SUMMARY": family["summary"] if family else "",
        "COMMAND_COUNT": str(len([s for s in skills if s.is_command])),
        "BUCKET_COUNT": str(stats["references"]),
        "WORD_COUNT": f"{stats['words'] // 1000}k",
        "VERSION": man.skill["version"],
        "SCOPE_NOTE": family_scope_note(man, family) if family else "",
        "PRECEDENCE_SCOPE": PRECEDENCE_SCOPE_NOTE if family else "",
    }
    # One document, one H1: every core file after the first is demoted a level so
    # the assembled SKILL.md reads as one file instead of six concatenated ones.
    core_files = sorted(CORE_DIR.glob("*.md"))
    chunks = []
    for i, cf in enumerate(core_files):
        text = read(cf).strip()
        for key, val in tokens.items():
            text = text.replace("{{" + key + "}}", val)
        if i:
            text = re.sub(r"^(#{1,5})(\s+)", lambda m: "#" * (len(m.group(1)) + 1) + m.group(2), text, flags=re.M)
        chunks.append(text)
    name = man.skill["name"] if not family else f"{man.skill['name']}-{family['id']}"
    if family:
        # a fragment must not promise the whole package in its frontmatter: the
        # description is what a host matches on before anything else is read
        desc = (f"{family['title']} fragment of One Skill — {family['summary']} "
                "Fallback for a host that cannot carry the full bundle: install this "
                "instead of one-skill, never beside it. Same always-on rules, fewer "
                "reference files. Register by destination, code byte-exact, one "
                "reference at a time.")
    else:
        desc = man.skill["description"]
    fm = [
        "---",
        f"name: {name}",
        f"description: >\n  {' '.join(desc.split())}",
        f"version: {man.skill['version']}",
        f"allowed-tools: {man.skill['allowed_tools']}",
        f"license: mixed — see references/SOURCES.md",
        f"sources: {len({s.source_slug for s in skills})} · skills: {len(skills)} · references: {stats['references']}",
        "---",
    ]
    write(out / "SKILL.md", "\n".join(fm) + "\n\n" + "\n\n".join(chunks) + "\n")
    if family:
        # the fragment's own title, above everything else, so nobody mistakes it
        # for the full skill
        text = read(out / "SKILL.md").replace(
            "# One Skill", f"# One Skill · {family['title']}", 1)
        write(out / "SKILL.md", text)

    # --- provenance -------------------------------------------------------- #
    prov = PROVENANCE.exists() and json.loads(read(PROVENANCE)) or {}
    rows = ["# Sources", "",
            "This skill is generated. `one-skill/sources.json` decides what is in it;",
            "`one-skill/build.py` writes this file. Editing `SKILL.md` or `references/`",
            "by hand is a mistake — the next build overwrites it.",
            "",
            "| source | upstream | revision | files vendored | license |",
            "|---|---|---|---|---|"]
    for src in man.sources:
        p = prov.get(src["slug"], {})
        origin = src.get("origin", {})
        up = origin.get("repo") or "this repository"
        rows.append(f"| {src['title']} | `{up}` | `{(p.get('revision') or '')[:10]}` | {p.get('files', '—')} | {src.get('license', '')} |")
    rows += ["", "## What the merge changed", "",
             "Upstream text is carried verbatim except for:",
             "",
             "1. YAML frontmatter stripped (the merged skill has one frontmatter block).",
             "2. Headings demoted one level, leading H1 dropped (each section is titled by",
             "   `sources.json`).",
             "3. Links to a sibling file rewritten to an in-file anchor, because siblings",
             "   ride in the same reference file.",
             "4. The sections listed in `strip_sections` — only the ones that instruct the",
             "   agent to fetch files or edit an entry file, which a merged skill must not do.",
             "5. Where a skill is mostly a driver for a tool this skill does not ship,",
             "   `keep_sections` carries only the sections that work without it, and",
             "   `markup` removes website markup (never words) from sources that are",
             "   generated pages. Both are listed per section below.",
             "",
             "Everything else is the author's wording. Nothing was paraphrased to make the",
             "packaging convenient.",
             ""]
    strip_notes = [s for s in skills if s.cfg.get("note") or s.dropped or s.edited]
    if strip_notes:
        rows += ["## Per-section notes", "", "| section | carried from | notes |", "|---|---|---|"]
        for s in strip_notes:
            note = s.cfg.get("note", "")
            if s.dropped:
                note = (note + " " if note else "") + f"Not carried: {', '.join(s.dropped)}."
            if s.edited:
                note += " Literal edits recorded in `replace`: " + "; ".join(f"`{e}`" for e in s.edited) + "."
            rows.append(f"| {s.title} | `{s.source_slug}/{s.id}` | {note} |")
        rows.append("")
    cast = [s for s in man.sources if s.get("not_merged") or s.get("not_vendored") or s.get("not_routed")]
    if cast and not family:
        rows += ["", "## What was deliberately not merged", "",
                 "Everything vendored from a source is either routed into a reference file above, or",
                 "listed here with the reason it was cast aside. The build fails if a vendored `SKILL.md`",
                 "is neither, so this table cannot go stale while upstream grows.", "",
                 "| source | left out | why |", "|---|---|---|"]
        for src in cast:
            for x in src.get("not_merged", []):
                rows.append(f"| `{src['slug']}` | skill `{x['skill']}` | {x['reason']} |")
            for x in src.get("not_routed", []):
                rows.append(f"| `{src['slug']}` | file `{Path(x['path']).name}` | {x['reason']} |")
            for x in src.get("not_vendored", []):
                rows.append(f"| `{src['slug']}` | not vendored: {x['what']} | {x['reason']} |")
        rows.append("")
    write(out / "references" / "SOURCES.md", "\n".join(rows).rstrip() + "\n")

    # upstream checksums, so a stale vendored file is detectable
    lock = {"generated_by": "one-skill/build.py", "manifest_sha": sha256(read(MANIFEST_PATH)),
            "skills": {}}
    for s in skills:
        lock["skills"][f"{s.source_slug}/{s.id}"] = {
            "entry": s.cfg["entry"],
            "sha": sha256(read(ROOT / s.cfg["entry"])),
            "bucket": s.cfg["bucket"],
        }
    write(out / "BUILD.json", json.dumps(lock, indent=2, sort_keys=True) + "\n")

    if family:
        downgrade_foreign_links(out)
    # measured on disk, after every post-pass: a fix that grows SKILL.md must be
    # paid for too, or the budget only guards the text before the last transform
    always = len(read(out / "SKILL.md").split())
    stats["always_words"] = always
    if always > ALWAYS_ON_BUDGET:
        die(f"{out.name}/SKILL.md is {always} words; the always-loaded file must stay under "
            f"{ALWAYS_ON_BUDGET}. Move depth into a bucket, shorten a table column, or "
            "cut a rule that no source asked for.")
    stats["dead_links"] = audit(registry, out)
    stats["orphans"] = orphans(man)
    if stats["orphans"] and not family:
        for o in stats["orphans"]:
            print(f"  unaccounted vendored file: {o}", file=sys.stderr)
        die(f"{len(stats['orphans'])} vendored file(s) are neither routed to a bucket nor "
            "listed in a source's not_routed with a reason")
    return stats



def downgrade_foreign_links(out: Path) -> None:
    """A fragment is a projection of the same bundle, so link rewriting is done
    against the full registry — which leaves links pointing at a reference file this
    tree does not carry. Those become a plain mention: the reader is told the file
    exists and where, instead of being handed a link that goes nowhere."""
    have = {p.name for p in (out / "references").glob("*.md")}
    pat = re.compile(r"\[([^\]]*)\]\((?!http|mailto|#)([^)\s]*?([A-Za-z0-9._-]+\.md))(#[^\s)]*)?\)")

    def fix(m: re.Match, cur: Path = Path(".")) -> str:
        label, resolved = m.group(1), cur / m.group(2)
        fname = m.group(3)
        if fname in have and (p.parent / m.group(2)).resolve().exists():
            return m.group(0)
        if (p.parent / m.group(2)).resolve().exists():
            return m.group(0)
        # the label of such a link is usually the file name itself; saying it twice
        # reads like a bug in the generator, which it is not
        if fname in label.replace("*", "").strip():
            return f"`{fname}`, in the full skill"
        return f"**{label}** (`{fname}`, in the full skill)"

    for p in sorted(out.rglob("*.md")):
        text = read(p)

        def sub(m: re.Match) -> str:
            return fix(m, cur=p)
        new = pat.sub(sub, text)
        if new != text:
            write(p, new)


def build_all(man: Manifest, base: Path) -> dict:
    """The unified skill, then every fragment. One manifest, one load, N trees: a
    fragment is a bucket subset, never a fork of the content."""
    stats = assemble(man, base / "skill")
    for fam in man.data.get("families", []):
        fam_stats = assemble(man, base / "families" / fam["id"], family=fam)
        stats.setdefault("families", {})[fam["id"]] = fam_stats
    return stats


def report(stats: dict) -> dict:
    print(f"built {stats['skills']} skills into {stats['references']} references "
          f"({stats['words'] // 1000}k words of reference material)")
    always = read(SKILL_DIR / "SKILL.md").split()
    print(f"SKILL.md: {len(always)} words always loaded")
    for p in stats["dead_links"]:
        print(f"  dead link: {p}", file=sys.stderr)
    if stats["dead_links"]:
        die(f"{len(stats['dead_links'])} dead link(s) in the merged skill")
    if stats.get("orphans"):
        print("  (orphans reported by the build; see above)")
    if len(always) > ALWAYS_ON_BUDGET:
        die(f"SKILL.md is {len(always)} words; the always-loaded file must stay under {ALWAYS_ON_BUDGET}. "
            "Move depth into a bucket, or shorten a table column.")
    return stats


# --------------------------------------------------------------------------- #
# install — mirror the single skill into every path this repo publishes
# --------------------------------------------------------------------------- #
INSTALL_DIRS = [
    REPO / ".claude" / "skills" / "one-skill",     # Claude Code, opened in this repo
    REPO / "claude-skills" / "app" / "one-skill",  # Claude app/web source
]


def cmd_install(man: Manifest) -> None:
    if not SKILL_DIR.exists():
        die("dist/skill missing — run `build` first")
    for dest in INSTALL_DIRS:
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(SKILL_DIR, dest)
        print(f"  installed → {dest.relative_to(REPO)}")

    for fam in man.data.get("families", []):
        src = DIST_DIR / "families" / fam["id"]
        dest = REPO / "claude-skills" / "fragments" / f"one-skill-{fam['id']}"
        if not src.exists():
            die(f"{src} missing — run `python one-skill/build.py build`")
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        fz = REPO / "claude-skills" / "fragments" / "zips" / f"one-skill-{fam['id']}.zip"
        fz.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(fz, "w", zipfile.ZIP_DEFLATED) as z:
            for q in sorted(src.rglob("*")):
                if q.is_file():
                    z.write(q, Path(f"one-skill-{fam['id']}") / q.relative_to(src))
        print(f"  fragment → {dest.relative_to(REPO)} "
              f"(+ {fz.relative_to(REPO)}, {fz.stat().st_size // 1024} KiB)")

    zip_path = REPO / "claude-skills" / "app" / "zips" / "one-skill.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(SKILL_DIR.rglob("*")):
            if p.is_file():
                z.write(p, Path("one-skill") / p.relative_to(SKILL_DIR))
    print(f"  zip → {zip_path.relative_to(REPO)} ({zip_path.stat().st_size // 1024} KiB)")

    # paste-only platforms: the router file alone, unchanged in substance
    pseudo = REPO / "pseudo-skills" / "one-skill.md"
    body = read(SKILL_DIR / "SKILL.md")
    refs = len(list((SKILL_DIR / "references").glob("*.md"))) - 1  # minus SOURCES.md
    head = (
        f"> **Paste-only setup.** This is the router half of the `one-skill` skill. The\n"
        f"> {refs} reference files it points at carry the upstream rule sets, SOURCES.md the\n"
        f"> provenance; none of them are pasted here, because a monolith of all of them\n"
        f"> would cost more context than it saves.\n"
        "> For a task that needs one, paste this file plus that reference. In the\n"
        "> repo they live next to this file at `one-skill/dist/skill/references/`; a host\n"
        "> that cannot read files at all should use a fragment instead\n"
        "> (`claude-skills/fragments/`), which is the same rules with fewer files.\n\n"
    )
    write(pseudo, head + body)
    print(f"  paste file → {pseudo.relative_to(REPO)}")


# --------------------------------------------------------------------------- #
def cmd_check(man: Manifest) -> None:
    """The gate CI runs. Rebuild from the manifest and compare against every
    tracked artifact this skill is published as.

    It compares against the mirrors rather than `dist/`, because `dist/` is
    gitignored — in CI there is no `dist/`, and a check that reads a directory
    which may simply be absent reports success on an empty tree. That is exactly
    how this build once shipped a stale bundle, so the mirrors are the contract.
    The fragments are mirrors too: a stale fragment is as broken as a stale skill."""
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        stats = build_all(man, base)

        trees = [(d, base / "skill") for d in INSTALL_DIRS]
        trees += [(REPO / "claude-skills" / "fragments" / f"one-skill-{fam['id']}",
                   base / "families" / fam["id"]) for fam in man.data.get("families", [])]
        for dest, src in trees:
            if not dest.exists():
                die(f"{dest.relative_to(REPO)} does not exist — run `python one-skill/build.py install`")
            for p in sorted(src.rglob("*")):
                if not p.is_file():
                    continue
                mirror = dest / p.relative_to(src)
                if not mirror.exists():
                    die(f"{mirror.relative_to(REPO)} is missing — run `python one-skill/build.py install`")
                if read(mirror) != read(p):
                    die(f"{mirror.relative_to(REPO)} is stale — run `python one-skill/build.py install`")
            extra = [q.relative_to(dest) for q in dest.rglob("*")
                     if q.is_file() and not (src / q.relative_to(dest)).exists()]
            if extra:
                die(f"{dest.relative_to(REPO)} holds files the build no longer emits: "
                    f"{', '.join(map(str, extra[:5]))}")

        paste = REPO / "pseudo-skills" / "one-skill.md"
        if not paste.exists() or read(base / "skill" / "SKILL.md") not in read(paste):
            die("pseudo-skills/one-skill.md is missing or is not the current SKILL.md")

        if SKILL_DIR.exists():
            for p in sorted((base / "skill").rglob("*")):
                if not p.is_file():
                    continue
                q = SKILL_DIR / p.relative_to(base / "skill")
                if q.exists() and read(q) != read(p):
                    die(f"one-skill/dist is out of step with a fresh build: {p.relative_to(base / 'skill')}")
    fam_note = ""
    if stats.get("families"):
        fam_note = "; fragments " + ", ".join(
            f"{k} ({v['skills']} skills, {v['words'] // 1000}k words of reference)"
            for k, v in stats["families"].items())
    print(f"published copies are current ({stats['skills']} skills, "
          f"{stats['references']} references, {len(stats['dead_links'])} dead links{fam_note})")


def main() -> int:
    ap = argparse.ArgumentParser(description="build the one skill from sources.json")
    ap.add_argument("cmd", nargs="?", default="all",
                    choices=["sync", "build", "install", "all", "check"])
    ap.add_argument("--only", help="with sync: vendor one source slug")
    args = ap.parse_args()
    man = Manifest(MANIFEST_PATH)
    if args.cmd == "sync":
        cmd_sync(man, args.only)
    elif args.cmd == "build":
        stats = report(build_all(man, DIST_DIR))
    elif args.cmd == "install":
        cmd_install(man)
    elif args.cmd == "check":
        cmd_check(man)
    else:
        report(build_all(man, DIST_DIR))
        cmd_install(man)
    return 0


if __name__ == "__main__":
    sys.exit(main())
