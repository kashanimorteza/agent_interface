# Project root: `.interface/`

The authoritative project root for this repository is the `.interface/` directory. It is the Agent Project Interface — the single source of truth for what the project is, how it is configured, and where work stands.

## Rule

- Whenever Claude Code — or any Skill, agent, or capability it runs — needs to inspect, understand, analyze, or modify the project, treat `.interface/` as the primary project root and source of truth. Start at `.interface/root.yaml`, the interface's entry point.
- This rule applies automatically. Skills and other capabilities must not redefine or re-resolve the target project directory individually; they inherit `.interface/` as the project root from this rule.
- Do not unnecessarily search, inspect, or operate in directories outside `.interface/` when performing project-related work. Go outside it only when the task explicitly requires it (for example, code under an item's declared `code_path`, or the Claude Code configuration in `.claude/`).

## Scope and boundaries

- This rule belongs exclusively to the Claude Code configuration layer (`.claude/`). It is not part of the Agent Interface itself and must never be moved into, duplicated in, or treated as one of the project's own rules, schemas, or configuration (`.interface/root.yaml`, `.interface/schema/`, `.interface/config/rules.yaml`, etc.).
- This rule changes nothing about the interface's own write policies and mode permissions; those remain governed entirely by `.interface/root.yaml`, the schemas, and the State contract.
