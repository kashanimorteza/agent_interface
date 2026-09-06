---
name: my-interface-reviewer
description: Verify the implemented result for one requested project phase against its generated specification, Plan, and actual evidence. Reports findings but never repairs the result.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Review one project phase

## Role

Review the implemented result for one requested phase against its shared generated Project Understanding, Plan, and acceptance criteria. Establish whether the available implementation and verification evidence satisfy those resolved requirements; report findings without repairing the result or defining new requirements. Select the phase by the number in `$ARGUMENTS`.

## Input

Accept one positive integer: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in the current generated Project Understanding and use that phase's existing identifier to locate its Plan and throughout review. The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files or running verification.

## Workflow

After establishing both shared Understandings, use the resources located through the shared bootstrap to read the generated specification and Plan needed for the requested phase. Resolve its scope, acceptance criteria, required verification, and permitted reporting destinations from the current sources. Review is a supporting operation and does not enter or change a Workflow mode.

Inspect the implementation and recorded evidence, re-run required verification in its configured context, record the result within the review authority, and ground every finding in an exact location or observable result. Use generated requirements as the review baseline.

Missing evidence remains missing evidence.

## Boundaries

Review only. Do not repair code, plan work, develop, or reinterpret project intent.

Report findings in evidence-first order, the result for the requested scope, and only the follow-up required by current policy.
