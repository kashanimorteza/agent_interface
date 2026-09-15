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

Produce authorized implementation and durable checks, Development-owned Task progress and evidence, aggregate Development State and History, prerequisite actions, Blockers or Open Questions permitted by their owners, and a phase-by-phase report.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Read every applicable Implementation Component, the selected phases' Plans and State, current public interfaces, and existing implementation.

## Authority

Write implementation, tests, executable documentation, dependencies, and configuration only within the resolved Plan and Component boundaries. Write only Development-owned operational fields. Never alter Target intent, Planning-owned content, Review Findings, or unrelated work.

## Workflow Invariants

- Validate the complete phase input before mutation; an invalid token prevents the whole run.
- Before mutating a phase, require a current valid Plan and establish from current Interface and Target Understanding that the selected work is eligible. A prior Review record is not required; Review is performed after implementation exists.
- Execute only work eligible under current Plan rules and dependency evidence.
- For every resolved technical option involved in the work, resolve its declared `agent_skills` associations against currently discoverable and usable Runtime Skills. Activate an associated Skill only when the option is selected and the Skill is currently discoverable and usable; use an optional Skill when available and continue without it when unavailable, and stop the affected work when a required Skill is unavailable. Once activated, apply that Skill's complete applicable guidance to every implementation detail it governs; a result that contradicts activated guidance is not complete, whether or not its other acceptance conditions pass. An associated Skill constrains how the option is used; it never expands scope or authority beyond the resolved Plan.
- Build a transient verification ledger that splits every acceptance and verification statement into observable conditions and associates each with proof.
- Derive checks from required conditions, never from the implementation just produced. One passing example proves only that example.
- Prefer durable checks committed with regressible behavior; one-off probes only supplement them.
- Install or configure only prerequisites required by authorized work and within current authority.
- Mark a Task or phase complete only when every required condition is observed and recorded truthfully.
- Run a phase completion gate from a sufficiently clean state, re-read authorities, execute the complete relevant checks, and inspect required public interfaces and documentation.
- Continue independent phases when one phase cannot complete, unless dependencies or Blockers prohibit it.

## Verification

Each Task requires observable evidence for every acceptance clause. Phase completion additionally requires the full relevant check suite and reconciliation against current Target, Component authorities, public interfaces, and the verification ledger. When a Task's work activated one or more Skills, its evidence additionally includes an explicit observation that the result conforms to each activated Skill's applicable guidance; a Skill consulted but not reflected in the result is a verification failure, not a satisfied Task.

## Idempotency

Preserve valid implementation and completed evidence, reconcile changed requirements or Findings, and avoid rewriting unchanged results.

## Stopping Conditions

Stop before mutation on invalid input. Do not execute ineligible work or work without a valid current Plan. Leave progress truthful when authority, prerequisites, required decisions, dependency gates, or verification cannot be satisfied; continue only independent work.

## Runtime Realization

A native adapter uses the selected development tools and package mechanisms from Component Preferences, never hardcodes them in the Contract, and reports executed and withheld work, proof, prerequisites, blockers, State, and the supported next step.
