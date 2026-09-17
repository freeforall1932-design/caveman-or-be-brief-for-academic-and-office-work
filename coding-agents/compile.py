#!/usr/bin/env python3
"""
Compile per-agent instruction packs.

Sources of truth:
  variants/*.md   — the four rule documents (grug / caveman / be-brief / unified)
  profiles/*.json — where each agent reads instructions from, and its quirks

Generated (committed, do not hand-edit):
  packs/<agent>/README.md                 install notes for that agent
  packs/<agent>/<variant>.md              paste-ready instruction file
  packs/<agent>/skills/<variant>/SKILL.md frontmatter skill (where supported)
  packs/<agent>/rules/<variant>.mdc       Cursor .mdc rule (Cursor only)
  packs/README.md                         index
  packs/coding-agents.zip                 everything, for easy download

    python coding-agents/compile.py

Design notes
------------
The generated instruction files contain **only instructions** — no install
prose — because every character in them is billed on every request. Install
notes live in the per-agent README instead.

Frontmatter is format-aware, because the agents disagree:

  * Claude Code / Qwen Code / Codex skills  → YAML frontmatter REQUIRED
    (name + description), in <name>/SKILL.md
  * QWEN.md / AGENTS.md / CLAUDE.md paste   → frontmatter stripped; it is
    noise in a context file
  * Cursor .cursor/rules/*.mdc              → frontmatter REQUIRED and with
    different fields (description, globs, alwaysApply); a plain .md file in
    that directory is ignored
"""

from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VARIANTS_DIR = ROOT / "variants"
PROFILES_DIR = ROOT / "profiles"
PACKS_DIR = ROOT / "packs"

VARIANT_ORDER = ["unified", "be-brief-output", "caveman-output", "grug-reasoning"]
VARIANT_LABEL = {
    "unified": "Unified — grug decides, caveman measures, be-brief writes",
    "be-brief-output": "Be Brief — professional prose for documents",
    "caveman-output": "Caveman — terse register for developer chat",
    "grug-reasoning": "Grug — internal reasoning layer (no output rules)",
}
VARIANT_BLURB = {
    "unified": "Recommended default. One agent, both jobs — developer chat and documents.",
    "be-brief-output": "Thesis, journal, report, memo, professional email. Full grammar.",
    "caveman-output": "Official caveman register. Fragments OK, code never touched.",
    "grug-reasoning": "Pair with an output variant — this one governs decisions only.",
}

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


@dataclass
class Variant:
    """A skill: SKILL.md body plus its progressive-disclosure support files."""
    key: str
    body: str
    meta: dict = field(default_factory=dict)
    references: "dict[str, str]" = field(default_factory=dict)
    examples: str = ""
    raw: str = ""  # the SKILL.md exactly as authored — frontmatter included

    @property
    def is_packaged(self) -> bool:
        """True when this variant ships as a directory with support files.

        A real skill keeps its reference material in separate files so the
        agent loads it only when needed. A flat instruction file has nowhere
        to put them, which is exactly why it stays a pseudo-skill.
        """
        return bool(self.references or self.examples)

    @property
    def name(self) -> str:
        return str(self.meta.get("name") or self.key)

    @property
    def description(self) -> str:
        raw = self.meta.get("description") or ""
        # Frontmatter descriptions are often folded YAML scalars.
        return re.sub(r"\s+", " ", str(raw)).strip()


def load_variants() -> dict[str, Variant]:
    variants: dict[str, Variant] = {}
    for path in sorted(VARIANTS_DIR.glob("*/SKILL.md")):
        raw = path.read_text(encoding="utf-8")
        match = _FRONTMATTER_RE.match(raw)
        meta: dict = {}
        body = raw
        if match:
            body = raw[match.end():]
            for line in match.group(1).splitlines():
                if line.strip().startswith("- ") or not line.strip():
                    continue
                if ":" in line:
                    key, _, value = line.partition(":")
                    key = key.strip()
                    value = value.strip()
                    if value.startswith(">") or value == "":
                        continue  # folded block scalar opener
                    meta[key] = value.strip('"').strip("'")
            # Capture folded description blocks that span lines.
            folded = re.search(r"^description:\s*>\s*\n((?:\s+\S.*\n?)+)", match.group(1), re.M)
            if folded:
                meta["description"] = re.sub(r"\s+", " ", folded.group(1)).strip()
        key = path.parent.name
        skill_dir = path.parent
        references: dict[str, str] = {}
        for ref in sorted((skill_dir / "references").glob("*.md")):
            references[ref.name] = ref.read_text(encoding="utf-8").strip()
        examples_path = skill_dir / "examples.md"
        examples = (
            examples_path.read_text(encoding="utf-8").strip()
            if examples_path.exists()
            else ""
        )
        variants[key] = Variant(
            key=key,
            body=body.strip() + "\n",
            meta=meta,
            references=references,
            examples=examples,
            raw=raw,
        )
    return variants


