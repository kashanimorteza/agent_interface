# developing Skill Contract

## Purpose

Turn eligible planned work into verified implementation.

## Responsibility

Execute eligible Tasks, choose implementation details within current authority, create durable checks from Task verification conditions, and record truthful evidence. Development never creates the Plan or performs independent Review.

## Trigger

Activate explicitly for zero or more phase selections after a valid current Plan exists and its prerequisites are ready.

## Inputs

Accept zero or more phase positions. Empty input selects every phase eligible under its current Plan. Resolve positions to stable identifiers, deduplicate them, and process them in Target order. Consume current Target Understanding, Component authorities, public interfaces, implementation, Plan, State, and Review Findings relevant to reconciliation.

## Outputs

Produce authorized implementation and durable checks, Development-owned Task progress and evidence, aggregate Development State and History, prerequisite actions, Blockers or Open Questions permitted by their owners, the Agent parameters applied, any reported as overridden by a higher authority, and the associated Skills applied or reported unavailable, and a phase-by-phase report.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Read every applicable Implementation Component, the selected phases' Plans and State, current public interfaces, and existing implementation.

## Authority

Write implementation, tests, executable documentation, dependencies, and configuration only within the resolved Plan and Component boundaries. Write only Development-owned operational fields. Never alter Target intent, Planning-owned content, Review Findings, or unrelated work.

## Workflow Invariants

- Validate the complete phase input before mutation; an invalid token prevents the whole run.
- Before mutating a phase, require a current valid Plan and establish from current Interface and Target Understanding that the selected work is eligible.
- A prior Review record is not required; Review is performed after implementation exists.
- Execute only work eligible under current Plan rules and dependency evidence.
- Read the Agent parameters the Task records, and gather from current Preferences any applicable parameter the Task does not record, on the item being worked on and on every item above it.
- Apply what an applicable `agent_consider` asks for and honour what an applicable `agent_avoid` rules out throughout the work, with the nearest parameter governing any point two of them speak to.
- Where such a parameter conflicts with an explicit Target statement or an applicable Principle, follow that authority and report the overridden parameter rather than choosing silently.
- Re-check each recorded `agent_skills` association against currently discoverable and usable Runtime Skills, because availability can change between planning and development, and report any difference between what the Task recorded and what is usable now.
- Match the declared name against the Skill's own name within a Runtime's namespaced identifier rather than requiring an exact string match.
- Activate an associated Skill only when the item carrying it is selected and the Skill is currently discoverable and usable.
- Apply a usable required Skill's complete applicable guidance as a completion gate, use optional Skills when available, and continue while reporting the unavailability when an associated Skill is not usable.
- When this work installs packages, the applicable Language Item's skill-provisioning rule applies to that installation.
- An associated Skill, and every Agent parameter, supplies guidance without changing scope or authority.
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
