"""
Integration tests against the real SkillOpt package.

These are skipped when SkillOpt is not installed, so the pure-reward tests
in ``test_evaluator.py`` still run in a bare environment.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

skillopt = pytest.importorskip("skillopt", reason="SkillOpt is not installed")

from caveman_skillopt.register import ENV_KEY, register_env  # noqa: E402
from caveman_skillopt.envs.caveman_brief import CavemanBriefAdapter  # noqa: E402


def test_adapter_satisfies_the_env_adapter_contract():
    from skillopt.envs.base import EnvAdapter

    assert issubclass(CavemanBriefAdapter, EnvAdapter)
    # Abstract methods must all be implemented, or instantiation fails.
    assert not getattr(CavemanBriefAdapter, "__abstractmethods__", set())


def test_registration_hits_skillopt_cli_registries():
    patched = register_env()
    assert patched, "no SkillOpt CLI registry was found to patch"
    for module_name in patched:
        module = sys.modules[module_name]
        assert module._ENV_REGISTRY[ENV_KEY] is CavemanBriefAdapter


def test_env_name_resolves_from_module_path():
    """_env_name is derived from ``...envs.<name>.adapter``."""
    adapter = CavemanBriefAdapter()
    assert adapter._env_name == "caveman_brief"


def test_adapter_loads_its_own_reflection_prompts():
    """Our prompts live in this repo, not inside the installed package."""
    adapter = CavemanBriefAdapter()
    error_prompt = adapter.get_error_minibatch_prompt()
    success_prompt = adapter.get_success_minibatch_prompt()
    assert error_prompt and "failure-analysis" in error_prompt.lower()
    assert success_prompt and "success" in success_prompt.lower()


def test_adapter_builds_envs_from_the_real_dataset():
    split_dir = ROOT / "data" / "caveman_brief_split"
    if not split_dir.is_dir():
        pytest.skip("dataset not built yet")
    adapter = CavemanBriefAdapter(split_dir=str(split_dir), split_mode="split_dir")
    adapter.setup({"split_dir": str(split_dir), "split_mode": "split_dir", "env": ENV_KEY})

    env = adapter.build_train_env(batch_size=4, seed=1)
    assert len(env) == 4
    assert all(item["id"] for item in env)

    types = adapter.get_task_types()
    assert "academic_prose" in types


def test_register_filter_narrows_training_to_one_philosophy():
    split_dir = ROOT / "data" / "caveman_brief_split"
    if not split_dir.is_dir():
        pytest.skip("dataset not built yet")
    adapter = CavemanBriefAdapter(
        split_dir=str(split_dir), split_mode="split_dir", register_filter="caveman"
    )
    adapter.setup({"split_dir": str(split_dir), "split_mode": "split_dir", "env": ENV_KEY})
    env = adapter.build_train_env(batch_size=8, seed=1)
    assert env
    assert all(item["register"] == "caveman" for item in env)
