# Agent Interface Skill policy

These are Claude-specific integration rules. They apply to every Agent Interface Skill and must not be duplicated inside the Interface.

## Operation bindings

- `my-interface-interpreter` performs the generic generation operation.
- `my-interface-tasker` performs the generic planning operation.
- `my-interface-developer` performs the generic development operation.
- `my-interface-reviewer` performs the generic review operation.
- `my-interface-clear` performs the generic clear operation.
- `my-interface-reset` performs the generic reset operation.
- `my-interface-skill-installer` is a supporting Claude operation and receives no Interface write authority.
- Except for the self-contained clear operation, a binding grants only the authority that the live Interface assigns to its generic operation. It never expands permissions, scope, interfaces, or modes.
- The clear operation receives no authority from the Interface, its map, or its State. Its sole authority is the human's explicit confirmation after the Skill previews its fixed deletion targets, and its scope is exactly the fixed workflow implemented by that Skill and its bundled script.

## Decision policy

- Every explicit project value, generated interface, Policy, authority, permission, and write boundary is binding and is never silently overridden.
- When an implementation or technical detail is not specified by an owning file, use available context, supported Preferences, current evidence, and professional judgment to choose a reasonable compatible option and continue without asking the human.
- Raise a question or blocker only when the missing or conflicting decision is critical: a reasonable choice could materially change project goals or scope, domain meaning, core architecture, security, data integrity, permissions, an interface, or an irreversible or destructive outcome; or no safe authorized path can continue.
- Agent discretion fills execution details inside authorized scope. It never invents project goals, product requirements, permissions, phases, interfaces, or write authority, and it never widens the requested work.
- Record a consequential agent-selected assumption or technical decision in the nearest owning generated configuration, Task, log, or final report when that format supports it. Ordinary incidental choices need no question.

## Technology guidance

- When the resolved technology is FastAPI, planning and development use the `fastapi` Skill as technical guidance when it is available.
- Technology guidance cannot change project requirements, phase scope, Interface Policy, interfaces, write boundaries, workflow operations, or State authority.
- Technology-to-Skill mappings exist only in Claude Rules. Never write a Skill name or Skill field into Interface Schema or Config.
