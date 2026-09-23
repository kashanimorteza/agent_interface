---
name: my-interface-configure
description: Agent Interface Core Skill `configure`. Creates or reconciles the three structural Config records (Application, Plan, State) in .interface/config/ from their current Schemas, and nothing else. Use when the Human or a coordinating Agent asks to configure the Interface, or when a Core Operation reports that required Config records are missing or invalid.
---

# Configure (`configure`)

The Core Skill for configuring. Required. Stable key: `configure`. Skill name: `my-interface-configure`.

This Skill is a synchronized, self-contained Runtime realization. Its meaning comes from the Configure Operation Definition and Preferences, read fresh on every run; this file never replaces them. Never read or search `.interface/agent/`. If something this Skill needs is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-configure`) or by an Agent (Skill tool), including a coordinating Skill.
- Input: an invocation request. No phase selection applies.
- When invoked by a coordinator, the coordinator supplies its reserved Log identifier; record it as this Log Entry's `parent_id`.

## Workflow

1. **Execution Log — start.** As soon as the State Config can be written (see step 5 for a first run), create one Log Entry for this execution with its `id`, `skill: configure`, and `started_at`. Recording this entry does not require State analysis.
2. **Enter through the Interface.** Read `.interface/interface.md` to locate current resources, as the global `interface-bootstrap` Rule requires. Keep Understanding narrow: use the Interface only to locate the Configure sources and Schemas. Do not read Target sources or Source.
3. **Read the Configure Operation completely** — `.interface/implementation/operations/configure/configure.md` (Definition and mandatory Principle) and `.interface/implementation/operations/configure/configure.yaml` (the Config directory and the record-to-Schema mappings). These are authoritative for Configure's responsibility and limits; if they differ from anything in this file, they win.
4. **Compose the two Schema layers for each declared record.** Each specialized Config Schema defines only its own record and file-specific generation parameters. Read the general YAML file structure separately from `.interface/foundation/schema/yaml.yaml` and compose it with the specialized Schema. A generated file must conform to both layers; specialized Schemas never copy the general structure.
   - Application: `.interface/foundation/schema/application.yaml`
   - Plan: `.interface/foundation/schema/plan.yaml`
   - State: `.interface/foundation/schema/state.yaml`
   Use the record list declared by the Configure Preferences as the authority; the three above are the current mapping.
5. **Generate or reconcile each record** in the declared Config directory. Create a missing record from its Schema's initial content inside the general YAML frame, preserving the explanatory comments the Schemas define. For an existing record, preserve valid operational content and change only what is required to restore Schema conformance; never reset operational data to defaults.
6. **Record the Workflow position.** Once the State Config is available, set the active Workflow position to `configuring`.
7. **Verify.** Re-read each generated record and confirm it conforms to both Schema layers. Configure is complete only when every declared record conforms.
8. **Execution Log — completion.** Update the same Log Entry with `completed_at`, `duration_ms`, `outcome`, a concise `report`, and any applicable `data` (Configure-specific details), Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Stop conditions

Stop — and record the actual outcome and reason in the Log Entry when State is writable — when a required Schema or mapping is invalid or unavailable, or when a Config record or Log Entry cannot be written.

## Boundaries

- Change only the declared Config records inside `.interface/config/` and this execution's own Configure Log Entry. Every other `.interface/` path is read-only.
- Never plan, develop, review, or perform another Operation; never interpret project meaning.
- Never read `.interface/agent/` and never invoke `/my-interface-agent-native`.

## Outputs

The Skill execution result and status: which records were created, reconciled, or already conformant; the verification evidence; the Log Entry `id`; and any Open Questions or Blockers.
