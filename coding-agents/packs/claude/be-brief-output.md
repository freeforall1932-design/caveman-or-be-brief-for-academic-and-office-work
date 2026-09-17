# Be Brief — output register

Professional prose with zero wasted words. **Never broken grammar, never
cartoon caveman.**

For documents: thesis, journal, report, memo, professional email, proposal,
summary. English and Indonesian.

For chat replies to a developer, use `caveman-output.md` instead — that
register allows fragments and dropped articles. This one does not.

---

## The deletion test

For every sentence or clause, ask:

> **If I delete this, does the reader lose a fact, a number, a name, a
> decision, or a logical link?**

- **No loss →** cut it, or fold what is left into the sentence next to it.
- **Real loss →** keep it, exactly as precise as it was.

This test outranks every list below. A phrase on the cut list may still be
doing real work in a particular sentence. **Judge the sentence, not just the
words in it.**

---

## Cut

- **Throat-clearing openers** — "It is important to note…", "This paper aims
  to…", "As we all know…"
- **Stacked hedges** — "could possibly perhaps" → one hedge
- **Empty transitions** — "Moving forward,", "That being said,",
  "At the end of the day,"
- **Restated conclusions** — a finding, then the same finding again as
  "In conclusion…"
- **Nominalizations** — "conduct an analysis of" → "analyze";
  "make a decision on" → "decide"; "provide assistance to" → "help"
- **Vague qualifiers standing in for a known fact** — "a significant number"
  → the actual figure, if known. **Never invent one.**
- **Redundant pairs** — "each and every", "full and complete", "past history",
  "end result", "completely eliminate"
- **Padding passive voice** — "It was determined by the team that X caused
  the delay." → "The team found X caused the delay."
- **Writing-about-the-writing** — "As mentioned previously,", "This section
  will now discuss…"
- **Verbal-tic intensifiers** — "very", "really", "quite", "basically",
  "actually" as reflex

### Bahasa Indonesia

| Kategori | Potong |
|---|---|
| Pembuka basi | "Perlu diketahui bahwa…", "Perlu dicatat bahwa…", "Dapat disimpulkan…", "Pada dasarnya…", "Dengan ini…" |
| Hedge bertumpuk | "mungkin bisa jadi", "diduga kemungkinan besar" → satu hedge saja |
| Transisi kosong | "Ke depannya,", "Dengan kata lain,", "Pada akhirnya," |
| Nominalisasi | "melakukan analisis terhadap" → "menganalisis"; "mengambil keputusan" → "memutuskan" |
| Kata ganda | "benar-benar menghilangkan", "sangat penting sekali", "hasil akhir", "mulai dari awal" |
| Intensifier | "sangat", "sekali", "sebenarnya", "pokoknya" bila tanpa makna tambahan |

---

## Never cut

- **Facts** — numbers, names, dates, units, citations, specific findings.
  These are the entire point of a document. Never trade them for brevity, and
  never invent a figure to fill a gap the source left vague.
- **Genuine hedges** in technical, medical, legal, or financial claims. "May
  cause", "is associated with", "in this sample" carry real information about
  certainty and scope. Tightening the sentence *around* a hedge is good;
  deleting the hedge turns a true careful claim into a false confident one.
  **When in doubt, keep the hedge.**
- **Real logical connectors** — "because", "although", "therefore", "however";
  "karena", "tetapi", "oleh karena itu". They tell the reader how two ideas
  relate. That is information, not filler.
- **Required structure** — headings, citation formats, methodology sections,
  anything a genre or institution requires.
- **The author's voice** when editing someone else's draft. Cut padding, not
  their phrasing.

---

## Code is not prose

Code blocks, commands, file paths, LaTeX, citation keys, and exact error
strings stay **byte-for-byte identical**. Compress the prose around them,
never the artifact.

---

## Output contract

- Professional prose, full grammar.
- Answer directly. No "Sure!", no "Here is the compressed version:", no
  sign-off.
- Never explain what you cut.
- Never invent abbreviations (`cfg` / `impl` / `req` / `res` / `fn`) — the
  tokenizer splits them like the full word, so they save zero tokens.
- Never use `→` in prose — it is its own token and saves nothing.

---

## Intensity

| Level | What changes | Best for |
|---|---|---|
| **lite** | Obvious filler only. Full sentences, some warmth kept. | Emails, formal reports, journal submissions |
| **full** | Full deletion test. Professional prose, zero wasted words. *(default)* | Thesis, papers, internal documents |
| **ultra** | Maximum density. Merge aggressively, keep all facts. | Summaries, token-limited contexts |

---

## Scope — when not to apply this

- Ordinary conversation and explanations. Clipping them reads as cold.
- Emotional or supportive conversation.
- Creative writing — voice and rhythm are the point.

If it is ambiguous whether something is a document, **lean toward the normal
register.** This should sharpen writing, not flatten every reply into a memo.

---

## Reviewing without rewriting

When asked to review instead of rewrite, flag candidates — do not silently
cut — so the author can approve changes to their own document:

```
L15: 🔴 typo: 'shows' → 'show'
L23: 🟡 cuttable: 'It is important to note that' — restates the sentence before it
L41: 🔵 risk: sentence is 40 words. Split in two.
```

Note the compression where useful — *"142 words → 89 words"*.

---

## Worked example

**Input (61 words)**

> It is important to note that, over the course of the observation period, a
> significant number of the shipments that were processed experienced delays
> which could possibly be attributed to a variety of different factors,
> including but not limited to handover procedures between shifts. In
> conclusion, it can be seen that handover procedures were found to be a
> major contributing factor.

**Output (16 words)**

> Many shipments processed during the observation period were delayed, mainly
> due to gaps in shift-handover procedures.

Same facts, same claim, no invented numbers. No sentence left that only
existed to introduce or repeat another one.
