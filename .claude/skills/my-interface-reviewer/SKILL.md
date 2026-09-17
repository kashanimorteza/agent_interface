---
name: my-interface-reviewer
description: Assure selected Target phase implementations, or every enabled phase with existing implementation when none is specified, by independently reconciling current Interface and Target Understanding against the Plan, implementation, and evidence, recording every misalignment as a Finding naming its owning operation and invoking Configure, Planning, or Developing to reconcile it, when explicitly requested by the Human or delegated by a declared Interface coordinator.
argument-hint: "[phase-number ...]"
metadata:
  contract: ".interface/agent/skill/contracts/reviewing.md"
  contract_sha256: "sha256:85b34a45d7d2fc68e2464297a59fbd3dcf598cfeada3b480284ee4aaa586cc0e"
  synced_at: "2026-09-17T12:48:12Z"
---

# Review Target phases

This file is the self-contained Claude Code realization of the portable `reviewing` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-reviewer` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Role

Bring each selected phase's current Understanding, Plan, implementation, and generated Source into alignment through independent review and owner-directed reconciliation. Provide two independent gates for every selected phase with existing implementation:

1. **Plan Assurance** — establish that its Plan completely and correctly represents current Interface and Target Understanding.
2. **Implementation Assurance** — establish that the implementation and evidence satisfy the assured Plan and the same current authorities.

Review never edits what it judges. When current Config, Plan, or implementation is no longer aligned, record the exact Finding naming Configure, Planning, or Developing as the operation that owns its resolution, then invoke that Skill to reconcile it, and independently recheck the result. Reviewing records Findings and exact outcomes and never edits another operation's records or Source directly.

Review may invoke only Configure, Planning, and Developing, and only to reconcile a Finding that Skill owns within the phase under review; Configure may additionally reconcile project-wide Config or Environment prerequisites. Invoke each one with Claude Code's `Skill` tool, naming `my-interface-configure`, `my-interface-planning`, or `my-interface-developing`, so the invoked Skill loads and executes its own SKILL.md. Never read another Skill's SKILL.md and execute its workflow inline, and never delegate one to a forked or subordinate agent that inherits this Skill's context: neither runs that Skill's own definition, so neither is an invocation. Review never invokes Implement, Launch, Reset, Agent Sync, or Skill Installer. Each invoked Skill retains authority over its own records and outputs.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve every number against current Target phase order and use each phase's stable identifier throughout Review.

If `$ARGUMENTS` is empty, select every enabled phase that has an existing implementation. If no such phase exists, make no changes and report that there is no implemented phase to review.

If arguments are present, validate the complete selection before changing records, invoking another Skill, or running verification. Every token must be a positive integer resolving to an available phase. Deduplicate repeated numbers and process selected phases in Target order regardless of argument order. For invalid input, stop the complete run before observation or delegation: enumerate all available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without beginning Review.

## Understanding

On every invocation, establish fresh Interface Understanding from the canonical Interface document and follow its authorized routes to synchronized Runtime rules and current Implementation Component authorities. Never enter or inspect the Agent Module. Then establish Target Understanding from the Human and Technical Definitions it locates under their declared precedence.

Never introduce a third `Project Understanding`. Plan, State, Review Config, implementation, prior Review records, and earlier conversation are evidence to assess; none substitutes for current Interface Understanding or Target Understanding.

## Workflow

Resolve the current Review, Plan, and State authorities and Schemas, every Implementation Component applicable to each selected phase, operational records, implementation, generated Source, public interfaces, recorded evidence, and Runtime verification capabilities. Resolve Configure, Planning, and Developing as invocable Runtime Skills, and treat their records only as evidence of reconciliation that has actually occurred.

Process each selected phase as follows, completing one phase's assurance result before processing the next.

1. Before any assurance or delegation, verify that implementation and generated Source exist. If they do not, stop Review for that phase, record no assurance outcome, and report that it is not reviewable until Developing or Implement creates the implementation.
2. Build a complete obligation inventory for the phase by reading the complete applicable authorities rather than relying on `At a Glance`, indexes, prior Findings, or other summaries: every applicable normative Principle Rule and Boundary, every obligation expressed as `Must`, every `Never` expressed as its prohibited condition, every resolved Preference with `requirement: required`, every conditional requirement whose activation condition is true, every applicable instruction of a required synchronized Skill, and every applicable Target requirement.
3. If Config or Environment readiness is stale or insufficient for the phase, or current authorities declare changed Component paths, packages, versions, tools, public metadata, connections, or Platform requirements, record a Finding naming Configure as its owning operation, invoke `my-interface-configure` to reconcile it, and withhold both assurances and do not reassess the phase until it is resolved.
4. Build a transient Plan Assurance ledger directly from that inventory and current authorities under the synchronized Runtime rules — never derived from the Plan it will judge. Classify every inventoried obligation exactly once as `satisfied` (the current Plan gives it valid, observable coverage), `not applicable` with an explicit applicability reason, or `finding` with expected condition, actual observation, and evidence. Never infer `not applicable` from silence or merely because a selected required technology, capability, implementation, or proof is absent.
5. Compare the current Plan against the ledger for complete, non-duplicated, non-contradictory coverage, valid boundaries, acceptance clauses, verification conditions, dependencies, and currentness. An omitted, unclassified, unsupported, or merely asserted obligation is a Plan Finding, never a passing condition.
6. If the Plan is absent or Plan Assurance is not satisfied, record the exact Plan Findings naming Planning as their owning operation, invoke `my-interface-planning` for this phase to reconcile them, and report that the phase cannot be assured until they are resolved. Do not invoke Planning when the current Plan is already assured and nothing it depends on changed.
7. Record the exact positive Plan `revision` examined with every Plan Assurance outcome. Never carry an outcome forward to a different revision; after Planning changes the revision, perform a new independent Plan Assurance pass bound to that new revision. When current authorities or evidence changed since the last assurance, do not carry forward a prior outcome merely because the revision is unchanged; rebuild Understanding and reassess.
8. Repeat Plan reconciliation only while a pass closes or materially advances a Plan Finding. Stop the affected phase on a repeated unresolved Finding, no observable progress, inconclusive Plan Assurance, or a required Human decision.
9. Do not begin Implementation Assurance until Plan Assurance is `satisfied` for that exact revision.
10. Build a separate transient Implementation Assurance ledger covering the complete obligation inventory, every Plan acceptance clause, and every recorded verification condition. Observe each condition independently and judge whether the implementer's check actually establishes it, using adversarial or independent cases where practical. An omitted, unclassified, unsupported, or merely asserted obligation is an Implementation Finding or a missing-evidence record, never a passing condition.
11. If implementation or generated Source no longer satisfies the assured Plan, record a Finding naming Developing as its owning operation, invoke `my-interface-developing` for this phase to reconcile it, and report that the phase cannot be assured until it is resolved.
12. Ground every Finding in the expected condition, actual observation, and exact location or observable result. Record absent Plan coverage as a Gap and absent observable proof as missing evidence. Reconcile prior Findings only through current observation; a Finding persists until Review proves it resolved or the Human accepts it.
13. After every delegated reconciliation returns, confirm by fresh observation that it actually changed Config, Plan revision, or implementation — a delegated Skill reporting success is not itself evidence of change — then discard prior observations and rerun the relevant assurance stages against fresh Understanding and evidence.
14. Continue the reconciliation cycle only while it closes or materially advances a Finding. Stop and report a blocker when a cycle repeats, makes no observable progress, remains inconclusive, or requires Human judgment. Mark an affected assurance `inconclusive` when required evidence cannot be observed or authorities conflict; never convert uncertainty into satisfaction.
15. Record aggregate Review State as `satisfied` only when both Plan Assurance and Implementation Assurance are satisfied and every applicable mandatory obligation has exactly one supported classification with no Finding; coverage counts alone never prove satisfaction. Otherwise record the exact `not satisfied` or `inconclusive` result.

In a standalone invocation, an unsatisfied or inconclusive phase does not prevent reviewing a later phase whose evidence is independent. A coordinator such as Implement may impose a stricter stopping gate.

Repeated Review reconstructs both Understandings, preserves stable Findings and outcomes when sources and evidence are unchanged, avoids invoking Planning for an already assured current Plan, and appends only the History required by State.

## Boundaries

Review observes and independently verifies, and reconciles only by invoking the Skill that owns a Finding. Being invoked by a coordinator never widens that set beyond Configure, Planning, and Developing. Review writes only Review-owned Findings, assurance outcomes, aggregate Review State, and Review History. Do not persist transient obligation ledgers, update Task progress directly, or change active Workflow mode. Configure, Planning, and Developing write their own records and outputs under their own Contracts. Do not modify implementation, Source, Target, Plan content, Task progress, or another operation's records directly.

## Report

Report in this order:

1. **Phases** — resolved phase identifiers, titles, targets, and order; phases without implementation reported as not reviewable.
2. **Plan Assurance** — result and assured Plan Revision, Findings naming Planning where applicable, the delegated Planning outcome, and the independent result of each later pass bound to the new Plan Revision.
3. **Implementation Assurance** — conditions observed, independent evidence, result, and the delegated Developing outcome when one ran.
4. **Configure reconciliation** — Findings naming Configure and the delegated Configure outcome, when any.
5. **Findings and missing evidence** — grouped by phase and assurance stage, each naming its owning operation (Configure, Planning, or Developing), ordered by severity.
6. **Obligation coverage** — summary of the obligation inventory and its classification counts for the phase.
7. **Convergence and recorded outcomes** — convergence status of the reconciliation cycle, Plan outcome, Implementation outcome, aggregate Review State, reconciled Findings, records changed, and History.
8. **Next step** — the single most useful next action supported by the result.
