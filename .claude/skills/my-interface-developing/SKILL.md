---
name: my-interface-developing
description: Execute and verify eligible planned work for one requested project phase, using the current project definition, the applicable Component authorities, and the phase's Task Plan. Never plans or reviews.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Develop one project phase

## Role

Implement and verify eligible planned work for one requested project phase, using current Target Understanding and the Task Plan as the specification.

Developing owns the implementation method and the arrangement of the source. The Plan says what must be achieved and what proves it; deciding how is this operation's work, and a Plan that already decided it would be describing code that does not exist yet.

Developing also builds the check that proves each result, because only the operation that made the result knows how to observe it. Build that check from the verification condition the Task states, not from the implementation just written: a check shaped around the code will pass whatever the code happens to do, and prove nothing about what was asked for.

Developing may write implementation and install and configure the prerequisites required by the authorized work, within the scope and write boundaries established by the Plan and the current Component authorities.

## Input

Accept one phase identifier from `$ARGUMENTS`, such as `P1`. Resolve it directly against the stable phase identifiers in Target Understanding and use that identifier to locate its current planning output and throughout development.

The identifier is matched exactly and never interpreted as an ordinal position. If it is missing, invalid, or does not uniquely select an existing phase, request a valid phase identifier before changing any files.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Developing's place in the Workflow, and the current locations of the resources Development needs.

Then establish Target Understanding by reading the human project definition, the Principles and Preferences applicable to the requested phase and its target Component, and the existing implementation and public interfaces. Plan and State Config are operational records, not a stored representation of this Understanding: a Task states an activity, and the technical context it needs is resolved from the Preferences at this moment rather than read back from the record.

Read the requested phase's current Task Plan and State. Derive work selection, ordering, eligibility, progress updates, evidence handling, validation, ownership, and write boundaries from the current Component authorities. Do not assume or reproduce their fields, statuses, or policies here, because they change independently of this Skill.

When development begins, record the active development mode and this phase's Development progress as `in progress`. Record it as `completed` only when every required Task is complete under Plan's current rules; otherwise keep the truthful incomplete value. Append each run outcome to State History without duplicating Task history.

Install and configure the runtimes, package managers, build tools, system software, and dependencies the authorized work requires. Resolve a missing prerequisite within the current authority whenever possible. Apply the shared decision policy and the current owning Component's blocking rules when evidence establishes that installation or configuration cannot proceed; a failed installation attempt is not required to establish such a condition.

Execute eligible planned work within the resolved scope and current authority. Apply the shared decision policy from those rules to unspecified implementation details while preserving project intent and existing interfaces.

Verify each result and record execution progress and evidence exactly as the live authorities require. A Task's verification states a condition to observe; construct the concrete executable check that satisfies it, run it, and record the check used and its outcome, so the proof survives even after the implementation is rearranged.

When work cannot complete, preserve truthful state and follow the current failure, question, and blocking policies. A record that overstates progress is worse than no record, because the next run trusts it.

After each outcome, reconcile Development-owned information and continue according to the current execution rules. The operation is repeatable and idempotent according to those rules.

## Boundaries

Perform only Development's role for eligible planned work in the requested phase. Do not perform another Interface Operation, alter Target intent, bypass resolved interfaces, or write outside Development's current authority.

## Report

Report in this order:

1. **Phase** — the resolved phase identifier, title, and target.
2. **Work executed** — each Task attempted, its outcome, and the check that proved it.
3. **Work not executed** — each eligible Task left undone and why, and each ineligible Task with the condition that held it back.
4. **Prerequisites handled** — runtimes, tools, or dependencies installed or configured during the run.
5. **Blockers and questions** — anything raised during the run, with what it prevents.
6. **State** — the aggregate phase progress and History outcome recorded for this run.
7. **Next step** — the single most useful next action supported by the result.
