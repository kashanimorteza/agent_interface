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

The following project-relative paths are fixed Understanding sources and may be used as navigation constants in shared rules and Skills:

- Interface root: `.interface/interface.yaml` — the current map of files, roles, and paths.
- Interface README: `.interface/readme.md` — the explanation of Agent Interface.
- Human project definition: `.interface/project.md` — the description and intent of the target project.

Stable paths do not imply stable contents. Read the current sources on each operation as required by its role, starting with the Interface root. Discover all other required sources and generated configuration through that map; do not copy their contents into Skill instructions. The fixed reset operation retains its explicit bootstrap exception.

- Keep **Interface Understanding** and **Project Understanding** distinct.
- Interface Understanding explains what Agent Project Interface is, how it works, and how the active Skill relates to it. Build it from the current Interface root and Interface README defined above.
- Project Understanding explains the particular project being built. Build it from the human project definition above and the current generated configuration discovered through the Interface root and required by the active Skill.
- The human project definition is the source of project intent. Generated configuration is its structured operational Understanding; it may be absent or incomplete before generation and may be reconciled by the authorized generation operation.
- Never treat Interface documentation as project requirements or project content as a definition of the Interface itself.

## Shared Skill workflow

For every Agent Interface Skill except the fixed reset operation:

1. Build current Interface Understanding and locate the active Skill's role in it.
2. Build the Project Understanding required for that role.
3. Discover relevant available Skills and plugin capabilities using the capability discovery policy below.
4. Execute the specialized `Workflow` in the active Skill, using the relevant capabilities discovered.
5. Validate and report the result as required by the current authorities.

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

## Development toolchain setup

- Development may install the runtimes, package managers, build tools, and system dependencies required to execute the requested project's planned work, including system-level installation when needed. Preparing these prerequisites is part of Development's execution scope.
- The human's request to develop the project authorizes installation of its required prerequisites; do not ask for a separate project-level confirmation for that installation. Use the resolved technology versions and an installation method compatible with the existing environment. Preserve unrelated installations and projects.
- Planning includes prerequisite installation and verification as actionable work when needed. It must not invent a blanket prohibition on installing system software or assign installation exclusively to the human unless an explicit applicable restriction requires it.
- A missing tool alone is work to perform, not a reason to stop. Record a blocker only when an actual installation obstacle prevents progress or the required tool cannot be obtained. Verify tool availability in the actual execution environment before declaring setup complete.

## Capability discovery and use

- After building both forms of Understanding, inspect the Skills and installed plugin capabilities available in the current Claude environment. Match their declared purpose and compatibility to the actual project technologies, work requirements, and active operation's role; do not rely on names alone.
- Perform this discovery once for the current operation, refreshing it if the work context or available capabilities change. Read the selected Skill's instructions before using it, and use relevant compatible capabilities within the active operation's scope.
- Keep this selection dynamic. Shared rules and Interface-operation Skills must not embed project-specific technology names or fixed technology-to-Skill mappings. A specialized Skill may describe its own technology; its presence does not mean every project uses that technology.
- If no relevant compatible capability is available, continue using current Understanding and professional judgment. The absence of an optional supporting Skill is not itself a blocker. Using available capabilities does not implicitly invoke installation of new plugins or Skills.
- Supporting capabilities do not change the active role, project requirements, resolved choices, or write boundaries. Their guidance cannot authorize implementation during planning, repairs during review, or modifications to protected files.
- Capability discovery and selection rules belong to the Claude layer. The Interface may catalog Skill names, paths, and descriptions as integration metadata without copying these execution instructions.
