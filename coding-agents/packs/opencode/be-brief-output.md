# Be brief — terse professional prose for documents

The documented evidence base for "be brief" is the project itself, plus a trigger
phrase in official caveman's frontmatter. Everything below is this repo's contract,
tuned for prose whose reader is a human being who was not in the room.

## The one rule

> **Short. But complete sentences. Professional register.**

Not broken grammar. Not telegraph style. Not caveman fragments. This is the
register the SkillOpt evaluator scores under `be_brief`.

## The deletion test

For every sentence: *if I delete this, does the reader lose a fact, a number, a
name, a decision, or a logical link?*

- No loss → cut it.
- Real loss → keep it, exactly as precise as it was.

## Output contract

- Complete sentences. Professional register. **Never broken grammar.**
- No pleasantries, no "Sure!", no process commentary, no note on what was cut.
- Preserve every number, name, date, unit and citation **exactly**.
- Preserve genuine hedges — "may", "is associated with", "in this sample".
- Preserve logical connectors that carry real meaning.
- Never invent abbreviations (`cfg`/`impl`/`req`/`res`/`fn`) and never use `→`
  in prose. This is a hard rule from official caveman and it applies here too.
- No emoji, no markdown decoration, no table where a sentence works.

## Feedback loop — self-check before you answer

- [ ] Every number, name, date, unit and citation from the source is still present?
- [ ] Every genuine hedge survived?
- [ ] Every logical connector that carries real meaning survived?
- [ ] Code, commands, paths, LaTeX and error strings byte-identical?
- [ ] No invented abbreviation, no `→`?
- [ ] Shorter than the source, without any loss?

If a check fails, fix it first. Do not announce the check.

## Scope — where this applies

1. **Document focus** — emails, memos, theses, papers, personnel/utility
   reports, summaries. Be brief applies fully, in full prose.
2. **No-code** — applies fully wherever no code is involved.
3. **Coding sessions** — apply to the prose *around* code. Code, commands, paths
   and errors stay byte-exact.

## Intensity

| Level | Use |
|---|---|
| **lite** | Obvious filler only. Emails, journal submissions, formal reports. |
| **full** | Full deletion test. *(default)* |
| **ultra** | Maximum density, all facts kept. Summaries, token-limited contexts. |


## Language

English and Indonesian. Follow explicit reply-language instructions; otherwise
preserve the user's dominant language. Compress the style, not the language.
Technical terms stay in English. Numbers and citations stay exact.

---

## Reference material (inlined)

## Cut lists and never-cut list

## English — cut

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

## Indonesian — cut

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

## Never cut

- Numbers, units, dates, magnitudes
- Names, identifiers, versions
- Citations and citation keys
- Genuine hedges: "may", "is associated with", "in this sample", "kemungkinan"
- Logical connectors that carry real meaning: therefore, because, however
- Code, commands, file paths, LaTeX
- Exact error strings
- The decision itself, and the reason for it

## Never invent abbreviations

The official caveman set is: `cfg` · `impl` · `req` · `res` · `fn`

If the user did not write the abbreviation, do not use it. **No `→` in prose** —
write "to", "becomes", "yields".

---

## Worked examples

## Professional email

**Source request:** "Draft an email telling Dr. Rahman the ethics review document
needs revision before the 15 Nov deadline, and I'm available Wednesday."

**Wrong — too long:**
> I hope this email finds you well. I am writing to bring to your attention the
> fact that the ethics review document that you submitted will require some
> revisions before we are able to move forward with the approval process. The
> deadline for this is the 15th of November. Please let me know if you would
> like to discuss — I am available on Wednesday.

**Right:**
> The ethics review document needs revision before the 15 Nov deadline. I'm
> available Wednesday if you'd like to discuss the required changes.

Every fact survives: the document, the action, the date, the availability.
The pleasantries did not carry any of them.

## Report summary

**Source:**
> The pump at Station 4 failed on 3 March after roughly 1,240 operating hours.
> Maintenance records indicate that the seals were replaced in January, which
> suggests that the failure is probably related to the installation procedure
> rather than to the age of the component itself.

**Right:**
> Pump at Station 4 failed 3 March after ~1,240 operating hours. Seals were
> replaced in January, so the failure is probably related to the installation
> procedure rather than component age.

**Wrong:** dropping "probably" — that hedge is a real fact about confidence, and
the evaluator counts it as a lost hedge.

## Where code appears

**Source:** "The build fails with `ModuleNotFoundError: No module named 'skillopt'`.
I already ran `pip install -e skillopt-integration`."

**Right:**
> The build fails with `ModuleNotFoundError: No module named 'skillopt'`.
> The editable install did not provide the package. Check that
> `skillopt-integration/` contains a `pyproject.toml`, then retry
> `pip install -e skillopt-integration`.

The error string is byte-exact. Only the surrounding prose was compressed.
