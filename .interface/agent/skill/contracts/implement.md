# implement Skill Contract

## Purpose

Provide one trustworthy sequential path from operational readiness through independently assured implementation and eligible launch.

## Responsibility

Validate phase selection, coordinate Configure once, then execute Planning, Plan Assurance through Reviewing, Development, and final Implementation Assurance through Reviewing for each phase in Target order. Reconcile Findings through their owning operations and advance only after the current phase is satisfied. Implement performs no product operation of its own.

## Trigger

Activate explicitly for zero or more phase selections when the Human wants complete orchestration rather than operation-by-operation control.

## Inputs

Accept zero or more phase positions. Empty input selects every phase currently enabled and ready. Resolve positions to stable identifiers, validate all tokens before mutation, deduplicate them, and retain Target order. Consume current operation Contracts, Target eligibility, operational records, dependencies, implementation, and Review evidence.

## Outputs

Produce the integrated ordered outcomes of Configure and every per-phase Planning, Plan Review, Development, final Review, and reconciliation cycle; Implementation State and History owned by Implement; withheld phase results; all Blockers and Open Questions; eligible Launch; and a truthful distinction between selected-scope completion and whole-Target completion.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Resolve the current Contracts and active implementations for Configure, Planning, Developing, Reviewing, and Launch, their owned records, and their gates.

## Authority

Coordinate operation Skills directly and write only Implementation State and its History independently. Every delegated mutation remains under the invoked Skill and owning Component. Never bypass Human approval or combine operation ownership.

## Workflow Invariants

1. Resolve and validate the complete phase selection before any mutation. Invalid input runs no operation.
2. Execute Configure exactly once, then confirm its required readiness before phase work.
3. Process selected implementable phases strictly in Target order, one complete phase at a time.
4. Execute Planning for the current phase even when a Plan exists; Planning's reconciliation and idempotency preserve valid current work.
5. Execute Reviewing as the Plan gate. Reviewing may coordinate Planning and independently recheck its result. Do not invoke Development until Plan Assurance is `satisfied`.
6. Execute Development for the current phase, including durable checks and its completion gate, then execute Reviewing again for final Plan and Implementation Assurance.
7. When final Review is not satisfied, route Plan Findings through Reviewing's Planning reconciliation and implementation Findings through Development, then run final Review again. Continue only while a cycle closes or materially advances at least one Finding.
8. Stop on a repeated unresolved Finding, no observable progress, inconclusive assurance, unmet dependency, failed operation gate, or required Human decision.
9. Advance to the next selected phase only after the current phase has satisfied Plan and Implementation Assurance. An incomplete phase withholds every later phase in this invocation.
10. Launch only when every currently enabled and ready phase—not merely the selected subset—has completed Planning and Development and has satisfied both Review assurances.

Implementation never derives its sequence from a mutable Target workflow. It locates and executes operation Skills directly rather than depending on nested command invocation. No incomplete or missing gate is passed.

## Verification

Verify every delegated operation's own success evidence and gate. A phase passes only when its current Review record proves both Plan Assurance and Implementation Assurance are satisfied. Overall completion additionally requires every currently implementable phase to pass and Launch to complete.

## Idempotency

Repeated invocation reruns the ordered gates against current authorities while each delegated Skill preserves valid completed work and avoids unnecessary mutation. A satisfied unchanged phase may produce no product change but is still revalidated before advancement.

## Stopping Conditions

Stop before all mutation on invalid input or an empty implementable selection. Stop the run on the first selected phase that cannot pass an operation or assurance gate, makes no reconciliation progress, reaches an inconclusive condition, has an unmet dependency, or requires a Human decision. Any incomplete implementable phase prevents Launch and overall completion.

## Runtime Realization

A native adapter exposes optional multi-phase input, resolves operation implementations through Skill Preferences, invokes Configure once and then the four per-phase gates directly in fixed Contract order, and reports every operation and reconciliation outcome in execution order.
