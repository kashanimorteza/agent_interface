---
name: my-interface-tasker
description: Create or reconcile the planning output for one requested project phase from current generated Project Understanding. Plans only; never implements.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Plan one project phase

## Role

Plan one requested project phase from the shared generated Project Understanding. Produce the planning output required by the current Interface for downstream Development without implementing the work. Select the phase by the number in `$ARGUMENTS`.

## Input

Accept one positive integer: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in the current generated Project Understanding and use that phase's existing identifier throughout planning. The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files.

## Workflow

After establishing both shared Understandings, use the shared bootstrap to locate and read the generated configuration needed to resolve the requested phase and the current authorities governing Planning. Treat generated project decisions as the authoritative resolved inputs for the Plan.

Derive the required planning format, content, granularity, progress handling, validation, ownership, and write boundaries from those live authorities. Do not assume or reproduce a fixed planning structure in this Skill.

Build a complete candidate for the requested phase that preserves its resolved identity, intent, scope, and decisions and is usable by downstream Development. Apply the current planning authorities to every part of the candidate; do not embed remembered fields, defaults, or policies when the live sources define them.

Validate the complete candidate using the current authorities before writing it only to the authorized destination.

On every run, rebuild the candidate from current sources and reconcile it with existing planning output according to the current ownership and reconciliation rules. Preserve information outside Tasker's authority and surface conflicts as required by the live policies.

The operation is idempotent with respect to unchanged sources and Tasker-owned planning information.

## Boundaries

Plan only for the requested phase. Do not implement product work, perform Review or Interpretation, alter project intent, or write outside Planning's current authority.

Report the result according to the current reporting rules.
