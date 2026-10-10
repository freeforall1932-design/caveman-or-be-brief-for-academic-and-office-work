# Session handoff

Written 2026-10-10, updated the same day for the second round of sources. Branch
`arena/b5b2025d-skills-repo`. State: the repository publishes **one** skill, built
from **69 skills across eight sources**, plus three generated fragment fallbacks; the
six-skill era is frozen under `legacy/`.

## What exists now

| Path | Role |
|---|---|
| `one-skill/sources.json` | ★ the manifest: sources → skills → buckets, plus `families` and each source's `not_merged` / `not_vendored` / `not_routed` records. The only file to edit to add a source. |
| `one-skill/build.py` | `sync` · `build` · `install` · `all` · `check` |
| `one-skill/core/` | six hand-written files: the merge's judgement (layers, precedence, always-on, router, commands, provenance) |
| `one-skill/upstream/` | vendored inputs, revision-pinned in `PROVENANCE.json`. `local/` reads this repo's working tree (`legacy/`), not a clone. |
| `one-skill/dist/skill/`, `dist/families/*/` | scratch build output — gitignored, so it does not exist in CI. The published skill is the mirrors below. |
| `.claude/skills/one-skill/`, `claude-skills/app/one-skill/`, `claude-skills/app/zips/one-skill.zip`, `pseudo-skills/one-skill.md` | mirrors written by `install`. Never hand-edit. |
| `claude-skills/fragments/one-skill-{prose,code,design}/` + `fragments/zips/*.zip` | the fallback skills, same rules / subset of references. Also mirrors, also never hand-edited. |
| `skillopt-integration/` | unchanged: trains the four **register** documents, which are now in `legacy/` |
| `legacy/` | `coding-agents/` (variants, profiles, packs, `compile.py`, philosophy), `caveman-universal/`, old `claude-skills/` trees + old install guide, old `pseudo-skills/`, `claude-reasoning-caveman.skill` |

Sources: this repo (`legacy/`, 12 skills), `miqdadbadjuber/anti-slop` (6),
`mattpocock/skills` (31), `JuliusBrussee/caveman` v3.2.0 (13),
`bigskysoftware/grugbrain.dev` (1 — the whole site text), `usestrix/strix` (4 of 9),
`mem0ai/mem0` (1 of 6), `tt-a1i/archify` (1 of 2). **21 skills are cast aside with a
written reason**, and `inventory()` fails the build if a vendored `SKILL.md` ends up
neither routed nor excused, so that list cannot rot silently when upstream grows.
Also not merged, on the record: `mattpocock/skills` `in-progress/` (betas) and
`deprecated/` (empty upstream).

## Commands

Run from the **repo root**. `build` and `check` are offline; only `sync` may reach
the network, to clone a source it does not have.

```bash
python3 one-skill/build.py all         # rebuild the skill + every mirror + every zip
python3 one-skill/build.py check       # fail if any published copy is not what the manifest builds
python3 -m pytest one-skill/tests -q   # 48 tests: fidelity, links, budget, gates, mirrors
python3 one-skill/build.py sync        # re-vendor upstream (needs network for a first clone)
python3 -m pytest skillopt-integration/tests -q
```

Score a prediction set without SkillOpt installed:

```bash
python -m caveman_skillopt.score \
  --split-dir skillopt-integration/data/caveman_brief_split \
  --split test \
  --predictions skillopt-integration/examples/predictions-good.json \
  --show-violations
```

Reference baseline on the 9-item test split: **0.9784**, 100% hard pass. Naive echo:
**0.6379**, 0% hard pass. Those numbers belong to the register documents; the merge
did not re-measure them and the README says so.

Legacy, frozen but runnable: `python3 legacy/coding-agents/compile.py` and
`pytest legacy/coding-agents/tests -q`. CI no longer runs them (see the comment at
the bottom of `.github/workflows/tests.yml`).

## Standing constraints

From the user, explicitly. Do not reverse them without asking.

- **One skill, generated from a manifest.** New sources are added by editing
  `sources.json` and rebuilding — the user said this is where the project is going,
  so a hand-merged bundle is the wrong shape.
- **One unified skill is the deliverable while it holds.** It holds: eleven reference
  files, `SKILL.md` still 2.4k words. Fragility is answered by **adding** generated
  fragments as a fallback, not by replacing the main skill or splitting it.
- **Only take what works; cast aside what is not implementable — on the record.** A
  skill whose instructions are "run this binary", "fetch these docs" or "install this
  package" is not capability in a markdown file. `not_merged` + the inventory gate are
  how that decision is kept auditable.
- **Vendor from the origin repo at its latest commit, not from the user's fork.**
  `anti-slop`, `strix`, `mem0` and `archify` all point at their upstream now; the
  anti-slop fork was verified byte-identical before the switch.
- **Replace, do not parallel.** The old skill sets are not install paths any more;
  they live in `legacy/` and nothing new is written into them.
- **Scope for Pocock's skills:** engineering + productivity + misc. Not `in-progress`.
- **Layer the sources by destination** rather than picking a winner or averaging
  them. That is the whole design of `core/10-precedence.md`.
