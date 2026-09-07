---
name: my-interface-reviewer
description: Verify one implemented project phase against the current project definition, applicable Component authorities, its Task Plan, and actual evidence. Reports findings but never repairs the result.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Review one project phase

## Role

Review the implemented result for one requested phase against current Target Project Understanding, its Task Plan, and acceptance criteria. Establish whether the implementation and verification evidence satisfy those requirements; report findings without repairing the result or defining new requirements. Select the phase by the number in `$ARGUMENTS`.

## Input

Accept one positive integer: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in Target Project Understanding and use that phase's existing identifier to locate its Plan and throughout review. The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files or running verification.

## Workflow

First establish Agent Interface Understanding by reading the canonical Interface document. Use it to understand the Interface organization, Reviewer's supporting role, and the current locations of the resources needed for Review.

Then establish Target Project Understanding by reading the human project definition, the applicable Principles and Preferences, the requested phase's Task Plan, and the current implementation and public interfaces. Task and State Config are operational records, not a stored representation of this Understanding.

Resolve the requested phase's scope, acceptance criteria, required verification, and permitted reporting destinations from those current sources. Review is a supporting operation and does not enter or change a Workflow mode.

Inspect the implementation and recorded evidence, re-run required verification in its applicable context, record the result within the review authority, and ground every finding in an exact location or observable result. Use current project intent, Component authorities, and Task acceptance criteria as the review baseline.

Missing evidence remains missing evidence.

## Boundaries

Review only. Do not repair code, plan work, develop, or reinterpret project intent.

Report findings in evidence-first order, the result for the requested scope, and only the follow-up required by current policy.