REQUIRED_PROFILE_KEYS = (
    "schema_version", "id", "display_name", "vendor", "homepage",
    "binary_names", "install", "wire_protocol", "instruction", "verification",
)
REQUIRED_INSTRUCTION_KEYS = ("method", "format", "frontmatter")
VALID_FORMATS = ("markdown", "mdc", "skill-md")
# "web-workspace" = a hosted agent with an uploadable workspace and no CLI.
# There is no config directory to write to, so paths do not apply.
VALID_WIRE_PROTOCOLS = (
    "openai-chat", "openai-responses", "anthropic-messages", "acp", "web-workspace"
)


def validate_profile(profile: dict, source: str = "<profile>") -> None:
    """Fail loudly on a malformed profile rather than emitting a broken pack.

    Honesty matters more than convenience here: a profile that claims a path
    or format we have not verified would send a user to a file their agent
    never reads.
    """
    missing = [key for key in REQUIRED_PROFILE_KEYS if key not in profile]
    if missing:
        raise ValueError(f"{source}: missing required key(s): {', '.join(missing)}")

    if profile["schema_version"] != "1":
        raise ValueError(f"{source}: unsupported schema_version {profile['schema_version']!r}")

    instruction = profile["instruction"]
    missing = [key for key in REQUIRED_INSTRUCTION_KEYS if key not in instruction]
    if missing:
        raise ValueError(f"{source}: instruction missing key(s): {', '.join(missing)}")

    if instruction["format"] not in VALID_FORMATS:
        raise ValueError(
            f"{source}: unknown instruction format {instruction['format']!r} "
            f"(expected one of {', '.join(VALID_FORMATS)})"
        )

    if profile["wire_protocol"] not in VALID_WIRE_PROTOCOLS:
        raise ValueError(
            f"{source}: unknown wire_protocol {profile['wire_protocol']!r} "
            f"(expected one of {', '.join(VALID_WIRE_PROTOCOLS)})"
        )

    is_web = profile["wire_protocol"] == "web-workspace"
    if is_web:
        # A hosted workspace agent has no config directory. Insisting on a path
        # here would force the profile to invent one, and the whole point of
        # these profiles is to never state an unverified path.
        if not instruction.get("paste_dir"):
            raise ValueError(
                f"{source}: web-workspace agent must declare instruction.paste_dir — "
                "the directory its uploadable files are prepared into"
            )
    elif not instruction.get("project_paths") and not instruction.get("global_paths"):
        raise ValueError(f"{source}: instruction declares no install path at all")

    verification = profile["verification"]
    for key in ("tested_agent_version", "last_verified_at", "verified_by", "source"):
        if key not in verification:
            raise ValueError(f"{source}: verification missing {key!r}")

    # A version we have not tested must say so, never a plausible-looking guess.
    if verification["tested_agent_version"] == "unverified":
        if "documentation review" not in verification["verified_by"]:
            raise ValueError(
                f"{source}: tested_agent_version is 'unverified' but verified_by does not "
                "say how the paths were established"
            )


def load_profiles() -> list[dict]:
    profiles = []
    for path in sorted(PROFILES_DIR.glob("*.json")):
        profile = json.loads(path.read_text(encoding="utf-8"))
        validate_profile(profile, source=path.name)
        if profile["id"] != path.stem:
            raise ValueError(f"{path.name}: id {profile['id']!r} must match the filename")
        profiles.append(profile)
    return profiles


def _paths(values: list[str]) -> str:
    return "\n".join(f"- `{value}`" for value in values) or "- (none)"


