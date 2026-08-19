# Claude Skills — Verified Installation Guide

Two skill formats exist, verified against Anthropic's official documentation (support.claude.com, 2026):

| Surface | Format | File | Description limit |
|---------|--------|------|-------------------|
| **Claude app & website** (Customize > Skills) | `## Metadata` section | `skill.md` (lowercase) | 200 chars |
| **Claude Code / agent SDK** | `---` YAML frontmatter | `SKILL.md` (uppercase) | 1024 chars |

```
claude-skills/
├── app/          # Claude app & claude.ai (upload ZIP)
│   ├── caveman-be-brief/skill.md      # ALL-IN-ONE: grug + caveman + be brief
│   ├── caveman/skill.md               # cut-the-fluff compression
│   ├── caveman-compress/skill.md      # document condensing
│   ├── caveman-review/skill.md        # line-numbered review
│   ├── grug-reasoning/skill.md        # internal Grug thinking only
│   ├── ralph-wiggum/skill.md          # optional polish loop (OFF by default)
│   └── zips/                          # ready-to-upload packages
└── code/         # Claude Code & SKILL.md-standard agents
    ├── caveman-be-brief/SKILL.md
    ├── caveman/
    ├── caveman-compress/
    ├── caveman-review/
    ├── claude-reasoning-caveman/
    └── ralph-wiggum/
```

---

## Your Packaging Options (pick one strategy)

### Option 1: ALL-IN-ONE (recommended daily driver)
One skill, one ZIP: **`caveman-be-brief.zip`** = Grug thinking + caveman output + be brief.
Install this alone for day-to-day thesis/report/email work.

### Option 2: SEPARATE SKILLS (modular)
Each layer as its own ZIP, installed independently:
- `grug-reasoning.zip` — internal reasoning only
- `caveman.zip` — compression only
- `caveman-compress.zip` — shrink long docs before sending to AI
- `caveman-review.zip` — one-line review comments

### Option 3: ALL-IN-ONE + RALPH (full control)
Install **`caveman-be-brief.zip`** + **`ralph-wiggum.zip`**:

| Scenario | What to do |
|----------|------------|
| **Deadline, low tokens** | Leave `ralph-wiggum` OFF. caveman-be-brief does one fast pass. Say "I want it fast, I don't have tokens to spare." |
| **Have time, need polish** | Say "ralph on" — Claude loads the ralph-wiggum skill and loops until quality is met. |
| **Quick double-check** | Say "ralph once" — one verification pass, then stop. |

Ralph is a **separate skill you toggle independently** — no coupling, no forced token burn.
It only activates when you invoke it, so it never slows down your deadline work.

---

## A. Claude App & claude.ai (Windows desktop app, web, Cowork)

Verified: works on **Free, Pro, Max, Team, Enterprise** plans. Requires **code execution enabled**.

### One-time setup
1. Open Claude → **Settings → Capabilities** → turn on **"Code execution and file creation"** (required for skills).
2. Go to **Customize → Skills** (also at `claude.ai/customize/skills`).

### Install each skill
1. In **Customize → Skills**, click **"+" → "+ Create skill" → "Upload a skill"**.
2. Upload a ZIP from `claude-skills/app/zips/` (e.g. `caveman-be-brief.zip`, `ralph-wiggum.zip`).
3. Claude reads `skill.md`, shows a summary — confirm.
4. **Toggle the skill ON** (uploaded ≠ enabled). Leave `ralph-wiggum` OFF until you need polish.
5. Test with a trigger prompt (e.g. "review this doc" / "caveman mode — draft this section").

### Using it
- Skills auto-trigger when your request matches the skill's description.
- In chat: "caveman mode — draft this thesis section" or "/caveman".
- Type `/` in the sidebar (or Cowork) to see available skills.

---

## B. Claude Code (terminal / CLI)

### Personal (all projects)
```bash
mkdir -p ~/.claude/skills
cp -r claude-skills/code/* ~/.claude/skills/
```
Restart Claude Code. Verify: ask Claude to "list your skills".

### Project-level (shared via git)
```bash
mkdir -p .claude/skills
cp -r claude-skills/code/* .claude/skills/
```
Commit and push. This repo already ships `.claude/skills/` — opening this repo in Claude Code auto-loads all 6 skills.

### Alternative: `npx skills add`
If you publish the repo on GitHub, users can install with:
```bash
npx skills add <your-repo-url> --agent claude-code
```

---

## C. Other agents using the SKILL.md standard (Open Agent Skills spec)

The `code/` format follows the open [agentskills.io](https://agentskills.io) standard, so the same folders work on other agents:

| Agent | Location |
|-------|----------|
| Codex CLI (OpenAI) | `~/.codex/skills/` |
| Cursor | `.cursor/skills/` (project) |
| OpenClaw | `~/.openclaw/skills/` |
| Claude Agent SDK | wire skills into custom agents programmatically |

Copy `claude-skills/code/*` into the corresponding folder and restart the agent.

---

## D. Models WITHOUT skill support (Gemini, ChatGPT, Qwen, Grok, DeepSeek, Kimi)

No skill system → use **pseudo-skills**: paste the frontmatter-free markdown into
Settings → Custom Instructions (or at conversation start). Same behavior, minus auto-triggering.
See `../../pseudo-skills/`.

| Model | Where to paste |
|-------|----------------|
| Gemini | Settings → Custom Instructions |
| Qwen app (Android/web) | Settings → System Prompt |
| ChatGPT | Custom instructions |
| Grok / DeepSeek / Kimi | at conversation start |

**For the on/off Ralph control on these models:** just don't paste `ralph-wiggum.md`
(or remove it) when low on tokens; paste it back when you want polish. Or keep it pasted
and rely on the commands — it's OFF by default and only loops when you say "ralph on".

---

## Format notes (for edits)

- **app/** skills: `## Metadata` block with `name` (≤64 chars) + `description` (≤200 chars), then markdown body. ZIP must contain the **folder as root** (folder/skill.md), not loose files.
- **code/** skills: `---` YAML frontmatter with `name` (kebab-case, must match folder name) + `description` (≤1024 chars), then markdown body.
- Keep `app/`, `code/`, `caveman-universal/skills/`, and `pseudo-skills/` in sync when rules change.
- Re-zip after editing: `cd claude-skills/app && zip -r zips/<name>.zip <name>/`

## All 6 ZIPs in `app/zips/`

| ZIP | What it is | Install when |
|-----|-----------|--------------|
| `caveman-be-brief.zip` | ALL-IN-ONE daily driver (grug + caveman + be brief) | Default |
| `caveman.zip` | Cut-the-fluff compression only | Modular setup |
| `grug-reasoning.zip` | Internal Grug reasoning only | Modular setup |
| `caveman-compress.zip` | Document condensing | Need to shrink docs |
| `caveman-review.zip` | One-line review comments | Document review |
| `ralph-wiggum.zip` | Optional polish loop (OFF by default) | Have time for polish |