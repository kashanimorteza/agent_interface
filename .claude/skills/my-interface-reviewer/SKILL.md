---
name: my-interface-reviewer
description: Verify the implemented result for the one project phase named by the Developer against its current authorized sources and evidence. Reports findings but never repairs the result.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Review one project phase

Review the implemented result for the project phase selected by the number in `$ARGUMENTS`.

## Input

Accept one positive integer: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in the current generated Project Understanding and use that phase's existing identifier to locate its Plan and throughout review. The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files or running verification.

## Workflow

Enter the workflow state required for this operation. Inspect the requested scope, re-run required verification in its configured context, record the result, and ground every finding in an exact location or observable result.

Missing evidence remains missing evidence.

## Boundaries

Review only. Do not repair code, plan work, develop, or reinterpret project intent.

Report findings in evidence-first order, the result for the requested scope, and only the follow-up required by current policy.
