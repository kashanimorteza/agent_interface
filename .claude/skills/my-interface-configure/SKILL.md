---
name: my-interface-configure
description: Core Skill for configuring. Creates or reconciles the two operational Config records (Plan Config and State Config in .config/) from their current Config Schemas, and nothing else. Use when the Config records are missing or structurally invalid, or when invoked as /my-interface-configure.
argument-hint: "[request]"
---
<!-- managed by /my-interface-native-implement: realized from the Executor Module Skill Contract `configure`; regenerated on every run — do not edit by hand -->

# Configure

The Core Skill for configuring. Required. Stable key: `configure`. Skill name: `my-interface-configure`.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## Inputs

An invocation request: `$ARGUMENTS` (may be empty).

## Invocation

May be invoked directly by a Human (`/my-interface-configure`) or by an Agent. Among Core Skills, only Implement may invoke it. Configure never invokes another Core Skill; it may use any Provider Skill or other available Skill.

## Authority — read at runtime

The Operation Component Definition and Preferences below are the authority for what Configure does. Read both completely at the start of every run and follow them; the workflow here is the Native realization of that understanding and never overrides them.

- `.interface/implementation/operations/configure/configure.md` — responsibility, limits, and the mandatory Principle.
- `.interface/implementation/operations/configure/configure.yaml` — the Config directory, the general YAML structure, and the record-to-Schema mappings.

The Principle in the Definition is mandatory. Configure Preferences supply current mappings but can never expand Configure's scope; the two Config Schemas and every applicable Principle take precedence over them.

Apply the project Rules (`.claude/rules/`), especially the Skill policy: the `.interface/` tree is read-only; Config records live in `.config/` at the project root.

## Workflow

1. Read the two authority files above. Resolve from the Preferences: the Config directory, the general YAML structure Schema, and each declared record with its file name and Schema.
2. If the State Config record already exists and is structurally valid, create this execution's Log Entry now (see Execution Log); otherwise create it as soon as the State Config record has been generated.
3. For each declared record, read its specialized Schema and the general YAML structure Schema. Compose them so the generated record conforms to both; never copy the general structure into the specialized Schema.
4. Generate the record when it is missing; when it exists, reconcile it with its current Schema, preserving every piece of valid operational content and the Schemas' comments, section order, spacing, and format.
5. Verify that every generated record conforms to its current Schema (and to the general structure).
6. Update the Log Entry with the outcome and report.

Stop and report the exact reason when a required Schema or mapping is invalid or unavailable, or when a Config record cannot be written. On a stop, update the Log Entry with the stopped outcome and reason when the State Config record is writable; otherwise report explicitly that the Entry could not be written.

## Boundaries

- Change only the two declared Config Records. Never change anything outside them — no Source, no Interface file, no other Config file.
- Read only the Config Schemas the Preferences declare. Do not interpret project meaning, plan, develop, inspect Source, or analyse State.
- Later operational content inside a record belongs to the Operation that owns it; preserve it.

## Execution Log

Every execution creates one Log Entry in State (the State Config record) with its `id` and Skill, and updates that same Entry with outcome, report, and any applicable `data`, Open Questions, or Blockers when work completes, stops, or is blocked. Follow the State Component (`.interface/implementation/operations/state/state.md`) and the State Schema for the Entry's shape and the next sequential `id`. When invoked by Implement, use the supplied Implement Log Entry ID as `parent_id`.

Recording the Log Entry does not require State analysis. If the State Config record cannot yet exist (it is the record being generated), write the Entry once it has been generated; if it cannot be written, report that explicitly.

## Outputs

The Skill execution result and status.
