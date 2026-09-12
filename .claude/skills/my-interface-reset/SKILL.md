---
name: my-interface-reset
description: Preview and, after explicit confirmation, reset Interface Config, Tasks, developed code, and any active project runtime covered by the selected stage. Choose 1 for configure, 2 for task, or 3 for develop.
argument-hint: "[1=configure | 2=task | 3=develop]"
disable-model-invocation: true
---

# Reset the project workflow

This file is the Claude Code adapter for the portable `reset` Skill Contract. Resolve and read that Contract through Agent Skill Profile before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Preview and reset exactly one selected workflow stage, using the current Interface authorities.

Reset is mechanical and destructive. It does not interpret project intent, generate configuration, create Tasks, develop, or review, because deciding what should exist is a different question from removing what does, and mixing them would let a reset quietly rebuild the thing it just deleted.

The three stages are nested, not ordered by size: `3` discards development, `2` discards planning and development, and `1` discards everything the Interface has generated. The number chooses how far back to go, so a lower number destroys more rather than less.

Reset removes or clears the outputs of the selected stage within its current authority. Show the complete preview so the human can approve the exact changes before they are applied. The initial invocation is never treated as approval, and nothing is removed that the preview did not name.

## Input

Accept exactly one numeric argument from `$ARGUMENTS`: `1` (configure), `2` (task), or `3` (develop). A lower number reaches further back and destroys more, so confirm which stage the human means when the request names an outcome rather than a number.

These numbers select a stage; they do not rename the existing State modes, which keep the names the State Component defines.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to locate the current Config records, ownership boundaries, and the implementation directories Reset affects. The three stage definitions below are Reset's fixed scope. Target Understanding is not required to decide that scope.

Resolve the implementation directories that may be removed from the code path each Component records in its own Preferences. Remove no directory that no Component claims, and hold no list of directories here.

When a selected stage removes developed output, resolve the active runtime and its shutdown order from the current Platform and Launch authorities and observable runtime evidence. Include every proposed stop action in the preview. After confirmation, stop the runtime in that declared order before removing its files. Preserve Environment preparation, system packages, and system-level settings unless the human separately requests their removal.

### 1 = Configure reset

Remove every operational Config file currently catalogued by the Interface and include every affected entry in the preview. After confirmation, remove those files and the developed implementation outputs the current Interface owns. Preserve the Config container itself. Do not regenerate Config, because regeneration belongs to Configure and running it here would hide whether the reset itself worked.

### 2 = Task reset

Clear planned Groups and Tasks according to the current Plan structure. Return every affected phase's Planning, Development, and Review progress to their initial values; return Implementation State to `not started`; reconcile Launch State with any stopped runtime; return active State to its pre-planning position and clear the active phase. Remove developed implementation outputs and recorded Findings for the affected phases. Preserve State History and append the reset outcome.

### 3 = Develop reset

Return every affected phase's Development and Review progress to their initial values while preserving truthful Planning progress; return Implementation State to `not started`; reconcile Launch State with any stopped runtime; return active State to its pre-development position and clear the active phase. Return every existing Task to the current initial Task status, remove transient blocking associations where required, and preserve each Task's content and history. Remove developed outputs and Findings for affected phases. Preserve State History and append the reset outcome.

### Confirmation

Inspect the resolved targets for the selected stage and show the exact changes without making any mutation. Then ask the user for confirmation.

The initial invocation is not approval. Apply the resolved changes only after the user explicitly accepts that preview. Deletion is permanent for untracked files unless they are separately backed up, which is why the preview exists and why it is never skipped.

Do not invoke another workflow operation after resetting.

## Boundaries

Perform only the selected Reset stage. Do not perform another Interface Operation, interpret Target intent, reverse Environment preparation, or remove anything outside the resolved targets shown in the preview.

## Report

Before mutating, present the preview:

1. **Stage selected** — the number given and the stage it resolves to.
2. **Resolved targets** — every file and directory that would be removed or changed, each with the source that established it as a target.
3. **What is preserved** — the operational records and content the selected stage keeps.

After confirmation, report the outcome:

4. **Applied** — what was actually removed or changed, and the resulting State position.
5. **Not applied** — anything in the preview that could not be changed, and why.
6. **Required next step** — when the applied stage removed operational Config records, identify which operations require those records and must wait for Configure to recreate them. Operations that do not require the removed records remain available within their current authority.
