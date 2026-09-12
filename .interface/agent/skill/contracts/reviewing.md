# reviewing Skill Contract

## Purpose

Provide independent evidence-based assurance of current phase Plans and, when present, their implemented results.

## Responsibility

Reconstruct current Interface Understanding and Target Understanding; assure that each selected phase Plan completely and correctly represents them; coordinate Planning when a Plan is missing, stale, incomplete, or invalid; independently recheck the reconciled Plan; and judge existing implementation and evidence against the assured Plan and current authorities. Reviewing records Findings and exact outcomes. It never writes Plan content or repairs implementation.

## Trigger

Activate explicitly for zero or more phase selections, after Planning as a Plan gate, as an assessment of existing work, or as an independent final gate after Development.

## Inputs

Accept zero or more phase positions. Empty input selects every enabled phase. Resolve positions to stable identifiers, deduplicate them, and process them in Target order. Consume current Interface Understanding, Target Understanding, applicable Developer Principles and Preferences, Agent Principles and Profiles, Plans, State, prior Review records, implementation, public interfaces, and recorded evidence.

## Outputs

Produce a separate Plan Assurance and Implementation Assurance outcome for every selected phase, the exact Plan Revision assured, reconciled Review Findings, aggregate Review State and History, missing-evidence records, delegated Planning outcomes, and an evidence-first phase report. When no implementation exists, record Implementation Assurance as `not reviewed` and aggregate Review State as `plan satisfied` only when Plan Assurance passes. Do not update Task progress or active Workflow mode.

## Required Understanding

Reconstruct Interface Understanding and current Target Understanding on every invocation. Read Review, Plan, and State authorities and every Component applicable to each selected phase. Existing Plan, State, implementation, and Review records are evidence to assess and never substitutes for either Understanding.

## Authority

Observe and execute non-repairing verification; invoke the current Planning Skill for the same selected phase when Plan reconciliation is required; and write only Review-owned Findings, assurance outcomes, aggregate Review State, and Review History. Planning retains all authority over Plan content. Never modify implementation, Target, Plan content directly, Task progress, or another operation's records, and never invoke Development.

## Workflow Invariants

- Validate all phase input before changing records, invoking Planning, or running verification.
- For each selected phase, rebuild a transient Plan Assurance ledger directly from current Target Understanding and applicable Developer Principles and Preferences together with Agent Principles and Profiles, then compare the current Plan against it for complete, non-duplicated, non-contradictory coverage, valid boundaries, acceptance, verification conditions, dependencies, and currentness.
- If the Plan is absent or Plan Assurance is not satisfied, record the exact Plan Findings, invoke Planning for that phase, then discard prior Plan observations and independently rebuild and apply the Plan Assurance ledger to Planning's result.
- Record the current positive Plan Revision with every Plan Assurance outcome. Never carry an outcome forward to a different revision; after Planning changes the revision, perform a new independent Plan Assurance pass and bind its result to that new revision.
- Repeat Plan reconciliation only while a pass closes or materially advances a Plan Finding. Stop the affected phase on a repeated unresolved Finding, no observable progress, inconclusive Plan Assurance, or required Human decision.
- Do not begin Implementation Assurance until Plan Assurance is satisfied.
- When no implementation or Development evidence exists, record Implementation Assurance as `not reviewed`; never manufacture a defect or proof for work that has not begun.
- When implementation exists, build a transient Implementation Assurance ledger covering every Target requirement, applicable Component obligation, Plan acceptance clause, and recorded verification condition. Observe each condition independently and judge whether the implementer's checks actually establish it.
- Ground every Finding in the expected condition, actual observation, and exact location or observable result. Record absent Plan coverage as a Gap and absent observable proof as missing evidence.
- Reconcile prior Findings only through current observation. A Finding persists until Review proves it resolved or the Human accepts it.
- Complete one phase's assurance result before processing the next selected phase. A standalone Review may continue to later independent phases when one phase is unsatisfied or inconclusive; a coordinating Skill may impose a stricter stopping gate.

## Verification

Plan Assurance is `satisfied` only when the current Plan completely and correctly covers the current Interface and Target authorities. Implementation Assurance is `satisfied` only when existing implementation and evidence satisfy that assured Plan and the same current authorities. Aggregate outcome is `plan satisfied` when only Plan Assurance applies, `satisfied` when both applicable assurances pass, and otherwise the exact `not satisfied` or `inconclusive` result. Every conclusion must be traceable to current observable evidence.

## Idempotency

Repeated Review reconstructs both Understandings, preserves stable Findings and outcomes when sources and evidence are unchanged, avoids invoking Planning for an already assured current Plan, and appends only History required by State.

## Stopping Conditions

Stop the complete run before observation or delegation on invalid input. Stop an affected phase before Implementation Assurance when Plan Assurance cannot be satisfied. Mark an affected assurance inconclusive when required evidence cannot be observed or authorities conflict; never convert uncertainty into satisfaction, direct Plan editing, or an implementation repair.

## Runtime Realization

A native adapter exposes optional multi-phase input, resolves and invokes the current Planning implementation directly when Plan reconciliation is required, uses read and verification capabilities without Development authority, and reports phase selection, Plan Assurance, delegated Planning, Implementation Assurance, Findings, missing evidence, aggregate outcomes, and records changed.
