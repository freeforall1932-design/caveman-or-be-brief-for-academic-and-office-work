"""
Reward function for the caveman_brief SkillOpt environment.

This module is where the philosophy becomes a number. SkillOpt does not
train weights — it edits the skill document so that rollouts score higher.
Whatever we reward here is therefore *exactly* what the trained skill will
optimise for, so every check below maps back to a rule in one of the three
upstream philosophies:

===================  ======================================================
Check                Source of truth
===================  ======================================================
fact / number /      Official caveman "What never to cut"
citation retention   (JuliusBrussee/caveman) — facts are the entire point
                     of a document; never trade them for brevity.

hedge retention      Official caveman — deleting a genuine hedge turns a
                     true careful claim into a false overconfident one.

code fidelity        This repo's CODE PRESERVATION rule + official caveman
                     "Code blocks unchanged. Errors quoted exact."

compression          The deletion test, mechanically: no loss → cut.

no invented          Official caveman: cfg/impl/req/res/fn are split the
abbreviations        same by the tokenizer — zero tokens saved, and the
                     reader still has to decode them.

no arrows            Official caveman: → is its own token, saves nothing.

banned polite        Official caveman: no throat-clearing, no tool-call
filler / narration   narration, no pleasantries.

grug voice must      This repo's caveman-be-brief TWO MODES rule: grug is
stay internal        the internal voice, the user sees professional prose.

reasoning trace      This repo's SNIFF → FEAR → PLAN → ACT → SPEAK flow and
coverage             the internal word budgets (<80 / 150 / 400 words).
===================  ======================================================

Registers
---------
``be_brief``       Professional prose, zero wasted words, never broken
                   grammar. The academic/office contract of this repo.
``caveman``        Terse output, fragments allowed, articles droppable.
                   The official JuliusBrussee/caveman contract.
``unified``        Fused: grug reasons, prose stays professional, code and
                   commands stay byte-exact.
``grug_reasoning`` Scores an internal grug trace *plus* the visible answer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .metrics import (
    compression_ratio,
    contains_number,
    contains_span,
    count_sentences,
    estimate_tokens,
    extract_code_spans,
    extract_numbers,
    iter_phrases,
    split_reasoning,
    strip_code_spans,
)

REGISTERS = ("be_brief", "caveman", "unified", "grug_reasoning")

# ── Soft-score weights (must sum to 1.0) ────────────────────────────────────
WEIGHTS: dict[str, float] = {
    "fact_retention": 0.35,
    "code_fidelity": 0.15,
    "compression": 0.20,
    "register_fidelity": 0.20,
    "hedge_retention": 0.10,
}

# ── Banned prose patterns ───────────────────────────────────────────────────
# Inventing these saves zero tokens: the tokenizer splits them exactly like
# the full word, and the reader pays to decode them. (official caveman)
#
# The list is deliberately kept to the exact set official caveman names.
# Wider lists produce false positives on legitimate words — "auth" is
# authentication, "res" is resources, "diff" is a real noun — and a reward
# function that punishes correct output teaches the wrong lesson.
INVENTED_ABBREV_RE = re.compile(
    r"(?<![A-Za-z0-9_])(cfg|impl|req|res|fn)(?![A-Za-z0-9_])",
    re.IGNORECASE,
)
# → is its own token; -> in prose (as opposed to code) is the same mistake.
ARROW_RE = re.compile(r"→|(?<![A-Za-z0-9_])->(?![A-Za-z0-9_])")

# Grug voice leaking into user-facing output. (caveman-be-brief: NEVER output
# grug voice to user.)
GRUG_LEAK_RE = re.compile(
    r"(?<![A-Za-z])(grug|me think|grug think|complexity very bad|big brain|"
    r"shiney rock|spirit demon|club)(?![A-Za-z])",
    re.IGNORECASE,
)

# Polite filler / tool-call narration the agent should have cut.
POLITE_FILLER = (
    "sure!", "certainly!", "of course", "great question", "good question",
    "i'd be happy to", "happy to help", "thanks for asking",
    "let me", "i'll start by", "first, i'll", "i will now", "let's begin",
    "here is the compressed version", "in summary,", "to summarize",
    "as an ai", "i hope this helps", "please note", "it should be noted",
)
THROAT_CLEARERS = (
    "it is important to note", "it should be noted that", "this paper aims to",
    "as we all know", "moving forward", "that being said", "at the end of the day",
    "in conclusion,", "as mentioned previously", "this section will now discuss",
    "needless to say", "it is worth mentioning",
    "perlu diketahui", "perlu dicatat", "dapat disimpulkan", "pada dasarnya",
    "ke depannya", "dengan ini", "seperti yang telah disebutkan",
)

# Grug reasoning flow markers (SNIFF → FEAR → PLAN → ACT → SPEAK).
FLOW_STAGES: dict[str, tuple[str, ...]] = {
    "sniff": ("sniff", "what user want", "what does the user want", "understand the ask"),
    "fear": ("fear", "what go wrong", "what could go wrong", "risk"),
    "plan": ("plan", "steps", "approach"),
    "act": ("act", "execute", "do it", "run"),
    "speak": ("speak", "answer", "output", "respond"),
}


@dataclass
class ScoreBreakdown:
    """Everything the optimizer (and a human) needs to see about one rollout."""

    fact_retention: float = 0.0
    hedge_retention: float = 0.0
    code_fidelity: float = 0.0
    compression: float = 0.0
    register_fidelity: float = 0.0
    soft: float = 0.0
    hard: int = 0
    violations: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "soft": round(self.soft, 4),
            "hard": self.hard,
            "fact_retention": round(self.fact_retention, 4),
            "hedge_retention": round(self.hedge_retention, 4),
            "code_fidelity": round(self.code_fidelity, 4),
            "compression": round(self.compression, 4),
            "register_fidelity": round(self.register_fidelity, 4),
            "violations": self.violations,
            "details": self.details,
        }


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _score_facts(item: dict, answer: str) -> tuple[float, list[str], dict[str, Any]]:
    """Retention of anything the reader would lose if it were deleted."""
    problems: list[str] = []
    keep_spans = [str(s) for s in item.get("must_keep", []) if str(s).strip()]
    keep_numbers = item.get("must_keep_numbers", []) or []
    citations = item.get("must_keep_citations", []) or []

    checks: list[bool] = []

    for span in keep_spans:
        ok = contains_span(answer, span)
        checks.append(ok)
        if not ok:
            problems.append(f"lost_span:{span[:40]}")

    for number in keep_numbers:
        ok = contains_number(answer, number)
        checks.append(ok)
        if not ok:
            problems.append(f"lost_number:{number}")

    for citation in citations:
        ok = contains_span(answer, str(citation))
        checks.append(ok)
        if not ok:
            problems.append(f"lost_citation:{str(citation)[:40]}")

    # Automatic backstop: any number present in the source and materially
    # sized should survive, even if the item did not enumerate it.
    source_numbers = [
        n for n in extract_numbers(item.get("source", ""))
        if any(ch.isdigit() for ch in n) and len(re.sub(r"[^\d]", "", n)) >= 2
    ]
    auto_missing = [
        n for n in source_numbers
        if n not in [str(x) for x in keep_numbers] and not contains_number(answer, n)
    ]
    if auto_missing:
        # Worth a penalty but not a hard failure — the model may legitimately
        # fold "1,200" into "1.2k" in prose. Only flag egregious loss.
        if len(auto_missing) > max(1, len(source_numbers) // 2):
            problems.append(f"lost_numbers_auto:{','.join(auto_missing[:5])}")
            checks.append(False)

    score = 1.0 if not checks else sum(1 for c in checks if c) / len(checks)
    details = {
        "checked": len(checks),
        "missing": [p for p in problems if p.startswith(("lost_span", "lost_number", "lost_citation"))],
    }
    return score, problems, details


def _score_hedges(item: dict, answer: str) -> tuple[float, list[str]]:
    """Genuine hedges in technical/medical/legal/financial claims must survive."""
    hedges = [str(h) for h in item.get("hedges", []) if str(h).strip()]
    if not hedges:
        return 1.0, []
    hay = answer.lower()
    missing = [h for h in hedges if h.lower() not in hay]
    problems = [f"lost_hedge:{h}" for h in missing]
    return _clamp(1.0 - len(missing) / len(hedges)), problems


def _score_code(item: dict, answer: str) -> tuple[float, list[str]]:
    """Code blocks are byte-for-byte artifacts, never prose to compress."""
    required = [str(c) for c in item.get("code_spans", []) if str(c).strip()]
    if not required:
        # No code in this item — also make sure the model did not mangle
        # code that *was* in the source.
        source_code = extract_code_spans(item.get("source", ""))
        present = [c for c in source_code if c.strip() in answer]
        if source_code and len(present) < len(source_code):
            return 0.0, ["code_lost_from_source"]
        return 1.0, []

    ok = [c for c in required if c in answer]
    problems = [f"code_not_verbatim:{i}" for i, c in enumerate(required) if c not in answer]
    return _clamp(len(ok) / len(required)), problems


def _score_compression(item: dict, answer: str, source: str) -> tuple[float, list[str]]:
    """Reward reaching the target reduction; punish growing or barely cutting."""
    target = float(item.get("target_compression", 0.5))
    floor = float(item.get("min_compression", target * 0.5))
    ratio = compression_ratio(source, answer)

    if ratio <= 0.0:
        return 0.0, ["no_compression_or_grew"]
    if ratio >= target:
        return 1.0, []
    if ratio < floor:
        return _clamp(ratio / floor * 0.5), [f"under_compressed:{ratio:.2f}<{floor:.2f}"]
    # Linear ramp between floor and target.
    span = max(1e-6, target - floor)
    return _clamp(0.5 + 0.5 * ((ratio - floor) / span)), []


def _score_register(
    register: str, item: dict, answer: str, trace: str
) -> tuple[float, list[str]]:
    """Register-specific contract checks on the *visible* answer."""
    problems: list[str] = []
    prose = strip_code_spans(answer)
    penalty = 0.0

    # ── Universal bans (all registers) ──────────────────────────────────
    if INVENTED_ABBREV_RE.search(prose):
        penalty += 0.25
        problems.append("invented_abbreviation")
    if ARROW_RE.search(prose):
        penalty += 0.15
        problems.append("arrow_in_prose")

    # ── Grug voice must never reach the user ────────────────────────────
    if register in ("be_brief", "unified", "grug_reasoning"):
        if GRUG_LEAK_RE.search(prose):
            penalty += 0.30
            problems.append("grug_voice_leaked")

    # ── Register-specific ───────────────────────────────────────────────
    if register == "be_brief":
        # Professional prose: full grammar, no polite filler, fluff cut.
        filler_hits = iter_phrases(prose, POLITE_FILLER)
        if filler_hits:
            penalty += 0.10 * len(filler_hits)
            problems.extend(f"filler:{p}" for p in filler_hits)
        # Fluff the source contained and the model failed to cut.
        survived = [p for p in iter_phrases(prose, THROAT_CLEARERS)
                    if p in iter_phrases(item.get("source", ""), [p])]
        if survived:
            penalty += 0.15 * len(survived)
            problems.extend(f"uncut_fluff:{p}" for p in survived)
        # Broken grammar: sentences that start lower-case mid-paragraph.
        broken = _broken_grammar_ratio(answer)
        if broken > 0.25:
            penalty += 0.25
            problems.append(f"broken_grammar:{broken:.2f}")
        # Dropped inflections ("check use", "system work") are caveman
        # voice, which this register promises not to emit.
        bare = _bare_verb_hits(answer)
        if bare:
            penalty += min(0.30, 0.15 * bare)
            problems.append(f"caveman_voice_in_prose:{bare}")

    elif register == "caveman":
        # Terse is good; narration and pleasantries are not.
        narration = iter_phrases(prose, POLITE_FILLER)
        if narration:
            penalty += 0.15 * len(narration)
            problems.extend(f"narration:{p}" for p in narration)

    elif register == "unified":
        filler_hits = iter_phrases(prose, POLITE_FILLER)
        if filler_hits:
            penalty += 0.10 * len(filler_hits)
            problems.extend(f"filler:{p}" for p in filler_hits)
        survived = [p for p in iter_phrases(prose, THROAT_CLEARERS)
                    if p in iter_phrases(item.get("source", ""), [p])]
        if survived:
            penalty += 0.15 * len(survived)
            problems.extend(f"uncut_fluff:{p}" for p in survived)
        broken = _broken_grammar_ratio(answer)
        if broken > 0.25:
            penalty += 0.20
            problems.append(f"broken_grammar:{broken:.2f}")
        bare = _bare_verb_hits(answer)
        if bare:
            penalty += min(0.25, 0.12 * bare)
            problems.append(f"caveman_voice_in_prose:{bare}")

    elif register == "grug_reasoning":
        trace_score, trace_problems = _score_grug_trace(item, trace, answer)
        problems.extend(trace_problems)
        # The visible answer still has to honour the professional contract.
        broken = _broken_grammar_ratio(answer)
        if broken > 0.25:
            penalty += 0.15
            problems.append(f"broken_grammar:{broken:.2f}")
        return _clamp(0.5 * trace_score + 0.5 * _clamp(1.0 - penalty)), problems

    return _clamp(1.0 - penalty), problems


def _score_grug_trace(item: dict, trace: str, answer: str) -> tuple[float, list[str]]:
    """Score the internal grug reasoning trace against this repo's rules."""
    problems: list[str] = []
    if not trace.strip():
        return 0.0, ["no_reasoning_trace"]

    budget = int(item.get("reasoning_budget_tokens", 300))
    used = estimate_tokens(trace)
    if used > budget:
        problems.append(f"trace_over_budget:{used}>{budget}")
    length_score = _clamp(1.0 - max(0.0, (used - budget) / max(1.0, budget)))

    lowered = trace.lower()
    covered = sum(
        1 for markers in FLOW_STAGES.values()
        if any(m in lowered for m in markers)
    )
    flow_score = covered / len(FLOW_STAGES)
    if covered < 3:
        problems.append(f"incomplete_flow:{covered}/5")

    # Internal monologue: no markdown emphasis, no headers.
    emphasis = len(re.findall(r"\*\*|__|^\s*#{1,6}\s", trace, re.MULTILINE))
    if emphasis:
        problems.append("markdown_in_trace")
    style_score = _clamp(1.0 - 0.1 * emphasis)

    return _clamp(0.4 * length_score + 0.4 * flow_score + 0.2 * style_score), problems


