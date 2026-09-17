---
name: my-interface-reviewer
description: Assure selected Target phase implementations, or every enabled phase with existing implementation when none is specified, by independently comparing current Interface and Target Understanding against the Plan, implementation, and evidence, and recording every misalignment as a Finding naming its owning operation. Invokes no other Skill and repairs nothing. Only when explicitly requested by the Human or delegated by a declared Interface coordinator.
argument-hint: "[phase-number ...]"
metadata:
  contract: ".interface/agent/skill/contracts/reviewing.md"
  contract_sha256: "sha256:ba7419e6361a9048af74e345a7a6bcde662ee4c0b3c2eebfbe39d240d4288ef1"
  synced_at: "2026-09-17T18:39:11Z"
---

# Review Target phases

This file is the self-contained Claude Code realization of the portable `reviewing` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-reviewer` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

Activate for zero or more phase selections after an implementation exists, including after Development, after a Component or Target change, or as a final convergence gate. Never start Review for a phase with no implementation.

## Role

Bring each selected phase's current Understanding, Plan, implementation, and generated Source into alignment through independent review. Provide two independent gates for every selected phase with existing implementation:

1. **Plan Assurance** — establish that its Plan completely and correctly represents current Interface and Target Understanding.
2. **Implementation Assurance** — establish that the implementation and evidence satisfy the assured Plan and the same current authorities.

Review is one assurance pass. It records every misalignment as a Finding owned by the operation that must resolve it — Configure, Planning, or Developing — so that the owning Skill reconciles it on its next run, and it reports whether the authorities and outputs are aligned or progress is blocked. Review invokes no other Skill, executes no other Skill's instructions inline, and repeats nothing within its own run: the loop that reruns Planning, Developing, and Review belongs to Implement, or to the Human in the Detailed path. Review never edits what it judges, never repairs another operation's records or Source, and never starts implementation for a phase that has none.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve every number against current Target phase order and use each phase's stable identifier throughout Review.

If `$ARGUMENTS` is empty, select every enabled phase that has an existing implementation. If no such phase exists, make no changes and report that there is no implemented phase to review.

If arguments are present, validate the complete selection before changing records or running verification. Every token must be a positive integer resolving to an available phase. Deduplicate repeated numbers and process selected phases in Target order regardless of argument order. For invalid input, stop the complete run before observation: enumerate all available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without beginning Review.

## Understanding

On every invocation, establish fresh Interface Understanding from the canonical Interface document and follow its authorized routes to synchronized Runtime rules and current Implementation Component authorities. Never enter or inspect the Agent Module. Then establish Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Read the Review, Plan, and State authorities and every Component applicable to each selected phase.

Every Review run starts from fresh Understanding and evidence and discards the observations of earlier runs. Never introduce a third `Project Understanding`. Plan, State, Review Config, implementation, prior Review records, and earlier conversation are evidence to assess; none substitutes for current Interface Understanding or Target Understanding.

## Workflow

Resolve the current Review, Plan, and State authorities and Schemas, every Implementation Component applicable to each selected phase, operational records, implementation, generated Source, public interfaces, recorded evidence, and Runtime verification capabilities. Compare the current authorities, Plan, implementation, generated Source, public boundaries, and evidence as one connected result.

Process each selected phase as follows, completing one phase's assurance result before processing the next.

1. Before any assurance, verify that implementation and generated Source exist. If they do not, stop Review for that phase, record no assurance outcome, and report that it is not reviewable until Developing or Implement creates the implementation.
2. Build a complete obligation inventory for the phase by reading the complete applicable authorities rather than relying on `At a Glance`, indexes, prior Findings, or other summaries: every applicable normative Principle Rule and Boundary, every obligation expressed as `Must`, every `Never` expressed as its prohibited condition, every resolved Preference with `requirement: required`, every conditional requirement whose activation condition is true, every applicable instruction of a required synchronized Skill, and every applicable Target requirement.
3. If Config or Environment readiness is stale or insufficient for the phase, or current authorities declare changed Component paths, packages, versions, tools, public metadata, connections, or Platform requirements, record a Finding naming Configure as its owning operation, withhold both assurances, and do not assess the phase until Configure has resolved it.
4. Build a transient Plan Assurance ledger directly from that inventory and current authorities under the synchronized Runtime rules — never derived from the Plan it will judge. Classify every inventoried obligation exactly once as `satisfied` (the current Plan gives it valid, observable coverage), `not applicable` with an explicit applicability reason, or `finding` with expected condition, actual observation, and evidence. Never infer `not applicable` from silence or merely because a selected required technology, capability, implementation, or proof is absent.
5. Compare the current Plan against the ledger for complete, non-duplicated, non-contradictory coverage, valid boundaries, acceptance clauses, verification conditions, dependencies, and currentness. An omitted, unclassified, unsupported, or merely asserted obligation is a Plan Finding, never a passing condition.
6. If the Plan is absent, stale, incomplete, or Plan Assurance is otherwise not satisfied, record the exact Plan Findings naming Planning as their owning operation and report that the phase cannot be assured until Planning has resolved them.
7. Record the exact positive Plan `revision` examined with every Plan Assurance outcome. Never carry an outcome forward to a different revision; after Planning changes the revision, a later Review run performs a new independent Plan Assurance pass bound to that new revision. When current authorities or evidence changed since the last assurance, do not carry forward a prior outcome merely because the revision is unchanged; rebuild Understanding and reassess.
8. Report a Plan Finding that is unchanged since the previous Review record as repeated, so the coordinating loop can stop on no observable progress, inconclusive Plan Assurance, or a required Human decision.
9. Do not begin Implementation Assurance until Plan Assurance is `satisfied` for that exact revision.
10. Build a separate transient Implementation Assurance ledger covering the complete obligation inventory, every Plan acceptance clause, and every recorded verification condition. Classify every obligation exactly once, where `satisfied` means current implementation and evidence prove it. Observe each condition independently and judge whether the implementer's check actually establishes it, using adversarial or independent cases where practical. An omitted, unclassified, unsupported, or merely asserted obligation is an Implementation Finding or a missing-evidence record, never a passing condition.
11. If implementation or generated Source no longer satisfies the assured Plan, record a Finding naming Developing as its owning operation and report that the phase cannot be assured until Developing has resolved it.
12. Ground every Finding in the expected condition, actual observation, and exact location or observable result. Record absent Plan coverage as a Gap and absent observable proof as missing evidence. Reconcile prior Findings only through current observation; a Finding persists until Review proves it resolved or the Human accepts it.
13. Report a blocker when a Finding repeats unchanged across runs, when evidence remains inconclusive, or when a decision requires Human judgment, so the coordinating loop stops instead of cycling. Mark an affected assurance `inconclusive` when required evidence cannot be observed or authorities conflict; never convert uncertainty into satisfaction.
14. Record aggregate Review State as `satisfied` only when both Plan Assurance and Implementation Assurance are satisfied and every applicable mandatory obligation has exactly one supported classification with no Finding; coverage counts alone never prove satisfaction. Otherwise record the exact `not satisfied` or `inconclusive` result. Every conclusion must be traceable to current observable evidence.

In a standalone invocation, an unsatisfied or inconclusive phase does not prevent reviewing a later phase whose evidence is independent. A coordinator such as Implement may impose a stricter stopping gate.

Repeated Review reconstructs both Understandings, preserves stable Findings and outcomes when sources and evidence are unchanged, records no new Finding for an already assured current Plan, and appends only the History required by State.

## Stopping conditions

Stop the complete run before observation on invalid input. Stop an affected phase before Implementation Assurance when Plan Assurance cannot be satisfied. Mark an affected assurance inconclusive when required evidence cannot be observed or authorities conflict. Never invoke another Skill, and never directly edit another operation's records or implementation.

## Boundaries

Review observes and independently verifies. It invokes no other Skill — not Configure, Planning, Developing, Implement, Launch, Reset, or the Agent Native Skill in any mode — and being invoked by a coordinator never changes that. Review writes only Review-owned Findings, assurance outcomes, aggregate Review State, and Review History. Do not persist transient obligation ledgers, update Task progress directly, or change active Workflow mode. Do not modify implementation, Source, Target, Plan content, Task progress, or another operation's records directly. Configure, Planning, and Developing reconcile the Findings they own on their own next run, invoked by Implement or the Human.

## Report

Report evidence first, in this order:

1. **Phases** — resolved phase identifiers, titles, targets, and order; phases without implementation reported as not reviewable.
2. **Plan Assurance** — result and the exact Plan Revision assured.
3. **Implementation Assurance** — conditions observed, independent evidence, and result.
4. **Findings and missing evidence** — grouped by phase and assurance stage, each naming its owning operation (Configure, Planning, or Developing), marked repeated when unchanged since the previous Review record, ordered by severity.
5. **Obligation coverage** — summary of the obligation inventory and its classification counts for the phase.
6. **Convergence and recorded outcomes** — whether Findings repeated, advanced, or closed since the previous record, any blocker, Plan outcome, Implementation outcome, aggregate Review State, reconciled Findings, records changed, and History.
7. **Next step** — the single most useful next action supported by the result, naming the owning operation the Human or Implement must rerun before Review runs again.
