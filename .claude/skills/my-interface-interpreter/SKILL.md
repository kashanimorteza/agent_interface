---
name: my-interface-interpreter
description: Translate the current human-managed project definition into the generated Agent Interface configuration. Use for explicit generation, refresh, or reconciliation requests.
disable-model-invocation: true
---

# Interpret the project

Convert the human project definition into the structured project Understanding consumed by downstream operations.

## Bootstrap

Read `.interface/map.yaml`. This is the only Interface path this Skill may assume. Follow its live structure, logical item mappings, and read order to discover the human-managed source, generated outputs, applicable Principles, optional Preferences, Schemas, file policies, write authorities, preservation rules, and validation dependencies required for this run. Do not assume that every item has every layer.

Re-read required sources on every invocation. Do not rely on remembered paths, fields, defaults, file shapes, authorities, or conclusions. Do not scan unrelated project files for project intent.

## Interpret

Treat the mapped human-managed definition as the source of project intent and facts. Treat each output's currently mapped owners as the source of its principles, technical defaults, structure, validation, ownership, preservation rules, and write authority. Apply the shared Claude decision policy from the project Rules.

Generate or reconcile only the configuration that the live Interface requires and authorizes. Derive every output file, section, field, relationship, default, and state change from its current owner; do not encode their present shape in this Skill.

Preserve protected and human-owned content according to its current owner. Resolve missing, ambiguous, or conflicting information through the shared decision policy and the applicable mapped owners. Never use interpretation to invent project intent or to widen the authorized scope.

Resolve and cross-check the complete candidate Understanding before writing. Validate every generated output against all of its applicable mapped Schemas, and apply only the write authorities and transitions discovered from their current owners. Preserve any live runtime authority or state that generation is not explicitly authorized to change.

## Boundaries

Interpret only. Do not plan work, implement code, review results, clear data, reset workflow, modify the human project definition, or change Interface authorities.

Report generated and preserved outputs, validation results, and only the questions or blockers required by the current policies.
