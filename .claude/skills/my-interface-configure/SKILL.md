---
name: my-interface-configure
description: Generate or refresh operational Config, synchronize phase State, and prepare the selected Platform Environment when explicitly requested by the Human or delegated by a declared Interface coordinator.
metadata:
  contract: ".interface/agent/skill/contracts/configure.md"
  contract_sha256: "sha256:39f03a0e748aea091b98ebe5dd6823b318a43acd9179d597cebaac91f2c8d6a0"
  synced_at: "2026-09-17T17:02:01Z"
---

# Configure the Interface

This file is the self-contained Claude Code realization of the portable `configure` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-configure` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Role

Configure prepares the operational Config records and the declared technical environment that the remaining Interface workflow depends on. It first establishes the required Interface and Target Understanding, then creates or reconciles the four operational Config files from their Schemas, and finally installs declared technical requirements and prepares the selected Platform Environment.

Configure never stores Target interpretation in Config and never performs product implementation. Its Target Understanding is limited to the information needed by Config generation and by the declared technical and Environment requirements. Configure never provisions, transfers, or installs an Agent Skill, plugin, or other Agent capability — that belongs entirely to the install mode of the Agent Native Skill (`/my-interface-agent-native 3`).

## Input

Accept no phase selection. Configure always operates on the complete operational Config and the selected Environment. When `$ARGUMENTS` is not empty, make no changes, report that Configure accepts no phase or scope input, and ask the Human to invoke it without arguments.

## Workflow

### 1. Understanding

Establish Interface Understanding from the canonical Interface document and follow its routes to the shared Runtime rules, operational Schemas, Config destinations, Implementation authorities, and Platform authorities. Then establish the limited Target Understanding required by this role from the Target sources located by the Interface under their declared precedence: stable phase identifiers and explicit Target and Platform selections. Resolve the selected Environment and Launch Item from explicit Target choices first and Platform defaults second.

### 2. Config generation

For each of the four operational Schemas (`plan.yaml`, `state.yaml`, `review.yaml`, and `application.yaml`):

  1. Read its current structure, initialization instructions, defaults, and update requirements. Derive the initialization method from those instructions rather than assuming a template key or record structure.
  2. When its Config file is absent, generate it according to those instructions.
  3. When its Config file exists, validate it and reconcile only the structural differences required by the Schema.
  4. Preserve every meaningful operational record already held by the file. If a change would discard information that exists nowhere else, leave it in place and report a conflict.
  5. Introduce only Schema-defined initial values and structures. Do not invent operational work, project facts, Target meaning, or technical decisions.
  6. For `application.yaml`, record only the public metadata a Component already publishes. When a declared Component does not yet exist, leave its Manifest section at its Schema default and report it as not yet generated. Never create, scaffold, or populate that Component to obtain its metadata.

State phase records are synchronized as part of generating `state.yaml`: create missing records from stable Target phase identifiers and current initial values, preserve existing progress, remove a stale record only while it contains nothing but initialization defaults, and otherwise preserve and report it. The same Schema-driven process applies to `application.yaml`; its component sections are part of that Schema and are created or reconciled in the same way. None of the four files is a temporary or optional side file.

### 3. Requirements and Environment preparation

Read all applicable Implementation Component Principles and Preferences, the selected Platform Preferences and Launch Item, and the public Component requirements exposed through the Interface. Resolve every applicable language, package-management, package, database, tool, platform, and version selection from those authorities before installation. Inspect every applicable Platform Component definition and apply its declared system requirements for the selected Launch Item.

Inspect the Environment before changing it and apply only missing declared requirements. Install or reconcile every required resolved technical item at project scope, preserve requirements already satisfied, and record each resolved item's concrete version and verification result. Never infer or invent a dependency, never remove or reverse existing Environment preparation, and never provision, transfer, or install an Agent Skill, plugin, or other Agent capability.

Use the selected Environment definition and compatible explicit Target requirements as the authority for system preparation.

### 4. Validation and outcome

Validate all four Config files against their applicable Schemas, verify phase identity reconciliation, verify every resolved technical item and its concrete version, and observe every Platform Environment requirement claimed as satisfied. Record this invocation's active Configure position and append its operational outcome under State ownership. Report created, installed, reconciled, preserved, already-satisfied, conflicted, and blocked results.

Repeating Configure against unchanged Schemas, Target identity, Config, resolved technical selections, and Platform Environment is idempotent: it makes no structural or installation mutation while still recording the current invocation as State permits.

## Stopping conditions

Stop, or preserve the affected item unchanged, when:

- reconciliation would lose meaningful operational records;
- a required Environment choice is unresolved;
- preparation would exceed Configure's authority; or
- a genuine preparation condition cannot be resolved safely.

Record each such condition as a Blocker through State and report it. Independently valid items continue to be generated, reconciled, or prepared.

## Boundaries

Perform only Configure's role. Do not launch the Target, plan, develop, review, reset, store Target Understanding, or create or modify any other Interface source or product implementation. Never provision, transfer, or install an Agent Skill, plugin, or other Agent capability; the install mode of the Agent Native Skill owns all of that. Never create, scaffold, or populate an Implementation Component root, package, source file, test, or lockfile; Component generation belongs to Developing. System preparation is limited to the selected Launch Item's declared requirements; it grants no authority over product implementation. Configure writes only the four operational Config files and the project-scoped technical or Environment state authorized by their sources.

## Report

Report in this order:

1. **Config** — the status of all four files, including `application.yaml`, and any records created, reconciled, or already valid.
2. **Phase synchronization** — phase records added, preserved, or left as conflicts.
3. **Environment and requirements** — the selected Environment and Launch Item, and each requirement's resolved concrete version, installation or preparation status, and verification result.
4. **Preserved records** — existing operational information carried through unchanged.
5. **Conflicts and blockers** — anything that could not be reconciled or prepared safely, and what it prevents.
