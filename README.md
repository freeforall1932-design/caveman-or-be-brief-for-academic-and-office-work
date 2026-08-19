# Caveman or Be Brief — for Academic & Office Work

**A companion to JuliusBrussee's caveman project.** Token-efficient AI communication for thesis writing, journal articles, reports, and DOCX/PDF review. Built around **Grug reasoning** (the thinking layer) + **Caveman compression** (the speaking layer) + optional **Ralph Wiggum loop** (the improvement layer).

**English & Indonesian only. Web/app only — no CLI.**

## What's Here

| Layer | What | File |
|-------|------|------|
| 🧠 **Grug Engine** | Internal reasoning — planning, fear assessment, tool strategy | `claude-reasoning-caveman.skill` |
| 🗣 **Caveman Compression** | Token-efficient output — cut fluff, keep data (latest method) | `caveman-universal/` |
| 🔄 **Ralph Wiggum Loop** | Optional iterative improvement | `caveman-universal/docs/ralph-wiggum-loop.md` |

## Deployment Formats (pick your platform)

| Format | Works on | Where |
|--------|----------|-------|
| **Claude app/web skills** (upload ZIP) | Claude Desktop app (Windows/Mac), claude.ai, Cowork — via Customize → Skills | `claude-skills/app/zips/` — 6 ready-made ZIPs |
| **Claude Code skills** (folder + SKILL.md) | Claude Code, Codex CLI, Cursor, OpenClaw (SKILL.md standard) | `claude-skills/code/` + `.claude/skills/` (auto-loads in this repo) |
| **Pseudo-skills** (frontmatter-free .md) | Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi — paste into custom instructions | `pseudo-skills/` or download `pseudo-skills.zip` |
| **Custom instructions** (.md) | Claude Desktop (Windows), Claude.ai, Qwen app (Android), Gemini | `caveman-universal/custom-instructions/` |

**Quick answer — yes, it ports to Claude and other frontier models:**

