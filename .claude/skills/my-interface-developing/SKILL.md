---
name: my-interface-developing
description: Execute and verify eligible planned work for selected project phases, or for every enabled phase when none is specified, using the current project definition, applicable Component authorities, and phase Task Plans. Never plans or reviews.
argument-hint: "[phase-number ...]"
disable-model-invocation: true
---

# Develop project phases

## Role

Implement and verify eligible planned work for the selected project phases, using current Target Understanding and their Task Plans as the specification.

Developing owns the implementation method and the arrangement of the source. The Plan says what must be achieved and what proves it; deciding how is this operation's work, and a Plan that already decided it would be describing code that does not exist yet.

Developing also builds the check that proves each result, because only the operation that made the result knows how to observe it. Build that check from the verification condition the Task states, not from the implementation just written: a check shaped around the code will pass whatever the code happens to do, and prove nothing about what was asked for.

Developing may write implementation and install and configure the prerequisites required by the authorized work, within the scope and write boundaries established by the Plan and the current Component authorities.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects the first phase, `2` selects the second phase, and so on. Resolve every number against the current phase order in Target Understanding and use each phase's stable identifier to locate its current planning output and throughout development.

The numbers are input conveniences; the Human does not need to type phase identifiers' `P` prefixes, and a number never renames a phase or changes stored identifiers or references.

If `$ARGUMENTS` is empty, select every phase whose current Target status marks it enabled. If no phase is enabled, make no changes and report that there is no phase to develop.

If arguments are present, validate the complete selection before changing any files. Every token must be a positive integer that resolves to an available phase. Deduplicate repeated numbers and process the selected phases in Target order, regardless of argument order. If any token is invalid, enumerate all available phases in Target order with their input number, stable identifier, title, status, and readiness, identify every invalid token, and ask the Human for a corrected list; do not begin development until the entire selection is valid.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Developing's place in the Workflow, and the current locations of the resources Development needs.

Then establish Target Understanding by reading the human project definition, the Principles and Preferences applicable to the selected phases and their target Components, and the existing implementation and public interfaces. Plan and State Config are operational records, not a stored representation of this Understanding: a Task states an activity, and the technical context it needs is resolved from the Preferences at this moment rather than read back from the record.

Read every selected phase's current Task Plan and State. Derive work selection, ordering, eligibility, progress updates, evidence handling, validation, ownership, and write boundaries from the current Component authorities. Do not assume or reproduce their fields, statuses, or policies here, because they change independently of this Skill.

Before executing a phase, create a transient verification ledger. Split every Task's acceptance and verification statements into individually observable conditions, then add the applicable Target and Component-authority requirements that the result must satisfy. Associate every condition with the check that will prove it. Do not store this ledger as a second source of requirements; use it to prevent a broad requirement from being marked complete after one narrow example passes.

Process selected phases in Target order. For each phase, when its development begins, record the active development mode and that phase's Development progress as `in progress`. Record it as `completed` only when every required Task is complete under Plan's current rules; otherwise keep the truthful incomplete value. Append each phase outcome to State History without duplicating Task history. A phase that has no eligible work or cannot complete does not prevent attempting a later selected phase unless the current authorities establish a dependency or Blocker that does.

Install and configure the runtimes, package managers, build tools, system software, and dependencies the authorized work requires. Resolve a missing prerequisite within the current authority whenever possible. Apply the shared decision policy and the current owning Component's blocking rules when evidence establishes that installation or configuration cannot proceed; a failed installation attempt is not required to establish such a condition.

Execute eligible planned work within the resolved scope and current authority. Apply the shared decision policy from those rules to unspecified implementation details while preserving project intent and existing interfaces.

Verify each result and record execution progress and evidence exactly as the live authorities require. A Task's verification states a condition to observe; construct the concrete executable checks that satisfy every condition in the transient verification ledger, run them, and record the checks used and their outcomes. A passing example proves only that example. Do not mark a Task complete while another acceptance clause is unobserved or while the implementation contains no durable representation of an outcome the Task requires.

For code, configuration, schemas, and executable documentation, prefer checks committed with the implementation whenever the condition can regress. Use the selected Component's configured test, type-check, lint, build, installation, and documentation-check capabilities as applicable. A one-off shell probe may supplement durable checks but does not replace them for behavior that can be tested repeatedly.

After all eligible Tasks in a phase have been handled, run a phase completion gate from a clean enough state to reveal undeclared dependencies and stale artifacts. Re-read the phase outcome and applicable authorities, reconcile them against the actual implementation and the verification ledger, run the complete relevant check suite, and inspect any required public interface and documentation. Previously recorded `done` statuses and passing logs are evidence to examine, not substitutes for current observation. Record the phase as `completed` only when this gate passes without uncovered requirements or missing evidence.

When work cannot complete, preserve truthful state and follow the current failure, question, and blocking policies. A record that overstates progress is worse than no record, because the next run trusts it.

After each outcome, reconcile Development-owned information and continue according to the current execution rules. The operation is repeatable and idempotent according to those rules.

## Boundaries

Perform only Development's role for eligible planned work in the selected phases. Do not perform another Interface Operation, alter Target intent, bypass resolved interfaces, or write outside Development's current authority.

## Report

Report in this order:

1. **Phases** — every resolved phase identifier, title, and target, in Target order.
2. **Work executed** — by phase, each Task attempted, its outcome, and the check that proved it.
3. **Work not executed** — by phase, each eligible Task left undone and why, and each ineligible Task with the condition that held it back.
4. **Prerequisites handled** — by phase, runtimes, tools, or dependencies installed or configured during the run.
5. **Blockers and questions** — by phase, anything raised during the run, with what it prevents.
6. **State** — each phase's aggregate progress and the History outcomes recorded for this run.
7. **Next step** — the single most useful next action supported by the result.
