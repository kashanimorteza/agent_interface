---
name: my-interface-implement
description: Execute the complete Agent Interface Workflow for the current Target by coordinating its currently declared executable operations in order.
disable-model-invocation: true
---

# Implement the Target

## Role

Coordinate the complete executable Workflow for an already defined Target. Implement is an orchestrator: each operation keeps its own role, authority, validation, and reporting rules.

## Workflow

Establish Interface Understanding and Target Understanding from the current authoritative sources located through the Interface document. Read the shared Skill rules and resolve the current Workflow, phase eligibility, operation Skills, operational records, and stopping conditions from their owners.

A phase is implementable only when Target marks it both enabled and ready for implementation. Preserve disabled, designing, and not-designed phases unchanged and report them as outside the current run.

Coordinate only the executable Agent steps in the ordered Workflow declared by the Interface. A Human-owned step is a prerequisite rather than work for Implement, and the Implement orchestration entry is excluded so the Skill never invokes itself.

For each executable step, locate its current operation Skill through the Interface, read that Skill's instructions, and execute its Workflow directly; do not depend on nested Slash Command invocation. Execute any Config initialization step first. At the first point State Config is available, record Implementation State as `in progress`, set this run's start provenance, and append its State History Event. Execute each later non-phase step once at its declared position. When consecutive steps operate on individual phases, process them in their declared order for one implementable phase before moving to the next. Preserve every operation's current authority boundaries.

Do not continue into an operation whose prerequisites or progression gates are incomplete. Record Implementation State as `blocked`, append the outcome, and report the stopping condition through the authority that owns it. Do not automatically retry a failed Review.

After every implementable phase and the final executable Workflow step complete, record Implementation State as `completed`, its completion time, and the outcome History Event.

Repeated invocation reconciles the current Target with existing operational records and implementation according to the individual operation rules; it does not discard completed work merely to repeat the Workflow.

## Boundaries

Implement coordinates operation roles and performs no product operation of its own. Its only independent write authority is its Implementation State and History under State. It does not define the Target, replace an operation's judgment, combine ownership boundaries, or bypass required human approval.

## Report

Report eligible and skipped phases, each operation outcome in Workflow order, the stopping point when incomplete, all Blockers and Open Questions, and the final Implementation and Launch result.
