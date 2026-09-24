---
name: my-interface-review
description: Core Interface Skill "review" — independently judges selected (or all) phases' Plans and implemented results against the current Interface, Target, and Plan, records grounded Findings in its State Log Entry, resolves what it is authorized to resolve, and rechecks. Use after development to establish whether a phase is satisfied.
argument-hint: "[phase-id ...]"
---

<!-- Synchronized by /my-interface-agent-native from the Review Skill Contract and its Sources. Do not edit here; this Skill is a Runtime realization, never an authority. -->

# Review

The Core Skill for reviewing. Stable key: `review`. Required. No Personality is declared.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-review [phase-id ...]`) or by an Agent (for example the Implement coordinator).
- Inputs: an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers; none selected means every phase). When a coordinator supplies a parent Log identifier, record it as `parent_id`.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Each selected phase must have a current Plan and a Development result. When the required result or evidence is unavailable, stop and record why.

## Before acting

1. Apply the project Rules `interface-bootstrap`, `interface-skill-policy`, and `git-discipline` (`.claude/rules/`). Never read `.interface/agent/`.
2. Read the current Operation authorities in full — they govern over this summary if they differ:
   - `.interface/implementation/operations/review/review.md` (Definition and mandatory Principles)
   - `.interface/implementation/operations/review/review.yaml` (Preferences; currently no defaults, and they can never lower the required evidence or independence)
3. Use current aggregate progress and prior Review Log Entries from State as context, never as authority.
4. For each phase, once generated Source is available, establish current Target Understanding, Interface Understanding, and Source Understanding within that phase's scope only (no unrelated Source).

## Workflow

1. When Review begins, record the active Workflow position as `reviewing` in State and create this execution's single Log Entry.
2. For each applicable phase: read the current Plan, then judge the generated Source, Public Interface, implemented result, and evidence against that Plan and the current authorities.
3. Record every Finding in the Log Entry's `data` **before** resolving anything. A Finding states what was expected, what was observed, and the exact location or observable result that shows it.
4. Resolve the Findings you are authorized and able to resolve, update those same Finding records with each resolution, and review the result again after each resolution.
5. A Finding that cannot be resolved is recorded in `open_questions` or `blockers` and stops the cycle.
6. Record the aggregate Review outcome per phase in State (`satisfied` when the result satisfies the current Plan and applicable authorities, otherwise `not satisfied`; set `completed_at` when satisfied).

A later independent Review execution creates its own Log Entry. Stop when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance.

## Principles (all mandatory)

- **Judge against the current Plan and authorities** — not against the implementer's intent or what a reviewer would have built. Never define a new requirement, change Plan content, or treat silence in the baseline as a requirement; work newly required by Target belongs to Planning.
- **Independence.** Observe each required condition for yourself. You may read the implementer's check and recorded evidence, but judge whether that check actually establishes the condition; a passing check is never proof by itself.
- **Every Finding is grounded in an observation** a reader can see without repeating the review. An unobservable concern is said as an observation about the review itself, not recorded as a Finding.
- **Missing evidence is a Finding.** An acceptance criterion with nothing observable behind it is recorded as a missing-evidence Finding. Never reconstruct or infer missing evidence, and never accept an explanation in its place. Missing evidence is not a claim that the requirement is unmet.
- **A Finding outlives the session.** Every Finding is stored in this Skill's State Log `data` and stays traceable through the Entry that raised, resolved, or left it open.

## Boundaries

Review may change only the reviewed implementation and the evidence needed to resolve one of its recorded Findings, plus its own State records. It never changes Target meaning, Plan content, Task status, or any other Operation's owned record, and never reopens Tasks. Never modify any `.interface/` path outside `.interface/config/`.

## Execution Log

At the start of every execution, create one Log Entry in State with its `id` (next project-wide sequential identifier, zero-padded to at least three digits), `skill: review`, and `started_at`. At completion, update that same entry with `completed_at`, `duration_ms`, `outcome`, `report`, `skills_used`, and any applicable `data` (Findings and resolutions), `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Output

The Skill execution result and status: per-phase outcome, Findings with evidence and resolution state, Blockers and Open Questions, and the Log Entry id.
