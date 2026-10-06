---
name: my-interface-review
description: Core Skill for reviewing. Independently judges selected phases' generated Source and evidence against the current Plan and each realized Development Component's Review category, recording, resolving, and rechecking grounded Findings in State. Use when asked to review a phase or when invoked as /my-interface-review [phase ...].
argument-hint: "[phase-id ...]"
---
<!-- managed by /my-interface-native-implement: realized from the Executor Module Skill Contract `review`; regenerated on every run — do not edit by hand -->

# Review

The Core Skill for reviewing. Required. Stable key: `review`. Skill name: `my-interface-review`.

## Inputs

An invocation request and an optional phase selection: `$ARGUMENTS` (zero or more Target phase identifiers).

## Invocation

May be invoked directly by a Human (`/my-interface-review`) or by an Agent. Among Core Skills, only Implement may invoke it. Review never invokes another Core Skill; it may use any Provider Skill or other suitable available Skill.

## Authority — read at runtime

Read completely at the start of every run and follow them; this workflow is the Native realization of that understanding and never overrides them.

- `.interface/implementation/operations/review/review.md` — Review's mandatory Principles.
- `.interface/implementation/operations/review/review.yaml` — Review Preferences.
- The `Review` category of every Development Component the phase realizes, and the applicable testing authority, located through the Interface.

Every Principle in the Definition is mandatory. Review Preferences can never lower the evidence or independence those Principles require.

Apply the project Rules (`.claude/rules/`).

## Workflow

1. If the State Config record exists and is structurally valid, create this execution's State Log Entry first, so that every outcome — including a stop — is recorded in it.
2. Verify required Config records are valid; otherwise stop. Record the stopped outcome in the Log Entry when State is writable; otherwise report explicitly that the Entry could not be written.
3. Select phases: the given identifiers, or every phase when none is given. Use current aggregate progress and prior Review Log Entries in State as context only, never as authority.
4. For each phase with generated Source available (whether or not Development completed): establish Source Understanding within that phase's scope only, read the current Plan, and judge the generated Source, Public Interface, implemented result, and evidence against it.
5. Also check every observation in the `Review` category of each Development Component the phase realizes — exactly as that Component states it, adding none. A Task's acceptance holds only once Review has established it.
6. Establish technical and repeatable conformance: validate generation inputs (completeness, uniqueness, compatibility, naming, reference resolution, technology support); verify installability and importability; run the selected technology's format, import, compile, build, lint, static type, dependency, and runtime checks with no fixable warning owned by the Component; verify zero-diff regeneration from unchanged authorities. When persistent testing is disabled, verify transiently; never widen the declared testing scope.
7. Observe every required condition independently: read the implementer's checks and evidence, but judge whether they actually establish the condition; a passing check is not proof. Independence concerns the judgment, not the sources: judge against the phase Plan and the generated Source, never an invented different standard.
8. Record each Finding (expected, observed, exact location or observable result) in this execution's Log Entry `data` before resolving it. An acceptance criterion with nothing observable behind it is its own Finding of missing evidence — never reconstruct or infer it, and never accept an explanation in its place. Missing evidence states what the record does not show; it is not a claim that the requirement is unmet.
9. Resolve Findings where possible, changing only the reviewed implementation and the evidence needed for that Finding, then recheck and update the same Finding record. A Finding that cannot be resolved goes to `open_questions` or `blockers` and stops further review work on that condition.
10. Set the Outcome (`satisfied` / `not satisfied`), update aggregate Review progress in State, complete the Log Entry, and report.

Stop when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance.

## Boundaries

Never define a new requirement (work newly required by Target belongs to Planning), treat silence in the Plan as a requirement, change Plan content, Target meaning, Task status, or any other Operation's owned record, or reopen Tasks. Never repair ambiguity by invention or change another Component while resolving a Finding. A concern that cannot be observed is reported as an observation about the review, not a Finding.

## Execution Log

Every execution creates one Log Entry in State with its `id` and Skill, and updates that same Entry with outcome, report, and any applicable `data` (all Findings and their states), Open Questions, or Blockers when work completes, stops, or is blocked. Follow the State Component (`.interface/implementation/operations/state/state.md`) and State Schema. When invoked by Implement, use the supplied Implement Log Entry ID as `parent_id`.

## Outputs

The Skill execution result and status.
