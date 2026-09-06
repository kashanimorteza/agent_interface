# Agent Interface bootstrap

Agent Interface Skills and the Interface structure are independent. Changing either one must not require changing the other.

## Understanding

Every Skill establishes both Understandings before executing its fixed role:

- **Agent Interface Understanding** comes from `.interface/interface.md`. It explains Agent Interface, its organization, resources, relationships, and operating path.
- **Target Project Understanding** comes from `.interface/project.md`. It explains the project being built, including its purpose, domain, scope, structure, Models, Behaviours, and phases.

Use Agent Interface Understanding to discover all other resources needed by the active role. Do not repeat the definitions of either Understanding elsewhere; referring to the applicable Understanding is sufficient.

## Separation

- Do not hardcode or copy Interface paths, structure, values, fields, defaults, Policies, or project facts into a Skill. Read them from their current owners through the shared Understandings.
- Each Skill contains only its own fixed role, specialized Workflow, and boundaries. Understanding informs execution but never defines or changes the role.
- The Interface may catalog Skill metadata, including a Skill's name, path, invocation, and short purpose.
- Change a Skill only when its own role or Workflow changes. A change to the Interface structure or target project must not require a Skill change.
