# Secure and harden — what an agent can and cannot prove about a codebase

**Read this when:** a security review, an OWASP-shaped audit, or findings to triage

**Layer:** Security layer. **Authorization first**: these procedures are for a codebase or deployment the user owns or is engaged to test. Do not point any of it at a third-party system. Methodology and reporting are transferable; live exploitation is not part of this skill.

Loaded on demand: the always-on rules live in the skill's `SKILL.md`. The
bodies below are upstream text carried verbatim, with the per-section
provenance and every declared edit listed in `SOURCES.md` beside this file.

| section | from | load |
|---|---|---|
| [What an agent can and cannot prove, per OWASP category](#what-an-agent-can-and-cannot-prove-per-owasp-category) | `strix` | always |
| [Security review of a diff, in scope](#security-review-of-a-diff-in-scope) | `strix` | always |
| [Triage, fix the root cause, report](#triage-fix-the-root-cause-report) | `strix` | always |
| [Application security testing, scoped and stated](#application-security-testing-scoped-and-stated) | `strix` | always |

---

## What an agent can and cannot prove, per OWASP category

> `strix` / `strix-owasp-coverage` / asked for a security audit, an OWASP review, or 'is this app secure?'

> **Merge note.** The transferable part of Strix is its honesty model, not its CLI: which OWASP categories an agent-driven review can actually cover from the outside, which are partial, and the rule that a clean exit code proves nothing about what was not analyzed. Stripping the run/re-run sections removes the commands this skill cannot execute; the coverage table and the reporting rules stay verbatim.

> *(not carried here: Run it. The command to run is not here; the coverage judgement and the reporting rules are, and they are what carry over.)*

The OWASP Top 10 is a taxonomy of risk categories, not a test suite — "OWASP Top 10 testing" means exercising each category against the real application and reporting what's actually exploitable. Strix's agents do the exploitation. What this skill carries is the category-by-category coverage model and the reporting rules, so a review done without Strix is scoped and reported the same honest way.

**Use the current edition: [OWASP Top 10:2025](https://owasp.org/Top10/)** (8th installment, superseding 2021). Ask the user before targeting an older edition — some compliance checklists still reference 2021, and a report labelled with the wrong edition is misleading. Key differences from 2021: **SSRF is folded into A01**, **A03 Software Supply Chain Failures** expands the old "Vulnerable and Outdated Components", and **A10 Mishandling of Exceptional Conditions** is new; A02 Security Misconfiguration moved 5→2.

Install, LLM setup, and the managed-cloud alternative: **penetration-testing-with-strix**. For a run with no Docker and no LLM key, the same binary drives the managed platform: `strix cloud login`, then `strix cloud scans start ...` (details in **managed-pentesting-with-strix**).

### What is and is not testable by an agent

Be straight with the user about this — claiming a clean sweep of all ten is misleading.

| Category (2025) | Coverage |
|---|---|
| A01 Broken Access Control (incl. SSRF) | **Strong** — cross-user/tenant access, privilege escalation, IDOR, and SSRF (including blind, via out-of-band callbacks) are all exploit-validated. Needs two accounts plus a privileged one to prove the authorization half. |
| A02 Security Misconfiguration | **Strong** — debug endpoints, verbose errors, permissive CORS, missing hardening, default credentials, exposed admin surfaces. |
| A03 Software Supply Chain Failures | **Partial** — version fingerprinting, and vulnerable/outdated dependency review when source is supplied. Build-system and distribution-infrastructure compromise (the broader half of this category) is out of scope for a runtime scan — pair with SCA plus build-provenance controls. |
| A04 Cryptographic Failures | **Partial** — transport config, unencrypted data in transit, secrets and tokens leaked in responses. At-rest crypto and key management need source or infra review. |
| A05 Injection | **Strong** — SQL/NoSQL/command/template injection and XSS, exploit-validated. |
| A06 Insecure Design | **Partial** — business-logic abuse (price/quantity tampering, workflow skipping, race conditions) is found where reachable; design intent still needs human review and threat modelling. |
| A07 Authentication Failures | **Strong** — auth bypass, weak session/token handling, password-reset and MFA flaws. |
| A08 Software or Data Integrity Failures | **Partial** — insecure deserialization and unsigned-update paths where reachable; CI/CD trust boundaries are not runtime-testable. |
| A09 Security Logging & Alerting Failures | **Not testable from outside** — requires reviewing the logging and alerting pipeline. State this rather than reporting it as passed. |
| A10 Mishandling of Exceptional Conditions | **Partial** — agents actively probe error handling and fail-open behavior (malformed input, forced errors, race and timeout conditions) and report what leaks or bypasses a control; exhaustive coverage of internal error paths needs source review. |

For APIs, run the same exercise against the **OWASP API Security Top 10 (2023)** — API1 BOLA, API3 Broken Object Property Level Authorization (2019's excessive data exposure + mass assignment merged), API5 broken function-level authorization — using the **api-security-testing** skill.

### Report honestly

From `strix_runs/<run>/`, group `vulnerabilities/*.md` by category and state, per category: what was attempted, what was proven, and what could not be assessed (A09 always; A03/A04/A06/A08/A10 partially). Label the report with the edition used. Verify each PoC yourself before it goes in front of the user.

A `0` exit code means nothing exploitable was proven **in what was analyzed** — check `run.json` status and cost against `--max-budget`; a budget-capped run is not a completed assessment.

### Then fix and re-test

Remediate with the triage-fix procedure in this same layer and re-test to prove each exploit is closed. For ongoing coverage as the app changes, gate pull requests with a scanner run in CI; that pipeline belongs to the user's repo and is not configured here.

## Security review of a diff, in scope

> `strix` / `strix-pr-review` / reviewing a PR or a recent change for security regressions

> *(not carried here: Run it. Upstream-only content; nothing to fetch inside a merged skill.)*

White-box security review with Strix: the agents read the source to build a model of routes, sinks, and authorization checks, then attempt real exploitation. Findings come with a proof-of-concept, so the output is a short list of proven issues rather than the hundreds of "potential" hits a pattern-matching scanner produces.

Install, LLM setup, all flags, and the managed-cloud path are in the **penetration-testing-with-strix** skill. For a run with no Docker and no LLM key, the same binary drives the managed platform: `strix cloud login`, then `strix cloud scans start ...` (details in **managed-pentesting-with-strix**).

## Local working tree
strix -n -t ./ --scan-mode standard --max-budget 15

## A GitHub repo directly
strix -n -t https://github.com/org/app --max-budget 15

## Monorepo: point at the service that matters, not the whole tree
strix -n -t ./services/checkout --max-budget 20

## Only what a branch changed (whole-repo review is wasteful on a large repo)
strix -n -t ./ --scope-mode diff --diff-base origin/main --max-budget 10
```

A local path is mounted into the sandbox **writable**, so the agents can modify it. Run against a clean checkout.

Two things sharply improve results:

1. **Add a running instance of the app.** `-t ./ -t http://host.docker.internal:3000` lets the agents confirm exploitability against live behavior instead of reasoning about it statically — this is the difference between "this looks unsafe" and a validated finding. If nothing is running, static-only findings should be described as unconfirmed.
2. **Scope the review.** Point at the risky subtree and say what matters:
   ```bash
   strix -n -t ./services/api --max-budget 15 \
     --instruction "Focus on the authorization layer in src/auth and every route under src/routes/admin. Multi-tenant app: tenant id comes from the JWT. Flag any query that filters by object id without also filtering by tenant."
   ```
   Tenancy model, trust boundaries, and which inputs are attacker-controlled are things the agents cannot infer reliably — tell them.

### Reviewing a pull request instead of the whole repo

For diff-scoped review of a branch or PR (and blocking merges on findings), use **ci-security-scanning-with-strix** — it covers diff scoping, PR comments, and SARIF upload to GitHub code scanning. The managed platform can also review PRs directly via API (**managed-pentesting-with-strix**).

### Read the results

In `strix_runs/<run>/`: `penetration_test_report.md` (start here), `vulnerabilities/*.md` (one per finding, with PoC and remediation), `vulnerabilities.json` / `.csv`, `findings.sarif` (upload to code scanning), `run.json`.

Before reporting to the user, open each finding and check the PoC actually demonstrates impact. Report file and line alongside the exploit so the fix is obvious.

Exit `0` means nothing exploitable was proven in what was analyzed — not that the codebase is clean. Check `run.json` status and cost against `--max-budget`, and note which paths went unreviewed if the run was capped.

### Complementary tooling

This is exploit-validated review, not an exhaustive inventory. Keep a dependency scanner (SCA) and secret scanning in place for complete coverage of known-CVE dependencies and committed credentials; use this for the logic, authorization, and injection bugs those tools structurally cannot find.

### Fix and verify

Hand results to the triage-fix procedure in this same layer: patch the root cause (the shared authorization helper, not the one route), then re-run the project's own scan to prove the exploit no longer works.

## Triage, fix the root cause, report

> `strix` / `strix-triage-fix` / turning scanner or pentest findings into changes

> **Merge note.** The 'verify by re-running' section is dropped because every line of it is a `strix` command; the principle survives in the two carried sections above and below, which say to re-test and to treat a capped run as unfinished.

> *(not carried here: 3. Verify by re-running Strix. Upstream-only content; nothing to fetch inside a merged skill.)*

Turn validated Strix findings into minimal, correct fixes — and prove they work by re-scanning.

### 1. Triage

Get the findings from wherever the scan ran:

- **OSS CLI** — artifacts in `strix_runs/<run-name>/`:
  - `vulnerabilities/*.md` — one finding per file: description, severity, PoC steps or script, affected code locations, remediation guidance.
  - `vulnerabilities.json` — the same findings as JSON (ids, severity, CWE/CVE, `code_locations` with `fix_before`/`fix_after` suggestions when available).
- **Cloud (app.strix.ai)** — pull findings with the CLI: `strix cloud vulns list --scan-id <scan-id> --json` (or `strix cloud scans get <scan-id> --json | jq '.vulnerabilities'`, or `strix cloud vulns list --severity critical` org-wide). Each finding carries `severity, cwe, endpoint, method, impact, technical_analysis, poc_description, poc_script_code` and, for code findings, `code_file`/`code_diff`/`code_before`/`code_after`. After a fix is verified, mark it with `strix cloud vulns update <id> --status fixed`. See the **managed-pentesting-with-strix** skill for `strix cloud login` and scopes.

Order work by severity: critical → high → medium → low. Every Strix finding was validated with a working proof-of-concept, so do not dismiss findings as false positives without re-testing the PoC yourself.

### 2. Fix

For each finding:

1. Reproduce it with the PoC from the finding file when feasible.
2. Fix the root cause, not the specific payload (parameterize every query instead of blocking one string, and enforce authorization in the handler instead of hiding the endpoint).
3. Prefer the framework's built-in defense (ORM parameterization, template auto-escaping, CSRF middleware, centralized authz) over ad-hoc sanitization.
4. Keep the diff minimal and apply the repo's existing patterns. Finding files often include `fix_before`/`fix_after` snippets — use them as a starting point, not verbatim.

Common finding classes and expected fixes: injection → parameterization/escaping at the sink; IDOR/broken access control → object-level authorization checks; SSRF → allowlist + block internal ranges; XSS → context-aware output encoding + CSP; secrets exposure → rotate the secret AND remove it from code/history; auth issues → fix the server-side check (never client-side).

## Re-test just the changed files (fast). Resolve the repo's real default
## branch instead of assuming origin/main (many repos use master/develop).
## Avoid the current branch's own upstream as the base — its merge base with
## HEAD would be HEAD, giving an empty diff and a falsely clean result.
DIFF_BASE=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)
## origin/HEAD can be a dangling symbolic ref — keep it only if its target exists.
git rev-parse --verify --quiet "$DIFF_BASE" >/dev/null 2>&1 || DIFF_BASE=""
if [ -z "$DIFF_BASE" ]; then
  for b in origin/main origin/master origin/develop; do
    git rev-parse --verify --quiet "$b" >/dev/null && DIFF_BASE="$b" && break
  done
fi
## No silent fallback: a guess like HEAD~1 would cover only the last commit of a
## multi-commit fix branch. If no base resolves, ask the user for the base branch
## (or use the focused --instruction verification below, which needs no diff base).
[ -n "$DIFF_BASE" ] || { echo "Set DIFF_BASE to the branch your fix will merge into." >&2; exit 1; }
strix -n -t ./ --scan-mode quick --scope-mode diff --diff-base "$DIFF_BASE" --max-budget 5

## Or re-test with the original finding as focus (no diff base needed)
strix -n -t ./ --instruction "Verify the SQL injection in app/api/search.py is fixed. Original PoC: <poc>" --max-budget 5
```
Exit codes: `2` = findings remain (read the new `strix_runs/<run>/vulnerabilities/` and iterate); `0` = clean **for what was analyzed**. Before trusting a `0`, confirm the run wasn't cut short — check `run.json` for a completed status and compare its `llm_usage.cost` with `--max-budget`: a hard budget stop leaves `status: "stopped"`, but a run that wrapped up on a budget warning records `"completed"` with partial coverage. Give verification enough budget to finish, and prefer re-running the specific PoC as the ground-truth signal.

**Cloud:** rerun with the same config and re-poll, then confirm the finding no longer appears:
```bash
new_id=$(curl -sS "$BASE/scans/$scan_id/rerun" "${auth[@]}" -X POST | jq -r .scan_id)
## poll GET /scans/$new_id until completed, then check its vulnerabilities[]
```
Or, if the cloud scan came from a repo/PR, trigger a fresh PR review on the fix branch (`POST /pr-reviews/start`). The platform also retests a single finding directly: `POST /api/v1/vulnerabilities/{vulnerabilityId}/retest`.

- Also re-run the PoC manually when it is a simple request/script — fastest signal.
- Run the project's own test suite to make sure the fix does not break behavior.

### 4. Report

Summarize per finding: severity, root cause, fix applied (file:line), verification result (re-scan clean / PoC no longer reproduces). Never include live secrets in the report; if a secret leaked, state that rotation is required.

## Application security testing, scoped and stated

> `strix` / `strix-appsec-baseline` / the user wants a security test plan for one application, with its scope written down

Entry point for "make my application secure" requests, where the target is not yet a single URL or repo. The job here is to pick the right test per asset, run it, and produce one ranked plan — not to run everything at maximum depth.

Install, LLM setup, all CLI flags, and the managed-cloud path live in the **penetration-testing-with-strix** skill. Read it first if `strix --version` fails. For a run with no Docker and no LLM key, the same binary drives the managed platform: `strix cloud login`, then `strix cloud scans start ...` (details in **managed-pentesting-with-strix**).

Only test assets the user owns or is authorized to test. Confirm authorization before the first run, and prefer staging over production, because the agents send real exploit payloads and can change data.

### 1. Map the assets

Ask (or read from the repo) and write the answers down before scanning:

- **Source** — one repo, a monorepo, several services? Which languages/frameworks?
- **Running environments** — is there a staging deployment? A public production site? A local dev server only?
- **APIs** — REST, GraphQL, gRPC? Is there an OpenAPI/GraphQL schema?
- **Authentication** — can you get two test accounts in different tenants? Most high-impact bugs need them.
- **Constraints** — out-of-scope paths, whether production may be touched, budget and wall-clock limits.

If there is no staging environment and production is off limits, say so early. A code-only review is still valuable, but it cannot prove exploitability against a live app.

### 2. Pick the right test per asset

| Asset | Skill to use |
| --- | --- |
| Repository or working tree | **find-security-vulnerabilities-in-code** |
| Live web app or staging site | **web-app-penetration-testing** |
| REST/GraphQL/gRPC API | **api-security-testing** |
| Assessment mapped to OWASP categories | **owasp-top-10-testing** |
| Every pull request, continuously | **ci-security-scanning-with-strix** |
| No Docker, no LLM key, or a report an auditor will accept | **managed-pentesting-with-strix** |

Those skills carry the flags, credential handling, and result-reading details. Do not duplicate their instructions here.

Sequence for a first assessment:

1. Review the code. It is the cheapest run and it maps the authorization model.
2. Pentest staging with credentials, and pass the repo as a second target so the agents keep source context.
3. Add CI scanning, so later regressions are caught without another manual pass.

Run one asset at a time and read each report before starting the next. Findings from the code review make the live run sharper.

### 3. Consolidate into one plan

Findings arrive per run in `strix_runs/<run>/`. Merge them into a single list and rank by **proven impact**, not by scanner severity:

1. Validated exploits reachable without authentication.
2. Validated cross-tenant or privilege-escalation issues.
3. Validated issues needing an authenticated account.
4. Unproven observations (configuration, dependency, and hardening notes) — flag as such, and never present them as confirmed vulnerabilities.

Deduplicate: the same root cause often surfaces in both the code review and the live pentest.

### 4. Be honest about coverage

State plainly what was *not* tested — assets with no staging environment, categories a black-box run cannot reach (logging and alerting, supply-chain integrity, insecure design), and any run that hit its budget or turn cap before finishing. Check `run.json` status and cost against `--max-budget` for each run. An empty result set from a truncated scan is not a clean bill of health.

Then remediate with **fix-security-vulnerabilities-with-strix**, which re-runs Strix against each fix to prove the exploit no longer works.
