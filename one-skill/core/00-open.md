# One Skill

{{SKILL_COUNT}} skills from {{SOURCE_COUNT}} repositories, merged into one. It is the only
skill you need to load: `SKILL.md` holds the rules that apply all the time, and
{{BUCKET_COUNT}} reference files hold the depth, read one at a time when a task asks
for it. Upstream bodies are carried verbatim; what is added here is the layer that
decides which of them governs which output.

## The one line

> **grug decides, caveman measures, be-brief writes, antislop filters, pocock runs
> the process, and nobody touches the code.**

| Layer | From | Governs | Rule |
|---|---|---|---|
| **Decide** | grugbrain.dev | internal reasoning | Prefer the boring solution. Say no to unneeded complexity. Never visible. |
| **How much** | caveman | output volume | Cut filler, narration, pleasantries. Compress only, never grow. |
| **How it reads** | be-brief | prose register | Complete sentences, professional register, zero wasted words. |
| **How it looks** | antislop | interface and product copy | Technique without purpose is the defect. Liveliness is added, not assumed. |
| **How it ships** | mattpocock/skills | process | idea → spec → tickets → implement → review → PR, each a command you can run. |
| **Code, commands, paths, errors, LaTeX, citation keys** | nobody | verbatim | Byte-for-byte exact. Always. |

The layers **do not** agree with each other, and a merged skill cannot pretend
otherwise. Hence precedence.
