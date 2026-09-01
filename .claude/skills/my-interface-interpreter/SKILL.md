---
name: my-interface-interpreter
description: Interpret `.interface/project.md` into the generated Understanding under `.interface/config/` using the Interface map and Schemas. Use when the Developer explicitly asks to generate, refresh, or reconcile Config after the target project definition changes.
disable-model-invocation: true
---

# Interpret the target project

Transform the Developer's natural-language target-project definition into the structured configuration consumed by the other Agent Interface Skills.

## Read before interpreting

1. Read `README.md` to understand Agent Interface, its workflow, and the Interpreter's role. README content is system context only; never treat it as a target-project fact.
2. Read `.interface/root.yaml` as the Interface entry point. Follow its mappings, read order, mode boundaries, and authority references rather than relying on paths or permissions remembered by this Skill.
3. Read `.interface/project.md` completely. The Interpreter is the only workflow Skill that reads it, and it must read it because it is the human-managed source for the target project.
4. Read the Schemas required by the Interface map before generating their corresponding Config files.
5. Read existing Config and the live State contract before writing so protected state and human-owned values are preserved exactly as their current authorities require.

## Sources of truth

- Target-project facts come only from `.interface/project.md`.
- Output structure, defaults, relationships, and validation requirements come only from the mapped Schemas.
- Write permissions, state transitions, carry-through rules, and human-only decisions come only from the current Interface map, file policies, and live State contract.
- Other generated Config may be used for consistency, but it never overrides the human's current project definition or the Schemas that shape it.

Do not reproduce configuration keys, Schema fields, transition identifiers, defaults, or mode permissions inside this Skill. Read them fresh from the files that own them.

## Generate the Understanding

Represent all project information supported by the current project definition and required by the current Schemas. Preserve the project's stated meaning without copying its prose mechanically and without inventing missing decisions.

Ensure the generated Understanding represents every project phase the Developer defined, including the information the applicable Schema requires to identify, order, target, and explain each phase. Later Skills must be able to resolve a requested phase entirely from Config without reading `project.md`.

When required information is absent or ambiguous, use the live Config's question and blocker mechanisms. Apply a Schema default only when the Schema actually defines one.

Generate or update only the files and fields authorized for this Interpreter run. Preserve protected runtime state and human-owned content according to their live policies. If current authorities conflict and their configured precedence does not resolve the conflict, stop and ask the Developer.

## Boundaries

This Skill creates Understanding, not plans or product code. Do not create tasks, execute tasks, implement, test, refactor, or modify the target project's source code.

Do not modify `README.md`, `.interface/root.yaml`, `.interface/project.md`, or the Schemas. A needed change to an input or authority is reported through the configured mechanism rather than applied here.

## Completion

Validate the generated files against their current Schemas and report which Config files changed, which gaps were recorded, and anything that prevented a complete interpretation.
