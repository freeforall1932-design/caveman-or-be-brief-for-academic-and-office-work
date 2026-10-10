# one skill — grug · caveman · be-brief · antislop · Pocock

**Everything in this repository, in one skill.** Fifty upstream skills from three
repositories, merged into a single loadable skill: the always-on rules in
`SKILL.md`, the depth in ten reference files read one at a time.

Token-efficient writing for thesis work, journals, reports and office documents; the
anti-slop filter for interfaces and product copy; and a real engineering process
from idea to merged PR. English and Indonesian. Web, app and agent — no CLI to run.

```bash
python one-skill/build.py all     # rebuild the one skill from its manifest
```

## Install

There is one artifact, and it is generated. Upload or copy it; do not edit it.

| Where | What to install |
|---|---|
| **Claude app / claude.ai** | [`claude-skills/app/zips/one-skill.zip`](claude-skills/app/zips/one-skill.zip) — Settings → Capabilities → enable *Code execution and file creation*, then Customize → Skills → Upload |
| **Claude Code** | open this repo ([`.claude/skills/one-skill/`](.claude/skills/one-skill) auto-loads) or `cp -r claude-skills/app/one-skill ~/.claude/skills/` |
| **Codex / Cursor / Copilot / OpenCode / Qwen Code** | [`claude-skills/app/one-skill/`](claude-skills/app/one-skill) into the agent's skill directory, or its `SKILL.md` into `AGENTS.md` / `CLAUDE.md` / `.cursor/rules/` |
| **Gemini, ChatGPT, Grok, DeepSeek, Kimi** (no skill uploader) | paste [`pseudo-skills/one-skill.md`](pseudo-skills/one-skill.md), then paste a reference file when a task needs one |

Then write as usual, or say `caveman`, `be brief`, or `ringkas`. Stop with
`stop caveman` / `stop grug` / `normal mode`.

## What you see, and what you never see

| You see | You do not see |
|---|---|
| Tight prose in the register the destination owns | the grug internal monologue |
| Facts, numbers, citations and hedges intact | an invented figure or a stripped *may* |
| Code, LaTeX and `[@Cite2023]` byte-for-byte identical | "compressed" code that no longer runs |
| Interfaces with a stated purpose behind each technique | gradient-and-glass defaults, unsourced stats, fake testimonials |
| A spec → tickets → implement → review → PR path, on request | a process skill run uninvited |

## The one line

> **grug decides, caveman measures, be-brief writes, antislop filters, pocock runs
> the process, and nobody touches the code.**

Those sources were not written for each other, and they contradict each other in
places. A merge that hides that produces a skill that fails in both directions at
once, so the conflicts are named and resolved **by destination** — in
[`one-skill/core/10-precedence.md`](one-skill/core/10-precedence.md). The short
version:

| The output is… | It reads like | Never like |
|---|---|---|
| a chat reply to a developer | caveman: terse, fragments allowed | formal |
| a document a person reads | be-brief: full grammar, zero waste | cartoon caveman |
| product UI copy | antislop-copywriting | AI tells, unsourced claims |
| code, paths, errors, LaTeX, citations | untouched | compressed |
| a persisted artifact (comment, commit, PR body) | normal prose, full length | shorthand a future human decodes |

## What is merged, and how

