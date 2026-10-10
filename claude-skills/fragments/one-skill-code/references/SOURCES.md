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
| Grug reasoning — internal, never shown | `local/grug-reasoning` | Not carried: Reference material, Language. |
| The unified workflow — sniff, fear, plan, act, speak | `local/unified-workflow` | Not carried: Reference material, Language. |
| Grug engine — the full internal reasoning rule set | `local/grug-engine` | Kept alongside the short `grug-reasoning` section because it holds what that one omits: hard length budgets, the sentence and paragraph rules for the internal trace, the word-swap table, the abbreviation trap and the continuation protocol for a truncated context. Not carried: CRITICAL DISTINCTION: TWO MODES, LANGUAGE, RALPH WIGGUM LOOP (Optional Iteration), STICKY REASONING MODE, EXIT PHRASES (Return to normal reasoning). |
| Grill me — the alias | `mattpocock-skills/grill-me` | Upstream this is a whole skill: one line that routes to `grilling`. Merged, there is no second skill to call, so the line is kept as the trigger and the work happens in the `grilling` section of this file. |
| Caveman review — one line per finding, in code order | `caveman/caveman-review-code` | Carried next to mattpocock's `code-review`, which wants an explanation per finding. The two disagree on output length on purpose: read the user's own skill for shape, this one for the severity ladder and the 'no praise, no hedging' rule. |
| Work pattern · investigate first | `caveman/investigate-first` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · lean build | `caveman/lean-build` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · surgical patch | `caveman/surgical-patch` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · safe refactor | `caveman/safe-refactor` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · migration | `caveman/migration` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · verify and stop | `caveman/verify-and-stop` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| What an agent can and cannot prove, per OWASP category | `strix/strix-owasp-coverage` | The transferable part of Strix is its honesty model, not its CLI: which OWASP categories an agent-driven review can actually cover from the outside, which are partial, and the rule that a clean exit code proves nothing about what was not analyzed. Stripping the run/re-run sections removes the commands this skill cannot execute; the coverage table and the reporting rules stay verbatim. Not carried: Run it. Literal edits recorded in `replace`: `Remediate with **fix-security-vulnerabilities-with-strix** and re-run to prove each exploit is closed. For ongoing coverage as the app changes, gate pull requests using **ci-security-scanning-with-strix**.`; `Strix's agents do the exploitation; this skill covers running it category-by-category and reporting coverage honestly.`. |
| Security review of a diff, in scope | `strix/strix-pr-review` | Not carried: Run it. Literal edits recorded in `replace`: `Hand results to **fix-security-vulnerabilities-with-strix**: patch the root cause (the shared authorization helper, not the one route), then re-run Strix to prove the exploit no longer works.`. |
| Triage, fix the root cause, report | `strix/strix-triage-fix` | The 'verify by re-running' section is dropped because every line of it is a `strix` command; the principle survives in the two carried sections above and below, which say to re-test and to treat a capped run as unfinished. Not carried: 3. Verify by re-running Strix. |
| Third-party integration, the additive way | `mem0/mem0-integration-principles` | This is the only part of mem0's skill set that is a rule rather than an SDK walkthrough, so it is the only part carried: keep one H2 section verbatim and drop the rest by name. Everything the dropped sections ask for (`npm view`, fetching docs at runtime, delegating to published skills) is not implementable here and would have been invented if kept. Not carried: Canonical sources (fetch before deciding anything), Agent-ready docs, Published Mem0 skills — delegate; do not reimplement, SDK source (read when docs are ambiguous), Quickstarts (for bootstrapping unfamiliar stacks), Skill delegation rules, Preconditions, Pipeline, Artifacts (all under `.mem0-integration/`), Modes, Invocation, Exit codes, Explicitly out of scope. Literal edits recorded in `replace`: `If no additive, gated fit exists after
   step 6 (plan), exit with code 1 and a rationale. A bad PR is worse
   than no PR.`. |
