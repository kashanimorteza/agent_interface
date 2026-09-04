---
name: my-interface-tasker
description: Create or reconcile the implementation plan for the one project phase named by the Developer. Plans only; never implements or interprets the human project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Plan one project phase

Create an implementation-ready plan for the project phase named in `$ARGUMENTS`.

## Bootstrap

Read `.interface/root.yaml`. This is the only Interface path this Skill may assume. Follow its current map and read order to discover every source, plan, authority, configuration, contract, Policy, and boundary required for this run.

Re-read required sources on every invocation. Resolve the requested phase and its technical context only through the current mapped files. Apply technology guidance supplied by the project Rules when relevant and available.

Do not rely on remembered paths, fields, task shapes, states, transitions, defaults, permissions, or decision rules. Information in the human project definition provides context but does not override or expand the generated operational sources.

## Plan

Enter, plan, reconcile, validate, and record the requested scope exactly as the current authorities permit. Let the live planning Schema and Policies determine output shape, decomposition, dependencies, acceptance, verification, paths, lifecycle, preservation behavior, and how missing information is handled.

Preserve existing progress, history, protected content, and everything outside current write authority. Apply technology guidance only inside the authorized scope.

Produce the smallest complete implementation-ready plan that satisfies the current project configuration. Do not invent or expand project requirements, contracts, permissions, or scope.

## Boundaries

Plan only. Do not implement, execute, test product code, review completed work, reinterpret inputs, or modify source files merely to make planning possible.

Report the handled scope, written or preserved plan content, validation result, and only the questions or blockers required by the live policies.