- **Claude app on Windows / claude.ai:** upload a ZIP from `claude-skills/app/zips/` in **Customize → Skills** (enable *Code execution and file creation* first). Works on Free/Pro/Max/Team/Enterprise.
- **Claude Code:** open this repo (skills auto-load from `.claude/skills/`) or copy `claude-skills/code/*` to `~/.claude/skills/`.
- **Other frontier apps (Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi):** no skill system — download [`pseudo-skills.zip`](pseudo-skills.zip) or paste one combo from `pseudo-skills/` (see [How to use pseudo-skills](#how-to-use-pseudo-skills)). Same rules as Claude skills, no YAML.

## What to install

Claude app: upload the `.zip`. Everyone else: paste the matching `.md` from [`pseudo-skills.zip`](pseudo-skills.zip).

```
★  caveman-be-brief.zip / .md              recommended daily driver
○  ralph-wiggum.zip / .md                  optional polish (OFF until "ralph on")
○  caveman-compress.zip / .md              optional one-shot (shrink input)
○  caveman-review.zip / .md                optional one-shot (line punch-list)
△  caveman.zip / .md + grug-reasoning.zip / .md
                                           modular — use this pair OR caveman-be-brief, never both
★  pseudo-skills.zip                       non-Claude only (extract, paste one combo)
△  claude-reasoning-caveman.skill          single-file Grug — skip if caveman-be-brief
                                           or grug-reasoning is already installed
```

### Combo TL;DR

| | Stack | Use |
|-|-------|-----|
| **A** | `caveman-be-brief` only | default |
| **B** | A + `ralph-wiggum` | polish (`ralph on`) |
| **C** | A or B + `caveman-compress` and/or `caveman-review` | long PDF / punch-list |
| **D** | `caveman` + `grug-reasoning` | same as A, two files |
| **E** | D + `ralph-wiggum` | same as B, two files |

**Don't:** `caveman-be-brief` + `caveman` · `caveman-be-brief` + `grug-reasoning` · `caveman-be-brief` + `claude-reasoning-caveman.skill` · paste the whole zip.

## How to use pseudo-skills

Models without a skill loader (Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi, Copilot) cannot upload Claude ZIPs. You **paste** a markdown file. Behavior matches the Claude skills (deletion test, EN+ID, code preserve, Grug hidden, Ralph optional).

### What you do

1. Download [`pseudo-skills.zip`](pseudo-skills.zip) and extract it, **or** open `pseudo-skills/` in this repo.
2. Open **one** file from a combo above (start with `caveman-be-brief.md`).
3. Copy the **entire** file.
4. Paste into:
   - **Gemini** — Settings → Custom Instructions
   - **Qwen** (app / web) — Settings → System Prompt / Custom Instructions
   - **ChatGPT** — Custom instructions, or paste at the start of a chat
   - **Grok / DeepSeek / Kimi / Copilot** — paste at conversation start (or system prompt if the app has one)
5. Start working. Say `caveman`, `be brief`, `ringkas`, or just write as usual — the instructions stay on.

### What you should expect

| You see | You should not see |
|---------|-------------------|
| Tight professional prose (full grammar) | Cartoon caveman / broken English in the reply |
| Facts, numbers, citations, hedges kept | Invented figures or stripped “may / suggests” |
| Code / LaTeX / `[@Cite2023]` unchanged | “Compressed” code that no longer runs |
| Optional word-count note (`142 → 89`) | Grug internal monologue (that stays hidden) |
| Until you say `stop caveman` / `stop grug` / `normal mode` | Skills turning off by themselves |

**Intensity:** `lite` (emails, journals) · `full` (default, thesis) · `ultra` (summaries). Say `/caveman lite` or “use lite”.

**Ralph (only if you also pasted `ralph-wiggum.md`):**

```
ralph off   → one pass (default)
ralph once  → one extra check
ralph on    → loop until you say stop / done
ralph max 3 → cap at 3 passes
```

**One-shots:** paste `caveman-compress.md` to shrink a long source *before* another chat. Paste `caveman-review.md` when you want `L15: 🔴 typo: …` only, not a rewrite.

Full pairing notes: [`pseudo-skills/README.md`](pseudo-skills/README.md).

## Quick Start (Claude)

1. **Claude app/web:** Settings → Capabilities → enable *Code execution and file creation*, then Customize → Skills → Upload → `claude-skills/app/zips/caveman-be-brief.zip`
2. **Claude Code:** open this repo, or `cp -r claude-skills/code/* ~/.claude/skills/`
3. **Grug thinking:** install `caveman-be-brief` (combined) **or** `grug-reasoning` (standalone) — not both with be-brief

### Extra copy-paste instructions (optional, thinner than skills)

All in `caveman-universal/custom-instructions/` unless noted.

| Use Case | File |
|----------|------|
| Minimal, zero-overhead | `caveman-adaptive-universal.md` |
| More explicit rules | `caveman-lite-universal.md` |
| Community-validated 85-token version | `caveman-micro-universal.md` |
| Grug philosophy + compression | `caveman-grug-universal.md` |
| Claude-specific (Windows app, web) | `claude.md` |
| Qwen-specific (Android, web) | `qwen.md` |
| Full phrase catalog (EN + ID) | `caveman-universal/references/patterns.md` |

## Method (Latest)

This project uses the **latest official caveman method**: professional prose with zero wasted words — *not* broken grammar. Core rule is the **deletion test**: *if I delete this, does the reader lose a fact, a number, a name, a decision, or a logical link?* No loss → cut. Real loss → keep, exact.

### Code preservation (for AI file generation)

When the AI generates code to assemble files (Python with python-docx, R, Pandoc pipelines, etc.),
**code blocks must remain byte-for-byte exact — never compressed.** Surrounding prose is compressed;
the code itself is a technical artifact. Inline code, file paths, LaTeX equations, and citation keys
are preserved verbatim. This is built into every skill and instruction file so generated documents
never break.

## What's Different From the Official Project

| Area | Official caveman (v2.1) | This project |
|------|-------------------------|--------------|
| **Method** | Cut-the-fluff prose | Same latest method (deletion test) |
| **Languages** | Universal | **English + Indonesian only** |
| **Deployment** | CLI, MCP, npm, agent SDK | **Web/app only — no CLI** |
| **Reasoning layer** | None | **Grug engine** (internal thinking) |
| **Iteration** | None | **Ralph Wiggum loop** (optional, separate) |
| **Engine model** | Compression engine for tool output | AI-prompt-based compression only |
| **Code in output** | Preserved | **Preserved exactly** (Python/R file assembly) |
| **Token claims** | 65% flat | **Honest split: ~65% chat/prose, ~8–21% structured tasks** |

## Benchmarks (Honest)

| Metric | Value | When |
|--------|-------|------|
| Output token savings | ~65% | Chat/prose (thesis, reports, email) |
| Output token savings | ~8–21% | Structured coding/document tasks |
| Input token savings | ~46% | After caveman-compress on documents |
| Data loss | 0% | Verified across all test runs |

Source: original caveman benchmarks + independent replication (JetBrains, community tests).

## Relationship to Original Caveman

This is a **companion**, not a replacement. The original [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (v2.1, 92K+ stars) provides:

- A real compression engine for tool outputs, logs, JSON
- MCP middleware (`npx caveman-shrink`)
- Support for 30+ coding agents

This project provides:
- **Grug reasoning engine** — the thinking layer original caveman doesn't ship
- **Document-focused workflow** — thesis, journals, reports, DOCX/PDF
- **Optional Ralph Wiggum loop** — iterative improvement when quality matters
- **English + Indonesian** — targeted language support

**Use both together:** original caveman for everyday coding, this project for academic/office writing. See [`caveman-universal/docs/relationship-with-caveman.md`](caveman-universal/docs/relationship-with-caveman.md).

## Ralph Wiggum Loop (Optional)

```
ralph off  → one pass, speed priority (default, for deadlines)
ralph once → one verification pass (quick double-check)
ralph on   → full iterative improvement (polish, quality)
```

**Deadline mode:** Leave OFF. Say "I want it fast, I don't have tokens to spare."
**Quality mode:** Turn ON. "I have time, I need this polished."

Ralph is a **separate, independently-toggleable skill** — zero coupling.

## Repository Map

```
├── README.md                        ← you are here
├── claude-reasoning-caveman.skill   ← Grug engine (single-file skill)
├── claude-skills/
│   ├── app/                         ← Claude app/web format (skill.md + zips/)
│   │   └── zips/                    ← 6 ready-to-upload ZIPs
│   ├── code/                        ← Claude Code format (SKILL.md, YAML frontmatter)
│   └── README.md                    ← verified install guide for every platform
├── pseudo-skills.zip                ← bundle for Gemini / Qwen / ChatGPT / Grok / etc.
├── pseudo-skills/                   ← frontmatter-free .md (same content as the zip)
├── caveman-universal/               ← the library
│   ├── custom-instructions/         ← adaptive, lite, micro, grug, claude, qwen
│   ├── skills/                      ← caveman, caveman-compress, caveman-review
│   ├── references/                  ← EN+ID phrase catalog + official upstream files
│   ├── examples/                    ← thesis in/out, report fixes
│   └── docs/                        ← ralph loop, relationship, benchmarks, tests
└── .claude/skills/                  ← auto-loads when this repo is opened in Claude Code
```

## License

Root project: Unlicense (public domain). `caveman-universal/`: MIT. See respective `LICENSE` files.
