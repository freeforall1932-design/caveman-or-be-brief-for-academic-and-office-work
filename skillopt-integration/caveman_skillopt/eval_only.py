#!/usr/bin/env python3
"""
Evaluate a skill on the caveman_brief benchmark without training.

    python -m caveman_skillopt.eval_only --config skillopt-integration/configs/be-brief.yaml

Use this to score a hand-written skill — including the ones shipped in this
repo — against the held-out test split before promoting it.
"""

from __future__ import annotations

import sys

from .register import ensure_registered


def main() -> int:
    module = ensure_registered("eval_only")
    return module.main() or 0


if __name__ == "__main__":
    sys.exit(main())
