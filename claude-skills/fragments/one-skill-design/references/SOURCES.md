# Sources

This skill is generated. `one-skill/sources.json` decides what is in it;
`one-skill/build.py` writes this file. Editing `SKILL.md` or `references/`
by hand is a mistake — the next build overwrites it.

| source | upstream | revision | files vendored | license |
|---|---|---|---|---|
| caveman-or-be-brief (this repository) | `freeforall1932-design/skills-repo` | `00a733ea4a` | 29 | Unlicense (root) / MIT (caveman-universal) |
| anti-slop — the design filter (miqdadbadjuber/anti-slop) | `miqdadbadjuber/anti-slop` | `388cbe3b6c` | 7 | MIT |
| mattpocock/skills — engineering, productivity, misc | `mattpocock/skills` | `49dd158d10` | 57 | MIT |
| Caveman — the token-efficiency voice (upstream v3.2.0) | `JuliusBrussee/caveman` | `2e08b9177c` | 22 | MIT |
| The Grug Brained Developer (grugbrain.dev) | `bigskysoftware/grugbrain.dev` | `b1b1ca855c` | 1 | CC BY-SA 4.0 (site) |
| Strix — security testing method (usestrix/strix) | `usestrix/strix` | `62b496430d` | 9 | Apache-2.0 |
| mem0 — integration discipline (mem0ai/mem0) | `mem0ai/mem0` | `b7ad69afda` | 6 | Apache-2.0 |
| Archify — diagram authoring discipline (tt-a1i/archify) | `tt-a1i/archify` | `54edef453c` | 2 | MIT |

## What the merge changed

Upstream text is carried verbatim except for:

1. YAML frontmatter stripped (the merged skill has one frontmatter block).
2. Headings demoted one level, leading H1 dropped (each section is titled by
   `sources.json`).
3. Links to a sibling file rewritten to an in-file anchor, because siblings
   ride in the same reference file.
4. The sections listed in `strip_sections` — only the ones that instruct the
   agent to fetch files or edit an entry file, which a merged skill must not do.
5. Where a skill is mostly a driver for a tool this skill does not ship,
   `keep_sections` carries only the sections that work without it, and
   `markup` removes website markup (never words) from sources that are
   generated pages. Both are listed per section below.

Everything else is the author's wording. Nothing was paraphrased to make the
packaging convenient.

## Per-section notes

| section | carried from | notes |
|---|---|---|
| antislop core — craftsmanship standard, R-rules, liveliness | `anti-slop/antislop-core` | The upstream install wizard and its pointer-block step are dropped: in this merged skill every sibling is already inside the same skill, so there is nothing for the agent to fetch and no entry file to edit. Not carried: First-Run Install Wizard, Already installed, and the user asks how to update. |
| antislop-human — contrast, keyboard, focus, states | `anti-slop/antislop-human` | The contrast checker no longer sits next to a standalone SKILL.md: it is carried at `scripts/contrast-check.py` inside this skill, which is what the command below resolves to. Literal edits recorded in `replace`: `(`contrast-check.py`, next to this `SKILL.md`)`; `point the script path at this skill's folder directly`. |
| Pick the diagram type, then be honest about the artifact | `archify/archify-method` | Three sections of a 1 456-word skill: the five-type router, the Mermaid mapping, and the reporting rule. The renderer sections (fast authoring path, delivery gates, setup and fallback, update awareness) are dropped by name because every one of them runs the Node toolchain. The three declared edits below exist because upstream keeps pointing at artifacts this bundle does not ship. Read the type table as a *choice of what to draw*, not as a validation step. Not carried: Existing candidate handoff, Fast authoring path, Update awareness, Delivery, Optional viewer capabilities, Setup and fallback. Literal edits recorded in `replace`: `run `node bin/archify.mjs guide "<scenario>" --json``; `then name them for the reader: use everyday `icon` values and `meta.legend` labels as in **Node icons** (`authoring-contract.md`, in the full skill).`; `Return the checked HTML as an absolute path, diagram type, validation summary, specification/artifact receipt, browser-evidence status, and truthful visual-review status. Do not claim success for a non-zero command or claim visual inspection you did not perform.`. |
