# Caveman Workflow for Academic & Office Work

**Universal token-compression workflow adapted from JuliusBrussee/caveman repository.**

Designed for: thesis writing, journal articles, reports, DOCX/PDF review, office documents.

## Quick Start

### For Claude Users
1. **Custom Instructions:** Copy content from `custom-instructions/claude-instructions.md`
2. **CLI Usage:** `./cli-scripts/claude-cli.sh full "your prompt"`

### For Qwen Users
1. **Custom Instructions:** Copy content from `custom-instructions/qwen-instructions.md`
2. **CLI Usage:** `./cli-scripts/qwen-cli.sh full "your prompt"`

### For AI Agent Platforms
1. **Skills:** Load files from `skills/` directory

---

## Key Benefits

| Metric | Savings | Use Case |
|--------|---------|----------|
| Output tokens | 65% reduction | Drafting, responses |
| Input tokens | 46% reduction | Document compression |
| Review time | ~80% faster | One-line feedback format |
| Language support | Universal | Works with any language |

---

## Repository Structure

```
caveman-workflow/
├── skills/                    # Skill definitions for AI agents
│   ├── caveman.md            # Main compression skill
│   ├── caveman-compress.md   # Document compression skill
│   └── caveman-review.md     # Code/document review skill
├── custom-instructions/       # Custom instructions per model
│   ├── claude-instructions.md
│   └── qwen-instructions.md
├── cli-scripts/               # Command-line usage scripts
│   ├── claude-cli.sh
│   └── qwen-cli.sh
└── README.md                  # This file
```

---

## Core Skills Summary

### 1. `caveman` — Compressed Communication Mode
**Purpose:** Reduce AI response verbosity by 65% while maintaining technical accuracy.

**Intensity Levels:**
| Level | Use Case | Example |
|-------|----------|---------|
| `lite` | Professional emails, formal reports | Keep articles, drop filler |
| `full` | Default for thesis drafting, notes | Drop articles, fragments OK |
| `ultra` | Quick summaries, token-critical | Maximum compression |

**Activation Triggers:**
- "caveman mode", "talk like caveman", "be brief", "less tokens"
- `/caveman lite|full|ultra`
- Auto-triggers when token efficiency requested

**What Gets Removed:**
- Articles: a, an, the
- Filler: just, really, basically, actually, simply
- Pleasantries: "sure", "certainly", "happy to help"
- Hedging: "it might be worth", "you could consider"
- Redundant phrases: "in order to" → "to"

**What Stays Exact:**
- Technical terms, API names, code blocks
- Citations, references, URLs
- File paths, commands, version numbers
- Error messages, log outputs

---

### 2. `caveman-compress` — Document Compression
**Purpose:** Compress existing documents (notes, CLAUDE.md, todos) to save input tokens.

**Workflow:**
1. Convert DOCX/PDF → Markdown (using Pandoc)
2. Run compression script
3. Backup saved as `.original.md`
4. Compressed version overwrites original

**Supported Formats:**
- ✅ `.md`, `.txt`, `.typ`, `.tex` (natural language)
- ❌ `.py`, `.js`, `.json`, `.yaml`, `.css` (code/config)

**Command:**
```bash
python3 -m scripts <absolute_filepath>
```

---

### 3. `caveman-review` — One-Line Review Comments
**Purpose:** Ultra-compressed feedback for code reviews, document edits, thesis corrections.

**Format:**
```
L<line>: <severity> <problem>. <fix>.
```

**Severity Prefixes:**
- `🔴 bug:` — Critical error, must fix
- `🟡 risk:` — Works but fragile
- `🔵 nit:` — Style preference, optional
- `❓ q:` — Question, not suggestion

**Example Output:**
```
L42: 🔴 bug: citation missing for claim. Add [Author et al., [YEAR]].
L88-95: 🟡 risk: section transition abrupt. Add bridging sentence.
L120: 🔵 nit: passive voice. Consider active construction.
L203: ❓ q: why this methodology over alternatives?
```

---

## Model-Specific Setup

See separate files for each model:
- **Claude:** `custom-instructions/claude-instructions.md`
- **Qwen:** `custom-instructions/qwen-instructions.md`
- **CLI:** `cli-scripts/` for command-line usage

---

## Academic & Office Workflow

### For Thesis/Journal Writing

**Step 1: Draft with caveman**
```
User: "/caveman full — draft methodology section"
AI: [Compressed draft, 65% fewer tokens]
```

**Step 2: Compress research notes**
```bash
# Before feeding notes to AI, compress them
python3 -m scripts /path/to/research-notes.md
```

**Step 3: Review with caveman-review**
```
User: "Review chapter 3 for clarity issues"
AI: 
L15: 🔴 bug: undefined term "heteroskedasticity". Define on first use.
L42: 🟡 risk: paragraph too long (12 lines). Split into 2-3 paragraphs.
L88: 🔵 nit: inconsistent tense. Use past tense for methods.
```

### For DOCX/PDF Review

**Step 1: Convert to Markdown**
```bash
pandoc document.docx -o document.md
# or
pandoc document.pdf -o document.md
```

**Step 2: Run caveman-review**
```
User: "Review document.md for errors"
AI: [Line-numbered fix list]
```

**Step 3: Apply fixes in original**
- Use line numbers to locate issues in original DOCX/PDF
- Fix directly in Word/Acrobat
- No need to convert back

### For Office Reports/Emails

**Quick Email:**
```
User: "/caveman lite — write email to team about deadline extension"
AI: "Team: Project deadline extend to Friday EOD. Reason: vendor delay. 
New timeline attached. Questions → reply thread."
```

**Report Summary:**
```
User: "/caveman ultra — summarize Q3 results"
AI: "Q3 revenue +12% YoY. OpEx -5%. Net margin 18.2%. Key driver: enterprise segment."
```

---

## Best Practices

### DO:
- Use `lite` mode for external communications (clients, reviewers)
- Use `full` mode for internal drafts, notes, brainstorming
- Use `ultra` mode for token-limited contexts
- Always preserve technical terms verbatim
- Switch to normal mode for security warnings, legal disclaimers

### DON'T:
- Use caveman for creative writing, poetry, marketing copy
- Invent abbreviations (cfg, impl, req) — tokenizer doesn't save tokens
- Use arrows (→) as own token — write "to" instead
- Apply to code files directly — only prose sections

---

## Language Support

Caveman preserves user's dominant language:
- User writes Portuguese → AI replies Portuguese caveman
- User writes Spanish → AI replies Spanish caveman
- User writes Chinese → AI replies Chinese caveman

**Compression applies to style, not language.**

---

## Integration Options

| Method | Best For | Setup Time |
|--------|----------|------------|
| **Skills** | AI agent platforms (OpenHands, Aider) | 5 min |
| **Custom Instructions** | Chat interfaces (Claude.ai, Web UI) | 2 min |
| **CLI Scripts** | Automation, batch processing | 10 min |

See model-specific files for detailed setup instructions.

---

## References

- Original Repository: https://github.com/JuliusBrussee/caveman
- Installation: `curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash`
- Documentation: See `/tmp/caveman-skill.md`, `/tmp/caveman-compress-skill.md`, `/tmp/caveman-review-skill.md`
