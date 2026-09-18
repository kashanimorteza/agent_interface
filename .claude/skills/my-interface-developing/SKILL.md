---
name: my-interface-developing
description: Execute and verify eligible planned work for selected Target phases, or every phase eligible under its current Plan when none is specified, only when explicitly requested by the Human or delegated by a declared Interface coordinator. Prepares each phase's own technical requirements; never plans or reviews.
argument-hint: "[phase-number ...]"
metadata:
  contract: ".interface/agent/skill/contracts/developing.md"
  contract_sha256: "sha256:0551c6b3dfc78bf99152c2ee77c9e8035fc25002478586dddaa35c8bbb527a20"
  synced_at: "2026-09-18T13:46:48Z"
---

# Develop project phases

This file is the self-contained Claude Code realization of the portable `developing` Skill Contract, placed here by Agent Sync as the Human authored it. Follow this file and the synchronized Runtime Rules under `.claude/rules/`; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-developing` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Purpose

Turn eligible planned work into verified implementation.

## Responsibility

Execute eligible Tasks, choose implementation details within current authority, create durable checks from Task verification conditions, and record truthful evidence. Development never creates the Plan or performs independent Review.

## Trigger

Activate explicitly for zero or more phase selections after a valid current Plan exists and its prerequisites are ready.

## Inputs

Accept zero or more phase positions. Empty input selects every phase eligible under its current Plan. Resolve positions to stable identifiers, deduplicate them, and process them in Target order. Consume current Target Understanding, Component authorities, public interfaces, implementation, Plan, State, and Review Findings relevant to reconciliation.

Claude Code input handling: the positions arrive as whitespace-separated positive integers in `$ARGUMENTS` — `1` selects the first phase, `2` the second, and so on. Resolve every number against the current phase order in Target Understanding and use each phase's stable identifier to locate its current planning output and throughout development; the numbers are input conveniences and never rename a phase or change stored identifiers or references. If `$ARGUMENTS` is empty and no phase is eligible, make no changes and report that there is no phase to develop. If any token is not a positive integer resolving to an available phase, enumerate all available phases in Target order with their input number, stable identifier, title, status, and readiness, identify every invalid token, and ask the Human for a corrected list; do not begin development until the entire selection is valid.

## Outputs

Produce authorized implementation and durable checks, Development-owned Task progress and evidence, aggregate Development State and History, prerequisite actions, Blockers or Open Questions permitted by their owners, the associated Skills applied and those reported unavailable, and a phase-by-phase report.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Read every applicable Implementation Component, the selected phases' Plans and State, current public interfaces, and existing implementation.

Claude Code routes: establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, then Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Follow its routes to the applicable Implementation Principles and Preferences, the selected phases' Plan and State Config, current public interfaces, and existing implementation. Plan and State Config are operational records, not a stored representation of this Understanding: a Task states an activity, and its technical context is resolved from the current Implementation Preferences rather than read back from the record. Derive work selection, ordering, eligibility, progress updates, evidence handling, validation, ownership, and write boundaries from the current authorities on every run.

## Authority

Write implementation, tests, executable documentation, dependencies, and configuration only within the resolved Plan and Component boundaries. Write only Development-owned operational fields. Never alter Target intent, Planning-owned content, Review Findings, or unrelated work.

## Workflow Invariants

- Validate the complete phase input before mutation; an invalid token prevents the whole run.
- Before mutating a phase, require a current valid Plan and establish from current Interface and Target Understanding that the selected work is eligible.
- A prior Review record is not required; Review is performed after implementation exists.
- Execute only work eligible under current Plan rules and dependency evidence.
- Read the governing associations the Task records in its `agent_skills` field, then re-check each one against currently discoverable and usable Runtime Skills, because availability can change between planning and development.
- Resolve an association the Task does not record from the technical option that declares it, and report any difference between what the Task recorded and what is usable now.
- Match the declared name against the Skill's own name within a Runtime's namespaced identifier rather than requiring an exact string match.
- Activate an associated Skill only when the option is selected and the Skill is currently discoverable and usable.
- Apply a usable required Skill's complete applicable guidance as a completion gate, use optional Skills when available, and continue while reporting the unavailability when an associated Skill is not usable.
- When this work installs packages, the applicable Language Item's skill-provisioning rule applies to that installation.
- An associated Skill supplies guidance without changing scope or authority.
- Build a transient verification ledger that splits every acceptance and verification statement into observable conditions and associates each with proof.
- Derive checks from required conditions, never from the implementation just produced.
- One passing example proves only that example.
- Read the Cross-cutting Capability applicability lists the Implementation authorities declare before constructing any check, and let the testing list decide the check's form for the Task's target Component.
- When the target Component is listed, prefer a durable check committed with regressible behavior and let one-off probes only supplement it.
- When the target Component is not listed, satisfy the verification condition with a transient check whose artifacts do not remain: run it, record its outcome in the Task log, and leave no test suite, test directory, test configuration, or test dependency behind in that Component.
- Availability of a test runner in the declared toolchain never authorizes a persisted test in an unlisted Component, and no check may apply a Cross-cutting Capability to a Component its applicability list omits.
- Before implementing a phase, resolve the technical requirements the applicable Implementation Preferences declare for that phase's Component — language, package manager, packages, database, tools, and versions — inspect the Environment, install or verify only what is missing, and record each item's concrete version and verification result.
- Configure does not do this; every phase prepares what it needs.
- Install or configure only prerequisites required by authorized work and within current authority.
- Mark a Task or phase complete only when every required condition is observed and recorded truthfully.
- Run a phase completion gate from a sufficiently clean state, re-read authorities, execute the complete relevant checks, and inspect required public interfaces and documentation.
- Continue independent phases when one phase cannot complete, unless dependencies or Blockers prohibit it.

Claude Code execution detail: the verification ledger is a validation aid, not a second source of requirements — do not store it. When a phase's development begins, record the active development mode and that phase's Development progress as `in progress`; record it as `completed` only when every required Task is complete under Plan's current rules and the completion gate passes, otherwise keep the truthful incomplete value, and append each phase outcome to State History without duplicating Task history. Previously recorded `done` statuses and passing logs are evidence to examine, not substitutes for current observation. For code, configuration, schemas, and executable documentation, use the selected Component's configured test, type-check, lint, build, installation, and documentation-check capabilities where applicable, subject to the applicability check above. Developing never invokes Reviewer or treats its own Plan inspection as independent assurance.

## Verification

- Each Task requires observable evidence for every acceptance clause.
- Phase completion additionally requires the full relevant check suite and reconciliation against current Target, Component authorities, public interfaces, and the verification ledger.
- Phase completion also requires proving that no Component outside a Cross-cutting Capability's applicability list carries that capability's artifacts, including a testing artifact left by a check.
- A Component outside the testing list that holds a test suite, test directory, test configuration, or test dependency fails this verification, and the failure is reported with that Component named.

## Idempotency

Preserve valid implementation and completed evidence, reconcile changed requirements or Findings, and avoid rewriting unchanged results.

## Stopping Conditions

- Stop before mutation on invalid input.
- Do not execute ineligible work or work without a valid current Plan.
- Leave progress truthful when authority, prerequisites, required decisions, dependency gates, or verification cannot be satisfied; continue only independent work.

## Runtime Realization

A native adapter uses the selected development tools and package mechanisms from Component Preferences, never hardcodes them in the Contract, and reports executed and withheld work, proof, prerequisites, blockers, State, and the supported next step.

In Claude Code this adapter reports, in this order:

1. **Phases** — every resolved phase identifier, title, and target, in Target order.
2. **Work executed** — by phase, each Task attempted, its outcome, and the check that proved it.
3. **Work not executed** — by phase, each eligible Task left undone and why, and each ineligible Task with the condition that held it back.
4. **Associated Skills** — by phase, each Skill applied while performing the work, and each declared association that was not usable.
5. **Prerequisites handled** — by phase, each technical requirement resolved for the phase's Component, its concrete version, whether it was already satisfied or installed during the run, and its verification result.
6. **Blockers and questions** — by phase, anything raised during the run, with what it prevents.
7. **State** — each phase's aggregate progress and the History outcomes recorded for this run.
8. **Next step** — the single most useful next action supported by the result.
