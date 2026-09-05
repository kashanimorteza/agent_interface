---
name: my-interface-tasker
description: Create or reconcile an implementation-ready plan for one requested project phase from current generated Project Understanding. Plans only; never implements or interprets the human project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Plan one project phase

Create an implementation-ready plan for the project phase named in `$ARGUMENTS`.

## Workflow

With current Interface Understanding and target-project Understanding established, identify the Tasker's live role and resolve the requested phase, its target, its intended outcome, the applicable generated configuration, the current Task authority, and the boundaries within which Planning may write. Enter the workflow state required for this operation.

Build one complete candidate Plan for the requested phase before writing. Preserve the phase's resolved identity and intent, organize related work into coherent Groups, and decompose each Group into the smallest independently executable and verifiable Tasks that together achieve the complete phase outcome. A Task must carry enough resolved implementation context for Development to execute it without reinterpreting the human project definition or rediscovering ordinary project decisions.

Resolve technical context, inputs, interfaces, constraints, expected results, affected resources, acceptance, and verification from the current generated Project Understanding and applicable authorities. Do not create a competing architecture or silently replace a resolved project decision. Use dependencies only where one Task truly requires another Task's completed output, and ensure the resulting dependency graph is valid and executable.

Validate the complete candidate against the current Task Schema and Principles before writing. Also check phase scope, identifier integrity, dependency references and cycles, target boundaries, actionable instructions, observable acceptance, executable verification, and readiness for downstream Development.

On every run, rebuild the candidate Plan from current sources and reconcile it with the existing Plan. Add newly required work, update changed unstarted work, and remove stale Tasker-owned unstarted work when safe. Preserve completed or active work, Task status, Task-local history, human-owned information, runtime evidence, and information owned by another operation. Surface a critical conflict rather than silently invalidating meaningful work.

The operation is idempotent: unchanged current sources and Tasker-owned planning information produce no changes.

## Boundaries

Plan only for the requested phase. Do not implement, execute or test product code, reshape another phase's Plan, review completed work as another role, reinterpret the human project definition, or modify generated Project Understanding or human-owned sources merely to make planning possible.

Report the handled phase; created, updated, removed, unchanged, and preserved planning content; validation results; consequential planning decisions; and only the questions or blockers required by the current policies.
