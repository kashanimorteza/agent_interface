# configure Skill Contract

## Purpose

Establish operational readiness for Interface work.

## Responsibility

Initialize and reconcile operational Config, synchronize aggregate phase identity and State, and prepare the selected Platform Environment. It owns no planning, implementation, review, launch, reset, or Target interpretation beyond the limited facts required for configuration.

## Trigger

Activate when operational Config or Environment readiness must be created, validated, repaired, or refreshed, and once at the start of end-to-end implementation orchestration.

## Inputs

Accept no phase selection. Consume current operational Schemas, existing Config, stable Target phase identifiers, explicit Platform selections and requirements, and Platform defaults where Target is silent.

## Outputs

Produce Schema-valid operational Config, synchronized phase State records, a prepared selected Environment, truthful State position and History, and a report of created, reconciled, preserved, conflicted, and blocked results.

## Required Understanding

Establish Interface Understanding. Establish only the Target Understanding needed to resolve stable phase identities and explicit Platform selections or Environment requirements. Read current Config Schemas, State authorities, and Platform authorities.

## Authority

Write only Config records owned by Configure and perform only system preparation required by the selected Environment. Never modify other Interface sources or product implementation.

## Workflow Invariants

- Derive initialization and reconciliation from each current Schema rather than a remembered structure.
- Preserve meaningful operational records through structural reconciliation; surface a conflict rather than discard information that has no other owner.
- Add missing phase records at current initial values and preserve progress. Remove a stale phase record only while it contains initialization defaults; otherwise preserve and report it.
- Never copy phase title, goal, target, status, readiness, or other Target meaning into State.
- Inspect the Environment before changing it and apply only missing declared requirements.
- Record active Configure position and append the outcome under State ownership.

## Verification

Validate every Config record against its applicable Schemas, verify phase identity reconciliation, and observe every Environment requirement claimed as satisfied.

## Idempotency

Repeating against unchanged Schemas, Target identity, Config, and Environment produces no structural or system mutation while still recording invocation outcomes as State permits.

## Stopping Conditions

Stop or preserve the affected item when reconciliation would lose meaningful records, a required Environment choice is unresolved, preparation exceeds authority, or a genuine preparation condition cannot be resolved safely. Independently valid items may continue.

## Runtime Realization

A native adapter exposes one project-scoped Configure capability, resolves all paths and native mechanisms through the current Interface and Runtime mapping, and reports Config, phase synchronization, Environment, preserved records, and blockers.
