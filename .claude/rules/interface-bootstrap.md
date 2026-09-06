# Agent Interface bootstrap

The sole fixed navigation entry point is `.interface/interface.md`. Its address belongs only in shared rules, never in individual Skills or agent instructions. It supplies the current Agent Interface definition, complete file map, structural context, and the source from which an operation establishes Agent Interface Understanding. The active Skill or agent instructions still define the operation's fixed role.

## Discovery

- Read the current Interface root at the start of every operation. Establish a current Understanding of Agent Interface—its purpose, organization, resources, relationships, and operating path—and use that Understanding to perform the role already defined in the active Skill or agent instructions.
- Resolve all other paths, file responsibilities, generated outputs, formats, Policies, authorities, modes, interfaces, and code boundaries through this map and the owning files it identifies. Do not hardcode these paths or copy the current file layout into Skills or agents. The explicit protected-file list is a write restriction, not an additional discovery map.
- Agent Interface Understanding informs how the fixed role participates in the current system; it never replaces, infers, or redefines that role.
- Use the map to locate the human project definition and all other sources required by the shared Understanding policy and the active role. Read access does not grant write access.
- Do not substitute remembered contents for current sources. Renaming or relocating a mapped resource must require only an Interface-root update, never a Skill update.

The self-contained reset operation is the only exception to this bootstrap. It does not interpret, generate, or reconcile Interface content and therefore does not read the Interface root. It may assume only the fixed targets and behavior defined by its own Skill. This exception grants no other capability permission to hardcode an Interface path.

## Separation

- The Interface remains structurally agent-independent when it catalogs an external Agent Skill. It may record a Skill's name, physical path, short purpose, invocation, and Mode binding as integration metadata outside the Interface Structure.
- Skill integration metadata grants no authority and does not define or override the Skill's instructions, shared execution rules, or the owning Interface files.
- Do not copy complete Skill instructions or shared Claude operating rules into the Interface. Discovery and selection of relevant available Skills and plugin capabilities are governed by the shared Claude rules and authorized project context, not fixed technology-to-Skill mappings.
- Claude-specific behavior belongs under the Claude configuration layer. Each Skill defines its fixed role, specialized workflow, and boundaries; shared behavior belongs in Rules. Structural metadata may constrain execution but cannot redefine that role. Report a critical mismatch rather than adopting another role.
- Do not copy current Interface structure, values, fields, defaults, Policies, or project facts into a Skill. Consume them from their live owners discovered through the Interface root.
- Change a Skill only when that Skill's own workflow changes. A change to Interface structure, Schemas, Config, project content, or mapped paths is not a reason to edit a Skill.
