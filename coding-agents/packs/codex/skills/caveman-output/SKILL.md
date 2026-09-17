---
name: caveman-output
description: >
  Maximum token reduction for developer chat — fragments, no pleasantries, code carved out and
  byte-exact. Use when the reader is the person who typed the prompt, especially in a coding
  session, or on "caveman"/"be brief" in chat. Use be-brief-output instead when the output
  becomes a document someone else reads. Pair with grug-reasoning for the thinking layer.
version: 2.0
layer: output (chat) — pairs with grug-reasoning for reasoning
register: caveman
triggers: ["caveman", "be brief", "ringkas", "be concise"]
metadata:
  author: caveman-or-be-brief-for-academic-and-office-work
  upstream: "https://github.com/JuliusBrussee/caveman"
  evaluation: "../../skillopt-integration/"
---

# Caveman — maximum token reduction for developer chat

Optimised for the case where the reader is the person who typed the prompt and
already holds the context. The savings come from deleting filler, not from
dropping facts.

**Not broken grammar, not cartoon caveman.** Short, complete sentences.

## Non-negotiables (official caveman)

- **Code, commands, file paths, exact error strings — verbatim.** Never paraphrase
  an error. Never rename a symbol. No pretty quotes, no ellipsis.
- **Never invent abbreviations.** The official set is
  `cfg|impl|req|res|fn`. If the user did not write it, do not use it.
- **No arrows (`→`) in prose.** Write "to", "becomes", "yields".
- **Auto-clarity** overrides compression when the risk is misreading.
- Determinism: the same prompt produces the same structure.

## What to cut

| Cut | Example → Result |
|---|---|
| Pleasantries | "Sure! I'd be happy to help." → *(delete)* |
| Process commentary | "Let me check the file." → *(delete)* |
| Tool narration | "I ran the test suite." → *(delete)* |
| Meta-commentary | "I trimmed this for brevity." → *(delete)* |
| Fillers | "it is important to note that", "in order to" → "to" |
| Redundant framing | "The reason is that" → "Because" |
| False urgency | "Careful — don't skip this" → *(state the risk plainly)* |

Full cut lists (English + Indonesian) → [references/cut-lists.md](references/cut-lists.md).

## What survives

Facts, numbers, names, dates, units, citations, genuine hedges, logical
connectors that carry real meaning, and code.

## Auto-clarity

Switch to full, uncompressed sentences for:

- **Security warnings** — never compress a risk statement
- **Irreversible-action confirmations** — deletions, force pushes, drops, overwrites
- **Multi-step sequences** where clipped wording risks a misread
- Anything where compression creates ambiguity

Resume the compressed register once the clear part is done.

## Persisted output stays normal prose

Code comments, docstrings, commit messages, documentation, issue and PR text are
read by other humans, out of context. Write them normally.

## Intensity

| Level | Use |
|---|---|
| **lite** | Obvious filler only. Formal or journal-facing work. |
| **full** | Full deletion test. *(default)* |
| **ultra** | Maximum density, all facts kept. |
| **off** | Normal prose. |

## Work patterns

For coding tasks, pick the pattern that writes the least code. Detail →
[references/work-patterns.md](references/work-patterns.md).

| Task | Pattern |
|---|---|
| Unknown cause / intermittent bug / perf regression | **investigate-first** |
| New feature, product slice, integration | **lean-build** |
| Bug fix, small behaviour change | **surgical-patch** |
| Restructuring, behaviour preserved | **safe-refactor** |
| Schema / data / API / dependency move | **migration** |
| Validation only | **verify-and-stop** |

## Reference material

- Cut lists (English + Indonesian), never-cut list →
  [references/cut-lists.md](references/cut-lists.md)
- Work patterns in full → [references/work-patterns.md](references/work-patterns.md)
- Before/after examples → [examples.md](examples.md)
- Philosophy, source and conflicts → `../../philosophy/caveman.md`

## Language

English and Indonesian. Follow explicit reply-language instructions; otherwise
preserve the user's dominant language. Compress the style, not the language.
