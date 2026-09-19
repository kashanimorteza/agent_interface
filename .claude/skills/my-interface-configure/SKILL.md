---
name: my-interface-configure
description: Prepare the four operational Config records (plan, state, review, application) from their Schemas and synchronize phase State, only when explicitly requested by the Human or delegated by a declared Interface coordinator. Installs nothing and prepares no Environment.
metadata:
  contract: ".interface/agent/skill/contracts/configure.md"
  contract_sha256: "sha256:eb92955042e47ed6c10e605bc001370fb4afac3ad20b1b53e4b9f132b5a365e8"
  preferences: ".interface/agent/skill/preferences.yaml"
  preferences_sha256: "sha256:386052d88bf6225ecc6b2cc35f60fc2e7344a26bce478741efa86371fde6d566"
  synced_at: "2026-09-19T16:31:31Z"
---

# Configure the Interface

This file is the self-contained Claude Code realization of the portable `configure` Skill Contract, placed here by Agent Sync as the Human authored it. Follow this file and the synchronized Runtime Rules under `.claude/rules/`; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-configure` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Purpose

Prepare the four operational Config records that the Interface workflow depends on.

## Responsibility

Establish Interface Understanding and the minimal Target Understanding needed for Config, and generate or reconcile the four operational Config files from their Schemas. It owns no planning, implementation, review, launch, reset, technical-requirement installation, Environment preparation, or Target interpretation beyond the limited facts required for configuration, and performs none of them. Each operation installs or prepares what its own work needs: Developing the technical requirements of the phase it implements, Launch the Environment of the selected Launch Item.

## Trigger

Activate when operational Config must be created, validated, repaired, or refreshed, and once at the start of end-to-end implementation orchestration.

## Inputs

Accept no phase selection. Consume current operational Schemas, existing Config, stable Target phase identifiers, and the public metadata already published by existing Implementation Components.

Claude Code input handling: when `$ARGUMENTS` is not empty, make no changes, report that Configure accepts no phase or scope input, and ask the Human to invoke it without arguments.

## Outputs

Produce or reconcile Schema-valid `plan.yaml`, `state.yaml`, `review.yaml`, and `application.yaml` Config files, truthful State position and History, and a report of created, reconciled, preserved, conflicted, and blocked results.

## Required Understanding

Configure first understands the Interface and the current Target context needed for configuration — its stable phase identifiers — and then the Config Schemas. Its work has two connected purposes: create the operational Config records from their Schemas, and reconcile and preserve those records. The four Config files, including `application.yaml`, follow the same schema-driven generation process; none is a temporary or optional side file. Configure does not implement product behavior, decide Target meaning, install anything, or prepare any Environment.

Establish Interface Understanding and only the Target Understanding needed for Config generation. Read current Config Schemas.

Claude Code routes: establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, follow its routes to the operational Schemas and the Config destination under `.interface/foundation/`, and take stable phase identifiers from the Target definitions it locates under their declared precedence.

## Authority

Write the four Config records owned by Configure. Never install a technical dependency, prepare a system or Environment, or provision, transfer, or install an Agent Skill, plugin, or capability; Developing installs what its phase needs, Launch prepares its Environment, and the install mode of the Agent Native Skill owns Agent capabilities. Never create or modify other Interface sources or any product implementation. Never create, scaffold, or populate an Implementation Component root, package, source file, test, or lockfile; Component generation belongs to Developing.

## Workflow Invariants

- Generate or reconcile all four Config files from their current Schemas rather than a remembered structure; `application.yaml` follows the same process as the other three files.
- Record only the public metadata a Component already publishes.
- When a declared Component does not yet exist, leave its Manifest section at its Schema default and report it as not yet generated; never create the Component to obtain its metadata.
- Preserve meaningful operational records through structural reconciliation; surface a conflict rather than discard information that has no other owner.
- Add missing phase records at current initial values and preserve progress while generating `state.yaml`; remove a stale record only while it contains initialization defaults, otherwise preserve and report it.
- Never copy Target meaning into Config.
- Record active Configure position and append the outcome under State ownership.

Claude Code execution detail: for each Schema, read its current structure, initialization instructions, defaults, and update requirements, and derive the initialization method from those instructions rather than assuming a template key or record structure. When a Config file is absent, generate it according to those instructions; when it exists, validate it and reconcile only the structural differences the Schema requires.

## Verification

- Validate every Config record against its applicable Schemas and verify phase identity reconciliation.

## Idempotency

Repeating against unchanged Schemas, Target identity, and Config produces no structural mutation while still recording invocation outcomes as State permits.

## Stopping Conditions

- Stop or preserve the affected item when reconciliation would lose meaningful records or a Schema cannot be applied safely.
- Independently valid items may continue.

Record each such condition as a Blocker through State and report it.

## Runtime Realization

A native adapter exposes one project-scoped Configure capability, resolves all paths and native mechanisms through the current Interface and Runtime mapping, and reports Config, phase synchronization, preserved records, and blockers.

In Claude Code this adapter reports, in this order:

1. **Config** — the status of all four files, including `application.yaml`, and any records created, reconciled, or already valid.
2. **Phase synchronization** — phase records added, preserved, or left as conflicts.
3. **Preserved records** — existing operational information carried through unchanged.
4. **Conflicts and blockers** — anything that could not be reconciled safely, and what it prevents.
