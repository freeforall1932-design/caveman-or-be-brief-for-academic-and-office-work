# Qwen Chat Agent — install

Vendor: Alibaba / Qwen · <https://chat.qwen.ai/>

## Pick one variant

| Variant | File | Use when |
|---|---|---|
| Unified — grug decides, caveman measures, be-brief writes ★ | [`unified.md`](unified.md) | Recommended default. One agent, both jobs — developer chat and documents. |
| Be Brief — professional prose for documents | [`be-brief-output.md`](be-brief-output.md) | Thesis, journal, report, memo, professional email. Full grammar. |
| Caveman — terse register for developer chat | [`caveman-output.md`](caveman-output.md) | Official caveman register. Fragments OK, code never touched. |
| Grug — internal reasoning layer (no output rules) | [`grug-reasoning.md`](grug-reasoning.md) | Pair with an output variant — this one governs decisions only. |

★ = recommended default for Qwen Chat Agent.

**Load one output register at a time.** `be-brief-output` and
`caveman-output` contradict each other on grammar; loading both gives you
inconsistent output rather than a clear winner.
`grug-reasoning` is the exception — it is a reasoning layer with no output
rules, so it composes with either one.

## Install

Install the agent: `Open https://chat.qwen.ai/ and start an agent session (no CLI to install)`

### Option A — upload [`workspace/`](workspace/) or paste its text

Attach one variant file from [`workspace/`](workspace/) to the agent's workspace, or paste its text at the start of a session.
No frontmatter — these read as ordinary text, which is the route that
works whether or not the agent parses skill files.

> This is the agent mode inside Qwen Chat, with a workspace you can attach files to. It is a DIFFERENT product from Qwen Code, the terminal CLI (see profiles/qwen.json). There is no ~/.qwen directory and no CLI to configure: instructions reach the agent by uploading a file into the workspace, or by pasting text at the start of a session. Because the workspace ingests uploaded files, a SKILL.md may or may not be parsed for its frontmatter — this is UNVERIFIED. The dependable route is a plain .md file with no frontmatter, which is read as ordinary text. That is why the pseudo-skill fallback exists.

## Quirks

- No verified skill-file convention. Treat SKILL.md frontmatter as a bonus if it is honoured, not as a dependency — the instructions must stand on their own as plain text.
- Upload size and file-type limits are set by the product and can change; keep the instruction file small so it survives them.
- Because there is no session-start hook, the instructions must be re-attached or re-pasted when a session resets.
- If the agent has a code-execution or file tool, the code-preservation rule matters here too: uploaded and generated files are real files.

## Verification

- Tested agent version: `unverified`
- Last verified: 2026-09-17
- Verified by: documentation review — no public specification of Qwen Chat Agent's instruction-file conventions was found, so nothing here is asserted about frontmatter parsing. Upload/paste is treated as the only dependable route.
- Source: <https://chat.qwen.ai/>
