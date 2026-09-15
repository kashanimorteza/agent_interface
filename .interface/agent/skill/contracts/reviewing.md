# reviewing Skill Contract

## Purpose

Bring the selected phase's current understanding, Plan, implementation, and generated Source into alignment through independent review and owner-directed reconciliation.

## Responsibility

Reconstruct current Interface Understanding and Target Understanding; compare the current Plan, implementation, generated Source, and evidence with those authorities; and coordinate Configure, Planning, and Developing through their own Skills whenever reconciliation is required. Independently recheck every resulting state and continue until the current authorities and outputs are aligned or progress is blocked. Reviewing records Findings and exact outcomes and never edits another operation's records or Source directly.

## Trigger

Activate explicitly for zero or more phase selections after an implementation exists, including after Development, a Component or Target change, or as a final convergence gate. Do not start Review for a phase with no implementation.

## Inputs

Accept zero or more phase positions. Empty input selects every enabled phase that has an implementation. Resolve positions to stable identifiers, deduplicate them, and process them in Target order. Consume current Interface Understanding, Target Understanding, applicable Implementation Principles and Preferences, synchronized Runtime rules, Configure, Planning, and Developing capabilities, Plans, State, prior Review records, implementation, generated Source, public interfaces, and recorded evidence. Never read Agent Module sources.

## Outputs

Produce a separate Plan Assurance and Implementation Assurance outcome for every selected phase with an implementation, the exact Plan Revision assured, reconciled Review Findings, aggregate Review State and History, delegated Configure/Planning/Developing outcomes, an obligation-coverage summary, and an evidence-first phase report. A phase without implementation is reported as not reviewable and receives no assurance outcome. Do not persist transient obligation ledgers, update Task progress directly, or change active Workflow mode.

## Required Understanding

Reconstruct Interface Understanding and current Target Understanding on every invocation. Read Review, Plan, and State authorities and every Component applicable to each selected phase. Existing Plan, State, implementation, and Review records are evidence to assess and never substitutes for either Understanding.

## Authority

Observe and independently verify; invoke Configure when current requirements or Config readiness require reconciliation, Planning when the Plan requires reconciliation, and Developing when implementation or generated Source requires reconciliation. Write only Review-owned Findings, assurance outcomes, aggregate Review State, and Review History. Each invoked Skill retains authority over its own records and outputs. Never modify implementation, Target, Plan content, Task progress, or another operation's records directly.

## Workflow Invariants

- Validate all phase input before changing records, invoking Planning, or running verification.
- Before beginning any assurance or delegation for a phase, verify that implementation and generated Source exist. If they do not, stop Review for that phase and report that Developing or Implement must create the implementation first.
- For each selected phase, read the complete applicable authorities rather than relying on `At a Glance`, indexes, prior Findings, or other summaries. Build a complete obligation inventory containing every applicable normative Principle Rule and Boundary, every obligation represented as `Must`, every `Never` expressed as its prohibited condition, every resolved Preference with `requirement: required`, every conditional requirement whose activation condition is true, every applicable instruction of a required synchronized Skill, and every applicable Target requirement.
- For each assurance stage, classify every inventoried obligation exactly once as `satisfied`, `not applicable` with an explicit applicability reason, or `finding` with expected condition, actual observation, and evidence. For Plan Assurance, `satisfied` means the current Plan gives the obligation valid, observable coverage; for Implementation Assurance, it means current implementation and evidence prove the obligation. Never infer `not applicable` from silence, and never use it merely because a selected required technology, capability, implementation, or proof is absent.
- Rebuild the transient Plan Assurance ledger directly from that inventory and current authorities under the synchronized Runtime rules, then compare the current Plan against it for complete, non-duplicated, non-contradictory coverage, valid boundaries, acceptance, verification conditions, dependencies, and currentness. An omitted, unclassified, unsupported, or merely asserted obligation is a Plan Finding.
- If the Plan is absent or Plan Assurance is not satisfied, record the exact Plan Findings, invoke Planning for that phase, then discard prior Plan observations and independently rebuild and apply the Plan Assurance ledger to Planning's result.
- Record the current positive Plan Revision with every Plan Assurance outcome. Never carry an outcome forward to a different revision; after Planning changes the revision, perform a new independent Plan Assurance pass and bind its result to that new revision.
- Repeat Plan reconciliation only while a pass closes or materially advances a Plan Finding. Stop the affected phase on a repeated unresolved Finding, no observable progress, inconclusive Plan Assurance, or required Human decision.
- Do not begin Implementation Assurance until Plan Assurance is satisfied.
- When implementation exists, build a transient Implementation Assurance ledger covering the complete obligation inventory, every Plan acceptance clause, and every recorded verification condition. Observe each condition independently and judge whether the implementer's checks actually establish it. An omitted, unclassified, unsupported, or merely asserted obligation is an Implementation Finding or missing-evidence record, never a passing condition.
- Ground every Finding in the expected condition, actual observation, and exact location or observable result. Record absent Plan coverage as a Gap and absent observable proof as missing evidence.
- Reconcile prior Findings only through current observation. A Finding persists until Review proves it resolved or the Human accepts it.
- Complete one phase's assurance result before processing the next selected phase. A standalone Review may continue to later independent phases when one phase is unsatisfied or inconclusive; a coordinating Skill may impose a stricter stopping gate.
- When current authorities or evidence changed since the last assurance, do not carry forward a prior outcome merely because the Plan revision is unchanged; rebuild Understanding and reassess the affected phase.
- If Config or Environment readiness is stale or insufficient for the current phase, invoke Configure before Plan or Implementation Assurance.
- If current authorities declare changed Component paths, packages, versions, tools, public metadata, connections, or Platform requirements, treat the change as a Configure trigger and invoke Configure before reassessing the phase.
- If Plan coverage is stale or incomplete, invoke Planning; if implementation or generated Source no longer satisfies the reconciled Plan, invoke Developing through its own Contract.
- After every delegated reconciliation, discard prior observations and rerun the relevant assurance stages against fresh Understanding and evidence.
- Continue the reconciliation cycle only while it closes or materially advances a Finding. Stop and report a blocker when a cycle repeats, makes no observable progress, remains inconclusive, or requires Human judgment.

## Verification

Plan Assurance is `satisfied` only when the current Plan completely and correctly covers the current Interface and Target authorities and every applicable mandatory obligation has exactly one supported classification with no Finding. Implementation Assurance is `satisfied` only when existing implementation and evidence satisfy that assured Plan and the same current authorities and every applicable mandatory obligation has exactly one supported classification with no Finding. Aggregate outcome is `satisfied` when both applicable assurances pass, and otherwise the exact `not satisfied` or `inconclusive` result. A phase without implementation has no Review assurance outcome. Every conclusion must be traceable to current observable evidence; coverage counts alone never prove satisfaction.

## Idempotency

Repeated Review reconstructs both Understandings, preserves stable Findings and outcomes when sources and evidence are unchanged, avoids invoking Planning for an already assured current Plan, and appends only History required by State.

## Stopping Conditions

Stop the complete run before observation or delegation on invalid input. Stop an affected phase before Implementation Assurance when Plan Assurance cannot be satisfied. Mark an affected assurance inconclusive when required evidence cannot be observed or authorities conflict; never convert uncertainty into satisfaction or directly edit another operation's records or implementation.

## Runtime Realization

A native adapter exposes optional multi-phase input, resolves and invokes the current Configure, Planning, and Developing implementations directly when reconciliation is required, and reports phase selection, every delegated outcome, both assurances, Findings, missing evidence, convergence status, aggregate outcomes, and records changed.
