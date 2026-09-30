---
name: my-interface-configure
description: Core Skill for configuring (stable key `configure`). Creates or reconciles the three declared Interface Config records (Application, Plan, State) in .interface/config/ from their Schemas, composing the general YAML structure with each specialized Schema. Use when the Config records are missing, invalid, or must be restored to Schema conformance. Invocable by the Human (/my-interface-configure) or by an Agent.
---

<!-- Synchronized by Agent Native Sync (/my-interface-agent-native) from the Configure Skill Contract and the Configure Operation Definition and Preferences it names. Change those Human-owned sources and re-run that synchronization; do not edit this copy. -->

# Configure

The Core Skill for configuring. Required. Stable key: `configure`. Skill name: `my-interface-configure`.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## Inputs

An invocation request. When a coordinating Skill supplies a `parent_id`, record it on this execution's Log Entry.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Sources

Read these current Operation sources in full before acting. They are the authority for Configure's responsibility, limits, Config directory, and record-to-Schema mappings; this Skill never copies their facts and never writes to them.

- `.interface/implementation/operations/configure/configure.md` — Configure Definition and its mandatory Principle.
- `.interface/implementation/operations/configure/configure.yaml` — Configure Preferences: the Config directory and each record's file and Schema.

Start from `.interface/interface.md` as the Interface entry point only to locate these resources; do not extend reading beyond what configuring requires.

## Workflow

1. Apply the project Rules (`interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`). If one is missing, report Runtime drift.
2. Note the start time. Read the Sources above and resolve the Config directory and the declared records from Configure Preferences.
3. For each declared record, read the general YAML file structure from `.interface/foundation/schema/yaml.yaml` separately, read the record's specialized Schema, and compose the two layers. Each specialized Schema defines only its own record and file-specific generation parameters; it never copies the general YAML structure.
4. Generate the record when it is absent. When it exists, preserve its valid operational content and change only what is required to restore conformance to both layers. Preserve the Schemas' explanatory comments, section order, spacing, and file format exactly.
5. Execution Log: as soon as the State Config is structurally valid (generated or reconciled in step 4 when it was absent), create this execution's Log Entry in State with its ID and Skill, following the current State Definition (`.interface/implementation/operations/state/state.md`) and State Schema. Recording this Entry does not require State analysis.
6. Verify that every generated or reconciled record conforms to both its general and specialized Schema layers.
7. Update the same Log Entry with the outcome, a concise report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

## Stop conditions

Stop and report the exact reason, recording it as a Blocker on the Log Entry when State is writable, when a required Schema or mapping is invalid or unavailable, or when a Config record cannot be written.

## Boundaries

- Must: generate each declared Config Record from its current Schema, composed with the general YAML structure, and preserve its comments and valid operational content during reconciliation.
- Never: perform another Operation, plan, develop, inspect Source, analyse State, or change anything outside the three declared Config Records in `.interface/config/`. Later operational content belongs to the Operation that owns it.
- Never: write any other `.interface/` path.

## Outputs

The Skill execution result and status. Configure is complete when every generated record conforms to its current Schema.
