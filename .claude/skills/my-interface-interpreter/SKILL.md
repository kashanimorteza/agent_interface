---
name: my-interface-interpreter
description: Translate the current human-managed project definition into the generated Agent Interface configuration. Use for explicit generation, refresh, or reconciliation requests.
disable-model-invocation: true
---

# Interpret the project

Convert the mapped human project definition into the generated project Understanding consumed by downstream operations.

## Workflow

Transform the mapped project facts into every generated configuration required by the current Interface.

On every run, rebuild the complete candidate Understanding from the current mapped sources before writing. Reconcile the generated configuration with that candidate so additions and changes in the human project definition are reflected consistently.

Cross-check the complete candidate Understanding and validate every generated output against its mapped Schema.

## Boundaries

Interpret only. Do not plan work, implement code, review results, clear data, reset workflow, modify the human project definition, or change Interface authorities.

Report generated and preserved outputs, validation results, and only the questions or blockers required by the current policies.
