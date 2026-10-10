# one-skill — the merge, and how to grow it

One skill, built from sixty-nine others across eight sources. Nothing in
`dist/skill/` is hand-written, so nothing in it has to be kept in sync by hand —
including the three fragment fallbacks under `dist/families/`.

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
│   ├── local/                this repository, read from the working tree (`legacy/`)
│   ├── anti-slop/                miqdadbadjuber/anti-slop — the origin, not the fork
│   ├── mattpocock-skills/        mattpocock/skills, engineering + productivity + misc
│   ├── caveman/                  JuliusBrussee/caveman at v3.2.0, SKILL.md only
│   ├── grug/                     bigskysoftware/grugbrain.dev, `index.md`
│   ├── strix/ mem0/ archify/     usestrix/strix, mem0ai/mem0, tt-a1i/archify
├── dist/skill/         scratch build output (gitignored `dist/`; not a deliverable)
├── dist/families/      the three fragments, generated from the same manifest
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
python one-skill/build.py install   # mirror dist into every install path + rebuild every zip
                                    # (the three fragments included)
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

**0.** Decide what is *implementable from a markdown file*. This is the filter that
decided four fifths of Strix, five sixths of mem0 and all of Archify's renderer: a skill
whose instructions are "run this binary", "fetch these docs" or "install this package"
cannot be obeyed here, and carrying it anyway does not add capability, it adds
hallucinated capability. Write the answer down per skill as `not_merged` — the build now
fails if a vendored `SKILL.md` is neither routed nor excused, so a cast-aside list
cannot rot when upstream grows.

**1.** Declare it in `sources.json` → `sources`. Vendored from the **origin at its
latest commit**, never from a personal fork — if a fork exists, clone both and
`diff -rq`; when they are identical, say so in `origin.note` and point at the origin:

```jsonc
{
  "slug": "my-new-source",
  "title": "owner/my-new-source — short description",
  "license": "MIT",
  "attribution": "owner/my-new-source",
  "origin": { "repo": "owner/my-new-source", "ref": "HEAD", "license": "MIT", "note": "" },
  "sync": {
    "include": [
      { "from": "skills", "to": "upstream/my-new-source",
        "skip": ["README.md", "agents"], "only": ["SKILL.md"] }
    ]
  },
  "skills": [],
  "not_routed": [], "not_merged": [], "not_vendored": []
}
```

`ref` may pin a tag or SHA; `HEAD` follows the default branch. `skip` drops per-agent
duplicates and non-instruction files at vendoring time; `only` narrows a whole
directory down to one file type, which is how a repo whose skills each carry an SDK
manual contributes only its instructions. `origin.kind: "local"` reads this
repository's working tree instead of cloning — needed for `legacy/`, which exists only
on the merged branch.

`discover` is a list of upstream directories to account for: at sync time every
`SKILL.md` beneath them is recorded in `PROVENANCE.json` as `discovered_upstream`, and
the build then requires each of those names to be routed or excused. Without it the
gate only sees what was already copied down, and a source that vendors one flat file
per skill (anti-slop, this repo's `legacy/`) would pass it by construction.

A missing path in `sync.include` is a hard stop, never a delete. An earlier version of
`sync` wiped a vendored tree because one path had moved upstream; if the source is not
there the builder now refuses to touch what it already has.

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
  "scripts": ["upstream/my-new-source/new-skill/check.py"],
  "strip_sections": ["Run it"], "strip_reason": "the command is not here; the judgement is",
  "keep_sections": ["Integration principles (non-negotiable)"],
  "markup": ["strip-html-lines", "unwrap-heading-anchors"],
  "replace": [{ "from": "run `node bin/tool`", "to": "this bundle ships no such command",
                "reason": "names a CLI the merged skill does not carry" }],
  "note": "one paragraph on what the merge took and why, shown above the section"
}
```

`keep_sections` is the inverse of `strip_sections`: for a skill that is mostly a tool
driver, keep the sections that survive on their own and drop the rest **by name**. The
alternative — rewriting a CLI walkthrough into tool-free prose — produces text whose
author is the build script.

`entry` is the body to carry. `markup` removes page furniture from a source that is
really a generated web page (the grug site wraps its headings in anchors); it may not
change a word. `docs` are sibling files that ride in the same
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
* **Every vendored file and skill is accounted for.** A file in `upstream/` that no
  skill routes and no source lists under `not_routed` fails the build; a `SKILL.md`
  that is neither routed nor listed under its source's `not_merged` fails it too, and so
  does an excuse with no reason. Three gates, one rule: skipping is a decision, so make
  it in writing.
* **A declared edit must land.** `strip_sections`, `keep_sections` and `replace` all
  fail the build when their target moves upstream. A `replace` that matches nothing is
  worse than no `replace` at all: `SOURCES.md` would advertise an edit that never
  happened while the misleading sentence stayed in the skill.
* **Add a bucket only for a new destination, and only for a big one.** Eleven buckets
  for eight sources is already the point where a router has to be a table rather than a
  list. Archify's diagram method first got its own bucket and the cut removed it: 410
  words of reference material did not pay for a router row and a file, so it sits in
  `ui-craft` beside the filter that asks it the same question.
* **Fragments are a projection, not a copy.** A family is a list of buckets in the
  manifest; `build.py` assembles each one with the same functions and the same verbatim
  rules. Never hand-edit `dist/families/` or `claude-skills/fragments/`: `check`
  compares them against a rebuild exactly like the main mirrors, and a stale fallback is
  worse than no fallback.

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