def render_agent_readme(profile: dict, variants: dict[str, Variant]) -> str:
    instruction = profile["instruction"]
    skills = profile.get("skills")
    recommended = profile.get("recommended_variant", "unified")

    lines: list[str] = []
    lines.append(f"# {profile['display_name']} — install")
    lines.append("")
    lines.append(f"Vendor: {profile['vendor']} · <{profile['homepage']}>")
    lines.append("")
    lines.append("## Pick one variant")
    lines.append("")
    lines.append("| Variant | File | Use when |")
    lines.append("|---|---|---|")
    for key in VARIANT_ORDER:
        if key not in variants:
            continue
        star = " ★" if key == recommended else ""
        lines.append(f"| {VARIANT_LABEL[key]}{star} | [`{key}.md`]({key}.md) | {VARIANT_BLURB[key]} |")
    lines.append("")
    lines.append(f"★ = recommended default for {profile['display_name']}.")
    lines.append("")
    lines.append("**Load one output register at a time.** `be-brief-output` and")
    lines.append("`caveman-output` contradict each other on grammar; loading both gives you")
    lines.append("inconsistent output rather than a clear winner.")
    lines.append("`grug-reasoning` is the exception — it is a reasoning layer with no output")
    lines.append("rules, so it composes with either one.")
    lines.append("")
    lines.append("## Install")
    lines.append("")
    lines.append(f"Install the agent: `{profile['install']}`")
    lines.append("")
    is_web = profile["wire_protocol"] == "web-workspace"
    if is_web:
        # A hosted workspace agent has no instruction file to paste into; the
        # file itself is uploaded, or its text pasted into the session.
        lines.append(
            f"### Option A — upload [`{instruction['paste_dir']}/`]({instruction['paste_dir']}/) "
            "or paste its text"
        )
    else:
        lines.append("### Option A — paste into the instruction file")
    lines.append("")
    if instruction["global_paths"]:
        lines.append("Global (all projects):")
        lines.append("")
        lines.append(_paths(instruction["global_paths"]))
        lines.append("")
    if instruction["project_paths"]:
        lines.append("Project (this repo only):")
        lines.append("")
        lines.append(_paths(instruction["project_paths"]))
        lines.append("")
    if is_web:
        lines.append(
            f"Attach one variant file from [`{instruction['paste_dir']}/`]({instruction['paste_dir']}/) "
            "to the agent's workspace, or paste its text at the start of a session.\n"
            "No frontmatter — these read as ordinary text, which is the route that\n"
            "works whether or not the agent parses skill files."
        )
    else:
        lines.append(
            "Copy the contents of one variant file from this directory into it — no\n"
            "frontmatter, ready to paste."
        )
    lines.append("")
    if instruction.get("notes"):
        lines.append(f"> {instruction['notes']}")
        lines.append("")

    if skills and skills.get("supported"):
        lines.append("### Option B — install as a skill")
        lines.append("")
        for directory in skills.get("user_dirs", []):
            lines.append(f"- user: `{directory}/<name>/SKILL.md`")
        for directory in skills.get("project_dirs", []):
            lines.append(f"- project: `{directory}/<name>/SKILL.md`")
        lines.append("")
        lines.append("Generated, frontmatter-complete skill files: [`skills/`](skills/).")
        lines.append("")
        if skills.get("notes"):
            lines.append(f"> {skills['notes']}")
            lines.append("")

    if Path(ROOT / "packs" / profile["id"] / "rules").exists() or instruction["format"] == "mdc":
        lines.append("### Option C — Cursor project rule")
        lines.append("")
        lines.append("Generated `.mdc` rules with correct frontmatter: [`rules/`](rules/).")
        lines.append("")
        lines.append("```bash")
        lines.append("mkdir -p .cursor/rules")
        lines.append(f"cp packs/{profile['id']}/rules/unified.mdc .cursor/rules/caveman-unified.mdc")
        lines.append("```")
        lines.append("")
        lines.append("> The `.mdc` extension is load-bearing — a plain `.md` file in")
        lines.append("> `.cursor/rules/` is ignored, because it has no frontmatter to declare")
        lines.append("> when it applies.")
        lines.append("")

    if profile.get("quirks"):
        lines.append("## Quirks")
        lines.append("")
        for quirk in profile["quirks"]:
            lines.append(f"- {quirk}")
        lines.append("")

    verification = profile["verification"]
    lines.append("## Verification")
    lines.append("")
    lines.append(f"- Tested agent version: `{verification['tested_agent_version']}`")
    lines.append(f"- Last verified: {verification['last_verified_at']}")
    lines.append(f"- Verified by: {verification['verified_by']}")
    lines.append(f"- Source: <{verification['source']}>")
    lines.append("")
    return "\n".join(lines)


