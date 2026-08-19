# Pseudo-Skills (for models WITHOUT skill support)

**Paste these markdown files into any model's custom instructions / system prompt.**

Download all seven files at once: [`../pseudo-skills.zip`](../pseudo-skills.zip).

Models like **Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi, Copilot** don't have a Claude-style
skill system. A "pseudo-skill" is a frontmatter-free markdown file you paste at conversation
start or into Settings → Custom Instructions. The model treats it as standing instructions.

These files are **feature-parity** with the Claude Code / Claude app skills (deletion test,
EN+ID catalogs, code preservation, Grug examples, Ralph loop, safety). They omit YAML /
`## Metadata` on purpose — those tags waste tokens on non-Claude models.

## How to use

1. Pick **one recommended file** (usually `caveman-be-brief.md`)
2. Copy the file content
3. Paste into:
   - **Gemini:** Settings → Custom Instructions
   - **Qwen app (Android/web):** Settings → System Prompt / Custom Instructions
   - **ChatGPT:** Custom instructions (or paste at conversation start)
   - **Grok / DeepSeek / Kimi:** paste at conversation start, or system prompt if supported
4. Done. Active until you say `"normal mode"` / `"stop caveman"` / `"stop grug"`

## Recommended vs optional

| File | Role | Install? |
|------|------|----------|
| `caveman-be-brief.md` | **PRIMARY.** Grug think + caveman speak. Daily driver. | **Recommended — paste this** |
| `ralph-wiggum.md` | Polish loop. OFF until you say `ralph on`. | Optional — add when quality > speed |
| `caveman-compress.md` | Shrink long docs for *input* (~46%). | Optional — one-shot |
| `caveman-review.md` | Line-numbered issue list only. | Optional — one-shot |
| `caveman.md` | Speak layer only (no Grug). | Modular alternative — **do not pair with be-brief** |
| `grug-reasoning.md` | Think layer only (full examples). | Modular alternative — **do not pair with be-brief** |
| `README.md` | This guide. | Do not paste |

## Combos (safe)

| Combo | Paste these | Use when |
|-------|-------------|----------|
| **A — Daily driver** | `caveman-be-brief.md` only | Almost always |
| **B — Deadline + polish switch** | `caveman-be-brief.md` + `ralph-wiggum.md` | Thesis polish; say `ralph off` until you need it |
| **C — Dense input then write** | session 1: `caveman-compress.md`; session 2: `caveman-be-brief.md` | 50-page PDF → then draft |
| **D — Scan then fix** | `caveman-review.md` then `caveman-be-brief.md` | Want a punch list first |
| **E — Modular (no all-in-one)** | `caveman.md` + `grug-reasoning.md` | You want layers separate |
| **E+Ralph** | `caveman.md` + `grug-reasoning.md` + `ralph-wiggum.md` | Modular + polish |

## Warnings — do not do this

- **Do not paste `caveman-be-brief.md` together with `caveman.md` or `grug-reasoning.md`.** Duplicate instructions fight each other and burn tokens.
- **Do not paste every file in the zip.** Pick a combo.
- **Do not leave Ralph on for deadline work.** Default is off. `ralph on` multiplies token cost.
- **Do not compress code, LaTeX, citation keys, or numbers.** Built into every file; if a model still rewrites a code block, say "preserve code exactly".
- **Do not overwrite originals.** Skills require `_v2` / `_backup`.
- **Claude users:** do not use this zip. Use `claude-skills/app/zips/` (app) or `claude-skills/code/` (Claude Code).

## Ralph Wiggum on/off (deadline vs polish)

- **Deadline / low tokens:** don't paste `ralph-wiggum.md`. Combo A.
- **Have time / need polish:** Combo B, then `"ralph on"` / `"ralph once"` / `"ralph max 3"`.

No coupling: caveman works without Ralph.

## Why no YAML frontmatter?

Claude skill files start with `---` frontmatter that the Claude loader parses.
On other models that text is noise. These files are **frontmatter-free**.

## Relationship to native skills

| Format | For | Where |
|--------|-----|-------|
| `.skill` / `SKILL.md` | Claude Code & skill-capable agents | `claude-skills/code/` |
| Claude app ZIPs | Claude Desktop / claude.ai | `claude-skills/app/zips/` |
| **Pseudo-skills (this folder)** | **Everything else — paste-in** | `pseudo-skills/` |

Keep the three in sync when updating rules.
