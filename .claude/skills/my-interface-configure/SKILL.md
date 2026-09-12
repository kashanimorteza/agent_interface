---
name: my-interface-configure
description: Generate or refresh operational Config, synchronize phase State, and prepare the selected Platform Environment.
disable-model-invocation: true
---

# Configure the Interface

This file is the Claude Code adapter for the portable `configure` Skill Contract. Resolve and read that Contract through Agent Skill Preferences before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Generate and maintain the operational Config files required by Agent Interface, synchronize aggregate State with current Target phase identifiers, and prepare the selected Platform Environment.

Configure never stores Target interpretation in Config. Its Target Understanding is limited to resolving stable phase identities and any explicit Platform selection or Environment requirement that overrides the Platform defaults.

## Workflow

First establish Interface Understanding from the canonical Interface document and follow its routes to the shared Skill rules. Then establish the limited Target Understanding required by this role from the Target Technical Definition located by the Interface. Use the Interface to locate operational Schemas, Config destinations, Target phase identities, and current Platform authorities. Resolve the selected Environment from explicit Target choices first and Platform defaults second.

For each operational Schema:

1. Read its current structure, initialization instructions, defaults, and update requirements. Derive the initialization method from those instructions rather than assuming a template key or record structure.
2. When its Config file is absent, generate it according to those initialization instructions.
3. When its Config file exists, validate it against the applicable Schemas and reconcile structural differences according to their current requirements, including additions and removals where those requirements call for them.
4. Preserve every operational record a Config file already holds — the owning Schema states what those are — throughout. Never drop operational data to satisfy a structural change: when a field the Schema no longer defines still carries information that exists nowhere else, surface it as a conflict and leave that part of the file unchanged, because a structural tidy-up that loses recorded work costs more than the untidiness it removes.
5. Introduce only the initial values and structural changes required by the applicable Schemas. Do not invent operational work, project facts, or technical decisions.

Synchronize State phase records with the stable phase identifiers currently defined by Target. Create missing records at their Schema defaults and preserve existing progress. Never copy phase titles, goals, targets, status, readiness, or other Target meaning into State. Remove a stale phase record only while it still contains initialization defaults; preserve and report any removed phase carrying meaningful progress or provenance.

Inspect the selected Environment before changing the system. Apply only missing Environment requirements, preserve requirements already satisfied, and use the Environment definition and any compatible explicit Target requirements as the complete authority for system preparation. Record a genuine unresolved preparation condition through State.

Record this invocation's active position and append its operational outcome according to State.

Validate every Config file against its applicable Schemas. Repeating the run against valid current files makes no structural changes and preserves existing work; recording the current invocation follows the owning Component's rules independently of structural reconciliation.

## Boundaries

Perform only Configure's role. Do not launch the Target, plan, develop, review, reset, store Target Understanding, or edit human-owned Interface sources. System preparation is limited to the selected Environment; it grants no authority over product implementation.

## Report

Report in this order:

1. **Config** — each resolved Config file and whether it was created, updated, or already valid.
2. **Phase synchronization** — phase records added, preserved, or left as conflicts.
3. **Environment** — the selected Environment, requirements already satisfied, and preparation performed.
4. **Preserved records** — existing operational information carried through unchanged.
5. **Conflicts and blockers** — anything that could not be reconciled or prepared safely.
