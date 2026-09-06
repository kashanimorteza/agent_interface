# Agent Interface Skill policy

These are shared Claude execution rules for every Agent Interface Skill and supporting agent, including read-only reporting, and must not be copied into individual instructions. The Interface may catalog Skill integration metadata, but that metadata neither defines nor overrides these rules.

## Human-owned files

Agent Interface Skills and supporting agents must never edit or delete these files. They are changed only by a human. Read access is governed separately by the Understanding and source-access policy below:

- `.interface/interface.md`
- `.interface/project.md`
- every file under `.interface/principles/`
- every file under `.interface/preferences/`
- every file under `.interface/schema/`

When an operation determines that one of these files should change, it reports the required change to the human and leaves the file untouched.

## Understanding and source access

- Roles and specialized workflows are defined once in each Skill's or agent's own instructions. Understanding informs execution of that fixed role; it never replaces, infers, or redefines the role.
- Every Agent Interface Skill and supporting agent except the fixed reset operation establishes two distinct Understandings on each run from the current sources located through the shared bootstrap.
- **Agent Interface Understanding** comes from the current Interface root. It explains what Agent Interface is, how its current system is organized, where its resources are, and how the fixed role participates in it. Interface metadata is structural context, not a target-project requirement.
- **Target Project Understanding** comes from the current human project definition. It explains the project being built, its intent, domain, scope, structure, and phases. Every role may read this definition for project context.
- Interpreter alone resolves the human project definition through the applicable Principles, Preferences, and Schemas and produces or refreshes the mapped generated configuration. Existing configuration may be absent or incomplete before generation.
- Every other role uses the human project definition for Understanding and consumes the applicable generated configuration as the authoritative record of resolved project decisions for its operation. It must not independently regenerate that configuration, write a competing interpretation, or silently replace a resolved decision with its own reading of the human definition.
- Consumers may read mapped structural authorities to apply current formats and execution rules. Plans, implementation files, dependency manifests, and verification results remain available as role-specific execution evidence; they do not replace either source of Understanding or generated configuration as the record of resolved decisions.
- If required generated information is missing, inconsistent, stale, or conflicts with the current human definition, do not silently reinterpret or regenerate it outside Interpreter. Report the affected work and the required Interpreter refresh. Continue independently supported work and use the decision policy for ordinary unspecified execution details; not every omission requires a refresh or a question.
- Supporting capabilities inherit the active operation's source restrictions and cannot bypass them.

## Shared Skill workflow

For every Agent Interface Skill except the fixed reset operation:

1. Follow the fixed role already defined in the active instructions.
2. Establish Agent Interface Understanding from the current Interface root and use its map to locate current resources.
3. Establish Target Project Understanding from the current human project definition, then load the generated configuration and other role-specific inputs required for the operation. Only Interpreter generates or refreshes Project Understanding in configuration.
4. Discover relevant available Skills and plugin capabilities using the capability discovery policy below.
5. Execute the specialized `Workflow` in the active Skill, using both Understandings, the fixed role, the current authorities, and relevant capabilities discovered.
6. Validate and report the result as required by the current authorities.

The reset operation skips map discovery and project interpretation and executes only its fixed local Workflow.

## Role and execution authority

- The active Skill or agent defines its operation and boundaries. The live Interface supplies applicable execution constraints and write authority for that operation, not a replacement role. Neither source expands the other's permissions.
- A supporting capability receives no additional Interface write authority merely because it is discovered or invoked.
- The reset operation receives no authority from the Interface root and performs no discovery. Its sole authority is the human's explicit confirmation after the Skill previews one fixed reset stage, and its scope is exactly the fixed workflow defined by that Skill.

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

- After loading the authorized project inputs for the fixed role, inspect the Skills and installed plugin capabilities available in the current Claude environment. Match their declared purpose and compatibility to the actual project technologies, work requirements, and active operation's role; do not rely on names alone.
- Perform this discovery once for the current operation, refreshing it if the work context or available capabilities change. Read the selected Skill's instructions before using it, and use relevant compatible capabilities within the active operation's scope.
- Keep this selection dynamic. Shared rules and Interface-operation Skills must not embed project-specific technology names or fixed technology-to-Skill mappings. A specialized Skill may describe its own technology; its presence does not mean every project uses that technology.
- If no relevant compatible capability is available, continue using authorized project context and professional judgment. The absence of an optional supporting Skill is not itself a blocker. Using available capabilities does not implicitly invoke installation of new plugins or Skills.
- Supporting capabilities do not change the active role, project requirements, resolved choices, or write boundaries. Their guidance cannot authorize implementation during planning, repairs during review, or modifications to protected files.
- Capability discovery and selection rules belong to the Claude layer. The Interface may catalog Skill names, paths, and descriptions as integration metadata without copying these execution instructions.
