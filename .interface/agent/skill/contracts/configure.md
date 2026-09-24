# Configure Skill Contract

## What it is

The Core Skill for configuring.

Required. Stable key: `configure`. Skill name: `my-interface-configure`.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## File Generation

Each specialized Config Schema defines only its own record and file-specific generation parameters: Application, Plan, or State. When generating a Config file, this Skill reads the general YAML file structure from `.interface/foundation/schema/yaml.yaml` separately and composes it with the specialized Schema. A generated file must conform to both layers; specialized Schemas never copy the general YAML structure.

- Application: `.interface/foundation/schema/application.yaml`
- Plan: `.interface/foundation/schema/plan.yaml`
- State: `.interface/foundation/schema/state.yaml`

## Inputs

An invocation request.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Execution Log

At the start of every execution, create one Log Entry in State for that execution, including its ID, Skill, and `started_at`. At completion, update that same Log Entry with `completed_at`, `duration_ms`, readable `duration`, outcome, report, and any applicable data, Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason. Recording this entry does not require State analysis.

## Outputs

The Skill execution result and status.

## Source

- `.interface/implementation/operations/configure/configure.md`
- `.interface/implementation/operations/configure/configure.yaml`
