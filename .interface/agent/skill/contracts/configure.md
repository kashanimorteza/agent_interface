# configure Skill Contract

## Purpose

Prepare the four operational Config records that the Interface workflow depends on.

## Responsibility

Establish Interface Understanding and the minimal Target Understanding needed for Config, and generate or reconcile the four operational Config files from their Schemas. It owns no planning, implementation, review, launch, reset, technical-requirement installation, Environment preparation, or Target interpretation beyond the limited facts required for configuration, and performs none of them. Each operation installs or prepares what its own work needs: Developing the technical requirements of the phase it implements, Launch the Environment of the selected Launch Item.

## Trigger

Activate when operational Config must be created, validated, repaired, or refreshed, and once at the start of end-to-end implementation orchestration.

## Inputs

Accept no phase selection. Consume current operational Schemas, existing Config, stable Target phase identifiers, and the public metadata already published by existing Implementation Components.

## Outputs

Produce or reconcile Schema-valid `plan.yaml`, `state.yaml`, `review.yaml`, and `application.yaml` Config files, truthful State position and History, and a report of created, reconciled, preserved, conflicted, and blocked results.

## Required Understanding

Configure first understands the Interface and the current Target context needed for configuration — its stable phase identifiers — and then the Config Schemas. Its work has two connected purposes: create the operational Config records from their Schemas, and reconcile and preserve those records. The four Config files, including `application.yaml`, follow the same schema-driven generation process; none is a temporary or optional side file. Configure does not implement product behavior, decide Target meaning, install anything, or prepare any Environment.

Establish Interface Understanding and only the Target Understanding needed for Config generation. Read current Config Schemas.

## Authority

Write the four Config records owned by Configure. Never install a technical dependency, prepare a system or Environment, or provision, transfer, or install an Agent Skill, plugin, or capability; Developing installs what its phase needs, Launch prepares its Environment, and the install mode of the Agent Native Skill owns Agent capabilities. Never create or modify other Interface sources or any product implementation. Never create, scaffold, or populate an Implementation Component root, package, source file, test, or lockfile; Component generation belongs to Developing.

## Workflow Invariants

- Generate or reconcile all four Config files from their current Schemas rather than a remembered structure; `application.yaml` follows the same process as the other three files.
- Record only the public metadata a Component already publishes. When a declared Component does not yet exist, leave its Manifest section at its Schema default and report it as not yet generated; never create the Component to obtain its metadata.
- Preserve meaningful operational records through structural reconciliation; surface a conflict rather than discard information that has no other owner.
- Add missing phase records at current initial values and preserve progress while generating `state.yaml`; remove a stale record only while it contains initialization defaults, otherwise preserve and report it.
- Never copy Target meaning into Config.
- Record active Configure position and append the outcome under State ownership.

## Verification

Validate every Config record against its applicable Schemas and verify phase identity reconciliation.

## Idempotency

Repeating against unchanged Schemas, Target identity, and Config produces no structural mutation while still recording invocation outcomes as State permits.

## Stopping Conditions

Stop or preserve the affected item when reconciliation would lose meaningful records or a Schema cannot be applied safely. Independently valid items may continue.

## Runtime Realization

A native adapter exposes one project-scoped Configure capability, resolves all paths and native mechanisms through the current Interface and Runtime mapping, and reports Config, phase synchronization, preserved records, and blockers.
