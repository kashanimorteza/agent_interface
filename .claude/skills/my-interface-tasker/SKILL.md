---
name: my-interface-tasker
description: Create or reconcile the Task Plan for one requested project phase from the current project definition and applicable Component authorities. Plans only; never implements.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Plan one project phase

## Role

Plan one requested project phase from current Target Project Understanding. Produce the planning output required by the current Interface for downstream Development without implementing the work. Select the phase by the number in `$ARGUMENTS`.

## Input

Accept one positive integer: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in Target Project Understanding and use that phase's existing identifier throughout planning. The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files.

## Workflow

First establish Agent Interface Understanding by reading the canonical Interface document. Use it to understand the Interface organization, Tasker's place in the Workflow, and the current locations of the resources needed by Planning.

Then establish Target Project Understanding by reading the human project definition and the Principles and Preferences applicable to the requested phase and its target Component. Inspect existing implementation and interfaces when they provide relevant current evidence. Task and State Config are operational records, not a stored representation of this Understanding.

Read the current Task and State Config files. Resolve the requested phase from the human project definition and derive planning structure, content, granularity, progress handling, validation, ownership, and write boundaries from the Task Component. Do not assume or reproduce a fixed planning structure in this Skill.

Build a complete candidate for the requested phase that preserves its resolved identity, intent, scope, and decisions and is usable by downstream Development. Apply the current planning authorities to every part of the candidate; do not embed remembered fields, defaults, or policies when the live sources define them.

Validate the complete candidate using the current authorities before writing it only to the authorized destination.

On every run, rebuild the candidate from current sources and reconcile it with existing planning output according to the current ownership and reconciliation rules. Preserve information outside Tasker's authority and surface conflicts as required by the live policies.

The operation is idempotent with respect to unchanged sources and Tasker-owned planning information.

## Boundaries

Plan only for the requested phase. Do not implement product work, perform Review or Configure, alter project intent, or write outside Planning's current authority.

Report the result according to the current reporting rules.
