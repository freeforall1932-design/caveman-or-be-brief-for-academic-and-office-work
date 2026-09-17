"""
Data loader for the caveman_brief SkillOpt environment.

Item schema (all keys except ``id`` optional; sensible defaults are filled in)::

    {
      "id": "acad-en-001",
      "task_type": "academic_prose",     # stratification key for sampling
      "register": "be_brief",            # be_brief | caveman | unified | grug_reasoning
      "language": "en",                  # en | id
      "source": "...verbose text...",     # what the model must compress / act on
      "instruction": "Tighten this.",     # the user turn
      "must_keep": ["n=150"],             # literal spans that must survive
      "must_keep_numbers": [150],
      "must_keep_citations": ["[@smith2023]"],
      "hedges": ["may"],                  # genuine hedges that must survive
      "code_spans": ["..."],              # code the ANSWER must contain byte-exact.
                                          # This is usually the deliverable the model
                                          # must emit, so it does not have to appear in
                                          # "source". Code that appears in "source" is
                                          # checked for survival automatically.
      "target_compression": 0.55,
      "min_compression": 0.30,
      "max_output_tokens": 220,
      "reasoning_budget_tokens": 300      # grug_reasoning register only
    }
"""

from __future__ import annotations

import glob
import json
import os
from pathlib import Path

from skillopt.datasets.base import SplitDataLoader

from .schema import normalise_item  # noqa: F401  (re-exported)

DEFAULT_REGISTER = "be_brief"
DEFAULT_TASK_TYPE = "prose"


class CavemanBriefDataLoader(SplitDataLoader):
    """Loads caveman_brief items from ``<split_dir>/<split>/*.json``."""

    def load_split_items(self, split_path: str) -> list[dict]:
        path = Path(split_path)
        json_files = sorted(path.glob("*.json"))
        if json_files:
            with json_files[0].open(encoding="utf-8") as handle:
                payload = json.load(handle)
            if not isinstance(payload, list):
                raise ValueError(f"Expected a JSON array at the top level of {json_files[0]}")
            return [normalise_item(row) for row in payload]

        jsonl_files = sorted(path.glob("*.jsonl"))
        if jsonl_files:
            items: list[dict] = []
            with jsonl_files[0].open(encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if line:
                        items.append(normalise_item(json.loads(line)))
            return items

        raise FileNotFoundError(f"No .json or .jsonl file found in {split_path}")

    def load_raw_items(self, data_path: str) -> list[dict]:
        """Support ``split_mode: ratio`` by normalising before splitting."""
        if os.path.isdir(data_path):
            candidates = sorted(glob.glob(os.path.join(data_path, "*.json")))
            candidates += sorted(glob.glob(os.path.join(data_path, "*.jsonl")))
            if len(candidates) != 1:
                raise ValueError(
                    f"Expected exactly one .json/.jsonl in {data_path}, got {len(candidates)}"
                )
            data_path = candidates[0]
        with open(data_path, encoding="utf-8") as handle:
            content = handle.read().strip()
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            payload = [json.loads(line) for line in content.splitlines() if line.strip()]
        if isinstance(payload, dict):
            payload = payload.get("data", [])
        return [normalise_item(row) for row in payload]