- **Never vendor the SkillOpt fork.** Install via pip.
- **Keep the plain-`.md` paste fallback.** It is the only route that works where
  there is no skill uploader. It ships the router half only; there is no monolith
  export, deliberately.
- **Carry the real upstream text**, not a paraphrase — including grug's own site text
  and caveman v3.2.0, which replaced this repo's v2.x-era copy.
- **English + Indonesian only, no CLI.**

## Work list

1. **Train the merged bundle.** SkillOpt still targets the four register documents
   under `legacy/`. Wiring the merge means: write `best_skill.md` over the vendored
   copy in `one-skill/upstream/local/`, repoint that skill's `entry`, rebuild.
   Decide first whether per-register scoring survives a single document, or the
   gate quietly averages the conflict away — which is what the four-variant split
   exists to prevent.
2. **Fix CodeQL — the one red check, pre-existing.** `codeql.yml` is the unmodified
   GitHub template with an **empty** `strategy.matrix.include`, so zero jobs run and
   GitHub marks it failed. Broken on `main` since 2026-08-19, not a regression here.
   Fix: `- language: python` with `build-mode: none`; consider `actions` for the
   workflow files. Verify by watching a run.
3. **`scripts/` name collisions.** `build.py` keeps the first script it sees per
   basename and skips later duplicates silently. Namespaced paths or a hard fail is
   needed before another source ships a `contrast-check.py` of its own.
4. **Compare `BUILD.json` checksums on build.** It stores a checksum per input, but
   nothing compares it against the vendored file's current bytes after a `sync`, so a
   hand-edit inside `upstream/` survives one build unnoticed. The manifest hash is
   checked; the files are not.
5. **The fragments are new; watch how they are used.** Three families
   (`prose`, `code`, `design`) built from the same manifest. Open questions: whether
   `origins` belongs in `prose` only (it is the "why" layer, and `code` may want it);
   whether a `secure`-only fragment is worth a fourth zip; whether `check` should
   assert fragment *budgets* separately (it compares bytes, and each fragment is
   already under `ALWAYS_ON_BUDGET`).
6. **Verify the three unverified agent profiles** (Cursor, Copilot, OpenCode are
   `tested_agent_version: "unverified"`, documentation review only). Needs those
   tools installed; the validator refuses a version claim it never tested.
7. **Run an actual SkillOpt training loop.** Never executed end to end (needs a real
   API key); `train` failing at `get_target_client()` with a dummy key is expected.
8. **Determine Qwen Chat Agent's real conventions** — whether it parses `SKILL.md`
   frontmatter is unknown; if tested, upgrade `profiles/qwen-agent.json` and drop
   `skills: null`.
9. **Re-check upstreams periodically, then `sync` + rebuild.** caveman v3.2.0,
   grugbrain.dev `b1b1ca8`, strix `62b4964`, mem0 `b7ad69a`, archify `54edef4`,
   anti-slop `388cbe3`, mattpocock `49dd158` are the pins as of 2026-10-10. If a
   release renames a section, the strips/keeps/replaces go stale — and the build now
   fails loudly instead of shipping a dead rule.
10. **ZIP ceiling.** 229 KiB for the main skill (fragments: 48–115 KiB). If the app
    upload limit becomes a problem, trim `references/`, never the router.

## Gotchas

- **Every install mirror is generated; `one-skill/dist/` is scratch and gitignored.**
  Hand-edits revert on the next build, and `build.py check` plus
  `test_published_mirror_is_what_the_manifest_builds` fail the PR — for the two main
  mirrors, the paste file, the zip and all three fragments. Change `core/` or
  `sources.json`.
- **`build.py sync` deletes and rewrites `upstream/`.** It used to do that even when
  the source path was missing: a `git mv` in this repo made the clone's pinned ref
  (the pre-move commit) lack `legacy/`, sync copied 0 files, and the tree it was
  supposed to refresh was already gone. Now a missing include is a hard stop and
  `sync` never deletes. If `upstream/` ever looks thin, `git checkout -- one-skill/upstream`.
- **`local` must use `origin.kind: "local"`.** Cloning this repository fetches the
  default branch, where `legacy/` does not exist; the working tree is the only place
  that has it.
- **A skill that tells the agent to fetch files is a defect in a merged skill.**
  antislop's first-run wizard does exactly that, so it is stripped. Same for
  instructions to run a CLI, install a package, or delegate to another published
  skill — which is why Strix, mem0 and Archify arrived as 6 sections out of 17 skills.
- **Bare filenames must not be rewritten.** `legacy/coding-agents` prose says "copy
  `block-dangerous-git.sh` to `.claude/hooks/…`" — the filename there is a
  *destination*. Rewriting prose mentions of a carried script corrupted it; only
  `${CLAUDE_SKILL_DIR}/name` and `./name` runtime paths are rewired now.
- **Links the builder itself created must resolve.** The audit ignores upstream prose
  about files that were never part of this bundle, but a target starting with
  `references/` is ours and a dead one fails the build. It caught a `diagrams` doc
  pointing at Archify's uncarried `delivery-contract.md`.
