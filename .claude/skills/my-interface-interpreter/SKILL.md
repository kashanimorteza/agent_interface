---
name: my-interface-interpreter
description: Generate or refresh complete structured project Understanding in all outputs required by the current Interface. Use for explicit interpretation, configuration generation, refresh, or reconciliation requests.
disable-model-invocation: true
---

# Interpret the project

## Role

Interpret the human project definition and produce or refresh the shared structured Project Understanding. This is the generation operation: downstream Planning turns its outputs into Tasks, Development executes those Tasks, and Review checks the implementation against the resolved requirements. Supply enough complete, consistent context for those consumers to work without independently resolving the human definition or creating competing configuration.

## Workflow

After establishing both shared Understandings, use the resources located through the shared bootstrap to read the current human project definition and its applicable source rules, defaults, and formats. Build the target-project Understanding and identify the full set of required generated outputs, their validation requirements, destinations, and ownership boundaries. Discover these from the current sources rather than assuming a fixed organization or list of outputs. Inspect existing generated content for reconciliation, not as a substitute for reading the current definition.

For each required output, build a complete candidate that expresses the current project intent under its applicable rules, uses defined defaults where intent leaves choices open, and follows its required format. An empty optional source contributes no information and does not remove a required output; handle a missing required source according to the current rules. Resolve unspecified details through the shared decision policy.

Build the complete candidate set before writing. Validate every candidate against the requirements discovered for it, check that every required output is covered, and cross-check the set for consistency and downstream readiness. Write valid results only to their discovered authorized destinations.

On every run, rebuild from the current Interface and target project rather than treating existing generated content as source truth. Reconcile the valid candidate with existing outputs: add new information, update changed information, remove stale interpreter-owned information, and preserve information owned by the human, runtime, or another operation.

The operation is idempotent: unchanged current sources and owned generated information produce no changes.

## Boundaries

Interpret only. Prepare Understanding for downstream Planning and Development, but do not create implementation Tasks or execute them. Do not review implementations, clear data, reset workflow, modify human-owned sources, or change Interface authorities.

Report created, updated, removed, unchanged, and preserved outputs; validation results; consequential decisions; and only the questions or blockers required by the current policies.
