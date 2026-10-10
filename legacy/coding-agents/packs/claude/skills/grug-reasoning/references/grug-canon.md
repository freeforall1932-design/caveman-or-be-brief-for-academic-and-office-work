# The grug canon

Compressed from [grugbrain.dev](https://grugbrain.dev/). Internal reading — this
voice never reaches the user.

## Complexity

> **Complexity very, very bad.**

The biggest brain is the one that says no. Every abstraction, dependency, mode
and config knob is a permanent tax. The magic word is **"no"**.

## 80/20

Most of the value sits in a small slice. Find that slice, build it, stop.

## Chesterton's Fence

Before you change or delete something, understand why it exists. If you cannot
say why, you are not ready to change it.

## Prototype early

Prototype the **riskiest** part first, not the easiest. Prototypes exist to be
thrown away.

## Refactoring

Make the change easy, then make the easy change. Refactor in small steps. Wait
for a genuine cut point before abstracting — **two uses is not a pattern**.

## Testing

**Integration tests are the sweet spot.** Test behaviour at the seam where
components meet. Unit-test the genuinely tricky logic. Do not chase coverage
numbers for their own sake.

## Performance

Premature optimization is a complexity generator. Measure, then optimise the
measured hot path.

## DRY in balance

The right amount of DRY depends on the factor, not on a rule. Some duplication
is cheaper than the wrong abstraction.

## Types, generics, closures

Great in small doses. Grug likes them "like salt" — a little improves everything,
too much ruins the dish.

## Tools and dependencies

Adding a dependency is adding a system you do not control. Prefer the standard
library; prefer the tool already present.

## Scale

Do not design for a scale you do not have. Solve today's problem, keep the seam
clean for tomorrow.

## Teams and process

Big process is complexity too. Small teams, clear ownership, short feedback
loops. Meetings that could be code review should be code review.

## Debugging

Reproduce first. Bisect. Do not guess — grug says *"grug not sure"* rather than
guessing. Change one thing at a time.

## Stop condition

Stop when acceptance proof is complete. The last 10% of polish usually costs
more than it returns.
