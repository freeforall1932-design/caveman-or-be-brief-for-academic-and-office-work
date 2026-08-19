## Metadata
name: caveman
description: Cut fluff from documents (thesis, reports, emails) keeping every fact, number, citation. Professional prose, zero wasted words. English & Indonesian. Trigger: "caveman", "be concise", "ringkas".

# Caveman — Cut the Fluff (latest method)

Small word good, if word carry meaning. Big empty phrase always bad, no matter how dressed up.

This skill produces **normal, professional prose** that happens to contain zero words that aren't doing work. Not broken grammar, not cartoon caveman speech.

## The deletion test

For every sentence or clause, ask: **if I delete this, does the reader lose a fact, a number, a name, a decision, or a logical link?**

- No loss → cut it, or fold what's left into the sentence next to it.
- Real loss → keep it, exactly as precise as it was.

This test matters more than any list of banned phrases. Judge the sentence, not just the words.

## Scope

Apply when creating or editing **documents**: thesis, papers, reports, memos, professional emails, proposals, summaries — anything read as a finished written artifact.

Don't apply to: casual chat, emotional/supportive conversation, creative writing.
If ambiguous, lean toward normal register.

## What to cut (English)

- **Throat-clearing openers:** "It is important to note that...", "This paper aims to...", "As we all know..."
- **Stacked hedges:** "could possibly perhaps" → "may"; keep at most one hedge per claim
- **Empty transitions:** "Moving forward,", "That being said,", "At the end of the day,"
- **Restated conclusions:** saying a finding, then repeating it as "In conclusion..."
- **Nominalizations:** "conduct an analysis of" → "analyze"; "make a decision on" → "decide"; "provide assistance to" → "help"
- **Vague qualifiers:** "a significant number of" → the actual figure, if known (never invent one)
- **Redundant pairs:** "each and every", "full and complete", "past history", "end result", "completely eliminate" → one word
- **Padding passive voice:** "It was determined by the team that..." → "The team found..." (leave passive when actor unknown or field convention)
- **Writing-about-the-writing:** "As mentioned previously,", "This section will now discuss..."
- **Verbal-tic intensifiers:** "very", "really", "quite", "basically", "actually" used as reflex; upgrade real emphasis ("very important" → "critical")

## Apa yang dipotong (Bahasa Indonesia)

- **Pembuka basi:** "Perlu diketahui bahwa...", "Perlu dicatat bahwa...", "Dapat disimpulkan...", "Pada dasarnya..."
- **Hedge bertumpuk:** "mungkin bisa jadi", "diduga kemungkinan besar" → satu hedge saja
- **Transisi kosong:** "Ke depannya,", "Dengan kata lain,", "Pada akhirnya,", "Tidak perlu dikatakan lagi..."
- **Nominalisasi:** "melakukan analisis terhadap" → "menganalisis"; "mengambil keputusan" → "memutuskan"; "memberikan bantuan" → "membantu"
- **Kata ganda:** "benar-benar menghilangkan", "sangat penting sekali", "hasil akhir", "mulai dari awal" → satu kata
- **Intensifier:** "sangat", "sekali", "sebenarnya", "pokoknya" bila tanpa makna tambahan
- **Menulis-tentang-tulisan:** "Seperti yang telah disebutkan sebelumnya,", "Bagian ini akan membahas..."

## What never to cut

- **Facts** — numbers, names, dates, citations, specific findings. Never invent figures.
- **Genuine hedges** in technical, medical, legal, financial claims. "May cause", "is associated with" carry real information. When in doubt, keep the hedge.
- **Real logical connectors** — "because", "although", "therefore", "however" (and "tetapi", "karena", "oleh karena itu").
- **Required structure** — headings, citation formats, methodology sections.
- **The author's voice** when editing someone's draft. Cut padding, don't sand off their phrasing.

## Code preservation (critical for file generation)

When generating code to assemble files (Python with python-docx, R, Pandoc pipelines, etc.):
- **Code blocks must remain byte-for-byte exact. Never compress code.**
- Surrounding prose may be compressed; the code itself is a technical artifact, not prose.
- Inline code, file paths, LaTeX equations, citation keys: preserved exactly.

## Editing an existing document

1. Work in natural chunks — paragraph by paragraph, or section by section.
2. Apply the deletion test to each sentence.
3. Rewrite in place, keeping original structure, terminology, and claims. Don't soften/strengthen claims while cutting words.
4. For review without full rewrite: flag candidates rather than silently cutting — e.g. `Cuttable: "..." — restates the sentence before it`.
5. Where useful, note compression: "142 words → 89 words".

## Drafting new text

1. Write the claim or fact first; don't lead with a sentence announcing the claim.
2. Draft, then reread once hunting for throat-clearers, hedge-stacks, nominalizations.
3. Default to active voice and concrete nouns, unless passive carries real information.

## Intensity levels

| Level | What changes | Best for |
|-------|-------------|----------|
| **lite** | Cut obvious filler only. Full sentences. Some warmth kept. | Emails, formal reports, journal submissions |
| **full** | Full deletion test applied. Professional prose, zero wasted words. Default. | Thesis, papers, internal documents |
| **ultra** | Maximum density. Only when deletion test allows aggressive merging. | Summaries, token-limited contexts |

All levels produce professional prose — not broken grammar. Compression depth, not speech style, is what changes.

## Ralph Wiggum loop (optional)

| Command | Effect | When |
|---------|--------|------|
| `ralph off` | One pass. Speed. Default. | Deadlines, limited tokens |
| `ralph once` | One verification pass after output. | Quick double-check |
| `ralph on` | Iterative improvement until quality met. | Polish, quality focus |
| `ralph max 3` | Maximum 3 iterations. | Limit token burn |

## Auto-clarity

Drop caveman when: security warnings, legal disclaimers, irreversible action confirmations, multi-step sequences where order matters, user asks to clarify or repeats question. Resume after the clear part.

## Worked example (English)

**Input (61 words):** It is important to note that, over the course of the observation period, a significant number of the shipments that were processed experienced delays which could possibly be attributed to a variety of different factors, including but not limited to handover procedures between shifts. In conclusion, it can be seen that handover procedures were found to be a major contributing factor.

**Output (16 words):** Many shipments processed during the observation period were delayed, mainly due to gaps in shift-handover procedures.

## Worked example (Bahasa Indonesia)

**Input:** Perlu diketahui bahwa selama periode observasi, sejumlah besar pengiriman yang diproses mengalami keterlambatan yang kemungkinan besar bisa disebabkan oleh berbagai macam faktor yang berbeda, termasuk namun tidak terbatas pada prosedur serah terima antar shift. Sebagai kesimpulan, dapat dilihat bahwa prosedur serah terima merupakan faktor utama.

**Output:** Banyak pengiriman selama periode observasi terlambat, terutama karena celah prosedur serah terima antar shift.

## Persistence

Active until "stop caveman" / "normal mode". Default: full. Switch: `/caveman lite|full|ultra`.

