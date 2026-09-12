---
name: my-interface-reviewer
description: Assure selected Target phase Plans and any existing implementation, or every enabled phase when none is specified, against current Interface and Target Understanding. Coordinates Planning for Plan reconciliation, records Findings, and never repairs implementation.
argument-hint: "[phase-number ...]"
disable-model-invocation: true
---

# Review Target phases

This file is the Claude Code adapter for the portable `reviewing` Skill Contract. Resolve and read that Contract through Agent Skill Preferences before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Provide two independent gates for every selected phase:

1. **Plan Assurance** — establish that its Plan completely and correctly represents current Interface and Target Understanding.
2. **Implementation Assurance** — when implementation exists, establish that the result and evidence satisfy the assured Plan and the same current authorities.

An individual Review pass never changes what it judges. When Plan Assurance fails, invoke the current Planning Skill as the sole Plan owner, preserve the original Findings, and then perform a new independent Review pass. Never write Plan content directly and never invoke Development or repair Source.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve every number against current Target phase order and use each phase's stable identifier throughout Review.

If `$ARGUMENTS` is empty, select every phase whose current Target status marks it enabled. If no phase is enabled, make no changes and report that there is no phase to review.

If arguments are present, validate the complete selection before changing records, invoking Planning, or running verification. Every token must be a positive integer resolving to an available phase. Deduplicate repeated numbers and process selected phases in Target order regardless of argument order. For invalid input, enumerate all available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without beginning Review.

## Understanding

On every invocation, establish Interface Understanding from the canonical Interface document and follow its routes to the shared Skill rules and current Component authorities. Then establish Target Understanding from the Human and Technical Definitions it locates under their declared precedence.

Never introduce a third `Project Understanding`. Plan, State, Review Config, implementation, and earlier conversation are evidence to assess; none substitutes for current Interface Understanding or Target Understanding.

## Workflow

Resolve the current Planning Skill, Review, Plan and State authorities, applicable Component authorities, operational records, implementation, public interfaces, and verification capabilities.

Process each selected phase as follows:

1. Build a transient Plan Assurance ledger directly from current Target Understanding and every applicable Component obligation. Do not derive this ledger from the Plan it will judge.
2. Compare the current Plan with the ledger for complete and current coverage, coherent Task boundaries, dependencies, acceptance clauses, verification conditions, and absence of contradiction or duplication.
3. If the Plan is missing or not satisfied, record exact Plan Findings and invoke the current Planning Skill directly for this phase. Do not depend on nested Slash Command invocation.
4. After Planning, discard the previous Plan observations, rebuild the ledger from current authorities, and independently Review the reconciled Plan. Repeat only while a cycle closes or materially advances a Finding; stop on repetition, no progress, an inconclusive result, or a required Human decision.
5. Do not begin Implementation Assurance until Plan Assurance is `satisfied`.
6. Detect whether implementation or Development evidence exists. If neither exists, record Implementation Assurance as `not reviewed`, aggregate Review State as `plan satisfied`, and report that the phase is ready for Development.
7. If implementation exists, build a separate transient Implementation Assurance ledger from the assured Plan, current Target, applicable Component obligations, acceptance clauses, verification conditions, and recorded evidence.
8. Inspect Source, public interfaces, durable checks, and evidence. Observe each condition independently and judge whether the implementer's check establishes it; use adversarial or independent cases where practical.
9. Record Findings with expected condition, actual observation, and exact evidence. Missing Plan coverage is a Gap; missing proof is missing evidence. Reconcile previous Findings only through current observation.
10. Record aggregate Review State as `satisfied` only when both Plan Assurance and applicable Implementation Assurance are satisfied. Otherwise record the exact `plan satisfied`, `not satisfied`, or `inconclusive` result.

Complete one selected phase before moving to the next. In a standalone invocation, an unsatisfied phase does not prevent reviewing a later phase whose evidence is independent. A coordinator such as Implement may require the current phase to pass before advancing.

## Boundaries

Review writes only Review-owned Findings, assurance results, aggregate Review State, and Review History. Planning writes any Plan reconciliation under its own Contract. Do not modify Source, Target, Plan content directly, Task progress, or another operation's records. Do not invoke Developing.

## Report

Report in this order:

1. **Phases** — resolved phase identifiers, titles, targets, and order.
2. **Plan Assurance** — original result, Findings, any delegated Planning outcome, and independent post-Planning result.
3. **Implementation Assurance** — `not reviewed` when absent; otherwise conditions observed, independent evidence, and result.
4. **Findings and missing evidence** — grouped by phase and assurance stage, ordered by severity.
5. **Recorded outcomes** — Plan outcome, Implementation outcome, aggregate Review State, reconciled Findings, and History.
6. **Next step** — Development when only the Plan is satisfied, correction through Developing when implementation Findings remain, or the next eligible phase when both gates pass.
