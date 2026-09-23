---
name: my-interface-implement
description: Core Interface Skill for implementing. Coordinates Configure (only when Config is absent or invalid), then Plan, Develop, and Review for each selected (or every) Target phase in Target order, linking every coordinated Log Entry to its Implement Log Entry through parent_id. Use when the Human asks to implement a phase end to end.
argument-hint: "[phase-id ...]"
---

<!--
Native realization (Claude Code) of the Core Skill Contract `implement`, synchronized by
/my-interface-agent-native. The Human-owned Agent Module remains authoritative; this Skill is
not a second authority. Its operational meaning is owned by the Implement Operation Component,
which this Skill reads from its current location at run time.
-->

# Implement (`my-interface-implement`)

Stable key: `implement`. Required. Invocable directly by the Human (`/my-interface-implement [phase-id ...]`) or by an Agent.

- **Input:** an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).
- **Output:** the Skill execution result and status.

## Before acting

1. Apply the synchronized project Rules (`.claude/rules/`), especially *Agent Interface Skill policy* and *Agent Interface bootstrap*.
2. Through `.interface/interface.md`, locate and read the Implement Operation Component Definition (currently `.interface/implementation/operations/implement/implement.md`) and Preferences (`implement.yaml`), and the State Config Schema for the Log Entry shape. They own this Skill's meaning; when they differ from the summary below, they win.
3. Implement does **not** establish Target or Interface Understanding for the work itself; each coordinated Operation establishes the Understanding its own responsibility requires.

## Coordination sequence

1. Accept the selected phase identifiers, or coordinate every Target phase in Target order when none is selected.
2. **Reserve** the Implement Log identifier.
3. Check the required Config records **once**. Coordinate Configure (`my-interface-configure`) only when they are absent or invalid.
4. Once Config is available, record the Workflow position `implementing` and write the Implement Log Entry with the reserved identifier.
5. For each phase, in order, coordinate: Plan (`my-interface-plan <phase>`) → Develop (`my-interface-develop <phase>`) → Review (`my-interface-review <phase>`). Invoke each synchronized Skill with the Skill tool. Review runs its own passes until satisfied or blocked.
6. Every coordinated Operation Log Entry records the reserved Implement Log identifier as its `parent_id` — pass it to each coordinated Skill.
7. Carry each Operation Outcome forward; stop when a required condition, Blocker, or unresolved decision prevents safe continuation.
8. Record common execution fields and coordination outcomes (including stopping information) in the Implement Log Entry's `data`.

## Boundaries

- Coordination only: each participating Operation keeps its own scope, authority, Understanding, records, outcomes, and stopping conditions.
- Apart from appending its own Implement Log Entry and Workflow position, **never** changes a Plan, Development result, Review Finding, or State record outside its owning Component's authority.
- Every other `.interface/` path is read-only.

## Report

Per phase: each coordinated Operation's outcome, the Implement Log identifier, where the cycle stopped and why, and required Human actions.
