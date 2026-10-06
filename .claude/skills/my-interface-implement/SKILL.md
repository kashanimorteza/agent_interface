---
name: my-interface-implement
description: Core Skill for implementing — the single coordinator of the Operations workflow. Checks Config once (running Configure only if needed), then runs Plan, Develop, and Review in order for each selected Target phase and reports aggregate Open Question and Blocker counts. Use when asked to implement phases end to end, or when invoked as /my-interface-implement [phase ...].
argument-hint: "[phase-id ...]"
---
<!-- managed by /my-interface-native-implement: realized from the Executor Module Skill Contract `implement`; regenerated on every run — do not edit by hand -->

# Implement

The Core Skill for implementing. Required. Stable key: `implement`. Skill name: `my-interface-implement`.

## Inputs

An invocation request and an optional phase selection: `$ARGUMENTS` (zero or more Target phase identifiers).

## Invocation

May be invoked directly by a Human (`/my-interface-implement`) or by an Agent. Implement is the only Core Skill that invokes Core Skills, and it invokes only Configure, Plan, Develop, and Review — through the Skill tool as `my-interface-configure`, `my-interface-plan`, `my-interface-develop`, and `my-interface-review`. It never invokes Launch or Reset. It may use any Provider Skill or other available Skill.

## Authority — read at runtime

Read completely at the start of every run and follow them; this workflow is the Native realization of that understanding and never overrides them.

- `.interface/implementation/operations/implement/implement.md` — Implement's mandatory coordination Principle.
- `.interface/implementation/operations/implement/implement.yaml` — Implement Preferences.

The Principle in the Definition is mandatory. Implement Preferences supply only coordination defaults and never replace an owning Component's authority.

Apply the project Rules (`.claude/rules/`). Implement does not establish Target or Interface Understanding; each coordinated Operation establishes the Understanding its own responsibility requires. Implement only locates the Target phase identifiers and their Target order, through the Interface, when no phase is selected.

## Workflow

1. If the State Config record exists and is structurally valid, create this execution's State Log Entry first, so its `id` can be supplied as `parent_id` to every coordinated Core Skill, including Configure.
2. Check the required Config records once. If they are absent or invalid, invoke `my-interface-configure` (with this Entry's `id` as `parent_id` when the Entry exists). If State was not available before Configure, create this execution's Log Entry as soon as it is, and record the Configure execution's Log Entry `id` in its `data`. If Config is still absent or invalid afterwards, record the stopped outcome (or report explicitly that the Entry could not be written) and stop before Plan, Develop, or Review.
3. Resolve phases: the given identifiers, or every Target phase in Target order when none is given.
4. For each phase, in order: invoke `my-interface-plan`, then `my-interface-develop`, then `my-interface-review`, each scoped to that phase and given this Entry's `id` as `parent_id`. A blocked Develop does not by itself skip Review: when Source is available, Review runs its own passes until satisfied or blocked. Unresolved Blockers or Open Questions may make the final outcome blocked, but never prevent an applicable Review.
5. Carry each Operation's outcome into the aggregate result; determine the unique counts of associated Open Questions and Blockers.
6. Complete the Log Entry and report.

## Boundaries

Implement owns coordination only. It never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component, and never takes ownership of another Operation's records or results.

## Execution Log

Every execution creates one Log Entry in State with its `id` and Skill, and updates that same Entry with outcome, report, and any applicable `data`, Open Questions, or Blockers when work completes, stops, or is blocked. Follow the State Component (`.interface/implementation/operations/state/state.md`) and State Schema. When coordinating another Core Skill, supply this Entry's `id` as that Skill's `parent_id`; this Entry's data includes the unique counts of associated Open Questions and Blockers.

## Outputs

The Skill execution result and status, including the aggregate counts of associated Open Questions and Blockers.
