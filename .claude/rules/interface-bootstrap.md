# Agent Interface bootstrap

Claude capabilities may assume the three fixed Understanding source paths defined in the shared Skill policy: the Interface root, the Interface README, and the human project definition. Their paths are stable; their contents must be read afresh.

## Discovery

- Read the Interface root before any other Interface source.
- Resolve paths other than the three fixed Understanding sources, along with file roles, read orders, generated outputs, Schemas, Policies, authorities, modes, interfaces, and code boundaries, through the current Interface root and the owning files it identifies.
- The three source paths are the only navigation constants permitted in Rules, Skills, agents, or remembered workflows. Do not hardcode other discovery paths or copy the current file layout. The explicit protected-file list is a write restriction, not an additional discovery map.
- Re-read the current Interface root and the other Understanding sources required for the active role on every operation. Do not substitute remembered contents for current files. Renaming or relocating another referenced file must require only an Interface-root update, never a Skill update.
- Read only the sources required for the active operation and its current authority. Structural discovery does not grant write access.

The self-contained reset operation is the only exception to this bootstrap. It does not interpret, generate, or reconcile Interface content and therefore does not read the Interface root. It may assume only the fixed targets and behavior defined by its own Skill and bundled script. This exception grants no other capability permission to hardcode an Interface path.

## Separation

- The Interface remains structurally agent-independent when it catalogs an external Agent Skill. It may record a Skill's name, physical path, short purpose, invocation, and Mode binding as integration metadata outside the Interface Structure.
- Skill integration metadata grants no authority and does not define or override the Skill's instructions, shared execution rules, or the owning Interface files.
- Do not copy complete Skill instructions or shared Claude operating rules into the Interface. Discovery and selection of relevant available Skills and plugin capabilities are governed by the shared Claude rules and current Understanding, not fixed technology-to-Skill mappings.
- Claude-specific behavior belongs under the Claude configuration layer. Skills contain only their specialized workflow; shared behavior belongs in Rules.
- Do not copy current Interface structure, values, fields, defaults, Policies, or project facts into a Skill. Consume them from their live owners discovered through the Interface root.
- Change a Skill only when that Skill's own workflow changes. A change to Interface structure, Schemas, Config, project content, or mapped paths is not a reason to edit a Skill.
