"""
SkillOpt environment adapter for the caveman / be-brief / grug skill family.

The adapter is deliberately thin: the *learning signal* lives in
:mod:`evaluator` and the *episode mechanics* live in :mod:`rollout`. This
class only wires them into SkillOpt's lifecycle.

One deviation from the built-in benchmarks is worth flagging: SkillOpt loads
env-specific reflection prompts from ``skillopt/envs/<env>/prompts/``. Our
env lives in this repository, not inside the installed package, so we
override the two prompt getters and read from our own ``prompts/``
directory. That is the documented escape hatch (``EnvAdapter`` docstring:
"Subclasses can still override ``get_*_prompt()`` for full control").
"""

from __future__ import annotations

import os

from skillopt.datasets.base import BatchSpec
from skillopt.envs.base import EnvAdapter

from .dataloader import CavemanBriefDataLoader
from .rollout import run_batch

_PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


def _load_own_prompt(name: str) -> str | None:
    path = os.path.join(_PROMPTS_DIR, f"{name}.md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class CavemanBriefAdapter(EnvAdapter):
    """EnvAdapter for token-efficient academic / office / agent writing.

    Registered under the key ``caveman_brief`` by
    :func:`caveman_skillopt.register.register_env`.
    """

    def __init__(
        self,
        split_dir: str = "",
        data_path: str = "",
        split_mode: str = "split_dir",
        split_ratio: str = "2:1:7",
        split_seed: int = 42,
        split_output_dir: str = "",
        workers: int = 8,
        analyst_workers: int = 8,
        failure_only: bool = False,
        minibatch_size: int = 8,
        edit_budget: int = 4,
        seed: int = 42,
        limit: int = 0,
        max_completion_tokens: int = 4096,
        register_filter: str = "",
    ) -> None:
        self.workers = workers
        self.analyst_workers = analyst_workers
        self.failure_only = failure_only
        self.minibatch_size = minibatch_size
        self.edit_budget = edit_budget
        self.max_completion_tokens = int(max_completion_tokens)
        # Empty string = train on every register at once. Set it in the config
        # to train one philosophy family in isolation (see configs/caveman.yaml).
        self.register_filter = str(register_filter or "").strip().lower()
        self.dataloader = CavemanBriefDataLoader(
            split_dir=split_dir,
            data_path=data_path,
            split_mode=split_mode,
            split_ratio=split_ratio,
            split_seed=split_seed,
            split_output_dir=split_output_dir,
            seed=seed,
            limit=limit,
        )

    # ── Lifecycle hooks ─────────────────────────────────────────────────

    def setup(self, cfg: dict) -> None:
        super().setup(cfg)
        self.dataloader.setup(cfg)

    def get_dataloader(self):
        return self.dataloader

    # ── Batch → item list ───────────────────────────────────────────────

    def build_env_from_batch(self, batch: BatchSpec, **kwargs):
        items = list(batch.payload or [])
        if self.register_filter:
            items = [
                item for item in items
                if str(item.get("register", "")).strip().lower() == self.register_filter
            ] or items
        return items

    def build_train_env(self, batch_size: int, seed: int, **kwargs):
        batch = self.dataloader.build_train_batch(batch_size=batch_size, seed=seed, **kwargs)
        return self.build_env_from_batch(batch, **kwargs)

    def build_eval_env(self, env_num: int, split: str, seed: int, **kwargs):
        batch = self.dataloader.build_eval_batch(env_num=env_num, split=split, seed=seed, **kwargs)
        return self.build_env_from_batch(batch, **kwargs)

    # ── Rollout ─────────────────────────────────────────────────────────

    def rollout(self, env_manager, skill_content: str, out_dir: str, **kwargs) -> list[dict]:
        items: list[dict] = env_manager
        return run_batch(
            items=items,
            skill_content=skill_content,
            out_root=out_dir,
            workers=self.workers,
            max_completion_tokens=self.max_completion_tokens,
        )

    # ── Reflection prompts (read from our own package) ──────────────────

    def get_error_minibatch_prompt(self) -> str | None:
        return _load_own_prompt("analyst_error")

    def get_success_minibatch_prompt(self) -> str | None:
        return _load_own_prompt("analyst_success")

    # ── Stratification ──────────────────────────────────────────────────

    def get_task_types(self) -> list[str]:
        seen: list[str] = []
        all_items = (
            self.dataloader.train_items
            + self.dataloader.val_items
            + self.dataloader.test_items
        )
        for item in all_items:
            task_type = str(item.get("task_type") or "prose")
            if task_type not in seen:
                seen.append(task_type)
        return seen or ["prose"]
