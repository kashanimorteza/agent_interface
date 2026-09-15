---
name: my-interface-reviewer
description: Assure selected Target phase implementations, or every enabled phase with existing implementation when none is specified, and coordinate owner Skills to reconcile changed work until current authorities and generated outputs converge.
argument-hint: "[phase-number ...]"
disable-model-invocation: true
---

# Review Target phases

This file is the self-contained Claude Code realization of the portable `reviewing` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Role

Provide two independent gates and a convergence cycle for every selected phase:

1. **Plan Assurance** — establish that its Plan completely and correctly represents current Interface and Target Understanding.
2. **Implementation Assurance** — when implementation exists, establish that the result and evidence satisfy the assured Plan and the same current authorities.

An individual Review pass never edits what it judges. When current Config, Plan, or implementation is no longer aligned, invoke Configure, Planning, or Developing through its owning Skill, preserve the original Findings, and then perform a new independent Review pass. Never write another operation's content directly.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve every number against current Target phase order and use each phase's stable identifier throughout Review.

If `$ARGUMENTS` is empty, select every enabled phase that has an existing implementation. If no such phase exists, make no changes and report that there is no implemented phase to review.

If arguments are present, validate the complete selection before changing records, invoking Planning, or running verification. Every token must be a positive integer resolving to an available phase. Deduplicate repeated numbers and process selected phases in Target order regardless of argument order. For invalid input, enumerate all available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without beginning Review.

## Understanding

On every invocation, establish Interface Understanding from the canonical Interface document and follow its authorized routes to synchronized Runtime rules and current Implementation Component authorities. Never enter or inspect the Agent Module. Then establish Target Understanding from the Human and Technical Definitions it locates under their declared precedence.

Never introduce a third `Project Understanding`. Plan, State, Review Config, implementation, and earlier conversation are evidence to assess; none substitutes for current Interface Understanding or Target Understanding.

## Workflow

Resolve the current synchronized Configure, Planning, Developing, Review, Plan and State authorities, applicable Implementation Component authorities, operational records, implementation, generated Source, public interfaces, and Runtime verification capabilities.

Process each selected phase as follows. Before beginning assurance or delegation, verify that implementation and generated Source exist; if they do not, skip the phase and report that Developing or Implement must create it first.

1. Build a transient Plan Assurance ledger directly from current Target Understanding and every applicable Component obligation. Do not derive this ledger from the Plan it will judge.
2. Compare the current Plan with the ledger for complete and current coverage, coherent Task boundaries, dependencies, acceptance clauses, verification conditions, and absence of contradiction or duplication.
3. If the Plan is missing or not satisfied, record exact Plan Findings and invoke the current Planning Skill directly for this phase. Do not depend on nested Slash Command invocation.
4. After Planning, discard the previous Plan observations, rebuild the ledger from current authorities, and independently Review the reconciled Plan. Repeat only while a cycle closes or materially advances a Finding; stop on repetition, no progress, an inconclusive result, or a required Human decision.
5. Record the exact positive `revision` of the Plan examined with the Plan Assurance outcome. Never reuse Plan Assurance after Planning changes that revision.
6. Do not begin Implementation Assurance until Plan Assurance is `satisfied` for that exact revision.
7. Build a separate transient Implementation Assurance ledger from the assured Plan, current Target, applicable Component obligations, acceptance clauses, verification conditions, and recorded evidence.
8. Inspect Source, public interfaces, durable checks, and evidence. Observe each condition independently and judge whether the implementer's check establishes it; use adversarial or independent cases where practical.
9. Record Findings with expected condition, actual observation, and exact evidence. Missing Plan coverage is a Gap; missing proof is missing evidence. Reconcile previous Findings only through current observation.
10. If current Config or Environment readiness is insufficient, invoke Configure and restart assurance from fresh observations.
11. If current authorities declare changed Component paths, packages, versions, tools, public metadata, connections, or Platform requirements, invoke Configure and restart assurance from fresh observations.
12. If implementation or generated Source no longer satisfies the assured Plan, invoke Developing through its own Contract, discard prior observations, and restart assurance.
13. Continue reconciliation only while a cycle closes or materially advances a Finding. Stop and report a blocker on repetition, no observable progress, inconclusive evidence, or required Human judgment.
14. Record aggregate Review State as `satisfied` only when both Plan Assurance and Implementation Assurance are satisfied. Otherwise record the exact `not satisfied` or `inconclusive` result.

Complete one selected phase before moving to the next. In a standalone invocation, an unsatisfied phase does not prevent reviewing a later phase whose evidence is independent. A coordinator such as Implement may require the current phase to pass before advancing.

## Boundaries

Review writes only Review-owned Findings, assurance results, aggregate Review State, and Review History. Configure, Planning, and Developing write their own records and outputs under their Contracts. Do not modify Source, Target, Plan content, Task progress, or another operation's records directly.

## Report

Report in this order:

1. **Phases** — resolved phase identifiers, titles, targets, and order.
2. **Plan Assurance** — original result and assured Plan Revision, Findings, any delegated Planning outcome, and independent post-Planning result with its revision.
3. **Implementation Assurance** — skipped and reported when implementation is absent; otherwise conditions observed, independent evidence, and result.
4. **Findings and missing evidence** — grouped by phase and assurance stage, ordered by severity.
5. **Recorded outcomes** — Plan outcome, Implementation outcome, aggregate Review State, reconciled Findings, and History.
6. **Next step** — the required owner Skill for reconciliation, another Review cycle, or the next eligible phase when both gates pass.
