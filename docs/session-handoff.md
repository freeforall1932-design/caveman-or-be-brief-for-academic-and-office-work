# Session handoff

Written 2026-10-10. Branch `arena/b5b2025d-skills-repo`. State: the repository
publishes **one** skill, built from fifty across three repos; the six-skill era is
frozen under `legacy/`.

## What exists now

| Path | Role |
|---|---|
| `one-skill/sources.json` | ★ the manifest: which sources, which skills, which bucket. The only file to edit to add a source. |
| `one-skill/build.py` | `sync` · `build` · `install` · `all` · `check` |
| `one-skill/core/` | six hand-written files: the merge's judgement (layers, precedence, always-on, router, commands, provenance) |
| `one-skill/upstream/` | vendored inputs, revision-pinned in `PROVENANCE.json`. `local/` now reads from `legacy/`. |
| `one-skill/dist/skill/` | ★ the single skill: `SKILL.md` (2373 words) + 10 references (75k words) + `scripts/` + `BUILD.json` |
| `.claude/skills/one-skill/`, `claude-skills/app/one-skill/`, `claude-skills/app/zips/one-skill.zip`, `pseudo-skills/one-skill.md` | mirrors written by `install`. Never hand-edit. |
| `skillopt-integration/` | unchanged: trains the four **register** documents, which are now in `legacy/` |
| `legacy/` | `coding-agents/` (variants, profiles, packs, `compile.py`, philosophy), `caveman-universal/`, old `claude-skills/` trees + old install guide, old `pseudo-skills/`, `claude-reasoning-caveman.skill` |

50 skills merged. Not merged, on the record: `mattpocock/skills` `in-progress/`
(betas) and `deprecated/` (empty upstream).

## Commands

Run from the **repo root**. `build` and `check` are offline; only `sync` may reach
the network, to clone a source it does not have.

```bash
python3 one-skill/build.py all         # rebuild the skill + every install mirror + the zip
python3 one-skill/build.py check       # fail if dist/ is stale or the build is not reproducible
python3 -m pytest one-skill/tests -q   # 24 tests: fidelity, links, budget, determinism, mirrors
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

Reference baseline on the 9-item test split: **0.9784**, 100% hard pass. Naive
echo: **0.6379**, 0% hard pass. Those numbers belong to the register documents; the
merge did not re-measure them and the README says so.

Legacy, frozen but runnable: `python3 legacy/coding-agents/compile.py` and
`pytest legacy/coding-agents/tests -q`. CI no longer runs them (see the comment at
the bottom of `.github/workflows/tests.yml`).

## Standing constraints

From the user, explicitly. Do not reverse them without asking.

- **One skill, generated from a manifest.** New sources are added by editing
  `sources.json` and rebuilding — the user said this is where the project is going,
  so a hand-merged bundle is the wrong shape.
- **Replace, do not parallel.** The old skill sets are not install paths any more;
  they live in `legacy/` and nothing new is written into them.
- **Scope for Pocock's skills:** engineering + productivity + misc. Not `in-progress`.
- **Layer the sources by destination** rather than picking a winner or averaging
  them. That is the whole design of `core/10-precedence.md`.
- **Never vendor the SkillOpt fork.** Install via pip.
- **Keep the plain-`.md` paste fallback.** It is the only route that works where
  there is no skill uploader. It ships the router half only; there is no monolith
  export, deliberately.
- **Carry the real upstream text**, not a paraphrase: grugbrain.dev,
  JuliusBrussee/caveman, anti-slop-fork, mattpocock/skills.
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
   needed before a fifth source ships a `contrast-check.py` of its own.
4. **Verify hashes on re-sync.** `BUILD.json` stores a checksum per input, but
   nothing compares it against the vendored file's current bytes after a `sync`, so
   a hand-edit inside `upstream/` survives one build unnoticed.
5. **Verify the three unverified agent profiles** (Cursor, Copilot, OpenCode are
   `tested_agent_version: "unverified"`, documentation review only). Needs those
   tools installed; the validator refuses a version claim it never tested.
6. **Run an actual SkillOpt training loop.** Never executed end to end (needs a real
   API key); `train` failing at `get_target_client()` with a dummy key is expected.
7. **Determine Qwen Chat Agent's real conventions** — whether it parses `SKILL.md`
   frontmatter is unknown; if tested, upgrade `profiles/qwen-agent.json` and drop
   `skills: null`.
8. **Re-check upstream caveman and antislop**, then `sync` + rebuild. If a release
   changed the non-negotiables (invented abbreviations, arrows in prose,
   auto-clarity) or antislop's rule numbering, the strips and replaces in the
   manifest go stale — and the build will now say so instead of shipping them.
9. **ZIP ceiling.** 194 KiB today. If the app upload limit becomes a problem, trim
   `references/`, never the router.

## Gotchas

- **Everything under `one-skill/dist/` and every install mirror is generated.**
  Hand-edits revert on the next build, and `build.py check` plus
  `test_install_path_matches_dist` fail the PR. Change `core/` or `sources.json`.
- **A skill that tells the agent to fetch files is a defect in a merged skill.**
  antislop's first-run wizard does exactly that, so it is stripped — the reason
  `strip_sections` exists. Same for instructions to edit an entry file.
- **Bare filenames must not be rewritten.** `legacy/coding-agents` prose says "copy
  `block-dangerous-git.sh` to `.claude/hooks/…`" — the filename there is a
  *destination*. Rewriting prose mentions of a carried script corrupted it; only
  `${CLAUDE_SKILL_DIR}/name` and `./name` runtime paths are rewired now.
- **Verbatim ≠ inert.** `replace` exists for the cases where carrying text exactly
  would make the skill lie about its own layout. Every substitution is recorded in
  `references/SOURCES.md`, and a needle that no longer matches fails the build — that
  guard caught two of my own guesses, so it is not theoretical.
- **Strips must name real headings.** A `strip_sections` entry that matches nothing
  upstream is a dead rule; the build refuses it. Declare only what the file has.
- **`ALWAYS_ON_BUDGET = 2400` words.** `SKILL.md` is billed on every request. When a
  new source wants a rule there, the answer is usually a reference file, or a cut.
- **Bucket = destination, not origin.** Add a bucket only for a genuinely new kind of
  output; otherwise the router becomes a list of repos.
- **`build.py sync` must run from the repo root** (`python3 one-skill/build.py sync`),
  same as the legacy `compile.py` before it.
- **PEP 668.** System-wide `pip install` fails with `externally-managed-environment`.
  Use a venv.
- **No pyyaml in this environment.** That is why the manifest is JSON and the parser in
  `build.py` is a hand-rolled frontmatter subset (scalars, block scalars, inline lists)
  rather than `yaml.safe_load`.
- **Pack reproducibility (legacy).** `legacy/coding-agents/compile.py` writes `ZipInfo`
  with a fixed timestamp so its archive is byte-reproducible. `build.py install` does not
  yet: `zipfile` records mtimes, so `one-skill.zip` is not bit-stable across rebuilds.
  It is not CI-gated on content, only on the tree that produced it.
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
  grug appears twice: the short variant and the longer app engine. Cutting to a
  single copy of every rule would mean deciding which author's phrasing survives —
  which is the paraphrase the verbatim rule exists to prevent. Where a section is a
  true duplicate of another *file*, it is not routed at all and is listed under
  `not_routed` with the reason.
- **75k words of references is a lot of skill.** The counterweight is the router and
  the "one reference at a time" rule; if that rule is not honoured in practice, the
  answer is fewer sources merged, not a longer `SKILL.md`.
