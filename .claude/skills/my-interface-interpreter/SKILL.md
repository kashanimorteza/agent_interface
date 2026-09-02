---
name: my-interface-interpreter
description: Translate the human-managed target-project definition into the generated Agent Interface Understanding using the current Interface map and Schemas. Use for explicit generation, refresh, or reconciliation requests.
disable-model-invocation: true
---

# Interpret the target project

Transform the Developer's target-project definition into the structured Understanding consumed by the other Agent Interface Skills.

## Developer guidance

### Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's role. Treat it as Interface context, not as a source of target-project facts.
- Inspect the repository root and the top-level structure of `.interface/` to understand how the Interface, its generated Config, and mapped target-project locations relate. Inspect structure only at this stage; do not use unrelated repository contents as project knowledge.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map, and select Config files according to the needs of the current interpretation rather than scanning them indiscriminately.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, values, state, configuration, or conclusions from an earlier run.

### Respect the project-knowledge boundary

- This is the only workflow Skill authorized to read the human-managed project-definition file. Resolve that file from the live map and read it completely on every invocation.
- Treat the current human-managed definition as the source of target-project intent and facts. Use Schemas, policies, authorities, and existing generated files only for structure, validation, preservation, reconciliation, and permitted state behavior.
- Do not let implementation files, prior generated output, or remembered context silently add to or replace the Developer's definition.

### Maintain role discipline

- Perform only this Skill's interpretation responsibility. Do not silently plan, develop, review, reset, or invoke another Skill's role.
- Treat the Developer's invocation as authority only for the operation and exact scope defined by this Skill and the live Interface.
- Apply this guidance only within the Skill's live authority and write boundaries.
- If this guidance conflicts with a live policy, authority, Schema, or safety boundary, stop and report the conflict instead of guessing.

### Apply working defaults

- Prefer current source evidence over memory or inference.
- Read and write only the smallest scope required for a complete authorized interpretation.
- Preserve ambiguity as a recorded gap; do not convert it into an invented project decision.
- Ground the result in current mapped sources and validation outcomes.
- Distinguish generated, preserved, blocked, and unresolved content, and identify any decision that remains with the Developer.

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
