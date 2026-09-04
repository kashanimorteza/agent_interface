# Agent Interface bootstrap

`.interface/map.yaml` is the only stable Interface path that Claude capabilities may assume.

## Discovery

- Read the map file before any other Interface source.
- Resolve every other path, file role, read order, generated output, Schema, Policy, authority, mode, contract, and code boundary through the map file and the owning files it identifies.
- Never hardcode, guess, or preserve another Interface path or current file layout in a Rule, Skill, agent, script, or remembered workflow.
- Re-read the current map on every operation. A renamed or relocated mapped file must require only a map update, never a Skill update.
- Read only the sources required for the active operation and its current authority. Structural discovery does not grant write access.

## Separation

- The Interface is agent-independent. Never place Claude configuration, Skill names, Skill paths, invocation syntax, technology-to-Skill mappings, or Claude-specific operating rules inside it.
- Claude-specific behavior belongs under the Claude configuration layer. Skills contain only their specialized workflow; shared behavior belongs in Rules.
- Do not copy current Interface structure, values, fields, defaults, Policies, or project facts into a Skill. Consume them from their live owners discovered through the Interface map.
- Change a Skill only when that Skill's own workflow changes. A change to Interface structure, Schemas, Config, project content, or mapped paths is not a reason to edit a Skill.
