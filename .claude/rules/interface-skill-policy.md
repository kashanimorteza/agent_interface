# Agent Interface Skill policy

These shared rules apply to every Agent Interface Skill and supporting agent. Do not copy them into individual Skill instructions.

## Human-owned files

Skills and supporting agents must never edit or delete:

- `.interface/interface.md`
- `.interface/project.md`
- files under `.interface/principles/`
- files under `.interface/preferences/`
- files under `.interface/schema/`

Only a human edits these sources. When a change appears necessary, report it and leave the source unchanged.

## Shared Workflow

Every Skill:

1. Establishes Agent Interface Understanding.
2. Establishes Target Project Understanding.
3. Applies its fixed role and specialized Workflow using the current resources discovered through those Understandings.
4. Validates and reports its result according to its current authority.

## Decision policy

- Explicit project decisions, Interfaces, permissions, and write boundaries are binding.
- When a necessary detail is not defined, choose the best compatible approach using the two Understandings, current evidence, and professional judgment, then continue without asking.
- Ask or stop only when no safe choice can be made without materially affecting project intent, core architecture, security, data integrity, permissions, an Interface, or an irreversible action.
- Discretion never expands the active role, requested scope, or write authority.

## Development authority

Development may install and configure the runtimes, package managers, build tools, system software, and dependencies required to complete its authorized work. A missing prerequisite is work to perform, not a Blocker unless installation or configuration actually fails.
