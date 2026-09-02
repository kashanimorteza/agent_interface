---
name: my-interface-tasker
description: Create or update the authorized implementation plan for the project scope named by the Developer, using the current generated Understanding and task standard. Plans only; never implements or interprets the human project definition.
argument-hint: "[phase-id ...]"
disable-model-invocation: true
---

# Plan from the generated configuration

Turn the current generated Understanding into an authorized implementation-ready plan.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine planning behavior but cannot expand this Skill's live authority, planning scope, or write boundaries.

## Refresh context before planning

1. Follow the live map to read the current State contract, generated Understanding, task standard and Schema, rules, target configuration, and every other mapped file required for this invocation.
2. Resolve `$ARGUMENTS` only from the current generated Understanding.

## Plan

Enter planning mode only as the current authorities permit. Plan exactly the requested authorized scope, in the order and structure defined by the current Understanding and task standard.

Derive every project fact, grouping, task field, status, lifecycle, transition, dependency, contract, path, verification rule, and write permission from the current file that owns it. Do not copy these parameters into this Skill or substitute remembered values.

If the requested scope or required information is missing, ambiguous, inconsistent, or unauthorized, use the live gap mechanism and stop. Do not select, reshape, or invent project scope or requirements.

Generate only the plan content authorized by the current files and validate it against the current task standard and Schema.

## Boundaries and completion

Do not implement, execute, test, review, reinterpret the project definition, or modify inputs merely to make planning possible. Record the outcome through the current State mechanism and report the handled scope, written plan content, and any blocker, open question, missing authority, or missing configuration.
