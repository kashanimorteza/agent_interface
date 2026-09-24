---
name: my-interface-implement
description: Core Interface Skill "implement" — coordinates Configure (only if Config is absent or invalid), then Plan, Develop, and Review for each selected (or every) Target phase in order, linking every coordinated Log Entry to its own Implement Log Entry and reporting aggregate Open Question and Blocker counts. Use to run the full implementation cycle.
argument-hint: "[phase-id ...]"
---

<!-- Synchronized by /my-interface-agent-native from the Implement Skill Contract and its Sources. Do not edit here; this Skill is a Runtime realization, never an authority. -->

# Implement

The Core Skill for implementing. Stable key: `implement`. Required. No Personality is declared. Implement owns coordination only — never the work performed by Configure, Plan, Develop, Review, or State.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-implement [phase-id ...]`) or by an Agent.
- Inputs: an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers; none selected means every Target phase in Target order).

## Before acting

1. Apply the project Rules `interface-bootstrap`, `interface-skill-policy`, and `git-discipline` (`.claude/rules/`). Never read `.interface/agent/`.
2. Read the current Operation authorities in full — they govern over this summary if they differ:
   - `.interface/implementation/operations/implement/implement.md` (Definition and mandatory Principle)
   - `.interface/implementation/operations/implement/implement.yaml` (Preferences; currently no defaults — they supply only coordination defaults)
3. Implement does not establish Target or Interface Understanding for the work; each coordinated Operation establishes the Understanding its own responsibility requires. Read `.interface/interface.md` only as needed to resolve the phase list and Target order.

## Coordinated Skills

| Operation | Claude Code Skill |
|---|---|
| Configure | `my-interface-configure` |
| Plan | `my-interface-plan` |
| Develop | `my-interface-develop` |
| Review | `my-interface-review` |

Invoke each through the Skill tool with the phase selection and the reserved Implement Log identifier as its `parent_id`. If one of these Skills is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Workflow

1. Reserve the Implement Log identifier (the next project-wide sequential State Log id, zero-padded to at least three digits).
2. Check the required Config records once. Coordinate Configure only when they are absent or invalid.
3. Once Config is available, record the active Workflow position as `implementing` in State and write the Implement Log Entry with the reserved identifier (`skill: implement`, `started_at`).
4. For each phase, in order, coordinate **Plan → Develop → Review**:
   - A blocked Develop does not by itself skip Review: when Source is available, Review still examines it and records its outcome.
   - Review continues its own passes until its result is satisfied or a Blocker prevents continuation.
   - Carry each Operation Outcome forward; unresolved Blockers or Open Questions may make the final outcome blocked but never prevent an applicable Review.
5. Verify every coordinated Operation Log Entry records the reserved Implement Log identifier as its `parent_id`.
6. Complete the Implement Log Entry: common execution fields, coordination-specific outcomes, and the unique counts of associated Open Questions and Blockers in `data`.

## Boundaries

Apart from appending and completing its own Implement Log Entry (and the Workflow position), Implement never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component. Each coordinated Skill retains its own scope, records, and outcome. Never modify any `.interface/` path outside `.interface/config/`.

## Execution Log

At the start of every execution, create one Log Entry in State with its `id`, `skill: implement`, and `started_at` (using the reserved identifier once Config is available). At completion, update that same entry with `completed_at`, `duration_ms`, `outcome`, `report`, `skills_used`, and applicable `data`, `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Output

The Skill execution result and status, including each coordinated Operation Outcome per phase and the aggregate (unique) counts of associated Open Questions and Blockers.
