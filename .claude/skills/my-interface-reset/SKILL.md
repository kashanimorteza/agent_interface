---
name: my-interface-reset
description: Preview and, after explicit confirmation, reset selected Target phases, every phase with generated work, operational Config only, or the complete Interface-generated system. Use phase identifiers, no argument for all generated phases, config, or complete.
argument-hint: "[phase-number ... | config | complete]"
disable-model-invocation: true
---

# Reset the project workflow

This file is the Claude Code adapter for the portable `reset` Skill Contract. Resolve and read that Contract through Agent Skill Profile before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Preview and reset exactly one selected scope, using the current Interface authorities.

Reset is mechanical and destructive. It does not interpret project intent, generate configuration, create Tasks, develop, or review, because deciding what should exist is a different question from removing what does, and mixing them would let a reset quietly rebuild the thing it just deleted.

Reset removes or clears the outputs of explicit phases, all generated phases, Config, or Complete scope within its current authority. Show the complete preview so the human can approve the exact changes before they are applied. The initial invocation is never treated as approval, and nothing is removed that the preview did not name.

## Input

Accept exactly one of these forms from `$ARGUMENTS`:

- no argument — discover and reset every phase with generated Plan, Review, Development, or implementation output;
- `<phase-number ...>` — one or more unique phase identifiers, written as `1`, `2`, `3`, or their canonical `P1`, `P2`, `P3` forms. Normalize them to canonical identifiers and process them in Target order.
- `config` — remove operational Config while preserving developed implementation outputs.
- `complete` — remove operational Config and the developed outputs of every phase owned by the Interface.

For an invocation without arguments, derive the affected set from current Plan entries, Review entries and Findings, non-initial Phase State, Task evidence, and attributable implementation outputs. Phases that have no generated work are not affected. If no generated phase exists, report a no-op preview and make no mutation.

Reject an unknown named mode, mixed named modes and phase identifiers, a duplicate phase, or a phase absent from the current Target and Config catalogs. Every numeric argument denotes a phase identifier; the former numeric reset-stage meaning no longer applies.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to locate the current Config records, ownership boundaries, and implementation outputs Reset may affect. For a phase reset, establish the minimum Target Understanding needed to validate phase identity, order, scope, and owning Components. Config scope does not require Target Understanding. Complete scope uses only the phase identities and ownership needed to enumerate all Interface-owned implementation outputs.

Resolve the implementation directories that may be removed from the code path each Component records in its own Preferences. Remove no directory that no Component claims, and hold no list of directories here.

When a selected scope removes developed output, resolve any affected active runtime and its shutdown order from the current Platform and Launch authorities and observable runtime evidence. Include every proposed stop action in the preview. After confirmation, stop only the affected runtime in that declared order before removing its files. Preserve Environment preparation, system packages, and system-level settings unless the human separately requests their removal.

### Phase reset

For every selected phase:

- remove that phase's Plan entry, including its Groups, Tasks, Task status, and Task history;
- remove that phase's Review entry and Findings, then recalculate Plan and Review aggregate counts;
- return that phase's Planning, Development, and Review progress to their initial values;
- remove developed outputs safely attributable to that phase; and
- reconcile active, Implementation, and Launch State with the outputs that remain, preserve State History, and append the reset outcome for that phase.

Resolve implementation attribution from the selected phase's Plan, Task evidence and logs, owning Component Preferences, and observable repository state. A Component code path may be removed as a whole only when it is owned exclusively by selected phases. When selected and preserved phases share a path, remove only changes attributable to the selected phases. If attribution is incomplete or removing a selected-phase change would damage preserved work, stop before mutation and report the ambiguity; never delete the shared path or guess a reverse patch.

Do not alter Plan, Review, phase State, implementation output, or History belonging only to an unselected phase. Preserve the Config files and their containers.

### Config reset

Remove every operational Config file currently catalogued by the Interface. Preserve the Config container, all developed implementation outputs, and Environment preparation. Do not regenerate Config, because regeneration belongs to Configure and running it here would hide whether the reset itself worked. Report that surviving implementation is no longer represented by operational Config until Configure recreates and later operations reconcile those records.

### Complete reset

Remove every operational Config file currently catalogued by the Interface and every developed implementation output attributable to any Target phase and owned by the current Interface. This is the union of Config reset and resetting all phases. Preserve only the Config container, Interface sources, Human and Technical Target definitions, Environment preparation, and anything outside Interface ownership. Do not regenerate Config or invoke another operation afterward.

### Confirmation

Inspect the resolved targets for the selected scope and show the exact changes without making any mutation. Then ask the user for confirmation.

The initial invocation is not approval. Apply the resolved changes only after the user explicitly accepts that preview. Deletion is permanent for untracked files unless they are separately backed up, which is why the preview exists and why it is never skipped.

Do not invoke another workflow operation after resetting.

## Boundaries

Perform only the selected Reset scope. Do not perform another Interface Operation, reinterpret Target intent, reverse Environment preparation, or remove anything outside the resolved targets shown in the preview.

## Report

Before mutating, present the preview:

1. **Scope selected** — the explicit normalized phase identifiers, the discovered generated phases for an argument-free invocation, `config`, or `complete`.
2. **Resolved targets** — every file and directory that would be removed or changed, each with the source that established it as a target.
3. **What is preserved** — the operational records, phases, implementation outputs, and Environment the selected scope keeps.

After confirmation, report the outcome:

4. **Applied** — what was actually removed or changed, and the resulting State position.
5. **Not applied** — anything in the preview that could not be changed, and why.
6. **Required next step** — for a phase reset, identify that Planning or Implement may rebuild the selected phases; for config or complete reset, identify which operations must wait for Configure to recreate operational Config. Operations that do not require removed records remain available within their current authority.
