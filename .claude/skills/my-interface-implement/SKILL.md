---
name: my-interface-implement
description: Execute the complete Agent Interface Workflow for the current Target by coordinating its currently declared executable operations in order.
disable-model-invocation: true
---

# Implement the Target

## Role

Coordinate the complete executable Workflow for an already defined Target. Implement is an orchestrator: each operation keeps its own role, authority, validation, and reporting rules.

## Workflow

Establish Interface Understanding and Target Understanding from the current authoritative sources located through the Interface document. Read the shared Skill rules and resolve the current Workflow, enabled phases, operation Skills, operational records, and stopping conditions from their owners.

Coordinate only the executable Agent steps in the ordered Workflow declared by the Interface. A Human-owned step is a prerequisite rather than work for Implement, and the Implement orchestration entry is excluded so the Skill never invokes itself.

For each executable step, locate its current operation Skill through the Interface, read that Skill's instructions, and execute its Workflow directly; do not depend on nested Slash Command invocation. Execute a non-phase step once at its declared position. When consecutive steps operate on individual phases, process them in their declared order for one enabled phase before moving to the next enabled phase. Preserve every operation's current authority boundaries.

Do not continue into an operation whose prerequisites or progression gates are incomplete. Record and report the stopping condition through the authority that owns it.

Repeated invocation reconciles the current Target with existing operational records and implementation according to the individual operation rules; it does not discard completed work merely to repeat the Workflow.

## Boundaries

Implement coordinates other operation roles and performs no independent operation of its own. It does not define the Target, replace an operation's judgment, combine ownership boundaries, or gain independent write authority. It performs changes only through the authority of the operation currently being coordinated and never bypasses required human approval.

## Report

Report the outcome of each operation and phase in Workflow order, the point at which execution stopped when incomplete, all Blockers and Open Questions, and whether the Workflow reached and completed its final executable step.
