---
name: my-interface-configure
description: Agent Interface Core Skill `configure`. Creates or reconciles the three structural Config records (.interface/config/application.yaml, plan.yaml, state.yaml) from their Schemas, records the `configuring` Workflow position, and logs its execution in State. Use when the Human or an Agent asks to configure the Interface, or when Implement finds Config absent or invalid.
argument-hint: "(no arguments)"
---

# Configure — Core Skill `configure`

Synchronized Claude Code realization of the Agent Interface Core Skill with stable key `configure` (required). It was produced by Agent Native Sync and is self-contained: it is not an authority, and it never needs the Agent Module. The Operation's authoritative meaning lives in the Implementation sources named under **Authorities** and is read at run time.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## Invocation and inputs

- Invoked directly by the Human (`/my-interface-configure`) or by an Agent (for example the `my-interface-implement` Skill through the Skill tool).
- Input: the invocation request only. There is no phase selection.
- Output: the Skill execution result and status.

## Standing rules

Apply the project Rules in `.claude/rules/` (interface-bootstrap, interface-skill-policy, git-discipline, interface-agent-capabilities). In particular: `.interface/` is read-only except the exact Config records this Skill owns; never commit; report capability health with the declared status vocabulary.

## Authorities (read at run time, before acting)

1. `.interface/interface.md` — the Interface entry point, only as far as this role needs it.
2. `.interface/implementation/operations/configure/configure.md` — Configure Definition and mandatory Principle.
3. `.interface/implementation/operations/configure/configure.yaml` — Configure Preferences: the Config directory and the record-to-Schema mappings.
4. `.interface/foundation/schema/yaml.yaml` — the general YAML file structure (meta, policy, resolution, read_order, content_map, content).
5. The specialized Schema of each record named by Configure Preferences (currently Application, Plan, and State under `.interface/foundation/schema/`).

If these sources disagree with this summary, the sources win.

## File generation

Each specialized Config Schema defines only its own record and file-specific generation parameters. Read the general YAML structure from `.interface/foundation/schema/yaml.yaml` separately and compose it with the specialized Schema. A generated file must conform to both layers; never copy the general YAML structure into a specialized Schema.

## Procedure

1. Read the Authorities above. Do not read Target sources beyond the minimum the Interface allows Configure (phase identities and Platform selections only when a Schema requires them).
2. For each record declared in Configure Preferences, compose general frame + specialized Schema:
   - missing record → generate it from the Schema's initial content and generation parameters, preserving the Schema's explanatory comments;
   - existing record → preserve its valid operational content and change only what restores Schema conformance; report conflicts instead of discarding meaningful data.
3. As soon as the State Config is available, create this execution's Log Entry (see **Execution log**) and record the active Workflow position as `configuring`.
4. Verify every generated or reconciled record against its current Schema (both layers). Configure is complete only when all conform.
5. Update the Log Entry with the outcome and report.

## Stop conditions

Stop and report (and record in the Log Entry when State is writable) when a required Schema or mapping is invalid or unavailable, or when an authorized Config record or Log Entry cannot be written.

## Execution log

At the start of every execution, create one Log Entry in State for that execution, including its `id`, `skill` (`my-interface-configure`), and `started_at`. At completion, update that same Log Entry with `completed_at`, `duration_ms`, `outcome`, `report`, and any applicable `data`, `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason. Recording this entry does not require State analysis. Use the State Config Schema for field shapes; when invoked by Implement, record the supplied Implement Log identifier as `parent_id`.

## Boundaries

- Writes only the three declared Config records and its own Configure Log Entry (plus the `configuring` Workflow position) inside `.interface/config/`.
- Never performs another Operation, interprets project meaning, or edits any other `.interface/` path.
