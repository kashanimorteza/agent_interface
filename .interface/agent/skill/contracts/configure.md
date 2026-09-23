# Configure Skill Contract

## What it is

The Core Skill for configuring.

Required. Stable key: `configure`. Skill name: `my-interface-configure`.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## File Generation

Each specialized Config Schema defines only its own record: Application, Plan, or State. When generating a Config file, this Skill applies that specialized Schema inside the general YAML file structure defined by `.interface/foundation/schema/yaml.yaml`. A generated file must conform to both layers.

- Application: `.interface/foundation/schema/application.yaml`
- Plan: `.interface/foundation/schema/plan.yaml`
- State: `.interface/foundation/schema/state.yaml`

## Inputs

An invocation request.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Outputs

The Skill execution result and status.

## Source

- `.interface/implementation/operations/configure/configure.md`
- `.interface/implementation/operations/configure/configure.yaml`
