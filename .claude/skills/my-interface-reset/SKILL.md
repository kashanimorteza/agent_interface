---
name: my-interface-reset
description: Preview and, after explicit confirmation, reset selected Target phases, every phase with generated work, operational Config only, or the complete Interface-generated system. Use phase identifiers, no argument for all generated phases, config, or complete.
argument-hint: "[phase-number ... | config | complete]"
disable-model-invocation: true
metadata:
  contract: ".interface/agent/skill/contracts/reset.md"
  contract_sha256: "sha256:fc85966236367706382051177df70c6f89c7a57aa220a80420365f142040ebef"
  synced_at: "2026-09-17T18:39:11Z"
---

# Reset the project workflow

This file is the self-contained Claude Code realization of the portable `reset` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Role

Provide controlled, previewed rollback of Interface workflow outputs: preview and reset exactly one selected scope, using the current Interface authorities. Run only on explicit Human invocation of `/my-interface-reset` with one reset scope.

Reset is mechanical and destructive. It does not interpret project intent, generate configuration, create Tasks, develop, or review, because deciding what should exist is a different question from removing what does, and mixing them would let a reset quietly rebuild the thing it just deleted.

Reset removes or clears the outputs of explicit phases, all generated phases, Config, or Complete scope within its current authority. Show the complete preview so the human can approve the exact changes before they are applied. The initial invocation is never treated as approval, and nothing is removed that the preview did not name.

## Input

Accept exactly one of these forms from `$ARGUMENTS`:

- no argument — discover and reset every phase with generated Plan, Review, Development, or implementation output;
- `<phase-number ...>` — one or more unique phase identifiers, written as `1`, `2`, `3`, or their canonical `P1`, `P2`, `P3` forms. Normalize them to canonical identifiers and process them in Target order.
- `config` — remove operational Config while preserving developed implementation outputs.
- `complete` — remove operational Config and the developed outputs of every phase owned by the Interface.

For an invocation without arguments, derive the affected set from current Plan entries, Review entries and Findings, non-initial Phase State, Task evidence, and attributable implementation outputs. Phases that have no generated work are not affected. If no generated phase exists, report a no-op preview and make no mutation.

Reject an unknown named mode, mixed named modes and phase identifiers, a duplicate phase, or a phase absent from the current Target and Config catalogs. Every numeric argument denotes a phase identifier, never a rollback stage.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to locate the current Config records, ownership boundaries, and implementation outputs Reset may affect. For a phase reset, establish the minimum Target Understanding needed to validate phase identity, order, scope, and owning Components. Config scope does not require Target Understanding. Complete scope uses only the phase identities and ownership needed to enumerate all Interface-owned implementation outputs. Read current Config catalogs, State, Plan, Review, Platform Launch authorities, Task evidence, and Component code-path ownership when applicable.

Resolve the implementation directories that may be removed from the code path each Component records in its own Preferences. Remove no directory that no Component claims, and hold no list of directories here.

When a selected scope removes developed output, resolve any affected active runtime and its shutdown order from the current Platform and Launch authorities and observable runtime evidence. Include every proposed stop action in the preview. After confirmation, stop only the affected runtime in that declared order before removing its files. Preserve Environment preparation, system packages, and system-level settings; Reset never reverses Environment preparation.

### Phase reset

For every selected phase:

- remove that phase's Plan entry, including its Groups, Tasks, Task status, and Task history;
- remove that phase's Review entry and Findings, then recalculate Plan and Review aggregate counts;
- return that phase's Planning, Development, and Review progress to their initial values;
- remove developed outputs safely attributable to that phase; and
- reconcile active, Implementation, and Launch State with the outputs that remain, preserve State History, and append one reset outcome for that phase.

Resolve implementation attribution from the selected phase's Plan, Task evidence and logs, owning Component Preferences, and observable repository state. A Component code path may be removed as a whole only when it is owned exclusively by selected phases. When selected and preserved phases share a path, remove only changes attributable to the selected phases. If attribution is incomplete or removing a selected-phase change would damage preserved work, stop before mutation and report the ambiguity; never delete the shared path or guess a reverse patch.

Do not alter Plan, Review, phase State, implementation output, or History belonging only to an unselected phase. An argument-free reset applies this same phase-reset behavior to every discovered phase with generated work. Preserve the Config files and their containers.

### Config reset

Remove every operational Config file currently catalogued by the Interface. Preserve the Config container, all developed implementation outputs, and Environment preparation. A removed Config file MUST be physically absent: clearing its records, truncating it, replacing it with schema defaults, or recreating an initialized file is not a Config reset.

