# Caveman or Be Brief — for Academic & Office Work

**A companion to JuliusBrussee's caveman project.** Token-efficient AI communication for thesis writing, journal articles, reports, and DOCX/PDF review. Built around **Grug reasoning** (the thinking layer) + **Caveman compression** (the speaking layer) + optional **Ralph Wiggum loop** (the improvement layer).

**English & Indonesian only. Web/app only — no CLI.**

**v4.0 release note** (recommended vs optional artifacts, illegal pairs, combos): [`RELEASE-v4.0.md`](RELEASE-v4.0.md)

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
- **Other frontier apps (Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi):** no skill system — download [`pseudo-skills.zip`](pseudo-skills.zip) (all 7 files) or paste `pseudo-skills/*.md` into custom instructions. Same behavior, manual trigger.

## Packaging — how to install

| Strategy | ZIPs to upload (Claude app) | Pseudo-skills to paste (other models) |
|----------|-----------------------------|----------------------------------------|
| **ALL-IN-ONE (daily driver)** | `caveman-be-brief.zip` only | `caveman-be-brief.md` only |
| **Modular** | `caveman.zip` + `grug-reasoning.zip` (+ `caveman-compress.zip`, `caveman-review.zip`) | matching `.md` files |
| **All-in-one + Ralph (full control)** | `caveman-be-brief.zip` + `ralph-wiggum.zip` | `caveman-be-brief.md` + `ralph-wiggum.md` |

**Ralph Wiggum on/off control (deadline vs polish):**

```
Deadline, low tokens → leave ralph-wiggum OFF (don't install/paste it)
                       "I want it fast, I don't have tokens to spare" → one pass
Have time, need polish → "ralph on" → loops until quality met
Quick double-check    → "ralph once" → one verification pass then stop
```

Ralph is a **separate, independently-toggleable skill** — zero coupling. It never
slows your deadline work because it only activates when you invoke it.

## Quick Start

1. **Claude app/web:** Settings → Capabilities → enable *Code execution and file creation*, then Customize → Skills → + → Create skill → Upload a skill → pick `claude-skills/app/zips/caveman-be-brief.zip`
2. **Claude Code:** open this repo (skills in `.claude/skills/` load automatically), or `cp -r claude-skills/code/* ~/.claude/skills/`
3. **Models without skills (Gemini/Qwen/ChatGPT/Grok/etc.):** extract `pseudo-skills.zip` or paste `pseudo-skills/caveman-be-brief.md` into custom instructions
4. **Grug thinking:** install `caveman-be-brief` (combined) or `grug-reasoning` (standalone)

### Which File to Use (all in `caveman-universal/custom-instructions/` unless noted)

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

## Repository Map

```
├── README.md                        ← you are here
├── claude-reasoning-caveman.skill   ← Grug engine (single-file skill)
├── claude-skills/
│   ├── app/                         ← Claude app/web format (skill.md + zips/)
│   │   └── zips/                    ← 6 ready-to-upload ZIPs (caveman-be-brief, ralph-wiggum, ...)
│   ├── code/                        ← Claude Code format (SKILL.md, YAML frontmatter)
│   └── README.md                    ← verified install guide for every platform
├── pseudo-skills.zip                ← downloadable bundle of all 7 pseudo-skill files
├── pseudo-skills/                   ← frontmatter-free .md — paste into Gemini/Qwen/ChatGPT/etc.
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