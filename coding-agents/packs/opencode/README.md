# OpenCode — install

Vendor: SST · <https://opencode.ai/docs>

## Pick one variant

| Variant | File | Use when |
|---|---|---|
| Unified — grug decides, caveman measures, be-brief writes ★ | [`unified.md`](unified.md) | Recommended default. One agent, both jobs — developer chat and documents. |
| Be Brief — professional prose for documents | [`be-brief-output.md`](be-brief-output.md) | Thesis, journal, report, memo, professional email. Full grammar. |
| Caveman — terse register for developer chat | [`caveman-output.md`](caveman-output.md) | Official caveman register. Fragments OK, code never touched. |
| Grug — internal reasoning layer (no output rules) | [`grug-reasoning.md`](grug-reasoning.md) | Pair with an output variant — this one governs decisions only. |

★ = recommended default for OpenCode.

**Load one output register at a time.** `be-brief-output` and
`caveman-output` contradict each other on grammar; loading both gives you
inconsistent output rather than a clear winner.
`grug-reasoning` is the exception — it is a reasoning layer with no output
rules, so it composes with either one.

## Install

Install the agent: `curl -fsSL https://opencode.ai/install | bash`

### Option A — paste into the instruction file

Global (all projects):

- `~/.config/opencode/AGENTS.md`

Project (this repo only):

- `AGENTS.md`

Copy the contents of one variant file from this directory into it — no
frontmatter, ready to paste.

> OpenCode traverses up from the current directory looking for AGENTS.md and CLAUDE.md, then falls back to ~/.config/opencode/AGENTS.md, then ~/.claude/CLAUDE.md unless disabled. Precedence: local > global > ~/.claude/CLAUDE.md. The `instructions` array in opencode.json can add more files or glob patterns (remote URLs supported, 5s timeout).

## Quirks

- Because OpenCode reads ~/.claude/CLAUDE.md by default, a Claude Code install can leak into OpenCode. Disable that fallback if you run different variants in each.
- opencode.json `instructions` accepts globs like `packages/*/AGENTS.md` — the cleanest way to share one rule set across a monorepo.

## Verification

- Tested agent version: `unverified`
- Last verified: 2026-09-17
- Verified by: documentation review of OpenCode Rules (AGENTS.md locations, traversal order, global fallback, ~/.claude/CLAUDE.md fallback, opencode.json instructions field).
- Source: <https://opencode.ai/docs/rules>
