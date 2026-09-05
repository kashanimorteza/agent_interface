# Agent Interface bootstrap

`.interface/interface.yaml` is the only stable Interface path that Claude capabilities may assume.

## Discovery

- Read the Interface root before any other Interface source.
- Resolve every other path, file role, read order, generated output, Schema, Policy, authority, mode, interface, and code boundary through the Interface root and the owning files it identifies.
- Never hardcode, guess, or preserve another Interface path or current file layout in a Rule, Skill, agent, script, or remembered workflow.
- Re-read the current Interface root on every operation. A renamed or relocated referenced file must require only an Interface-root update, never a Skill update.
- Read only the sources required for the active operation and its current authority. Structural discovery does not grant write access.

The self-contained clear and reset operations are the only exceptions to this bootstrap. They do not interpret, generate, or reconcile Interface content and therefore do not read the Interface root. Each may assume only the fixed targets and behavior defined by its own Skill and bundled script. These exceptions grant no other capability permission to hardcode an Interface path.

## Separation

- The Interface remains structurally agent-independent when it catalogs an external Agent Skill. It may record a Skill's name, physical path, short purpose, invocation, and Behaviour binding as integration metadata outside the Interface Structure.
- Skill integration metadata grants no authority and does not define or override the Skill's instructions, shared execution rules, or the owning Interface files.
- Do not copy complete Skill instructions or shared Claude operating rules into the Interface. Technology-to-Skill guidance remains in the Claude Rules unless the Interface explicitly introduces a separate agent-independent capability model.
- Claude-specific behavior belongs under the Claude configuration layer. Skills contain only their specialized workflow; shared behavior belongs in Rules.
- Do not copy current Interface structure, values, fields, defaults, Policies, or project facts into a Skill. Consume them from their live owners discovered through the Interface root.
- Change a Skill only when that Skill's own workflow changes. A change to Interface structure, Schemas, Config, project content, or mapped paths is not a reason to edit a Skill.
