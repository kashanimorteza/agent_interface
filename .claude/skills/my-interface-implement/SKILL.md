---
name: my-interface-implement
description: Core Skill for implementing (stable key `implement`). Coordinates the Operations workflow across the selected (or every) Target phase in Target order — Configure once only when Config is absent or invalid, then Plan, Develop, and Review for each phase — carrying each outcome forward and reporting aggregate Open Question and Blocker counts. Use to run the full implementation workflow. Invocable by the Human (/my-interface-implement [phase-id ...]) or by an Agent.
argument-hint: "[phase-id ...]"
---

<!-- Synchronized by Agent Native Sync (/my-interface-agent-native) from the Implement Skill Contract and the Implement Operation Definition and Preferences it names. Change those Human-owned sources and re-run that synchronization; do not edit this copy. -->

# Implement

The Core Skill for implementing. Required. Stable key: `implement`. Skill name: `my-interface-implement`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection: zero or more Target phase identifiers (`$ARGUMENTS`).

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Sources

Read these current Operation sources in full before acting. They are the authority for coordination; this Skill never copies their facts and never writes to them.

- `.interface/implementation/operations/implement/implement.md` — Implement Definition and its mandatory Principle.
- `.interface/implementation/operations/implement/implement.yaml` — Implement Preferences (currently no coordination defaults).

Implement does not establish Target or Interface Understanding for the work; each coordinated Skill establishes the Understanding its own responsibility requires. Locate the phase identifiers and their Target order through `.interface/interface.md`.

## Coordinated Skills

Invoke each through the Skill tool, passing the phase selection and `parent_id=<this execution's Log Entry ID>` as arguments:

- `my-interface-configure`
- `my-interface-plan`
- `my-interface-develop`
- `my-interface-review`

## Workflow

1. Apply the project Rules (`interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`). If one is missing, report Runtime drift.
2. Read the Sources above. Check the required Config records once.
3. Execution Log: create one Log Entry in State for this execution, including its ID and Skill, following the current State Definition and Schema, as soon as State Config is valid. Supply this ID as the `parent_id` of every Skill you coordinate.
4. If the Config records are absent or invalid, coordinate `my-interface-configure` once (with `parent_id` when this execution's Entry already exists; when State Config did not yet exist, create this execution's Entry right after Configure and report that the Configure Entry could not carry a `parent_id`). Never edit another Skill's Log Entry. If Config remains absent or invalid after that attempt, stop before Plan, Develop, or Review.
5. Resolve the phases: the selected phase identifiers, or every Target phase in Target order when none is selected.
6. For each phase in order, coordinate `my-interface-plan`, then `my-interface-develop`, then `my-interface-review`. A blocked Develop does not by itself skip Review: when Source is available, Review still runs and performs its own passes until its result is satisfied or a Blocker prevents continuation.
7. Carry each Operation Outcome forward. Unresolved Blockers or Open Questions may make the final outcome blocked, but do not prevent an applicable Review.
8. Update the same Log Entry with the outcome, a concise report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. Its execution data includes the unique counts of associated Open Questions and Blockers.

## Boundaries

Implement owns coordination only. Preserve each coordinated Skill's scope and outcome; never change a Plan, Development result, Review Finding, or State record outside the authority of its owning Component, and never perform a coordinated Skill's work itself.

## Outputs

The Skill execution result and status, including the aggregate counts of associated Open Questions and Blockers.
