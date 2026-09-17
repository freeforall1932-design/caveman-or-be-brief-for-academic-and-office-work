"""Tests for the coding-agent pack compiler.

These guard the packaging, not the prose: every profile must be well-formed
and honest about what was verified, and every generated file must be valid
for the agent it targets.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import compile as compile_mod  # noqa: E402

VARIANT_KEYS = ("unified", "be-brief-output", "caveman-output", "grug-reasoning")


@pytest.fixture(scope="module")
def compiled():
    subprocess.run([sys.executable, str(ROOT / "compile.py")], check=True, cwd=ROOT.parent)
    return ROOT / "packs"


# ── profiles ─────────────────────────────────────────────────────────────────


def test_every_profile_validates():
    profiles = compile_mod.load_profiles()
    assert len(profiles) >= 6
    for profile in profiles:
        assert profile["schema_version"] == "1"


@pytest.mark.parametrize("agent", ["qwen", "claude", "codex", "cursor", "copilot", "opencode"])
def test_expected_agents_exist(agent):
    path = ROOT / "profiles" / f"{agent}.json"
    assert path.is_file(), f"missing profile for {agent}"


def test_qwen_is_a_first_class_profile():
    """Qwen Code is why this section exists — it must not silently regress."""
    profile = json.loads((ROOT / "profiles" / "qwen.json").read_text(encoding="utf-8"))
    assert profile["display_name"] == "Qwen Code"
    assert "~/.qwen/QWEN.md" in profile["instruction"]["global_paths"]
    assert "QWEN.md" in profile["instruction"]["project_paths"]
    assert profile["skills"]["supported"] is True
    assert "~/.qwen/skills" in profile["skills"]["user_dirs"]
    assert ".qwen/skills" in profile["skills"]["project_dirs"]


def test_malformed_profile_is_rejected():
    with pytest.raises(ValueError, match="missing required key"):
        compile_mod.validate_profile({"id": "broken"})
    with pytest.raises(ValueError, match="unknown instruction format"):
        compile_mod.validate_profile({
            "schema_version": "1", "id": "x", "display_name": "X", "vendor": "V",
            "homepage": "https://example.com", "binary_names": ["x"],
            "install": "true", "wire_protocol": "openai-chat",
            "instruction": {"method": "file", "format": "docx", "frontmatter": False,
                            "project_paths": ["a.md"]},
            "verification": {"tested_agent_version": "unverified",
                             "last_verified_at": "2026-01-01",
                             "verified_by": "documentation review",
                             "source": "https://example.com"},
        })


def test_unverified_versions_must_explain_themselves():
    base = {
        "schema_version": "1", "id": "x", "display_name": "X", "vendor": "V",
        "homepage": "https://example.com", "binary_names": ["x"],
        "install": "true", "wire_protocol": "openai-chat",
        "instruction": {"method": "file", "format": "markdown", "frontmatter": False,
                        "project_paths": ["a.md"]},
        "verification": {"tested_agent_version": "unverified",
                         "last_verified_at": "2026-01-01",
                         "verified_by": "vibes",
                         "source": "https://example.com"},
    }
    with pytest.raises(ValueError, match="does not say how"):
        compile_mod.validate_profile(dict(base))


# ── variants ─────────────────────────────────────────────────────────────────


def test_all_four_variants_load_with_frontmatter():
    variants = compile_mod.load_variants()
    for key in VARIANT_KEYS:
        assert key in variants, f"missing variant {key}"
        assert variants[key].name, f"{key} has no name"
        assert variants[key].description, f"{key} has no description"


def test_variant_layers_are_declared():
    variants = compile_mod.load_variants()
    assert variants["grug-reasoning"].meta["layer"] == "reasoning"
    assert variants["caveman-output"].meta["layer"] == "output"
    assert variants["be-brief-output"].meta["register"] == "be_brief"
    assert variants["caveman-output"].meta["register"] == "caveman"


# ── generated packs ──────────────────────────────────────────────────────────


@pytest.mark.parametrize("agent", ["qwen", "claude", "codex", "cursor", "copilot", "opencode"])
def test_every_agent_gets_every_variant(compiled, agent):
    agent_dir = compiled / agent
    assert (agent_dir / "README.md").is_file()
    for key in VARIANT_KEYS:
        assert (agent_dir / f"{key}.md").is_file(), f"{agent} missing {key}.md"


def test_paste_files_have_no_frontmatter(compiled):
    """A context file is pasted verbatim — frontmatter there is pure noise."""
    for path in compiled.glob("*/*.md"):
        if path.name == "README.md":
            continue
        assert not path.read_text(encoding="utf-8").startswith("---"), path


@pytest.mark.parametrize("agent", ["qwen", "claude", "codex"])
def test_skill_dirs_have_valid_frontmatter(compiled, agent):
    for skill in (compiled / agent / "skills").glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        assert match, f"{skill} has unterminated frontmatter"
        block = match.group(1)
        assert "name:" in block, f"{skill} frontmatter missing name"
        assert "description:" in block, f"{skill} frontmatter missing description"
        yaml = pytest.importorskip("yaml")
        parsed = yaml.safe_load(block)
        assert "name" in parsed and "description" in parsed


def test_cursor_rules_use_mdc_frontmatter(compiled):
    rules = list((compiled / "cursor" / "rules").glob("*.mdc"))
    assert len(rules) == len(VARIANT_KEYS)
    yaml = pytest.importorskip("yaml")
    for rule in rules:
        text = rule.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        assert match, f"{rule} has no frontmatter — Cursor would ignore it"
        parsed = yaml.safe_load(match.group(1))
        # Cursor reads exactly three fields, and alwaysApply is what makes
        # the rule load without a glob match.
        assert set(parsed) == {"description", "globs", "alwaysApply"}, parsed
        assert parsed["alwaysApply"] is True


def test_zip_is_generated(compiled):
    import zipfile

    zip_path = compiled / "coding-agents.zip"
    assert zip_path.is_file()
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        assert "README.md" in names
        assert "qwen/unified.md" in names
        assert not any(name.endswith(".zip") for name in names)
