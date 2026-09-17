"""
Register the ``caveman_brief`` environment with SkillOpt's CLI entry points.

SkillOpt keeps one lazy ``_ENV_REGISTRY`` dict per CLI script and populates
it inside ``_register_builtins()``. Rather than patching SkillOpt's source
files, we import the CLI module and add our adapter class to its registry.
The CLI then resolves ``env.name: caveman_brief`` exactly like a built-in
benchmark, and the registration survives ``pip install --upgrade skillopt``.

Layout note
-----------
Depending on how SkillOpt was installed, its CLI modules live under a
different import path:

* ``pip install skillopt``  → top-level ``scripts.train`` / ``scripts.eval_only``
* working from a source checkout → ``scripts.train`` with the repo root on
  ``sys.path``
* some builds vendor them as ``skillopt.scripts.train``

We therefore probe every known location instead of assuming one.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from .envs.caveman_brief import CavemanBriefAdapter

ENV_KEY = "caveman_brief"

# Candidate module prefixes, most likely first.
_CLI_PREFIXES = ("scripts", "skillopt.scripts")
_CLI_NAMES = ("train", "eval_only")


def _candidate_sources() -> list[str | None]:
    """Additional sys.path entries to try, from the environment."""
    extra: list[str | None] = [None]  # None = current sys.path
    for var in ("SKILLOPT_SRC", "SKILLOPT_PATH"):
        value = os.environ.get(var, "").strip()
        if value:
            extra.append(value)
    return extra


def _import_cli(name: str) -> ModuleType:
    """Import SkillOpt's ``train`` / ``eval_only`` CLI module.

    Raises ``ImportError`` with actionable guidance when SkillOpt is missing.
    """
    assert name in _CLI_NAMES, f"unknown SkillOpt CLI script: {name}"

    for source in _candidate_sources():
        if source and source not in sys.path:
            sys.path.insert(0, source)
        for prefix in _CLI_PREFIXES:
            module_name = f"{prefix}.{name}"
            try:
                module = importlib.import_module(module_name)
            except Exception:  # noqa: BLE001 - probe every candidate
                continue
            if hasattr(module, "_ENV_REGISTRY") and hasattr(module, "main"):
                return module

    raise ImportError(
        f"Could not find SkillOpt's '{name}' CLI script.\n"
        "Install SkillOpt with:\n"
        "    pip install skillopt\n"
        "or, if you are working from a checkout (e.g. the fork at\n"
        "https://github.com/freeforall1932-design/SkillOpt-fork), point at it:\n"
        "    export SKILLOPT_SRC=/path/to/SkillOpt\n"
        f"Probed: {[f'{p}.{name}' for p in _CLI_PREFIXES]}"
    )


def register_env() -> list[str]:
    """Inject the adapter into every SkillOpt CLI registry we can reach.

    Returns the list of module names that were patched.
    """
    patched: list[str] = []
    for name in _CLI_NAMES:
        try:
            module = _import_cli(name)
        except ImportError:
            continue
        registry: dict[str, Any] = module._ENV_REGISTRY
        if registry.get(ENV_KEY) is not CavemanBriefAdapter:
            registry[ENV_KEY] = CavemanBriefAdapter
        patched.append(module.__name__)
    return patched


def ensure_registered(name: str = "train") -> ModuleType:
    """Register the env and return the SkillOpt CLI module ready to run."""
    try:
        import skillopt  # noqa: F401
    except ImportError as exc:  # pragma: no cover - environment problem
        raise ImportError(
            "SkillOpt is required to train the caveman_brief environment.\n"
            "    pip install skillopt"
        ) from exc

    module = _import_cli(name)
    module._ENV_REGISTRY[ENV_KEY] = CavemanBriefAdapter
    return module


def default_data_dir() -> Path:
    """Absolute path of the shipped train/val/test split."""
    return Path(__file__).resolve().parents[1] / "data" / "caveman_brief_split"