# Caveman voice markers: a third-person subject followed by an uninflected
# verb ("check use", "system work", "it not"). Perfectly fine in the caveman
# register, a defect in be_brief / unified, which promise full grammar.
_BARE_VERB_RE = re.compile(
    r"\b(?:it|this|that|he|she|the\s+\w+|system|server|token|check|code|build|test|"
    r"app|api|client|query|handler|module|component|script|process|request|response)\s+"
    r"(use|need|want|work|make|give|take|run|break|show|call|move|go|do|have|say|look|"
    r"return|fail|pass|start|stop|create|read|write)\b",
    re.IGNORECASE,
)


def _bare_verb_hits(text: str) -> int:
    """Count dropped-inflection markers that only the caveman register allows."""
    return len(_BARE_VERB_RE.findall(strip_code_spans(text)))


def _broken_grammar_ratio(text: str) -> float:
    """Fraction of sentences that look clipped rather than written.

    Heuristic only: a sentence counts as broken when it starts lower-case
    and is not the first sentence, or when it has no space after it and no
    terminal punctuation anywhere in the answer.
    """
    prose = strip_code_spans(text)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if s.strip()]
    if len(sentences) < 2:
        return 0.0
    broken = 0
    for idx, sentence in enumerate(sentences):
        if idx == 0:
            continue
        if sentence[:1].islower():
            broken += 1
    return broken / max(1, len(sentences) - 1)


