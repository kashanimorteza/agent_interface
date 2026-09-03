---
name: my-interface-tasker
description: Create or update the authorized implementation plan for the one project phase named by the Developer, resolving its target item from the generated Understanding. Plans only; never implements or interprets the human project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Plan from the generated configuration

Turn the current generated Understanding into an authorized implementation-ready plan.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine planning behavior but cannot expand this Skill's live authority, planning scope, or write boundaries.

## Refresh context before planning

1. Resolve the one requested phase id in `$ARGUMENTS` from the current generated Understanding. Refuse an omitted, additional, or unknown phase rather than choosing one.
2. Resolve that phase's target item from the phase itself, then follow the live map to read the current State contract, task standard and Schema, target-item Policy, mapped item configuration and contracts, and every other file required for this invocation.
3. From the resolved target-item configuration, collect every non-empty `skill` named by a selected technology entry. Resolve and read each available named Skill before planning. If a configured Skill is unavailable, record a gap instead of silently ignoring it, guessing a replacement, or planning without its required guidance. A technology with no configured Skill needs no Skill lookup.

## Plan

Enter planning mode only as the current authorities permit. Plan exactly the requested authorized phase under `content.plans.<phase-id>`, using its target item only as technical context and a write boundary.

Apply configured technology Skills as technical planning guidance wherever relevant to task decomposition, acceptance criteria, and verification. They never create project requirements or expand the authorized phase.

Derive every project fact, grouping, task field, status, lifecycle, transition, dependency, contract, path, verification rule, and write permission from the current file that owns it. Do not copy these parameters into this Skill or substitute remembered values.

Where an implementation-ready plan requires planning-owned configuration for the phase's target item or a draft contract to be refined, reconcile only the parts authorized by the live files and only for the requested phase. Do not change a frozen, protected, or human-owned value, and do not turn a planning decision into a new project requirement.

Treat an update as reconciliation, not replacement. Preserve existing progress, history, confirmed content, and every value outside this Skill's current write authority. Change only the planning-owned content required by the requested scope, and use the live gap mechanism when the requested change conflicts with protected or already-executed work.

If the requested scope or required information is missing, ambiguous, inconsistent, or unauthorized, use the live gap mechanism and stop. Do not select, reshape, or invent project scope or requirements.

Generate only the plan content authorized by the current files and validate it against the current task standard and Schema.

## Boundaries and completion

Do not implement, execute, test, review, reinterpret the project definition, or modify inputs merely to make planning possible. Record the outcome through the current State mechanism and report the handled scope, written plan content, and any blocker, open question, missing authority, or missing configuration.
