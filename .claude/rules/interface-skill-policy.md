# Agent Interface Skill policy

These are shared Claude execution rules for every Agent Interface Skill and must not be copied into individual Skills. The Interface may catalog Skill integration metadata, but that metadata neither defines nor overrides these rules.

## Human-owned files

Agent Interface Skills may read these files, but must never edit or delete them. They are changed only by a human:

- `.interface/interface.yaml`
- `.interface/project.md`
- `.interface/readme.md`
- every file under `.interface/principles/`
- every file under `.interface/preferences/`
- every file under `.interface/schema/`

When an operation determines that one of these files should change, it reports the required change to the human and leaves the file untouched.

## Understanding

- Keep **Interface Understanding** and **Project Understanding** distinct.
- Interface Understanding explains what Agent Project Interface is, how its Structure and Behaviours work, and how the active Skill relates to them. Build it from the current Interface root and the referenced Interface README.
- Project Understanding explains the particular project being built. Build it from the referenced human project definition and the current referenced generated configuration required by the active Skill.
- The human project definition is the source of project intent. Generated configuration is its structured operational Understanding; it may be absent or incomplete before generation and may be reconciled by the authorized generation operation.
- Never treat Interface documentation as project requirements or project content as a definition of the Interface itself.

## Shared Skill workflow

For every Agent Interface Skill except the fixed reset operation:

1. Build current Interface Understanding and locate the active Skill's role in it.
2. Build the Project Understanding required for that role.
3. Execute the specialized `Workflow` in the active Skill.
4. Validate and report the result as required by the current authorities.

The reset operation skips both forms of Understanding and executes only its fixed local Workflow.

## Operation bindings

- `my-interface-interpreter` performs the generic generation operation.
- `my-interface-tasker` performs the generic planning operation.
- `my-interface-developer` performs the generic development operation.
- `my-interface-reviewer` performs the generic review operation.
- `my-interface-reset` performs the generic reset operation.
- `my-interface-skill-installer` is a supporting Claude operation and receives no Interface write authority.
- Except for the self-contained reset operation, a binding grants only the authority that the live Interface assigns to its generic operation. It never expands permissions, scope, interfaces, or modes.
- The reset operation receives no authority from the Interface root and performs no discovery. Its sole authority is the human's explicit confirmation after the Skill previews one fixed reset stage, and its scope is exactly the fixed workflow implemented by that Skill and its bundled script.

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
