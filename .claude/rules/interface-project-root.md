# Project root: `.interface/`

The authoritative project root for this repository is the `.interface/` directory. It is the Agent Project Interface — the single source of truth for what the project is, how it is configured, and where work stands.

## Rule

- At the start of project work, read the repository `README.md` completely for context about Agent Interface, its workflow, and the current capability's role. The README explains the Interface; it is not a source of target-project facts.
- Inspect the repository root and the top-level structure of `.interface/` only far enough to understand how the Interface, its generated configuration, and any mapped target-project locations relate. This structural inspection does not authorize reading the contents of a protected or role-specific source.
- Then treat `.interface/` as the primary project root and source of truth. Start Interface inspection at `.interface/root.yaml`, use its current map to resolve all other paths, and read only the mapped Config and authority files required for the current task.
- This rule applies automatically. Skills and other capabilities must not redefine or re-resolve the target project directory individually; they inherit `.interface/` as the project root from this rule.
- Do not unnecessarily search, inspect, or operate in directories outside `.interface/` when performing project-related work. Go outside it only when the task explicitly requires it (for example, code under an item's declared `code_path`, or the Claude Code configuration in `.claude/`).

## Scope and boundaries

- This rule belongs exclusively to the Claude Code configuration layer (`.claude/`). It is not part of the Agent Interface itself and must never be moved into, duplicated in, or treated as one of the project's own authorities, item Policies, Schemas, or generated configuration (`.interface/root.yaml`, `.interface/schema/`, `.interface/config/`, etc.).
- This rule establishes discovery order and permits every Agent Interface Skill to read `project.md` for current project context. Only `my-interface-interpreter` may interpret it into generated Understanding. Access to generated Config, target-project code, and every other mapped source remains limited by the active Skill or capability.
- This rule changes nothing about the interface's own write policies and mode permissions; those remain governed entirely by `.interface/root.yaml`, the schemas, and the State contract.
