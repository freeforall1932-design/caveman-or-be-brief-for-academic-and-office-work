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
| antislop core — craftsmanship standard, R-rules, liveliness | `anti-slop/antislop-core` | The upstream install wizard and its pointer-block step are dropped: in this merged skill every sibling is already inside the same skill, so there is nothing for the agent to fetch and no entry file to edit. Not carried: First-Run Install Wizard, Already installed, and the user asks how to update. |
| antislop-human — contrast, keyboard, focus, states | `anti-slop/antislop-human` | The contrast checker no longer sits next to a standalone SKILL.md: it is carried at `scripts/contrast-check.py` inside this skill, which is what the command below resolves to. Literal edits recorded in `replace`: `(`contrast-check.py`, next to this `SKILL.md`)`; `point the script path at this skill's folder directly`. |
| Grill me — the alias | `mattpocock-skills/grill-me` | Upstream this is a whole skill: one line that routes to `grilling`. Merged, there is no second skill to call, so the line is kept as the trigger and the work happens in the `grilling` section of this file. |
| Caveman — the voice contract (upstream v3.2.0) | `caveman/caveman-voice` | Upstream original, replaces this repo's v2.x copy. Its 'Anti-slop and the voice' section is the honest bridge to the anti-slop filter; both are carried, and where anti-slop's own rule is stricter, `antislop-human` wins for prose (see the precedence table). |
| Caveman compress — memory and instruction files | `caveman/caveman-compress-upstream` | Different job from this repo's `caveman-review`/`caveman-compress` pair, which compress *documents*. Upstream compresses the instruction files the agent itself loads. Both are carried; pick by artifact. |
| Caveman review — one line per finding, in code order | `caveman/caveman-review-code` | Carried next to mattpocock's `code-review`, which wants an explanation per finding. The two disagree on output length on purpose: read the user's own skill for shape, this one for the severity ladder and the 'no praise, no hedging' rule. |
| Work pattern · investigate first | `caveman/investigate-first` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · lean build | `caveman/lean-build` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · surgical patch | `caveman/surgical-patch` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · safe refactor | `caveman/safe-refactor` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · migration | `caveman/migration` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Work pattern · verify and stop | `caveman/verify-and-stop` | Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen. |
| Grug — the full text of the site | `grug/grug-canonical` | The site's markdown source, so it carries page furniture: an empty anchor before each heading and a link to that anchor. The four `markup` transforms remove that scaffolding and nothing else; no word of grug's prose is changed. Read this instead of the compressed summary when the argument matters more than the rule. |
| What an agent can and cannot prove, per OWASP category | `strix/strix-owasp-coverage` | The transferable part of Strix is its honesty model, not its CLI: which OWASP categories an agent-driven review can actually cover from the outside, which are partial, and the rule that a clean exit code proves nothing about what was not analyzed. Stripping the run/re-run sections removes the commands this skill cannot execute; the coverage table and the reporting rules stay verbatim. Not carried: Run it. Literal edits recorded in `replace`: `Remediate with **fix-security-vulnerabilities-with-strix** and re-run to prove each exploit is closed. For ongoing coverage as the app changes, gate pull requests using **ci-security-scanning-with-strix**.`; `Strix's agents do the exploitation; this skill covers running it category-by-category and reporting coverage honestly.`. |
| Security review of a diff, in scope | `strix/strix-pr-review` | Not carried: Run it. Literal edits recorded in `replace`: `Hand results to **fix-security-vulnerabilities-with-strix**: patch the root cause (the shared authorization helper, not the one route), then re-run Strix to prove the exploit no longer works.`. |
| Triage, fix the root cause, report | `strix/strix-triage-fix` | The 'verify by re-running' section is dropped because every line of it is a `strix` command; the principle survives in the two carried sections above and below, which say to re-test and to treat a capped run as unfinished. Not carried: 3. Verify by re-running Strix. |
| Third-party integration, the additive way | `mem0/mem0-integration-principles` | This is the only part of mem0's skill set that is a rule rather than an SDK walkthrough, so it is the only part carried: keep one H2 section verbatim and drop the rest by name. Everything the dropped sections ask for (`npm view`, fetching docs at runtime, delegating to published skills) is not implementable here and would have been invented if kept. Not carried: Canonical sources (fetch before deciding anything), Agent-ready docs, Published Mem0 skills — delegate; do not reimplement, SDK source (read when docs are ambiguous), Quickstarts (for bootstrapping unfamiliar stacks), Skill delegation rules, Preconditions, Pipeline, Artifacts (all under `.mem0-integration/`), Modes, Invocation, Exit codes, Explicitly out of scope. Literal edits recorded in `replace`: `If no additive, gated fit exists after
   step 6 (plan), exit with code 1 and a rationale. A bad PR is worse
   than no PR.`. |
| Pick the diagram type, then be honest about the artifact | `archify/archify-method` | Three sections of a 1 456-word skill: the five-type router, the Mermaid mapping, and the reporting rule. The renderer sections (fast authoring path, delivery gates, setup and fallback, update awareness) are dropped by name because every one of them runs the Node toolchain. The three declared edits below exist because upstream keeps pointing at artifacts this bundle does not ship. Read the type table as a *choice of what to draw*, not as a validation step. Not carried: Existing candidate handoff, Fast authoring path, Update awareness, Delivery, Optional viewer capabilities, Setup and fallback. Literal edits recorded in `replace`: `run `node bin/archify.mjs guide "<scenario>" --json``; `then name them for the reader: use everyday `icon` values and `meta.legend` labels as in [Node icons](references/authoring-contract.md#node-icons).`; `Return the checked HTML as an absolute path, diagram type, validation summary, specification/artifact receipt, browser-evidence status, and truthful visual-review status. Do not claim success for a non-zero command or claim visual inspection you did not perform.`. |


## What was deliberately not merged

Everything vendored from a source is either routed into a reference file above, or
listed here with the reason it was cast aside. The build fails if a vendored `SKILL.md`
is neither, so this table cannot go stale while upstream grows.

| source | left out | why |
|---|---|---|
| `local` | skill `caveman` | The app's copy of this repo's v2.x-era voice skill, next to the universal copy already listed under not_routed. Both are superseded by JuliusBrussee/caveman v3.2.0, which is carried; three copies of one voice in one skill is noise, not redundancy. |
| `local` | skill `claude-reasoning-caveman` | The standalone `.skill` pack for grug-style reasoning in Claude Code: a zip of the same variant this bundle carries as `grug-reasoning`, plus its own install script. The install half is what the merge cannot use, and the text half would be the second copy. |
| `local` | file `caveman-compress.md` | the `app` copy is what every install path ships; the two differ only in frontmatter and app-vs-library wording, so one is carried. |
| `local` | file `caveman-review.md` | same as caveman-compress. |
| `local` | file `cut-lists.md` | byte-identical to be-brief-output's copy, which is carried. |
| `local` | file `caveman.md` | This repo's v2.x-era copy of the caveman voice skill. Superseded: the same skill is now carried from JuliusBrussee/caveman at the v3.2.0 tag, which is the version the user asked to sync against. Keeping both would ship two rulesets for one voice. |
| `mattpocock-skills` | not vendored: skills/in-progress/ (betas, several with SKILL.md) | Beta skills with no documentation pages, in an upstream directory that can vanish without warning; merging an unreleased beta into a published bundle means the bundle changes whenever a maintainer pushes an experiment. Re-check on each sync. |
| `mattpocock-skills` | not vendored: skills/deprecated/ | Empty upstream, and empty by policy: the directory exists to remember what was removed. |
| `caveman` | skill `megacave` | Classical-Chinese (wenyan) register. This repo ships English and Indonesian output only; a third register would need its own language routing, and 'translate into literary Chinese' is not implementable here. |
| `caveman` | skill `caveman-setup` | Installs the Caveman Cloud gateway, writes hooks and config files, and edits an entry file. This skill is read-only guidance: no installer, no hooks, no file to edit. |
| `caveman` | skill `caveman-learn` | Reads the user's chat history through the Caveman plugin and rewrites personal config files. Needs that plugin's storage; the same idea (learn the user's deletions) is already covered by `learn-in-public`. |
| `caveman` | skill `caveman-discover` | Searches a hosted skill registry over the network and installs results. No registry, no network write access, and a merged skill must not install anything. |
| `caveman` | skill `caveman-optimize` | Runs the plugin's own performance probes against a local daemon and rewrites its config. |
| `caveman` | skill `caveman-evidence-review` | Reviews evidence recorded by the Caveman plugin's own hooks; the artifact it reviews does not exist here. |
| `caveman` | skill `caveman-manage` | Add/remove/list/repair commands for the plugin install; every step needs the plugin's file layout and CLI. |
| `caveman` | skill `caveman-stats` | Reads a local token-accounting database written by the plugin's hooks and reports percentages. Without the hook there is nothing to count, and an invented number is the exact failure the skill warns about. |
| `caveman` | skill `caveman-help` | A menu of slash commands for the Caveman product (`/caveman ultra`, `/caveman status`…). Those commands do not exist in a merged skill; the equivalent behaviour is carried as the `ultracave` section instead. |
| `caveman` | not vendored: skills/caveman-compress/scripts/ (8.2k words of stdlib Python) and each skill's references/ | The deterministic rules in `caveman-compress` are carried; its scripts are not. The compression orchestrator shells out to an OpenAI-compatible endpoint (default localhost:11434, Ollama) for its semantic pass, and a skill that told you to start a local model server before compressing a file would be a different product. |
| `strix` | skill `penetration-testing-with-strix` | Whole skill is a driver for the `strix` binary (Docker image, LLM API key, live target). No binary ships with this skill, so every instruction in it would be a hallucination prompt. |
| `strix` | skill `web-app-penetration-testing` | Same: it configures and launches a Strix run against a URL. |
| `strix` | skill `api-security-testing` | Same, and its OWASP API Top 10 coverage notes are already quoted inside the carried `owasp-top-10-testing`. |
| `strix` | skill `ci-security-scanning-with-strix` | Writes a CI workflow that runs the Strix CLI; the file to write and the action to pin belong to the user's repo, not to this skill. |
| `strix` | skill `managed-pentesting-with-strix` | Describes Strix's paid managed-service API and portal. No agent-side procedure exists without that service. |
| `mem0` | skill `mem0` | Wiring the mem0 SDK into an app: needs `pip install mem0ai`, an API key and network access to api.mem0.ai. It is an integration tutorial, not a behaviour rule. |
| `mem0` | skill `mem0-cli` | Drives the `mem0` CLI, which is not installed and cannot be installed from a skill. |
| `mem0` | skill `mem0-vercel-ai-sdk` | Package-specific provider setup for one framework's version line. |
| `mem0` | skill `mem0-oss-to-platform` | A migration script between two hosted backends; both need credentials. |
| `mem0` | skill `mem0-test-integration` | Writes and runs a test suite against a live memory backend. |
| `mem0` | not vendored: each skill's references/ (SDK, API and provider docs) plus CLAUDE.md/AGENTS.md | Library and API documentation for a service this skill does not install. Only the one section of one skill here is a rule rather than a walkthrough, and that is what is carried. |
| `archify` | skill `archify-review` | Marked `internal: true` by its author and aimed at triaging Archify's own issues and PRs. Its value/cost/impact rubric is good, but the project it judges is not this one. |
| `archify` | not vendored: bin/ (472 KB), renderers/ (1.6 MB), schemas/ (72 KB), assets/ (720 KB), examples/ (4 MB), test/ (3.7 MB) | The `bin/` (472 KB), `renderers/` (1.6 MB), `schemas/` (72 KB), `assets/` (720 KB) and `examples/` (4 MB) are a Node 18 pipeline with npm deps. A skill cannot install them, and a diagram 'validated' by a renderer that is not present would be a fabricated artifact. Only the authoring judgement that survives without the tool is carried. |
| `archify` | not vendored: references/ (authoring-contract 3 769w, delivery-contract 5 809w, architecture-layout-repair 669w, brand-marks 455w) | Every one of them is a contract with the renderer: layout rules expressed as schema fields, delivery gates defined as CLI commands, and the repair procedure that ends in `finalize` and `visual-check`. Carrying them would put instructions in the bundle for commands that are not in the bundle, which is the failure mode this whole merge is built to avoid. |
