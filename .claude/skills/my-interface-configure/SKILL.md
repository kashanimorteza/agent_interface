---
name: my-interface-configure
description: Generate or refresh the Task and State Config files from their Schema defaults. Use when Interface Config must be created or brought to its current operational structure.
disable-model-invocation: true
---

# Configure the Interface

## Role

Generate the two operational Config files required by Agent Interface: Task Config and State Config.

## Workflow

First establish Agent Interface Understanding by reading the canonical Interface document. Use it to understand Configure's role and locate the common YAML Schema, the Task and State Schemas, and their Config destinations. Target Project Understanding is not required because Configure does not interpret the project being built.

For each operational Schema:

1. Read its complete `initial` template and declared defaults.
2. When its Config file is absent, generate it by copying the initial template.
3. When its Config file exists, validate its common file frame and operational content. Preserve existing Tasks, progress, active State, Blockers, and Open Questions, and add only structural defaults missing from the current Schema.
4. Do not create phase Plans, Groups, Tasks, Blockers, Open Questions, project descriptions, or technical Component configuration.

Validate both Config files against the common YAML Schema and their owning Schemas. A second run against valid current files makes no changes.

## Boundaries

Configure only. Do not produce or store Target Project Understanding, create planning work, change operational progress, implement the project, review implementation, reset workflow, or edit human-owned Interface sources.

Report which Config files were created, updated, or already valid, and report any structural conflict that cannot be reconciled without losing existing operational data.
