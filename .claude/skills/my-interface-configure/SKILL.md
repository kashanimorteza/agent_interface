---
name: my-interface-configure
description: Generate or refresh the operational Config files from their Schema templates. Use when Interface Config must be created, or brought to the current operational structure after a Schema change.
disable-model-invocation: true
---

# Configure the Interface

## Role

Generate and maintain the operational Config files required by Agent Interface. Resolve which they are from the Interface document rather than counting on a fixed set, because a Component that gains a Config record adds one without this Skill changing.

Configure is mechanical. It brings the stored files to the shape their Schemas currently define and changes nothing about what the project means, because interpreting the project is another operation's work and a Config file that carries interpretation would compete with the sources that own it.

## Workflow

First establish Agent Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand Configure's role and locate the common YAML Schema, every operational Schema, and each one's Config destination. Target Project Understanding is not required, because Configure does not interpret the project being built.

For each operational Schema:

1. Read its complete `initial` template and its declared defaults.
2. When its Config file is absent, generate it by copying the initial template.
3. When its Config file exists, validate its common file frame and its operational content, then bring it to the current Schema in both directions: add the structural defaults the Schema defines and the file lacks, and remove the fields the Schema no longer defines. A Schema that has narrowed is the only way a stored file sheds a field it no longer needs, so the removal direction matters as much as the addition.
4. Preserve every operational record a Config file already holds — the owning Schema states what those are — throughout. Never drop operational data to satisfy a structural change: when a field the Schema no longer defines still carries information that exists nowhere else, surface it as a conflict and leave that part of the file unchanged, because a structural tidy-up that loses recorded work costs more than the untidiness it removes.
5. Create no operational record of any kind — no Plan, Group, Task, Blocker, Open Question, Review, or Finding — and no project description or technical Component configuration. Those belong to the operations that own them, and inventing an empty one here would look like real work to whatever reads the file next.

Validate every Config file against the common YAML Schema and its owning Schema. A second run against valid current files makes no changes.

## Boundaries

Configure only. Do not produce or store Target Project Understanding, create planning work, change operational progress, implement the project, review implementation, reset the workflow, or edit human-owned Interface sources.

## Report

Report in this order:

1. **Each Config file** — every operational Config resolved from the Interface document, each reported as created, updated, or already valid, with the Schema it was validated against.
2. **What changed** — the structural defaults added and the obsolete fields removed, per file. State "no change" explicitly when nothing changed.
3. **Preserved operational data** — what existing work was carried through unchanged.
4. **Conflicts** — any structural change that could not be applied without losing information, what the information is, and where it currently lives. Report these even when everything else succeeded.
