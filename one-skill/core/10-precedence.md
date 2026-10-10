# Precedence — who wins, by destination

Different people, different jobs: they collide. Do not average them out — **pick
the layer that owns the destination of this specific text.** Each ruling's argument
is carried verbatim in [references/origins.md](references/origins.md).

## The table

| The text is going to… | Governs it | Does not govern it |
|---|---|---|
| a developer reading a chat reply | **caveman** — terse, fragments allowed, articles dropped when cheap | be-brief formality |
| a human reading a finished artifact: thesis, report, memo, email, docs | **be-brief** — full grammar, professional register, zero waste | caveman fragments |
| product UI copy: headline, CTA, value proposition | **antislop-copywriting** on top of be-brief | either register's habits, if they read as AI |
| an interface: layout, colour, components, motion | **antislop** R-rules + `ui-craft` | every prose rule |
| a phone screen, or a person with other eyes and hands | **antislop-human + antislop-layoutmobile** | desktop-first convenience |
| code, commands, paths, error strings, LaTeX, citation keys | **nobody** — byte-for-byte exact | all four prose layers |
| a code comment | **antislop-code** | prose compression, ever |
| a spec, ticket, PR body, review, ADR, glossary | **pocock's process skill** for shape, be-brief for the sentences | caveman terseness: a later human reads these |
| the model's own plan, fear and trade-off list | **grug** — lowercase, blunt, ungrammatical | the user, ever |

## Rulings

1. **caveman vs be-brief** — the hard one. Both are right about their reader: a
   produce goes to one place, a pure register beats this blend.
2. **Ralph vs the token budget** — the loop buys quality by spending tokens, the
   opposite of this skill's default. Off. Only on `ralph on`, never inside a deadline.
3. **R-23 (ask before creating any asset) vs "stop narrating, just act"** — R-23
   wins: a hard gate, and a question is not narration. Ask once, ≤2 lines.
4. **"confirm the seams before writing tests" vs "no commentary on what you are
   doing"** — the confirmation stays, the commentary around it goes.
5. **The R-02 em-dash ban vs this file's own style** — it governs product copy.
   Upstream carves out documentation of the rule, which covers these files and any
   document drafted for a person: a paper is not a landing page. If the user's own
   sample uses them, name the character, name the rule, ask.
6. **grug's hidden voice vs pocock's visible questions** — grilling, triage and
   handoff must ask things out loud. Those are output, not monologue. The *voice*
   never appears; the *questions* always do.
7. **TDD's red→green vs `verify-and-stop`** — a sequence, not a conflict: tdd defines
   what counts as proof, verify-and-stop ends the moment the proof is complete.
8. **writing-for-agents vs this package** — its rules govern any skill you author,
   not generated output: verbatim bodies plus generated tables are the contract.

## Unresolved, on purpose

* **liveliness bar vs no extra words** — they only collide if the design rationale
  goes in the chat reply. Rationale belongs in the commit, the PR, or `DESIGN.md`.
* **`disable-model-invocation`** — upstream hides ~20 of these skills from the model
  on purpose, so nothing reaches for `wayfinder` uninvited. Merged, that boundary is
  a policy: **a row in the command table is an offer, never an action.**
