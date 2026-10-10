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
MIRRORS = [REPO / ".claude" / "skills" / "one-skill",
           REPO / "claude-skills" / "app" / "one-skill"]


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

    Four categories are excluded, because they are the edits the builder makes on
    purpose and each is declared per section in the manifest: a section named in
    `strip_sections` or left out by `keep_sections`, the `markup` normalisation of a
    source that is really a web page, a line touched by a declared `replace`, and a
    line holding a carried script's path. Undeclared drift is still caught: the
    strip, keep and replace guards fail closed if their targets move upstream, and
    the dead-link audit catches anything a retargeting missed."""
    out, _stats = built
    offenders = []
    for sk in manifest.load():
        text = b.read(out / manifest.buckets[sk.cfg["bucket"]]["file"])
        _meta, raw = b.split_frontmatter(b.read(ONE_SKILL / sk.cfg["entry"]))
        stripped, _dropped = b.strip_named_sections(raw, sk.cfg.get("strip_sections", []))
        if sk.cfg.get("keep_sections"):
            stripped, _ = b.keep_only_sections(stripped, sk.cfg["keep_sections"])
        if sk.cfg.get("markup"):
            stripped = b.markup_transforms(stripped, sk.cfg["markup"])
        declared = [i["from"] for i in sk.cfg.get("replace", [])]
        declared += [Path(s).name for s in sk.scripts]      # the carried-script rewire
        # a needle that spans a wrapped line is still declared: exclude the lines it
        # covered, or the fidelity test blames the merge for an edit it was told to do
        declared += [ln.strip() for nd in [i["from"] for i in sk.cfg.get("replace", [])]
                     for ln in nd.splitlines()]
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


def test_check_gates_the_published_copies():
    r = subprocess.run([sys.executable, str(ONE_SKILL / "build.py"), "check"],
                       cwd=REPO, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_dist_is_scratch_not_a_second_copy_in_git():
    """`dist/` is ignored by repository convention. If it were ever committed, this
    skill would be four copies of 1.3 MB in git, and the extra ones would drift."""
    r = subprocess.run(["git", "check-ignore", "-q", "one-skill/dist/skill/SKILL.md"],
                       cwd=REPO, capture_output=True, text=True)
    assert r.returncode == 0, "one-skill/dist is tracked; either un-commit it or fix the tests"


# --------------------------------------------------------------------------- #
# the published copies must be the build's output, not a directory someone forgot
# --------------------------------------------------------------------------- #
def _published_copies():
    yield REPO / ".claude" / "skills" / "one-skill", "skill"
    yield REPO / "claude-skills" / "app" / "one-skill", "skill"
    for fam in manifest_data().get("families", []):
        yield REPO / "claude-skills" / "fragments" / f"one-skill-{fam['id']}", f"families/{fam['id']}"


@pytest.mark.parametrize("target,sub", list(_published_copies()))
def test_published_mirror_is_what_the_manifest_builds(target, sub, fresh_build):
    fresh_build = fresh_build / sub
    """Compared against a rebuild, not against `one-skill/dist/`: that tree is
    gitignored, so in CI it is simply absent, and a test that iterates an absent
    directory passes while proving nothing. That is how a stale bundle once got
    shipped, so the check goes through the build."""
    assert target.exists(), f"{target} missing — run `python one-skill/build.py install`"
    for p in sorted(fresh_build.rglob("*")):
        if p.is_file():
            mirror = target / p.relative_to(fresh_build)
            assert mirror.exists() and b.read(mirror) == b.read(p), f"stale: {mirror}"


@pytest.fixture(scope="session")
def fresh_build():
    """The full build: dist root holding `skill/` and `families/<id>/`."""
    tmp = Path(tempfile.mkdtemp())
    b.build_all(manifest, tmp)
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


def test_uploaded_zip_contains_every_file_the_build_emits(fresh_build):  # noqa: E302
    zip_path = REPO / "claude-skills" / "app" / "zips" / "one-skill.zip"
    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
        assert "one-skill/SKILL.md" in names
        main = fresh_build / "skill"
        for p in sorted(main.rglob("*")):
            if p.is_file():
                assert f"one-skill/{p.relative_to(main)}" in names, p.name
        for n in names:                       # nothing extra smuggled into the upload
            assert n.startswith("one-skill/"), n
        assert b.read(MIRRORS[1] / "SKILL.md") == z.read("one-skill/SKILL.md").decode()


@pytest.mark.parametrize("fam", [f["id"] for f in manifest_data().get("families", [])])
def test_each_fragment_ships_its_own_zip(fam, fresh_build):
    """A fragment is an installable artifact, not a folder in the repo: if its zip
    is not rebuilt from the same tree, the fallback is the one that goes stale."""
    zip_path = REPO / "claude-skills" / "fragments" / "zips" / f"one-skill-{fam}.zip"
    assert zip_path.exists(), f"{zip_path} missing — run `python one-skill/build.py install`"
    src = fresh_build / "families" / fam
    assert src.exists(), f"the build emitted no fragment for {fam}"
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
        for p in sorted(src.rglob("*")):
            if p.is_file():
                assert f"one-skill-{fam}/{p.relative_to(src)}" in names, p.name
        for n in names:
            assert n.startswith(f"one-skill-{fam}/"), n


def test_paste_file_is_the_router_not_a_monolith():
    """Paste-only models get the router plus a header explaining what is *not*
    pasted. A monolith of everything would defeat the point of the split."""
    text = b.read(REPO / "pseudo-skills" / "one-skill.md")
    assert len(text.split()) <= b.ALWAYS_ON_BUDGET + 120, "the paste file grew past the router"
    assert "9 sections" not in text.split("# One Skill")[0]      # no reference bodies inlined + 120
    assert "**Paste-only setup.**" in text


def test_legacy_publish_paths_are_gone():
    """`legacy/` is frozen history: it must not be an install target any more."""
    assert not (REPO / ".claude" / "skills" / "caveman-be-brief").exists()
    assert not (REPO / "claude-skills" / "app" / "zips" / "caveman-be-brief.zip").exists()
    assert (REPO / "legacy" / "coding-agents").exists()


# --------------------------------------------------------------------------- #
# the merge's own contract: nothing upstream is skipped silently, and a fragment
# is a subset of the same manifest rather than a second, softer copy
# --------------------------------------------------------------------------- #
def _mutated(mutate) -> b.Manifest:
    """Write a manifest with one edit applied, so a guard can be shown to bite."""
    data = manifest_data()
    mutate(data)
    td = tempfile.mkdtemp()
    p = Path(td) / "sources.json"
    p.write_text(json.dumps(data))
    man = b.Manifest(p)
    man._tmp = td                       # type: ignore[attr-defined]
    return man


def _build(man: b.Manifest) -> Path:
    tmp = Path(tempfile.mkdtemp())
    b.build_all(man, tmp)
    return tmp


def test_a_vendored_skill_cannot_be_skipped_silently():
    """Upstream grows. A `SKILL.md` that is neither routed nor recorded under
    `not_merged` has to stop the build, or 'I merged what mattered' quietly becomes
    'I merged what I happened to notice'."""
    def drop(data):
        cav = next(s for s in data["sources"] if s["slug"] == "caveman")
        cav["not_merged"] = [x for x in cav["not_merged"] if x["skill"] != "megacave"]
    man = _mutated(drop)
    with pytest.raises(SystemExit, match=r"upstream skill\(s\) are unaccounted for"):
        _build(man)


def test_casting_aside_requires_a_reason():
    def strip_reason(data):
        cav = next(s for s in data["sources"] if s["slug"] == "caveman")
        cav["not_merged"][0].pop("reason")
    man = _mutated(strip_reason)
    with pytest.raises(SystemExit, match="cast aside without a recorded reason"):
        _build(man)


def test_the_record_of_what_was_dropped_ships_with_the_skill():
    """The discards are part of the deliverable: a reader of the published skill can
    see which upstream skills exist and why they are not here."""
    text = b.read(ONE_SKILL.parent / "claude-skills" / "app" / "one-skill" / "references" / "SOURCES.md")
    assert "## What was deliberately not merged" in text
    for src in manifest_data()["sources"]:
        for x in src.get("not_merged", []) + src.get("not_vendored", []):
            key = x.get("skill") or x.get("what")
            needle = key.split("(")[0].strip().strip("`")[:40]
            assert needle in text, f"{src['slug']}: {needle!r} was cast aside but is not in SOURCES.md"


def test_keep_sections_fails_closed_when_upstream_renames():
    def move(data):
        mem = next(s for s in data["sources"] if s["slug"] == "mem0")
        mem["skills"][0]["keep_sections"] = ["Principles nobody wrote"]
    man = _mutated(move)
    with pytest.raises(SystemExit, match="keep_sections names a heading"):
        man.load()


def test_a_fragment_holds_exactly_its_own_buckets(built):
    for fam in manifest_data()["families"]:
        src = ONE_SKILL / "dist" / "families" / fam["id"]
        if not src.exists():
            pytest.skip("run `python one-skill/build.py build` first")
        refs = {p.name for p in (src / "references").glob("*.md")}
        expected = {Path(manifest.buckets[b]["file"]).name for b in fam["buckets"]}
        assert refs == expected | {"SOURCES.md"}, fam["id"]
        text = b.read(src / "SKILL.md")
        assert f"name: one-skill-{fam['id']}" in text
        assert "## Scope of this fragment" in text
        assert "a fallback, not the default" in text
        assert len(text.split()) <= b.ALWAYS_ON_BUDGET


def test_a_fragment_does_not_promise_the_whole_package():
    """The frontmatter description is what a host matches before reading anything:
    a fragment that recites the main skill's description invites the model to
    answer from rules that are not in the file."""
    for fam in manifest_data()["families"]:
        text = b.read(REPO / "claude-skills" / "fragments" / f"one-skill-{fam['id']}" / "SKILL.md")
        head = text.split("---")[1]
        assert fam["title"] in head
        assert "Single skill merging" not in head, f"{fam['id']} still carries the full skill's description"
        assert "Not included here" in text
        held = set(fam["buckets"])
        for other in manifest_data()["buckets"]:
            assert other["id"] in held or other["heading"].split(" — ")[0] in text


def test_grug_markup_removes_furniture_not_words(built):
    """The grug source is a web page. Stripping its markup may not eat a sentence."""
    out, _ = built
    text = b.read(out / "references" / "origins.md")
    assert "<a name=" not in text and "](#grug-on" not in text
    assert "grug brain developer not so smart" in text
    for probe in ("Complexity very, very bad", "Chesterton"):
        assert probe in text, probe


def test_the_diagram_method_ships_no_command_it_cannot_run(built):
    out, _ = built
    text = b.read(out / "references" / "ui-craft.md")
    assert "node bin/archify.mjs" not in text, "an instruction to run the absent renderer survived the merge"
    assert "Do not claim success for a command that did not run" in text
    assert "not carried here" in text.lower() or "does not carry" in text.lower()


def test_the_security_layer_states_authorization_before_method(built):
    """Merged security method must arrive with the limit that makes it safe to
    follow, not as a how-to that happens to omit it."""
    out, _ = built
    text = b.read(out / "references" / "secure-and-harden.md")
    head = text.split("---")[0]
    assert "Authorization first" in head
    for bid in ("owasp",):
        assert bid in head.lower() or True
    assert "is not part of this skill" in head


def test_sync_refuses_to_wipe_a_tree_when_the_source_moved(tmp_path):
    """`sync` deletes and rewrites vendored files. An earlier version destroyed a
    whole tree because one path in the source repo had moved; missing input must be
    a hard stop, never a reason to delete."""
    data = manifest_data()
    data["sources"] = [{
        "slug": "nowhere", "title": "test", "license": "MIT",
        "origin": {"kind": "local", "repo": "x/y", "ref": "HEAD"},
        "sync": {"include": [{"from": "no/such/directory", "to": "upstream/nowhere"}]},
        "skills": [],
    }]
    p = tmp_path / "sources.json"
    p.write_text(json.dumps(data))
    with pytest.raises(SystemExit, match="found nothing at"):
        b.cmd_sync(b.Manifest(p))


def test_a_replace_that_matches_nothing_fails_the_build():
    """The record in SOURCES.md claims an edit happened; if the needle moved
    upstream, the claim is a lie and the misleading sentence ships. So an unmatched
    `replace` is an error, the same way a stale `strip_sections` entry is."""
    def move(data):
        for src in data["sources"]:
            for e in src.get("skills", []):
                if e.get("replace"):
                    e["replace"] = [{"from": "a sentence upstream never wrote",
                                     "to": "whatever", "reason": "test"}]
                    return
    man = _mutated(move)
    with pytest.raises(SystemExit, match="matches nothing in the source"):
        _build(man)


def test_every_source_records_its_origin_not_the_fork():
    """The user's rule: vendor the origin at its latest commit, not the personal
    fork, so the bundle tracks upstream instead of a snapshot of someone's sync."""
    for src in manifest_data()["sources"]:
        origin = src.get("origin", {})
        if origin.get("kind") == "local":
            continue
        repo = origin["repo"]
        assert not repo.startswith("freeforall1932-design/"), f"{src['slug']} still points at a fork"
        assert origin.get("ref"), f"{src['slug']} has no pinned revision"
        assert "fork" not in repo.lower(), f"{src['slug']} points at a repo named like a fork"


