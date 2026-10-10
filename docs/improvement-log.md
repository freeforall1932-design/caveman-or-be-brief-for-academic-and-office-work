# Improvement log

Chronicles substantive changes and the reasoning behind them. Entries are
dated; newest first.

## 2026-10-10 — one skill: three repositories merged behind a manifest

**Change:** every skill in this repo, plus
[freeforall1932-design/anti-slop-fork](https://github.com/freeforall1932-design/anti-slop-fork)
(6 skills) and
[mattpocock/skills](https://github.com/mattpocock/skills) (31 skills: engineering,
productivity, misc), is merged into a single skill at `one-skill/dist/skill/`, built
by `one-skill/build.py` from a `one-skill/sources.json` manifest. 50 upstream skills
landed in 10 reference files (75k words) behind a 2.4k-word `SKILL.md`. The previous
skill sets moved to `legacy/`, and `.claude/skills/`, `claude-skills/app/`,
`claude-skills/app/zips/` and `pseudo-skills/` now carry only `one-skill`. CI's
pack-building job was replaced by a merge job (`pytest one-skill/tests` +
`build.py check` + an offline-reproducibility gate).

**Why generated rather than hand-merged:** the ask is to keep adding sources. A
hand-written merge means the fourth repository is another 300 files to reconcile by
eye; a manifest makes it one entry and a rebuild. Router table, command table,
per-bucket indexes, provenance and counts all regenerate.

**Why verbatim rather than rewritten:** four of these sources contradict each other
on the same sentence (caveman: *fragments OK*; be-brief: *never broken grammar*;
antislop: *liveliness is added*; Pocock: *ask before you build*). Paraphrasing them
into agreement is how a merge destroys the thing each author was protecting, and
this repo already had the right precedent — the four variants quoted upstream rather
than summarising it. So bodies are carried as written, and the reconciliation lives
in `core/10-precedence.md` as *rulings by destination*, with the argument one hop
away in `references/origins.md` (which carries the old `philosophy/conflicts.md`
verbatim).

**Two escape hatches, both fail-closed.** `strip_sections` drops an upstream
section that only makes sense for a standalone install — antislop's first-run wizard
literally tells the agent to fetch files and edit an entry file, which a merged skill
must never do. `replace` makes a literal wording edit where verbatim carriage would
otherwise make the skill lie about its own layout ("the script sits next to this
`SKILL.md`"). Both are recorded per section in `references/SOURCES.md`, and both
**fail the build** when their target string no longer exists upstream: a strip that
silently stopped matching is a rule shipping on a file that moved. The first run
caught a stale strip I had over-declared, and the second caught a needle I had
guessed instead of read — which is the argument for the guard existing.

**Why an always-loaded budget.** `SKILL.md` rides in every request, so bloat there is
taxed on every turn. `ALWAYS_ON_BUDGET = 2400` words, enforced by the build. It
forced real cuts (the eight named rulings lost their prose but not their verdicts,
and one duplicated rule in `always-on` was deleted rather than restated). Getting
from the first draft's 2912 words to 2373 was mostly removing duplication between
the merge layer and the buckets.

**Why buckets are destinations, not origins.** Two skills from different repos that
govern the same output sit adjacent in one reference file. That is where a
contradiction is visible to a reader; sorting by repo hides it in two places at once.

**What is deliberately not merged:** `mattpocock/skills/in-progress/` (betas, no docs
pages, "can change or disappear without warning") and `skills/deprecated/` (empty by
upstream policy). Recorded in the manifest, not silently dropped.

**Kept honest about size:** a 50-skill package is heavy, and a merged skill that
loads all 75k words would cost more context than the writing saves. Hence the split:
one always-loaded file, ten on-demand references, and a paste path for models with no
uploader that ships the router alone. Also hence the decision *not* to build a
monolith export, and to say so in `pseudo-skills/one-skill.md`.

**Follow-ups, in order of value:**
1. Train the merged bundle with SkillOpt as one document (today the trainer still
   targets the four register documents in `legacy/`). The wiring is one manifest
   `entry` pointing at a `best_skill.md`; the reward function already scores per
   register, so decide whether that gate survives the merge.
2. `build.py sync` could record upstream file hashes in `BUILD.json` *and* verify
   them, so a re-vendored file that changed underneath a hand-edit is caught.
3. `scripts/` is shared across buckets: if a future source ships a script with a
   colliding basename, the build silently keeps the first. Namespace or fail.
4. The ZIP is 194 KiB. If the app surface has an upload ceiling, the fix is trimming
   `references/`, not the router.

## 2026-09-17 — CI: pin SkillOpt, make the integration job blocking

**Change:** `skillopt-integration` CI job went from
`continue-on-error: true` + `pip install skillopt` to
`continue-on-error: ${{ github.event_name == 'schedule' }}` +
`pip install skillopt==0.2.0`, with a weekly `schedule` trigger that installs
latest instead.

**Why:** the previous configuration was the worst of both worlds — un-pinned, so
not reproducible, *and* non-blocking, so not a gate. An un-pinned blocking job
would be worse (upstream publishes, this repo's CI turns red on unrelated PRs).
Pinning is what makes blocking safe: with the version fixed, the job is
deterministic, so a failure means *this* repo broke it.

**Why not just drop the job:** it covers the tests that
`pytest.importorskip("skillopt")` skips in the no-SkillOpt job — the dataloader
and adapter paths. That is the part of the integration layer most likely to
drift against upstream.

**Why the weekly un-pinned run:** pinning alone means silently testing against
an old version forever. The scheduled run installs latest and is allowed to
fail, so upstream breaking changes surface on their own schedule and get a
deliberate pin bump rather than an emergency.

**Verified:** clean-room venv on Python 3.11, `skillopt==0.2.0` from PyPI,
39 passed. 0.2.0 is simultaneously the latest on PyPI and the version the whole
integration was developed against, so pinning introduced zero drift.

## 2026-09-17 — variants became real skills, not instruction documents

**Change:** `variants/*.md` (four flat files) → `variants/<name>/SKILL.md` +
`references/` + `examples.md`.

**Why:** an outside review judged the flat files "more like just text
instruction than an actual skill," and that was correct. Against the Agent
Skills spec they were missing:

| Requirement | Before | After |
|---|---|---|
| Progressive disclosure | one flat file, everything always loaded | `SKILL.md` + `references/`, one level deep |
| Optional frontmatter fields | none | `metadata`; `disallowed-tools` on grug |
| Description discipline | approximate | third person, states *what* and *when*, triggers front-loaded, ≤1024 chars |
| Workflow with feedback loop | absent | numbered flow + self-check checklist |
| Worked examples | absent from the skills | `examples.md` per variant |
| Evals | existed, never linked | `metadata.evaluation` points at `skillopt-integration/` |

**The two that mattered most.** Feedback loops turn rules the model follows into
rules it audits itself against — each variant now ends in a self-check ("every
number survived? every hedge survived? code byte-identical?") with instructions
to fix silently rather than announce. Progressive disclosure means the agent
sees SKILL.md and pulls `references/cut-lists.md` only when it is actually
cutting.

**Consequence for packaging:** the paste route now *flattens* the same content
into one self-contained file, because a pasted file has no filesystem beside it
and relative links to `references/` would be dead on arrival. Cursor `.mdc` does
the same, being a single-file format. A test asserts no `](../../` links survive
into packs, where they would resolve to nothing.

**Deliberate omissions:** no `scripts/` or `assets/` — there is nothing
genuinely executable here, and adding one to tick a spec box would be
cargo-culting. `disallowed-tools` appears only on `grug-reasoning`, a reasoning
layer that should not be writing files; the output variants need unrestricted
access.

## 2026-09-17 — Qwen split into two profiles

**Change:** added `profiles/qwen-agent.json` (Qwen Chat agent) alongside
`profiles/qwen.json` (Qwen Code CLI). Added `web-workspace` as a wire protocol
and `upload` as an instruction method; `compile.py` now requires
`instruction.paste_dir` for such agents instead of config paths.

**Why:** these are different products. Qwen Code is a terminal CLI with a config
directory. The Qwen Chat agent is a hosted agent with an uploadable workspace,
no CLI, and no config directory. One profile could not describe both honestly.

**Correction made:** the Qwen Code profile pinned `0.22.3`, inherited from the
official caveman profile registry. Checked on 2026-09-17 and corrected to
`0.24.0`: npm `@qwen-code/qwen-code` `dist-tags.latest` = 0.24.0 published
2026-09-16, GitHub release v0.24.0 published 2026-09-16, repo last pushed
2026-09-17, ~27.9k stars, not archived. Note the npm package is
`@qwen-code/qwen-code` — a package named `qwen-coder` does not exist, which is
a plausible source of an "it was abandoned" impression.

**Honesty constraint preserved:** the Chat agent's `SKILL.md` handling is
genuinely unknown, so the profile sets `skills: null` rather than guessing, and
its pack ships plain `.md` with no frontmatter. That is why the pseudo-skill
fallback must stay.

## 2026-09-17 — CI added, zip made reproducible

**Change:** `.github/workflows/tests.yml` with three jobs. Made `compile.py`
write `ZipInfo` with a fixed timestamp.

**Why:** the stale-packs gate (`compile`, then `git diff --exit-code`) is only
meaningful if compilation is deterministic. The first attempt embedded file
mtimes, so every run produced a different zip and the gate failed on noise.
Verified reproducible by hashing two independent runs.

The SkillOpt job installs only `skillopt-integration` (not `skillopt`) and still
exercises the reward function, because the scorer was made dependency-free —
see below.

## 2026-09-17 — offline scorer made dependency-free

**Change:** extracted `normalise_item` into
`caveman_skillopt/envs/caveman_brief/schema.py`; made the package and env
`__init__.py` resolve SkillOpt-dependent modules lazily via `__getattr__`.

**Why:** the reward function is useful as a plain linter, without the training
framework. Took three attempts — the package `__init__`, then the env
`__init__`, then `score.py` itself each imported SkillOpt transitively. Result:
23 passed / 2 skipped with SkillOpt absent, 39 passed with it installed.

## Earlier in the session — evaluator correctness fixes

Each of these was a real bug found by testing, not a stylistic change.

- `contains_number` flagged `1240` as lost when the output wrote `1,240` — strip
  thousands separators on both sides.
- `contains_span` called "delays"→"delayed" a lost fact — added a conservative
  stem fallback (min 4-char stem), erring toward recall.
- Caveman fragments scored register fidelity 1.0 under `be_brief` — added
  `_BARE_VERB_RE` to catch bare-verb fragments like "check use".
- The identity copy passed the hard gate (a degenerate optimum) — added
  `no_compression_or_grew` as a blocking violation.
- Code-assist items could never reach 0.5 compression, since byte-exact code is
  uncompressible — target clamped via `_adjust_target_for_code` to
  `min(target, 0.30)`.
- `INVENTED_ABBREV_RE` false-positived on "auth", "res", "diff", "doc" —
  narrowed to the official set `cfg|impl|req|res|fn`.
- Cursor `.mdc` generation emitted an unquoted YAML scalar containing `": "`,
  which made the entire frontmatter unparseable so Cursor silently ignored the
  rule — fixed with `_yaml_scalar()` (double-quote + escape).
