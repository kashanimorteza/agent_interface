---
name: my-interface-reset
description: Preview and, after explicit confirmation, reset Interface Config, Tasks, or developed code. Choose 1 for configure, 2 for task, or 3 for develop.
argument-hint: "[1=configure | 2=task | 3=develop]"
disable-model-invocation: true
---

# Reset the project workflow

## Role

Preview and reset exactly one selected workflow stage using the current Interface authorities. Reset does not interpret project intent, generate configuration, create Tasks, develop, or review.

## Workflow

First establish Agent Interface Understanding by reading the canonical Interface document. Use it to locate the current Config records, reset definitions, ownership boundaries, and implementation directories affected by Reset. Target Project Understanding is not required for this mechanical operation.

Accept exactly one numeric argument: `1` (configure), `2` (task), or `3` (develop).

### 1 = Configure reset

Remove the Task and State Config files and developed implementation outputs owned by the current Interface. Preserve their container directory. Do not regenerate Config.

### 2 = Task reset

Clear planned Groups and Tasks according to the current Task structure. Return State to its pre-planning position and clear the active phase. Remove developed implementation outputs. Preserve shared operational records according to current ownership.

### 3 = Develop reset

Return State to its pre-development position and clear the active phase. Return every existing Task to the current initial Task status, remove transient blocking association when required, and preserve its content and history. Remove developed implementation outputs while preserving Plans, Groups, and shared operational records according to current ownership.

Numeric stage arguments do not rename the existing State modes.

### Confirmation

First inspect the resolved targets for the selected stage and show the exact changes without making any mutation. Ask the user for confirmation.

The initial invocation is not approval. Apply the resolved changes only after the user explicitly accepts that preview. Report the result and deleted targets briefly; deletion is permanent for untracked files unless separately backed up. Do not invoke another workflow operation.
