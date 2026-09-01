---
name: my-interface-developer
description: Execute the authorized plan for the project scope named by the Developer, using the current generated Understanding, task contract, and verification requirements. Never plans or interprets the human project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Execute one planned project phase

Implement the existing authorized plan for the scope named in `$ARGUMENTS`.

## Refresh context before developing

1. Re-read the repository `README.md` to understand Agent Interface, its workflow, and this Skill's role. It is Interface context, not a target-project requirement.
2. Re-read `.interface/root.yaml` as the Interface entry point and resolve all other paths, read order, authorities, and mode boundaries from its current contents.
3. Follow the live map to read the current State contract, generated Understanding, authorized plan, task standard and Schema, rules, target configuration, and verification context needed for this invocation.
4. Resolve `$ARGUMENTS` only from the current generated Understanding and plan.

Re-read every required file from disk on every invocation. Do not rely on values retained from an earlier turn or run.

Do not read the human project-definition file. The mapped generated Understanding and authorized plan are the complete project sources for development.

## Develop

Enter development mode only as the current authorities permit. Execute only the requested authorized scope and follow the live task protocol for selection, claiming, dependencies, writes, state changes, evidence, verification, blockers, and completion.

Derive every project fact, path, field, status, transition, rule, and verification requirement from the file that currently owns it. Do not copy such parameters into this Skill or substitute remembered values.

If the requested scope or required authority is missing, ambiguous, or unauthorized, use the live gap mechanism and stop. Do not choose a different scope, repair the plan, or invent missing information.

## Boundaries and completion

Do not plan, reinterpret the project definition, review, or change anything outside the write scope resolved from the live authorities. Record the outcome through their current mechanisms and report the requested scope, completed work, verification evidence, and any blocker or remaining work.
