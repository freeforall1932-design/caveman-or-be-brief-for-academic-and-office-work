# SkillOpt integration — train the skills instead of hand-tuning them

This directory connects this repository to
[**SkillOpt**](https://github.com/microsoft/SkillOpt) (via the
[`freeforall1932-design/SkillOpt-fork`](https://github.com/freeforall1932-design/SkillOpt-fork)),
a text-space optimizer that trains natural-language skills for frozen LLM
agents.

SkillOpt treats **the skill document as the trainable state of a frozen
model**. It runs scored rollouts, reflects on the failures, and applies
bounded add / delete / replace edits behind a held-out validation gate. The
deployed artifact is a compact `best_skill.md` that costs **zero extra
inference-time calls**.

That maps onto this repo unusually well: the skills here *are* markdown
documents, and the argument about whether to cut a clause is exactly the kind
of thing a validation gate can settle with data instead of opinion.

---

## What was added

```
skillopt-integration/
├── caveman_skillopt/                 # installable package
│   ├── register.py                   # injects the env into SkillOpt's CLI registry
│   ├── train.py                      # python -m caveman_skillopt.train
│   ├── eval_only.py                  # python -m caveman_skillopt.eval_only
│   ├── score.py                      # offline scoring, no API calls
│   └── envs/caveman_brief/
│       ├── adapter.py                # EnvAdapter wiring
│       ├── dataloader.py             # train / val / test splits
│       ├── rollout.py                # one episode = one compression task
│       ├── evaluator.py              # ← the philosophy, as a number
│       ├── metrics.py                # deterministic token / fact / code metrics
│       ├── prompts/analyst_*.md      # reflection prompts for the optimizer
│       └── skills/initial*.md        # seed skills, one per philosophy family
├── configs/                          # one YAML per variant
│   ├── _base_/default.yaml
│   ├── default.yaml                  # all registers mixed
│   ├── be-brief.yaml · caveman.yaml · grug.yaml · coding-agent.yaml
├── data/caveman_brief_split/         # 45 items, stratified 27 / 9 / 9
├── examples/                         # reference + naive predictions
├── scripts/build_dataset.py          # rebuild the splits deterministically
└── tests/                            # 39 tests
```

**No SkillOpt source was vendored.** The environment plugs into an installed
SkillOpt through its documented extension points (`EnvAdapter`,
`SplitDataLoader`, and the lazy `_ENV_REGISTRY` that each CLI script owns), so
`pip install --upgrade skillopt` keeps working.

---

## Install

```bash
pip install skillopt            # the optimizer
pip install -e skillopt-integration
```

Working from a SkillOpt checkout (for example the fork) instead of the wheel:

```bash
export SKILLOPT_SRC=/path/to/SkillOpt
```

## Run

```bash
# Academic / office prose (the repo's daily driver)
python -m caveman_skillopt.train --config skillopt-integration/configs/be-brief.yaml

# Terse coding-agent output, official caveman contract
python -m caveman_skillopt.train --config skillopt-integration/configs/caveman.yaml

# Internal grug reasoning + professional answer
python -m caveman_skillopt.train --config skillopt-integration/configs/grug.yaml

# Unified coding-agent variant, Qwen Code as the target
python -m caveman_skillopt.train --config skillopt-integration/configs/coding-agent.yaml
```

Every flag from SkillOpt's own `train.py` works unchanged:

```bash
python -m caveman_skillopt.train --config skillopt-integration/configs/be-brief.yaml \
    --cfg-options train.num_epochs=6 optimizer.learning_rate=6 model.target=gpt-4.1
```

The run writes to `runs/<variant>/`, including the validation-gated
`best_skill.md`. Promote that file back into `.claude/skills/` or
`pseudo-skills/` once you are happy with the numbers.

---

## The reward function

`envs/caveman_brief/evaluator.py` is the heart of this integration. Whatever
it rewards is what the trained skill will optimise for, so every check maps
back to a rule in one of the three upstream philosophies:

| Check | Weight | Source of truth |
|---|---|---|
| Fact / number / citation retention | 0.35 | official caveman — *"facts are the entire point of a document"* |
| Code fidelity (byte-exact) | 0.15 | this repo's CODE PRESERVATION rule + *"Code blocks unchanged"* |
| Compression achieved | 0.20 | the deletion test, mechanically applied |
| Register fidelity | 0.20 | be-brief's two-modes rule; official caveman's token traps |
| Hedge retention | 0.10 | official caveman — *"deleting a hedge can turn a true claim into a false one"* |

The **hard gate** (what SkillOpt's validation gate counts as a pass) fires on
the things that make an output *wrong* rather than merely suboptimal:

- a required fact, number, citation or genuine hedge was dropped
- a code block was not reproduced byte-for-byte
- the grug voice leaked into user-facing output
- an invented abbreviation (`cfg`/`impl`/`req`/`res`/`fn`) or a decorative `→` appeared
- **zero compression** — "copy the input verbatim" is the degenerate optimum
  that preserves every fact while achieving nothing, so it is gated out
  deliberately

Two calibration details worth knowing, because they were bugs before they
were design decisions:

- Inflection is ignored when matching facts. A compression that turns "delays"
  into "delayed" has not lost the fact.
- Items whose answer must carry a required code block get a lower compression
  target. Required code is uncompressible, so holding those tasks to a
  prose-level reduction would punish a perfect answer for the code it was
  told to emit.

### Scoring without spending tokens

```bash
python -m caveman_skillopt.score \
    --split-dir skillopt-integration/data/caveman_brief_split \
    --split test \
    --predictions skillopt-integration/examples/predictions-good.json
```

Exits `0` only when every scored item passes the hard gate, so it drops
straight into CI as a regression check on a shipped skill.

The two shipped baselines show the reward function discriminates:

| Baseline | Mean soft reward | Hard pass rate |
|---|---|---|
| `examples/predictions-good.json` (hand-written reference) | 0.978 | 100% |
| `examples/predictions-naive.json` (source echoed back) | 0.638 | 0% |

---

## The four registers

One environment, four output contracts. Train them together
(`configs/default.yaml`) or separately, which is what the per-variant configs
do — see [`coding-agents/philosophy/conflicts.md`](../coding-agents/philosophy/conflicts.md)
for why they are kept apart.

| Register | Output contract | Seed skill |
|---|---|---|
| `be_brief` | Professional prose, full grammar, zero wasted words | `skills/initial.md` |
| `caveman` | Terse, fragments allowed, code never touched | `skills/initial_caveman.md` |
| `unified` | Grug reasons, prose answers, code stays exact | `skills/initial_coding_agent.md` |
| `grug_reasoning` | Scored on the internal `<thinking>` trace *and* the visible answer | `skills/initial_grug.md` |

## Dataset

45 hand-authored items, stratified 27 train / 9 val / 9 test across
`academic_prose`, `office_email`, `code_assist`, and `agent_reply`, in English
and Indonesian. Not scraped, and deliberately small — the point is a clean,
checkable signal, not scale. Rebuild with:

```bash
python skillopt-integration/scripts/build_dataset.py
```

Ground truth is asserted in `tests/test_dataloader.py`: every `must_keep` and
`hedges` entry is verified to actually appear in its source, because a reward
function that penalises facts that were never there is pure noise.

## Tests

```bash
pip install -e "skillopt-integration[dev]"
pytest skillopt-integration/tests -q
```

39 tests. The reward-function tests encode philosophy, not just behaviour —
for example, `test_fact_loss_beats_compression_gain` asserts that a shorter
output which drops data scores below a longer one that keeps it.
