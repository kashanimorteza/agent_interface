---
name: my-interface-review
description: Core Skill for reviewing (stable key `review`). Independently judges each selected (or every) phase's generated Source, Public Interface, implemented result, and evidence against its current Plan; records grounded Findings (including missing evidence) in its State Log Entry, resolves those it is authorized to resolve, and rechecks. Use when generated Source for a planned phase must be reviewed. Invocable by the Human (/my-interface-review [phase-id ...]) or by an Agent.
argument-hint: "[phase-id ...]"
---

<!-- Synchronized by Agent Native Sync (/my-interface-agent-native) from the Review Skill Contract and the Review Operation Definition and Preferences it names. Change those Human-owned sources and re-run that synchronization; do not edit this copy. -->

# Review

The Core Skill for reviewing. Required. Stable key: `review`. Skill name: `my-interface-review`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection: zero or more Target phase identifiers (`$ARGUMENTS`). When a coordinating Skill supplies a `parent_id`, record it on this execution's Log Entry.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs. Each selected phase must have a current Plan and generated Source available for examination. Development need not have completed when Source is available.

## Sources

Read these current Operation sources in full before acting. They are the authority for Review; this Skill never copies their facts and never writes to them.

- `.interface/implementation/operations/review/review.md` — Review Definition and its mandatory Principles.
- `.interface/implementation/operations/review/review.yaml` — Review Preferences (currently no defaults; they can never lower the required evidence or independence).

## Workflow

1. Apply the project Rules (`interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`). If one is missing, report Runtime drift.
2. Verify the Requirements. Execution Log: create one Log Entry in State for this execution, including its ID and Skill, following the current State Definition and Schema.
3. Read the Sources above. Resolve the phases: the selected phase identifiers, or every phase when none is selected.
4. For each phase with generated Source available, establish Source Understanding within that phase's scope only, read its current Plan, and judge the generated Source, Public Interface, implemented result, and evidence against that Plan. Use prior Review Log Entries and aggregate progress as context, never as authority.
5. Record every Finding in this execution's Log Entry `data` before resolving it.
6. Resolve the Findings you are authorized and able to resolve, updating those same Finding records, then review the result again. Continue until the result is satisfied or an unresolved condition prevents continuation. Record a Finding that cannot be resolved in `open_questions` or `blockers`; it stops further review work on that condition.
7. Record State's review position and each phase's aggregate Review outcome (`satisfied` or `not satisfied`) as the State Definition prescribes.
8. Update the same Log Entry with the outcome, a concise report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

## Review obligations

- Judge against the current Plan only. Never define a new requirement, change Plan content, or treat silence in the Plan as a requirement; work newly required by Target belongs to Planning.
- Observe each required condition independently. Read the implementer's check and recorded evidence, but judge whether that check actually establishes the condition; a passing check is never proof by itself.
- Every Finding states what was expected, what was observed, and the exact location or observable result that shows it. An untraceable concern is reported as an observation about the review, not recorded as a Finding.
- An acceptance criterion with nothing observable behind it is a Finding of missing evidence. Never reconstruct, infer, or accept an explanation in place of missing evidence; missing evidence is not a claim the requirement is unmet.
- Every Finding is stored in the Review execution's State Log `data` and keeps its state there until resolved or left open.

## Boundaries

Change only the reviewed implementation and the evidence needed to resolve one of your recorded Findings. Never change Target meaning, Plan content, Task status, or any other Operation's owned record, and never reopen Tasks.

## Stop conditions

Stop and report the exact reason, recording it on the Log Entry, when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance.

## Outputs

The Skill execution result and status.
