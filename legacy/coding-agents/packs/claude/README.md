# Claude Code — install

Vendor: Anthropic · <https://code.claude.com/docs>

## Pick one variant

| Variant | File | Use when |
|---|---|---|
| Unified — grug decides, caveman measures, be-brief writes ★ | [`unified.md`](unified.md) | Recommended default. One agent, both jobs — developer chat and documents. |
| Be Brief — professional prose for documents | [`be-brief-output.md`](be-brief-output.md) | Thesis, journal, report, memo, professional email. Full grammar. |
| Caveman — terse register for developer chat | [`caveman-output.md`](caveman-output.md) | Official caveman register. Fragments OK, code never touched. |
| Grug — internal reasoning layer (no output rules) | [`grug-reasoning.md`](grug-reasoning.md) | Pair with an output variant — this one governs decisions only. |

★ = recommended default for Claude Code.

**Load one output register at a time.** `be-brief-output` and
`caveman-output` contradict each other on grammar; loading both gives you
inconsistent output rather than a clear winner.
`grug-reasoning` is the exception — it is a reasoning layer with no output
rules, so it composes with either one.

## Install

Install the agent: `npm i -g @anthropic-ai/claude-code`

### Option A — paste into the instruction file

Global (all projects):

- `~/.claude/CLAUDE.md`

Project (this repo only):

- `CLAUDE.md`
- `.claude/CLAUDE.md`

Copy the contents of one variant file from this directory into it — no
frontmatter, ready to paste.

> CLAUDE.md is auto-loaded from the project root and the user home directory. It is the canonical instruction surface for Claude Code.

### Option B — install as a skill

- user: `~/.claude/skills/<name>/SKILL.md`
- project: `.claude/skills/<name>/SKILL.md`

Generated, frontmatter-complete skill files: [`skills/`](skills/).

> Skills are directories holding SKILL.md with YAML frontmatter (name + description). Project skills auto-load when the repo is opened in Claude Code. This repo already ships .claude/skills/ in that format.

## Quirks

- Claude Code is the strongest reader of YAML-frontmatter skills — prefer the skills directory over pasting into CLAUDE.md when the variant has frontmatter.
- Extended thinking is separate from the <thinking> tag used by the grug variant. If thinking is enabled, keep the grug trace short or it double-counts tokens.

## Verification

- Tested agent version: `2.1.259`
- Last verified: 2026-09-17
- Verified by: documentation review; version pinned from the official caveman profile (agents/profiles/claude.json), verified there by a local pinned-binary probe.
- Source: <https://code.claude.com/docs>
