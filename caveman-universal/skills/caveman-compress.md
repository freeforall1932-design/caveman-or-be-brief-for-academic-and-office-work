---
name: caveman-compress
description: Compress input documents/notes by ~46% while preserving all data.
version: 2.0
mode: full
triggers: ["compress this", "summarize dense", "condense"]
---

# Caveman Compress Skill

## Purpose
Shrink long documents, notes, or inputs before sending to AI.  
Saves ~46% input tokens while keeping 100% of facts.

## Rules

### Cut
- Repetitive explanations
- Redundant examples
- Verbose introductions/conclusions
- Filler phrases in any language
- Unnecessary politeness

### Preserve
- All numbers, dates, names, places
- Citations, references, bibliography entries
- Technical terms, formulas, code
- Tables, figures, captions (summarize if huge)
- Logical flow and arguments

## Process

1. **Scan** document for key data points
2. **Identify** redundant sections
3. **Compress** sentences using caveman rules
4. **Verify** no data loss
5. **Output** compressed version only

## Context Mismatch Warning
If source document contradicts previous context:
```
⚠️ Context Mismatch: Potential desynchronization detected. Verify your input source.
```
Then compress the new document silently.

## Examples

**Input**:  
"It is important to emphasize that the methodology employed in this study, which was conducted in [YEAR] at [INSTITUTION], involved a comprehensive analysis of n=[SAMPLE_SIZE] participants. The results indicate that there could potentially be a significant correlation..."

**Output**:  
"Methodology ([YEAR], [INSTITUTION]): n=[SAMPLE_SIZE] participants. Results: significant correlation..."

**Input**:  
"The quarterly report for Q[QUARTER] [YEAR] demonstrates that revenue increased by approximately [PERCENTAGE]% compared to the previous period, which suggests that the strategic initiatives implemented have been effective."

**Output**:  
"Q[QUARTER] [YEAR]: Revenue +[PERCENTAGE]%. Strategic initiatives effective."

## Format Support
- Markdown, plain text
- Convert DOCX/PDF → Markdown first (use pandoc)
- Preserve LaTeX math: `$E = mc^2$` → `$E = mc^2$`
- Keep citation keys: `[@Author2023]` → `[@Author2023]`

## Output
Return ONLY compressed text. No commentary.
