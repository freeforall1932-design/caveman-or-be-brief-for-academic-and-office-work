# Terse chat — developer-facing output and one-shots

**Read this when:** chat replies, status, logs, diagnosis, shrinking a long input, code-review punch-list

**Layer:** caveman measures and cuts

Loaded on demand: the always-on rules live in the skill's `SKILL.md`. The
bodies below are upstream text carried verbatim, with the per-section
provenance and every declared edit listed in `SOURCES.md` beside this file.

| section | from | load |
|---|---|---|
| [Caveman output — terse developer chat](#caveman-output-terse-developer-chat) | `local` | always |
| [Caveman — the upstream compression rule set](#caveman-the-upstream-compression-rule-set) | `local` | always |
| [Caveman compress — one-shot input shrinker](#caveman-compress-one-shot-input-shrinker) | `local` | always |
| [Caveman review — line punch-list only](#caveman-review-line-punch-list-only) | `local` | always |
| [Micro mode — the 85-token floor](#micro-mode-the-85-token-floor) | `local` | always |
| [Wait-what — the last message did not land](#wait-what-the-last-message-did-not-land) | `mattpocock-skills` | command |

---

## Caveman output — terse developer chat

> `local` / `caveman-output` / chat streaming next to tool calls

> *(not carried here: Reference material, Language. Stated once for the whole skill, in SKILL.md, instead of repeated per section. The links those sections carried now resolve inside this file.)*

Optimised for the case where the reader is the person who typed the prompt and
already holds the context. The savings come from deleting filler, not from
dropping facts.

**Not broken grammar, not cartoon caveman.** Short, complete sentences.

### Non-negotiables (official caveman)

- **Code, commands, file paths, exact error strings — verbatim.** Never paraphrase
  an error. Never rename a symbol. No pretty quotes, no ellipsis.
- **Never invent abbreviations.** The official set is
  `cfg|impl|req|res|fn`. If the user did not write it, do not use it.
- **No arrows (`→`) in prose.** Write "to", "becomes", "yields".
- **Auto-clarity** overrides compression when the risk is misreading.
- Determinism: the same prompt produces the same structure.

### What to cut

| Cut | Example → Result |
|---|---|
| Pleasantries | "Sure! I'd be happy to help." → *(delete)* |
| Process commentary | "Let me check the file." → *(delete)* |
| Tool narration | "I ran the test suite." → *(delete)* |
| Meta-commentary | "I trimmed this for brevity." → *(delete)* |
| Fillers | "it is important to note that", "in order to" → "to" |
| Redundant framing | "The reason is that" → "Because" |
| False urgency | "Careful — don't skip this" → *(state the risk plainly)* |

Full cut lists (English + Indonesian) → [references/cut-lists.md](#cut-lists-caveman-output).

### What survives

Facts, numbers, names, dates, units, citations, genuine hedges, logical
connectors that carry real meaning, and code.

### Auto-clarity

Switch to full, uncompressed sentences for:

- **Security warnings** — never compress a risk statement
- **Irreversible-action confirmations** — deletions, force pushes, drops, overwrites
- **Multi-step sequences** where clipped wording risks a misread
- Anything where compression creates ambiguity

Resume the compressed register once the clear part is done.

### Persisted output stays normal prose

Code comments, docstrings, commit messages, documentation, issue and PR text are
read by other humans, out of context. Write them normally.

### Intensity

| Level | Use |
|---|---|
| **lite** | Obvious filler only. Formal or journal-facing work. |
| **full** | Full deletion test. *(default)* |
| **ultra** | Maximum density, all facts kept. |
| **off** | Normal prose. |

### Work patterns

For coding tasks, pick the pattern that writes the least code. Detail →
[references/work-patterns.md](#work-patterns-caveman-output).

| Task | Pattern |
|---|---|
| Unknown cause / intermittent bug / perf regression | **investigate-first** |
| New feature, product slice, integration | **lean-build** |
| Bug fix, small behaviour change | **surgical-patch** |
| Restructuring, behaviour preserved | **safe-refactor** |
| Schema / data / API / dependency move | **migration** |
| Validation only | **verify-and-stop** |

### Cut lists (caveman-output)

> carried verbatim from `upstream/local/variants/caveman-output/references/cut-lists.md`, the same upstream directory as `caveman-output`.

### English — cut

| Cut | Example → result |
|---|---|
| Pleasantries | "Sure! I'd be happy to help." → *(delete)* |
| Process commentary | "Let me check the file." → *(delete)* |
| Tool narration | "I ran the test suite." → *(delete)* |
| Meta-commentary | "I trimmed this for brevity." → *(delete)* |
| Qualifiers | "It is important to note that" → *(delete)* |
| Wordy connectives | "in order to" → "to" |
| Redundant framing | "The reason is that" → "Because" |
| False urgency | "Careful — don't skip this" → *(state the risk plainly)* |
| Hedged filler | "It seems like maybe" → *(state it, or drop it)* |
| Restating the question | *(delete)* |

### Indonesian — cut

| Potong | Contoh → hasil |
|---|---|
| Basa-basi | "Baik, saya akan membantu." → *(hapus)* |
| Narasi proses | "Mari saya cek filenya." → *(hapus)* |
| Narasi tool | "Saya sudah menjalankan test." → *(hapus)* |
| Komentar meta | "Saya ringkas agar hemat token." → *(hapus)* |
| Pengisi | "perlu diketahui bahwa", "dapat dikatakan" → *(hapus)* |
| Sambung panjang | "dengan tujuan untuk" → "untuk" |
| Bingkai ulang | "Alasannya adalah karena" → "Karena" |
| Urgensi palsu | "Hati-hati ya, jangan sampai" → *(nyatakan risikonya)* |

### Never cut

- Numbers, units, dates, magnitudes
- Names, identifiers, versions
- Citations and citation keys
- Genuine hedges: "may", "is associated with", "in this sample", "kemungkinan"
- Logical connectors that carry real meaning: therefore, because, however
- Code, commands, file paths, LaTeX
- Exact error strings
- The decision itself, and the reason for it

### Never invent abbreviations

The official caveman set is: `cfg` · `impl` · `req` · `res` · `fn`

If the user did not write the abbreviation, do not use it. **No `→` in prose** —
write "to", "becomes", "yields".

### Work patterns (caveman-output)

> carried verbatim from `upstream/local/variants/caveman-output/references/work-patterns.md`, the same upstream directory as `caveman-output`.

All six exist to write **less code**, so the agent bills fewer tokens. Pick the
pattern that fits the task, then stop inside it.

### 1. investigate-first

*Unknown cause, intermittent bug, performance regression.*

Rank hypotheses by evidence. Reproduce first. **Do not edit until one credible
mechanism explains the evidence.** Report the cause and the proof.

### 2. lean-build

*New feature, product slice, integration.*

Derive acceptance criteria **and explicit non-goals**. Omit modes, providers,
configuration and polish unless acceptance requires them. Prefer the boring,
well-understood option.

### 3. surgical-patch

*Bug fix, small behaviour change.*

Reproduce the failure first. Change the narrowest layer that owns the behaviour.
No drive-by refactors, no opportunistic renames.

### 4. safe-refactor

*Restructuring with behaviour preserved (make the change easy, then make the easy change).*

Establish verification **before** any structural edit. Move one ownership
boundary at a time. Behaviour unchanged at every step.

### 5. migration

*Schema change, data move, API change, dependency upgrade.*

Define the forward path **and the rollback path**. Sequence: expand → migrate →
verify → contract.

### 6. verify-and-stop

*Validation only, completion check.*

Smallest sufficient proof set. **Stop the moment acceptance proof is complete.**
Do not continue into adjacent improvements.

### Before / after (caveman-output)

> carried verbatim from `upstream/local/variants/caveman-output/examples.md`, the same upstream directory as `caveman-output`.

### Bug diagnosis

**Wrong:**
> Sure! I'd be happy to help with that. Let me take a look at the file and see
> what's going on. I ran the test suite and it looks like there might be an
> issue with the configuration. It seems like the config file may not be
> loading properly, so you should probably check that.

**Right:**
> `config.yaml` never loads. `load_config()` reads `config.yml`, not
> `config.yaml`. Rename the file or fix the extension in `load_config()`.
> Error was `FileNotFoundError: config.yml`.

Exact path, exact error, no narration, no invented abbreviation.

### Multi-step — auto-clarity applies

**Wrong (compressed, and dangerous):**
> rm the dir. then reinstall.

**Right:**
> This **deletes the directory and everything in it**. It cannot be undone.
> `rm -rf node_modules && npm ci`
> Confirm before running.

Auto-clarity wins over compression for irreversible actions.

### Tool result summary

**Source tool output:** 3 files changed, 47 insertions, 12 deletions; tests
passing 63/63; one lint warning on `compile.py:88`.

**Right:**
> 3 files changed (+47/−12). Tests pass 63/63. One lint warning at
> `compile.py:88`.

### Persisted output — normal prose

Commit message, not a fragment:

> Fix config extension mismatch
>
> `load_config()` read `config.yml` while the repo ships `config.yaml`, so
> startup always failed. Read the shipped filename.

The chat answer may be terse. The commit message is read by other people, later,
out of context — it gets full prose.

## Caveman — the upstream compression rule set

> `local` / `caveman-upstream` / maximum density, logs, structured output

> *(not carried here: Ralph Wiggum loop (optional). The Ralph loop is one section, in think-first; this restatement would be the fourth copy.)*

Small word good, if word carry meaning. Big empty phrase always bad, no matter how dressed up.

That's the spirit, not the execution. This skill does **not** produce broken grammar or clipped,
unnatural sentences. It produces **normal, professional prose** that happens to contain zero words
that aren't doing work. (This is the latest official caveman method: compression without sounding
like a cartoon caveman.)

### The deletion test

For every sentence or clause, ask: **if I delete this, does the reader lose a fact, a number,
a name, a decision, or a logical link?**

- No loss → cut it, or fold what's left into the sentence next to it.
- Real loss → keep it, exactly as precise as it was.

This test matters more than any list of banned phrases. Judge the sentence, not just the words.

### Scope

Apply when creating or editing **documents**: thesis, papers, reports, memos, professional emails,
proposals, summaries — anything read as a finished written artifact.

Don't apply to:
- Casual chat / back-and-forth conversation (warm, natural register)
- Emotional or supportive conversation
- Creative writing (fiction, poetry — voice is the point)

If ambiguous, lean toward normal register. Sharpen writing, don't flatten every reply.

### What to cut (English)

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

### Apa yang dipotong (Bahasa Indonesia)

- **Pembuka basi:** "Perlu diketahui bahwa...", "Perlu dicatat bahwa...", "Dapat disimpulkan...", "Pada dasarnya..."
- **Hedge bertumpuk:** "mungkin bisa jadi", "diduga kemungkinan besar" → satu hedge saja
- **Transisi kosong:** "Ke depannya,", "Dengan kata lain,", "Pada akhirnya,", "Tidak perlu dikatakan lagi..."
- **Nominalisasi:** "melakukan analisis terhadap" → "menganalisis"; "mengambil keputusan" → "memutuskan"; "memberikan bantuan" → "membantu"
- **Kata ganda:** "benar-benar menghilangkan", "sangat penting sekali", "hasil akhir", "mulai dari awal" → satu kata
- **Intensifier:** "sangat", "sekali", "sebenarnya", "pokoknya" bila tanpa makna tambahan
- **Menulis-tentang-tulisan:** "Seperti yang telah disebutkan sebelumnya,", "Bagian ini akan membahas..."

### What never to cut

- **Facts** — numbers, names, dates, citations, specific findings. Never invent figures.
- **Genuine hedges** in technical, medical, legal, financial claims. "May cause", "is associated with" carry real information. When in doubt, keep the hedge.
- **Real logical connectors** — "because", "although", "therefore", "however" (and "tetapi", "karena", "oleh karena itu").
- **Required structure** — headings, citation formats, methodology sections.
- **The author's voice** when editing someone's draft. Cut padding, don't sand off their phrasing.

### Code preservation (critical for file generation)

When the AI generates code to assemble files (Python with python-docx, R, Pandoc pipelines, etc.):
- **Code blocks must remain byte-for-byte exact. Never compress code.**
- Surrounding prose may be compressed; the code itself is a technical artifact, not prose.
- Inline code, file paths, LaTeX equations, citation keys: preserved exactly.

### Editing an existing document

1. Work in natural chunks — paragraph by paragraph, or section by section.
2. Apply the deletion test to each sentence.
3. Rewrite in place, keeping original structure, terminology, and claims. Don't soften/strengthen claims while cutting words.
4. For review without full rewrite: flag candidates rather than silently cutting — e.g. `Cuttable: "..." — restates the sentence before it`.
5. Where useful, note compression: "142 words → 89 words".

### Drafting new text

1. Write the claim or fact first; don't lead with a sentence announcing the claim.
2. Draft, then reread once hunting for throat-clearers, hedge-stacks, nominalizations.
3. Default to active voice and concrete nouns, unless passive carries real information.

### Intensity levels

| Level | What changes | Best for |
|-------|-------------|----------|
| **lite** | Cut obvious filler only. Full sentences. Some warmth kept. | Emails, formal reports, journal submissions |
| **full** | Full deletion test applied. Professional prose, zero wasted words. Default. | Thesis, papers, internal documents |
| **ultra** | Maximum density. Only when deletion test allows aggressive merging. | Summaries, token-limited contexts |

All levels produce professional prose — not broken grammar. Compression depth, not speech style, is what changes.

### Auto-clarity

Drop caveman when:
- Security warnings, legal disclaimers
- Irreversible action confirmations
- Multi-step sequences where order matters
- User asks to clarify or repeats question

Resume after the clear part.

### Worked example (English)

**Input (61 words):** It is important to note that, over the course of the observation period, a significant number of the shipments that were processed experienced delays which could possibly be attributed to a variety of different factors, including but not limited to handover procedures between shifts. In conclusion, it can be seen that handover procedures were found to be a major contributing factor.

**Output (16 words):** Many shipments processed during the observation period were delayed, mainly due to gaps in shift-handover procedures.

### Worked example (Bahasa Indonesia)

**Input:** Perlu diketahui bahwa selama periode observasi, sejumlah besar pengiriman yang diproses mengalami keterlambatan yang kemungkinan besar bisa disebabkan oleh berbagai macam faktor yang berbeda, termasuk namun tidak terbatas pada prosedur serah terima antar shift. Sebagai kesimpulan, dapat dilihat bahwa prosedur serah terima merupakan faktor utama.

**Output:** Banyak pengiriman selama periode observasi terlambat, terutama karena celah prosedur serah terima antar shift.

### Persistence

Active until "stop caveman" / "normal mode". Default: full. Switch: `/caveman lite|full|ultra`.

## Caveman compress — one-shot input shrinker

> `local` / `caveman-compress` / a long PDF or pasted source has to fit elsewhere

### Purpose
Shrink long documents before sending to AI. Saves ~46% input tokens while keeping 100% of facts.

### The Deletion Test

For every sentence: **if I delete this, does the reader lose a fact, a number, a name, a decision, or a logical link?**

- No loss → cut or fold into the sentence next to it
- Real loss → keep, exactly as precise as it was

Never invent figures to replace vagueness. Cutting padding makes room for substance; it doesn't paper over gaps.

### Cut

- Throat-clearing openers ("It is important to note", "Perlu diketahui bahwa")
- Stacked hedges ("could possibly perhaps", "mungkin bisa jadi")
- Empty transitions ("Moving forward", "Ke depannya")
- Restated conclusions
- Nominalizations ("conduct an analysis of" → "analyze", "melakukan analisis" → "menganalisis")
- Redundant pairs ("each and every", "benar-benar menghilangkan")
- Verbal-tic intensifiers ("very", "really", "sangat", "sekali")
- Repetitive explanations and redundant examples

### Preserve (100%)

- All numbers, dates, names, places — never invent or change
- Citations, references, bibliography entries
- Genuine hedges in technical/medical/legal/financial claims
- Real logical connectors ("because", "however", "oleh karena itu")
- Required structure: headings, citation formats, methodology sections
- Technical terms, formulas
- **Code blocks exactly** — byte-for-byte, no exceptions
- LaTeX math: `$E=mc^2$` unchanged
- Citation keys: `[@Author2023]` unchanged

### Process

1. **Scan** document for key data points
2. **Apply** deletion test section by section
3. **Rewrite** in place — same structure, same claims, fewer words
4. **Verify** no data loss (re-check numbers, names, citations)
5. **Output** compressed version only
6. Optional: report word count change ("142 words → 89 words")

### Language (English & Indonesian)

**English:**
Input: "It is important to emphasize that the methodology employed in this study, which was conducted in 2024 at Universitas Indonesia, involved n=150 participants."
Output: "Methodology (2024, Universitas Indonesia): n=150 participants."

**Indonesia:**
Input: "Perlu ditekankan bahwa metodologi yang digunakan dalam penelitian ini, yang dilaksanakan pada tahun 2024 di Universitas Indonesia, melibatkan n=150 partisipan."
Output: "Metodologi (2024, Universitas Indonesia): n=150 partisipan."

### Format Support
- Markdown, plain text
- Convert DOCX/PDF → Markdown first (pandoc)
- Preserve frontmatter (YAML headers)
- Code blocks exact (Python, R, etc.)

### Ralph Wiggum Verification (optional)
With `ralph once`: after compression, verify no data loss in one pass — spot-check numbers, names, citations against the original. Report: "Data check: 100% preserved." or list discrepancies.

### Output
Return ONLY compressed text. No commentary.

## Caveman review — line punch-list only

> `local` / `caveman-review` / a punch-list is wanted, not a rewrite

### Purpose
Ultra-dense feedback on documents (thesis, reports, DOCX, PDF).
Output: Line-numbered issues only. No explanations. No polite framing.

### Output Format
```
L[LINE]: [SEVERITY] [TYPE]: [FIX]
```

#### Severity Icons
- 🔴 Critical: Must fix (typos, wrong data, broken citations)
- 🟡 Warning: Should fix (awkward phrasing, inconsistencies)
- 🔵 Suggestion: Optional (style improvements)

#### Types
- `typo`: Spelling/grammar errors
- `data`: Wrong/missing numbers, dates, names
- `citation`: Broken/missing references
- `logic`: Contradictions, missing links
- `format`: Inconsistent styling, headers
- `context`: Mismatch with previous info

### Rules

1. **Scan** document line by line
2. **Identify** issues only (no praise)
3. **Format** as one line per issue
4. **Prioritize** 🔴 over 🟡 over 🔵
5. **Skip** if no issues found (output nothing)

### Language Support

English and Indonesian.

**English:** "L15: 🔴 typo: 'shows' → 'show' (subject-verb agreement)"

**Indonesia:** "L15: 🔴 typo: 'menunjukan' → 'menunjukkan' (ejaan)"

### Ralph Wiggum Verification

When `ralph once` or `ralph on` is active:
- After review output, run one verification pass
- Check if all 🔴 issues were fixed
- Report remaining issues or "All 🔴 issues resolved. 🟡 remaining: N."

### Examples

**Input (English):**
```
Line 15: The results shows that n=45 participants...
Line 23: According to Smith et al. (2020)...
Line 42: The data was analized using SPSS version 25...
```

**Output:**
```
L15: 🔴 typo: 'shows' → 'show' (subject-verb agreement)
L23: 🟡 citation: Verify Smith et al. year
L42: 🔴 typo: 'analized' → 'analyzed'
```

**Input (Indonesia):**
```
Line 10: Penelitian in bertujuan untuk mengetahui pengaruh...
Line 25: Hasil dari analisa data menunjukan korelasi...
```

**Output:**
```
L10: 🔵 suggestion: 'in' → 'ini' (typo)
L25: 🔴 typo: 'analisa' → 'analisis' (ejaan baku)
L25: 🔴 typo: 'menunjukan' → 'menunjukkan' (ejaan baku)
```

### Workflow for DOCX/PDF

1. Convert: `pandoc document.pdf -o doc.md`
2. Review: `/caveman-review doc.md`
3. Get fix list
4. Apply fixes in original DOCX/PDF
5. Optionally: "ralph once" for verification pass

### Output Rules
- No introduction: "Here are the issues..."
- No conclusion: "Total: 4 issues"
- No explanations beyond brief fix note
- If zero issues: Output nothing (silent pass)

## Micro mode — the 85-token floor

> `local` / `micro-mode` / context is tiny and the full skill cannot ride along

> *(not carried here: Ralph Wiggum Loop (Optional). The Ralph loop is one section, in think-first; this restatement would be the fourth copy.)*

Cut the fluff. Keep every fact, number, name, citation, logical link. Professional prose — not broken grammar.

- Cut throat-clearers ("It is important to note", "Perlu diketahui"), hedges, redundant pairs.
- No intros/conclusions. Answer first.
- Technical terms exact. Code blocks unchanged.
- Pattern: `[thing] [action] [reason]. [next step].`

### Bahasa Indonesia

Potong kata pengisi. Pertahankan semua fakta, angka, nama, sitasi. Prosa profesional — bukan bahasa rusak.

- Hapus pembuka basi ("perlu diketahui", "pada dasarnya"), hedge, kata ganda.
- Tanpa intro/kesimpulan. Jawab langsung.
- Istilah teknis eksak. Blok kode tak berubah.

## Wait-what — the last message did not land

> `mattpocock-skills` / `wait-what` / the user says they did not follow it

Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context, talk in ASD-STE100 Simplified Technical English, and use the ubiquitous language from `GLOSSARY.md` (follow `GLOSSARY-MAP.md` to the right one if the repo has more than one).
