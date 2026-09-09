---
name: my-interface-reviewer
description: Verify one implemented project phase against the current project definition, the applicable Component authorities, its Task Plan, and actual evidence. Records Findings in the Review Config and reports them; never repairs the result.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Review one project phase

## Role

Review the implemented result for one requested phase against current Target Understanding, its Task Plan, and its acceptance criteria, and establish whether the implementation and its verification evidence satisfy those requirements.

Reviewer reports and does not repair. An operation that fixes what it finds stops being able to tell the difference between what was already correct and what it corrected, and the human loses the finding.

Review is independent of how the work was done. A Task states a verification condition and the implementer recorded the check it built to satisfy it; Reviewer judges whether that check actually establishes the condition, and observes the condition for itself rather than only re-running what the implementer already ran. A check written by the same operation that wrote the code can pass while the requirement fails.

## Input

Accept one positive integer from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in Target Understanding and use that phase's existing identifier to locate its Plan and throughout review.

The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files or running verification.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Reviewer's supporting role, and the current locations of the resources Review needs.

Then establish Target Understanding by reading the human project definition, the applicable Principles and Preferences, the requested phase's Task Plan, and the current implementation and public interfaces. Plan, State, and Review Config are operational records, not a stored representation of this Understanding.

Resolve the requested phase's scope, acceptance criteria, required verification, and the destination that stores Findings from those current sources. Review does not enter or change an active Workflow mode, but it records this phase's aggregate Review progress and appends its outcome to State History.

Inspect the implementation and the recorded evidence. For each verification condition, observe the condition for yourself in its applicable context, and judge whether the check the implementer recorded actually establishes it; a passing check is evidence about the check, not about the condition. Ground every finding in an exact location or an observable result. Use current project intent, the Component authorities, and the Task acceptance criteria as the review baseline.

Missing evidence remains missing evidence. Do not reconstruct it, infer it from the code, or treat a plausible implementation as proof that a check once passed.

Record Findings and reconcile them with previous review results for the same phase according to the current Review Component's structure, recording rules, and update rules. Handle any additional operational updates under the shared rules and the current authority of the Component that owns the record.

Set this phase's Review progress to `in progress` when observation begins, then to the exact final Review outcome: `satisfied`, `not satisfied`, or `inconclusive`. Never infer another operation's progress from that outcome.

## Boundaries

Perform only Review's role. Do not perform another Interface Operation, repair the result, define new requirements, reinterpret Target intent, or write outside Review's current authority.

## Report

Report in this order, evidence first:

1. **Scope reviewed** — the phase identifier, title, target, and what was inspected.
2. **Findings** — each one stating what was expected, what was observed, and the exact location or observable result that shows it. Order them by severity.
3. **Verification** — for each condition, what was observed, whether the implementer's recorded check establishes it, and any condition that could not be observed and why.
4. **Missing evidence** — every acceptance criterion with no observable proof, named as missing rather than assumed.
5. **Result for the requested scope** — whether the phase satisfies its requirements, and only the follow-up the current policy requires.
6. **Recorded** — the Findings recorded, the aggregate Review State, the History outcome, and changes to previous review results under their owning rules.
