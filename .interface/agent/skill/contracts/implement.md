# implement Skill Contract

## Purpose

Provide one trustworthy sequential path from operational readiness through independently assured implementation and eligible launch.

## Responsibility

Validate phase selection, coordinate Configure once, then execute Planning, Developing, and Review for each phase in Target order. Reconcile Findings through their owning operations and advance only after the current phase is satisfied. Implement performs no product operation of its own.

## Trigger

Activate explicitly for zero or more phase selections when the Human wants complete orchestration rather than operation-by-operation control.

## Inputs

Accept zero or more phase positions. Empty input selects every phase currently enabled and ready. Resolve positions to stable identifiers, validate all tokens before mutation, deduplicate them, and retain Target order. Consume current operation Contracts, Target eligibility, operational records, dependencies, implementation, and Review evidence.

## Outputs

Produce the integrated ordered outcomes of Configure when it ran, and of every per-phase Planning, Developing, Review, and reconciliation cycle; Implementation State and History owned by Implement, including one step-by-step run entry under State's implementation record that lists the selection, whether Configure ran, and for every phase each Planning → Developing → Reviewing cycle with its outcome, the stop reason when the loop stopped, and the Launch decision; withheld phase results; all Blockers and Open Questions; eligible Launch; and a truthful distinction between selected-scope completion and whole-Target completion.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Resolve the synchronized active Runtime implementations for Configure, Planning, Developing, Reviewing, and Launch, their owned records, and their gates. Never enter the Agent Module to resolve them or their Contracts.

## Authority

Coordinate operation Skills directly and write only Implementation State — its status and the step-by-step run log — and its History independently. Every delegated mutation remains under the invoked Skill and owning Component. Never bypass Human approval or combine operation ownership.

## Workflow Invariants

1. Resolve and validate the complete phase selection before any mutation.
   - Invalid input runs no operation.
2. Resolve Configure, Planning, Reviewing, Developing, and Launch through the synchronized Runtime capability catalog and prove that the Runtime permits Implement to invoke each one as the declared coordinator.
   - Never read Agent Module sources.
   - An unavailable or coordinator-incompatible Child Skill blocks the run before mutation.
3. Execute Configure exactly once when the invocation carried no phase selection, then confirm its required readiness before phase work.
   - When the invocation selected specific phases, do not execute Configure.
4. Process selected implementable phases strictly in Target order, one complete phase at a time.
5. Choose the phase's entry from current records.
   - When the phase already has an implementation — its State record shows Development completed or a Review record exists for it — enter through Reviewing first: Review judges the existing Plan and implementation against current Understanding, so that a changed Target (new models, changed fields, new requirements) surfaces as Findings before any work is redone.
   - When Review is satisfied, the phase is complete as it stands and no Planning or Developing runs.
   - When the phase has no implementation, enter through Planning.
6. Execute Planning for the current phase — even when a Plan exists — reading any recorded Findings; Planning's reconciliation and idempotency preserve valid current work.
7. Execute Developing for the current phase, including durable checks and its completion gate, reading any recorded Findings.
8. Execute Reviewing after implementation exists.
   - Reviewing invokes nothing; it judges the current Plan and implementation against current Understanding and records every Finding with its owning operation.
   - When Review is not satisfied, rerun the cycle for the same phase: Configure when a Finding names it, then Planning, then Developing, then Reviewing.
   - Continue only while a cycle closes or materially advances at least one Finding.
9. Stop on a repeated unresolved Finding, no observable progress, inconclusive assurance, unmet dependency, failed operation gate, or required Human decision.
10. Advance to the next selected phase only after the current phase has satisfied Plan and Implementation Assurance.
   - An incomplete phase withholds every later phase in this invocation.
11. Launch only when every currently enabled and ready phase—not merely the selected subset—has completed Planning and Development and has satisfied both Review assurances.

Implementation never derives its sequence from a mutable Target workflow. It locates and executes operation Skills directly rather than depending on nested command invocation. No incomplete or missing gate is passed.

## Verification

- Verify every delegated operation's own success evidence and gate.
- A phase passes only when its current Review record proves both Plan Assurance and Implementation Assurance are satisfied.
- Overall completion additionally requires every currently implementable phase to pass and Launch to complete.

## Idempotency

Repeated invocation reruns the ordered gates against current authorities while each delegated Skill preserves valid completed work and avoids unnecessary mutation. A satisfied unchanged phase may produce no product change but is still revalidated before advancement.

## Stopping Conditions

- Stop before all mutation on invalid input or an empty implementable selection.
- Stop the run on the first selected phase that cannot pass an operation or assurance gate, makes no reconciliation progress, reaches an inconclusive condition, has an unmet dependency, or requires a Human decision.
- Any incomplete implementable phase prevents Launch and overall completion.

## Runtime Realization

A native adapter exposes optional multi-phase input, resolves operation implementations through synchronized Runtime capabilities, invokes Configure once when no phase was selected and then, for each phase, either Review first when an implementation already exists or Planning first when none does, followed by the Planning → Developing → Review cycle repeated while Review records Findings and progress continues, and reports every operation and reconciliation outcome in execution order without reading Agent Module sources.
