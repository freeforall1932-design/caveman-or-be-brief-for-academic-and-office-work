# Cursor — install

Vendor: Cursor (Anysphere) · <https://cursor.com/docs/rules>

## Pick one variant

| Variant | File | Use when |
|---|---|---|
| Unified — grug decides, caveman measures, be-brief writes ★ | [`unified.md`](unified.md) | Recommended default. One agent, both jobs — developer chat and documents. |
| Be Brief — professional prose for documents | [`be-brief-output.md`](be-brief-output.md) | Thesis, journal, report, memo, professional email. Full grammar. |
| Caveman — terse register for developer chat | [`caveman-output.md`](caveman-output.md) | Official caveman register. Fragments OK, code never touched. |
| Grug — internal reasoning layer (no output rules) | [`grug-reasoning.md`](grug-reasoning.md) | Pair with an output variant — this one governs decisions only. |

★ = recommended default for Cursor.

**Load one output register at a time.** `be-brief-output` and
`caveman-output` contradict each other on grammar; loading both gives you
inconsistent output rather than a clear winner.
`grug-reasoning` is the exception — it is a reasoning layer with no output
rules, so it composes with either one.

## Install

Install the agent: `https://cursor.com/download`

### Option A — paste into the instruction file

Project (this repo only):

- `.cursor/rules/*.mdc`
- `AGENTS.md`

Copy the contents of one variant file from this directory into it — no
frontmatter, ready to paste.

> Project rules live in .cursor/rules/ as .mdc files — Markdown WITH YAML frontmatter. The extension is load-bearing: a plain .md file in .cursor/rules/ is ignored, because it has no frontmatter to declare when it applies. Frontmatter has exactly three fields: description, globs, alwaysApply. The legacy root .cursorrules file is still read for backwards compatibility but is documented as legacy. Cursor also reads AGENTS.md (root and subdirectories) and CLAUDE.md.

### Option C — Cursor project rule

Generated `.mdc` rules with correct frontmatter: [`rules/`](rules/).

```bash
mkdir -p .cursor/rules
cp packs/cursor/rules/unified.mdc .cursor/rules/caveman-unified.mdc
```

> The `.mdc` extension is load-bearing — a plain `.md` file in
> `.cursor/rules/` is ignored, because it has no frontmatter to declare
> when it applies.

## Quirks

- Rules apply to Agent only — not Tab completion, Inline Edit, or Bugbot PR reviews. If a rule appears to do nothing, check the surface you tested it in.
- With alwaysApply: true, globs and description are ignored. With false, a glob auto-attaches the rule; a description lets the agent pull it in; neither means it loads only when @-mentioned.
- Team Rules > Project Rules > User Rules, and all applicable rules are MERGED — two rules that disagree both reach the model. Do not load two conflicting variants at once.
- Keep rules under ~500 lines. An always-applied rule is billed on every request.

## Verification

- Tested agent version: `unverified`
- Last verified: 2026-09-17
- Verified by: documentation review of Cursor Rules reference (frontmatter fields, .mdc requirement, legacy .cursorrules status, AGENTS.md and CLAUDE.md support, Agent-only scope, merge precedence).
- Source: <https://cursor.com/docs/rules>
