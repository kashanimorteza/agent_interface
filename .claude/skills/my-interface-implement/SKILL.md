---
name: my-interface-implement
description: Core Skill for implementing. Coordinates the Operations workflow across the selected (or every) Target phase — Configure once only if Config is absent or invalid, then Plan, Develop, and Review per phase in that order — carrying each outcome forward and reporting aggregate Open Question and Blocker counts. Use for end-to-end phase implementation.
argument-hint: "[phase-id ...]"
---

# Implement (Core Skill)

The Core Skill for implementing. Required. Stable key: `implement`. Skill name: `my-interface-implement`.

This Skill is the Claude Code realization of the Implement Operation. The current Implement Operation Definition and Preferences, located through the Interface, remain the authority for Implement's meaning; this Skill restates them so it can run. If they disagree with this Skill, follow the current owning source and report Runtime drift so the Human can run Agent Native Sync. Implement Preferences supply only coordination defaults and never replace an owning Component's authority; they currently declare none (an empty section is an absence of defaults, not a wildcard).

## Personality

No Personality is declared.

## Invocation and inputs

- May be invoked directly by a Human (`/my-interface-implement [phase-id ...]`) or by an Agent.
- Inputs: an invocation request and an optional phase selection (one or more Target phase identifiers).

## Coordinated Core Skills

Coordinate through the Skill tool, one at a time, in the required order:

| Operation | Skill |
|---|---|
| Configure | `my-interface-configure` |
| Plan | `my-interface-plan` |
| Develop | `my-interface-develop` |
| Review | `my-interface-review` |

When invoking one, pass the phase identifier(s) it applies to and this execution's Log Entry ID as its `parent_id`. Each coordinated Skill establishes the Understanding required for its own responsibility and records its own outcome.

## Procedure

1. Apply the project Rules loaded as project memory (Interface bootstrap, Interface Skill policy, Git discipline).
2. **Execution Log — start.** Create one Log Entry in State for this execution, with its ID, Skill (`my-interface-implement`), and `started_at`. If the State record does not exist yet, create this entry as soon as Configure (step 4) has established it, with the true `started_at`.
3. Determine the phases: the given Target phase identifiers, or every Target phase in Target order when none is selected. Locate phase identifiers and order through the Interface only to sequence coordination; Implement does not establish Target or Interface Understanding for the work.
4. **Config check — once.** Check whether the required Config records exist and are structurally valid. Coordinate Configure only when they are absent or invalid. If Config remains absent or invalid after that attempt, stop before Plan, Develop, or Review.
5. **Per phase, in order:** coordinate Plan, then Develop, then Review.
   - A blocked Develop does not by itself skip Review: when Source is available, Review still examines it, performing its own passes until its result is satisfied or a Blocker prevents continuation.
   - Carry each Operation Outcome forward. Unresolved Blockers or Open Questions may make the final outcome blocked but do not prevent an applicable Review.
6. Determine the unique counts of associated Open Questions and Blockers across this execution and the executions it coordinated.
7. **Execution Log — completion.** Update the same Log Entry with `completed_at`, `duration_ms`, readable `duration`, outcome, report, the unique counts of associated Open Questions and Blockers in its data, and any applicable data, Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Principle (mandatory) — Implement coordinates the Operations workflow

- **Must** — accept one or more Target phase identifiers, or every Target phase in Target order when none is selected.
- **Must** — check Config once and coordinate Configure only when Config is absent or invalid.
- **Must** — stop before Plan, Develop, and Review if required Config remains absent or invalid after Configure.
- **Must** — coordinate Plan, Develop, and Review in that order for each phase; a blocked Develop does not skip an applicable Review.
- **Must** — preserve each Component's scope and outcome and determine the aggregate counts of associated Open Questions and Blockers.
- **Never** — take ownership of another Operation Component's records or results; never change a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.

Terms: **Operation Outcome** — the recorded result of one coordinated Operation.

Ownership: Implement owns coordination, not the work performed by Configure, Plan, Develop, Review, or State. Each participating Component retains its own authority and records.

## Outputs

The Skill execution result and status, including the aggregate counts of associated Open Questions and Blockers.
