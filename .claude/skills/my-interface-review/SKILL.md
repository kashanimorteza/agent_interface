---
name: my-interface-review
description: Core Skill for reviewing. Independently judges each selected (or every) phase's generated Source, Public Interface, implemented result, and evidence against its current Plan; records grounded Findings in State, resolves what it is authorized to resolve, and rechecks. Use when phase work must be reviewed.
argument-hint: "[phase-id ...]"
---

# Review (Core Skill)

The Core Skill for reviewing. Required. Stable key: `review`. Skill name: `my-interface-review`.

This Skill is the Claude Code realization of the Review Operation. The current Review Operation Definition and Preferences, located through the Interface, remain the authority for Review's meaning; this Skill restates them so it can run. If they disagree with this Skill, follow the current owning source and report Runtime drift so the Human can run Agent Native Sync. Review Preferences can never lower the evidence or independence required below; they currently declare no defaults (an empty section is an absence of defaults, not a wildcard).

## Personality

No Personality is declared.

## Invocation and inputs

- May be invoked directly by a Human (`/my-interface-review [phase-id ...]`) or by an Agent (for example, coordinated by `my-interface-implement`).
- Inputs: an invocation request and an optional phase selection (one or more Target phase identifiers). When coordinated by Implement, the request carries the coordinator's Log Entry ID as `parent_id`; record it on this execution's Log Entry.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Each selected phase must have a current Plan and generated Source available for examination. Development need not have completed when Source is available.

## Terms

- **Review** — one independent examination of one phase's Plan, generated Source, and evidence.
- **Source Understanding** — understanding the generated Source needed to examine the selected phase without reading unrelated Source.
- **Finding** — one specific way in which the result does not demonstrably satisfy what was asked, recorded with what was expected, what was observed, and where.
- **Evidence** — the exact location or observable result that supports a Finding, so a reader can see it without repeating the review.
- **Outcome** — the aggregate result: `satisfied` when the reviewed result satisfies the current Plan, or `not satisfied` otherwise.
- **Missing evidence** — an acceptance criterion for which nothing observable demonstrates that it holds.

## Procedure

1. Apply the project Rules loaded as project memory (Interface bootstrap, Interface Skill policy, Git discipline).
2. **Execution Log — start.** Create one Log Entry in State for this execution, with its ID, Skill (`my-interface-review`), `started_at`, and `parent_id` when supplied.
3. Select phases: the given Target phase identifiers, or every phase when none is selected.
4. For each phase, once generated Source is available: establish Source Understanding within that phase's scope (do not read unrelated Source), read the current Plan, and examine the generated Source, Public Interface, implemented result, and evidence against that Plan. Use current aggregate progress and prior Review Log Entries from State without treating either as authority.
5. **Record** every Finding in this execution's Log Entry `data` before resolving it. Each Finding states what was expected, what was observed, and the exact location or observable result that shows it.
6. **Resolve** the Findings you are authorized and able to resolve, changing only the reviewed implementation and the evidence needed to resolve that recorded Finding. Update the same Finding record with each resolution, then review the result again. Continue passes until the result is satisfied or a Blocker prevents continuation.
7. A Finding that cannot be resolved is recorded in `open_questions` or `blockers` and stops further review work on that unresolved condition; it remains open.
8. **Stop** when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance. Report the exact reason.
9. **Execution Log — completion.** Update the same Log Entry with `completed_at`, `duration_ms`, readable `duration`, outcome (`satisfied` / `not satisfied` per phase and aggregate), report, Findings and their states, and any Open Questions or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Principles (all mandatory)

### Review examines Source against the current Plan
- Judge the generated Source, Public Interface, implemented result, and evidence against the current Plan — not against what the implementer intended or what a reviewer would have built.
- **Never** define a new requirement, change Plan content, or treat silence in the Plan as a requirement. Work newly required by Target belongs to Planning.

### Review records, resolves, and rechecks its findings
- Record Findings before resolving them and update the same Finding records with each resolution.
- **Never** write Plan content, change Target meaning, change Task status or progress, or change any other Operation's owned record.

### Review is independent of how the work was done
- Observe the required condition for yourself. You may read the implementer's check and recorded evidence, but judge whether that check actually establishes the condition.
- **Never** accept that a check passed as proof that the condition holds. Independence is about the judgment, not the sources: use the phase Plan and the generated Source; do not invent a different standard.

### Every Finding is grounded in an observation
- Every Finding states what was expected, what was observed, and the exact evidence that shows it.
- **Never** record an untraceable statement as a Finding. An unobservable concern may be stated as an observation about the review itself, not as a Finding.

### Missing evidence is a Finding, not an absence
- An acceptance criterion with nothing observable behind it is recorded as a Finding of missing evidence.
- **Never** reconstruct missing evidence, infer it from the implementation, treat a plausible result as proof a check once passed, or accept the implementer's explanation in its place. Missing evidence is not a claim that the requirement is unmet.

### A Finding outlives the session that raised it
- Every Finding is stored in the Review execution's State Log `data`, traceable through that execution's Entry, and its state is updated there when resolved or left open.
- **Never** reopen Tasks or change Plan content.

Ownership: Review owns its Findings, review data, and the resolutions it can perform; it supplies State with the phase's aggregate Review outcome and Review-specific Findings and resolutions. Plan owns planned work; Develop owns implementation work outside Review's resolution scope.

## Outputs

The Skill execution result and status.
