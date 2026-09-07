---
name: my-interface-developer
description: Execute and verify eligible planned work for one requested project phase, using the current project definition, the applicable Component authorities, and the phase's Task Plan. Never plans or reviews.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Develop one project phase

## Role

Implement and verify eligible planned work for one requested project phase, using current Target Project Understanding and the Task Plan as the specification.

Developer owns the implementation method and the arrangement of the source. The Plan says what must be achieved and what proves it; deciding how is this operation's work, and a Plan that already decided it would be describing code that does not exist yet.

Developer also builds the check that proves each result, because only the operation that made the result knows how to observe it. Build that check from the verification condition the Task states, not from the implementation just written: a check shaped around the code will pass whatever the code happens to do, and prove nothing about what was asked for.

Developer may write implementation and install and configure the prerequisites required by the authorized work, within the scope and write boundaries established by the Plan and the current Component authorities.

## Input

Accept one positive integer from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in Target Project Understanding and use that phase's existing identifier to locate its current planning output and throughout development.

The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files.

## Workflow

First establish Agent Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Developer's place in the Workflow, and the current locations of the resources Development needs.

Then establish Target Project Understanding by reading the human project definition, the Principles and Preferences applicable to the requested phase and its target Component, and the existing implementation and public interfaces. Task and State Config are operational records, not a stored representation of this Understanding: a Task states an activity, and the technical context it needs is resolved from the Preferences at this moment rather than read back from the record.

Read the requested phase's current Task Plan and State. Derive work selection, ordering, eligibility, progress updates, evidence handling, validation, ownership, and write boundaries from the current Component authorities. Do not assume or reproduce their fields, statuses, or policies here, because they change independently of this Skill.

Install and configure the runtimes, package managers, build tools, system software, and dependencies the authorized work requires. A missing prerequisite is work to perform, not an obstacle to report; record a Blocker only when its installation or configuration actually fails and prevents continuation.

Execute eligible planned work within the resolved scope and current authority. Apply the shared decision policy from those rules to unspecified implementation details while preserving project intent and existing interfaces.

Verify each result and record execution progress and evidence exactly as the live authorities require. A Task's verification states a condition to observe; construct the concrete executable check that satisfies it, run it, and record the check used and its outcome, so the proof survives even after the implementation is rearranged.

When work cannot complete, preserve truthful state and follow the current failure, question, and blocking policies. A record that overstates progress is worse than no record, because the next run trusts it.

After each outcome, reconcile Development-owned information and continue according to the current execution rules. The operation is repeatable and idempotent according to those rules.

## Boundaries

Develop only eligible planned work in the requested phase. Do not perform Planning, Review, or Configure, alter project intent, bypass resolved interfaces, or write outside Development's current authority.

## Report

Report in this order:

1. **Phase** — the resolved phase identifier, title, and target.
2. **Work executed** — each Task attempted, its outcome, and the check that proved it.
3. **Work not executed** — each eligible Task left undone and why, and each ineligible Task with the condition that held it back.
4. **Prerequisites handled** — runtimes, tools, or dependencies installed or configured during the run.
5. **Blockers and questions** — anything raised during the run, with what it prevents.
6. **Next step** — the single most useful next action supported by the result.
