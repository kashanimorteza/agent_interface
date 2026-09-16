---
name: my-interface-configure
description: Generate or refresh operational Config, synchronize phase State, and prepare the selected Platform Environment when explicitly requested by the Human or delegated by a declared Interface coordinator.
disable-model-invocation: true
---

# Configure the Interface

This file is the self-contained Claude Code realization of the portable `configure` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Role

Configure prepares the project for the remaining Interface workflow. It first establishes the required Interface and Target Understanding, then creates or reconciles the four operational Config files from their Schemas, and finally installs declared technical requirements and prepares the selected project Environment for Development.

Configure never stores Target interpretation in Config and never performs product implementation. Its Target Understanding is limited to the information needed by Config generation and by the declared technical and Environment requirements. After installing technical requirements, Configure also runs the declared skill-provisioning mechanism so Skills named by Implementation's `agent_skills` associations become usable before later operations need them.

## Workflow

### 1. Understanding

Establish Interface Understanding from the canonical Interface document and follow its routes to the shared Runtime rules, operational Schemas, Config destinations, Implementation authorities, and Platform authorities. Then establish the limited Target Understanding required by this role from the Target sources located by the Interface under their declared precedence. Resolve the selected Environment from explicit Target choices first and Platform defaults second.

### 2. Config generation

For each of the four operational Schemas (`plan.yaml`, `state.yaml`, `review.yaml`, and `application.yaml`):

  1. Read its current structure, initialization instructions, defaults, and update requirements. Derive the initialization method from those instructions rather than assuming a template key or record structure.
  2. When its Config file is absent, generate it according to those instructions.
  3. When its Config file exists, validate it and reconcile only the structural differences required by the Schema.
  4. Preserve every meaningful operational record already held by the file. If a change would discard information that exists nowhere else, leave it in place and report a conflict.
  5. Introduce only Schema-defined initial values and structures. Do not invent operational work, project facts, Target meaning, or technical decisions.

State phase records are synchronized as part of generating `state.yaml`: create missing records from stable Target phase identifiers and Schema defaults, preserve existing progress, and report stale records that contain meaningful provenance instead of silently deleting them. The same Schema-driven process applies to `application.yaml`; its component sections are part of that Schema and are created or reconciled in the same way.

### 3. Requirements and Environment preparation

Read the applicable Implementation and Platform Preferences and public Component requirements exposed through the Interface. Resolve declared packages, languages, tools, versions, and Environment requirements. Install or remove only explicitly declared project-scoped requirements, preserve requirements already satisfied, and report each result. Never infer or invent a dependency or removal.

Use the selected Environment definition and compatible explicit Target requirements as the authority for system preparation. Record any unresolved preparation condition as a blocker through State.

### 4. Skill provisioning

After resolving and installing the declared technical requirements, run the skill-provisioning mechanism the applicable Language Item declares, so Skills named by Implementation's `agent_skills` associations become usable before later operations need them. Resolve those names from the applicable Implementation authorities only; never enter or resolve an Agent Module source. Report a named Skill that remains unavailable; never adopt a Skill that no association names, and never remove an existing Skill. An unavailable Skill never blocks Configure or fails its verification — preparation continues and the unavailability is reported for the later operation that needs it.

### 5. Validation and outcome

Validate all four Config files against their applicable Schemas. Record this invocation's active position and append its operational outcome according to State. Report created, updated, preserved, conflicted, installed, removed, already-satisfied, and blocked results.

Repeating Configure against unchanged valid sources is idempotent: it makes no unnecessary structural or Environment changes while still recording the current invocation according to State.

## Boundaries

Perform only Configure's role. Do not launch the Target, plan, develop, review, reset, store Target Understanding, or edit human-owned Interface sources. System preparation is limited to the selected Environment; it grants no authority over product implementation. Configure writes only the four operational Config files and the project-scoped technical or Environment state authorized by their sources.

## Report

Report in this order:

1. **Config** — the status of all four files, including `application.yaml`, and any records created, updated, or already valid.
2. **Phase synchronization** — phase records added, preserved, or left as conflicts.
3. **Environment and requirements** — the selected Environment, each requirement's resolved version and preparation status, and any removal performed.
4. **Skill provisioning** — Skills named by applicable `agent_skills` associations that became usable, and any named Skill that remains unavailable.
5. **Preserved records** — existing operational information carried through unchanged.
6. **Conflicts and blockers** — anything that could not be reconciled or prepared safely.
