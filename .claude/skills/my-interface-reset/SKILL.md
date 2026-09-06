---
name: my-interface-reset
description: Preview and, after explicit confirmation, reset generated configuration, tasks, or developed code. Choose 1 for interpreter, 2 for task, or 3 for develop.
argument-hint: "[1=interpreter | 2=task | 3=develop]"
disable-model-invocation: true
---

# Reset the project workflow

## Workflow

Perform the fixed reset directly from the project root for exactly one numeric argument: `1` (interpreter), `2` (task), or `3` (develop).

Do not read the Interface root, project definition, Schema, Principles, Preferences, or unrelated configuration. The operation uses only these fixed targets:

- `.interface/config/` (all entries for `1`; only `task.yaml` and `state.yaml` for `2` and `3`)
- Root `model/`, `models/`, `backend/`, `frontend/`, `database/`, and `developer/` directories in all three stages

### 1 = Interpreter reset

Delete every entry inside the fixed config directory, preserving the directory itself, and delete the fixed root output directories when present. This stage works even when config files are missing or malformed. It does not regenerate configuration or create State.

### 2 = Task reset

Clear all Groups and Tasks while preserving the Task frame and phase Plan shells. Set active State to `not set` with a null phase and reset provenance. Delete the fixed root output directories when present. Preserve other configuration, shared blockers, and open questions.

### 3 = Develop reset

Set active State to `planning` with a null phase and reset provenance. Return every existing Task to `todo`, remove its blocker field, and preserve its content and log. Delete the fixed root output directories when present. Preserve Plans, Groups, other configuration, shared blockers, and open questions.

Numeric stage arguments do not rename the existing State modes.

### Confirmation

First inspect the fixed targets for the selected stage and show the exact changes without making any mutation. Ask the user for confirmation.

The initial invocation is not approval. Apply the fixed changes directly only after the user explicitly accepts that preview. Report the result and deleted targets briefly; deletion is permanent for untracked files unless separately backed up. Do not invoke another workflow operation.
