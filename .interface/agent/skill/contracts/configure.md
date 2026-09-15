# configure Skill Contract

## Purpose

Prepare the project for the Interface workflow.

## Responsibility

Establish Interface and Target Understanding, generate or reconcile the four operational Config files from their Schemas, install declared technical requirements, and prepare the selected project Environment for Development. It owns no planning, implementation, review, launch, reset, or Target interpretation beyond the limited facts required for configuration.

## Trigger

Activate when operational Config or Environment readiness must be created, validated, repaired, or refreshed, and once at the start of end-to-end implementation orchestration.

## Inputs

Accept no phase selection. Consume current operational Schemas, existing Config, stable Target phase identifiers, explicit Target and Platform selections, all applicable Implementation Component Principles and Preferences, the selected Platform Preferences and Launch Item, and Platform defaults where Target is silent.

## Outputs

Produce or reconcile Schema-valid `plan.yaml`, `state.yaml`, `review.yaml`, and `application.yaml` Config files, resolved and prepared technical requirements and Environment, truthful State position and History, and a report of created, installed, reconciled, preserved, conflicted, and blocked results.

## Required Understanding

Establish Interface Understanding and only the Target Understanding needed for Config generation and declared technical or Environment requirements. Read current Config Schemas, applicable Implementation Component authorities, and Platform authorities.

## Authority

Write the four Config records owned by Configure and perform technical dependency installation and system preparation required by the selected Platform Launch Item. Never modify other Interface sources or product implementation.

## Workflow Invariants

- Generate or reconcile all four Config files from their current Schemas rather than a remembered structure; `application.yaml` follows the same process as the other three files.
- Preserve meaningful operational records through structural reconciliation; surface a conflict rather than discard information that has no other owner.
- Add missing phase records at current initial values and preserve progress while generating `state.yaml`; remove a stale record only while it contains initialization defaults, otherwise preserve and report it.
- Never copy Target meaning into Config.
- Resolve every applicable language, package-management, package, database, tool, platform, and version selection from Implementation and Platform authorities before installation.
- Install or reconcile every required resolved technical item and record its concrete version and verification result.
- Inspect every applicable Platform Component definition and apply its declared system requirements for the selected Launch Item.
- Inspect the Environment before changing it and apply only missing declared requirements.
- Record active Configure position and append the outcome under State ownership.

## Verification

Validate every Config record against its applicable Schemas, verify phase identity reconciliation, verify every resolved technical item and its concrete version, and observe every Platform Environment requirement claimed as satisfied.

## Idempotency

Repeating against unchanged Schemas, Target identity, Config, resolved technical selections, and Platform Environment produces no structural or installation mutation while still recording invocation outcomes as State permits.

## Stopping Conditions

Stop or preserve the affected item when reconciliation would lose meaningful records, a required Environment choice is unresolved, preparation exceeds authority, or a genuine preparation condition cannot be resolved safely. Independently valid items may continue.

## Runtime Realization

A native adapter exposes one project-scoped Configure capability, resolves all paths and native mechanisms through the current Interface and Runtime mapping, and reports Config, phase synchronization, Environment, preserved records, and blockers.
