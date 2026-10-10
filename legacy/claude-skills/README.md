# Claude Skills — install guide

One skill, one format. Everything the old six-skill matrix covered is inside it.

| Surface | What to install | How |
|---|---|---|
| **Claude app & claude.ai** (Settings → Customize → Skills → Upload) | [`zips/one-skill.zip`](zips/one-skill.zip) | upload the ZIP |
| **Claude Code / agent SDK** | [`app/one-skill/`](app/one-skill/) | `cp -r claude-skills/app/one-skill ~/.claude/skills/`, or open this repo: [`.claude/skills/one-skill/`](../.claude/skills/one-skill) auto-loads |
| **Codex, Cursor, Copilot, OpenCode, Qwen Code** | same folder | copy it into the agent's skill directory; paste [`../../pseudo-skills/one-skill.md`](../pseudo-skills/one-skill.md) where there is no uploader |

Format requirements, still verified against Anthropic's docs:

* the ZIP must contain `one-skill/SKILL.md`
* `SKILL.md` must start with `---` on line 1
* `name` + `description` are the only frontmatter fields the surface requires; the
  description limit is 200 chars on the app and 1024 on Claude Code, and this one is
  written for the wider limit. On the app, trim the description in the upload dialog
  rather than editing the file — the file is generated.

## Do not hand-edit anything here

`app/one-skill/` is a copy of [`../one-skill/dist/skill/`](../one-skill/dist/skill),
which `python one-skill/build.py` writes from
[`../one-skill/sources.json`](../one-skill/sources.json). A hand edit is overwritten
on the next build, and CI fails the pull request that ships one. To change what the
skill says, change the manifest or [`one-skill/core/`](../one-skill/core) and rebuild.

## What is inside

| Path | What it is |
|---|---|
| `SKILL.md` | the always-loaded half: nine universal rules, precedence by destination, the router, the command table |
| `references/*.md` | ten on-demand files, one per destination: prose, chat, thinking, code craft, ship workflow, UI, reflow + access, repo setup, teaching, origins |
| `references/SOURCES.md` | which upstream file every section came from, what was not carried, and why |
| `scripts/` | the carried executables: `contrast-check.py` (WCAG AA gate), `block-dangerous-git.sh`, the diagnosis and wizard templates |
| `BUILD.json` | checksum of every input, so a vendored file that moved without a rebuild is detectable |

The `SKILL.md` of the previous setup was ~1.5k words across six documents; this one
is ~2.4k words plus nothing, and the 75k words behind it are read a file at a time.

## Six-skill era

The old per-platform matrix — `caveman`, `caveman-be-brief`, `caveman-compress`,
`caveman-review`, `grug-reasoning`, `ralph-wiggum`, with their ZIPs — is in
[`../legacy/claude-skills/`](../legacy/claude-skills), including this file's
predecessor. They stay readable for reference and for `skillopt-integration/`, and
they are no longer install paths.