_EXTERNAL_LINK_RE = re.compile(r"\[([^\]]+)\]\((\.\./[^)]+)\)")


def _external_links_to_text(text: str) -> str:
    """Turn links pointing outside the pack into plain paths.

    Inside the repo, `../../philosophy/caveman.md` resolves. Once the file is
    copied into packs/<agent>/skills/<name>/ it does not, and a broken link is
    worse than a bare path the reader can find in the same repo.
    """
    return _EXTERNAL_LINK_RE.sub(lambda m: f"`{m.group(2)}`", text)


def render_flattened(variant: Variant) -> str:
    """SKILL.md body + inlined support files, as one self-contained document.

    A pasted instruction file has no filesystem beside it, so relative links to
    references/ would be dead on arrival. The support material is therefore
    appended inline. This is the pseudo-skill route: the same content, delivered
    as text an agent will read regardless of whether it parses frontmatter.
    """
    body = _external_links_to_text(variant.body).strip()
    if variant.references or variant.examples:
        # The source SKILL.md ends with a "Reference material" block that links
        # to references/ and examples.md. Those links are dead in a pasted file
        # and the content follows inline, so the pointer block is dropped.
        body = re.sub(
            r"\n?## Reference material\n(?:\n|[-*].*\n|.*\n)*?(?=\n## |\Z)",
            "\n",
            body,
        ).strip()
    parts = [body]
    if variant.references:
        parts.append("")
        parts.append("---")
        parts.append("")
        parts.append("## Reference material (inlined)")
        parts.append("")
        for name in sorted(variant.references):
            body = _external_links_to_text(variant.references[name]).strip()
            # Promote the file's H1 to H2 so the inlined sections nest correctly.
            body = re.sub(r"^#\s+", "## ", body, count=1)
            parts.append(body)
            parts.append("")
            parts.append("---")
            parts.append("")
    if variant.examples:
        body = _external_links_to_text(variant.examples).strip()
        body = re.sub(r"^#\s+", "## ", body, count=1)
        parts.append(body)
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_paste_file(variant: Variant, profile: dict) -> str:
    """Plain markdown, frontmatter stripped, ready to paste into a context file."""
    return render_flattened(variant)


def render_skill_file(variant: Variant, profile: dict) -> str:
    """The SKILL.md itself, emitted verbatim.

    The source SKILL.md already carries the complete frontmatter — name,
    description, version, layer, register, triggers, metadata, and for
    grug-reasoning a disallowed-tools list. Rewriting it here would strip the
    optional fields that make it a real skill rather than a text file, so the
    only change is rewriting links that would break once copied.
    """
    return _external_links_to_text(variant.raw).strip() + "\n"


def _yaml_scalar(value: str) -> str:
    """Render *value* as a YAML double-quoted scalar.

    Descriptions contain colons, commas and apostrophes. An unquoted YAML
    scalar breaks on the first ": " — which would make the entire frontmatter
    unparseable, and Cursor would silently ignore the rule.
    """
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_mdc_file(variant: Variant, profile: dict) -> str:
    """Cursor .cursor/rules/*.mdc — description + globs + alwaysApply.

    Cursor reads exactly three frontmatter fields and ignores a plain .md
    file in .cursor/rules/, so getting this block right is the difference
    between a rule that loads and one that silently does nothing. Cursor rules
    are single files, so the support material is inlined.
    """
    description = variant.description or VARIANT_BLURB[variant.key]
    return (
        "---\n"
        f"description: {_yaml_scalar(description)}\n"
        "globs: \n"
        "alwaysApply: true\n"
        "---\n\n"
        + render_flattened(variant).strip()
        + "\n"
    )


