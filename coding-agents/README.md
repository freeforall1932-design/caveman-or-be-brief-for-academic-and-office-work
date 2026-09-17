# Coding agents

The rest of this repository targets **Claude (app/web) and paste-in chat
models** for academic and office writing. This section targets **coding
agents** — Qwen Code, Claude Code, Codex, Cursor, Copilot, OpenCode — where
the same three philosophies apply to a different job: reading and writing
code, not chapters.

It exists because the three philosophies do **not** agree with each other,
and a coding agent is where that disagreement actually bites.

---

## Start here

**If you only read one file:** [`philosophy/conflicts.md`](philosophy/conflicts.md).

It states plainly where grug, caveman, and be-brief contradict each other, and
resolves each conflict by destination. The short version:

> **grug decides, caveman measures, be-brief writes, and nobody touches the
> code.**

**If you just want to install something:** pick your agent, open
`packs/<agent>/README.md`, and copy one variant file.

| Agent | Instruction file | Recommended |
|---|---|---|
| [Qwen Code](packs/qwen/README.md) | `QWEN.md` / `~/.qwen/QWEN.md`, or `.qwen/skills/` | `unified` |
| [Claude Code](packs/claude/README.md) | `CLAUDE.md`, or `.claude/skills/` | `unified` |
| [Codex CLI](packs/codex/README.md) | `AGENTS.md` (no project skills dir) | `unified` |
| [Cursor](packs/cursor/README.md) | `.cursor/rules/*.mdc` | `unified` |
| [GitHub Copilot](packs/copilot/README.md) | `.github/copilot-instructions.md`, or `AGENTS.md` | `unified` |
| [OpenCode](packs/opencode/README.md) | `AGENTS.md` | `unified` |

Everything is also bundled in [`packs/coding-agents.zip`](packs/coding-agents.zip).

---

## The four variants

Sources of truth live in [`variants/`](variants/). Everything in
[`packs/`](packs/) is generated from them.

| Variant | Layer | What it governs | Use when |
|---|---|---|---|
| [`unified`](variants/unified.md) | reasoning + output | **Recommended default.** Assigns each philosophy to a layer where it does not collide. | One agent, both jobs — developer chat *and* documents |
| [`be-brief-output`](variants/be-brief-output.md) | output | Professional prose, full grammar, zero wasted words | Thesis, journal, report, memo, professional email |
| [`caveman-output`](variants/caveman-output.md) | output | Terse register, fragments OK, code never touched | Chat replies to a developer |
| [`grug-reasoning`](variants/grug-reasoning.md) | reasoning | **No output rules at all.** How the agent decides. | Pair with either output variant |

### Load exactly one output register

`be-brief-output` and `caveman-output` contradict each other on grammar — one
requires full sentences, the other drops articles and allows fragments.
Loading both gives you inconsistent output, not a blend.

`grug-reasoning` is the exception: it has no output rules, so it composes
cleanly with either one. That is why it ships as a reasoning-only document.

---

## The three philosophies, kept honest

| Document | Source | What it governs |
|---|---|---|
| [`philosophy/grug.md`](philosophy/grug.md) | [grugbrain.dev](https://grugbrain.dev/) | How to decide. Complexity is the eternal enemy. |
| [`philosophy/caveman.md`](philosophy/caveman.md) | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | How much to say. Terse output, code untouched. |
| [`philosophy/be-brief.md`](philosophy/be-brief.md) | this repo, built on official caveman | How it should read. Professional prose for documents. |
| [`philosophy/conflicts.md`](philosophy/conflicts.md) | ours | Where they clash, and which one wins where. |
| [`philosophy/sources.md`](philosophy/sources.md) | — | Exactly what came from where, and what is ours. |

Grug is the only one of the three that is **not** an output style. It is a way
of deciding, and its broken register is part of its rhetorical power — which
is exactly why it must never leak into user-facing text.

---

## Why Qwen Code specifically

Qwen Code is the priority target here, for two reasons.

First, its instruction surface is a plain Markdown context file
(`QWEN.md`, configurable via `context.fileName`), plus a genuine skills
directory at `~/.qwen/skills/` and `.qwen/skills/` — so both delivery routes
work, and the generated pack ships both.

Second, Qwen models expose a reasoning trace, which makes the `grug_reasoning`
register a natural fit: the internal SNIFF → FEAR → PLAN → ACT → SPEAK flow
costs little and reads cleanly. The SkillOpt integration trains against Qwen
as the target by default — see
[`skillopt-integration/configs/coding-agent.yaml`](../skillopt-integration/configs/coding-agent.yaml).

---

## Training these skills instead of hand-tuning them

[`skillopt-integration/`](../skillopt-integration/) adds a SkillOpt
environment that treats these documents as the trainable state of a frozen
model and optimises them behind a validation gate. It scores **per register**,
which is what makes training the four variants separately meaningful:

```bash
python -m caveman_skillopt.train --config skillopt-integration/configs/coding-agent.yaml
```

If you flatten the registers into one, the optimizer averages the conflict
away and you get mush.

---

## Layout

```
coding-agents/
├── README.md              ← you are here
├── philosophy/            ← the three upstream philosophies, plus the conflicts
├── variants/              ← 4 rule documents — SOURCE OF TRUTH
├── profiles/              ← 6 agent profiles (JSON) + schema.md
├── packs/                 ← GENERATED: per-agent × per-variant files + zip
│   └── coding-agents.zip
├── compile.py             ← variants + profiles → packs
└── tests/                 ← 24 tests on profiles and generated output
```

**Do not hand-edit `packs/`.** Change `variants/` or `profiles/`, then:

```bash
python coding-agents/compile.py
pytest coding-agents/tests -q
```

### What the compiler emits, and why the formats differ

| Output | Format | Why |
|---|---|---|
| `packs/<agent>/<variant>.md` | plain Markdown, **frontmatter stripped** | Pasted into a context file, where frontmatter is noise billed on every request |
| `packs/<agent>/skills/<variant>/SKILL.md` | YAML frontmatter (`name` + `description`) | Claude Code, Qwen Code and Codex require it to discover a skill |
| `packs/cursor/rules/<variant>.mdc` | `description` + `globs` + `alwaysApply` | Cursor **ignores** a plain `.md` file in `.cursor/rules/` — the `.mdc` extension and frontmatter are load-bearing |

Agents with no verified skill convention (Cursor, Copilot, OpenCode) get the
paste file and, for Cursor, the `.mdc` rule. No invented paths.

---

## Verification honesty

Three profiles carry a tested binary version, inherited from the official
caveman profile registry where they were verified by a local pinned-binary
probe. Three are marked `"unverified"` and say so, with a documentation
source, because they were established from vendor docs only.

`compile.py` fails closed on a profile that claims a version it never tested.
See [`profiles/schema.md`](profiles/schema.md).

---

## Relationship to the rest of the repo

| | `caveman-universal/` + `pseudo-skills/` | `coding-agents/` |
|---|---|---|
| Audience | Claude app/web, paste-in chat models | Coding agent CLIs |
| Work | Thesis, journals, reports, office docs | Reading and writing code |
| Languages | English + Indonesian | Follows the user's language |
| Philosophy | Grug thinks, caveman/be-brief speaks | Same three, resolved per layer |
| Packaging | zips + `.md` | profiles + generated packs |

They are complementary, not competing. The deletion test is identical; only
the register and the destination differ.
