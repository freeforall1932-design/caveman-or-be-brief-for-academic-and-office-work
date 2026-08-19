---
name: caveman-compress
description: "Compress long documents (~46% token savings) before sending to AI. Preserves 100% of data, citations, code. EN & ID. Triggers: \"compress this\", \"condense\", \"ringkas dokumen\"."
---

# Caveman Compress

## Purpose
Shrink long documents before sending to AI. Saves ~46% input tokens while keeping 100% of facts.

## The Deletion Test

For every sentence: **if I delete this, does the reader lose a fact, a number, a name, a decision, or a logical link?**

- No loss → cut or fold into the sentence next to it
- Real loss → keep, exactly as precise as it was

Never invent figures to replace vagueness. Cutting padding makes room for substance; it doesn't paper over gaps.

## Cut

- Throat-clearing openers ("It is important to note", "Perlu diketahui bahwa")
- Stacked hedges ("could possibly perhaps", "mungkin bisa jadi")
- Empty transitions ("Moving forward", "Ke depannya")
- Restated conclusions
- Nominalizations ("conduct an analysis of" → "analyze", "melakukan analisis" → "menganalisis")
- Redundant pairs ("each and every", "benar-benar menghilangkan")
- Verbal-tic intensifiers ("very", "really", "sangat", "sekali")
- Repetitive explanations and redundant examples

## Preserve (100%)

- All numbers, dates, names, places — never invent or change
- Citations, references, bibliography entries
- Genuine hedges in technical/medical/legal/financial claims
- Real logical connectors ("because", "however", "oleh karena itu")
- Required structure: headings, citation formats, methodology sections
- Technical terms, formulas
- **Code blocks exactly** — byte-for-byte, no exceptions
- LaTeX math: `$E=mc^2$` unchanged
- Citation keys: `[@Author2023]` unchanged

## Process

1. **Scan** document for key data points
2. **Apply** deletion test section by section
3. **Rewrite** in place — same structure, same claims, fewer words
4. **Verify** no data loss (re-check numbers, names, citations)
5. **Output** compressed version only
6. Optional: report word count change ("142 words → 89 words")

## Language (English & Indonesian)

**English:**
Input: "It is important to emphasize that the methodology employed in this study, which was conducted in 2024 at Universitas Indonesia, involved n=150 participants."
Output: "Methodology (2024, Universitas Indonesia): n=150 participants."

**Indonesia:**
Input: "Perlu ditekankan bahwa metodologi yang digunakan dalam penelitian ini, yang dilaksanakan pada tahun 2024 di Universitas Indonesia, melibatkan n=150 partisipan."
Output: "Metodologi (2024, Universitas Indonesia): n=150 partisipan."

## Format Support
- Markdown, plain text
- Convert DOCX/PDF → Markdown first (pandoc)
- Preserve frontmatter (YAML headers)
- Code blocks exact (Python, R, etc.)

## Ralph Wiggum Verification (optional)
With `ralph once`: after compression, verify no data loss in one pass — spot-check numbers, names, citations against the original. Report: "Data check: 100% preserved." or list discrepancies.

## Output
Return ONLY compressed text. No commentary.

