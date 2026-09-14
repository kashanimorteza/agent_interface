---
name: my-interface-configure
description: Generate or refresh operational Config, synchronize phase State, and prepare the selected Platform Environment when explicitly requested by the Human or delegated by a declared Interface coordinator.
disable-model-invocation: false
---

# Configure the Interface

This file is the self-contained Claude Code realization of the portable `configure` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Role

Generate and maintain the persistent `.interface/foundation/config/application.yaml` Application Manifest and the operational Config files required by Agent Interface, synchronize aggregate State with current Target phase identifiers, and prepare the selected Platform Environment.

Configure never stores Target interpretation in Config. Its Target Understanding is limited to resolving stable phase identities and any explicit Platform selection or Environment requirement that overrides the Platform defaults.

## Workflow

First establish Interface Understanding from the canonical Interface document and follow its routes to the shared Skill rules. Then establish the limited Target Understanding required by this role from the Target sources located by the Interface under their declared precedence. Use the Interface to locate operational Schemas, Config destinations, Target phase identities, and current Platform authorities. Resolve the selected Environment from explicit Target choices first and Platform defaults second.

For each operational Schema:

1. Read its current structure, initialization instructions, defaults, and update requirements. Derive the initialization method from those instructions rather than assuming a template key or record structure.
2. When its Config file is absent, generate it according to those initialization instructions.
3. When its Config file exists, validate it against the applicable Schemas and reconcile structural differences according to their current requirements, including additions and removals where those requirements call for them.
4. Preserve every operational record a Config file already holds — the owning Schema states what those are — throughout. Never drop operational data to satisfy a structural change: when a field the Schema no longer defines still carries information that exists nowhere else, surface it as a conflict and leave that part of the file unchanged, because a structural tidy-up that loses recorded work costs more than the untidiness it removes.
5. Introduce only the initial values and structural changes required by the applicable Schemas. Do not invent operational work, project facts, or technical decisions.

Create or reconcile `.interface/foundation/config/application.yaml` on every Configure run from the Application Manifest Schema. Build its Component sections from the current Development Component Profiles and public metadata exposed by each Component. Include a section for every declared Implementation Component even when that section is empty. Preserve public metadata that remains valid, reconcile stale metadata from its authoritative source, and report conflicts rather than silently discarding meaningful information. Keep the Manifest limited to non-secret composition metadata: Component identity, repository-relative root, Component Type, public entrypoint or interface metadata, and declared Connections. Never write Target meaning, private implementation details, internal storage structure, credentials, secret values, or undeclared dependencies into it.
When a Component is generated or configured, publish its non-secret `package_name` when applicable, repository-relative `path`, `public_entrypoint` when applicable, and `public_interface` metadata in that Component's section.

Synchronize State phase records with the stable phase identifiers currently defined by Target. Create missing records at their Schema defaults and preserve existing progress. Never copy phase titles, goals, targets, status, readiness, or other Target meaning into State. Remove a stale phase record only while it still contains initialization defaults; preserve and report any removed phase carrying meaningful progress or provenance.

Inspect the selected Environment before changing the system. Apply only missing Environment requirements, preserve requirements already satisfied, and use the Environment definition and any compatible explicit Target requirements as the complete authority for system preparation. Record a genuine unresolved preparation condition through State.

Record this invocation's active position and append its operational outcome according to State.

Validate every Config file against its applicable Schemas. Repeating the run against valid current files makes no structural changes and preserves existing work; recording the current invocation follows the owning Component's rules independently of structural reconciliation.

## Boundaries

Perform only Configure's role. Do not launch the Target, plan, develop, review, reset, store Target Understanding, or edit human-owned Interface sources. System preparation is limited to the selected Environment; it grants no authority over product implementation. The Application Manifest Config is the sole additional generated output owned by Configure.

## Report

Report in this order:

1. **Application Manifest** — whether `.interface/foundation/config/application.yaml` was created, updated, or already valid, and its public sections.
2. **Config** — each resolved Config file and whether it was created, updated, or already valid.
3. **Phase synchronization** — phase records added, preserved, or left as conflicts.
4. **Environment** — the selected Environment, requirements already satisfied, and preparation performed.
5. **Preserved records** — existing operational information carried through unchanged.
6. **Conflicts and blockers** — anything that could not be reconciled or prepared safely.
