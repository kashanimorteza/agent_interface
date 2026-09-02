---
name: my-interface-tasker
description: Create or update the authorized implementation plan for the project scope named by the Developer, using the current generated Understanding and task standard. Plans only; never implements or interprets the human project definition.
argument-hint: "[item] [phase-id ...]"
disable-model-invocation: true
---

# Plan from the generated configuration

Turn the current generated Understanding into an authorized implementation-ready plan.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine planning behavior but cannot expand this Skill's live authority, planning scope, or write boundaries.

## Refresh context before planning

1. Follow the live map to read the current State contract, generated Understanding, task standard and Schema, rules, target configuration, and every other mapped file required for this invocation.
2. Resolve the requested item and project phases in `$ARGUMENTS` only from the current generated Understanding. Require every requested phase to target that item; do not infer scope from active state, prior plans, or memory.

## Plan

Enter planning mode only as the current authorities permit. Plan exactly the requested authorized phases for the named item, in the order and structure defined by the current Understanding and task standard.

Derive every project fact, grouping, task field, status, lifecycle, transition, dependency, contract, path, verification rule, and write permission from the current file that owns it. Do not copy these parameters into this Skill or substitute remembered values.

Where an implementation-ready plan requires planning-owned item configuration or a draft contract to be refined, reconcile only the parts authorized by the live files and only for the requested scope. Do not change a frozen, protected, or human-owned value, and do not turn a planning decision into a new project requirement.

Treat an update as reconciliation, not replacement. Preserve existing progress, history, confirmed content, and every value outside this Skill's current write authority. Change only the planning-owned content required by the requested scope, and use the live gap mechanism when the requested change conflicts with protected or already-executed work.

If the requested scope or required information is missing, ambiguous, inconsistent, or unauthorized, use the live gap mechanism and stop. Do not select, reshape, or invent project scope or requirements.

Generate only the plan content authorized by the current files and validate it against the current task standard and Schema.

## Boundaries and completion

Do not implement, execute, test, review, reinterpret the project definition, or modify inputs merely to make planning possible. Record the outcome through the current State mechanism and report the handled scope, written plan content, and any blocker, open question, missing authority, or missing configuration.
