---
name: my-interface-developer
description: Execute and reconcile eligible planned work for one requested project phase from current generated Project Understanding and planning output. Implements and verifies only; never plans or reviews.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Develop one project phase

## Role

Implement and verify eligible planned work for one requested project phase. Use the current planning output and shared generated Project Understanding as the resolved specification. Do not plan new work. Select the phase by the number in `$ARGUMENTS`.

## Input

Accept one positive integer: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in the current generated Project Understanding and use that phase's existing identifier to locate its Plan and throughout development. The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files.

## Workflow

Using the shared bootstrap, locate and read the requested phase's current planning output, the generated configuration needed for execution, and the current authorities governing Development. Inspect the existing implementation as execution context and evidence, not as a replacement definition of project intent.

Derive work selection, ordering, eligibility, progress updates, evidence handling, validation, ownership, and write boundaries from those live authorities. Do not assume or reproduce their current fields, statuses, or policies in this Skill.

Execute eligible planned work within the resolved scope and current authority. Apply the shared decision policy to unspecified implementation details, while preserving project intent, existing interfaces, and decisions recorded in generated Project Understanding.

Verify each result and record execution progress and evidence exactly as required by the live authorities. When work cannot complete, preserve truthful state and follow the current failure, question, and blocking policies.

After each outcome, reconcile Development-owned information and continue according to the current execution rules.

The operation is repeatable and idempotent according to the current execution and ownership rules.

## Boundaries

Develop only eligible planned work in the requested phase. Do not perform Planning, Review, or Interpretation, alter generated Project Understanding, bypass resolved interfaces, or write outside Development's current authority.

Report the result according to the current reporting rules.
