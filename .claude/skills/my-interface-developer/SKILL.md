---
name: my-interface-developer
description: Execute and verify eligible planned work for one requested project phase using the current project definition, applicable Component authorities, and Task Plan. Never plans or reviews.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Develop one project phase

## Role

Implement and verify eligible planned work for one requested project phase. Use current Target Project Understanding and the Task Plan as the specification. Do not plan new work. Select the phase by the number in `$ARGUMENTS`.

## Input

Accept one positive integer: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in Target Project Understanding and use that phase's existing identifier to locate its current planning output and throughout development. The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files.

## Workflow

First establish Agent Interface Understanding by reading the canonical Interface document. Use it to understand the Interface organization, Developer's place in the Workflow, and the current locations of the resources needed by Development.

Then establish Target Project Understanding by reading the human project definition, the Principles and Preferences applicable to the requested phase and its target Component, and the existing implementation and public interfaces. Task and State Config are operational records, not a stored representation of this Understanding.

Read the requested phase's current Task Plan and State. Derive work selection, ordering, eligibility, progress updates, evidence handling, validation, ownership, and write boundaries from the current Component authorities. Do not assume or reproduce their current fields, statuses, or policies in this Skill.

Install and configure the runtimes, package managers, build tools, system software, and dependencies required for the authorized work. A missing prerequisite is work to perform; record a Blocker only when its installation or configuration actually fails and prevents continuation.

Execute eligible planned work within the resolved scope and current authority. Apply the shared decision policy to unspecified implementation details while preserving project intent and existing interfaces.

Verify each result and record execution progress and evidence exactly as required by the live authorities. When work cannot complete, preserve truthful state and follow the current failure, question, and blocking policies.

After each outcome, reconcile Development-owned information and continue according to the current execution rules.

The operation is repeatable and idempotent according to the current execution and ownership rules.

## Boundaries

Develop only eligible planned work in the requested phase. Do not perform Planning, Review, or Configure, alter project intent, bypass resolved interfaces, or write outside Development's current authority.

Report the result according to the current reporting rules.
