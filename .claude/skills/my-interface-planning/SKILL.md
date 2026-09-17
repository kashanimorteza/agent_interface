---
name: my-interface-planning
description: Create or reconcile Task Plans for selected Target phases, or every enabled phase when none is specified, only when explicitly requested by the Human or delegated by a declared Interface coordinator. Plans only; never implements.
argument-hint: "[phase-number ...]"
metadata:
  contract: ".interface/agent/skill/contracts/planning.md"
  contract_sha256: "sha256:7a25f56def74f950ba75b2f805e0990b02175db59c3fdf0b87db16acea909623"
  synced_at: "2026-09-17T18:39:10Z"
---

# Plan project phases

This file is the self-contained Claude Code realization of the portable `planning` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-planning` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

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

Then establish Target Understanding from the Human and Technical Definitions located by the Interface under their declared precedence, and read the applicable Implementation Principles and Preferences under synchronized Runtime rules. Never enter or inspect the Agent Module. Inspect existing implementation and interfaces when they provide relevant current evidence. Plan and State Config are operational records, not a stored representation of this Understanding, so reading them back is not a substitute for reading the authorized sources.

Read the current Plan, State, and Review authorities and their Schemas, including the Plan and State Config files and the Review Config for each selected phase. Derive the meaning of review Findings and how Planning handles them from the current Review and Plan Implementation Component authorities. Resolve the selected phases from current Target Understanding, then derive planning structure, content, granularity, progress handling, validation, ownership, and write boundaries from the current applicable Implementation Components. Do not assume or reproduce a fixed planning structure here: the Plan Component changes independently of this Skill, and a structure remembered from an earlier run will silently disagree with it.

For every technical option a selected phase resolves, resolve its declared `agent_skills` associations against currently discoverable and usable Runtime Skills. Match the declared name against the Skill's own name within a Runtime's namespaced identifier rather than requiring an exact string match. When an associated Skill is required and currently discoverable and usable, shape the governed Task's acceptance and verification to require observable conformance with that Skill's applicable guidance, not only completion of the underlying requirement. Record the unavailability and continue when an associated Skill is not currently usable; an unavailable associated Skill — required or optional — never blocks planning.

Before building a candidate, create a transient coverage ledger for each selected phase. Enumerate every requirement in that phase's Target definition, every applicable obligation from the owning Implementation Component authorities and synchronized Runtime rules, and every unresolved Review Finding. Map each item to exactly one Task that owns the required outcome and proof, or to the higher-level context from which the Task inherits it. This ledger is a validation aid, not planning content: do not store it or copy authoritative meaning into the Plan. A candidate is incomplete while any item is unmapped, duplicated across Tasks, contradicted, or represented only by a narrower example.

Process selected phases in Target order. For each phase, when its planning begins, record the active planning mode and that phase's Planning progress as `in progress`. After reconciliation, record it as `completed` only when the complete phase Plan is valid; otherwise preserve the truthful incomplete value. Append each outcome to State History under the current State rules. A phase that cannot be completed does not prevent planning a later selected phase unless the current authorities establish a dependency or Blocker that does.

Build a complete candidate for each selected phase that preserves its resolved identity, intent, scope, and decisions, and that is usable by downstream Development. Apply the current planning authorities to every part of each candidate rather than embedding remembered fields, defaults, or policies.

Set a newly created phase Plan's `revision` to `1`. When reconciliation changes any Planning-owned semantic content—including Plan, Group, or Task definition, boundary, dependency, acceptance, or verification meaning—increment the existing revision exactly once for that run. Preserve the revision when Planning-owned meaning is unchanged; Task status, blocker references, and execution logs belong to Development progress and never increment it.

Prefer stable decomposition over stylistic regeneration. Preserve an existing valid Group and Task boundary, identifier, dependency, and wording when its meaning and coverage remain current. When no Plan exists, derive boundaries from distinct responsibilities and real dependencies rather than document layout or arbitrary batch size.

Before stating any verification condition for a Task, read the Cross-cutting Capability applicability lists the current Implementation authorities declare, and treat the testing list as the authority over which Components carry a testing concern. A Task whose target Component appears on that testing list may state a verification condition whose proof persists as a test belonging to that Component. A Task whose target Component is not listed states a verification condition satisfiable only by a transient check, never one that can only be satisfied by a persisted test. Availability of a test tool in the declared toolchain is not applicability; an unlisted Component stays unlisted.

Validate the complete candidate against the transient coverage ledger, the current authorities, and applicable Schemas before writing it. Every clause of a Task's expected result and acceptance must be covered by its verification condition; one representative example does not prove a compound requirement. Write only to the authorized destination. Prove that every selected technical option's declared `agent_skills` associations were resolved and recorded, either as a shaped acceptance condition or as a reported unavailability.

On every run, rebuild the candidate from current sources and reconcile it with existing planning output according to the current ownership and reconciliation rules. Preserve information outside Planning's authority and surface conflicts as the live policies require, because planning runs repeatedly over the life of a phase and work already recorded is the most expensive thing the file holds.

The operation is idempotent with respect to unchanged sources and Planning-owned planning information.

## Boundaries

Perform only Planning's role, and only for the selected phases. Do not perform another Interface Operation, alter Target intent, or write outside Planning's current authority.

## Report

Report in this order:

1. **Phases** — every resolved phase identifier, title, order, and target, in Target order.
2. **Plan results** — for each phase, created, reconciled, or already current, with its resulting Plan Revision and the counts the Plan Component defines.
3. **What changed** — by phase, work added, work reconciled, and work left untouched because it lies outside Planning's authority.
4. **Associated Skills** — by phase, each `agent_skills` association a selected option declared, whether it resolved to a usable Runtime Skill, and where its conformance was written into acceptance.
5. **Conflicts and unresolved decisions** — by phase, anything that could not be planned safely, and any Blocker or Open Question raised, each with what it prevents.
6. **State** — each phase's aggregate progress and the History outcomes recorded for this run.
7. **Next step** — the single most useful next action supported by the result.
