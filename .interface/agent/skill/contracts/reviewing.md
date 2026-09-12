# reviewing Skill Contract

## Purpose

Provide independent evidence-based judgment of implemented phase results.

## Responsibility

Observe whether implementation satisfies current Target intent, Component authorities, Plans, acceptance criteria, and verification conditions; record Findings and exact Review outcomes. Review reports and never repairs or replans.

## Trigger

Activate explicitly for zero or more phase selections, as a baseline assessment of existing work, or as an independent final gate after Development.

## Inputs

Accept zero or more phase positions. Empty input selects every enabled phase. Resolve positions to stable identifiers, deduplicate them, and process in Target order. Consume current Target Understanding, applicable Principles and Preferences, Plans, State, prior Review records, implementation, public interfaces, and recorded evidence.

## Outputs

Produce reconciled Review Findings, exact aggregate Review outcomes and History, missing-evidence records, and an evidence-first phase report. Do not update Task progress or active Workflow mode.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Read Review, Plan, and State authorities and every Component applicable to each selected phase.

## Authority

Observe and execute non-repairing verification. Write only Review-owned Findings, aggregate Review State, and Review History. Never modify implementation, Plan, Target, Task progress, or another operation's records.

## Workflow Invariants

- Validate all phase input before changing records or running verification.
- Build a transient review ledger covering every Target requirement, applicable Component obligation, Plan acceptance clause, and recorded verification condition.
- Observe each condition independently and judge whether the implementer's check actually establishes it; use adversarial or independent cases where practical.
- Ground every Finding in the expected condition, actual observation, and exact location or observable result.
- Record missing Plan coverage as a Gap and absent observable proof as missing evidence; never reconstruct or infer missing evidence.
- Record phase-level work absent from every Task as a phase Finding without planning its repair.
- Reconcile prior Findings only through current observation. A Finding persists until Review proves it resolved or the Human accepts it.
- Review later independent phases even when another phase is not satisfied or inconclusive.

## Verification

Every Review conclusion must be traceable to current observable evidence. A phase ends only as `satisfied`, `not satisfied`, or `inconclusive` under current Review authority.

## Idempotency

Repeated Review preserves stable Findings and outcomes when evidence is unchanged, while appending only the operational History required by State.

## Stopping Conditions

Stop the complete run before observation on invalid input. Mark an affected phase inconclusive when required evidence cannot be observed or authorities conflict; never convert uncertainty into satisfaction or a repair action.

## Runtime Realization

A native adapter exposes optional multi-phase input, uses read and verification capabilities without repair authority, and reports reviewed scope, Findings, verification, missing evidence, outcomes, and records changed.
