# Agent profile schema

One JSON file per agent under `profiles/`. Adding an agent is a new file
here plus a `compile.py` run — no code changes, no installer.

The shape borrows its philosophy from the official caveman profile registry
(`agents/profiles/*.json` in
[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)): profiles
are **data**, and an unverified claim is worse than no claim.

The fields differ, though. Caveman's profiles describe how to *route an agent
through a proxy*. Ours describe **where an agent reads instruction files
from**, because this repo ships prompts, not a runtime.

---

## Required fields

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | `"1"` | Const. Bump when a breaking change lands. |
| `id` | string | kebab-case, must equal the filename (e.g. `qwen.json` → `qwen`). The pack directory name. |
| `display_name` | string | Human name, e.g. `Qwen Code`. |
| `vendor` | string | Who ships it. |
| `homepage` | URI | Docs root. |
| `binary_names` | string[] | Matched against argv basename for auto-detection. |
| `install` | string | One-line install hint shown when the binary is missing. |
| `wire_protocol` | enum | `openai-chat` · `anthropic-messages` · `openai-responses` · `gemini-generatecontent` |
| `instruction` | object | Where the agent reads instructions — see below. |
| `verification` | object | What was tested and how — see below. |

## Optional fields

| Field | Type | Meaning |
|---|---|---|
| `skills` | object \| null | The agent's on-disk skill surface, if it has one. |
| `recommended_variant` | string | Which of the four variants to default to. |
| `quirks` | string[] | Behaviour that will surprise you. |
| `maintainer` | string \| null | `null` = this repo. |

---

## `instruction`

| Field | Type | Meaning |
|---|---|---|
| `method` | `"file"` | How instructions are delivered. Only `file` today. |
| `format` | enum | `markdown` · `mdc` · `skill-md`. Drives how `compile.py` renders frontmatter. |
| `frontmatter` | bool | Whether the agent **at the paste path** parses YAML frontmatter. |
| `global_paths` | string[] | User-level instruction files (`~` = home). |
| `project_paths` | string[] | Repo-level instruction files. |
| `notes` | string | Anything load-bearing about discovery order or config. |

`frontmatter` is deliberately about the **paste path**, not the agent. Qwen
Code parses frontmatter in `.qwen/skills/*/SKILL.md` but not in `QWEN.md`, so
`compile.py` emits both from the same source: a frontmatter-complete
`SKILL.md` and a stripped `unified.md`.

## `skills`

| Field | Type | Meaning |
|---|---|---|
| `supported` | bool | Does the agent discover skills on disk? |
| `format` | `"skill-md"` | Directory per skill, holding `SKILL.md`. |
| `user_dirs` | string[] | User-level skill roots. |
| `project_dirs` | string[] | Repo-level skill roots. May be empty — Codex has none. |
| `notes` | string | Discovery order, hot-reload behaviour. |

Omit the whole object when the agent has no verified skill convention. Do not
guess one.

## `verification`

| Field | Type | Meaning |
|---|---|---|
| `tested_agent_version` | string | Exact version validated against, or the literal `"unverified"`. |
| `last_verified_at` | ISO date | When. |
| `verified_by` | string | **Who or what.** Must explain how the paths were established. |
| `source` | URI | The doc that was read. |

**The honesty rule:** if `tested_agent_version` is `"unverified"`, then
`verified_by` must contain `"documentation review"`. `compile.py` fails closed
on a profile that claims a version it never tested, or labels itself unverified
without saying where the information came from.

We would rather ship a profile that says "read from the docs, not probed on a
real binary" than one with a plausible-looking invented version string.

---

## Current status

| Agent | Version | How verified |
|---|---|---|
| Qwen Code | 0.22.3 | settings + skills docs; version pinned from official caveman profile |
| Claude Code | 2.1.259 | docs; version pinned from official caveman profile (binary-probed there) |
| Codex CLI | 0.153.0 | docs; version pinned from official caveman profile (binary-probed there) |
| Cursor | unverified | documentation review |
| GitHub Copilot | unverified | documentation review |
| OpenCode | unverified | documentation review |

The three verified versions come from the official caveman profile registry,
which records them as local pinned-binary probes. The three marked
`unverified` were established from vendor documentation only.

## Adding an agent

1. Create `profiles/<id>.json` matching the schema above.
2. Run `python coding-agents/compile.py` — it validates and generates.
3. Run `pytest coding-agents/tests -q`.
4. Add a row to the table in [`../README.md`](../README.md).
