# one-skill — the merge, and how to grow it

One skill, built from fifty others across three repositories. Nothing in
`dist/skill/` is hand-written, so nothing in it has to be kept in sync by hand.

```
one-skill/
├── sources.json      ★ the manifest: sources → skills → buckets. The only file to edit.
├── build.py            sync · build · install · all · check
├── core/               the hand-written integration layer (the merge's judgement)
│   ├── 00-open.md          what the layers are, the one line
│   ├── 10-precedence.md    who wins, by destination + the named conflicts
│   ├── 20-always-on.md     the nine rules that hold with no reference loaded
│   ├── 30-router.md         loop, router table (generated), registers, language
│   ├── 40-commands.md        the procedure table (generated) + how to run one
│   └── 50-sources.md          provenance summary (generated)
├── upstream/           vendored copies the builder reads (see PROVENANCE.json)
│   ├── local/                this repository, from `legacy/`
│   ├── anti-slop-fork/       freeforall1932-design/anti-slop-fork
│   └── mattpocock-skills/    mattpocock/skills, engineering + productivity + misc
├── dist/skill/         scratch build output (gitignored `dist/`; not a deliverable)
└── tests/
```

The **published** skill is what the install mirrors hold — `.claude/skills/one-skill/`,
`claude-skills/app/one-skill/` and the ZIP. `dist/` is scratch: the repository's
`.gitignore` keeps generated `dist/` out of git, so 1.3 MB is not committed four
times. `build.py check` therefore compares a fresh build against the *mirrors*, not
against `dist/` — a gate that walks a directory which may simply be absent reports
success on an empty tree, which is exactly how this bundle once shipped stale.

## Commands

```bash
python one-skill/build.py sync      # re-vendor upstream (clones into .cache/, gitignored)
python one-skill/build.py build     # upstream/ + core/ + sources.json → dist/skill/
python one-skill/build.py install   # mirror dist into every install path + rebuild the zip
python one-skill/build.py all       # build + install
python one-skill/build.py check     # rebuild in a temp dir and fail if dist/ is stale
python -m pytest one-skill/tests -q
```

`sync` needs network only to clone a source it does not have yet; `build` is
offline and deterministic (same inputs → same bytes).

## What the merge is

Two halves, deliberately separated:

* **`upstream/` + `dist/skill/references/` — verbatim.** Every rule set is the
  author's own wording. A body is changed only by four mechanical normalisations
  (frontmatter, heading level, link retargeting) plus the two declared escape
  hatches below. The `references/SOURCES.md` inside the skill lists exactly which
  sections lost what, and why.
* **`core/` — judgement.** Six short files that decide *which* of those rule sets
  governs *which* output. This is where grug, caveman, be-brief, antislop and
  Pocock's skills are reconciled, because they genuinely contradict each other:
  caveman says "drop articles, fragments OK", be-brief says "never broken grammar",
  antislop says "liveliness is added", and Pocock says "ask before you build".
  The resolution is **by destination**, never by averaging. See
  `core/10-precedence.md`.

Two escape hatches, both recorded in provenance, both fail-closed:

| Manifest key | For | Guard |
|---|---|---|
| `strip_sections` | upstream sections a *merged* skill must not obey (an install wizard that tells the agent to fetch files, duplicated rule restatements) | names a heading that no longer exists → build fails, so a stale strip cannot silently ship |
| `replace` | literal wording that would make the merged skill lie about its own layout (e.g. "the script sits next to this `SKILL.md`") | target string not found → build fails |

Anything else is left exactly as upstream wrote it.

## Adding a repository

This is the reason the manifest exists: the merge is a build step, so the fourth
source is an entry, not a rewrite.

**1.** Declare it in `sources.json` → `sources`:

