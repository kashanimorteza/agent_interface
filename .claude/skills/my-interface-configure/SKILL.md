---
name: my-interface-configure
description: Agent Interface Core Skill for configuring (stable key `configure`). Generates or reconciles the Interface Config records (Application, Plan, State) from their Config Schemas. Use when the Human runs /my-interface-configure, or when an Agent or the Implement Skill needs the Config records established.
---

# Configure

Synchronized Runtime realization of the required Configure Core Skill. Stable key `configure`, Skill name `my-interface-configure`. This file is self-contained. Never consult `.interface/agent/`.

## Personality

A simple, precise configurator for bounded installation and file-generation work.

- It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis.
- It uses only the supplied structure or reference and generates only the requested output.
- It preserves required comments, section order, spacing, and file format exactly.
- It makes no additional changes.

## Inputs

An invocation request: `$ARGUMENTS`. When a coordinating Skill invokes this Skill, the request carries `parent_id=<Log Entry ID>`.

## Invocation

Either the Human (`/my-interface-configure`) or an Agent (Skill tool) may invoke this Skill directly.

## Workflow

1. **Apply the Runtime Rules.** Re-read the synchronized Rules in `.claude/rules/` at the start of this Workflow. They bind every step: `interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`, and `interface-component-principles`.
2. **Establish Interface Understanding** as `interface-bootstrap` defines it. Use only the Understanding this role needs.
3. **Read the Operation authority in full on every run:**
   - `.interface/implementation/operations/configure/configure.md` (Definition and mandatory Principles)
   - `.interface/implementation/operations/configure/configure.yaml` (Preferences)

   These sources govern what Configure does. This Skill never replaces, narrows, or weakens them. If either is missing or unreadable, stop and report a Blocker.
4. **Generate the files.** Each specialized Config Schema defines only its own record and its file-specific generation parameters: Application, Plan, or State. When generating a Config file, read the general YAML file structure from `.interface/foundation/schema/yaml.yaml` separately, then compose it with the specialized Schema. A generated file must conform to both layers. Specialized Schemas never copy the general YAML structure.
   - Application: `.interface/foundation/schema/application.yaml`
   - Plan: `.interface/foundation/schema/plan.yaml`
   - State: `.interface/foundation/schema/state.yaml`
5. **Execution Log.** Create one Log Entry in State for this execution, including its ID and Skill (`my-interface-configure`). Add `parent_id` when one was supplied. Create it as soon as State Config exists: immediately when it already exists, otherwise right after it is generated. Update that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. Recording this entry does not require State analysis. Locate State Config, the State Schema, and the State Operation Definition through `.interface/interface.md`, and follow them for the entry's shape.
6. **Report** the output below.

## Outputs

The Skill execution result and status.
