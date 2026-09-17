"""
Item schema and normalisation for the caveman_brief environment.

Dependency-free on purpose. The offline scorer and the dataset builder both
need ``normalise_item``, and neither should require SkillOpt to be installed
just to parse a JSON record.
"""

from __future__ import annotations

from typing import Any

DEFAULT_REGISTER = "be_brief"
DEFAULT_TASK_TYPE = "prose"


def _as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [v for v in value if v is not None]
    return [value]


def normalise_item(raw: dict) -> dict:
    """Coerce one raw record into the canonical item shape."""
    source = str(raw.get("source") or raw.get("input") or raw.get("document") or "")
    item = {
        "id": str(raw.get("id") or raw.get("uid") or raw.get("qid") or ""),
        "task_type": str(raw.get("task_type") or raw.get("category") or DEFAULT_TASK_TYPE),
        "register": str(raw.get("register") or DEFAULT_REGISTER).strip().lower(),
        "language": str(raw.get("language") or raw.get("lang") or "en").strip().lower(),
        "source": source,
        "instruction": str(raw.get("instruction") or raw.get("prompt") or ""),
        "must_keep": [str(x) for x in _as_list(raw.get("must_keep"))],
        "must_keep_numbers": _as_list(raw.get("must_keep_numbers")),
        "must_keep_citations": [str(x) for x in _as_list(raw.get("must_keep_citations"))],
        "hedges": [str(x) for x in _as_list(raw.get("hedges"))],
        "code_spans": [str(x) for x in _as_list(raw.get("code_spans"))],
    }
    # Numeric knobs.
    item["target_compression"] = float(raw.get("target_compression", 0.5))
    item["min_compression"] = float(raw.get("min_compression", item["target_compression"] * 0.5))
    item["max_output_tokens"] = int(raw.get("max_output_tokens", 0) or 0)
    item["reasoning_budget_tokens"] = int(raw.get("reasoning_budget_tokens", 300) or 300)
    # Anything else (reference output, provenance, notes) rides along untouched.
    for key, value in raw.items():
        item.setdefault(key, value)
    return item