def evaluate(item: dict, output: str) -> ScoreBreakdown:
    """Score one rollout. Returns both the scalar reward and the diagnosis.

    ``hard`` is the validation gate signal (1 = contract kept, 0 = broken).
    ``soft`` is the shaped reward in ``[0, 1]`` that SkillOpt maximises.
    """
    register = str(item.get("register", "be_brief")).strip().lower()
    if register not in REGISTERS:
        register = "be_brief"

    source = str(item.get("source", ""))
    trace, visible = split_reasoning(output)
    if register != "grug_reasoning":
        visible = output.strip()

    fact_score, fact_problems, fact_details = _score_facts(item, visible)
    hedge_score, hedge_problems = _score_hedges(item, visible)
    code_score, code_problems = _score_code(item, visible)
    comp_score, comp_problems = _score_compression(item, visible, source)
    reg_score, reg_problems = _score_register(register, item, visible, trace)

    # Redistribute the code-fidelity weight when an item has no code, so the
    # shaped reward keeps its [0, 1] range across heterogeneous task types.
    has_code = bool(item.get("code_spans")) or bool(extract_code_spans(source))
    if has_code:
        weights = dict(WEIGHTS)
    else:
        spare = WEIGHTS["code_fidelity"]
        weights = {k: (v + spare / 4 if k != "code_fidelity" else 0.0)
                   for k, v in WEIGHTS.items()}
        code_score = 1.0
        code_problems = []

    soft = (
        weights["fact_retention"] * fact_score
        + weights["code_fidelity"] * code_score
        + weights["compression"] * comp_score
        + weights["register_fidelity"] * reg_score
        + weights["hedge_retention"] * hedge_score
    )

    # ── Hard gate ───────────────────────────────────────────────────────
    # These are the things that make an output *wrong* rather than merely
    # sub-optimal. A skill that drops a fact or mangles code must never be
    # accepted by the validation gate, however terse it got.
    #
    # Zero compression is on the list too, and deliberately so: "copy the
    # input verbatim" is the degenerate optimum that preserves every fact
    # while achieving nothing. Without this gate the optimizer would happily
    # converge on it.
    violations = (
        fact_problems + hedge_problems + code_problems + reg_problems + comp_problems
    )
    blocking = {
        "lost_span", "lost_number", "lost_citation", "lost_hedge",
        "code_not_verbatim", "code_lost_from_source", "grug_voice_leaked",
        "invented_abbreviation", "arrow_in_prose", "no_compression_or_grew",
    }
    hard_fail = any(
        v.split(":", 1)[0] in blocking for v in violations
    )
    max_tokens = int(item.get("max_output_tokens", 0) or 0)
    if max_tokens and estimate_tokens(visible) > max_tokens * 1.5:
        hard_fail = True
        violations.append("over_token_budget")

    breakdown = ScoreBreakdown(
        fact_retention=fact_score,
        hedge_retention=hedge_score,
        code_fidelity=code_score,
        compression=comp_score,
        register_fidelity=reg_score,
        soft=_clamp(soft),
        hard=0 if hard_fail else 1,
        violations=violations,
        details={
            **fact_details,
            "register": register,
            "output_tokens": estimate_tokens(visible),
            "trace_tokens": estimate_tokens(trace),
            "source_tokens": estimate_tokens(source),
            "compression_ratio": round(compression_ratio(source, visible), 4),
        },
    )
    return breakdown
