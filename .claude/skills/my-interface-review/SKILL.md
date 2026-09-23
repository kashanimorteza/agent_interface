---
name: my-interface-review
description: Core Interface Skill for reviewing. Independently judges each selected (or every) phase's current Plan and implemented result against the current Interface and Target, records grounded Findings in State Log data, resolves what it is authorized to resolve, and re-reviews until satisfied or blocked. Use when the Human asks to review a developed phase or when Implement coordinates Review.
argument-hint: "[phase-id ...]"
---

<!--
Native realization (Claude Code) of the Core Skill Contract `review`, synchronized by
/my-interface-agent-native. The Human-owned Agent Module remains authoritative; this Skill is
not a second authority. Its operational meaning is owned by the Review Operation Component,
which this Skill reads from its current location at run time.
-->

# Review (`my-interface-review`)

Stable key: `review`. Required. Invocable directly by the Human (`/my-interface-review [phase-id ...]`) or by an Agent.

- **Input:** an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).
- **Output:** the Skill execution result and status.
- **Requirements:** a successful Configure execution must have established the required Config records before this Skill runs; each selected phase must have a current Plan and a Development result.

## Before acting

1. Apply the synchronized project Rules (`.claude/rules/`), especially *Agent Interface Skill policy* and *Agent Interface bootstrap*.
2. Through the Interface, locate and read the Review Operation Component Definition (currently `.interface/implementation/operations/review/review.md`) and Preferences (`review.yaml`). They own this Skill's meaning; when they differ from the summary below, they win.
3. Record the Workflow position `reviewing` when Review begins.

## What Review does

- Considers selected phases, or every phase when none is selected. For each phase with generated Source available, establishes current Target, Interface, and Source Understanding **within that phase's scope** (no unrelated Source).
- Reads the current Plan, then judges the generated Source, Public Interface, implemented result, and evidence against that Plan and the current authorities — never against the implementer's intent or what a reviewer would have built. Silence in the baseline is not a requirement.
- **Independent:** observes each required condition itself; may read the implementer's check and evidence but judges whether that check actually establishes the condition, never accepting "it passed" as proof.
- **Every Finding** states what was expected, what was observed, and the exact location or observable result that shows it. Untraceable concerns are reported as observations about the review, not Findings.
- **Missing evidence** for an acceptance criterion is its own Finding; never reconstruct, infer, or accept an explanation in its place.
- **Cycle per pass:** write one Log Entry per pass with Findings in its `data` → resolve each Finding Review is authorized and able to resolve → record the resolution in a new Log Entry → run another independent pass. Continue until no Finding remains or a Blocker prevents continuation. An unresolvable Finding goes to `open_questions` or `blockers` and stops the cycle.
- Records the phase's aggregate Review outcome (`satisfied`, `not satisfied`, or `inconclusive`) in State.

## Boundaries

- May change only the reviewed implementation and the evidence needed to resolve one of its recorded Findings.
- **Never** defines new requirements, changes Target meaning, Plan content, or Task status, reopens Tasks, or changes another Operation's record. Work newly required by Target belongs to Planning.
- Every other `.interface/` path is read-only.

## Stop conditions

Required result or evidence unavailable, an authority cannot be established, or an unresolved condition prevents assurance. Always report the reason.
