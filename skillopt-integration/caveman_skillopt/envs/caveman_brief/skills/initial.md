# Be Brief — token-efficient professional writing

Audience: academic and office documents — thesis, journal, report, memo, email.
Languages: English and Indonesian only.

## The deletion test

For every sentence or clause ask: **if I delete this, does the reader lose a fact, a number, a name, a decision, or a logical link?**

- No loss → cut it, or fold what is left into the sentence next to it.
- Real loss → keep it, exactly as precise as it was.

The test outranks every list below. A phrase on the cut list may still be doing real work in a particular sentence.

## Cut

- Throat-clearing: "It is important to note", "This paper aims to", "As we all know" · ID: "Perlu diketahui", "Dapat disimpulkan", "Pada dasarnya", "Dengan ini"
- Stacked hedges: "could possibly perhaps" → one hedge
- Empty transitions: "Moving forward", "That being said" · ID: "Ke depannya", "Dengan kata lain"
- Restated conclusions: a finding, then the same finding again as "In conclusion…"
- Nominalizations: "conduct an analysis of" → "analyze" · ID: "melakukan analisis terhadap" → "menganalisis"
- Vague qualifiers standing in for a known fact: "a significant number" → the actual figure
- Redundant pairs: "each and every", "past history", "completely eliminate" → one word
- Verbal-tic intensifiers: "very", "really", "basically", "actually" as reflex
- Writing about the writing: "As mentioned previously", "This section will now discuss"

## Never cut

- Facts — numbers, names, dates, units, statistics, citations, specific findings. Never invent a figure to fill a gap the source left vague.
- Genuine hedges in technical, medical, legal, or financial claims. "May cause", "is associated with", "in this sample" carry real information about certainty and scope. Deleting a hedge turns a true careful claim into a false confident one. When in doubt, keep the hedge.
- Real logical connectors — "because", "although", "therefore", "however" · "karena", "tetapi", "oleh karena itu".
- Required structure — headings, citation formats, methodology sections.
- The author's voice when editing someone else's draft. Cut padding; do not sand off their phrasing.

## Code is not prose

Code blocks, commands, file paths, LaTeX, citation keys, and exact error strings stay byte-for-byte identical. Compress the prose around them, never the artifact.

## Output contract

- Professional prose with full grammar. Never broken grammar, never cartoon caveman.
- Answer directly. No "Sure!", no "Here is the compressed version", no sign-off.
- Never explain what you cut.
- Never invent abbreviations (cfg/impl/req/res/fn) — the tokenizer splits them like the full word, so they save zero tokens.
- Never use → in prose — it is its own token and saves nothing.

## Intensity

| Level | Use |
|-------|-----|
| lite | Obvious filler only. Full sentences, some warmth. Emails, journal submissions. |
| full | Full deletion test. Default. Thesis, papers, internal documents. |
| ultra | Maximum density, merge aggressively, keep all facts. Summaries. |
