# Sources

This skill is generated. `one-skill/sources.json` decides what is in it;
`one-skill/build.py` writes this file. Editing `SKILL.md` or `references/`
by hand is a mistake — the next build overwrites it.

| source | upstream | revision | files vendored | license |
|---|---|---|---|---|
| caveman-or-be-brief (this repository) | `this repository` | `84c9518158` | 29 | Unlicense (root) / MIT (caveman-universal) |
| anti-slop-fork — the anti-slop design filter | `freeforall1932-design/anti-slop-fork` | `388cbe3b6c` | 7 | MIT |
| mattpocock/skills — engineering, productivity, misc | `mattpocock/skills` | `49dd158d10` | 57 | MIT |

## What the merge changed

Upstream text is carried verbatim except for:

1. YAML frontmatter stripped (the merged skill has one frontmatter block).
2. Headings demoted one level, leading H1 dropped (each section is titled by
   `sources.json`).
3. Links to a sibling file rewritten to an in-file anchor, because siblings
   ride in the same reference file.
4. The sections listed in `strip_sections` — only the ones that instruct the
   agent to fetch files or edit an entry file, which a merged skill must not do.

Everything else is the author's wording. Nothing was paraphrased to make the
packaging convenient.

## Per-section notes

| section | carried from | notes |
|---|---|---|
| Be brief — professional prose with zero wasted words | `local/be-brief-output` | Not carried: Reference material, Language. |
| Caveman be brief — document modes, intensity, Indonesian | `local/caveman-be-brief-app` | Not carried: THE CORE RULE: Deletion Test, LANGUAGE, INTENSITY LEVELS, RALPH WIGGUM LOOP (separate skill — optional), AUTO-CLARITY. |
| Caveman output — terse developer chat | `local/caveman-output` | Not carried: Reference material, Language. |
| Caveman — the upstream compression rule set | `local/caveman-upstream` | Not carried: Ralph Wiggum loop (optional). |
| Micro mode — the 85-token floor | `local/micro-mode` | Not carried: Ralph Wiggum Loop (Optional). |
| Grug reasoning — internal, never shown | `local/grug-reasoning` | Not carried: Reference material, Language. |
| The unified workflow — sniff, fear, plan, act, speak | `local/unified-workflow` | Not carried: Reference material, Language. |
| Where grug, caveman and be-brief disagree | `local/philosophies` | Verbatim, with the paths updated for where those files now live: the merge moved the per-variant skills under `legacy/`, and a skill that tells an agent to run a script at a path that no longer exists is a defect. Each substitution is a declared literal, checked at build time. A pointer that left the skill folder for its own build tooling cannot resolve once installed, so it became plain text. Literal edits recorded in `replace`: `Every rule in `coding-agents/` traces`; `MIT (`caveman-universal/`)`; `The coding-agent packaging** in `coding-agents/``; `[`skillopt-integration/`](../skillopt-integration/)`; ``caveman-universal/references/upstream/official-caveman-skill.md``; ``python coding-agents/compile.py``; `at `caveman-universal/references/upstream/``; `this repo's `caveman-universal/``; `which is why `coding-agents/` looks the way it does`. |
| Grug engine — the full internal reasoning rule set | `local/grug-engine` | Kept alongside the short `grug-reasoning` section because it holds what that one omits: hard length budgets, the sentence and paragraph rules for the internal trace, the word-swap table, the abbreviation trap and the continuation protocol for a truncated context. Not carried: CRITICAL DISTINCTION: TWO MODES, LANGUAGE, RALPH WIGGUM LOOP (Optional Iteration), STICKY REASONING MODE, EXIT PHRASES (Return to normal reasoning). |
| antislop core — craftsmanship standard, R-rules, liveliness | `anti-slop-fork/antislop-core` | The upstream install wizard and its pointer-block step are dropped: in this merged skill every sibling is already inside the same skill, so there is nothing for the agent to fetch and no entry file to edit. Not carried: First-Run Install Wizard, Already installed, and the user asks how to update. |
| antislop-human — contrast, keyboard, focus, states | `anti-slop-fork/antislop-human` | The contrast checker no longer sits next to a standalone SKILL.md: it is carried at `scripts/contrast-check.py` inside this skill, which is what the command below resolves to. Literal edits recorded in `replace`: `(`contrast-check.py`, next to this `SKILL.md`)`; `point the script path at this skill's folder directly`. |
| Grill me — the alias | `mattpocock-skills/grill-me` | Upstream this is a whole skill: one line that routes to `grilling`. Merged, there is no second skill to call, so the line is kept as the trigger and the work happens in the `grilling` section of this file. |
