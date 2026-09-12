# reset Skill Contract

## Purpose

Provide controlled, previewed rollback of Interface workflow outputs.

## Responsibility

Resolve one fixed reset stage, preview its complete impact, obtain explicit Human confirmation, and apply only that preview. Reset removes; it never interprets intent or rebuilds what it removed.

## Trigger

Activate only through explicit Human invocation with one reset stage. Invocation itself is never approval to mutate.

## Inputs

Accept exactly one semantic stage: Configure reset, Task reset, or Develop reset. Native commands may map these to stable arguments. Resolve Config targets from the Interface and developed output directories from owning Component Preferences.

## Outputs

Before mutation, produce the selected stage, every resolved file, directory, runtime stop, and record change, plus everything preserved. After confirmation, produce the applied outcome, resulting State, anything not applied, and required next steps.

## Required Understanding

Establish Interface Understanding and current ownership boundaries. Target Understanding is unnecessary for the fixed reset scope. Read current Config catalogs, State, Plan, Review, Platform Launch authorities, and Component code-path ownership when applicable.

## Authority

After confirmation, remove or reset only exact targets shown in the preview and owned by the selected stage. Stop only affected project runtime parts. Never reverse Environment preparation or remove an unclaimed implementation path.

## Workflow Invariants

- The stages are nested: Configure reset removes Config and developed outputs; Task reset clears planning plus downstream development and review; Develop reset preserves planning while clearing development and review.
- A lower native stage number may represent a broader rollback, but semantic stage names remain authoritative.
- Resolve every target before mutation and disclose whether untracked deletion is unrecoverable.
- Stop affected runtime in declared dependency order before removing developed output.
- Configure reset preserves the Config container and does not regenerate Config.
- Task reset preserves State History, returns affected operational aggregates and Tasks to owned initial values, removes affected implementation and Findings, and appends reset History.
- Develop reset preserves truthful Planning content and progress, resets affected Development and Review state and Task execution state, removes implementation and Findings, and appends reset History.
- Never invoke another workflow operation after Reset.

## Verification

After confirmation, verify every previewed target's actual outcome, confirm no unlisted target changed, and reconcile surviving State with surviving outputs.

## Idempotency

Preview is always safe to repeat. Applying an already-realized stage produces no additional deletion beyond the newly resolved and confirmed preview.

## Stopping Conditions

Stop before mutation for missing or ambiguous stage input, unresolved ownership, unsafe target resolution, inability to stop a dependent runtime safely, or absent explicit confirmation. A changed preview requires renewed confirmation.

## Runtime Realization

A native adapter exposes the three stable semantic stages through Agent Command Profile, separates preview from apply, and uses recoverable deletion where practical while truthfully warning when recovery is unavailable.
