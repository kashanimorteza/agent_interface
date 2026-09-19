---
name: my-interface-reviewer
description: Assure selected Target phase implementations, or every enabled phase with existing implementation when none is specified, by independently comparing current Interface and Target Understanding against the Plan, implementation, and evidence, and recording every misalignment as a Finding naming its owning operation. Invokes no other Skill and repairs nothing. Only when explicitly requested by the Human or delegated by a declared Interface coordinator.
argument-hint: "[phase-number ...]"
metadata:
  contract: ".interface/agent/skill/contracts/reviewing.md"
  contract_sha256: "sha256:76814adb200b59d6ca8a9855e98a73405156892e328b9905c5520f0330fb4c6d"
  preferences: ".interface/agent/skill/preferences.yaml"
  preferences_sha256: "sha256:386052d88bf6225ecc6b2cc35f60fc2e7344a26bce478741efa86371fde6d566"
  synced_at: "2026-09-19T16:31:31Z"
---

# Review Target phases

This file is the self-contained Claude Code realization of the portable `reviewing` Skill Contract, placed here by Agent Sync as the Human authored it. Follow this file and the synchronized Runtime Rules under `.claude/rules/`; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-reviewer` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Purpose

Bring the selected phase's current understanding, Plan, implementation, and generated Source into alignment through independent review; reconciliation is performed by the owning operations, rerun by Implement or the Human.

## Responsibility

Reconstruct current Interface Understanding and Target Understanding; compare the current Plan, implementation, generated Source, and evidence with those authorities; and record every misalignment as a Finding owned by the Skill that must resolve it, so that the owning Skill reconciles it on its next run. Report whether the authorities and outputs are aligned or progress is blocked. Reviewing invokes no other Skill; the loop that reruns Planning, Developing, and Review belongs to Implement, or to the Human in the Detailed path. Reviewing records Findings and exact outcomes and never edits another operation's records or Source directly.

## Trigger

Activate explicitly for zero or more phase selections after an implementation exists, including after Development, a Component or Target change, or as a final convergence gate. Do not start Review for a phase with no implementation.

## Inputs

Accept zero or more phase positions. Empty input selects every enabled phase that has an implementation. Resolve positions to stable identifiers, deduplicate them, and process them in Target order. Consume current Interface Understanding, Target Understanding, applicable Implementation Principles and Preferences, synchronized Runtime rules, Plans, State, prior Review records, implementation, generated Source, public interfaces, and recorded evidence. Never read Agent Module sources.

Claude Code input handling: the positions arrive as whitespace-separated positive integers in `$ARGUMENTS` — `1` selects phase one, `2` phase two, and so on. Resolve every number against current Target phase order and use each phase's stable identifier throughout Review. If `$ARGUMENTS` is empty and no enabled phase has an implementation, make no changes and report that there is no implemented phase to review. If any token is not a positive integer resolving to an available phase, stop the complete run before observation: enumerate all available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without beginning Review.

## Outputs

Produce a separate Plan Assurance and Implementation Assurance outcome for every selected phase with an implementation, the exact Plan Revision assured, reconciled Review Findings, aggregate Review State and History, an obligation-coverage summary including the applicable `agent` parameters and how each was classified, and an evidence-first phase report. A phase without implementation is reported as not reviewable and receives no assurance outcome. Do not persist transient obligation ledgers, update Task progress directly, or change active Workflow mode.

## Required Understanding

Review establishes fresh Interface and Target Understanding on every invocation. It then compares the current authorities, Plan, implementation, generated Source, public boundaries, and evidence as one connected result. Review is one assurance pass: it assures the Plan, assures existing implementation when present, and records a Finding naming Configure, Planning, or Developing when a gap requires one of them. It invokes nothing and repeats nothing within its run; Implement reruns the owning operations and Review again until Review is satisfied, and in the Detailed path the Human does. Review never repairs another operation's records or Source directly and never starts implementation for a phase that has no implementation.

Reconstruct Interface Understanding and current Target Understanding on every invocation. Read Review, Plan, and State authorities and every Component applicable to each selected phase. Existing Plan, State, implementation, and Review records are evidence to assess and never substitutes for either Understanding.

Claude Code routes: establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, then Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Follow its routes to the Review, Plan, and State authorities, their Schemas and Config files, and the Implementation Components applicable to each selected phase. Never introduce a third `Project Understanding`.

## Authority

Observe and independently verify. Invoke no other Skill and execute no other Skill's instructions inline. Write only Review-owned Findings, assurance outcomes, aggregate Review State, and Review History. Never modify implementation, Target, Plan content, Task progress, or another operation's records directly.

## Workflow Invariants

- Validate all phase input before changing records or running verification.
- Before beginning any assurance for a phase, verify that implementation and generated Source exist.
- If they do not, stop Review for that phase and report that Developing or Implement must create the implementation first.
- For each selected phase, read the complete applicable authorities rather than relying on `At a Glance`, indexes, prior Findings, or other summaries.
- Build a complete obligation inventory containing every applicable normative Principle Rule and Boundary, every obligation represented as `Must`, every `Never` expressed as its prohibited condition, every resolved Preference with `requirement: required`, every conditional requirement whose activation condition is true, every applicable instruction of a required synchronized Skill, and every applicable Target requirement.
- Include in that inventory every applicable `agent` parameter: each `agent.consider` statement as a condition the work is expected to meet and each `agent.avoid` statement as a prohibited condition, gathered from the item worked on and every item above it, with the nearest parameter governing any point two of them speak to.
- Classify an `agent` parameter that an explicit Target statement or an applicable Principle overrides as `not applicable`, with that authority as its applicability reason, rather than as a Finding.
- For each assurance stage, classify every inventoried obligation exactly once as `satisfied`, `not applicable` with an explicit applicability reason, or `finding` with expected condition, actual observation, and evidence.
- For Plan Assurance, `satisfied` means the current Plan gives the obligation valid, observable coverage; for Implementation Assurance, it means current implementation and evidence prove the obligation.
- Never infer `not applicable` from silence, and never use it merely because a selected required technology, capability, implementation, or proof is absent.
- Rebuild the transient Plan Assurance ledger directly from that inventory and current authorities under the synchronized Runtime rules, then compare the current Plan against it for complete, non-duplicated, non-contradictory coverage, valid boundaries, acceptance, verification conditions, dependencies, and currentness.
- An omitted, unclassified, unsupported, or merely asserted obligation is a Plan Finding.
- If the Plan is absent or Plan Assurance is not satisfied, record the exact Plan Findings naming Planning as their owning operation and report that the phase cannot be assured until Planning has resolved them.
- Record the current positive Plan Revision with every Plan Assurance outcome.
- Never carry an outcome forward to a different revision; after Planning changes the revision, perform a new independent Plan Assurance pass and bind its result to that new revision.
- Report a Plan Finding that is unchanged since the previous Review record as repeated, so the coordinating loop can stop on no observable progress, inconclusive Plan Assurance, or a required Human decision.
- Do not begin Implementation Assurance until Plan Assurance is satisfied.
- When implementation exists, build a transient Implementation Assurance ledger covering the complete obligation inventory, every Plan acceptance clause, and every recorded verification condition.
- Observe each condition independently and judge whether the implementer's checks actually establish it.
- An omitted, unclassified, unsupported, or merely asserted obligation is an Implementation Finding or missing-evidence record, never a passing condition.
- Ground every Finding in the expected condition, actual observation, and exact location or observable result.
- Record absent Plan coverage as a Gap and absent observable proof as missing evidence.
- Reconcile prior Findings only through current observation.
- A Finding persists until Review proves it resolved or the Human accepts it.
- Complete one phase's assurance result before processing the next selected phase.
- A standalone Review may continue to later independent phases when one phase is unsatisfied or inconclusive; a coordinating Skill may impose a stricter stopping gate.
- When current authorities or evidence changed since the last assurance, do not carry forward a prior outcome merely because the Plan revision is unchanged; rebuild Understanding and reassess the affected phase.
- If Config is stale or invalid for the current phase, record a Finding naming Configure as its owning operation and withhold both assurances until Configure has resolved it.
- If the phase's technical Environment is insufficient, record a Finding naming Developing.
- If current authorities declare changed public metadata or Config structure, record a Finding naming Configure; if they declare changed Component paths, packages, versions, tools, or connections, record a Finding naming Developing; if they declare changed Platform requirements, record a Finding naming Launch.
- Do not assess the phase until the owning operation has resolved it.
- If Plan coverage is stale or incomplete, record a Finding owned by Planning; if implementation or generated Source no longer satisfies the current Plan, record a Finding owned by Developing.
- Every Review run starts from fresh Understanding and evidence and discards observations of earlier runs; a Finding recorded earlier is reconciled only through current observation.
- Report a blocker when a Finding repeats unchanged across runs, when evidence remains inconclusive, or when a decision requires Human judgment, so the coordinating loop stops instead of cycling.

Claude Code execution detail: the Plan Assurance ledger is built from the obligation inventory and current authorities, never derived from the Plan it will judge. Where practical, observe Implementation Assurance conditions with adversarial or independent cases rather than only the implementer's own checks.

## Verification

- Plan Assurance is `satisfied` only when the current Plan completely and correctly covers the current Interface and Target authorities and every applicable mandatory obligation has exactly one supported classification with no Finding.
- Implementation Assurance is `satisfied` only when existing implementation and evidence satisfy that assured Plan and the same current authorities and every applicable mandatory obligation has exactly one supported classification with no Finding.
- Aggregate outcome is `satisfied` when both applicable assurances pass, and otherwise the exact `not satisfied` or `inconclusive` result.
- A phase without implementation has no Review assurance outcome.
- Every conclusion must be traceable to current observable evidence; coverage counts alone never prove satisfaction.

## Idempotency

Repeated Review reconstructs both Understandings, preserves stable Findings and outcomes when sources and evidence are unchanged, records no new Finding for an already assured current Plan, and appends only History required by State.

## Stopping Conditions

- Stop the complete run before observation on invalid input.
- Stop an affected phase before Implementation Assurance when Plan Assurance cannot be satisfied.
- Mark an affected assurance inconclusive when required evidence cannot be observed or authorities conflict; never convert uncertainty into satisfaction, never invoke another Skill, and never directly edit another operation's records or implementation.

## Runtime Realization

A native adapter exposes optional multi-phase input, invokes no other Skill, and reports phase selection, both assurances, every Finding with its owning operation, missing evidence, convergence status, aggregate outcomes, and records changed.

In Claude Code this adapter invokes no Skill — not Configure, Planning, Developing, Implement, Launch, Reset, or the Agent Native Skill in any mode — and being invoked by a coordinator never changes that. It reports evidence first, in this order:

1. **Phases** — resolved phase identifiers, titles, targets, and order; phases without implementation reported as not reviewable.
2. **Plan Assurance** — result and the exact Plan Revision assured.
3. **Implementation Assurance** — conditions observed, independent evidence, and result.
4. **Findings and missing evidence** — grouped by phase and assurance stage, each naming its owning operation (Configure, Planning, Developing, or Launch), marked repeated when unchanged since the previous Review record, ordered by severity.
5. **Obligation coverage** — summary of the obligation inventory and its classification counts for the phase, including the applicable `agent` parameters and how each was classified.
6. **Convergence and recorded outcomes** — whether Findings repeated, advanced, or closed since the previous record, any blocker, Plan outcome, Implementation outcome, aggregate Review State, reconciled Findings, records changed, and History.
7. **Next step** — the single most useful next action supported by the result, naming the owning operation the Human or Implement must rerun before Review runs again.
