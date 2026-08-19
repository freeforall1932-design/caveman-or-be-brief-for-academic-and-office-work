# Release v4.0 — Latest caveman method, EN/ID, Ralph loop

Professional cut-the-fluff prose (deletion test). English & Indonesian only. Web/app only — no CLI. Ralph Wiggum is a separate, off-by-default polish loop.

## Warnings (read first)

1. **Pick one speak+think package.** `caveman-be-brief` already contains Grug + caveman. Do **not** also install `caveman` + `grug-reasoning`. Duplicate rules, wasted tokens, conflicting voices.
2. **Ralph is optional and OFF by default.** Installing `ralph-wiggum` does nothing until you say `ralph on` / `ralph once`. Deadline work: leave it out.
3. **Claude vs everyone else.** Claude app/web → upload ZIPs from `claude-skills/app/zips/`. Claude Code → folders in `claude-skills/code/`. Gemini / Qwen / ChatGPT / Grok / DeepSeek / Kimi → **`pseudo-skills.zip` only** (paste `.md`, do not upload Claude ZIPs).
4. **Never overwrite originals.** Skills write `_v2` / `_backup`.
5. **Never compress code, LaTeX, or citation keys.** Surrounding prose only.
6. **Languages:** English and Indonesian only. Other languages are out of scope.

## Artifact tree — recommended vs optional

```
Release v4.0
│
├── caveman-be-brief.zip              ★ RECOMMENDED primary (Claude app)
│                                      Grug think + caveman speak. Install this.
│
├── ralph-wiggum.zip                  ○ OPTIONAL polish (Claude app)
│                                      Pair with be-brief. Say "ralph on" when ready.
│
├── caveman.zip                       △ MODULAR speak-only (Claude app)
│                                      ⚠ DON'T PAIR WITH caveman-be-brief.zip — PICK ONE
│
├── grug-reasoning.zip                △ MODULAR think-only (Claude app)
│                                      Pair with caveman.zip if you skipped be-brief.
│                                      ⚠ DON'T PAIR WITH caveman-be-brief.zip
│
├── caveman-compress.zip              ○ OPTIONAL one-shot (Claude app)
│                                      Shrink long input ~46%. Safe with be-brief.
│
├── caveman-review.zip                ○ OPTIONAL one-shot (Claude app)
│                                      Line-numbered punch list. Safe with be-brief.
│
├── claude-reasoning-caveman.skill    △ SINGLE-FILE Grug engine
│                                      Claude Code / agents that load .skill
│                                      Same brain as grug-reasoning.zip (full examples).
│                                      ⚠ Redundant if you already installed be-brief
│                                      or grug-reasoning.
│
└── pseudo-skills.zip                 ★ RECOMMENDED for NON-CLAUDE models
                                       All 7 frontmatter-free .md files.
                                       Extract, then paste ONE combo (see below).
                                       Do not upload this zip to Claude Skills.
```

Paths in the repo:

| Artifact | Path |
|----------|------|
| Claude app ZIPs (6) | `claude-skills/app/zips/` |
| Claude Code skills | `claude-skills/code/` |
| Single-file Grug | `claude-reasoning-caveman.skill` |
| Pseudo-skills bundle | `pseudo-skills.zip` |
| Loose pseudo-skills | `pseudo-skills/*.md` |

## Combos

### Claude app / claude.ai (upload ZIPs)

| Combo | Upload | Say / leave | When |
|-------|--------|-------------|------|
| **A — Daily driver** | `caveman-be-brief.zip` only | — | Default. Deadline-safe. |
| **B — Daily + polish** | `caveman-be-brief.zip` + `ralph-wiggum.zip` | `ralph off` until needed | Thesis / journal polish |
| **C — Daily + tools** | A or B + `caveman-compress.zip` and/or `caveman-review.zip` | "compress this" / "review this" | Long PDF in, or punch-list review |
| **D — Modular** | `caveman.zip` + `grug-reasoning.zip` | — | Same as A, two layers |
| **D+Ralph** | D + `ralph-wiggum.zip` | `ralph on` | Same as B, two layers |

**Illegal pairs:** `caveman-be-brief.zip` + `caveman.zip` · `caveman-be-brief.zip` + `grug-reasoning.zip` · `caveman-be-brief.zip` + `claude-reasoning-caveman.skill`

### Claude Code

Copy `claude-skills/code/*` to `~/.claude/skills/` **or** open this repo (`.claude/skills/` auto-loads). Same combo rules: enable `caveman-be-brief` **or** (`caveman` + `claude-reasoning-caveman`), plus optional `ralph-wiggum` / `caveman-compress` / `caveman-review`.

### Non-Claude models (paste from `pseudo-skills.zip`)

| Combo | Paste | When |
|-------|-------|------|
| **A — Daily driver** | `caveman-be-brief.md` only | Almost always |
| **B — Daily + polish** | `caveman-be-brief.md` + `ralph-wiggum.md` | Quality > tokens |
| **C — Shrink then write** | session 1: `caveman-compress.md`; session 2: combo A or B | Huge source docs |
| **D — Scan then fix** | `caveman-review.md`, then combo A | Want issues first |
| **E — Modular** | `caveman.md` + `grug-reasoning.md` (+ optional Ralph) | Layers separate |

**Illegal:** `caveman-be-brief.md` + `caveman.md` and/or `grug-reasoning.md`. Do not paste the whole zip.

## What's new in v4.0

- Latest caveman method: professional prose, deletion test — not broken-grammar speech
- English & Indonesian phrase catalogs; other languages removed
- CLI deleted — web/app / paste-in only
- Ralph Wiggum as a separate toggle (`off` / `once` / `on` / `max N`)
- Grug: trust-but-verify, small-chunk, continuation protocol, three worked examples
- Four deploy formats: Claude app ZIPs, Claude Code SKILL.md, `.skill` file, pseudo-skills
- Honest token claims: ~65% chat/prose, ~8–21% structured tasks
- Pseudo-skills brought to feature parity with Claude Code (examples, process flow, edit/draft rules)

## Install cheatsheet

```
Claude app/web
  Settings → Capabilities → enable Code execution and file creation
  Customize → Skills → Upload → caveman-be-brief.zip
  Optional: ralph-wiggum.zip

Claude Code
  open this repo   OR   cp -r claude-skills/code/* ~/.claude/skills/

Everyone else
  unzip pseudo-skills.zip
  paste caveman-be-brief.md into custom instructions
```
