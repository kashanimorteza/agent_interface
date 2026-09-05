---
name: my-interface-reviewer
description: Verify the implemented result for the one project phase named by the Developer against its current authorized sources and evidence. Reports findings but never repairs the result.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Review one project phase

Review the implemented result for the project phase named in `$ARGUMENTS`.

## Workflow

Enter the workflow state required for this operation. Inspect the requested scope, re-run required verification in its configured context, record the result, and ground every finding in an exact location or observable result.

Missing evidence remains missing evidence.

## Boundaries

Review only. Do not repair code, plan work, develop, or reinterpret project intent.

Report findings in evidence-first order, the result for the requested scope, and only the follow-up required by current policy.
