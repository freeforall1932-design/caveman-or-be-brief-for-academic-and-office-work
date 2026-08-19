# Caveman or Be Brief — for Academic & Office Work

Token-efficient writing for thesis work, journals, reports, and DOCX/PDF review. Professional prose — not cartoon caveman.

A companion to [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman): **Grug** thinks, **caveman** speaks, optional **Ralph** polishes.

English and Indonesian only. Web/app only — no CLI.

## Highlights

- Latest caveman method: deletion test, facts and hedges kept, code/LaTeX/citations left untouched
- Grug reasoning stays internal — you see the tight answer, not the monologue
- Optional Ralph Wiggum loop for polish (`ralph on`) — off by default
- Same rules on Claude (upload a ZIP) and everywhere else (paste one `.md`)

## Install

Claude app: upload the `.zip`. Everyone else: paste the matching `.md` from [`pseudo-skills.zip`](pseudo-skills.zip).

- ★ [caveman-be-brief.zip](claude-skills/app/zips/caveman-be-brief.zip) / [`.md`](pseudo-skills/caveman-be-brief.md)
  - recommended daily driver
- ○ [ralph-wiggum.zip](claude-skills/app/zips/ralph-wiggum.zip) / [`.md`](pseudo-skills/ralph-wiggum.md)
  - optional polish (OFF until `ralph on`)
- ○ [caveman-compress.zip](claude-skills/app/zips/caveman-compress.zip) / [`.md`](pseudo-skills/caveman-compress.md)
  - optional one-shot (shrink input)
- ○ [caveman-review.zip](claude-skills/app/zips/caveman-review.zip) / [`.md`](pseudo-skills/caveman-review.md)
  - optional one-shot (line punch-list)
- △ [caveman.zip](claude-skills/app/zips/caveman.zip) / [`.md`](pseudo-skills/caveman.md) + [grug-reasoning.zip](claude-skills/app/zips/grug-reasoning.zip) / [`.md`](pseudo-skills/grug-reasoning.md)
  - modular — this pair **or** caveman-be-brief, never both
- ★ [pseudo-skills.zip](pseudo-skills.zip)
  - non-Claude only (extract, paste one combo)
- △ [claude-reasoning-caveman.skill](claude-reasoning-caveman.skill)
  - single-file Grug — skip if caveman-be-brief or grug-reasoning is already installed

### Combo

- **A** — `caveman-be-brief`
  - default
- **B** — A + `ralph-wiggum`
  - polish (`ralph on`)
- **C** — A or B + `caveman-compress` and/or `caveman-review`
  - long PDF / punch-list
- **D** — `caveman` + `grug-reasoning`
  - same as A, two files
- **E** — D + `ralph-wiggum`
  - same as B, two files

**Don't**

- `caveman-be-brief` + `caveman`
- `caveman-be-brief` + `grug-reasoning`
- `caveman-be-brief` + `claude-reasoning-caveman.skill`
- paste the whole zip

## Quick start

**Claude app / claude.ai** — Settings → Capabilities → enable *Code execution and file creation*, then Customize → Skills → Upload → [`caveman-be-brief.zip`](claude-skills/app/zips/caveman-be-brief.zip). Free/Pro/Max/Team/Enterprise.

**Claude Code** — open this repo (skills auto-load from `.claude/skills/`), or `cp -r claude-skills/code/* ~/.claude/skills/`.

**Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi, Copilot** — no skill uploader. Download [`pseudo-skills.zip`](pseudo-skills.zip), extract, copy **one** combo file (start with `caveman-be-brief.md`), paste into custom instructions or at the start of a chat.

Then write as usual, or say `caveman`, `be brief`, or `ringkas`. Stop with `stop caveman` / `stop grug` / `normal mode`.

| You see | You should not see |
|---------|-------------------|
| Tight professional prose (full grammar) | Cartoon caveman / broken English |
| Facts, numbers, citations, hedges kept | Invented figures or stripped “may / suggests” |
| Code / LaTeX / `[@Cite2023]` unchanged | “Compressed” code that no longer runs |
| Optional word-count note (`142 → 89`) | Grug internal monologue |
| Until you say stop | Skills turning off by themselves |

**Intensity:** `lite` (emails, journals) · `full` (default, thesis) · `ultra` (summaries). Say `/caveman lite` or “use lite”.

**Ralph** (only if `ralph-wiggum` is also installed):

```
ralph off   → one pass (default, deadlines)
ralph once  → one extra check
ralph on    → loop until you say stop / done
ralph max 3 → cap at 3 passes
```

**One-shots:** `caveman-compress` shrinks a long source *before* another chat. `caveman-review` prints `L15: 🔴 typo: …` only — not a rewrite.

Pairing notes for paste-in models: [`pseudo-skills/README.md`](pseudo-skills/README.md). Platform matrix: [`claude-skills/README.md`](claude-skills/README.md).

## Thinner alternatives

Optional copy-paste files in `caveman-universal/custom-instructions/` — lighter than a full skill.

| Use | File |
|-----|------|
| Minimal, zero-overhead | `caveman-adaptive-universal.md` |
| More explicit rules | `caveman-lite-universal.md` |
| Community-validated 85-token version | `caveman-micro-universal.md` |
| Grug philosophy + compression | `caveman-grug-universal.md` |
| Claude-specific (Windows app, web) | `claude.md` |
| Qwen-specific (Android, web) | `qwen.md` |
| Full phrase catalog (EN + ID) | `caveman-universal/references/patterns.md` |

## Method

Latest official caveman method: professional prose with zero wasted words — *not* broken grammar. **Deletion test:** if you delete this, does the reader lose a fact, a number, a name, a decision, or a logical link? No loss → cut. Real loss → keep, exact.

When the model writes code to assemble files (python-docx, R, Pandoc, …), **code blocks stay byte-for-byte exact.** Surrounding prose is compressed. Inline code, paths, LaTeX, and citation keys stay verbatim.

## vs official caveman

This is a **companion**, not a replacement. [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (v2.1) is a compression engine for tool output, logs, and JSON, plus MCP (`npx caveman-shrink`). Use that for everyday coding. Use this for academic/office writing.

| | Official caveman | This project |
|--|------------------|--------------|
| Method | Cut-the-fluff prose | Same deletion test |
| Languages | Universal | **English + Indonesian only** |
| Deploy | CLI, MCP, npm, agent SDK | **Web/app only — no CLI** |
| Reasoning | None | **Grug** (hidden) |
| Iteration | None | **Ralph** (optional, separate) |
| Engine | Compresses tool output | Prompt-based only |
| Code in output | Preserved | **Preserved exactly** |
| Token claims | 65% flat | **~65% chat/prose, ~8–21% structured tasks** |

| Metric | Value | When |
|--------|-------|------|
| Output token savings | ~65% | Chat/prose (thesis, reports, email) |
| Output token savings | ~8–21% | Structured coding/document tasks |
| Input token savings | ~46% | After caveman-compress on documents |
| Data loss | 0% | Verified across all test runs |

Source: original caveman benchmarks + independent replication (JetBrains, community tests). Full notes: [`caveman-universal/docs/relationship-with-caveman.md`](caveman-universal/docs/relationship-with-caveman.md).

## Repository map

```
├── README.md                        ← you are here
├── claude-reasoning-caveman.skill   ← Grug engine (single-file skill)
├── claude-skills/
│   ├── app/                         ← Claude app/web format (SKILL.md YAML + zips/)
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
