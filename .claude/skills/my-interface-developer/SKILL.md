---
name: my-interface-developer
description: Execute and reconcile eligible planned work for one requested project phase from its current implementation-ready Plan. Implements and verifies only; never plans, reviews, or interprets the human project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Develop one project phase

Execute the unfinished eligible work for the project phase named in `$ARGUMENTS`.

## Workflow

With current Interface Understanding and target-project Understanding established, identify the Developer's live role and resolve the requested phase, its target, its current Plan, the applicable generated configuration, the implementation boundary, and the current Task and State authorities. Enter the workflow state required for this operation.

Derive eligibility from the current Plan and live Task rules. Skip work already complete, work whose dependencies are incomplete, and work outside the requested phase. Select an eligible unfinished Task, claim it through its authorized state transition, and re-read the information that can affect its execution.

Before editing, inspect the Task's declared inputs, affected resources, constraints, existing implementation, and the interfaces it must preserve. Implement only the Task's resolved outcome within its authorized Component boundary. Use professional judgment for unspecified implementation details, but do not expand phase scope, invent project intent, reshape the Plan, or replace decisions recorded in generated Project Understanding.

Run the Task's current verification and compare the observable result with its acceptance criteria. Mark a Task complete only after its required verification passes, and append the actual evidence to its Task-local history. When verification fails, preserve the truthful unfinished state and record useful evidence. Raise a Blocker or Open Question only when the current policies require one.

After every Task outcome, reconcile the live Task and State information owned by Development, then continue through other eligible work in the requested phase while the live rules allow it. Failure or blocking of one Task prevents only work that truly depends on it; independent eligible work may continue when safe.

The operation is repeatable and idempotent with respect to completed work: rerunning Development skips valid completed Tasks, resumes eligible unfinished Tasks, and never repeats or rewrites completed implementation without an explicit current Task requiring that change.

## Boundaries

Develop only the eligible Tasks in the requested phase. Do not create or reshape Plans, reinterpret the human project definition, review as another role, modify generated Project Understanding, bypass declared interfaces, or write outside the resolved implementation and workflow boundaries.

Report claimed, completed, resumed, skipped, failed, and blocked work; the observable verification evidence for every completed Task; consequential implementation decisions; remaining eligible work; and only the questions or blockers required by the current policies.
