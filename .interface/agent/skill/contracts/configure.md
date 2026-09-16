# configure Skill Contract

## Purpose

Prepare the operational Config records and the declared technical environment that the Interface workflow depends on.

## Responsibility

Establish Interface and Target Understanding, generate or reconcile the four operational Config files from their Schemas, install declared technical requirements, provision the Agent Skills named by applicable `agent_skills` associations through the declared ecosystem mechanism, and prepare the selected Platform Environment. It owns no planning, implementation, review, launch, reset, or Target interpretation beyond the limited facts required for configuration, and performs none of them.

## Trigger

Activate when operational Config or Environment readiness must be created, validated, repaired, or refreshed, and once at the start of end-to-end implementation orchestration.

## Inputs

Accept no phase selection. Consume current operational Schemas, existing Config, stable Target phase identifiers, explicit Target and Platform selections, all applicable Implementation Component Principles and Preferences, the selected Platform Preferences and Launch Item, and Platform defaults where Target is silent.

## Outputs

Produce or reconcile Schema-valid `plan.yaml`, `state.yaml`, `review.yaml`, and `application.yaml` Config files, resolved and prepared technical requirements and Environment, truthful State position and History, and a report of created, installed, reconciled, preserved, conflicted, and blocked results.

## Understanding

Configure first understands the Interface and the current Target context needed for configuration. It then understands the Config Schemas, the applicable Implementation and Platform authorities, and the selected Environment. Its work has three connected purposes: create the operational Config records from their Schemas, reconcile and preserve those records, and prepare the project by resolving and installing the technical requirements declared by the applicable authorities. The four Config files, including `application.yaml`, follow the same schema-driven generation process; none is a temporary or optional side file. Configure does not implement product behavior or decide Target meaning.

## Required Understanding

Establish Interface Understanding and only the Target Understanding needed for Config generation and declared technical or Environment requirements. Read current Config Schemas, applicable Implementation Component authorities, and Platform authorities.

## Authority

Write the four Config records owned by Configure and perform technical dependency installation and system preparation required by the selected Platform Launch Item, including the skill-provisioning mechanism declared by an applicable Language Item. Never create or modify other Interface sources or any product implementation. Never create, scaffold, or populate an Implementation Component root, package, source file, test, or lockfile; Component generation belongs to Developing.

## Workflow Invariants

- Generate or reconcile all four Config files from their current Schemas rather than a remembered structure; `application.yaml` follows the same process as the other three files.
- Record only the public metadata a Component already publishes. When a declared Component does not yet exist, leave its Manifest section at its Schema default and report it as not yet generated; never create the Component to obtain its metadata.
- Preserve meaningful operational records through structural reconciliation; surface a conflict rather than discard information that has no other owner.
- Add missing phase records at current initial values and preserve progress while generating `state.yaml`; remove a stale record only while it contains initialization defaults, otherwise preserve and report it.
- Never copy Target meaning into Config.
- Resolve every applicable language, package-management, package, database, tool, platform, and version selection from Implementation and Platform authorities before installation.
- Install or reconcile every required resolved technical item and record its concrete version and verification result.
- After resolving and installing the declared technical requirements, run the skill-provisioning mechanism the applicable Language Item declares, so Skills named by Implementation's `agent_skills` associations become usable before later operations need them. Resolve those names from the applicable Implementation authorities only; never enter or resolve an Agent Module source. Report a named Skill that remains unavailable; never adopt a Skill that no association names, and never remove an existing Skill. An unavailable Skill never blocks Configure or fails its verification; preparation continues and the unavailability is reported for the later operation that needs it.
- Inspect every applicable Platform Component definition and apply its declared system requirements for the selected Launch Item.
- Inspect the Environment before changing it and apply only missing declared requirements.
- Record active Configure position and append the outcome under State ownership.

## Verification

Validate every Config record against its applicable Schemas, verify phase identity reconciliation, verify every resolved technical item and its concrete version, and observe every Platform Environment requirement claimed as satisfied.

## Idempotency

Repeating against unchanged Schemas, Target identity, Config, resolved technical selections, and Platform Environment produces no structural or installation mutation while still recording invocation outcomes as State permits.

## Stopping Conditions

Stop or preserve the affected item when reconciliation would lose meaningful records, a required Environment choice is unresolved, preparation exceeds authority, or a genuine preparation condition cannot be resolved safely. Independently valid items may continue.

## Runtime Realization

A native adapter exposes one project-scoped Configure capability, resolves all paths and native mechanisms through the current Interface and Runtime mapping, and reports Config, phase synchronization, Environment, preserved records, and blockers.
