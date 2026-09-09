---
name: my-interface-tasker
description: Create or reconcile the Task Plan for one requested project phase from the current project definition and the applicable Component authorities. Plans only; never implements.
argument-hint: "[phase-number]"
disable-model-invocation: true
---

# Plan one project phase

## Role

Plan one requested project phase from current Target Understanding, and produce the planning output the current Interface requires.

Tasker decides what work exists and how it is organized. It does not decide how that work is implemented, because a plan that prescribes implementation removes the judgment the implementer needs when the code turns out differently than the plan imagined.

## Input

Accept one positive integer from `$ARGUMENTS`: `1` selects phase one, `2` selects phase two, and so on. Resolve the number against the phase order in Target Understanding and use that phase's existing identifier throughout planning.

The number is an input convenience; it never renames a phase or changes stored identifiers or references. If the number is missing, invalid, or does not uniquely select an existing phase, request a valid phase number before changing any files.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Tasker's place in the Workflow, and the current locations of the resources Planning needs.

Then establish Target Understanding by reading the human project definition and the Principles and Preferences applicable to the requested phase and its target Component. Inspect existing implementation and interfaces when they provide relevant current evidence. Plan and State Config are operational records, not a stored representation of this Understanding, so reading them back is not a substitute for reading the sources.

Read the current Plan and State Config files, and the Review Config for the requested phase. Derive the meaning of review Findings and how Planning handles them from the current Review and Plan Component authorities. Resolve the requested phase from the human project definition, then derive planning structure, content, granularity, progress handling, validation, ownership, and write boundaries from the current owning Components. Do not assume or reproduce a fixed planning structure here: the Plan Component changes independently of this Skill, and a structure remembered from an earlier run will silently disagree with it.

Build a complete candidate for the requested phase that preserves its resolved identity, intent, scope, and decisions, and that is usable by downstream Development. Apply the current planning authorities to every part of the candidate rather than embedding remembered fields, defaults, or policies.

Validate the complete candidate using the current authorities before writing it, and write only to the authorized destination.

On every run, rebuild the candidate from current sources and reconcile it with existing planning output according to the current ownership and reconciliation rules. Preserve information outside Tasker's authority and surface conflicts as the live policies require, because planning runs repeatedly over the life of a phase and work already recorded is the most expensive thing the file holds.

The operation is idempotent with respect to unchanged sources and Tasker-owned planning information.

## Boundaries

Plan only, and only for the requested phase. Do not implement product work, perform Review or Configure, alter project intent, or write outside Planning's current authority.

## Report

Report in this order:

1. **Phase** — the resolved phase identifier, title, order, and target.
2. **Plan result** — created, reconciled, or already current, with the counts the Plan Component defines.
3. **What changed** — work added, work reconciled, and work left untouched because it lies outside Tasker's authority.
4. **Conflicts and unresolved decisions** — anything that could not be planned safely, and any Blocker or Open Question raised, each with what it prevents.
5. **Next step** — the single most useful next action supported by the result.
