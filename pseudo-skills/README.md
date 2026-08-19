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

```
★  caveman-be-brief.md                 recommended daily driver
○  ralph-wiggum.md                     optional polish (OFF until "ralph on")
○  caveman-compress.md                 optional one-shot (shrink input)
○  caveman-review.md                   optional one-shot (line punch-list)
△  caveman.md + grug-reasoning.md      modular — this pair OR caveman-be-brief, never both
   README.md                           do not paste
```

### Combo TL;DR

| | Paste | Use |
|-|-------|-----|
| **A** | `caveman-be-brief.md` | default |
| **B** | A + `ralph-wiggum.md` | polish |
| **C** | A or B + compress and/or review | long PDF / punch-list |
| **D** | `caveman.md` + `grug-reasoning.md` | same as A, two files |
| **E** | D + `ralph-wiggum.md` | same as B, two files |

**Don't:** `caveman-be-brief.md` + `caveman.md` · `caveman-be-brief.md` + `grug-reasoning.md` · paste the whole zip. Claude users: use `claude-skills/`, not this folder.

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
