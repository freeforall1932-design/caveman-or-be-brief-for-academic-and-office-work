# Qwen Code — install

Vendor: QwenLM · <https://github.com/QwenLM/qwen-code>

## Pick one variant

| Variant | File | Use when |
|---|---|---|
| Unified — grug decides, caveman measures, be-brief writes ★ | [`unified.md`](unified.md) | Recommended default. One agent, both jobs — developer chat and documents. |
| Be Brief — professional prose for documents | [`be-brief-output.md`](be-brief-output.md) | Thesis, journal, report, memo, professional email. Full grammar. |
| Caveman — terse register for developer chat | [`caveman-output.md`](caveman-output.md) | Official caveman register. Fragments OK, code never touched. |
| Grug — internal reasoning layer (no output rules) | [`grug-reasoning.md`](grug-reasoning.md) | Pair with an output variant — this one governs decisions only. |

★ = recommended default for Qwen Code.

**Load one output register at a time.** `be-brief-output` and
`caveman-output` contradict each other on grammar; loading both gives you
inconsistent output rather than a clear winner.
`grug-reasoning` is the exception — it is a reasoning layer with no output
rules, so it composes with either one.

## Install

Install the agent: `npm i -g @qwen-code/qwen-code`

### Option A — paste into the instruction file

Global (all projects):

- `~/.qwen/QWEN.md`

Project (this repo only):

- `QWEN.md`

Copy the contents of one variant file from this directory into it — no
frontmatter, ready to paste.

> The context filename is configurable via `context.fileName` in ~/.qwen/settings.json or .qwen/settings.json; QWEN.md is the default. Hierarchical: the global file supplies defaults for all projects, the project file overrides it.

### Option B — install as a skill

- user: `~/.qwen/skills/<name>/SKILL.md`
- project: `.qwen/skills/<name>/SKILL.md`

Generated, frontmatter-complete skill files: [`skills/`](skills/).

> Each skill is a directory containing SKILL.md with YAML frontmatter. Priority: Project > User > Extension > Bundled. Qwen Code watches the personal and project skill directories and refreshes automatically after a short delay — except in bare mode, which needs a restart.

## Quirks

- A structured <thinking> trace is the natural fit here: Qwen models expose reasoning, so the grug variant's internal trace costs little and reads cleanly.
- The official caveman profile disables skill levels (project/user/extension/bundled) when wrapping through its proxy. If you route Qwen Code through a proxy that injects its own system settings, the AGENTS.md/QWEN.md file route is more reliable than the skills directory.

## Verification

- Tested agent version: `0.22.3`
- Last verified: 2026-09-17
- Verified by: documentation review: Qwen Code settings (context files, context.fileName) and Agent Skills docs; binary version pinned from the official caveman profile (agents/profiles/qwen.json).
- Source: <https://github.com/QwenLM/qwen-code/blob/main/docs/users/configuration/settings.md>
