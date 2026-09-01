---
name: my-interface-tasker
description: Create or update the authorized implementation plan for the project scope named by the Developer, using the current generated Understanding and task standard. Plans only; never implements or interprets the human project definition.
argument-hint: "[phase-id ...]"
disable-model-invocation: true
---

# Plan from the generated configuration

Turn the current generated Understanding into an authorized implementation-ready plan.

## Refresh context before planning

1. Re-read the repository `README.md` to understand Agent Interface, its workflow, and this Skill's role.
2. Re-read `.interface/root.yaml` as the Interface entry point and resolve all other paths, read order, authorities, and mode boundaries from its current contents.
3. Follow the live map to read the current State contract, generated Understanding, task standard and Schema, rules, target configuration, and every other mapped file required for this invocation.
4. Resolve `$ARGUMENTS` only from the current generated Understanding.

Re-read every required file from disk on every invocation. Do not rely on values retained from an earlier turn or run.

Do not read the human project-definition file. Interpreting it belongs exclusively to the Interpreter; planning consumes only the current generated Understanding.

## Plan

Enter planning mode only as the current authorities permit. Plan exactly the requested authorized scope, in the order and structure defined by the current Understanding and task standard.

Derive every project fact, grouping, task field, status, lifecycle, transition, dependency, contract, path, verification rule, and write permission from the current file that owns it. Do not copy these parameters into this Skill or substitute remembered values.

If the requested scope or required information is missing, ambiguous, inconsistent, or unauthorized, use the live gap mechanism and stop. Do not select, reshape, or invent project scope or requirements.

Generate only the plan content authorized by the current files and validate it against the current task standard and Schema.

## Boundaries and completion

Do not implement, execute, test, review, reinterpret the project definition, or modify inputs merely to make planning possible. Record the outcome through the current State mechanism and report the handled scope, written plan content, and any blocker, open question, missing authority, or missing configuration.
