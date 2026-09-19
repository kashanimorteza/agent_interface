---
name: my-interface-planning
description: Create or reconcile Task Plans for selected Target phases, or every enabled phase when none is specified, only when explicitly requested by the Human or delegated by a declared Interface coordinator. Plans only; never implements.
argument-hint: "[phase-number ...]"
metadata:
  contract: ".interface/agent/skill/contracts/planning.md"
  contract_sha256: "sha256:c3aff518e90952fcae91a1be3a32a1e13ac56ac132ba3a7bfcc42a077fb2349c"
  preferences: ".interface/agent/skill/preferences.yaml"
  preferences_sha256: "sha256:386052d88bf6225ecc6b2cc35f60fc2e7344a26bce478741efa86371fde6d566"
  synced_at: "2026-09-19T19:40:02Z"
---

# Plan project phases

This file is the self-contained Claude Code realization of the portable `planning` Skill Contract, placed here by Agent Sync as the Human authored it. Follow this file and the synchronized Runtime Rules under `.claude/rules/`; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-planning` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Purpose

Define complete, bounded, ordered, and verifiable work for Target phases.

## Responsibility

Create or reconcile Plans, Groups, and Tasks from current Target intent and applicable Component authorities. Planning owns what work must achieve and how achievement is observed; it never prescribes implementation or performs downstream operations.

## Trigger

Activate explicitly for zero or more phase selections, or when a coordinator requires a current valid Plan.

## Inputs

Accept zero or more phase positions. Empty input selects every enabled phase. Resolve positions to stable phase identifiers, deduplicate them, and process them in Target order. Consume Target Understanding, applicable Component authorities, current Plan and State, Review Findings, and relevant implementation evidence.

Claude Code input handling: the positions arrive as whitespace-separated positive integers in `$ARGUMENTS` — `1` selects the first phase, `2` the second, and so on. Resolve every number against the current phase order in Target Understanding and use each phase's stable identifier throughout planning; the numbers are input conveniences and never rename a phase or change stored identifiers or references. If `$ARGUMENTS` is empty and no phase is enabled, make no changes and report that there is no phase to plan. If any token is not a positive integer resolving to an available phase, enumerate all available phases in Target order with their input number, stable identifier, title, status, and readiness, identify every invalid token, and ask the Human for a corrected list; do not begin planning until the entire selection is valid.

## Outputs

Produce or reconcile only Planning-owned Plan content and Plan Revision, Planning aggregate State and History outcomes, conflicts, Blockers or Open Questions permitted by their owners, the applicable Agent parameters carried into each governed Task and the resolution of every selected item's `agent_skills` associations, and a phase-by-phase report.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Read current Plan, State, and Review authorities and Schemas plus every Implementation Component applicable to the selected phases.

Claude Code routes: establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, then Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Follow its routes to the Plan, State, and Review authorities, their Schemas and Config files, and the Implementation Components applicable to the selected phases. Plan and State Config are operational records, not a stored representation of this Understanding, so reading them back is not a substitute for reading the authorized sources. Derive planning structure, content, granularity, progress handling, validation, ownership, and write boundaries from the current authorities on every run rather than from a structure remembered from an earlier run.

## Authority

Write only Planning-owned Plan fields and Planning-owned aggregate State and History. Preserve implementation, Review ownership, Target intent, and every field outside Planning authority.

## Workflow Invariants

- Validate the complete input before mutation.
- Any invalid token prevents the whole planning run and produces the available phase list.
- Build a transient coverage ledger mapping every selected phase requirement, applicable Principle obligation, and unresolved Review Finding to exactly one owning Task or inherited phase context.
- A Plan is incomplete while coverage is missing, duplicated, contradictory, or represented only by a narrower example.
- Preserve valid identities, boundaries, dependencies, wording, progress, and history; prefer stable decomposition over stylistic regeneration.
- Set a new Plan's revision to `1`.
- Increment an existing Plan's revision exactly once when any Planning-owned semantic content changes during the run; preserve it when only Development-owned progress or logs changed or when reconciliation is semantically idempotent.
- Derive new Task boundaries from responsibilities and real dependencies, never document layout or arbitrary batch size.
- Keep planning content implementation-independent and require verification conditions to cover every acceptance clause.
- Read the Cross-cutting Capability applicability lists the Implementation authorities declare before stating any verification condition, and treat the testing list as the authority over which Components carry a testing concern.
- A Task whose target Component is listed may state a verification condition whose proof persists as a test belonging to that Component.
- A Task whose target Component is not listed states a verification condition satisfiable by a transient check, and never one that can only be satisfied by a persisted test.
- Availability of a test tool in the declared toolchain is not applicability; an unlisted Component stays unlisted.
- Process phases independently in Target order unless an owned dependency or Blocker prevents continuation.
- For every item a selected phase resolves, gather every Agent parameter on the path to that item — the parameter on the item itself and on each item above it — and carry them into the governed Task together, the nearest one governing any point two of them speak to.
- Shape the governed Task's acceptance and verification so that what an applicable `agent_consider` asks for and what an applicable `agent_avoid` rules out are observable conditions of the Task, not background advice.
- Report rather than silently resolve a conflict between an Agent parameter and an explicit Target statement or an applicable Principle; the Target or the Principle governs and the parameter is recorded as overridden.
- Resolve the `agent_skills` associations of every selected item against currently discoverable and usable Runtime Skills.
- Match the declared name against the Skill's own name within a Runtime's namespaced identifier rather than requiring an exact string match.
- When an associated Skill is required and currently discoverable and usable, shape the governed Task's acceptance and verification to require observable conformance with that Skill's applicable guidance, not only completion of the underlying requirement.
- Record the unavailability and continue when an associated Skill is not currently usable; an unavailable associated Skill never blocks planning.

Claude Code execution detail: the coverage ledger is a validation aid, not planning content — do not store it or copy authoritative meaning into the Plan. When a phase's planning begins, record the active planning mode and that phase's Planning progress as `in progress`; after reconciliation record it as `completed` only when the complete phase Plan is valid, otherwise preserve the truthful incomplete value, and append each outcome to State History under the current State rules.

## Verification

- Validate the complete candidate against the transient coverage ledger, current Plan authorities, and applicable Schemas before writing.
- Prove that every selected item's applicable Agent parameters were gathered and carried into the governed Task, that each `agent_skills` association was resolved and recorded either as a shaped acceptance condition or as a reported unavailability, and that every conflict between a parameter and a higher authority was reported.
- Planning is complete only when the selected phase Plan is complete and valid.

## Idempotency

Rebuild from current authorities and reconcile rather than regenerate. Unchanged sources and valid Planning-owned content produce no semantic mutation.

## Stopping Conditions

- Stop before mutation on any invalid input.
- Leave an affected phase incomplete when required intent cannot be resolved safely, coverage cannot be completed, a conflict crosses ownership, or a genuine Blocker applies; continue independent selected phases.

## Runtime Realization

A native adapter exposes optional multi-phase input using the Command mapping, locates all live structures through the Interface, and reports phases, Plan results, changes, conflicts, State, and the supported next step.

In Claude Code this adapter reports, in this order:

1. **Phases** — every resolved phase identifier, title, order, and target, in Target order.
2. **Plan results** — for each phase, created, reconciled, or already current, with its resulting Plan Revision and the counts the Plan Component defines.
3. **What changed** — by phase, work added, work reconciled, and work left untouched because it lies outside Planning's authority.
4. **Agent parameters and associated Skills** — by phase, the Agent parameters carried into each governed Task and any recorded as overridden, and each `agent_skills` association a selected item declared, whether it resolved to a usable Runtime Skill, and where its conformance was written into acceptance.
5. **Conflicts and unresolved decisions** — by phase, anything that could not be planned safely, and any Blocker or Open Question raised, each with what it prevents.
6. **State** — each phase's aggregate progress and the History outcomes recorded for this run.
7. **Next step** — the single most useful next action supported by the result.
