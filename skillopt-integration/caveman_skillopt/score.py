#!/usr/bin/env python3
"""
Score model outputs against the caveman_brief reward function — no API calls.

This is the cheapest way to compare two skills, or to check whether a
candidate edit is actually an improvement before spending tokens on a full
SkillOpt run.

    python -m caveman_skillopt.score \
        --split-dir skillopt-integration/data/caveman_brief_split \
        --split test \
        --predictions preds.json

``preds.json`` maps item id → model output::

    {"shipments-be_brief": "Many shipments were delayed...", ...}

Exit code is 0 when every scored item passes the hard gate, 1 otherwise, so
it can be wired into CI as a regression check on a shipped skill.

Deliberately dependency-free: it reads the split JSON directly rather than
going through the SkillOpt ``SplitDataLoader``, so it runs on a machine that
has this package installed but not SkillOpt itself. Scoring a skill should
never require the training framework.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from .envs.caveman_brief.schema import normalise_item
from .envs.caveman_brief.evaluator import evaluate


def _load_split(split_dir: str, split: str) -> list[dict]:
    """Read one split straight off disk."""
    split_path = Path(split_dir) / split
    if not split_path.is_dir():
        raise SystemExit(f"No such split directory: {split_path}")

    json_files = sorted(split_path.glob("*.json"))
    if json_files:
        payload = json.loads(json_files[0].read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise SystemExit(f"Expected a JSON array at the top level of {json_files[0]}")
        return [normalise_item(row) for row in payload]

    jsonl_files = sorted(split_path.glob("*.jsonl"))
    if jsonl_files:
        rows = []
        for line in jsonl_files[0].read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(normalise_item(json.loads(line)))
        return rows

    raise SystemExit(f"No .json or .jsonl file found in {split_path}")


def _load_predictions(path: str) -> dict[str, str]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {str(row["id"]): str(row.get("output", "")) for row in payload}
    return {str(k): str(v) for k, v in payload.items()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--split-dir", default="skillopt-integration/data/caveman_brief_split")
    parser.add_argument("--split", default="test", choices=("train", "val", "test"))
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--register", default="", help="Only score one register.")
    parser.add_argument("--show-violations", action="store_true")
    args = parser.parse_args(argv)

    items = _load_split(args.split_dir, args.split)
    predictions = _load_predictions(args.predictions)

    per_register: dict[str, list[float]] = defaultdict(list)
    per_task: dict[str, list[float]] = defaultdict(list)
    soft_total: list[float] = []
    failures: list[tuple[str, list[str]]] = []
    missing: list[str] = []

    for item in items:
        if args.register and item.get("register") != args.register:
            continue
        item_id = str(item["id"])
        if item_id not in predictions:
            missing.append(item_id)
            continue
        score = evaluate(item, predictions[item_id])
        soft_total.append(score.soft)
        per_register[item["register"]].append(score.soft)
        per_task[item["task_type"]].append(score.soft)
        if not score.hard:
            failures.append((item_id, score.violations))

    if not soft_total:
        print("No items scored. Check --split, --register and the prediction ids.")
        return 2

    def _mean(values: list[float]) -> float:
        return sum(values) / len(values)

    print(f"\nScored {len(soft_total)} item(s) from split '{args.split}'")
    if missing:
        print(f"  no prediction for {len(missing)} item(s): {', '.join(missing[:5])}")
    print(f"  mean soft reward : {_mean(soft_total):.4f}")
    print(f"  hard pass rate   : {(len(soft_total) - len(failures)) / len(soft_total):.1%}")

    print("\n  by register")
    for register, values in sorted(per_register.items()):
        print(f"    {register:<16} {_mean(values):.4f}  (n={len(values)})")

    print("\n  by task type")
    for task, values in sorted(per_task.items()):
        print(f"    {task:<16} {_mean(values):.4f}  (n={len(values)})")

    if failures:
        print(f"\n  {len(failures)} hard-gate failure(s)")
        if args.show_violations:
            for item_id, violations in failures:
                print(f"    {item_id}: {', '.join(violations) or 'n/a'}")
    else:
        print("\n  all items passed the hard gate")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
