---
name: my-interface-configure
description: Core Skill for configuring. Creates or reconciles the Interface's three structural Config records (Application, Plan, State) from their current Schemas and changes nothing else. Use when Config records must be created, restored to Schema conformance, or established before Plan, Develop, Review, or Implement can run.
argument-hint: "[request]"
---

# Configure (Core Skill)

The Core Skill for configuring. Required. Stable key: `configure`. Skill name: `my-interface-configure`.

This Skill is the Claude Code realization of the Configure Operation. The current Configure Operation Definition and Preferences, located through the Interface, remain the authority for Configure's meaning and mappings; this Skill restates them so it can run. If they disagree with this Skill, follow the current owning source and report Runtime drift so the Human can run Agent Native Sync.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## Invocation and inputs

- May be invoked directly by a Human (`/my-interface-configure`) or by an Agent (for example, coordinated by `my-interface-implement`).
- Input: an invocation request. When coordinated by Implement, the request carries the coordinator's Log Entry ID as `parent_id`; record it on this execution's Log Entry.

## Responsibility and limits

Configure creates and reconciles the three declared Config Records from their current Schemas, and does nothing beyond producing Schema-derived records.

- **Config Schema** — the structure that defines one of the three Config files.
- **Config Record** — a generated Config file that conforms to its Config Schema.

Mandatory Principle — *Configure generates only the declared Config records from their Schemas*:

- Read only the Config Schemas declared by the Configure Preferences, generate only their structurally valid Config Records, preserve the Schemas' comments in the generated records, and preserve valid operational content when reconciling an existing record.
- **Must** — generate each declared Config Record from its current Schema and preserve its comments and valid operational content during reconciliation.
- **Never** — perform another Operation or change anything outside those Config Records. Configure changes only the three declared Config Records.

Configure owns structural creation of Config records only. The Config Schemas own their shapes; later Operations own the operational content written into those records. Preferences supply current mappings but cannot expand Configure's scope.

## Procedure

1. Apply the project Rules loaded as project memory (Interface bootstrap, Interface Skill policy, Git discipline). Enter through the canonical Interface document as the bootstrap Rule requires; beyond that entry, use only the supplied structure (the Configure Preferences and the Schemas they name).
2. **Execution Log — start.** Create one Log Entry in State for this execution, with its ID, Skill (`my-interface-configure`), `started_at`, and `parent_id` when supplied. Recording this entry does not require State analysis. If the State record does not yet exist, generate it first as one of the declared records (step 4), then create the entry with the true `started_at`.
3. Read the current Configure Preferences for the Config directory and the record-to-Schema mappings. Currently declared (verify against the current Preferences):
   - Config directory: `.interface/config/`
   - Application Config → `application.yaml` from `.interface/foundation/schema/application.yaml`
   - Plan Config → `plan.yaml` from `.interface/foundation/schema/plan.yaml`
   - State Config → `state.yaml` from `.interface/foundation/schema/state.yaml`
4. **File generation.** Each specialized Config Schema defines only its own record and file-specific generation parameters (Application, Plan, or State). For every Config file, read the general YAML file structure from `.interface/foundation/schema/yaml.yaml` separately and compose it with the specialized Schema. A generated file must conform to both layers; specialized Schemas never copy the general YAML structure.
   - Missing record → generate it from its composed Schema, preserving the Schemas' comments, section order, spacing, and file format exactly.
   - Existing record → preserve its valid operational content and change only what is required to restore Schema conformance.
5. **Completion.** Configure is complete when every generated record conforms to its current Schema.
6. **Stop** when a required Schema or mapping is invalid or unavailable, or when a Config record cannot be written. Report the exact reason.
7. **Execution Log — completion.** Update the same Log Entry with `completed_at`, `duration_ms`, readable `duration`, outcome, report, and any applicable data, Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Outputs

The Skill execution result and status.
