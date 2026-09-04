---
name: my-interface-interpreter
description: Translate the current human-managed project definition into the generated Agent Interface configuration. Use for explicit generation, refresh, or reconciliation requests.
disable-model-invocation: true
---

# Interpret the project

Convert the human project definition into the structured project Understanding consumed by downstream operations.

## Bootstrap

Read `.interface/root.yaml`. This is the only Interface path this Skill may assume. Follow its current map and read order to discover every source, output, Schema, Policy, Preference, authority, and preservation rule required for this run.

Re-read required sources on every invocation. Do not rely on remembered paths, fields, defaults, file shapes, authorities, or conclusions. Do not scan unrelated project files for project intent.

## Interpret

Treat the human-managed definition as the source of project intent and facts. Treat the currently mapped Interface files as the source of output structure, defaults, validation, ownership, preservation rules, and write authority. Apply the shared Claude decision policy from the project Rules.

Generate or reconcile only the configuration that the live Interface requires and authorizes. Derive every output file, section, field, relationship, default, and state change from its current owner; do not encode their present shape in this Skill.

Preserve protected and human-owned content according to current policy. Resolve missing, ambiguous, or conflicting information exactly as the live decision and gap policies direct. Never use interpretation to invent project intent or to widen the authorized scope.

Validate every generated output against its current Schema and record the run through the live State mechanism.

## Boundaries

Interpret only. Do not plan work, implement code, review results, clear data, reset workflow, modify the human project definition, or change Interface authorities.

Report generated and preserved outputs, validation results, and only the questions or blockers required by the current policies.
