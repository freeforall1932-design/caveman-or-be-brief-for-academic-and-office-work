"""
caveman_skillopt — SkillOpt integration layer for the
`caveman-or-be-brief-for-academic-and-office-work` repository.

It contributes one SkillOpt environment, ``caveman_brief``, that treats the
repo's skill documents as the trainable state of a frozen LLM and optimises
them with SkillOpt's rollout → reflect → aggregate → select → update →
evaluate loop.

Quick start::

    pip install skillopt
    pip install -e skillopt-integration

    python -m caveman_skillopt.train \\
        --config skillopt-integration/configs/be-brief.yaml

The loop produces a validation-gated ``best_skill.md`` that can be dropped
into the merge: drop it on top of the vendored copy it came from under
``one-skill/upstream/local/``, point that skill's ``entry`` at it in
``one-skill/sources.json``, and rebuild with ``python one-skill/build.py all``.
The published ``.claude/skills/one-skill/`` tree is generated and must not be
edited directly.

Nothing SkillOpt-dependent is imported at package import time. The offline
scorer (``python -m caveman_skillopt.score``) therefore works on a machine
that has this package but not SkillOpt, and ``register_env`` is resolved
lazily on first use.
"""

__version__ = "0.1.0"

__all__ = ["register_env", "ensure_registered", "ENV_KEY", "__version__"]


def __getattr__(name: str):
    """Lazily resolve the SkillOpt-dependent entry points.

    Importing ``register`` pulls in ``EnvAdapter``, which needs SkillOpt.
    Deferring it keeps ``import caveman_skillopt`` — and the offline scorer —
    working without SkillOpt installed.
    """
    if name in ("register_env", "ensure_registered", "ENV_KEY"):
        from . import register as _register

        return getattr(_register, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
