---
name: my-interface-planning
description: Create or reconcile Task Plans for selected Target phases, or every enabled phase when none is specified, only when explicitly requested by the Human or delegated by a declared Interface coordinator. Plans only; never implements.
argument-hint: "[phase-number ...]"
disable-model-invocation: false
---

# Plan project phases

This file is the Claude Code adapter for the portable `planning` Skill Contract. Resolve and read that Contract through Agent Skill Profile before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Plan the selected project phases from current Target Understanding, and produce the planning output the current Interface requires.

Planning decides what work exists and how it is organized. It does not decide how that work is implemented, because a plan that prescribes implementation removes the judgment the implementer needs when the code turns out differently than the plan imagined.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects the first phase, `2` selects the second phase, and so on. Resolve every number against the current phase order in Target Understanding and use each phase's stable identifier throughout planning.

The numbers are input conveniences; the Human does not need to type phase identifiers' `P` prefixes, and a number never renames a phase or changes stored identifiers or references.

If `$ARGUMENTS` is empty, select every phase whose current Target status marks it enabled. If no phase is enabled, make no changes and report that there is no phase to plan.

If arguments are present, validate the complete selection before changing any files. Every token must be a positive integer that resolves to an available phase. Deduplicate repeated numbers and process the selected phases in Target order, regardless of argument order. If any token is invalid, enumerate all available phases in Target order with their input number, stable identifier, title, status, and readiness, identify every invalid token, and ask the Human for a corrected list; do not begin planning until the entire selection is valid.

## Workflow

First establish Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Planning's place in the Workflow, and the current locations of the resources Planning needs.

Then establish Target Understanding from the Human and Technical Definitions located by the Interface under their declared precedence, and read the applicable Developer Principles and Preferences together with Agent Principles and Profiles. Inspect existing implementation and interfaces when they provide relevant current evidence. Plan and State Config are operational records, not a stored representation of this Understanding, so reading them back is not a substitute for reading the sources.

Read the current Plan and State Config files, and the Review Config for each selected phase. Derive the meaning of review Findings and how Planning handles them from the current Review and Plan Component authorities. Resolve the selected phases from current Target Understanding, then derive planning structure, content, granularity, progress handling, validation, ownership, and write boundaries from the current owning Components. Do not assume or reproduce a fixed planning structure here: the Plan Component changes independently of this Skill, and a structure remembered from an earlier run will silently disagree with it.

Before building a candidate, create a transient coverage ledger for each selected phase. Enumerate every requirement in that phase's Target definition, every applicable obligation from the owning Component authorities, and every unresolved Review Finding. Map each item to exactly one Task that owns the required outcome and proof, or to the higher-level context from which the Task inherits it. This ledger is a validation aid, not planning content: do not store it or copy authoritative meaning into the Plan. A candidate is incomplete while any item is unmapped, duplicated across Tasks, contradicted, or represented only by a narrower example.

Process selected phases in Target order. For each phase, when its planning begins, record the active planning mode and that phase's Planning progress as `in progress`. After reconciliation, record it as `completed` only when the complete phase Plan is valid; otherwise preserve the truthful incomplete value. Append each outcome to State History under the current State rules. A phase that cannot be completed does not prevent planning a later selected phase unless the current authorities establish a dependency or Blocker that does.

Build a complete candidate for each selected phase that preserves its resolved identity, intent, scope, and decisions, and that is usable by downstream Development. Apply the current planning authorities to every part of each candidate rather than embedding remembered fields, defaults, or policies.

Prefer stable decomposition over stylistic regeneration. Preserve an existing valid Group and Task boundary, identifier, dependency, and wording when its meaning and coverage remain current. When no Plan exists, derive boundaries from distinct responsibilities and real dependencies rather than document layout or arbitrary batch size.

Validate the complete candidate against the transient coverage ledger and the current authorities before writing it. Every clause of a Task's expected result and acceptance must be covered by its verification condition; one representative example does not prove a compound requirement. Write only to the authorized destination.

On every run, rebuild the candidate from current sources and reconcile it with existing planning output according to the current ownership and reconciliation rules. Preserve information outside Planning's authority and surface conflicts as the live policies require, because planning runs repeatedly over the life of a phase and work already recorded is the most expensive thing the file holds.

The operation is idempotent with respect to unchanged sources and Planning-owned planning information.

## Boundaries

Perform only Planning's role, and only for the selected phases. Do not perform another Interface Operation, alter Target intent, or write outside Planning's current authority.

## Report

Report in this order:

1. **Phases** — every resolved phase identifier, title, order, and target, in Target order.
2. **Plan results** — for each phase, created, reconciled, or already current, with the counts the Plan Component defines.
3. **What changed** — by phase, work added, work reconciled, and work left untouched because it lies outside Planning's authority.
4. **Conflicts and unresolved decisions** — by phase, anything that could not be planned safely, and any Blocker or Open Question raised, each with what it prevents.
5. **State** — each phase's aggregate progress and the History outcomes recorded for this run.
6. **Next step** — the single most useful next action supported by the result.
