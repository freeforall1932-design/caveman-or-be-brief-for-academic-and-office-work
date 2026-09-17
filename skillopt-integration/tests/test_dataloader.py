"""Tests for the caveman_brief dataloader and dataset integrity."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

pytest.importorskip("skillopt", reason="CavemanBriefDataLoader subclasses SkillOpt's SplitDataLoader")

from caveman_skillopt.envs.caveman_brief.dataloader import (  # noqa: E402
    CavemanBriefDataLoader,
    normalise_item,
)
from caveman_skillopt.envs.caveman_brief.evaluator import REGISTERS  # noqa: E402

SPLIT_DIR = ROOT / "data" / "caveman_brief_split"


@pytest.fixture(scope="module")
def loader() -> CavemanBriefDataLoader:
    if not SPLIT_DIR.is_dir():
        pytest.skip("dataset not built yet — run scripts/build_dataset.py")
    instance = CavemanBriefDataLoader(split_dir=str(SPLIT_DIR), split_mode="split_dir")
    instance.setup({"split_dir": str(SPLIT_DIR), "split_mode": "split_dir", "env": "caveman_brief"})
    return instance


def test_normalise_item_fills_defaults():
    item = normalise_item({"uid": "x1", "source": "hello world"})
    assert item["id"] == "x1"
    assert item["register"] == "be_brief"
    assert item["task_type"] == "prose"
    assert item["must_keep"] == []
    assert item["target_compression"] == pytest.approx(0.5)


def test_normalise_item_keeps_unknown_keys():
    item = normalise_item({"id": "x2", "source": "s", "provenance": "hand-authored"})
    assert item["provenance"] == "hand-authored"


def test_all_three_splits_are_populated(loader):
    assert loader.train_items
    assert loader.val_items
    assert loader.test_items


def test_split_ids_do_not_overlap(loader):
    train = {i["id"] for i in loader.train_items}
    val = {i["id"] for i in loader.val_items}
    test = {i["id"] for i in loader.test_items}
    assert not (train & val)
    assert not (train & test)
    assert not (val & test)


def test_every_item_has_a_valid_register(loader):
    for item in loader.train_items + loader.val_items + loader.test_items:
        assert item["register"] in REGISTERS, item["id"]


def test_every_item_has_a_source(loader):
    for item in loader.train_items + loader.val_items + loader.test_items:
        assert item["source"].strip(), item["id"]


def test_declared_facts_actually_appear_in_the_source(loader):
    """Every must_keep / hedge must be checkable against the source.

    Otherwise the reward function would penalise the model for a fact that
    was never there, and the whole signal would be noise.
    """
    for item in loader.train_items + loader.val_items + loader.test_items:
        haystack = item["source"].lower()
        for span in item["must_keep"]:
            assert span.lower() in haystack, f"{item['id']}: must_keep {span!r} not in source"
        for hedge in item["hedges"]:
            assert hedge.lower() in haystack, f"{item['id']}: hedge {hedge!r} not in source"


def test_declared_code_spans_are_non_trivial(loader):
    """Code spans are the artifact the answer must emit byte-exact.

    They are the deliverable, so unlike must_keep they need not appear in
    the source — but they must be real code, not empty strings.
    """
    for item in loader.train_items + loader.val_items + loader.test_items:
        for code in item["code_spans"]:
            assert code.strip(), f"{item['id']}: empty code span"
            assert len(code.strip()) > 10, f"{item['id']}: code span too small to be meaningful"


def test_all_task_types_appear_in_every_split(loader):
    """Stratified split: no task type should be missing from a split."""
    for split_name in ("train_items", "val_items", "test_items"):
        tasks = {i["task_type"] for i in getattr(loader, split_name)}
        assert tasks, split_name


def test_manifest_matches_disk(loader):
    manifest = json.loads((SPLIT_DIR / "split_manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"]["train"] == len(loader.train_items)
    assert manifest["counts"]["val"] == len(loader.val_items)
    assert manifest["counts"]["test"] == len(loader.test_items)
