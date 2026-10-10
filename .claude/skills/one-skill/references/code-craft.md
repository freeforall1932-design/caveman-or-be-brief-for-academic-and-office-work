# Code craft — design, tests, debugging, comments

**Read this when:** writing or restructuring code, choosing a seam, diagnosing a bug, touching a comment

**Layer:** pocock's engineering discipline; antislop-code on comments

Loaded on demand: the always-on rules live in the skill's `SKILL.md`. The
bodies below are upstream text carried verbatim, with the per-section
provenance and every declared edit listed in `SOURCES.md` beside this file.

| section | from | load |
|---|---|---|
| [Caveman explore — read a codebase before touching it](#caveman-explore-read-a-codebase-before-touching-it) | `caveman` | always |
| [Cavecrew — what to delegate, and at what level](#cavecrew-what-to-delegate-and-at-what-level) | `caveman` | always |
| [TDD — red → green at agreed seams](#tdd-red-green-at-agreed-seams) | `mattpocock-skills` | always |
| [Codebase design — deep modules, seams, leverage](#codebase-design-deep-modules-seams-leverage) | `mattpocock-skills` | always |
| [Caveman review — one line per finding, in code order](#caveman-review-one-line-per-finding-in-code-order) | `caveman` | always |
| [Domain modelling — glossary and ADRs](#domain-modelling-glossary-and-adrs) | `mattpocock-skills` | always |
| [Diagnosing bugs — red loop first, then hypothesis](#diagnosing-bugs-red-loop-first-then-hypothesis) | `mattpocock-skills` | always |
| [Work pattern · investigate first](#work-pattern-investigate-first) | `caveman` | always |
| [Work pattern · lean build](#work-pattern-lean-build) | `caveman` | always |
| [Work pattern · surgical patch](#work-pattern-surgical-patch) | `caveman` | always |
| [Work pattern · safe refactor](#work-pattern-safe-refactor) | `caveman` | always |
| [Work pattern · migration](#work-pattern-migration) | `caveman` | always |
| [Work pattern · verify and stop](#work-pattern-verify-and-stop) | `caveman` | always |
| [Improve codebase architecture — scan, report, grill](#improve-codebase-architecture-scan-report-grill) | `mattpocock-skills` | command |
| [Prototype — throwaway, to answer one question](#prototype-throwaway-to-answer-one-question) | `mattpocock-skills` | always |
| [antislop-code — comment hygiene, code untouched](#antislop-code-comment-hygiene-code-untouched) | `anti-slop` | always |

---

## Caveman explore — read a codebase before touching it

> `caveman` / `caveman-explore` / the task starts with 'understand this repo' or the context window is being spent on file-by-file reading

You are FastContext, a fast, cheap, read-only repository explorer. Another agent
(the solver) delegates a localization question to you. Your only job is to find
WHERE the relevant code lives and report it as a compact list of file paths with
line ranges. You never edit files, run commands, or propose a solution.

How to work:

1. Issue several tool calls IN PARALLEL in your first turn — cast a broad net.
   Cover complementary hypotheses at once: likely path patterns (Glob), symbol and
   string matches (Grep), and reading the most promising files (Read). Do not probe
   one file at a time when you can fan out.
2. Follow the evidence over one or two more turns only if needed. Stop as soon as
   you can name the relevant locations. You are optimizing for the solver's token
   budget, so finish fast.
3. Only cite line ranges you actually read. Never invent or estimate a range, and
   never cite a range past the end of a file. A precise small range beats a vague
   large one.

Your reply MUST be ONLY an evidence block: one citation per line, nothing else.
No preamble, no explanation, no summary, no markdown headings. Use exactly this
shape, one per line:

  path/to/file.ext:START-END  reason it is relevant

Example reply:

  src/router/pick.go:42-71  route selection — where a model is chosen
  src/router/pick_test.go:18-40  the table test covering pick()

If you genuinely cannot find anything relevant, reply with the single line:

  no relevant locations found

That honest answer is better than a guess. The solver reads your citations and
nothing else from your work, so keep the list short, specific, and correct.

## Cavecrew — what to delegate, and at what level

> `caveman` / `cavecrew` / deciding whether a subagent/teammate should do the work, or writing their prompts

Cavecrew = three subagent presets that answer in ultracave voice (tool runs: one status line in, one out; nothing between routine calls). Same job as Anthropic defaults (`Explore`, edit-style agents, reviewer); difference is the tool-result they return is compressed, so main context shrinks per delegation.

### When to use cavecrew vs alternatives

| Task | Use |
|---|---|
| "Where is X defined / what calls Y / list uses of Z" | `cavecrew-investigator` |
| Same but you also want suggestions/architecture commentary | `Explore` (vanilla) |
| Surgical edit, ≤2 files, scope obvious | `cavecrew-builder` |
| New feature / 3+ files / cross-cutting refactor | Main thread, or `feature-dev:code-architect` if installed |
| Review diff, branch, or file for bugs | `cavecrew-reviewer` |
| Deep code review with rationale + alternatives | `Code Reviewer` (vanilla) if installed, else main thread |
| One-line answer you already know | Main thread, no subagent |

Rule of thumb: **if you'd want the subagent's output in 1/3 the tokens, pick cavecrew. If you'd want prose, pick vanilla.**

### Why this exists (the real win)

Subagent tool results get injected into main context verbatim. A vanilla `Explore` that returns 2k tokens of prose costs 2k tokens of main-context budget every time. The same finding from `cavecrew-investigator` comes back as a compressed `path:line` table instead. Across 20 delegations in one session that's the difference between context exhaustion and finishing the task.

### Output contracts

What main thread can rely on per agent:

**`cavecrew-investigator`**
```
<Header>:
- path:line — `symbol` — short note
totals: <counts>.
```
Or `No match.` Always file-path-first, line-number-attached, backticked symbols. Safe to grep with `path:\d+`.

**`cavecrew-builder`**
```
<path:line-range> — <change ≤10 words>.
verified: <re-read OK | mismatch @ path:line>.
```
Or one of: `too-big.` / `needs-confirm.` / `ambiguous.` / `regressed.` (terminal first token).

**`cavecrew-reviewer`**
```
path:line: <emoji> <severity>: <problem>. <fix>.
totals: N🔴 N🟡 N🔵 N❓
```
Or `No issues.` Findings sorted file → line ascending.

### Chaining patterns

**Locate → fix → verify** (most common):
1. `cavecrew-investigator` returns site list.
2. Main thread picks 1-2 sites, hands paths to `cavecrew-builder`.
3. `cavecrew-reviewer` audits the diff.

**Parallel scout** (when investigation is broad):
Spawn 2-3 `cavecrew-investigator` calls in one message (different angles: defs vs callers vs tests). Aggregate in main thread.

**Single-shot edit** (when site is already known):
Skip investigator. Hand exact path:line to `cavecrew-builder` directly.

### What NOT to do

- Don't use `cavecrew-builder` when you don't already know the file. Spawn investigator first or main thread will eat tokens passing context.
- Don't chain `cavecrew-investigator → cavecrew-builder` for a 5-file refactor. Builder will return `too-big.` and you'll have wasted a turn.
- Don't ask `cavecrew-reviewer` for "general feedback" — it returns findings only, no architecture opinions. Use `Code Reviewer` for that when installed.
- Don't expect prose. Cavecrew output is structured, sometimes terse to the point of cryptic. If a human will read it directly, paraphrase.

### Auto-clarity (inherited)

Subagents drop caveman → normal English for security warnings, irreversible-action confirmations, and any output where fragment ambiguity could be misread. Resume caveman after.

## TDD — red → green at agreed seams

> `mattpocock-skills` / `tdd` / building a feature or fixing a bug test-first

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read `GLOSSARY.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

### What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See [tests.md](#what-a-good-test-looks-like-tdd) for examples and [mocking.md](#mocking-tdd) for mocking guidelines.

### Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?" Give each proposed seam a one-line note on what it catches and what it misses.

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with "codebase-design" for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

### Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

### Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.

### What a good test looks like (tdd)

> carried verbatim from `upstream/mattpocock-skills/engineering/tdd/tests.md`, the same upstream directory as `tdd`.

### Good Tests

**Integration-style**: Test through real interfaces, not mocks of internal parts.

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

### Bad Tests

**Implementation-detail tests**: Coupled to internal structure.

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**Tautological tests**: Expected value restates the implementation, so the test passes by construction.

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

### Mocking (tdd)

> carried verbatim from `upstream/mattpocock-skills/engineering/tdd/mocking.md`, the same upstream directory as `tdd`.

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer test DB)
- Time/randomness
- File system (sometimes)

Don't mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

### Designing for Mockability

At system boundaries, design interfaces that are easy to mock:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create specific functions for each external operation instead of one generic function with conditional logic:

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means:
- Each mock returns one specific shape
- No conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint

## Codebase design — deep modules, seams, leverage

> `mattpocock-skills` / `codebase-design` / interface shape, module depth, where a seam goes

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this language and these principles wherever code is being designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

### Glossary

Use these terms exactly: don't substitute "component," "service," "API," or "boundary." Consistent language is the whole point.

**Module**: anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice. _Avoid_: unit, component, service.

**Interface**: everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_: API, signature (too narrow, they refer only to the type-level surface).

**Implementation**: what's inside a module, its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**: leverage at the interface. The amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_: a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it. _Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter**: a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).

**Leverage**: what callers get from depth. More capability per unit of interface they learn. One implementation pays back across N call sites and M tests.

**Locality**: what maintainers get from depth. Change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers. Fix once, fixed everywhere.

### Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

### Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts; they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

### Designing for testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params = simpler test setup.

### Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

### Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use depth-as-leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow: interface here includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.

### Going deeper

- **Deepening a cluster given its dependencies**, see [DEEPENING.md](#deepening-codebase-design): dependency categories, seam discipline, and replace-don't-layer testing.
- **Exploring alternative interfaces**, see [DESIGN-IT-TWICE.md](#design-it-twice-codebase-design): spin up parallel sub-agents to design the interface several radically different ways, then compare on depth, locality, and seam placement.

### Deepening (codebase-design)

> carried verbatim from `upstream/mattpocock-skills/engineering/codebase-design/DEEPENING.md`, the same upstream directory as `codebase-design`.

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [SKILL.md](#codebase-design-deep-modules-seams-leverage): **module**, **interface**, **seam**, **adapter**.

### Dependency categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

#### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable: merge the modules and test through the new interface directly. No adapter needed.

#### 2. Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem). Deepenable if the stand-in exists. The deepened module is tested with the stand-in running in the test suite. The seam is internal; no port at the module's external interface.

#### 3. Remote but owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

#### 4. True external (Mock)

Third-party services (Stripe, Twilio, etc.) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

### Seam discipline

- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a port unless at least two adapters are justified (typically production + test). A single-adapter seam is just indirection.
- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) as well as the external seam at its interface. Don't expose internal seams through the interface just because tests use them.

### Testing strategy: replace, don't layer

- Old unit tests on shallow modules become waste once tests at the deepened module's interface exist; delete them.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not internal state.
- Tests should survive internal refactors, since they describe behaviour, not implementation. If a test has to change when the implementation changes, it's testing past the interface.

### Design it twice (codebase-design)

> carried verbatim from `upstream/mattpocock-skills/engineering/codebase-design/DESIGN-IT-TWICE.md`, the same upstream directory as `codebase-design`.

When the user wants to explore alternative interfaces for a chosen deepening candidate, use this parallel sub-agent pattern. Based on "Design It Twice" (Ousterhout): your first idea is unlikely to be the best.

Uses the vocabulary in [SKILL.md](#codebase-design-deep-modules-seams-leverage): **module**, **interface**, **seam**, **adapter**, **leverage**.

### Process

#### 1. Frame the problem space

Before spawning sub-agents, write a user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](#deepening-codebase-design))
- A rough illustrative code sketch to ground the constraints, not a proposal, just a way to make the constraints concrete

Show this to the user, then immediately proceed to Step 2. The user reads and thinks while the sub-agents work in parallel.

#### 2. Spawn sub-agents

Spawn 3+ sub-agents in parallel. Each must produce a **radically different** interface for the deepened module.

Prompt each sub-agent with a separate technical brief (file paths, coupling details, dependency category from [DEEPENING.md](#deepening-codebase-design), what sits behind the seam). The brief is independent of the user-facing problem-space explanation in Step 1. Give each agent a different design constraint:

- Agent 1: "Minimize the interface: aim for 1–3 entry points max. Maximise leverage per entry point."
- Agent 2: "Maximise flexibility: support many use cases and extension."
- Agent 3: "Optimise for the most common caller: make the default case trivial."
- Agent 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."

Include both [SKILL.md](#codebase-design-deep-modules-seams-leverage) vocabulary and GLOSSARY.md vocabulary in the brief so each sub-agent names things consistently with the architecture language and the project's domain language.

Each sub-agent outputs:

1. Interface (types, methods, params, plus invariants, ordering, error modes)
2. Usage example showing how callers use it
3. What the implementation hides behind the seam
4. Dependency strategy and adapters (see [DEEPENING.md](#deepening-codebase-design))
5. Trade-offs: where leverage is high, where it's thin

#### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by **depth** (leverage at the interface), **locality** (where change concentrates), and **seam placement**.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated: the user wants a strong read, not a menu.

## Caveman review — one line per finding, in code order

> `caveman` / `caveman-review-code` / reviewing a diff and the report should be findings, not prose

> **Merge note.** Carried next to mattpocock's `code-review`, which wants an explanation per finding. The two disagree on output length on purpose: read the user's own skill for shape, this one for the severity ladder and the 'no praise, no hedging' rule.

Write code review comments terse and actionable. One line per finding. Location, problem, fix. No throat-clearing.

### Rules

**Format:** `L<line>: <problem>. <fix>.` — or `<file>:L<line>: ...` when reviewing multi-file diffs.

**Severity prefix (optional, when mixed):**
- `🔴 bug:` — broken behavior, will cause incident
- `🟡 risk:` — works but fragile (race, missing null check, swallowed error)
- `🔵 nit:` — style, naming, micro-optim. Author can ignore
- `❓ q:` — genuine question, not a suggestion

**Drop:**
- "I noticed that...", "It seems like...", "You might want to consider..."
- "This is just a suggestion but..." — use `nit:` instead
- "Great work!", "Looks good overall but..." — say it once at the top, not per comment
- Restating what the line does — the reviewer can read the diff
- Hedging ("perhaps", "maybe", "I think") — if unsure use `q:`

**Keep:**
- Exact line numbers
- Exact symbol/function/variable names in backticks
- Concrete fix, not "consider refactoring this"
- The *why* if the fix isn't obvious from the problem statement

### Examples

❌ "I noticed that on line 42 you're not checking if the user object is null before accessing the email property. This could potentially cause a crash if the user is not found in the database. You might want to add a null check here."

✅ `L42: 🔴 bug: user can be null after .find(). Add guard before .email.`

❌ "It looks like this function is doing a lot of things and might benefit from being broken up into smaller functions for readability."

✅ `L88-140: 🔵 nit: 50-line fn does 4 things. Extract validate/normalize/persist.`

❌ "Have you considered what happens if the API returns a 429? I think we should probably handle that case."

✅ `L23: 🟡 risk: no retry on 429. Wrap in withBackoff(3).`

### Auto-Clarity

Drop terse mode for: security findings (CVE-class bugs need full explanation + reference), architectural disagreements (need rationale, not just a one-liner), and onboarding contexts where the author is new and needs the "why". In those cases write a normal paragraph, then resume terse for the rest.

### Boundaries

Reviews only — does not write the code fix, does not approve/request-changes, does not run linters. Output the comment(s) ready to paste into the PR. "stop caveman-review" or "normal mode": revert to verbose review style.

## Domain modelling — glossary and ADRs

> `mattpocock-skills` / `domain-modeling` / terminology, GLOSSARY.md, ADRs

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

### File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

### During the session

#### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

#### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

#### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

#### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

#### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](#glossary-format-domain-modeling).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

#### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](#adr-format-domain-modeling).

### ADR format (domain-modeling)

> carried verbatim from `upstream/mattpocock-skills/engineering/domain-modeling/ADR-FORMAT.md`, the same upstream directory as `domain-modeling`.

ADRs live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

Create the `docs/adr/` directory lazily: only when the first ADR is needed.

### Template

```md
## {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why*, not in filling out sections.

### Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`): useful when decisions are revisited
- **Considered Options**: only when the rejected alternatives are worth remembering
- **Consequences**: only when non-obvious downstream effects need to be called out

### Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

### When to offer an ADR

All three of these must be true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it: you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

#### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library: just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it; otherwise someone will suggest GraphQL again in six months.

### Glossary format (domain-modeling)

> carried verbatim from `upstream/mattpocock-skills/engineering/domain-modeling/GLOSSARY-FORMAT.md`, the same upstream directory as `domain-modeling`.

### Structure

```md
## {Context Name}

{One or two sentence description of what this context is and why it exists.}

### Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

### Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

### Single vs multi-context repos

**Single context (most repos):** One `GLOSSARY.md` at the repo root.

**Multiple contexts:** A `GLOSSARY-MAP.md` at the repo root lists the contexts, where they live, and how they relate to each other:

```md
## Glossary Map

### Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

### Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

The skill infers which structure applies:

- If `GLOSSARY-MAP.md` exists, read it to find contexts
- If only a root `GLOSSARY.md` exists, single context
- If neither exists, create a root `GLOSSARY.md` lazily when the first term is resolved

When multiple contexts exist, infer which one the current topic relates to. If unclear, ask.

## Diagnosing bugs — red loop first, then hypothesis

> `mattpocock-skills` / `diagnosing-bugs` / broken, throwing, failing, slow

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring the codebase, read `GLOSSARY.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

### Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

### Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug (one that goes red on _this_ bug), you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

#### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

#### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight, a debugging superpower.

#### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not, so keep raising the rate until it's debuggable.

#### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a redacted captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

#### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** (a script path, a test invocation, a curl) that you have **already run at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring"; it must be able to _catch this specific bug_.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, **stop: jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

### Phase 2: Reproduce + minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

#### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut, and keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing**: removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

### Phase 3: Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it; proceed with your ranking if the user is AFK.

### Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

### Phase 5: Fix + regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail. If you forced the red by mutating code or a fixture, `diff` against a pristine copy to prove the mutation landed before you trust it.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

### Phase 6: Cleanup

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message, so the next debugger learns

## Work pattern · investigate first

> `caveman` / `investigate-first` / the cause is unknown, intermittent, or performance-shaped

> **Merge note.** Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen.

Gather evidence before changing product code.

- Separate observed symptom from inferred cause.
- Trace inputs, state transitions, ownership boundaries, and failure output.
- Rank hypotheses by evidence and cheap falsification value.
- Do not edit until one credible mechanism explains evidence.
- Stop exploration when evidence is sufficient to name cause or exact blocker.

Report cause and proof. Make no fix unless task authorizes implementation.

## Work pattern · lean build

> `caveman` / `lean-build` / about to add a feature, dependency, abstraction or flag

> **Merge note.** Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen.

Native Core's architecture-first simplicity remains mandatory. Turn feature into complete narrow outcome fitting system.

- Derive observable acceptance and explicit non-goals from request and repository.
- Trace entry point through layers owning invariants.
- Deliver coherent end-to-end path across responsible layers; never force work into one file, direct expression, or local patch.
- Reuse fitting seam. Refactor when patching duplicates behavior, weakens ownership, or hides root cause.
- Omit modes, providers, config, extensibility, and polish unless acceptance needs them.
- Add surface, dependency, service, config, or migration only for lifecycle design or acceptance; state material tradeoff.
- Keep work runnable; preserve Core safety.

Exercise path. Run focused proof. Stop when acceptance passes. Report only material omissions and trigger.

## Work pattern · surgical patch

> `caveman` / `surgical-patch` / making a small, reviewable change to existing code

> **Merge note.** Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen.

Reproduce failure first when economical; otherwise capture strongest available evidence.

- Trace symptom to responsible mechanism.
- Change narrowest layer that owns incorrect behavior.
- Preserve unrelated behavior and user changes.
- Avoid cleanup, renaming, and abstraction outside fix.
- Add only regression proof relevant to task.

Run focused proof plus nearest affected gate. Stop when failure is fixed and regression proof passes.

## Work pattern · safe refactor

> `caveman` / `safe-refactor` / restructuring without changing behaviour

> **Merge note.** Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen.

Define behavior-preservation boundary and establish verification before structural edits.

- Keep feature changes outside refactor.
- Move one ownership boundary at a time.
- Preserve public interfaces, failure behavior, ordering, and compatibility unless explicitly scoped.
- Keep intermediate states buildable and testable.
- Avoid dependency or configuration growth without correctness need.

Run same proof after change. Stop when behavior matches and requested structure is achieved.

## Work pattern · migration

> `caveman` / `migration` / moving data, schema or a whole codebase from one shape to another

> **Merge note.** Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen.

Map current readers, writers, data shape, compatibility window, and ownership before editing.

- Define forward path and rollback path.
- Preserve existing data; make destructive steps explicit and separately authorized.
- Keep mixed-version operation safe where rollout can overlap.
- Sequence expand, migrate, verify, then contract when applicable.
- Make retries idempotent and partial failure observable.
- Verify old and new paths at required transition stages.

Stop after requested stage passes; do not perform later destructive contraction implicitly.

## Work pattern · verify and stop

> `caveman` / `verify-and-stop` / deciding when work is done and evidence is good enough to stop

> **Merge note.** Upstream original of the six-work-pattern table in the always-on rules. The table stays in `SKILL.md` because it never turns off; this is the full text for when one pattern is chosen.

Translate acceptance conditions into smallest sufficient proof set.

- Reuse still-current results with matching repository state.
- Run focused checks before wider gates.
- Distinguish pass, fail, unavailable, and blocked exactly.
- Do not edit product code unless verification request includes fixes.
- Do not add polish, cleanup, or unrelated tests after criteria pass.

Stop immediately when acceptance proof is complete. Report commands, results, and unresolved risk only.

## Improve codebase architecture — scan, report, grill

> `mattpocock-skills` / `improve-codebase-architecture` / codebase health is the question

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Call the Skill tool with "codebase-design" for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion, and don't drift into "component," "service," "API," or "boundary."
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

### Process

#### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`GLOSSARY.md`) and any ADRs in the area you're touching first.

Then spawn a sub-agent to walk the codebase. Don't follow rigid heuristics; explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

#### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user (`xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows) and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals: use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram**: side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use GLOSSARY.md vocabulary for the domain, and the `/codebase-design` vocabulary for the architecture.** If `GLOSSARY.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](#html-report-format-improve-codebase-architecture) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

#### 3. Grilling loop

Once the user picks a candidate, call the Skill tool with "grilling" to walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize; call the Skill tool with "domain-modeling" to keep the domain model current as you go:

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Add the term to `GLOSSARY.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `GLOSSARY.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing; skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Call the Skill tool with "codebase-design" and use its design-it-twice parallel sub-agent pattern.

### HTML report format (improve-codebase-architecture)

> carried verbatim from `upstream/mattpocock-skills/engineering/improve-codebase-architecture/HTML-REPORT.md`, the same upstream directory as `improve-codebase-architecture`.

The architectural review is rendered as a single self-contained HTML file in the OS temp directory. Tailwind and Mermaid both come from CDNs. Mermaid handles graph-shaped diagrams reliably; hand-built divs and inline SVG handle the more editorial visuals (mass diagrams, cross-sections). Mix the two: don't lean on Mermaid for everything, it'll start to look generic.

### Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

### Header

Repo name, date, and a compact legend: solid box = module, dashed line = seam, red arrow = leakage, thick dark box = deep module. No introduction paragraph. Straight into the candidates.

### Candidate card

The diagrams carry the weight. Prose is sparse, plain, and uses the glossary terms (from the `/codebase-design` skill) without ceremony.

Each candidate is one `<article>`:

- **Title**: short, names the deepening (e.g. "Collapse the Order intake pipeline").
- **Badge row**: recommendation strength (`Strong` = emerald, `Worth exploring` = amber, `Speculative` = slate), plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **Files**: monospaced list, `font-mono text-sm`.
- **Before / After diagram**: the centrepiece. Two columns, side by side. See patterns below.
- **Problem**: one sentence. What hurts.
- **Solution**: one sentence. What changes.
- **Wins**: bullets, ≤6 words each. e.g. "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR callout** (if applicable): one line in an amber-tinted box.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

### Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same. Variety is part of the point.

#### Mermaid graph (the workhorse for dependencies / call flow)

Use a Mermaid `flowchart` or `graph` when the point is "X calls Y calls Z, and look at the mess." Wrap it in a Tailwind-styled card so it doesn't feel parachuted in. Style with classDef to colour leakage edges red and the deep module dark. Sequence diagrams work well for "before: 6 round-trips; after: 1."

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

#### Hand-built boxes-and-arrows (when Mermaid's layout fights you)

Modules as `<div>`s with borders and labels. Arrows as inline SVG `<line>` or `<path>` elements positioned absolutely over a relative container. Reach for this when you want the "after" diagram to feel like one thick-bordered deep module with greyed-out internals, since Mermaid won't render that with the right weight.

#### Cross-section (good for layered shallowness)

Stack horizontal bands (`h-12 border-l-4`) to show layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band labelled with the consolidated responsibility.

#### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module: one for interface surface area, one for implementation. Before: interface rectangle is nearly as tall as the implementation rectangle (shallow). After: interface rectangle is short, implementation rectangle is tall (deep).

#### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one box, with the now-internal calls shown faded inside it.

### Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace. Serif optional for headings (`font-serif` works well with stone/slate).
- Colour sparingly: one accent (emerald or indigo) plus red for leakage and amber for warnings.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Use `text-xs uppercase tracking-wider` for module labels inside diagrams, so they read as schematic, not as UI.
- The only scripts are the Tailwind CDN and the Mermaid ESM import. The report is otherwise static: no app code, no interactivity beyond Mermaid's own rendering.

### Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

### Tone

Plain English, concise, but the architectural nouns and verbs come straight from the `/codebase-design` skill. Concision is not an excuse to drift.

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

**Never substitute:** component, service, unit (for module) · API, signature (for interface) · boundary (for seam) · layer, wrapper (for module, when you mean module).

**Phrasings that fit the style:**

- "Order intake module is shallow: interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** name the gain in glossary terms: *"locality: bugs concentrate in one module"*, *"leverage: one interface, N call sites"*, *"interface shrinks; implementation absorbs the wrappers"*. Don't write *"easier to maintain"* or *"cleaner code"*, because those terms aren't in the glossary and don't earn their place.

No hedging, no throat-clearing, no "it's worth noting that…". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it. If a term isn't in the `/codebase-design` glossary, reach for one that is before inventing a new one.

## Prototype — throwaway, to answer one question

> `mattpocock-skills` / `prototype` / sanity-checking a state model or a UI direction

A prototype is **throwaway code that answers a question**. The question decides the shape.

### Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](#logic-branch-prototype). Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](#ui-branch-prototype). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

### Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user double-clicks. Either way, no thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Capture it when done.** Fold any validated decision into the real code, then capture the prototype itself as a **primary source**: commit it to a throwaway branch, out of main, and leave a context pointer to that branch on the implementation issue. Capture the answer too (the verdict and the question it settled) in the issue or a commit. The main branch keeps only the validated decision.

### Logic branch (prototype)

> carried verbatim from `upstream/mattpocock-skills/engineering/prototype/LOGIC.md`, the same upstream directory as `prototype`.

A single, self-contained HTML file (a **shareable demo**) that lets anyone drive a state model by clicking buttons. Use this when the question is about **business logic, state transitions, or data shape**: the kind of thing that looks reasonable on paper but only feels wrong once you push it through real cases.

Because it's one file with nothing to install, you can hand it to a non-developer (a designer, a PM, a domain expert) and let them feel the model for themselves. So it speaks their language, not the code's.

### When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where someone wants to **press buttons and watch state change**.

If the question is "what should this look like," this is the wrong branch. Use [UI.md](#ui-branch-prototype).

### Process

#### 1. State the question

Before writing code, write down what state model and what question you're prototyping. One paragraph, at the top of the demo (in a visible intro, not just a comment). A logic prototype that answers the wrong question is pure waste, so make the question explicit so it can be checked later, whether the user is watching now or returning to it AFK.

#### 2. Isolate the logic in a portable module

Put the actual logic (the bit that's answering the question) in a single `<script>` block written as a small, pure module that could be lifted out and dropped into the real codebase later. The page around it is throwaway; this module isn't.

The right shape depends on the question:

- **A pure reducer**: `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine**: explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state, just transformations.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick whichever shape best fits the question being asked, *not* whichever is easiest to wire to a page. Keep it pure: no DOM, no `document`, no button handlers reaching inside it. The page calls into it; nothing flows the other direction. This is what makes the prototype useful past its own lifetime: once the question's answered, the validated reducer / machine / function set lifts into the real module on its own.

#### 3. Build the shareable HTML file

One file, plain HTML/CSS/JS: no framework, no bundler, no server, everything inline so it opens by double-click and survives being emailed around. Anyone should be able to run it by opening it.

Write it for a non-developer. Every label is in **domain language**, not code: buttons and state read like the business, not the reducer. Explain in plain words what's happening.

Lay it out with a clean hierarchy, top to bottom:

1. **Title and one-line explanation** of what this demo lets you explore (the question from step 1).
2. **Current state**: the full relevant state, rendered as a readable panel (labelled fields, not a raw JSON dump), re-rendered after every click so the change is visible. Where it helps a non-developer follow, call out what just changed.
3. **Free-play buttons**: one button per action, always available, so anyone can poke at the model in any order. Each click dispatches its action and re-renders the state.
4. **Guided walkthroughs**: a set of **scenarios**, one per tab. Each tab holds a short plain-language description of the scenario (the situation it sets up and what to watch for) and underneath it, the ordered **buttons to press** for that scenario. Each step is a real button: clicking it performs that action and moves to the next step. Starting a walkthrough resets to a known initial state so the scenario runs the same way every time.

Choose scenarios that demonstrate the awkward cases, the ones hard to reason about on paper: the happy path, a tricky edge case, an attempt at something that should be illegal.

Keep it beautiful but restrained: clean typography, generous spacing, one accent colour. No animations, no gimmicks: nothing that competes with the state and the buttons.

#### 4. Hand it over

Send them the file, or open it for them. They'll click through the walkthroughs and free-play whenever they get to it; the interesting moments are when they say "wait, that shouldn't be possible" or "huh, I assumed X would be different"; those are the bugs in the _idea_, which is the whole point. If they want new actions or a new scenario, add them. Prototypes evolve.

#### 5. Capture the answer and the prototype

Once the prototype has answered its question, capture the answer, then capture the prototype the way the [SKILL](#prototype-throwaway-to-answer-one-question) describes. The logic-specific mapping: the validated reducer / machine / function set lifts into the real module (the decision, absorbed); the HTML shell rides along to the throwaway branch that keeps the prototype as a primary source, and being one self-contained file, it stays trivially re-runnable there.

### Anti-patterns

- **Don't add tests.** A prototype that needs tests is no longer a prototype.
- **Don't wire it to the real database.** Use in-memory state unless the question is specifically about persistence.
- **Don't generalise.** No "what if we wanted to support X later." The prototype answers one question.
- **Don't blur the logic and the page together.** If the pure module references the DOM, `document`, or button handlers, it's no longer liftable. Keep the page as a thin shell over a pure module.
- **Don't reach for a framework, bundler, or server.** One file the recipient double-clicks; a React app or a dev server defeats "shareable".
- **Don't ship the HTML shell into production.** The page is optimised for being clicked through by hand. The logic module behind it is the bit worth keeping.

### UI branch (prototype)

> carried verbatim from `upstream/mattpocock-skills/engineering/prototype/UI.md`, the same upstream directory as `prototype`.

Generate **several radically different UI variations** on a single route, switchable from a floating bottom bar. The user flips between variants in the browser, picks one (or steals bits from each), then throws the rest away.

If the question is about logic/state rather than what something looks like, this is the wrong branch. Use [LOGIC.md](#logic-branch-prototype).

### When this is the right shape

- "What should this page look like?"
- "I want to see a few options for this dashboard before committing."
- "Try a different layout for the settings screen."
- Any time the user would otherwise spend a day picking between three vague mockups in their head.

### Two sub-shapes: strongly prefer sub-shape A

A UI prototype is much easier to judge when it's **butting up against the rest of the app**: real header, real sidebar, real data, real density. A throwaway route on its own is a vacuum: every variant looks fine in isolation. Default to sub-shape A whenever there's a plausible existing page to host the variants. Only reach for sub-shape B if the prototype genuinely has no nearby home.

#### Sub-shape A: adjustment to an existing page (preferred)

The route already exists. Variants are rendered **on the same route**, gated by a `?variant=` URL search param. The existing data fetching, params, and auth all stay. Only the rendering swaps. This is the default; pick it unless there's a specific reason not to.

If the prototype is for something that doesn't yet have a page but *would naturally live inside one* (a new section of the dashboard, a new card on the settings screen, a new step in an existing flow), it's still sub-shape A. Mount the variants inside the host page.

#### Sub-shape B: a new page (last resort)

Only use this when the thing being prototyped genuinely has no existing page to live inside (e.g. an entirely new top-level surface, or a flow that can't be embedded anywhere sensible).

Create a **throwaway route** following whatever routing convention the project already uses. Don't invent a new top-level structure. Name it so it's obviously a prototype (e.g. include the word `prototype` in the path or filename). Same `?variant=` pattern.

Before committing to sub-shape B, sanity-check: is there really no existing page this could be embedded in? An empty route hides design problems that a populated one would expose.

In both sub-shapes the floating bottom bar is identical.

### Process

#### 1. State the question and pick N

Default to **3 variants**. More than 5 stops being radically different and starts being noise, so cap there.

Write down the plan in one line, in the prototype's location or a top-of-file comment:

> "Three variants of the settings page, switchable via `?variant=`, on the existing `/settings` route."

This works whether the user is here to push back or not.

#### 2. Generate radically different variants

Draft each variant. Hold each one to:

- The page's purpose and the data it has access to.
- The project's component library / styling system (TailwindCSS, shadcn, MUI, plain CSS, whatever).
- A clear exported component name, e.g. `VariantA`, `VariantB`, `VariantC`.

Variants must be **structurally different**: different layout, different information hierarchy, different primary affordance, not just different colours. Three slightly-tweaked card grids isn't a UI prototype, it's wallpaper. If two drafts come out too similar, redo one with explicit "do not use a card grid" guidance.

#### 3. Wire them together

Create a single switcher component on the route:

```tsx
// pseudo-code, adapt to the project's framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

For sub-shape A (existing page): keep all the existing data fetching above the switcher; only the rendered subtree changes per variant.

For sub-shape B (new page): the throwaway route under `/prototype/<name>` mounts the same switcher.

#### 4. Build the floating switcher

A small fixed-position bar at the bottom-centre of the screen with three pieces:

- **Left arrow**: cycles to the previous variant (wraps around).
- **Variant label**: shows the current variant key and, if the variant exports a name, that name too. e.g. `B (Sidebar layout)`.
- **Right arrow**: cycles forward (wraps around).

Behaviour:

- Clicking an arrow updates the URL search param (use the framework's router, e.g. `router.replace` on Next, `navigate` on React Router, etc) so the variant is shareable and reload-stable.
- Keyboard: `←` and `→` arrow keys also cycle. Don't intercept arrow keys when an `<input>`, `<textarea>`, or `[contenteditable]` is focused.
- Visually distinct from the page (e.g. high-contrast pill, subtle shadow) so it's obviously not part of the design being evaluated.
- Hidden in production builds: gate on `process.env.NODE_ENV !== 'production'` or an equivalent check, so a stray prototype merge can't ship the bar to users.

Put the switcher in a single shared component so both sub-shapes can reuse it. Locate it wherever shared UI lives in the project.

#### 5. Hand it over

Surface the URL (and the `?variant=` keys). The user will flip through whenever they get to it. The interesting feedback is usually **"I want the header from B with the sidebar from C"**, which is the actual design they want.

#### 6. Capture the answer and clean up

Once a variant has won, capture the answer (which variant and why), then capture the prototype the way the [SKILL](#prototype-throwaway-to-answer-one-question) describes. Fold the winner into the real code and move the rest onto the throwaway branch, not into main:

- **Sub-shape A**: fold the winner into the existing page; drop the losing variants and the switcher from main.
- **Sub-shape B**: promote the winning variant to a real route; drop the throwaway route and the switcher from main.

The full set of variants is the primary source, so it lands on the throwaway branch, not the bin, since variant components and the switcher left in the main branch rot fast and confuse the next reader.

### Anti-patterns

- **Variants that differ only in colour or copy.** That's a tweak, not a prototype. Real variants disagree about structure.
- **Sharing too much code between variants.** A shared `<Header>` is fine; a shared `<Layout>` defeats the point. Each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Read-only prototypes are fine. If a variant needs to mutate, point it at a stub: the question is "what should this look like", not "does the backend work".
- **Promoting the prototype directly to production.** The variant code was written under prototype constraints (no tests, minimal error handling). Rewrite it properly when you fold it in.

## antislop-code — comment hygiene, code untouched

> `anti-slop` / `antislop-code` / writing or editing code comments

> Anti Slop: Rules for AI Coding Agents. Code Comments skill

> Part of the antislop system. Read together with `antislop.md` (the core). This skill filters comments that read as generically AI (decorative, restating the obvious, stiff, loud) while preserving the comments that carry real information. It references core rules by number and never duplicates or renumbers them. Load it when the task writes or edits code comments.

### How to use this skill

- Load together with `antislop.md` whenever the task touches code comments. The core holds the mechanism (the purpose test, the three tiers, the Delivery Gate); this skill holds comment-specific depth.
- Every entry has the same shape: **Tell** (the pattern), **Why** (why it reads as slop), **Fix** (what to do instead), with the governing core rule cited as R-XX.
- **Scope guardrail:** this skill only modifies comments. Never modify executable code, identifiers, imports, formatting, indentation, whitespace, control flow, or logic. When in doubt, leave the code untouched.
- The Delivery Gate in the core remains the gate. The "Code Comment Checklist" at the end of this file is the comment-specific supplement to run alongside it.

### Comments That Add Nothing

#### Decorative Separators

- **Tell:** banner comments built from repeated characters, ALL CAPS labels, or box drawing around a section name: `// =======================` around `Authentication`, `// -------- WORKFLOW --------`, or a `/* ---- ROUTES ---- */` header.
- **Why:** the decoration is the message. A label wrapped in `=` or `-` signals "AI made this" without adding information, and ALL CAPS reads as shouting.
- **Fix:** replace with a single plain line, or remove entirely if the label adds nothing (R-31).

#### Restating the Obvious

- **Tell:** a comment that repeats what the next line or declaration already shows, like `// Initialize the variable` above `let count = 0`, `// User class` above `class User {}`, `// Validate user` above `function validateUser()`, or `const userAge = 25; // User age is 25`.
- **Why:** it doubles the reading load without adding anything. The code already says it; the comment just repeats it.
- **Fix:** remove and leave the line of code alone.

#### Workflow Narration

- **Tell:** comments that narrate the flow step by step, like `// Step 1: Validate input`, `// Step 2: Process request`, `// Step 3: Return response`, or `// First...`, `// Next...`, `// Finally...`.
- **Why:** the control flow is visible in the code itself. Numbering it reads as a checklist, not an explanation.
- **Fix:** remove. If the flow is genuinely hard to follow, that is a structure problem, not a missing comment problem.

#### Empty Labels

- **Tell:** generic labels with no information behind them: `// Main logic`, `// Core logic`, `// Business logic`, `// Helper function`, `// Entry point`, `// Error handling`, or `// Note: This is important.` / `// Important: Please read.`
- **Why:** the label names a category, not a fact. "Main logic" tells the reader nothing they could not infer from the code.
- **Fix:** remove unless the label carries specific information. "Note: retries happen only on 5xx" earns its place; "Note: this is important" does not.

#### Vague Placeholders

- **Tell:** comments that promise future work without saying what: `// TODO: Improve this`, `// Future improvements`, `// Additional optimization can be added here`, `// Add more validation`.
- **Why:** a vague TODO is noise. It names a feeling (this could be better) instead of a task (what, and why).
- **Fix:** remove. Keep a TODO only when it names a specific task with enough context to act on.

#### Signature Echo

- **Tell:** documentation that only restates the signature, like a JSDoc block that repeats `@param price The price.` and `@returns Total price.` for a function whose name and parameters already say all of it.
- **Why:** docs that echo the signature add length, not understanding. The reader learns nothing new.
- **Fix:** simplify or remove the echo. Keep documentation that explains business rules, edge cases, assumptions, algorithms, limitations, side effects, API behavior, or security implications. Never strip real documentation.

#### Decorative Emoji

- **Tell:** emoji used as decoration in comments, like `// ✅ Validation` or `// 🚀 Performance`.
- **Why:** emoji is visual noise in code, and the specific set (✅, 🚀, 🔒) is the AI default vocabulary.
- **Fix:** replace with plain English, or remove if the label adds nothing.

#### End Markers

- **Tell:** comments that only mark the end of a block, like `} // end if`, `# End of function`, or `// End processOrder`.
- **Why:** the closing brace already ends the block. The marker exists out of habit, not need.
- **Fix:** remove. In the rare case an end marker genuinely helps a long file, keep it only where it prevents confusion, not as a habit.

### How It Should Read

#### The Over-Explained Comment

- **Tell:** one comment that runs on for several lines, stacking reasons, context, and history around a fact that fits in one line: a four-line block explaining that a stub sits on PATH, which release introduced the workaround, and what broke before it. Every sentence is true. The length is the tell.
- **Why:** a person leaves a note, a generator writes a case. Padding a one-line fact into a paragraph, building a "because X, so Y, and therefore Z" chain, or citing the issue number and the version that fixed it are the same flourish as any other AI pattern, and they bury the one line that matters under the ones that do not.
- **Fix:** cut to the constraint alone: one line, two at most, never three. Keep the platform trap, the silent failure, the protocol rule, the performance cost. Drop the issue number, the version history, and the reasoning chain.

#### Line-by-Line Narration

- **Tell:** a comment on every trivial statement, narrating each line as it is written: `// Initialize count`, then `// Loop items`, then `// Get item`, then `// Increment`, then `// Return result`.
- **Why:** when every line is commented, none of the comments matter. The reader has to check each one to find the one that carries meaning.
- **Fix:** write one concise comment per logical block instead of one per line. If the block needs no comment, write none.

#### Stiff or Loud Wording

- **Tell:** comments that sound formal, long, or shout: "This function is responsible for validating whether the supplied credentials are valid before continuing with the authentication process", or `// MAIN LOGIC` in caps.
- **Why:** formal and loud wording reads as generated, not as an engineer leaving a note for the next person.
- **Fix:** write short, sentence-case lines in a natural developer voice: `// Validate credentials before issuing a token.` Good comments explain why, not what, and they stay short.

### Not a Ban (preserve these)

Never remove comments that explain:

- business logic and intent
- architectural decisions
- security considerations
- performance trade-offs
- concurrency behavior
- protocol details
- API contracts
- workarounds
- edge cases and assumptions
- licensing and legal notices

Example that must stay:

```js
// Stripe may retry webhook deliveries for up to three days.
// Ignore duplicate events using the event ID.
```

A comment earns its place when it explains something the code does not already show: the reason, the constraint, the non-obvious behavior.

Earning a place says what may stay, never how long it may run. A workaround note is one line about the workaround, not a paragraph about it. The example above is two lines because two facts are real, not because two lines is a target. This list is the most common reason a comment survives a review it should not: the content is legitimately valuable, so the length goes unexamined. Value is not length.

### Code Comment Checklist

Run these alongside the core Delivery Gate when the task touches comments. All answers must be **yes**:

- [ ] Does every comment add information the code does not already show? (R-31)
- [ ] Do the comments avoid decorative separators, ALL CAPS banners, and box-drawn headers?
- [ ] Do the comments avoid restating the obvious line, declaration, or signature?
- [ ] Do the comments avoid step-by-step workflow narration?
- [ ] Do the comments avoid empty labels and vague TODOs that name no task?
- [ ] Do the comments avoid decorative emoji and end markers?
- [ ] Is the comment density one per logical block, not one per line?
- [ ] Is every comment one line, or two only when the second carries a new fact?
- [ ] Do the remaining comments read short, natural, and in sentence case?
- [ ] Is the scope guardrail held: only comments changed, the code untouched?