- **The audit skips code spans.** `SOURCES.md` quotes the exact text it replaced, so a
  link inside backticks is an example of a link, not one. Without that, recording an
  edit looks like a broken link.
- **Verbatim ≠ inert.** `replace` exists for the cases where carrying text exactly
  would make the skill lie about its own layout ("run `node bin/archify.mjs`",
  "re-run Strix", "see `delivery-contract.md`"). Every substitution is recorded in
  `references/SOURCES.md`, and **a needle that no longer matches fails the build** —
  that guard caught three of my own guesses, so it is not theoretical.
- **`keep_sections` is for tool-coupled sources, not for taste.** It keeps named H2
  sections and drops the rest *by name*. If you find yourself keeping a section
  because its prose is nicer, delete the entry and put the judgement in the note.
- **`markup` may remove only markup.** The grug source is a generated page whose
  headings wrap themselves in anchors; the transforms drop HTML lines and unwrap those
  headings. The fidelity test asserts grug's sentences still appear verbatim.
- **`ALWAYS_ON_BUDGET = 2400` words, enforced inside `assemble`.** `SKILL.md` is
  billed on every request, so this round paid for two new router rows and a
  nine-row provenance table by *moving* the table into `references/SOURCES.md`,
  adding licenses to each reference head instead, and shortening the open paragraph.
  It is now 2398. Adding a bucket costs ~30 words; find the cut first.
- **Bucket = destination, not origin.** Add a bucket only for a genuinely new kind of
  output. `diagrams` was created for Archify and deleted in the same session: 410
  words of reference material do not pay for a router row, and the anti-slop filter
  asks diagrams the same question it asks interfaces.
- **`build.py check` compares against the mirrors, never `dist/`.** `dist/` is
  gitignored, so it is absent in CI, and a gate that walks an absent tree passes while
  proving nothing — that is how a stale bundle got one red run. Both the gate and the
  mirror test rebuild from the manifest, and both were proven to bite by hand-editing
  a mirror and watching them fail.
- **`main` is a function name; do not shadow it in a comprehension.** `cmd_check`
  briefly bound `main` as its loop variable and reported "free variable … not
  associated with a value". Loop targets are `main_tree`/`src` now, deliberately
  named: an earlier version compared the paste file against whichever *fragment*
  happened to be last in the list.
- **`build.py sync` must run from the repo root** (`python3 one-skill/build.py sync`),
  same as the legacy `compile.py` before it.
- **PEP 668.** System-wide `pip install` fails with `externally-managed-environment`.
  Use a venv.
- **No pyyaml in this environment.** That is why the manifest is JSON and the parser in
  `build.py` is a hand-rolled frontmatter subset (scalars, block scalars, inline lists)
  rather than `yaml.safe_load`.
- **Pack reproducibility (legacy).** `legacy/coding-agents/compile.py` writes `ZipInfo`
  with a fixed timestamp so its archive is byte-reproducible. `build.py install` does not
  yet: `zipfile` records mtimes, so no zip is bit-stable across rebuilds. They are not
  CI-gated on content, only on the trees that produced them.
- **`one-skill/.cache/` is scratch clones** (gitignored, and it inflates `du` to ~5 MB).
  `rm -rf one-skill/.cache` before measuring the tree.
- **Lazy imports are load-bearing** in `caveman_skillopt` — they keep the offline
  scorer working with SkillOpt absent. Do not add eager imports back.

## Known trade-offs

- The evaluator's `contains_span` uses a conservative stem fallback (min 4-char stem)
  so "delays"→"delayed" is not scored as a lost fact; it errs toward recall.
- `INVENTED_ABBREV_RE` is narrowed to the official set `cfg|impl|req|res|fn`, because
  it false-positived on "auth", "res", "diff", "doc".
- Code-assist items can never reach 0.5 compression — byte-exact code is
  uncompressible — so the target is clamped to 0.30 for those items.
- The identity copy used to pass the hard gate (a degenerate optimum);
  `no_compression_or_grew` blocks it.
- **Duplication is accepted inside the bundle, not eliminated.** `be-brief-output` and
  `caveman-be-brief-app` overlap by design (agent-facing vs app-facing wording), and
  two more pairs arrived with the origin syncs: grug appears as the site's full text
  *and* the short variant's operational rules, and the six work patterns exist as the
  always-on table *and* as upstream's own verb skills. Cutting to a single copy of
  every rule would mean deciding which author's phrasing survives — which is the
  paraphrase the verbatim rule exists to prevent. Where a section is a true duplicate
  of another *file*, it is not routed at all and is listed under `not_routed` with the
  reason (that is what happened to this repo's v2.x caveman copy).
- **87k words of references is a lot of skill.** The counterweight is the router and
  the "one reference at a time" rule; if that rule is not honoured in practice, the
  answer is the fragments, then fewer sources merged — never a longer `SKILL.md`.
- **The security layer is method, not a scanner.** It says which OWASP categories an
  agent-driven review can and cannot prove and how to report honestly; it carries no
  exploitation capability and its reference file opens with the authorization rule.
  If a user wants actual scanning, the answer is Strix itself, in their repo.
