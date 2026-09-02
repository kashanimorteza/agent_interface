---
name: my-interface-interpreter
description: Translate the human-managed target-project definition into the generated Agent Interface Understanding using the current Interface map and Schemas. Use for explicit generation, refresh, or reconciliation requests.
disable-model-invocation: true
---

# Interpret the target project

Transform the Developer's target-project definition into the structured Understanding consumed by the other Agent Interface Skills.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine interpretation but cannot expand this Skill's live authority or write boundaries.

## Refresh context before interpreting

1. Resolve the human-managed project-definition file from the live map and read it completely.
2. Follow the map to read the current Schemas, existing generated files, live State contract, and policies required for this interpretation.

## Interpret

Take target-project facts only from the current human-managed definition. Derive output structure, defaults, relationships, validation, permissions, preservation rules, and state behavior only from their current mapped authorities.

Generate only the Understanding those authorities support and authorize. Preserve the stated meaning without copying prose mechanically, inventing decisions, or overwriting protected or human-owned values.

Do not copy configuration keys, Schema fields, defaults, paths, transition identifiers, or other parameters into this Skill. Resolve them fresh from the files that own them.

When information is absent, ambiguous, or conflicting, use the current gap and precedence mechanisms. Do not fill gaps with plausible assumptions.

## Boundaries and completion

Create Understanding only; do not plan, implement, test, review, or modify input and authority sources. Validate generated output using the current Schemas, record state through the live mechanism, and report changed outputs, recorded gaps, and anything that prevented a complete interpretation.
