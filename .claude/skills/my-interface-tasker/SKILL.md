---
name: my-interface-tasker
description: Create or reconcile the implementation plan for the one project phase named by the Developer. Plans only; never implements or interprets the human project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Plan one project phase

Create an implementation-ready plan for the project phase named in `$ARGUMENTS`.

## Workflow

Enter the workflow state required for this operation. Create or reconcile the smallest complete implementation-ready plan for the requested scope, validate it, and record the result. Use the current planning sources to determine its decomposition, dependencies, acceptance, verification, and preservation behavior.

## Boundaries

Plan only. Do not implement, execute, test product code, review completed work, reinterpret inputs, or modify source files merely to make planning possible.

Report the handled scope, written or preserved plan content, validation result, and only the questions or blockers required by the live policies.