`one-skill/sources.json` is the manifest; `one-skill/build.py` is the merge. Every
upstream body is carried **verbatim** — same as the four variants this repo used to
publish, taken from [grugbrain.dev](https://grugbrain.dev/) and
[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) and not
paraphrased. What the merge adds is the routing layer.

| Source | Skills | License |
|---|---|---|
| this repository (`legacy/`: unified, be-brief, caveman, grug, ralph, compress, review, phrase catalog, philosophy) | 13 | Unlicense / MIT |
| [freeforall1932-design/anti-slop-fork](https://github.com/freeforall1932-design/anti-slop-fork) | 6 | MIT |
| [mattpocock/skills](https://github.com/mattpocock/skills) — engineering, productivity, misc | 31 | MIT |

`mattpocock/skills` also ships `skills/in-progress/` (betas with no docs pages that
can vanish without warning) and `skills/deprecated/` (empty by policy). Neither is
merged; `sources.json` says so on the record.

Two escapes let a merged skill stay honest, and both fail the build when they go
stale: `strip_sections` drops an upstream section that only makes sense for a
standalone install (antislop's download wizard), and `replace` makes a literal
wording edit so the skill cannot lie about its own layout. Both are listed in
`references/SOURCES.md` inside the skill, per section.

**Adding a fourth repository is a manifest entry and a rebuild**, not a rewrite:
[`one-skill/README.md`](one-skill/README.md) has the four steps.

```
one-skill/
├── sources.json     ← the manifest: sources, skills, buckets, strips
├── build.py         ← sync · build · install · all · check
├── core/            ← the hand-written merge: layers, precedence, always-on, router
├── upstream/        ← vendored copies, revision-pinned in PROVENANCE.json
├── dist/skill/      ← ★ the single skill
└── tests/           ← 24 tests: fidelity, dead links, budget, determinism, staleness
```

## Inside the skill

| File | Read it when |
|---|---|
| `SKILL.md` | always: nine universal rules, precedence, router, commands |
| `references/write-prose.md` | thesis, journal, report, memo, email, docs, landing copy |
| `references/terse-chat.md` | chat, status, diagnosis, log-reading, one-shot compression |
| `references/think-first.md` | before acting; when a plan needs attacking; `ralph on` |
| `references/code-craft.md` | module design, tests, debugging, prototypes, comments |
| `references/ship-workflow.md` | spec → tickets → implement → review → PR → retro |
| `references/ui-craft.md` | any interface: colour, layout, components, motion |
| `references/responsive-access.md` | reflow across sizes, contrast, keyboard, focus |
| `references/setup-repo.md` | first use of the process skills, git guardrails, hooks |
| `references/teach-and-author.md` | writing a skill or `AGENTS.md`; teaching a concept |
| `references/origins.md` | you want the argument behind a ruling, in upstream's words |

**Intensity:** `lite` (emails, journals) · `full` (default) · `ultra` (summaries).
**Ralph loop:** `ralph off` (default) · `once` · `on` · `max 3`. **Antislop mode:**
`antislop during` · `antislop after` (numbered findings, you pick) · `antislop ask`.

## Numbers

Measured on the four documents this skill is built from, using that corpus; not
re-measured on the merged bundle. The merged skill changes what is *always loaded*,
not what the rules cost when a task runs.

| Metric | Value | When |
|---|---|---|
| Output token savings | ~65% | chat and prose (thesis, reports, email) |
| Output token savings | ~8–21% | structured coding/document tasks |
| Input token savings | ~46% | after `caveman-compress` on a document |
| Data loss | 0% | verified across all test runs |
| Always loaded, per request | 2.4k words | `SKILL.md`, budgeted and enforced by `build.py` |
| On demand | 75k words | ten reference files, loaded one at a time |
| Vendored skills | 50 | across three repositories |

Source: original caveman benchmarks plus independent replication (JetBrains,
community tests). Notes: [`legacy/caveman-universal/docs/relationship-with-caveman.md`](legacy/caveman-universal/docs/relationship-with-caveman.md).

## Relationship to upstream caveman

Still a companion, not a replacement.
[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (v2.1) is a
compression engine for tool output, logs and JSON, plus MCP via `npx caveman-shrink`.
Use that for everyday coding; use this for writing, design judgment and process.

| | Official caveman | one skill |
|--|------------------|-----------|
| Method | cut-the-fluff prose | same deletion test, plus its sources' rules |
| Languages | universal | **English + Indonesian** |
| Deploy | CLI, MCP, npm, agent SDK | **one skill folder — no CLI** |
| Reasoning | none | **grug** (hidden) |
| Iteration | none | **ralph** (opt-in) |
| Interface design | out of scope | **antislop** filter + accessibility gate |
| Engineering process | out of scope | **31 Pocock skills**, as commands |
| Code in output | preserved | **preserved, byte-exact** |

## Train it, do not hand-tune it

[`skillopt-integration/`](skillopt-integration/README.md) connects to
[**SkillOpt**](https://github.com/microsoft/SkillOpt) (via
[`freeforall1932-design/SkillOpt-fork`](https://github.com/freeforall1932-design/SkillOpt-fork)),
which treats the skill document as the trainable state of a frozen model and
optimises it behind a held-out validation gate. Its reward function encodes the
philosophy — fact and hedge retention, byte-exact code, compression achieved,
register fidelity — and gates out the degenerate "echo the input" solution.

```bash
pip install skillopt && pip install -e skillopt-integration
python -m caveman_skillopt.train --config skillopt-integration/configs/be-brief.yaml
```

It trains the four register documents under `legacy/`, per register, because
averaging the registers is how the conflict gets optimised away. A trained
`best_skill.md` becomes an input to the merge: drop it into
`one-skill/upstream/local/`, point that skill's `entry` at it, rebuild. Training the
merged bundle as one document is the obvious next step and is not done yet.

## Repository map

```
├── .claude/skills/one-skill/   ← auto-loads when this repo is opened in Claude Code
├── claude-skills/              ← the skill, in app/web format, + the upload ZIP
├── pseudo-skills/one-skill.md  ← paste half, for models with no skill uploader
├── one-skill/                  ← ★ the merge: manifest, builder, hand-written core, vendored sources
├── skillopt-integration/       ← SkillOpt training environment (39 tests)
├── legacy/                     ← the six-skill era: per-variant skills, packs, the universal library
│   ├── coding-agents/              variants · profiles · packs · compile.py · philosophy
│   ├── caveman-universal/          custom-instructions · references · examples · docs
│   ├── claude-skills/              the old app/ and code/ trees, and the old install guide
│   ├── pseudo-skills/              the old paste files and their pairing notes
│   └── claude-reasoning-caveman.skill
├── docs/                       ← session handoff + improvement log
└── .github/workflows/          ← tests for the merge and for SkillOpt
```

`legacy/` is frozen: read it, do not add to it. It stays because
`skillopt-integration/` trains against those documents and because the reasoning
behind the registers is written down there.

## Project docs

- [`one-skill/README.md`](one-skill/README.md) — how the merge works, how to add a source
- [`docs/session-handoff.md`](docs/session-handoff.md) — current state, constraints, work list
- [`docs/improvement-log.md`](docs/improvement-log.md) — substantive changes and why

## License

Root: Unlicense (public domain). `legacy/caveman-universal/`: MIT. Vendored upstream
work stays under its own license, named per source in
`one-skill/upstream/PROVENANCE.json` and inside the skill at
`references/SOURCES.md`: anti-slop-fork MIT, mattpocock/skills MIT. Merged output is
therefore MIT-encumbered — keep the attribution.
