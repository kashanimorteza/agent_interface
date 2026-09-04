---
name: my-interface-reset
description: Preview and, after explicit confirmation, reset planning output or developed code using two fixed reset stages.
argument-hint: "[planning|development]"
disable-model-invocation: true
---

# Reset the project workflow

Run the bundled `scripts/reset.py` from the project root with exactly one stage: `planning` or `development`.

Do not read the Interface map, project definition, Schema, Principles, Preferences, or unrelated configuration. The operation uses only these fixed targets:

- `.interface/config/task.yaml`
- `.interface/config/state.yaml`
- Root `backend/`, `frontend/`, and `database/` directories for a development reset

## Planning reset

Preserve the Task frame and every phase Plan, but replace every Plan's `groups` value with an empty mapping. Set `content.active` in State to `null`. Do not change blockers, open questions, or any other file.

## Development reset

First set State active mode to `planning` with no active phase. Then set every existing Task status to `todo`, remove its blocker field when present, and preserve its other fields and log. Delete the root `backend/`, `frontend/`, and `database/` directories when present. Do not change blockers, open questions, Plans, Groups, or any other file.

## Confirmation

First run `scripts/reset.py <stage>` without `--apply`. It prints the exact changes and makes no mutation. Show the preview to the user and ask for confirmation.

The initial invocation is not approval. Run `scripts/reset.py <stage> --apply` only after the user explicitly accepts that preview. Report the script result briefly and do not invoke another workflow operation.
