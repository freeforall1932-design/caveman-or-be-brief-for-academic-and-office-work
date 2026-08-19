# Pseudo-Skills (for models WITHOUT skill support)

**Paste these markdown files into any model's custom instructions / system prompt.**

Models like **Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi, Copilot** don't have a Claude-style
skill system. For them, a "pseudo-skill" is simply a markdown file you paste at conversation
start or into Settings → Custom Instructions. That's it — the model treats it as standing
instructions for the whole session.

## How to use

1. Pick the pseudo-skill you need
2. Copy the file content
3. Paste into:
   - **Gemini:** Settings → Custom Instructions
   - **Qwen app (Android/web):** Settings → System Prompt / Custom Instructions
   - **ChatGPT:** Custom instructions (or paste at conversation start)
   - **Grok / DeepSeek / Kimi:** paste at conversation start, or system prompt if supported
4. Done. The pseudo-skill stays active until you tell it to stop ("normal mode" / "stop caveman" / "stop grug")

## Files

| Pseudo-Skill | Paste when... | Active until |
|--------------|---------------|--------------|
| `caveman-be-brief.md` | All-in-one daily driver (Grug + caveman + be brief) | "stop caveman" / "normal mode" |
| `grug-reasoning.md` | You want Grug internal reasoning + professional output | "stop grug" / "normal mode" |
| `caveman.md` | You want token-compressed professional prose | "stop caveman" / "normal mode" |
| `caveman-compress.md` | You need to shrink long documents for AI input | one-shot |
| `caveman-review.md` | You want line-numbered document review | one-shot |
| `ralph-wiggum.md` | Optional polish loop — quality > speed | "ralph off" / "done" |

## Ralph Wiggum on/off control (deadline vs polish)

The `ralph-wiggum.md` pseudo-skill is **OFF by default** — it only loops when you say
"ralph on". For full token control:

- **Deadline / low tokens:** don't paste `ralph-wiggum.md`, or delete it from custom
  instructions. `caveman-be-brief.md` still gives fast one-pass output.
- **Have time / need polish:** paste it (or keep it) and say "ralph on" / "ralph once".

No coupling: caveman works without Ralph, Ralph only acts when invoked.

## Why no YAML frontmatter?

Claude skill files start with `---` frontmatter (name/description) that the Claude skill loader
parses. When pasted as plain text into another model, that frontmatter is just noise tokens.
These pseudo-skill files are **frontmatter-free** — every token does work.

## Ralph Wiggum Loop

All pseudo-skills support the optional loop commands — use them when quality > speed:

```
ralph off  → one pass (default, for deadlines)
ralph once → one verification pass
ralph on   → iterative improvement until quality met
```

## Relationship to native skills

| Format | For | Where |
|--------|-----|-------|
| `.skill` / `SKILL.md` | Claude Code & skill-capable agents | `claude-skills/` |
| YAML-frontmatter skills | Skill-capable platforms | `caveman-universal/skills/` |
| **Pseudo-skills (this folder)** | **Everything else — paste-in** | `pseudo-skills/` |

Keep the three in sync when updating rules.