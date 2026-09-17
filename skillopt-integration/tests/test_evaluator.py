"""Tests for the caveman_brief reward function.

These assert that the reward function encodes the philosophy rather than
merely running: a compression that drops a fact must score worse than one
that keeps it, invented abbreviations must cost more than they save, and
code must never be touched.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caveman_skillopt.envs.caveman_brief.evaluator import evaluate  # noqa: E402
from caveman_skillopt.envs.caveman_brief.metrics import (  # noqa: E402
    compression_ratio,
    estimate_tokens,
    split_reasoning,
    strip_code_spans,
)

SOURCE = (
    "It is important to note that, over the course of the observation period, "
    "a significant number of the shipments that were processed experienced delays "
    "which could possibly be attributed to handover procedures between shifts. "
    "In conclusion, handover procedures were found to be a major contributing factor."
)

GOOD = "Many shipments processed during the observation period were delayed, mainly due to gaps in shift-handover procedures."


def _item(**overrides):
    item = {
        "id": "t1",
        "task_type": "academic_prose",
        "register": "be_brief",
        "language": "en",
        "source": SOURCE,
        "instruction": "Tighten this.",
        "must_keep": ["shipments", "delays", "handover procedures"],
        "must_keep_numbers": [],
        "hedges": [],
        "code_spans": [],
        "target_compression": 0.55,
        "max_output_tokens": 400,
    }
    item.update(overrides)
    return item


# ── metrics ──────────────────────────────────────────────────────────────────


def test_token_estimate_is_monotone():
    assert estimate_tokens("") == 0
    assert estimate_tokens("hello") < estimate_tokens("hello world again")


def test_compression_ratio_bounds():
    assert compression_ratio("word " * 100, "word " * 100) == 0.0
    assert compression_ratio("word " * 100, "word " * 25) == pytest.approx(0.75, abs=0.02)
    assert compression_ratio("word", "word " * 500) == 0.0  # grew → clamped to 0


def test_strip_code_spans_removes_fences_and_latex():
    text = "Prose here.\n```python\nx = cfg.impl()\n```\nAnd $E = mc^2$ inline `code`."
    stripped = strip_code_spans(text)
    assert "cfg.impl()" not in stripped
    assert "mc^2" not in stripped
    assert "Prose here." in stripped


def test_split_reasoning_extracts_trace():
    out = "<thinking>internal grug thought</thinking>Visible professional answer."
    trace, visible = split_reasoning(out)
    assert "internal grug thought" in trace
    assert trace not in visible
    assert visible == "Visible professional answer."


def test_split_reasoning_no_tags():
    trace, visible = split_reasoning("Just an answer.")
    assert trace == ""
    assert visible == "Just an answer."


# ── the deletion test, mechanically ──────────────────────────────────────────


def test_good_compression_scores_high_and_passes_gate():
    score = evaluate(_item(), GOOD)
    assert score.hard == 1
    assert score.fact_retention == 1.0
    assert score.compression > 0.6
    assert score.soft > 0.85


def test_identity_copy_fails_on_compression():
    score = evaluate(_item(), SOURCE)
    assert score.hard == 0
    assert "no_compression_or_grew" in score.violations or \
        any("under_compressed" in v for v in score.violations)


def test_dropping_a_fact_is_a_hard_failure():
    # Same length as GOOD, but "handover procedures" is gone.
    dropped = "Many shipments processed during the observation period were delayed for reasons that remain unclear."
    score = evaluate(_item(), dropped)
    assert score.hard == 0
    assert any("lost_span" in v for v in score.violations)
    assert score.fact_retention < 1.0


def test_fact_loss_beats_compression_gain():
    """A short output that drops data must score below a longer one that keeps it."""
    keep = "Shipments delayed. Handover procedures are the cause, affecting shipments broadly."
    drop = "Shipments delayed."
    score_keep = evaluate(_item(), keep)
    score_drop = evaluate(_item(), drop)
    assert score_drop.soft < score_keep.soft


# ── hedges ───────────────────────────────────────────────────────────────────


def test_deleting_a_genuine_hedge_fails_the_gate():
    item = _item(hedges=["may"], must_keep=["handover procedures"])
    passing = "Delays may stem from handover procedures between shifts."
    failing = "Delays stem from handover procedures between shifts."
    assert evaluate(item, passing).hard == 1
    assert evaluate(item, failing).hard == 0


# ── code fidelity ────────────────────────────────────────────────────────────


def test_code_must_stay_byte_exact():
    code = "df = df.dropna(subset=['revenue'])\n"
    item = _item(code_spans=[code], task_type="code_assist", must_keep=[])
    exact = f"Drop the nulls.\n```python\n{code}```"
    compressed = "Drop the nulls.\n```python\ndf=df.dropna(subset=['revenue'])\n```"
    assert evaluate(item, exact).hard == 1
    assert evaluate(item, compressed).hard == 0


def test_code_in_source_must_survive_even_when_not_declared():
    code = "print('hi')\n"
    source = f"Please improve this.\n```python\n{code}```\nIt is too slow."
    item = _item(source=source, must_keep=[], must_keep_numbers=[])
    kept = f"Vectorise the loop.\n```python\n{code}```"
    assert evaluate(item, kept).hard == 1


# ── token traps ──────────────────────────────────────────────────────────────


def test_invented_abbreviations_fail_the_gate():
    bad = "Cfg issue. Impl ships late. Req unclear. Handover procedures cause shipment delays."
    score = evaluate(_item(), bad)
    assert score.hard == 0
    assert "invented_abbreviation" in score.violations


def test_arrow_in_prose_fails_the_gate():
    bad = "Shipments delayed → handover procedures."
    score = evaluate(_item(must_keep=["shipments"]), bad)
    assert score.hard == 0
    assert "arrow_in_prose" in score.violations


def test_arrow_inside_code_is_not_punished():
    code = "f = lambda x: x -> y\n"
    item = _item(code_spans=[code], task_type="code_assist", must_keep=[])
    out = f"Use the mapping.\n```python\n{code}```"
    assert evaluate(item, out).hard == 1


# ── grug must stay internal ──────────────────────────────────────────────────


def test_grug_voice_leak_fails_the_gate():
    leaked = "Grug think handover procedures cause shipment delays. Complexity very bad."
    score = evaluate(_item(), leaked)
    assert score.hard == 0
    assert "grug_voice_leaked" in score.violations


def test_grug_voice_allowed_inside_trace_only():
    item = _item(register="grug_reasoning")
    out = (
        "<thinking>sniff: user want tight paragraph. fear: lose the cause. "
        "plan: cut throat-clearers, keep cause. act: rewrite. "
        "speak: professional prose.</thinking>"
        "Many shipments were delayed, mainly due to handover procedures."
    )
    score = evaluate(item, out)
    assert score.hard == 1
    assert "grug_voice_leaked" not in score.violations


def test_grug_trace_flow_is_scored():
    item = _item(register="grug_reasoning")
    full = (
        "<thinking>sniff: tighten. fear: drop the cause. plan: cut fluff. "
        "act: rewrite. speak: professional.</thinking>"
        "Many shipments were delayed, mainly due to handover procedures."
    )
    partial = (
        "<thinking>ok just rewriting it now.</thinking>"
        "Many shipments were delayed, mainly due to handover procedures."
    )
    assert evaluate(item, full).register_fidelity > evaluate(item, partial).register_fidelity


def test_grug_trace_over_budget_is_flagged():
    item = _item(register="grug_reasoning", reasoning_budget_tokens=40)
    long_trace = "<thinking>sniff fear plan act speak " + "word " * 300 + "</thinking>Answer with shipments and delays."
    assert any("trace_over_budget" in v for v in evaluate(item, long_trace).violations)


# ── registers differ ─────────────────────────────────────────────────────────


def test_caveman_register_tolerates_fragments():
    caveman = "Bug in auth middleware. Token expiry check use `<` not `<=`. Fix:"
    brief = _item(register="be_brief", must_keep=["auth middleware", "token expiry"])
    score = evaluate(brief, caveman)
    assert score.register_fidelity < 1.0  # broken grammar costs something
    assert score.hard == 1  # but fragments keep the facts, so the gate opens

    caveman_item = _item(register="caveman", must_keep=["auth middleware", "token expiry"])
    assert evaluate(caveman_item, caveman).hard == 1


def test_unknown_register_falls_back_to_be_brief():
    assert evaluate(_item(register="nonsense"), GOOD).hard == 1


# ── reward shaping invariants ────────────────────────────────────────────────


def test_soft_reward_stays_in_unit_interval():
    for output in (GOOD, SOURCE, "", "x", GOOD * 50):
        score = evaluate(_item(), output)
        assert 0.0 <= score.soft <= 1.0
        assert score.hard in (0, 1)


def test_over_token_budget_fails_the_gate():
    item = _item(max_output_tokens=20)
    assert evaluate(item, GOOD * 10).hard == 0
