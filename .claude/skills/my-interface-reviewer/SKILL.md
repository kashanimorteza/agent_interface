---
name: my-interface-reviewer
description: Assure selected Target phase implementations, or every enabled phase with existing implementation when none is specified, by independently reconciling current Interface and Target Understanding against the Plan, implementation, and evidence, recording every misalignment as a Finding naming its owning operation for Implement to route.
argument-hint: "[phase-number ...]"
---

# Review Target phases

This file is the self-contained Claude Code realization of the portable `reviewing` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-reviewer` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Role

Provide two independent gates for every selected phase with existing implementation:

1. **Plan Assurance** — establish that its Plan completely and correctly represents current Interface and Target Understanding.
2. **Implementation Assurance** — when implementation exists, establish that the result and evidence satisfy the assured Plan and the same current authorities.

An individual Review pass never edits what it judges. When current Config, Plan, or implementation is no longer aligned, record the exact Finding naming Configure, Planning, or Developing as the operation that owns its resolution, then invoke that Skill to reconcile it. Reviewing records Findings and exact outcomes and never edits another operation's records or Source directly.

Review may invoke only Configure, Planning, and Developing, and only to reconcile a Finding that Skill owns within the phase under review. Invoke each one with Claude Code's `Skill` tool, naming `my-interface-configure`, `my-interface-planning`, or `my-interface-developing`, so the invoked Skill loads and executes its own SKILL.md. Never read another Skill's SKILL.md and execute its workflow inline, and never delegate one to a forked or subordinate agent that inherits this Skill's context: neither runs that Skill's own definition, so neither is an invocation. Review never invokes Implement, Launch, Reset, Agent Sync, or Skill Installer.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve every number against current Target phase order and use each phase's stable identifier throughout Review.

If `$ARGUMENTS` is empty, select every enabled phase that has an existing implementation. If no such phase exists, make no changes and report that there is no implemented phase to review.

If arguments are present, validate the complete selection before changing records or running verification. Every token must be a positive integer resolving to an available phase. Deduplicate repeated numbers and process selected phases in Target order regardless of argument order. For invalid input, stop the complete run before observation: enumerate all available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without beginning Review.

## Understanding

On every invocation, establish Interface Understanding from the canonical Interface document and follow its authorized routes to synchronized Runtime rules and current Implementation Component authorities. Never enter or inspect the Agent Module. Then establish Target Understanding from the Human and Technical Definitions it locates under their declared precedence.

Never introduce a third `Project Understanding`. Plan, State, Review Config, implementation, and earlier conversation are evidence to assess; none substitutes for current Interface Understanding or Target Understanding.

## Workflow

Resolve the current synchronized Review, Plan, and State authorities, applicable Implementation Component authorities, operational records, implementation, generated Source, public interfaces, and Runtime verification capabilities. Resolve Configure, Planning, and Developing as invocable Runtime Skills, and resolve their records as evidence of reconciliation that has actually occurred.

Process each selected phase as follows. Before beginning assurance, verify that implementation and generated Source exist; if they do not, stop Review for that phase and report that Developing or Implement must create it first.

1. Build a complete obligation inventory for the phase by reading the complete applicable authorities rather than relying on `At a Glance`, indexes, prior Findings, or other summaries: every applicable normative Principle Rule and Boundary, every obligation expressed as `Must`, every `Never` expressed as its prohibited condition, every resolved Preference with `requirement: required`, every conditional requirement whose activation condition is true, every applicable instruction of a required synchronized Skill, and every applicable Target requirement.
2. Build a transient Plan Assurance ledger directly from that inventory and current Target Understanding — never derived from the Plan it will judge. Classify every inventoried obligation exactly once as `satisfied` (the current Plan gives it valid, observable coverage), `not applicable` with an explicit applicability reason, or `finding` with expected condition, actual observation, and evidence. Never infer `not applicable` from silence or merely because a required technology, capability, implementation, or proof is absent.
3. Compare the current Plan against the ledger for complete, non-duplicated, non-contradictory coverage, valid boundaries, acceptance clauses, verification conditions, dependencies, and currentness. An omitted, unclassified, unsupported, or merely asserted obligation is a Plan Finding, never a passing condition.
4. If the Plan is missing or Plan Assurance is not satisfied, record the exact Plan Findings naming Planning as their owning operation, and report that the phase cannot be assured until Implement routes them to Planning and Planning resolves them.
5. Repeat Plan reconciliation only while a pass closes or materially advances a Plan Finding — across separate Review invocations, after Implement has routed a Finding and Planning has acted on it. On each such invocation, discard prior Plan observations and rebuild the ledger from current authorities before reassessing. Stop the affected phase on a repeated unresolved Finding, no observable progress, inconclusive Plan Assurance, or required Human decision.
6. Record the exact positive `revision` of the Plan examined with the Plan Assurance outcome. Never reuse a Plan Assurance outcome after Planning changes that revision; perform a new independent pass bound to the new revision.
7. Do not begin Implementation Assurance until Plan Assurance is `satisfied` for that exact revision.
8. Build a separate transient Implementation Assurance ledger covering the complete obligation inventory, every Plan acceptance clause, and every recorded verification condition. Observe each condition independently and judge whether the implementer's check actually establishes it, using adversarial or independent cases where practical. An omitted, unclassified, unsupported, or merely asserted obligation is an Implementation Finding or a missing-evidence record, never a passing condition.
9. Record Findings with expected condition, actual observation, and exact evidence. Missing Plan coverage is a Gap; missing proof is missing evidence. Reconcile previous Findings only through current observation; a Finding persists until Review proves it resolved or the Human accepts it.
10. If current Config or Environment readiness is stale or insufficient for the current phase, record a Finding naming Configure as its owning operation and report that both assurances are withheld until Implement routes it to Configure and it is resolved.
11. If current authorities declare changed Component paths, packages, versions, tools, public metadata, connections, or Platform requirements, record a Finding naming Configure as its owning operation and report that the phase cannot be reassessed until it is resolved.
12. If implementation or generated Source no longer satisfies the assured Plan, record a Finding naming Developing as its owning operation and report that the phase cannot be assured until Implement routes it to Developing and Developing resolves it.
13. After each delegated reconciliation returns, confirm by fresh observation that it actually changed Config, Plan revision, or implementation, then discard prior observations and rerun the relevant assurance stages against fresh Understanding and evidence. A delegated Skill reporting success is not itself evidence of change.
14. Continue the reconciliation cycle only while it closes or materially advances a Finding across invocations. Stop and report a blocker when a cycle repeats, makes no observable progress, remains inconclusive, or requires Human judgment. Mark an affected assurance `inconclusive` when required evidence cannot be observed or authorities conflict; never convert uncertainty into satisfaction.
15. Record aggregate Review State as `satisfied` only when both Plan Assurance and Implementation Assurance are satisfied and every applicable mandatory obligation has exactly one supported classification with no Finding; coverage counts alone never prove satisfaction. Otherwise record the exact `not satisfied` or `inconclusive` result.

Complete one selected phase's assurance result before processing the next selected phase. In a standalone invocation, an unsatisfied phase does not prevent reviewing a later phase whose evidence is independent. A coordinator such as Implement may require the current phase to pass before advancing.

## Boundaries

Review observes and independently verifies, and reconciles only by invoking the Skill that owns a Finding. Being invoked by a coordinator never widens that set beyond Configure, Planning, and Developing. Review writes only Review-owned Findings, assurance outcomes, aggregate Review State, and Review History. Do not persist transient obligation ledgers, update Task progress directly, or change active Workflow mode. Configure, Planning, and Developing write their own records and outputs under their own Contracts; each retains authority over its own records and outputs. Do not modify Source, Target, Plan content, Task progress, or another operation's records directly.

## Report

Report in this order:

1. **Phases** — resolved phase identifiers, titles, targets, and order.
2. **Plan Assurance** — result and assured Plan Revision, Findings naming Planning where applicable, any delegated Planning outcome, and the independent result of each later pass bound to the new Plan Revision.
3. **Implementation Assurance** — skipped and reported when implementation is absent; otherwise conditions observed, independent evidence, and result.
4. **Findings and missing evidence** — grouped by phase and assurance stage, each naming its owning operation (Configure, Planning, or Developing), ordered by severity.
5. **Obligation coverage** — summary of the obligation inventory and its classification counts for the phase.
6. **Recorded outcomes** — Plan outcome, Implementation outcome, aggregate Review State, reconciled Findings, and History.
7. **Next step** — the owning operation Implement must route reconciliation to, another Review cycle, or the next eligible phase when both gates pass.
