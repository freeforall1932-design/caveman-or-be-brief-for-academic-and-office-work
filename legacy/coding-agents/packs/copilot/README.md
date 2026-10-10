# GitHub Copilot — install

Vendor: GitHub / Microsoft · <https://docs.github.com/en/copilot>

## Pick one variant

| Variant | File | Use when |
|---|---|---|
| Unified — grug decides, caveman measures, be-brief writes ★ | [`unified.md`](unified.md) | Recommended default. One agent, both jobs — developer chat and documents. |
| Be Brief — professional prose for documents | [`be-brief-output.md`](be-brief-output.md) | Thesis, journal, report, memo, professional email. Full grammar. |
| Caveman — terse register for developer chat | [`caveman-output.md`](caveman-output.md) | Official caveman register. Fragments OK, code never touched. |
| Grug — internal reasoning layer (no output rules) | [`grug-reasoning.md`](grug-reasoning.md) | Pair with an output variant — this one governs decisions only. |

★ = recommended default for GitHub Copilot.

**Load one output register at a time.** `be-brief-output` and
`caveman-output` contradict each other on grammar; loading both gives you
inconsistent output rather than a clear winner.
`grug-reasoning` is the exception — it is a reasoning layer with no output
rules, so it composes with either one.

## Install

Install the agent: `https://docs.github.com/en/copilot/get-started`

### Option A — paste into the instruction file

Project (this repo only):

- `.github/copilot-instructions.md`
- `.github/instructions/*.instructions.md`
- `AGENTS.md`

Copy the contents of one variant file from this directory into it — no
frontmatter, ready to paste.

> .github/copilot-instructions.md is the repo-wide surface. Scoped instructions live in .github/instructions/*.instructions.md with YAML frontmatter (applyTo for path globs, excludeAgent to hide a file from code-review or coding-agent). The Copilot coding agent additionally reads AGENTS.md, CLAUDE.md and GEMINI.md, including nested AGENTS.md files for subdirectories.

## Quirks

- applyTo uses glob patterns; without excludeAgent, a file is used by all agents. Set excludeAgent: "code-review" to keep a writing-style rule out of review passes.
- AGENTS.md is the portable option here and is read by Copilot, Codex, Cursor and OpenCode — one file, four agents.

## Verification

- Tested agent version: `unverified`
- Last verified: 2026-09-17
- Verified by: documentation review of GitHub changelog entries for copilot-instructions.md, .github/instructions/*.instructions.md (applyTo, excludeAgent), and AGENTS.md support in the coding agent.
- Source: <https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/>
