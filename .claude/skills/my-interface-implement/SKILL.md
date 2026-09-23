---
name: my-interface-implement
description: Agent Interface Core Skill `implement`. Coordinates the Operations workflow for selected (or every) Target phase — Configure only when Config is absent or invalid, then Plan, Develop, and Review per phase in order — linking every coordinated Log Entry to its own Implement Log Entry. Use when the Human or an Agent asks to implement one or more phases end to end.
argument-hint: "[phase-id ...]"
---

# Implement — Core Skill `implement`

Synchronized Claude Code realization of the Agent Interface Core Skill with stable key `implement` (required). It was produced by Agent Native Sync and is self-contained: it is not an authority, and it never needs the Agent Module. The Operation's authoritative meaning lives in the Implementation sources named under **Authorities** and is read at run time.

## Personality

No Personality is declared. Use the project's standing conduct Rules.

## Invocation and inputs

- Invoked directly by the Human (`/my-interface-implement [phase-id ...]`) or by an Agent.
- Inputs: the invocation request and an optional phase selection. Selected phases: `$ARGUMENTS` (empty means every Target phase, in Target order).
- Output: the Skill execution result and status.

## Standing rules

Apply the project Rules in `.claude/rules/` (interface-bootstrap, interface-skill-policy, git-discipline, interface-agent-capabilities).

## Authorities (read at run time, before acting)

1. `.interface/interface.md` — to locate resources (Implement does not establish Target or Interface Understanding for the work; each coordinated Operation establishes its own).
2. `.interface/implementation/operations/implement/implement.md` and `implement.yaml` — Implement Definition, Principle, and Preferences.
3. The Config Schemas and current `.interface/config/` records, only to check Config validity and to write the Implement Log Entry.

If these sources disagree with this summary, the sources win.

## Coordinated Skills (Claude Code realization)

Invoke each coordinated Operation through the Skill tool, passing the phase selection and the reserved Implement Log identifier as `parent_id`:

| Operation | Skill |
|---|---|
| Configure | `my-interface-configure` |
| Plan | `my-interface-plan <phase>` |
| Develop | `my-interface-develop <phase>` |
| Review | `my-interface-review <phase>` |

No other Operation (for example Launch or Reset) is coordinated by this Skill.

## Procedure (summary of the Implement Definition)

1. Reserve the Implement Log identifier.
2. Check the required Config records once. Coordinate Configure only when they are absent or invalid.
3. Once Config is available, record the active Workflow position as `implementing` and write the Implement Log Entry with the reserved identifier.
4. For each applicable phase in Target order: coordinate Plan, then Develop, then Review. Review performs its own passes until satisfied or blocked.
5. Carry each Operation's outcome forward. Stop when a required condition, Blocker, or unresolved decision prevents safe continuation.
6. Update the Implement Log Entry: common execution fields plus coordination outcomes and child relationships in `data`.

## Execution log

At the start of every execution, create one Log Entry in State for that execution, including its `id` (the reserved identifier), `skill` (`my-interface-implement`), and `started_at`. At completion, update that same Log Entry with `completed_at`, `duration_ms`, `outcome`, `report`, `skills_used`, and any applicable `data`, `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason. Every coordinated Operation Log Entry records this identifier as its `parent_id`.

## Boundaries

- Owns coordination only. Apart from its own Implement Log Entry and the `implementing` position, never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.
- Each coordinated Operation keeps its own scope, authority, Understanding, outcomes, and stopping conditions.
- The primary Agent stays accountable for the integrated result (see the Delegation section of the interface-skill-policy Rule).
