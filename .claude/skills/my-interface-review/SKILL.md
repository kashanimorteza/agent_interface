---
name: my-interface-review
description: Core Skill `review` — independently judges the generated Source, Public Interface, and evidence of one or more Target phases against the current Plan and each realized Component's Review category, then records, resolves, and rechecks its Findings. Optional phase identifiers; with none, reviews every phase.
argument-hint: "[phase-id ...] [parent_id=<id>]"
---

# Review — Core Skill `review`

Required Core Skill. Stable key: `review`. Skill name: `my-interface-review`.

Native realization. The governing authority is the current Review Operation Definition and Preferences in the Implementation Module; this Skill realizes their meaning and never overrides them.

## Invocation and inputs

- May be invoked directly by the Human or by an Agent (including a coordinating Core Skill).
- Inputs: an invocation request and an optional phase selection — one or more Target phase identifiers. When a coordinating Core Skill invokes it, the request carries `parent_id=<that Skill's Log Entry ID>`.

## Start

1. Apply the loaded Runtime Rules first: `interface-skill-policy`, `interface-bootstrap`, `agent-conduct`, `git-discipline`.
2. Locate through `.interface/interface.md` (Implementation Module → Operations → Review) and read in full the current Review Definition and Review Preferences (located, when this Skill was realized, at `.interface/implementation/operations/review/review.md` and `review.yaml`), plus the State Definition and Schema needed to write records. If they contradict this Skill, follow them and report Runtime drift so the Human can run `/my-interface-native-implement`.
3. Never read, search, or use `.interface/executor/`.

## Workflow

1. **Config prerequisite.** Start only when the required Config records are valid; otherwise stop (never run Configure).
2. **Log Entry.** Create this execution's State Log Entry (see Execution Log).
3. **Phase selection.** Use the selected phase identifiers, or every phase when none is selected.
4. **Prior record.** Read current aggregate progress and prior Review Log Entries in State, including earlier unresolved Findings, without treating either as authority.
5. **Source Understanding.** Once generated Source exists for a phase — whether or not Development completed — establish Source Understanding within that phase's scope only, without reading unrelated Source.
6. **Judge against the current Plan.** Read the phase's current Plan and judge the generated Source, Public Interface, implemented result, and evidence against its coverage, acceptance criteria, and verification conditions. Silence in the Plan is never a requirement.
7. **Judge against each Component's Review category.** Read the `Review` category of every Development Component the phase realizes and check each of its observations as that Component states them, adding none. A result failing either baseline is a Finding; a Task's acceptance holds only once Review establishes it.
8. **Technical and repeatable conformance.** Validate generation inputs (completeness, uniqueness, compatibility, naming, reference resolution, technology support). Verify that output is installable and importable and passes the selected technology's format, import, compile, build, lint, static type, dependency, and runtime checks without a fixable Component-owned warning, and that regeneration from unchanged authorities yields zero source or documentation difference. The applicable testing authority decides persisted versus transient evidence: when persistent testing is disabled, verify transiently instead of skipping; never widen the declared testing scope.
9. **Independence.** Observe each required condition yourself. You may read the implementer's checks and recorded evidence, but judge whether a check actually establishes the condition — a passing check is never proof by itself.
10. **Findings.** Each Finding states what was expected, what was observed, and the exact location or observable result that shows it. An acceptance criterion with nothing observable behind it is its own missing-evidence Finding — never reconstruct, infer, or accept an explanation in its place. A concern that cannot be observed is reported as an observation about the review, not recorded as a Finding.
11. **Record, resolve, recheck.** Record every Finding in this execution's Log Entry `data` before resolving it. Resolve a Finding only by changing the reviewed implementation and the evidence needed for that Finding, then update the same Finding record and recheck. A Finding that cannot be resolved goes to `open_questions` or `blockers` and stops further review work on that condition. Never repair ambiguity by invention or change another Component while resolving.
12. **Outcome.** `satisfied` when the reviewed result satisfies the current Plan, otherwise `not satisfied`. Update only the aggregate Review progress and Active State as the State Definition assigns to reviewing.
13. **Stop** when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance; report the exact reason.

## Execution Log (mandatory)

- At start (after the Config prerequisite holds), create exactly one Log Entry in the State Config: next project-wide sequential zero-padded `id`, the Skill, `parent_id` when supplied, the Phase when phase-specific, the event, start time, and an in-progress outcome, following the current State Definition and Schema.
- When work completes, stops, or is blocked, update that same Entry with outcome, report, `data` (every Finding with its current state), Open Questions, Blockers, and `duration` when timing is known. Findings live there so they outlive the session.
- If the State Config is missing or invalid, do not create or repair it; report the stop and the unrecorded Entry as a Blocker in the output.
- Never copy Task histories, transcripts, secrets, or Target content into the Log.

## Boundaries

- Never defines new requirements, changes Plan content, changes Target meaning, changes Task status, reopens Tasks, or changes another Operation's owned record. Work newly required by Target belongs to Planning.
- Never edits `.interface/`. Never commits or pushes.

## Output

The Skill execution result and status: per-phase outcome (`satisfied` / `not satisfied`), Findings with their evidence and state, checks performed, the Log Entry ID, and any Blockers and Open Questions.
