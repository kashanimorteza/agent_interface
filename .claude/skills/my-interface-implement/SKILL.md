---
name: my-interface-implement
description: Agent Interface Core Skill `implement`. Coordinates the Operations workflow for each selected (or every) Target phase — Configure only when Config is absent or invalid, then Plan, Develop, and Review in that order — carrying outcomes forward and recording the coordination and its Open Question and Blocker counts in State. Use when the Human or an Agent asks to implement one or more phases end to end.
argument-hint: "[phase-id ...]"
---

# Implement (`implement`)

The Core Skill for implementing. Required. Stable key: `implement`. Skill name: `my-interface-implement`.

This Skill is a synchronized, self-contained Runtime realization. Its meaning comes from the Implement Operation Definition and Preferences, read fresh on every run; this file never replaces them. Never read or search `.interface/agent/`. If something this Skill needs is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Personality

No Personality is declared. Work under the global Rules and the active Output Style.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-implement [phase-id ...]`) or by an Agent (Skill tool).
- Inputs: an invocation request and an optional phase selection — zero or more Target phase identifiers in `$ARGUMENTS`. With none, coordinate every Target phase in Target order.

## Coordinated Skills

Invoke each participating Operation through its synchronized Skill (Skill tool), passing the phase selection and the reserved Implement Log identifier to record as `parent_id`:

| Operation | Skill |
|---|---|
| Configure | `my-interface-configure` |
| Plan | `my-interface-plan` |
| Develop | `my-interface-develop` |
| Review | `my-interface-review` |

If one of these Skills is missing or unusable, stop that step, report Runtime drift, and ask the Human to run `/my-interface-agent-native`.

## Workflow

1. **Read the Implement Operation completely** — `.interface/implementation/operations/implement/implement.md` (Definition and mandatory Principle) and `.interface/implementation/operations/implement/implement.yaml` (Preferences). They are authoritative; if they differ from anything in this file, they win. Locate them through `.interface/interface.md` per the global `interface-bootstrap` Rule. Implement does not itself establish Target or Interface Understanding for the work; each participating Skill establishes the Understanding its own responsibility requires.
2. **Reserve the Implement Log identifier** before anything else runs.
3. **Check the required Config records once.** Coordinate `my-interface-configure` only when they are absent or invalid.
4. **Execution Log — start.** Once Config is available, record the active Workflow position as `implementing` and write this execution's Implement Log Entry with the reserved `id`, `skill: implement`, and `started_at`.
5. **For each phase, in order: Plan → Develop → Review.** A blocked Develop does not by itself skip Review: when Source is available, Review still runs its own passes until its result is satisfied or a Blocker prevents continuation. Carry each Operation's outcome forward; unresolved Blockers or Open Questions may make the final outcome blocked but do not prevent an applicable Review.
6. **Execution Log — completion.** Update the same Implement Log Entry with `completed_at`, `duration_ms`, `outcome`, a concise `report`, coordination-specific outcomes in `data`, and the unique counts of associated Open Questions and Blockers in `data`. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Boundaries

- Apart from its own Implement Log Entry and the Workflow position, never change a Plan, Development result, Review Finding, or State record outside the authority of its owning Component. Every other `.interface/` path is read-only.
- Coordination never takes ownership of another Operation's work, records, or results.
- Never read `.interface/agent/` and never invoke `/my-interface-agent-native`.

## Outputs

The Skill execution result and status, including each coordinated Operation's outcome per phase and the aggregate counts of associated Open Questions and Blockers; the Implement Log Entry `id`.
