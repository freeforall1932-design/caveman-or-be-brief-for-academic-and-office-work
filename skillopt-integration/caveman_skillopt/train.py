#!/usr/bin/env python3
"""
Train a caveman / be-brief / grug skill document with SkillOpt.

Thin wrapper around SkillOpt's own training CLI: it registers the
``caveman_brief`` environment, then hands over to SkillOpt's ``scripts/train.py``.

    python -m caveman_skillopt.train --config skillopt-integration/configs/be-brief.yaml

    python -m caveman_skillopt.train --config skillopt-integration/configs/coding-agent.yaml \
        --cfg-options train.num_epochs=6 optimizer.learning_rate=6

Every flag from SkillOpt's own ``train.py`` works unchanged.

Working from a SkillOpt checkout instead of the wheel? Point at it:

    export SKILLOPT_SRC=/path/to/SkillOpt
"""

from __future__ import annotations

import sys

from .register import ensure_registered


def main() -> int:
    module = ensure_registered("train")
    return module.main() or 0


if __name__ == "__main__":
    sys.exit(main())
