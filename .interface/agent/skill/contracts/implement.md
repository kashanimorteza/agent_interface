# implement Skill Contract

## Purpose

Provide one trustworthy end-to-end path from operational readiness through verified implementation and eligible launch.

## Responsibility

Coordinate Configure, baseline Review where work exists, Planning, Development, independent final Review, Finding reconciliation, and Launch while preserving every operation's authority. Implement performs no product operation of its own.

## Trigger

Activate explicitly for zero or more phase selections when the Human wants complete orchestration rather than operation-by-operation control.

## Inputs

Accept zero or more phase positions. Empty input selects every phase currently enabled and ready. Resolve positions to stable identifiers, validate all tokens, deduplicate them, and process in Target order. Consume current operation Contracts, Target eligibility, operational records, dependencies, implementation, and Review evidence.

## Outputs

Produce the integrated ordered outcomes of each delegated operation, Implementation State and History owned by Implement, withheld dependency results, all Blockers and Open Questions, and a truthful distinction between selected-scope completion and whole-Target completion.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Resolve the current Contracts and active implementations for Configure, Planning, Developing, Reviewing, and Launch, their owned records, and their gates.

## Authority

Coordinate operation Skills directly and write only Implementation State and its History independently. Every delegated mutation remains under the invoked Skill and owning Component. Never bypass Human approval or combine operation ownership.

## Workflow Invariants

1. Execute Configure once.
2. Resolve selected implementable phases and their authorities, records, dependencies, and current outputs.
3. For existing work, run independent baseline Review. Preserve work and skip regeneration only when Review is satisfied, Planning and Development are truthfully complete, and their sources are current.
4. For a phase with no work, skip empty baseline Review and run Planning.
5. Reconcile unsatisfied existing work through Planning using baseline Findings.
6. Require complete, valid, current Planning and passed coverage validation before Development.
7. Execute Development and its completion gate, then independent final Review.
8. Reconcile a not-satisfied result through Planning, Development, and Review only while each cycle closes or materially advances a Finding. Stop on a repeated unresolved Finding, no observable progress, inconclusive result, or Human decision.
9. Withhold later work that depends on an incomplete phase; independent phases may continue.
10. Launch only when every currently enabled and ready phase—not merely the selected subset—has completed Planning and Development and has satisfied Review.

Implementation never derives its sequence from a mutable project Workflow. It locates and executes operation Skills directly rather than depending on nested command invocation. No incomplete or missing gate is passed.

## Verification

Verify every delegated operation's own success evidence and gate. Overall completion additionally requires every currently implementable phase to be independently satisfied and Launch to complete.

## Idempotency

Repeated invocation reconciles current authorities with existing work, preserves valid completed output, and does not repeat satisfied work without changed sources.

## Stopping Conditions

Stop before all mutation on invalid input or an empty implementable selection. Stop an affected phase on an unmet operation gate, repeated Finding, no progress, inconclusive Review, dependency failure, or required Human decision. Any incomplete implementable phase prevents Launch and overall completion.

## Runtime Realization

A native adapter exposes optional multi-phase input, resolves operation implementations through Skill Preferences, invokes them directly in the fixed Contract order, and reports every operation and reconciliation outcome in execution order.