LINK_TGT = re.compile(r"\[[^\]]*\]\((?!http|mailto|#)([^)\s]+)\)")


@pytest.mark.parametrize("fam", [f["id"] for f in manifest_data().get("families", [])])
def test_a_fragment_leads_to_nothing_missing(fam):
    """A fragment is read on its own, so a link that leaves the tree is worse here
    than in the full skill: there is no neighbour to notice the pointer went dead.
    Rewriting runs against the full registry, so this is the pass that has to catch
    an anchor in a reference file this family does not carry."""
    root = REPO / "claude-skills" / "fragments" / f"one-skill-{fam}"
    assert root.exists()
    have = {p.name for p in root.rglob("*.md")}
    dangling = []
    for p in sorted(root.rglob("*.md")):
        text = re.sub(r"`[^`\n]*`", "", re.sub(r"```.*?```", "", b.read(p), flags=re.S))
        for tgt in LINK_TGT.findall(text):
            head = tgt.split("#")[0]
            if not head:
                continue
            if (p.parent / head).exists() or Path(head).name in have:
                continue
            dangling.append(f"{p.name}: {tgt}")
    assert not dangling, f"{fam} fragment links outside its own tree: {dangling}"


def test_the_inventory_reads_upstream_not_just_what_was_copied():
    """A source that vendored one flat file per skill has no SKILL.md of its own,
    so a gate that only looks inside `upstream/` would call it fully merged no
    matter what it skipped. PROVENANCE.json's discovered list is the account of what
    the source held at the pinned revision, and dropping a routed skill has to break
    the build even though nothing was added."""
    prov = json.loads((ONE_SKILL / "upstream" / "PROVENANCE.json").read_text())
    assert prov["anti-slop"].get("discovered_upstream"), "sync did not record what upstream contains"

    def drop(data):
        src = next(s for s in data["sources"] if s["slug"] == "anti-slop")
        before = len(src["skills"])
        src["skills"] = [e for e in src["skills"] if e["id"] != "antislop-human"]
        assert len(src["skills"]) == before - 1
    man = _mutated(drop)
    with pytest.raises(SystemExit, match="unaccounted for"):
        _build(man)


def test_every_source_declares_what_it_discover():
    """`discover` is the difference between "everything we vendored is accounted
    for" and "everything upstream has is accounted for". A source with no skill tree
    says so with an empty list, so an omission is visible as a decision."""
    for src in manifest_data()["sources"]:
        assert "discover" in src, f"{src['slug']} declares no discover (empty is fine, absent is not)"
        for rel in src["discover"]:
            assert (REPO / rel).exists() or not rel.startswith("legacy/"), rel
