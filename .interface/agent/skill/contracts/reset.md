# reset Skill Contract

## Purpose

Provide controlled, previewed rollback of Interface workflow outputs.

## Responsibility

Resolve one declared reset scope—explicit phases, all phases with generated work, Config, or complete—preview its complete impact, obtain explicit Human confirmation, and apply only that preview. Reset removes; it never reinterprets intent or rebuilds what it removed.

## Trigger

Activate only through explicit Human invocation with one reset scope. Invocation itself is never approval to mutate.

## Inputs

Accept exactly one semantic scope: explicit-phase reset with one or more valid phase identifiers, argument-free reset of every phase with generated work, Config-only reset, or complete reset. Native commands expose these as `<phase-number ...>`, no argument, `config`, and `complete`; named modes cannot be mixed with phase identifiers. Every number denotes a phase, not a rollback stage. Normalize phase identifiers, reject duplicates and unknown phases, and process affected phases in Target order. Discover generated phases from Plan, Review, non-initial Phase State, Task evidence, and attributable implementation outputs; exclude phases with no generated work. Resolve Config targets from the Interface and implementation ownership from phase Plans, Task evidence, owning Component Preferences, and observable repository state.

## Outputs

Before mutation, produce the selected scope, every resolved file, directory, runtime stop, and record change, plus everything preserved. After confirmation, produce the applied outcome, resulting State, anything not applied, and required next steps.

## Required Understanding

Establish Interface Understanding and current ownership boundaries. For selected phases, establish the minimum Target Understanding needed to validate phase identity, order, scope, and Component ownership. Config scope needs no Target Understanding. Complete scope uses only phase identities and ownership needed to enumerate all Interface-owned implementation outputs. Read current Config catalogs, State, Plan, Review, Platform Launch authorities, Task evidence, and Component code-path ownership when applicable.

## Authority

After confirmation, remove or reset only exact targets shown in the preview and owned by the selected scope. Stop only affected project runtime parts. Never reverse Environment preparation, remove an unclaimed implementation path, or damage work belonging to an unselected phase.

## Workflow Invariants

- A selected-phase reset removes each selected phase's Plan, Task content and history, Review and Findings, attributable implementation output, and aggregate progress while preserving unselected phases.
- An argument-free reset applies the same phase-reset behavior to every discovered phase with generated work and preserves operational Config.
- When an argument-free invocation discovers no generated phase, produce a no-op preview and perform no mutation.
- Recalculate Plan and Review aggregate counts after removing selected phase records.
- Reconcile active, Implementation, and Launch State with surviving outputs; preserve State History and append one reset outcome for each selected phase.
- Remove an entire Component code path only when selected phases own it exclusively. For a path shared with preserved phases, remove only safely attributable selected-phase changes; unresolved attribution stops mutation.
- A Config reset removes all operational Config files while preserving developed implementation outputs, the Config container, and Environment preparation; report that implementation records must later be reconciled.
- A Complete reset is the union of Config reset and all-phase reset: remove all operational Config and all developed implementation outputs owned by Target phases, while preserving Interface and Target sources, the Config container, and Environment preparation.
- Resolve every target before mutation and disclose whether untracked deletion is unrecoverable.
- Stop affected runtime in declared dependency order before removing developed output.
- Config and Complete reset do not regenerate Config.
- Never invoke another workflow operation after Reset.

## Verification

After confirmation, verify every previewed target's actual outcome, confirm no unlisted target changed, and reconcile surviving State with surviving outputs.

## Idempotency

Preview is always safe to repeat. Applying an already-realized scope produces no additional deletion beyond the newly resolved and confirmed preview.

## Stopping Conditions

Stop before mutation for missing or ambiguous scope input, an invalid phase selection, unresolved attribution or ownership, unsafe target resolution, inability to stop an affected runtime safely, or absent explicit confirmation. A changed preview requires renewed confirmation.

## Runtime Realization

A native adapter exposes explicit phases, argument-free all-generated phases, config, and complete scopes through Agent Command Profile, separates preview from apply, and uses recoverable deletion where practical while truthfully warning when recovery is unavailable.
