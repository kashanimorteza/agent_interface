---
name: my-interface-develop
description: Agent Interface Core Skill `develop`. Executes the authorized, eligible planned Tasks of selected (or every active and developable) Target phases, records Task evidence and status in the Plan Config, records the `development` Workflow position, and logs its execution in State. Use when the Human or an Agent asks to develop one or more planned phases.
argument-hint: "[phase-id ...]"
---

# Develop — Core Skill `develop`

Synchronized Claude Code realization of the Agent Interface Core Skill with stable key `develop` (required). It was produced by Agent Native Sync and is self-contained: it is not an authority, and it never needs the Agent Module. The Operation's authoritative meaning lives in the Implementation sources named under **Authorities** and is read at run time.

## Personality

No Personality is declared. Use the project's standing conduct Rules.

## Invocation and inputs

- Invoked directly by the Human (`/my-interface-develop [phase-id ...]`) or by an Agent (for example `my-interface-implement` through the Skill tool).
- Inputs: the invocation request and an optional phase selection. Selected phases: `$ARGUMENTS` (empty means every active and developable Target phase, in Target order).
- Output: the Skill execution result and status.

## Standing rules

Apply the project Rules in `.claude/rules/` (interface-bootstrap, interface-skill-policy, git-discipline, interface-agent-capabilities).

## Requirements

- A successful Configure execution must already have established the required Config records.
- Each selected phase must have a current Plan.

If either is absent, stop and record the unmet prerequisite in State; never run Configure or Plan.

## Authorities (read at run time, before acting)

1. Interface Understanding: `.interface/interface.md` and the Foundation section files it links.
2. Target Understanding: both Target definitions the Interface locates, under the precedence it declares.
3. `.interface/implementation/operations/develop/develop.md` and `develop.yaml` — Develop Definition, Principle, and Preferences.
4. The Plan Definition's rules on Task progress (`.interface/implementation/operations/plan/plan.md`), and the Development Component Definitions and Preferences the Interface locates for the product being built.
5. Current `.interface/config/plan.yaml` (the work) and `.interface/config/state.yaml` (execution record, never authority).

If these sources disagree with this summary, the sources win.

## Procedure (summary of the Develop Definition)

1. Verify prerequisites; create this execution's Log Entry; record the active Workflow position as `development`.
2. Establish current Interface and Target Understanding; read the current Plan of each applicable phase.
3. Select only eligible Tasks whose authority, scope, inputs, outputs, dependencies, and completion conditions are understood. Readiness comes from `depends_on`, never from file order.
4. When a new Task names an earlier developed Task in `replaces`, mark the earlier Task `replaced` and record the relationship in its Task Log first.
5. Claim each Task (`claimed`) before changing its result. Consider its Task Skills and use any other suitable available Skill.
6. Perform the work, preserving valid existing work. Build and run the concrete check that satisfies the Task's verification condition; record the check and its observed outcome in the append-only Task Log (no secret values). Mark `done` only when the check passes.
7. For a verified Blocker resolution: record evidence and transition, clear the obsolete reference, return the Task to `todo`, recheck dependencies. A missing Blocker record alone is not evidence of resolution.
8. If no eligible Task exists, record that no development was required.
9. Update the Log Entry with the overall outcome, unresolved conditions, and Skills used.

## Stop conditions

Stop when a dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion. Record the reason.

## Execution log

At the start of every execution, create one Log Entry in State for that execution, including its `id`, `skill` (`my-interface-develop`), and `started_at`. At completion, update that same Log Entry with `completed_at`, `duration_ms`, `outcome`, `report`, `skills_used`, and any applicable `data`, `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason. When invoked by Implement, record the supplied Implement Log identifier as `parent_id`.

## Boundaries

- Writes the implementation (project Source) and Task status/history under Plan rules, and Development progress, the `development` position, and its Log Entry under State rules.
- Never changes Target meaning, Plan content or authority, Development Principles, or another Component's owned record; never designs or changes Tasks; never runs another Core Operation — it stops and reports when one is required.
