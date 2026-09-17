"""
Deterministic text metrics for the caveman_brief SkillOpt environment.

Everything in here is dependency-free and reproducible. The reward signal
that drives SkillOpt's optimizer has to be stable across epochs, so we use
tokenizer-free heuristics rather than a real BPE tokenizer or an LLM judge
by default.

If ``tiktoken`` happens to be installed we use it for token counts, but the
deterministic estimator is the default so that a run is reproducible on any
machine that just has SkillOpt installed.
"""

from __future__ import annotations

import re
from typing import Iterable

# ── Token estimation ────────────────────────────────────────────────────────

# Split on whitespace and on punctuation boundaries, then further split long
# camelCase / snake_case identifiers the way a BPE tokenizer roughly would.
_TOKEN_RE = re.compile(
    r"[A-Za-z]+(?:[a-z](?=[A-Z]))?|\d+(?:[.,]\d+)?%?|[^\sA-Za-z\d]"
)
_CAMEL_RE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")


def estimate_tokens(text: str) -> int:
    """Estimate the token count of *text* deterministically.

    Approximates cl100k-style BPE for English/Indonesian prose:

    * each word is charged ``ceil(len/4)`` sub-word tokens (min 1),
    * standalone punctuation and digits are charged 1 token each,
    * code-ish identifiers are split on camelCase / snake_case boundaries.

    It is not exact, but it is monotone and stable, which is all the
    optimizer needs: it rewards *relative* shrinkage.
    """
    if not text:
        return 0

    total = 0
    for raw in _TOKEN_RE.findall(text):
        if raw.isdigit() or not raw.isalnum():
            total += 1
            continue
        if len(raw) > 12 and ("_" in raw or any(c.isupper() for c in raw[1:])):
            pieces = [p for p in re.split(r"[_\-.]+", raw) if p]
            for piece in pieces:
                total += max(1, (len(piece) + 3) // 4)
            continue
        total += max(1, (len(raw) + 3) // 4)
    return total


def compression_ratio(source: str, output: str) -> float:
    """Return ``1 - out/in`` — 0.0 means no change, 0.65 means 65% smaller."""
    src = estimate_tokens(source)
    if src <= 0:
        return 0.0
    return max(0.0, min(1.0, 1.0 - (estimate_tokens(output) / src)))


# ── Structural extraction ───────────────────────────────────────────────────

_FENCE_RE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
_LATEX_RE = re.compile(r"\$\$?[^$]+\$\$?")

# Numbers that carry data: 150, 62%, 3.14, n=150, 1,200, p<0.05, 2023
_NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(?:[A-Za-z]{1,3}\s?[=<>≤≥]\s?)?"       # optional n= / p< prefix
    r"\d{1,3}(?:[.,]\d{3})*(?:\.\d+)?\s?%?"   # the number
    r"(?:\s?(?:kg|km|mm|cm|ms|GB|MB|TB|Hz))?" # optional unit
)

# Citation-ish tokens: [@smith2023], (Smith, 2023), [1], [12], DOI strings
_CITATION_RE = re.compile(
    r"\[@[^\]]+\]"
    r"|\([A-Z][A-Za-z\-]+(?:\s(?:and|&|et al\.?)\s[A-Z][A-Za-z\-]+)?,?\s*\d{4}[a-z]?\)"
    r"|\[\d+(?:[,\s–-]\d+)*\]"
    r"|\bdoi:\S+"
    r"|\bhttps?://\S+"
)


def extract_code_spans(text: str) -> list[str]:
    """Return every fenced code block body (triple-backtick) in *text*."""
    return [m.group(1) for m in _FENCE_RE.finditer(text)]


def strip_code_spans(text: str) -> str:
    """Return *text* with fenced code blocks, inline code and LaTeX removed.

    Prose-level checks (banned abbreviations, arrows, grug-voice leakage)
    must run on this, never on the raw text, otherwise legitimate code
    content is punished.
    """
    out = _FENCE_RE.sub(" ", text)
    out = _LATEX_RE.sub(" ", out)
    out = _INLINE_CODE_RE.sub(" ", out)
    return out


def extract_numbers(text: str) -> list[str]:
    """Return normalised numeric tokens (data that must survive compression)."""
    found: list[str] = []
    for m in _NUMBER_RE.finditer(text):
        token = re.sub(r"\s+", "", m.group(0)).rstrip(".,;:")
        if token and token not in found:
            found.append(token)
    return found


def extract_citations(text: str) -> list[str]:
    """Return citation-like tokens that must survive compression verbatim."""
    found: list[str] = []
    for m in _CITATION_RE.finditer(text):
        token = m.group(0).strip()
        if token not in found:
            found.append(token)
    return found


def normalise(text: str) -> str:
    """Whitespace-normalised, lowercased text used for containment checks."""
    return re.sub(r"\s+", " ", (text or "").strip().lower())


# Light suffix stripping, so that "delays" in the source still matches
# "delayed" in a compressed rewrite. Deliberately conservative: only the
# most regular English inflections are stripped, and never below 4 chars.
_STEM_SUFFIXES = ("ies", "ing", "ed", "es", "s")


def _stem_word(word: str) -> str:
    lowered = word.lower()
    for suffix in _STEM_SUFFIXES:
        if len(lowered) - len(suffix) >= 4 and lowered.endswith(suffix):
            return lowered[: -len(suffix)]
    return lowered


def stem_normalise(text: str) -> str:
    """Normalise, then reduce each word to a light stem."""
    return " ".join(_stem_word(w) for w in normalise(text).split())


def contains_span(haystack: str, needle: str) -> bool:
    """Whitespace- and inflection-insensitive containment check.

    A compressed sentence legitimately re-inflects a word ("delays" →
    "delayed"), so matching must survive regular English inflection or the
    reward function punishes correct compressions.
    """
    if not needle:
        return True
    if normalise(needle) in normalise(haystack):
        return True
    return stem_normalise(needle) in stem_normalise(haystack)


def contains_number(haystack: str, number: str | int | float) -> bool:
    """True if *number* appears in *haystack* as a numeric token.

    Thousands separators are ignored on both sides, so a source figure of
    ``1240`` still matches a compressed ``1,240``. That distinction matters:
    a compression that re-formats a number has not lost it.
    """
    token = str(number).strip()
    if not token:
        return True
    core = re.sub(r"[^\d.,]", "", token).replace(",", "")
    if not core:
        return contains_span(haystack, token)
    # Digits only, separators removed: "1,240 survey responses" -> "...1240..."
    haystack_digits = re.sub(r"\s+", "", haystack).replace(",", "")
    return core in haystack_digits or contains_span(haystack, token)


# ── Grug reasoning trace ────────────────────────────────────────────────────

_THINK_OPEN = ("<thinking>", "<grug>", "<reasoning>")
_THINK_CLOSE = ("</thinking>", "</grug>", "</reasoning>")


def split_reasoning(output: str) -> tuple[str, str]:
    """Split *output* into ``(reasoning_trace, visible_answer)``.

    Coding agents and reasoning models often wrap internal reasoning in a
    tagged block. We support the common spellings so the grug register can be
    scored on the trace while the user-facing contract is scored on the rest.
    """
    if not output:
        return "", ""
    lowered = output.lower()
    for open_tag, close_tag in zip(_THINK_OPEN, _THINK_CLOSE):
        start = lowered.find(open_tag)
        end = lowered.find(close_tag)
        if start != -1 and end != -1 and end > start:
            trace = output[start + len(open_tag): end]
            visible = (output[:start] + output[end + len(close_tag):]).strip()
            return trace.strip(), visible
    return "", output.strip()


def count_sentences(text: str) -> int:
    """Cheap sentence counter used by the fluency / fragmentation checks."""
    if not text.strip():
        return 0
    return len([s for s in re.split(r"[.!?]+(?:\s|$)", text) if s.strip()])


def iter_phrases(text: str, phrases: Iterable[str]) -> list[str]:
    """Return the subset of *phrases* that occur in *text*."""
    hay = normalise(text)
    return [p for p in phrases if p and normalise(p) in hay]
