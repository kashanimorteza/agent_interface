---
name: my-interface-reviewer
description: Verify selected implemented project phases, or every enabled phase when none is specified, against the current project definition, applicable Component authorities, Task Plans, and actual evidence. Records Findings and never repairs results.
argument-hint: "[phase-number ...]"
disable-model-invocation: true
---

# Review project phases

This file is the Claude Code adapter for the portable `reviewing` Skill Contract. Resolve and read that Contract through Agent Skill Preferences before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Review the implemented results for the selected phases against current Target Understanding, their Task Plans, and their acceptance criteria, and establish whether the implementation and its verification evidence satisfy those requirements.

Reviewer reports and does not repair. An operation that fixes what it finds stops being able to tell the difference between what was already correct and what it corrected, and the human loses the finding.

Review is independent of how the work was done. A Task states a verification condition and the implementer recorded the check it built to satisfy it; Reviewer judges whether that check actually establishes the condition, and observes the condition for itself rather than only re-running what the implementer already ran. A check written by the same operation that wrote the code can pass while the requirement fails.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve every number against phase order in Target Understanding and use each phase's stable identifier throughout review.

The numbers are input conveniences; they never rename phases or change stored identifiers or references.

If `$ARGUMENTS` is empty, select every phase whose current Target status marks it enabled. If no phase is enabled, make no changes and report that there is no phase to review.

If arguments are present, validate the complete selection before changing files or running verification. Every token must be a positive integer that resolves to an available phase. Deduplicate repeated numbers and process selected phases in Target order regardless of argument order. If any token is invalid, enumerate all available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without beginning Review.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Reviewer's supporting role, and the current locations of the resources Review needs.

Then establish Target Understanding from the Human and Technical Definitions located by the Interface under their declared precedence, and read the applicable Principles and Preferences, each selected phase's Task Plan, and the current implementation and public interfaces. Plan, State, and Review Config are operational records, not a stored representation of this Understanding.

Resolve every selected phase's scope, acceptance criteria, required verification, and the destination that stores Findings from those current sources. Process phases in Target order. Review does not enter or change an active Workflow mode, but it records each phase's aggregate Review progress and appends each outcome to State History.

For each phase, build a transient review ledger that enumerates every requirement in the phase's Target definition, every applicable Component-authority obligation, every Plan acceptance clause, and every recorded verification condition. Use it to establish complete review coverage without storing a duplicate source of requirements. A missing Plan mapping is a Gap; a mapped condition without observable proof is missing evidence.

Inspect the implementation and the recorded evidence. For every item in the transient review ledger, observe the condition for yourself in its applicable context, and judge whether the check the implementer recorded actually establishes it. Use an independent observation or adversarial case where practical instead of relying only on the implementer's happy path; a passing check is evidence about the check, not about the condition. Ground every finding in an exact location or an observable result. Use current project intent, the Component authorities, and the Task acceptance criteria as the review baseline.

Missing evidence remains missing evidence. Do not reconstruct it, infer it from the code, or treat a plausible implementation as proof that a check once passed.

Record Findings and reconcile them with previous review results for each phase according to the current Review Component's structure, recording rules, and update rules. Handle any additional operational updates under the shared rules and the current authority of the Component that owns the record. An inconclusive or not-satisfied phase does not prevent reviewing later selected phases whose evidence can be observed independently.

Set each phase's Review progress to `in progress` when its observation begins, then to its exact final Review outcome: `satisfied`, `not satisfied`, or `inconclusive`. Never infer another operation's progress from that outcome.

## Boundaries

Perform only Review's role. Do not perform another Interface Operation, repair the result, define new requirements, reinterpret Target intent, or write outside Review's current authority.

## Report

Report in this order, evidence first:

1. **Scopes reviewed** — every phase identifier, title, target, and what was inspected, in Target order.
2. **Findings** — by phase, each one stating what was expected, what was observed, and the exact location or observable result that shows it. Order each phase's Findings by severity.
3. **Verification** — by phase and condition, what was observed, whether the implementer's recorded check establishes it, and any condition that could not be observed and why.
4. **Missing evidence** — by phase, every acceptance criterion with no observable proof, named as missing rather than assumed.
5. **Results for the requested scopes** — whether each phase satisfies its requirements, and only the follow-up the current policy requires.
6. **Recorded** — by phase, the Findings recorded, aggregate Review State, History outcome, and changes to previous review results under their owning rules.