```jsonc
{
  "slug": "my-new-source",
  "title": "owner/my-new-source — short description",
  "license": "MIT",
  "attribution": "owner/my-new-source",
  "origin": { "kind": "github", "repo": "owner/my-new-source", "ref": "HEAD" },
  "sync": {
    "include": [
      { "from": "skills", "to": "upstream/my-new-source", "skip": ["README.md", "agents"] }
    ]
  },
  "skills": [],
  "not_routed": []
}
```

`ref` may pin a tag or SHA; `HEAD` follows the default branch. `skip` drops
per-agent duplicates and non-instruction files at vendoring time.

**2.** `python one-skill/build.py sync` — the files land in `upstream/` and their
revision is recorded in `upstream/PROVENANCE.json`.

**3.** Add one entry per skill you want merged, into that source's `skills`:

```jsonc
{
  "id": "new-skill",                    // the name a user says, if it is a procedure
  "bucket": "code-craft",               // an existing destination; see buckets[]
  "order": 70,                          // position inside the bucket file
  "title": "New skill — one clause on what it governs",
  "when": "the sentence that belongs in the router table",
  "command": true,                       // a procedure to offer, not to run unasked
  "entry": "upstream/my-new-source/new-skill/SKILL.md",
  "docs":    [{ "path": "upstream/my-new-source/new-skill/extra.md", "label": "Extra" }],
  "scripts": ["upstream/my-new-source/new-skill/check.py"]
}
```

`entry` is the body to carry. `docs` are sibling files that ride in the same
reference section, with links to them retargeted to in-file anchors. `scripts` are
copied to `scripts/` in the built skill, and `${CLAUDE_SKILL_DIR}/name.py` style runtime
paths are rewritten to the carried location.

**4.** `python one-skill/build.py all && python one-skill/build.py check`
and `python -m pytest one-skill/tests -q`.

The router table, the command table, the per-bucket index, the provenance block,
the counts and the `SKILL.md` frontmatter all regenerate. Nothing else in the
repository moves.

### Rules worth keeping while you do it

* **Route by destination, not by origin.** Two skills from different repos that
  govern the same output belong in the same reference file, adjacent — that is
  where a contradiction is visible to the reader instead of smuggled past them.
* **Carry verbatim.** If upstream is wrong for this package, drop the section by
  name with a reason, or declare a literal `replace`. Do not paraphrase someone's
  rules into agreement.
* **The always-on budget is real.** `SKILL.md` rides in every request;
  `build.py` fails it above `ALWAYS_ON_BUDGET` words (2400). When a new source
  wants a rule there, the answer is usually a reference file, or a cut.
* **Every vendored file is accounted for.** A file in `upstream/` that no skill
  routes and no source lists under `not_routed` fails the build: either merge it
  or record why it is not worth the tokens.
* **Add a bucket only for a new destination.** Ten buckets for four sources is
  already the point where a router needs to be a table rather than a list.

## Install paths refreshed by `install`

| Path | For |
|---|---|
| `.claude/skills/one-skill/` | Claude Code with this repo open |
| `claude-skills/app/one-skill/` + `claude-skills/app/zips/one-skill.zip` | Claude app/web upload |
| `pseudo-skills/one-skill.md` | paste-only models (the router half; see below) |

Paste-only platforms (Gemini, Qwen, ChatGPT, Grok, DeepSeek, Kimi) get `SKILL.md`
alone — the nine rules and the router — not a monolith of all 75k words, which
would cost more context than the writing saves. When a task needs a reference,
paste that file next to it. `coding-agents/` in `legacy/` shows how to compile a
paste file per agent if a monolith is genuinely what you want; that build was not
carried forward, and the pack generator is frozen there.

## History

`legacy/` holds the standalone skills this one replaces: the `caveman`,
`be-brief`, `grug-reasoning`, `ralph-wiggum`, `caveman-compress` and
`caveman-review` skill sets, their per-agent packs, the `caveman-universal`
library and the `.skill` single-file engine. They are kept for reference and for
`skillopt-integration/`, which still trains against those documents; they are no
longer published install paths, and nothing new should be written into them.
