# Commands

Most of what this skill holds is *policy*, applied to whatever you are doing.
{{COMMAND_COUNT}} of the {{SKILL_COUNT}} merged skills are different: they are
**procedures** you run when named, each with its own start and stop. Upstream
marked them `disable-model-invocation`; that policy is kept, so a row here is an
**offer, never an action** — do not run one unless the user named it.

{{COMMANDS_TABLE}}

## Running one

1. Read the reference in its row, then the section the command names.
2. Announce the shape in one line (`grilling: 3 questions, then I stop`) and start.
3. Do not narrate the procedure from inside it, and do not summarise the skill
   instead of running it.
4. Stop at its last step. Chain nothing because the output "obviously" wants a
   follow-up: offer it in a line.

## Setup order

On a fresh repo run `setup-matt-pocock-skills` before `to-spec`, `to-tickets`,
`triage` or `wayfinder`: it configures the issue tracker, the triage labels, and
where `GLOSSARY.md` and the ADRs live. (`setup-repo` is the reference file that
carries it, not a command.)
