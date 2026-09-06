# Agent Interface bootstrap

The sole fixed navigation entry point is `.interface/interface.yaml`. Its address belongs only in shared rules, never in individual Skills or agent instructions. It supplies the current file map and structural metadata, not a role to infer.

## Discovery

- Read the current Interface root at the start of every operation. Use it to locate the resources needed by the role already defined in the active Skill or agent instructions.
- Resolve all other paths, file responsibilities, generated outputs, formats, Policies, authorities, modes, interfaces, and code boundaries through this map and the owning files it identifies. Do not hardcode these paths or copy the current file layout into Skills or agents. The explicit protected-file list is a write restriction, not an additional discovery map.
- There is no runtime Interface Understanding or role-discovery stage. The Interface README is a design-time reference for human-approved maintenance of role instructions, not a prerequisite that operating Skills reread to determine their role.
- Read only the current mapped sources required for the operation, subject to the shared project-source policy. A mapped path or read order does not authorize any role other than Interpreter to read the human project definition. Structural discovery does not grant write access.
- Do not substitute remembered contents for current sources. Renaming or relocating a mapped resource must require only an Interface-root update, never a Skill update.

The self-contained reset operation is the only exception to this bootstrap. It does not interpret, generate, or reconcile Interface content and therefore does not read the Interface root. It may assume only the fixed targets and behavior defined by its own Skill. This exception grants no other capability permission to hardcode an Interface path.

## Separation

- The Interface remains structurally agent-independent when it catalogs an external Agent Skill. It may record a Skill's name, physical path, short purpose, invocation, and Mode binding as integration metadata outside the Interface Structure.
- Skill integration metadata grants no authority and does not define or override the Skill's instructions, shared execution rules, or the owning Interface files.
- Do not copy complete Skill instructions or shared Claude operating rules into the Interface. Discovery and selection of relevant available Skills and plugin capabilities are governed by the shared Claude rules and authorized project context, not fixed technology-to-Skill mappings.
- Claude-specific behavior belongs under the Claude configuration layer. Each Skill defines its fixed role, specialized workflow, and boundaries; shared behavior belongs in Rules. Structural metadata may constrain execution but cannot redefine that role. Report a critical mismatch rather than adopting another role.
- Do not copy current Interface structure, values, fields, defaults, Policies, or project facts into a Skill. Consume them from their live owners discovered through the Interface root.
- Change a Skill only when that Skill's own workflow changes. A change to Interface structure, Schemas, Config, project content, or mapped paths is not a reason to edit a Skill.
