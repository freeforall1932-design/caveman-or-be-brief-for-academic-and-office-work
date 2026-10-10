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
| Be brief — professional prose with zero wasted words | `local/be-brief-output` | Not carried: Reference material, Language. |
| Caveman be brief — document modes, intensity, Indonesian | `local/caveman-be-brief-app` | Not carried: THE CORE RULE: Deletion Test, LANGUAGE, INTENSITY LEVELS, RALPH WIGGUM LOOP (separate skill — optional), AUTO-CLARITY. |
| Caveman output — terse developer chat | `local/caveman-output` | Not carried: Reference material, Language. |
| Micro mode — the 85-token floor | `local/micro-mode` | Not carried: Ralph Wiggum Loop (Optional). |
| Grug reasoning — internal, never shown | `local/grug-reasoning` | Not carried: Reference material, Language. |
| The unified workflow — sniff, fear, plan, act, speak | `local/unified-workflow` | Not carried: Reference material, Language. |
| Where grug, caveman and be-brief disagree | `local/philosophies` | Verbatim, with the paths updated for where those files now live: the merge moved the per-variant skills under `legacy/`, and a skill that tells an agent to run a script at a path that no longer exists is a defect. Each substitution is a declared literal, checked at build time. A pointer that left the skill folder for its own build tooling cannot resolve once installed, so it became plain text. Literal edits recorded in `replace`: `Every rule in `coding-agents/` traces`; `MIT (`caveman-universal/`)`; `The coding-agent packaging** in `coding-agents/``; `[`skillopt-integration/`](../skillopt-integration/)`; ``caveman-universal/references/upstream/official-caveman-skill.md``; ``python coding-agents/compile.py``; `at `caveman-universal/references/upstream/``; `this repo's `caveman-universal/``; `which is why `coding-agents/` looks the way it does`. |
| Grug engine — the full internal reasoning rule set | `local/grug-engine` | Kept alongside the short `grug-reasoning` section because it holds what that one omits: hard length budgets, the sentence and paragraph rules for the internal trace, the word-swap table, the abbreviation trap and the continuation protocol for a truncated context. Not carried: CRITICAL DISTINCTION: TWO MODES, LANGUAGE, RALPH WIGGUM LOOP (Optional Iteration), STICKY REASONING MODE, EXIT PHRASES (Return to normal reasoning). |
| Grill me — the alias | `mattpocock-skills/grill-me` | Upstream this is a whole skill: one line that routes to `grilling`. Merged, there is no second skill to call, so the line is kept as the trigger and the work happens in the `grilling` section of this file. |
| Caveman — the voice contract (upstream v3.2.0) | `caveman/caveman-voice` | Upstream original, replaces this repo's v2.x copy. Its 'Anti-slop and the voice' section is the honest bridge to the anti-slop filter; both are carried, and where anti-slop's own rule is stricter, `antislop-human` wins for prose (see the precedence table). |
| Caveman compress — memory and instruction files | `caveman/caveman-compress-upstream` | Different job from this repo's `caveman-review`/`caveman-compress` pair, which compress *documents*. Upstream compresses the instruction files the agent itself loads. Both are carried; pick by artifact. |
| Grug — the full text of the site | `grug/grug-canonical` | The site's markdown source, so it carries page furniture: an empty anchor before each heading and a link to that anchor. The four `markup` transforms remove that scaffolding and nothing else; no word of grug's prose is changed. Read this instead of the compressed summary when the argument matters more than the rule. |
