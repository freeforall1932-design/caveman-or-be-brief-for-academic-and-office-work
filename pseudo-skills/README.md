# pseudo-skills — paste files

For models with no skill uploader: Gemini, ChatGPT, Grok, DeepSeek, Kimi,
Copilot Chat, and any agent whose skill conventions are unknown.

| File | What it is |
|---|---|
| [`one-skill.md`](one-skill.md) | the router half of the one skill: nine universal rules, precedence by destination, the register table, the command table |

Paste it into custom instructions, or at the top of a chat. Then write as usual, or
say `caveman`, `be brief`, `ringkas`. Stop with `normal mode`.

## Why there is no all-in-one paste file

The skill's ten reference files carry 75k words of upstream rule text. Inlining them
into one paste document would spend more context than the writing saves, which is the
whole thing these rules exist to prevent. So paste the router, and paste a reference
next to it when a task needs one:

| Task | Paste this too |
|---|---|
| thesis, report, memo, docs, landing copy | [`../one-skill/dist/skill/references/write-prose.md`](../one-skill/dist/skill/references/write-prose.md) |
| chat with an agent, logs, quick diagnosis | `references/terse-chat.md` |
| a plan that needs attacking before building | `references/think-first.md` |
| code structure, tests, debugging, comments | `references/code-craft.md` |
| spec → tickets → implement → review → PR | `references/ship-workflow.md` |
| any interface | `references/ui-craft.md` |
| phone layouts, contrast, keyboard, focus | `references/responsive-access.md` |
| wiring a repo up for the process skills | `references/setup-repo.md` |
| writing a skill or `AGENTS.md`; teaching | `references/teach-and-author.md` |

One at a time. Two at once is already the point where the model is reading a library
instead of answering.

## Generated

`one-skill.md` is a copy of the built skill's `SKILL.md` with this header above it.
It is written by `python one-skill/build.py install` — edit
[`../one-skill/core/`](../one-skill/core) or
[`../one-skill/sources.json`](../one-skill/sources.json) and rebuild instead.

The per-pairing notes for the previous six paste files (which combos to paste
together, and which pairs must never be pasted together) are in
[`../legacy/pseudo-skills/README.md`](../legacy/pseudo-skills/README.md). That
constraint no longer applies: there is one file, so there is nothing to mis-pair.
