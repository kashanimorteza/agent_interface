---
name: my-interface-reset
description: Preview and, after explicit confirmation, reset Interface Config, Tasks, or developed code. Choose 1 for configure, 2 for task, or 3 for develop.
argument-hint: "[1=configure | 2=task | 3=develop]"
disable-model-invocation: true
---

# Reset the project workflow

## Role

Preview and reset exactly one selected workflow stage, using the current Interface authorities.

Reset is mechanical and destructive. It does not interpret project intent, generate configuration, create Tasks, develop, or review, because deciding what should exist is a different question from removing what does, and mixing them would let a reset quietly rebuild the thing it just deleted.

The three stages are nested, not ordered by size: `3` discards development, `2` discards planning and development, and `1` discards everything the Interface has generated. The number chooses how far back to go, so a lower number destroys more rather than less.

This is the only operation that deletes. Its preview is the one point in the Workflow where a human decides before something is lost, which is why the preview is always shown in full, the initial invocation is never treated as approval, and nothing is removed that the preview did not name.

## Input

Accept exactly one numeric argument from `$ARGUMENTS`: `1` (configure), `2` (task), or `3` (develop). A lower number reaches further back and destroys more, so confirm which stage the human means when the request names an outcome rather than a number.

These numbers select a stage; they do not rename the existing State modes, which keep the names the State Component defines.

## Workflow

First establish Agent Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to locate the current Config records, the reset definitions, the ownership boundaries, and the implementation directories Reset affects. Target Project Understanding is not required for this mechanical operation.

Resolve the implementation directories that may be removed from the code path each Component records in its own Preferences. Remove no directory that no Component claims, and hold no list of directories here.

### 1 = Configure reset

Remove every operational Config file the Interface document lists and the developed implementation outputs the current Interface owns. Preserve their container directory. Do not regenerate Config, because regeneration belongs to Configure and running it here would hide whether the reset itself worked.

### 2 = Task reset

Clear planned Groups and Tasks according to the current Task structure. Return State to its pre-planning position and clear the active phase. Remove the developed implementation outputs. Clear the recorded Findings for the affected phases, because a Finding about work that no longer exists misleads whoever reads it next. Preserve shared operational records according to current ownership.

### 3 = Develop reset

Return State to its pre-development position and clear the active phase. Return every existing Task to the current initial Task status, remove the transient blocking association where required, and preserve each Task's content and history. Remove the developed implementation outputs and clear the recorded Findings for the affected phases, since both describe an implementation that is being discarded. Preserve Plans, Groups, and shared operational records according to current ownership.

### Confirmation

Inspect the resolved targets for the selected stage and show the exact changes without making any mutation. Then ask the user for confirmation.

The initial invocation is not approval. Apply the resolved changes only after the user explicitly accepts that preview. Deletion is permanent for untracked files unless they are separately backed up, which is why the preview exists and why it is never skipped.

Do not invoke another workflow operation after resetting.

## Boundaries

Reset one selected stage only. Do not interpret project intent, generate configuration, create Tasks, develop, review, or remove anything outside the resolved targets shown in the preview.

## Report

Before mutating, present the preview:

1. **Stage selected** — the number given and the stage it resolves to.
2. **Resolved targets** — every file and directory that would be removed or changed, each with the source that established it as a target.
3. **What is preserved** — the operational records and content the selected stage keeps.

After confirmation, report the outcome:

4. **Applied** — what was actually removed or changed, and the resulting State position.
5. **Not applied** — anything in the preview that could not be changed, and why.
6. **Required next step** — when the applied stage removed the operational Config records, say plainly that no other operation can run until Configure recreates them.
