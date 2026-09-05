---
name: my-interface-interpreter
description: Generate or refresh complete project Understanding for every current Interface Component. Use for explicit interpretation, configuration generation, refresh, or reconciliation requests.
disable-model-invocation: true
---

# Interpret the project

Produce complete current project Understanding that downstream Planning can turn into Tasks and Development can execute.

## Workflow

Begin with both current Interface Understanding and current target-project Understanding. Use them to identify the Interpreter's live role, every current Component, each Component's applicable Layers and output, source precedence, validation requirements, and ownership boundaries.

For every Component, build one complete candidate configuration. Apply explicit project intent, enforce its Principles, use its Preferences for choices the project leaves open, and express the result in the form required by its Schema. An empty Layer contributes no information but never removes a required Component output. Use permitted judgment for non-critical unresolved details without inventing project intent.

Build the complete candidate set before writing. Validate each candidate against its current Schema and cross-check the complete set for consistency and downstream readiness.

On every run, rebuild from the current Interface and target project rather than treating existing generated content as source truth. Reconcile the valid candidate with existing outputs: add new information, update changed information, remove stale interpreter-owned information, and preserve information owned by the human, runtime, or another Behaviour.

The operation is idempotent: unchanged current sources and owned generated information produce no changes.

## Boundaries

Interpret only. Prepare Understanding for downstream Planning and Development, but do not create implementation Tasks or execute them. Do not review implementations, clear data, reset workflow, modify human-owned sources, or change Interface authorities.

Report created, updated, removed, unchanged, and preserved outputs; validation results; consequential decisions; and only the questions or blockers required by the current policies.
