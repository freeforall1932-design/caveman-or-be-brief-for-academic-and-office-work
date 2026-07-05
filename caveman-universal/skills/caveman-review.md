---
name: caveman-review
description: One-line feedback with line numbers. Format: L42: 🔴 bug: fix X
version: 2.0
mode: review
triggers: ["review this", "check for errors", "caveman-review"]
---

# Caveman Review Skill

## Purpose
Provide ultra-dense feedback on documents (thesis, reports, DOCX, PDF).  
Output: Line-numbered issues only. No explanations. No polite framing.

## Output Format
```
L[LINE]: [SEVERITY] [TYPE]: [FIX]
```

### Severity Icons
- 🔴 Critical: Must fix (typos, wrong data, broken citations)
- 🟡 Warning: Should fix (awkward phrasing, minor inconsistencies)
- 🔵 Suggestion: Optional (style improvements, clarity)

### Types
- `typo`: Spelling/grammar errors
- `data`: Wrong/missing numbers, dates, names
- `citation`: Broken/missing references
- `logic`: Contradictions, missing links
- `format`: Inconsistent styling, headers
- `context`: Mismatch with previous info

## Rules

1. **Scan** document line by line
2. **Identify** issues only (no praise)
3. **Format** as one line per issue
4. **Prioritize** 🔴 over 🟡 over 🔵
5. **Skip** if no issues found (output nothing)

## Context Mismatch Warning
If document contradicts previous context:
```
⚠️ Context Mismatch: Potential desynchronization detected. Verify your input source.
```
Then continue reviewing the current document.

## Examples

**Input Document** (excerpt):
```
Line 15: The results shows that n=45 participants...
Line 23: According to Smith et al. (2020)...
Line 42: The data was analized using SPSS version 25...
Line 58: Revenue increased by 95% in Q4 2023...
```

**Output**:
```
L15: 🔴 typo: 'shows' → 'show' (subject-verb agreement)
L23: 🟡 citation: Verify Smith et al. year (conflict with bibliography)
L42: 🔴 typo: 'analized' → 'analyzed'
L58: 🟡 data: Replace specific values with [PERCENTAGE]% and Q[QUARTER] for universal template
```

## Workflow for DOCX/PDF

1. Convert: `pandoc document.pdf -o doc.md`
2. Review: `/caveman-review doc.md`
3. Get fix list (see output above)
4. Apply fixes in original DOCX/PDF
5. Repeat until no issues

## Language Support
Works with any language. Error types remain in English for universality:
- `typo`, `data`, `citation`, `logic`, `format`, `context`

## Output Rules
- No introduction: "Here are the issues..."
- No conclusion: "Total: 4 issues"
- No explanations beyond brief fix note
- If zero issues: Output nothing (silent pass)