The bounded Config-removal helper ships with this Skill at `.claude/skills/my-interface-reset/scripts/remove_config_files.py`; run it from the project root by that path. It unlinks only individually listed regular files below the exact Config directory and never removes that directory recursively. Use it for both preview and apply. Before confirmation, run `python3 .claude/skills/my-interface-reset/scripts/remove_config_files.py --config-root <resolved-config-directory> <resolved-config-file ...>` without `--apply` and include its validated target list in the preview. After confirmation, run the same command with `--apply`. Do not use Edit or Write to simulate deletion. Do not regenerate Config, because regeneration belongs to Configure and running it here would hide whether the reset itself worked. Report that surviving implementation is no longer represented by operational Config until Configure recreates and later operations reconcile those records.

### Complete reset

Remove every operational Config file currently catalogued by the Interface and every developed implementation output attributable to any Target phase and owned by the current Interface. This is the union of Config reset and resetting all phases. Preserve only the Config container, Interface sources, Human and Technical Target definitions, Environment preparation, and anything outside Interface ownership.

Resolve and remove implementation outputs first, keeping Config records available as ownership evidence throughout, then physically delete the Config files last through `.claude/skills/my-interface-reset/scripts/remove_config_files.py` using the same previewed target list. Do not truncate, initialize, rewrite, or recreate them. Do not regenerate Config or invoke another operation afterward.

### Confirmation

Resolve every target for the selected scope before any mutation, and show the exact changes without making any mutation. Then ask the Human for confirmation.

The initial invocation is not approval. Apply the resolved changes only after the Human explicitly accepts that preview.

Use recoverable deletion wherever practical. For each resolved target, state in the preview whether it is recoverable — for example, tracked by version control so it can be restored from history — or whether its deletion is unrecoverable because it is untracked and not otherwise backed up. Never describe an unrecoverable deletion as recoverable. This disclosure is why the preview exists and why it is never skipped.

Confirmation authorizes only the exact targets validated in the preview, for every scope. If that list changes for any reason, preview again and obtain renewed confirmation before applying anything.

Do not invoke another workflow operation after resetting.

## Verification

After confirmation and application, verify every previewed target's actual outcome and confirm that no target outside the preview changed. For Config and Complete scopes, additionally verify that every previewed Config path is physically absent and that every protected Interface source observed during preview remains present and unchanged. A remaining, empty, initialized, or recreated Config file makes the Reset failed, regardless of scope. Reconcile surviving State with surviving outputs only when a State record remains after the applied removal.

## Idempotency

Preview is always safe to repeat and never mutates anything. Re-running Reset against a scope that is already fully realized (its previewed targets are already absent or already reset) produces no additional deletion beyond whatever the newly resolved and confirmed preview still names; do not re-delete, re-clear, or otherwise touch a target that is no longer present.

## Boundaries

Perform only the selected Reset scope. Do not perform another Interface Operation, reinterpret Target intent, reverse Environment preparation, remove an unclaimed implementation path, damage work belonging to an unselected phase, or remove anything outside the resolved targets shown in the preview. Stop only affected project runtime parts.

Never remove or modify an Interface source outside `.interface/foundation/config/`. Before reporting success for any scope, verify that every protected Interface source observed during preview still exists and is unchanged; this verification is mandatory for Config and Complete scopes.

## Stopping Conditions

Stop before any mutation, and report why, when any of the following holds:

- the scope input is missing, ambiguous, mixes named modes with phase identifiers, or names a duplicate or unknown phase;
- a phase selection cannot be validated against the current Target and Config catalogs;
- implementation attribution or code-path ownership cannot be resolved unambiguously;
- a resolved target cannot be safely established (for example, an untracked or unattributable path);
- an affected runtime part cannot be stopped safely in its declared order; or
- explicit Human confirmation of the exact previewed targets has not been given.

If the resolved target list changes for any reason after a preview was shown, treat any prior confirmation as void and require renewed confirmation against the new preview before applying anything.

## Report

Before mutating, present the preview:

1. **Scope selected** — the explicit normalized phase identifiers, the discovered generated phases for an argument-free invocation, `config`, or `complete`.
2. **Resolved targets** — every file and directory that would be removed or changed, every runtime stop action, and every record change, each with the source that established it as a target and whether its removal is recoverable or unrecoverable.
3. **What is preserved** — the operational records, phases, implementation outputs, and Environment the selected scope keeps.

After confirmation, report the outcome:

4. **Applied** — what was actually removed or changed, and the resulting State position.
5. **Not applied** — anything in the preview that could not be changed, and why.
6. **Required next step** — for a phase reset, identify that Planning or Implement may rebuild the selected phases; for config or complete reset, identify which operations must wait for Configure to recreate operational Config. Operations that do not require removed records remain available within their current authority.

For Config and Complete scopes, report success only when every previewed Config path is absent. A remaining, empty, initialized, or recreated Config file is a failed Reset and MUST be listed under **Not applied**.
