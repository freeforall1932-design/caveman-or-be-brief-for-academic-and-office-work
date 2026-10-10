# OpenAI Codex CLI — install

Vendor: OpenAI · <https://developers.openai.com/codex>

## Pick one variant

| Variant | File | Use when |
|---|---|---|
| Unified — grug decides, caveman measures, be-brief writes ★ | [`unified.md`](unified.md) | Recommended default. One agent, both jobs — developer chat and documents. |
| Be Brief — professional prose for documents | [`be-brief-output.md`](be-brief-output.md) | Thesis, journal, report, memo, professional email. Full grammar. |
| Caveman — terse register for developer chat | [`caveman-output.md`](caveman-output.md) | Official caveman register. Fragments OK, code never touched. |
| Grug — internal reasoning layer (no output rules) | [`grug-reasoning.md`](grug-reasoning.md) | Pair with an output variant — this one governs decisions only. |

★ = recommended default for OpenAI Codex CLI.

**Load one output register at a time.** `be-brief-output` and
`caveman-output` contradict each other on grammar; loading both gives you
inconsistent output rather than a clear winner.
`grug-reasoning` is the exception — it is a reasoning layer with no output
rules, so it composes with either one.

## Install

Install the agent: `npm i -g @openai/codex`

### Option A — paste into the instruction file

Global (all projects):

- `~/.codex/AGENTS.md`

Project (this repo only):

- `AGENTS.md`

Copy the contents of one variant file from this directory into it — no
frontmatter, ready to paste.

> AGENTS.md is read from the project root and, for user-level defaults, from ~/.codex/AGENTS.md.

### Option B — install as a skill

- user: `~/.codex/skills/<name>/SKILL.md`

Generated, frontmatter-complete skill files: [`skills/`](skills/).

> Codex discovers user-level skills only; there is no project-level skills directory in the Codex convention.

## Quirks

- Codex has no project-level skill directory, so a repo that wants to ship instructions should use AGENTS.md at the root.
- AGENTS.md is the most portable surface in this list — Copilot, Cursor and OpenCode read it too. Prefer it when you want one file to work everywhere.

## Verification

- Tested agent version: `0.153.0`
- Last verified: 2026-09-17
- Verified by: documentation review; version pinned from the official caveman profile (agents/profiles/codex.json), verified there by a local pinned-binary probe.
- Source: <https://developers.openai.com/codex>
