---
name: my-interface-reset
description: Preview and, after explicit confirmation, reset generated configuration, tasks, or developed code. Choose 1 for interpreter, 2 for task, or 3 for develop.
argument-hint: "[1=interpreter | 2=task | 3=develop]"
disable-model-invocation: true
---

# Reset the project workflow

## Role

Preview and reset exactly one selected workflow stage using the current Interface authorities. Reset does not interpret project intent, generate configuration, create Tasks, develop, or review.

## Workflow

After establishing both shared Understandings, accept exactly one numeric argument: `1` (interpreter), `2` (task), or `3` (develop). Use the current Interface authorities to resolve the generated outputs, workflow records, ownership boundaries, and implementation directories affected by the selected stage. Do not hardcode or reproduce their current addresses in this Skill.

### 1 = Interpreter reset

Remove all generated configuration contents and developed implementation outputs owned by the current Interface. Preserve their container when required by the current structure. Do not regenerate configuration or create State.

### 2 = Task reset

Clear planned Groups and Tasks while preserving the Task frame and phase Plan shells. Return State to its resolved pre-planning position and clear the active phase. Remove developed implementation outputs. Preserve other generated Understanding and shared records according to current ownership.

### 3 = Develop reset

Return State to its resolved pre-development position and clear the active phase. Return every existing Task to the current initial Task status, remove transient blocking association when required, and preserve its content and history. Remove developed implementation outputs while preserving Plans, Groups, other generated Understanding, and shared records according to current ownership.

Numeric stage arguments do not rename the existing State modes.

### Confirmation

First inspect the resolved targets for the selected stage and show the exact changes without making any mutation. Ask the user for confirmation.

The initial invocation is not approval. Apply the resolved changes only after the user explicitly accepts that preview. Report the result and deleted targets briefly; deletion is permanent for untracked files unless separately backed up. Do not invoke another workflow operation.
