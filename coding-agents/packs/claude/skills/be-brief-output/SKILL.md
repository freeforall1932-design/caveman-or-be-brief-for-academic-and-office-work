---
name: be-brief-output
description: >
  Terse professional prose for documents, emails, theses and reports — short but complete
  sentences, never broken grammar. Use when drafting or tightening emails, memos, theses,
  papers, personnel/utility reports, or summaries; or on "be brief", "be concise", "tighten
  this", "terse", "ringkas". Compresses only; facts, numbers, citations and hedges survive.
  Pair with grug-reasoning for the thinking layer.
version: 2.0
layer: output (prose) — pairs with grug-reasoning for reasoning
register: be_brief
triggers: ["be brief", "be concise", "tighten this", "terse", "ringkas", "shorten", "condense"]
metadata:
  author: caveman-or-be-brief-for-academic-and-office-work
  upstream: "https://github.com/JuliusBrussee/caveman (project; provides only a trigger phrase)"
  evaluation: "../../skillopt-integration/"
---

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

## Reference material

- Cut lists (English + Indonesian), never-cut list →
  [references/cut-lists.md](references/cut-lists.md)
- Before/after examples → [examples.md](examples.md)

## Language

English and Indonesian. Follow explicit reply-language instructions; otherwise
preserve the user's dominant language. Compress the style, not the language.
Technical terms stay in English. Numbers and citations stay exact.
