---
name: my-interface-implement
description: "Implement the current Target through a fixed sequence: Configure, then Plan, Develop, and independently Review every active ready phase, then Launch."
disable-model-invocation: true
---

# Implement the Target

## Role

Implement an already defined Target end to end through a fixed orchestration sequence. Implement coordinates other operation Skills, while each operation keeps its own role, authority, validation, and reporting rules.

## Workflow

Establish Interface Understanding and Target Understanding from the current authoritative sources located through the Interface document. Read the shared Skill rules and resolve phase eligibility, the current Skills for Configure, Planning, Development, Review, and Launch, their operational records, and their stopping conditions.

A phase is implementable only when Target marks it both enabled and ready for implementation. Preserve disabled, designing, and not-designed phases unchanged and report them as outside the current run.

Implement does not read, derive, or follow the Interface Workflow. Its sequence is fixed:

1. Execute Configure once.
2. Resolve implementable phases in Target order.
3. For each implementable phase, execute Planning, Development, and then independent Review for that phase before moving to the next phase.
4. When Review is `not satisfied`, run another Planning and Development reconciliation for that phase using the recorded Findings, then review it again. Continue only while each cycle makes observable progress. Stop with a truthful blocked result when a cycle repeats an unresolved Finding, produces no progress, or requires a Human decision.
5. Execute Launch once after every implementable phase has completed Development and reached a `satisfied` Review outcome.

Locate each operation's current Skill through the Interface, read its instructions, and execute them directly; do not depend on nested Slash Command invocation. After Configure makes State available, record Implementation State as `in progress`, set this run's start provenance, and append its State History Event.

Do not continue when the current operation's prerequisites or progression gates are incomplete. A missing, inconclusive, or not-satisfied Review outcome is an incomplete phase gate. Record Implementation State as `blocked`, append the outcome, and report the stopping condition through its owner.

After every implementable phase is independently satisfied and Launch completes, record Implementation State as `completed`, its completion time, and the outcome History Event.

Repeated invocation reconciles the current Target with existing operational records and implementation according to the individual operation rules; it does not discard completed work merely to repeat the sequence.

## Boundaries

Implement coordinates operation roles and performs no product operation of its own. Its only independent write authority is its Implementation State and History under State. It does not define the Target, replace an operation's judgment, combine ownership boundaries, or bypass required human approval.

## Report

Report eligible and skipped phases, each operation outcome in implementation-sequence order, the stopping point when incomplete, all Blockers and Open Questions, and the final Implementation and Launch result.
