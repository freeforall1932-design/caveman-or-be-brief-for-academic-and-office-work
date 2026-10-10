"""
Tests for the merge itself.

These do not check that the writing is good. They check the four properties the
packaging depends on, the ones that rot quietly when a source is added or upstream
moves:

    fidelity        upstream text survives the merge unparaphrased
    integrity       no link or anchor in the generated skill points at nothing,
                    and no vendored file is left unrouted
    determinism     the same inputs produce the same bytes
    budget          SKILL.md, which rides in every request, stays small
    installed       what the repository publishes is what the builder emitted
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import pytest

ONE_SKILL = Path(__file__).resolve().parents[1]
REPO = ONE_SKILL.parent
DIST = ONE_SKILL / "dist" / "skill"


def _load_build():
    spec = importlib.util.spec_from_file_location("one_skill_build", ONE_SKILL / "build.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module          # dataclass needs the module registered
    spec.loader.exec_module(module)
    return module


b = _load_build()
manifest = b.Manifest(ONE_SKILL / "sources.json")


@pytest.fixture(scope="session")
def built():
    """dist/skill/, regenerated into a temp dir so tests never read stale output."""
    tmp = Path(tempfile.mkdtemp()) / "skill"
    stats = b.assemble(manifest, tmp)
    yield tmp, stats
    shutil.rmtree(tmp.parent, ignore_errors=True)


def manifest_data() -> dict:
    return json.loads((ONE_SKILL / "sources.json").read_text())


# --------------------------------------------------------------------------- #
# manifest shape
# --------------------------------------------------------------------------- #
def test_manifest_parses_and_loads():
    skills = manifest.load()
    assert len(skills) >= 40, "the merge is meant to hold every skill in three repos"


def test_skill_ids_unique():
    ids = [cfg["id"] for _src, cfg in manifest.entries()]
    assert len(ids) == len(set(ids)), f"duplicate ids: {[i for i in ids if ids.count(i) > 1]}"


def test_every_bucket_is_declared():
    declared = set(manifest.buckets)
    for _src, cfg in manifest.entries():
        assert cfg["bucket"] in declared, f"{cfg['id']} routes to unknown bucket {cfg['bucket']}"


def test_every_bucket_has_content():
    used = {cfg["bucket"] for _src, cfg in manifest.entries()}
    empty = set(manifest.buckets) - used
    assert not empty, f"buckets declared with nothing in them: {empty}"


def test_each_skill_declares_a_when_and_title():
    for _src, cfg in manifest.entries():
        assert cfg.get("title") and cfg.get("when"), f"{cfg.get('id')} needs title + when for the router"


def test_upstream_and_license_are_recorded():
    for src in manifest.sources:
        assert src.get("license"), f"{src['slug']} needs a license: this skill redistributes it"
        assert src.get("attribution") or src.get("origin", {}).get("kind") == "local"


# --------------------------------------------------------------------------- #
# fidelity: upstream text must arrive unparaphrased
# --------------------------------------------------------------------------- #
PROSE_LINE = re.compile(r"^[^#|>\[\s`*].{60,}$")


def _prose_lines(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not PROSE_LINE.match(s) or "](" in s or "`" in s or "**" in s:
            continue
        out.append(s)
    return out


def test_bodies_are_carried_verbatim(built):
    """For every merged skill, its plain prose lines must appear verbatim in the
    reference file that carries it. A rewrite for "clarity" fails here.

    Three categories are excluded, because they are edits the builder makes on
    purpose: sections named in `strip_sections`, lines touched by a declared
    `replace`, and lines holding a carried script's path. Undeclared drift is still
    caught: the strip and replace guards fail if their targets move upstream, and
    the dead-link audit catches anything a retargeting missed."""
    out, _stats = built
    offenders = []
    for sk in manifest.load():
        text = b.read(out / manifest.buckets[sk.cfg["bucket"]]["file"])
        _meta, raw = b.split_frontmatter(b.read(ONE_SKILL / sk.cfg["entry"]))
        stripped, _dropped = b.strip_named_sections(raw, sk.cfg.get("strip_sections", []))
        declared = [i["from"] for i in sk.cfg.get("replace", [])]
        declared += [Path(s).name for s in sk.scripts]      # the carried-script rewire
        lines = [l for l in _prose_lines(stripped) if not any(d in l for d in declared)]
        if len(lines) < 3:
            continue                      # tiny skill, nothing to sample
        missing = [l for l in lines if l not in text]
        if missing:
            offenders.append(f"{sk.id}: {len(missing)}/{len(lines)} prose lines did not survive"
                             f"\n    " + "\n    ".join(m[:110] for m in missing[:3]))
    assert not offenders, "\n".join(offenders)


def test_docs_ride_with_their_skill(built):
    """A sibling file must land in the same section as the skill that linked it, or
    the retargeted links point at nothing."""
    out, _ = built
    text = b.read(out / "references" / "code-craft.md")
    for heading in ("### What a good test looks like (tdd)", "### Mocking (tdd)",
                    "### Deepening (codebase-design)"):
        assert heading in text, heading
    assert "](#what-a-good-test-looks-like-tdd)" in text


def test_scripts_are_carried_and_invocable(built):
    out, _ = built
    checker = out / "scripts" / "contrast-check.py"
    assert checker.exists()
    r = subprocess.run([sys.executable, str(checker), "#FFFFFF", "#777777"],
                       capture_output=True, text=True)
    assert "4.48" in r.stdout and "FAIL" in r.stdout and "PASS" in r.stdout, r.stdout + r.stderr
    # non-zero is the point: the checker is a gate, and this pair fails AA
    assert r.returncode == 1, "the contrast gate no longer signals failure by exit code"
    ok = subprocess.run([sys.executable, str(checker), "#000000", "#FFFFFF"],
                        capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_install_wizard_sections_do_not_survive(built):
    """A merged skill must never tell the agent to download a file or edit an entry
    file. Those sections are stripped, so their tell-tale phrasing must be gone."""
    out, _ = built
    for p in out.rglob("*.md"):
        text = b.read(p)
        if p.name == "SOURCES.md" or p.parent == out:      # provenance may quote them
            continue
        for forbidden in ("run the wizard", "Append the pointer block at the END",
                          "Get the chosen skill(s) in place"):
            assert forbidden not in text, f"{p.name} still tells the agent to install things: {forbidden!r}"


# --------------------------------------------------------------------------- #
# integrity
# --------------------------------------------------------------------------- #
def test_no_dead_links_or_anchors(built):
    _out, stats = built
    assert not stats["dead_links"], "\n".join(stats["dead_links"])


def test_no_vendored_file_is_left_unaccounted(built):
    _out, stats = built
    assert not stats["orphans"], (
        "vendored but routed nowhere (merge it or record it in a source's not_routed):\n"
        + "\n".join(stats["orphans"]))


def test_stale_strip_and_replace_targets_fail_loudly():
    """A declared strip or replace that matches nothing upstream must be an error,
    not a silent no-op: it means the rule shipped is describing a file that moved."""
    with pytest.raises(SystemExit, match="strip_sections names a heading that is not in"):
        bad = json.loads((ONE_SKILL / "sources.json").read_text())
        bad["sources"][0]["skills"][0]["strip_sections"] = ["Section nobody wrote"]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "sources.json"
            p.write_text(json.dumps(bad))
            b.Manifest(p).load()


def test_skill_lists_every_command(built):
    """A procedure is offered only if it is named in the always-loaded file: the
    table is the whole boundary that keeps 'disable-model-invocation' honest."""
    out, _ = built
    text = b.read(out / "SKILL.md")
    for sk in manifest.load():
        if sk.is_command:
            assert f"`{sk.id}`" in text, f"{sk.id} is a command but is not in the command table"


def test_router_reaches_every_populated_bucket(built):
    out, _ = built
    text = b.read(out / "SKILL.md")
    for bid, bucket in manifest.buckets.items():
        fname = Path(bucket["file"]).name
        assert f"references/{fname}" in text, f"router never points at {fname}"
        assert (out / bucket["file"]).exists()


def test_bucket_index_links_resolve(built):
    out, _ = built
    for bucket in manifest.buckets.values():
        p = out / bucket["file"]
        text = b.read(p)
        anchors = {b.slugify(m.group(1)) for m in re.finditer(r"^#{1,6}\s+(.*)$", text, re.M)}
        for target in re.findall(r"\| \[[^\]]*\]\(#([^)]+)\)", text):
            assert target in anchors, f"{p.name}: index link #{target} has no section"


# --------------------------------------------------------------------------- #
# budget and size
# --------------------------------------------------------------------------- #
def test_always_on_file_within_budget(built):
    out, _ = built
    words = len(b.read(out / "SKILL.md").split())
    assert words <= b.ALWAYS_ON_BUDGET, f"SKILL.md is {words} words, budget {b.ALWAYS_ON_BUDGET}"


def test_references_are_indexed(built):
    """Every reference file opens with an index, because a 9k-word file without a
    table of contents is a reason not to read it."""
    out, _ = built
    for bucket in manifest.buckets.values():
        text = b.read(out / bucket["file"])
        assert "| section | from | load |" in text, bucket["file"]
        assert "**Read this when:**" in text


def test_commit_is_clean_and_dist_current():
    r = subprocess.run([sys.executable, str(ONE_SKILL / "build.py"), "check"],
                       cwd=REPO, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


# --------------------------------------------------------------------------- #
# the published copies must be the build's output, not a directory someone forgot
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("target", [
    REPO / ".claude" / "skills" / "one-skill",
    REPO / "claude-skills" / "app" / "one-skill",
])
def test_install_path_matches_dist(target):
    assert target.exists(), f"{target} missing — run `python one-skill/build.py install`"
    for p in sorted(DIST.rglob("*")):
        if p.is_file():
            mirror = target / p.relative_to(DIST)
            assert mirror.exists() and b.read(mirror) == b.read(p), f"stale: {mirror}"


def test_uploaded_zip_matches_dist():
    zip_path = REPO / "claude-skills" / "app" / "zips" / "one-skill.zip"
    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
        assert "one-skill/SKILL.md" in names
        for p in sorted(DIST.rglob("*")):
            if p.is_file():
                assert f"one-skill/{p.relative_to(DIST)}" in names, p.name
        skill_md = z.read("one-skill/SKILL.md").decode()
    assert skill_md == b.read(DIST / "SKILL.md")


def test_paste_file_is_the_router_not_a_monolith():
    """Paste-only models get the router plus a header explaining what is *not*
    pasted. A monolith of everything would defeat the point of the split."""
    paste = REPO / "pseudo-skills" / "one-skill.md"
    text = b.read(paste)
    assert len(text.split()) <= b.ALWAYS_ON_BUDGET + 120, "the paste file grew past the router"
    assert "9 sections" not in text.split("# One Skill")[0]      # no reference bodies inlined + 120
    assert "**Paste-only setup.**" in text


def test_no_legacy_skill_is_still_a_publish_path():
    """`legacy/` is frozen history: it must not be an install target any more."""
    assert not (REPO / ".claude" / "skills" / "caveman-be-brief").exists()
    assert not (REPO / "claude-skills" / "app" / "zips" / "caveman-be-brief.zip").exists()
    assert (REPO / "legacy" / "coding-agents").exists()
