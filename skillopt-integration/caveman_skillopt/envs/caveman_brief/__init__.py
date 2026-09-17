"""caveman_brief — SkillOpt environment for the caveman / be-brief / grug skill family.

Only the dependency-free modules are imported eagerly. The SkillOpt-dependent
adapter and dataloader are resolved lazily, so ``python -m caveman_skillopt.score``
works without SkillOpt installed.
"""

from __future__ import annotations

from .evaluator import REGISTERS, ScoreBreakdown, evaluate
from .metrics import estimate_tokens
from .schema import normalise_item

__all__ = [
    "CavemanBriefAdapter",
    "CavemanBriefDataLoader",
    "normalise_item",
    "evaluate",
    "estimate_tokens",
    "ScoreBreakdown",
    "REGISTERS",
]


def __getattr__(name: str):
    if name in ("CavemanBriefAdapter", "CavemanBriefDataLoader"):
        if name == "CavemanBriefAdapter":
            from .adapter import CavemanBriefAdapter

            return CavemanBriefAdapter
        from .dataloader import CavemanBriefDataLoader

        return CavemanBriefDataLoader
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