def render_index(profiles: list[dict], variants: dict[str, Variant]) -> str:
    lines = [
        "# Coding agent packs",
        "",
        "**Generated by `python coding-agents/compile.py`. Do not hand-edit.**",
        "",
        "Sources of truth: [`../variants/`](../variants/) (the four rule documents) and",
        "[`../profiles/`](../profiles/) (where each agent reads instructions from).",
        "",
        "## Agents",
        "",
        "| Agent | Instruction file(s) | Recommended |",
        "|---|---|---|",
    ]
    for profile in profiles:
        paths = ", ".join(
            profile["instruction"]["project_paths"][:2] or profile["instruction"]["global_paths"][:1]
        )
        lines.append(
            f"| [{profile['display_name']}]({profile['id']}/README.md) "
            f"| `{paths}` | {profile.get('recommended_variant', 'unified')} |"
        )
    lines += [
        "",
        "## Variants",
        "",
        "| Variant | What it governs |",
        "|---|---|",
    ]
    for key in VARIANT_ORDER:
        if key in variants:
            lines.append(f"| `{key}` | {VARIANT_BLURB[key]} |")
    lines += [
        "",
        "## Rules of thumb",
        "",
        "- **One output register per agent.** `be-brief-output` and `caveman-output`",
        "  contradict each other on grammar.",
        "- **`grug-reasoning` composes with either one** — it has no output rules.",
        "- **Use `unified` if unsure.** It assigns each philosophy to a layer where it",
        "  does not collide with the others.",
        "- Every agent reads `AGENTS.md` except Cursor (prefers `.mdc`) — if you want",
        "  one file to work everywhere, start there.",
        "",
        "See [`../philosophy/conflicts.md`](../philosophy/conflicts.md) for why the three",
        "philosophies are kept apart, and how `unified` resolves them.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    variants = load_variants()
    profiles = load_profiles()

    if PACKS_DIR.exists():
        for child in PACKS_DIR.iterdir():
            if child.is_dir():
                for inner in sorted(child.rglob("*"), reverse=True):
                    inner.unlink() if inner.is_file() else inner.rmdir()
                child.rmdir()
            elif child.suffix != ".zip":
                child.unlink()

    for profile in profiles:
        agent_dir = PACKS_DIR / profile["id"]
        agent_dir.mkdir(parents=True, exist_ok=True)
        instruction = profile["instruction"]
        skills = profile.get("skills")

        # Hosted workspace agents get a dedicated folder, because their files are
        # uploaded rather than written into the repo.
        paste_dir = agent_dir
        if instruction.get("paste_dir"):
            paste_dir = agent_dir / instruction["paste_dir"]
            paste_dir.mkdir(parents=True, exist_ok=True)

        (agent_dir / "README.md").write_text(
            render_agent_readme(profile, variants), encoding="utf-8"
        )

        for key in VARIANT_ORDER:
            if key not in variants:
                continue
            variant = variants[key]
            (paste_dir / f"{key}.md").write_text(
                render_paste_file(variant, profile), encoding="utf-8"
            )
            if skills and skills.get("supported"):
                skill_dir = agent_dir / "skills" / variant.name
                (skill_dir / "references").mkdir(parents=True, exist_ok=True)
                (skill_dir / "SKILL.md").write_text(
                    render_skill_file(variant, profile), encoding="utf-8"
                )
                # Progressive disclosure: the support files ship beside SKILL.md
                # so the agent loads them only when the task needs them. This is
                # what separates a skill from a single instruction document.
                for name in sorted(variant.references):
                    (skill_dir / "references" / name).write_text(
                        _external_links_to_text(variant.references[name]).strip() + "\n",
                        encoding="utf-8",
                    )
                if variant.examples:
                    (skill_dir / "examples.md").write_text(
                        _external_links_to_text(variant.examples).strip() + "\n",
                        encoding="utf-8",
                    )
            if instruction["format"] == "mdc":
                rules_dir = agent_dir / "rules"
                rules_dir.mkdir(parents=True, exist_ok=True)
                (rules_dir / f"{key}.mdc").write_text(
                    render_mdc_file(variant, profile), encoding="utf-8"
                )

    (PACKS_DIR / "README.md").write_text(render_index(profiles, variants), encoding="utf-8")

    zip_path = PACKS_DIR / "coding-agents.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKS_DIR.rglob("*")):
            if path.is_file() and path != zip_path:
                info = zipfile.ZipInfo(str(path.relative_to(PACKS_DIR)))
                # Fixed timestamp so the archive is byte-reproducible. Without
                # this, every compile run produces a different zip and CI's
                # "are the generated packs stale?" check fails on noise.
                info.date_time = (1980, 1, 1, 0, 0, 0)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, path.read_bytes())

    n_agents = len(profiles)
    n_variants = len([k for k in VARIANT_ORDER if k in variants])
    print(f"Compiled {n_agents} agents x {n_variants} variants -> {PACKS_DIR}")
    for profile in profiles:
        print(f"  {profile['id']:<10} {profile['display_name']}")


if __name__ == "__main__":
    main()
