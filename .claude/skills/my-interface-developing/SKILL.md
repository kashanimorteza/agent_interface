---
name: my-interface-developing
description: Execute and verify eligible planned work for selected Target phases, or every phase eligible under its current Plan when none is specified, only when explicitly requested by the Human or delegated by a declared Interface coordinator. Never plans or reviews.
argument-hint: "[phase-number ...]"
metadata:
  contract: ".interface/agent/skill/contracts/developing.md"
  contract_sha256: "sha256:71a186904e3ff78c9b85ff9e42379dfbe320062e96d0ac619fd946b6541ce898"
  synced_at: "2026-09-17T12:58:42Z"
---

# Develop project phases

This file is the self-contained Claude Code realization of the portable `developing` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-developing` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Role

Implement and verify eligible planned work for the selected project phases, using current Target Understanding and their Task Plans as the specification.

Developing owns the implementation method and the arrangement of the source. The Plan says what must be achieved and what proves it; deciding how is this operation's work, and a Plan that already decided it would be describing code that does not exist yet.

Developing also builds the check that proves each result, because only the operation that made the result knows how to observe it. Build that check from the verification condition the Task states, not from the implementation just written: a check shaped around the code will pass whatever the code happens to do, and prove nothing about what was asked for.

Developing may write implementation and install and configure the prerequisites required by the authorized work, within the scope and write boundaries established by the Plan, applicable Implementation Component authorities, and synchronized Runtime rules.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects the first phase, `2` selects the second phase, and so on. Resolve every number against the current phase order in Target Understanding and use each phase's stable identifier to locate its current planning output and throughout development.

The numbers are input conveniences; the Human does not need to type phase identifiers' `P` prefixes, and a number never renames a phase or changes stored identifiers or references.

If `$ARGUMENTS` is empty, select every phase eligible under its current Plan, as current Implementation and operational Component authorities define eligibility. If no phase is eligible, make no changes and report that there is no phase to develop.

If arguments are present, validate the complete selection before changing any files. Every token must be a positive integer that resolves to an available phase. Deduplicate repeated numbers and process the selected phases in Target order, regardless of argument order. If any token is invalid, enumerate all available phases in Target order with their input number, stable identifier, title, status, and readiness, identify every invalid token, and ask the Human for a corrected list; do not begin development until the entire selection is valid.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Developing's place in the Workflow, and the current locations of the resources Development needs.

Then establish Target Understanding from the Human and Technical Definitions located by the Interface under their declared precedence, and read the applicable Implementation Principles and Preferences under synchronized Runtime rules, together with existing implementation and public interfaces. Never enter or inspect the Agent Module. Plan and State Config are operational records, not a stored representation of this Understanding: a Task states an activity, and its technical context is resolved from the current Implementation Preferences rather than read back from the record.

Read every selected phase's current Task Plan and State. Derive work selection, ordering, eligibility, progress updates, evidence handling, validation, ownership, and write boundaries from current Implementation and operational Component authorities. Do not assume or reproduce their fields, statuses, or policies here, because they change independently of this Skill.

Read the governing associations the Task records in its `agent_skills` field, then re-check each one against currently discoverable and usable Runtime Skills, because availability can change between planning and development. Resolve an association the Task does not record from the technical option that declares it, and report any difference between what the Task recorded and what is usable now. Match the declared name against the Skill's own name within a Runtime's namespaced identifier rather than requiring an exact string match. Activate an associated Skill only when the option is selected and the Skill is currently discoverable and usable. When a required associated Skill is usable, apply its complete applicable guidance as a completion gate for the governed work; use an optional Skill's guidance when it is available. Continue the work and report the unavailability when an associated Skill — required or optional — is not currently usable; an unavailable associated Skill never stops Development. When this work installs packages, the applicable Language Item's skill-provisioning rule applies to that installation. An associated Skill supplies guidance without changing scope or authority.

Before changing implementation or Task progress for a phase, read its current Plan and establish current Interface and Target Understanding. Require a valid current Plan and eligible work; a prior Review record is not required because Review runs after implementation exists. Developing never invokes Reviewer or treats its own Plan inspection as independent assurance.

Before executing a phase, create a transient verification ledger. Split every Task's acceptance and verification statements into individually observable conditions, then add the applicable Target and Component-authority requirements that the result must satisfy. Associate every condition with the check that will prove it. Do not store this ledger as a second source of requirements; use it to prevent a broad requirement from being marked complete after one narrow example passes.

Process selected phases in Target order. For each phase, when its development begins, record the active development mode and that phase's Development progress as `in progress`. Record it as `completed` only when every required Task is complete under Plan's current rules; otherwise keep the truthful incomplete value. Append each phase outcome to State History without duplicating Task history. A phase that has no eligible work or cannot complete does not prevent attempting a later selected phase unless the current authorities establish a dependency or Blocker that does.

Install and configure the runtimes, package managers, build tools, system software, and dependencies the authorized work requires. Resolve a missing prerequisite within the current authority whenever possible. Apply the shared decision policy and the current owning Component's blocking rules when evidence establishes that installation or configuration cannot proceed; a failed installation attempt is not required to establish such a condition.

Execute eligible planned work within the resolved scope and current authority. Apply the shared decision policy from those rules to unspecified implementation details while preserving project intent and existing interfaces.

Verify each result and record execution progress and evidence exactly as the live authorities require. A Task's verification states a condition to observe; construct the concrete executable checks that satisfy every condition in the transient verification ledger, run them, and record the checks used and their outcomes. A passing example proves only that example. Do not mark a Task complete while another acceptance clause is unobserved or while the implementation contains no durable representation of an outcome the Task requires.

Before constructing any check, read the Cross-cutting Capability applicability lists the current Implementation authorities declare, and let the testing list decide that check's form for the Task's target Component. When the target Component is listed, prefer a durable check committed with the implementation whenever the condition can regress, and let one-off probes only supplement it. When the target Component is not listed, satisfy the verification condition with a transient check whose artifacts do not remain: run it, record its outcome in the Task log, and leave no test suite, test directory, test configuration, or test dependency behind in that Component. Availability of a test runner in the declared toolchain never authorizes a persisted test in an unlisted Component, and no check may apply a Cross-cutting Capability to a Component its applicability list omits. For code, configuration, schemas, and executable documentation, use the selected Component's configured test, type-check, lint, build, installation, and documentation-check capabilities where applicable, subject to that same applicability check.

After all eligible Tasks in a phase have been handled, run a phase completion gate from a clean enough state to reveal undeclared dependencies and stale artifacts. Re-read the phase outcome and applicable authorities, reconcile them against the actual implementation and the verification ledger, run the complete relevant check suite, and inspect any required public interface and documentation. Also prove that no Component outside a Cross-cutting Capability's applicability list carries that capability's artifacts, including a testing artifact left by a check; a Component outside the testing list that holds a test suite, test directory, test configuration, or test dependency fails this gate, and the failure is reported with that Component named. Previously recorded `done` statuses and passing logs are evidence to examine, not substitutes for current observation. Record the phase as `completed` only when this gate passes without uncovered requirements or missing evidence.

When work cannot complete, preserve truthful state and follow the current failure, question, and blocking policies. A record that overstates progress is worse than no record, because the next run trusts it.

After each outcome, reconcile Development-owned information and continue according to the current execution rules. The operation is repeatable and idempotent according to those rules: it preserves valid implementation and completed evidence, reconciles changed requirements or Findings, and avoids rewriting unchanged results.

## Boundaries

Perform only Development's role for eligible planned work in the selected phases. Do not perform another Interface Operation, alter Target intent, bypass resolved interfaces, or write outside Development's current authority.

## Report

Report in this order:

1. **Phases** — every resolved phase identifier, title, and target, in Target order.
2. **Work executed** — by phase, each Task attempted, its outcome, and the check that proved it.
3. **Work not executed** — by phase, each eligible Task left undone and why, and each ineligible Task with the condition that held it back.
4. **Associated Skills** — by phase, each Skill applied while performing the work, and each declared association that was not usable.
5. **Prerequisites handled** — by phase, runtimes, tools, or dependencies installed or configured during the run.
6. **Blockers and questions** — by phase, anything raised during the run, with what it prevents.
7. **State** — each phase's aggregate progress and the History outcomes recorded for this run.
8. **Next step** — the single most useful next action supported by the result.
