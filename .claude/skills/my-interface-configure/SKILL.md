---
name: my-interface-configure
description: Core Interface Skill "configure" — creates and reconciles the three declared Config records (Application, Plan, State) under .interface/config/ from their current Schemas, then records its Configure Log Entry in State. Use when the Config records must be created or restored to Schema conformance, or when another Interface Skill reports missing or invalid Config.
---

<!-- Synchronized by /my-interface-agent-native from the Configure Skill Contract and its Sources. Do not edit here; this Skill is a Runtime realization, never an authority. -->

# Configure

The Core Skill for configuring. Stable key: `configure`. Required.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-configure`) or by an Agent (for example the Implement coordinator).
- Input: an invocation request. When a coordinator supplies a parent Log identifier, record it as `parent_id` in this execution's Log Entry.

## Before acting

1. Apply the project Rules `interface-bootstrap`, `interface-skill-policy`, and `git-discipline` (`.claude/rules/`). Never read `.interface/agent/`.
2. Read the current Operation authorities in full — they govern over this summary if they differ:
   - `.interface/implementation/operations/configure/configure.md` (Definition and mandatory Principle)
   - `.interface/implementation/operations/configure/configure.yaml` (Preferences: Config directory and record-to-Schema mappings)
3. Read only the Schemas those Preferences declare, plus the general YAML file structure — nothing else. Configure needs no Target Understanding and never inspects Source.

## File generation

Each specialized Config Schema defines only its own record and file-specific generation parameters. Read the general YAML file structure from `.interface/foundation/schema/yaml.yaml` separately and compose it with the specialized Schema; a generated file must conform to both layers. Specialized Schemas never copy the general YAML structure.

- Application: `.interface/foundation/schema/application.yaml`
- Plan: `.interface/foundation/schema/plan.yaml`
- State: `.interface/foundation/schema/state.yaml`

Resolve the Config directory, record file names, and Schema paths from the current Configure Preferences; the list above must match them, and the Preferences govern if they differ.

## Workflow

1. For each declared record, generate it in the Config directory from its current Schema (initial content placed inside the general YAML structure, with the Schema's generation values), preserving the explanatory comments each Schema defines.
2. When a record already exists, preserve its valid operational content and change only what is required to restore Schema conformance. Never reset operational data to defaults.
3. Once the State Config is available:
   - record the active Workflow position as `configuring` (`active.mode`, with `mode_reason`, `set_by`, `set_at`);
   - append one Configure Log Entry (see Execution Log). Configure-specific details go in its `data`.
4. Configure is complete when every generated record conforms to its current Schema.

Stop — and record the actual outcome and reason — when a required Schema or mapping is invalid or unavailable, or when a Config record or Log Entry cannot be written.

## Execution Log

At the start of every execution, create one Log Entry in State for that execution with its `id` (next project-wide sequential identifier, zero-padded to at least three digits), `skill: configure`, and `started_at`. At completion, update that same entry with `completed_at`, `duration_ms`, `outcome`, `report`, and any applicable `data`, `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason. Recording this entry does not require State analysis. If State does not yet exist at start, create the entry as soon as the State Config is available.

## Boundaries

- Change only the three declared Config records and this execution's Configure Log Entry in State.
- Never perform another Operation (no Plan, Develop, Review, or Implement work) and never interpret project meaning.
- Never modify any `.interface/` path outside `.interface/config/`.

## Output

The Skill execution result and status: records created, reconciled, or unchanged; Schema conformance evidence; the Log Entry id; and any stop reason.
