# Caveman Universal — Academic & Office Workflow

**Dense, professional token compression for thesis, journals, reports, DOCX/PDF review.**
Cuts output ~65% (chat/prose) while preserving 100% of technical data, citations, and logic.
Uses the **latest caveman method**: professional prose with zero wasted words (not broken grammar).
**English & Indonesian only. No CLI — web/app only. Ralph Wiggum loop optional.**

## Quick Start (Recommended)

**Use `custom-instructions/caveman-adaptive-universal.md`** (~255 words, zero net token cost).

- Auto-detects intent: casual → dense output, formal/serious → standard model behavior
- Works with all AI models: Claude, Qwen, Gemini, Grok, Kimi, DeepSeek
- Install: copy into custom instructions / system prompt (Claude app, Qwen app, etc.)

## Files

### Custom Instructions

| File | Words | Best For |
|------|-------|----------|
| `caveman-adaptive-universal.md` | ~255 | General purpose, auto-detect intent |
| `caveman-lite-universal.md` | ~870 | More explicit rules and examples |
| `caveman-micro-universal.md` | ~85 | Community-validated minimal version |
| `caveman-grug-universal.md` | ~1.5K | Grug philosophy + compression |
| `claude.md` | ~350 | Claude-specific setup (Windows app, web) |
| `qwen.md` | ~350 | Qwen-specific setup (Android app, web) |

### Skills (for AI Agent Platforms)

| Skill | Purpose |
|-------|---------|
| `skills/caveman.md` | Main compression skill (lite/full/ultra, deletion test) |
| `skills/caveman-compress.md` | Document condensing (~46% input savings) |
| `skills/caveman-review.md` | One-line fix format for reviews |

### References & Docs

| File | What |
|------|------|
| `references/patterns.md` | Full phrase catalog, English + Indonesian |
| `docs/ralph-wiggum-loop.md` | Optional iterative improvement loop |
| `docs/relationship-with-caveman.md` | How this differs from original caveman |
| `docs/verification-report.md` | Benchmark results |
| `docs/debug-analysis.md` | Before/after comparison with original |
| `docs/debug-test.md` | Test cases |
| `docs/universal-context-fix.md` | Placeholder standardization rationale |

## Benchmarks (Honest)

| Metric | Value | When |
|--------|-------|------|
| Output token savings | ~65% | Chat/prose (thesis, reports, email) |
| Output token savings | ~8-21% | Structured coding/document tasks |
| Input token savings | ~46% | After caveman-compress on documents |
| Data loss | 0% | Verified across all test runs |
| Instruction overhead | Pays for itself in 2-3 responses | Via output compression |

Source: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) benchmarks + community replication (JetBrains, independent benchmarks).

## Ralph Wiggum Loop

| Command | Effect | Token Cost |
|---------|--------|------------|
| `ralph off` | Default. One pass. Fast. | None |
| `ralph once` | One verification pass. | ~2x output |
| `ralph on` | Full loop till quality met. | Variable |
| `ralph max 3` | Max 3 iterations. | ~3x output |

**Deadline:** "Saya butuh cepat, token terbatas" → ralph off
**Quality:** "Saya punya waktu, perlu hasil maksimal" → ralph on

## Language

English and Indonesian. Technical terms stay in English. Code blocks unchanged.
Citations preserved exactly.

## Structure

```
caveman-universal/
├── skills/                      # Skills for AI agent platforms
│   ├── caveman.md
│   ├── caveman-compress.md
│   └── caveman-review.md
├── custom-instructions/         # Copy-paste for Claude/Qwen apps etc.
│   ├── caveman-adaptive-universal.md  # Recommended
│   ├── caveman-lite-universal.md
│   ├── caveman-micro-universal.md     # 85-token version
│   ├── caveman-grug-universal.md
│   ├── claude.md
│   └── qwen.md
├── references/
│   └── patterns.md              # Phrase catalog (EN + ID)
├── examples/
│   ├── thesis-input.md
│   ├── thesis-output.md
│   └── report-fixes.txt
├── docs/
│   ├── ralph-wiggum-loop.md
│   ├── relationship-with-caveman.md
│   ├── debug-analysis.md
│   ├── debug-test.md
│   ├── universal-context-fix.md
│   └── verification-report.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Integration

| Method | Best For | How |
|--------|----------|-----|
| **Custom Instructions** | Claude Desktop App (Windows), Claude.ai, Qwen Chat, Gemini | Copy `.md` into system prompt |
| **Claude Code skills** | Claude Code CLI/agents | Copy `../../claude-skills/*` to `~/.claude/skills/` |
| **Pseudo-skills** | Models without skill support (Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi) | Paste `../../pseudo-skills/*.md` into custom instructions |
| **Android APK** | Qwen, Gemini, other chat apps | Copy `qwen.md` or adaptive file into app settings |

No CLI. No API key required. Just paste and use.

## Sync Note

The same rules ship in five formats — keep them in sync when editing:
- `skills/*.md` — YAML frontmatter (for skill-capable platforms)
- `../../claude-skills/app/*/SKILL.md` — Claude app/web format (`---` YAML frontmatter, ≤200-char description) + ZIPs in `app/zips/` (includes combined `caveman-be-brief` and standalone `ralph-wiggum`)
- `../../claude-skills/code/*/SKILL.md` and `../../.claude/skills/` — Claude Code format (YAML frontmatter, ≤1024-char description)
- `../../pseudo-skills/*.md` — frontmatter-free (paste into any model; includes `caveman-be-brief.md` and `ralph-wiggum.md`)

## License

MIT License (see `LICENSE`). The root project uses the Unlicense — see root `LICENSE`.
Inspired by [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman).

---
*English + Indonesia. Ralph optional. Complexity very bad.*