---
name: my-interface-review
description: Agent Interface Core Skill `review`. Independently judges each selected (or every) Target phase's Plan and implemented result against the current Interface, Target, and Plan — recording grounded Findings in State, resolving what it may, and re-reviewing until satisfied or blocked. Use when the Human or a coordinating Agent asks to review developed work.
argument-hint: "[phase-id ...]"
---

# Review (`review`)

The Core Skill for reviewing. Required. Stable key: `review`. Skill name: `my-interface-review`.

This Skill is a synchronized, self-contained Runtime realization. Its meaning comes from the Review Operation Definition and Preferences, read fresh on every run; this file never replaces them. Never read or search `.interface/agent/`. If something this Skill needs is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Personality

No Personality is declared. Work under the global Rules and the active Output Style.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-review [phase-id ...]`) or by an Agent (Skill tool), including a coordinating Skill.
- Inputs: an invocation request and an optional phase selection — zero or more Target phase identifiers in `$ARGUMENTS`. With none, consider every phase.
- When invoked by a coordinator, the coordinator supplies its reserved Log identifier; record it as each Log Entry's `parent_id`.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Each selected phase must have a current Plan and a Development result.

If either is absent, stop and record the unmet prerequisite. Never run another Core Operation yourself.

## Workflow

1. **Execution Log — start.** Create one Log Entry in the State Config (`.interface/config/state.yaml`) for this execution with its `id`, `skill: review`, and `started_at`. Each later review pass writes its own Log Entry, as the Review Operation requires.
2. **Establish Understanding.** Read `.interface/interface.md` and the Foundation section files it links, as the global `interface-bootstrap` Rule requires; then establish Target Understanding from the Target definitions the Interface locates, under the precedence it declares, and Source Understanding limited to the selected phase's scope.
3. **Read the Review Operation completely** — `.interface/implementation/operations/review/review.md` (Definition and every mandatory Principle) and `.interface/implementation/operations/review/review.yaml` (Preferences). These are authoritative; if they differ from anything in this file, they win.
4. **Validate prerequisites** as stated under Requirements, then record the active Workflow position as `reviewing`.
5. **Review each phase.** Read its current Plan; judge the generated Source, Public Interface, implemented result, and evidence against that Plan and the current authorities. Observe each required condition yourself — an implementer's passing check is not proof. Every Finding states what was expected, what was observed, and the exact evidence; an acceptance criterion with nothing observable behind it is a Finding of missing evidence. Silence in the baseline is never a requirement.
6. **Record, resolve, recheck.** Record the pass's Findings in its Log Entry `data` first; then resolve each Finding you are authorized and able to resolve, record the resolution in a new Log Entry, and run another independent pass. A Finding that cannot be resolved goes to `open_questions` or `blockers` and stops the cycle.
7. **Record the aggregate Review outcome** per phase in State — `satisfied` or `not satisfied`.
8. **Execution Log — completion.** Update the Log Entry with `completed_at`, `duration_ms`, `outcome`, a concise `report`, Findings and resolutions in `data`, the Skills actually used, and any Open Questions or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Stop conditions

Stop when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance — and record why.

## Boundaries

- Change only the reviewed implementation and the evidence needed to resolve one of your recorded Findings, plus this execution's State records inside `.interface/config/`. Every other `.interface/` path is read-only.
- Never define new requirements, change Plan content or Task status, reopen Tasks, change Target meaning, or change another Operation's owned record.
- Never read `.interface/agent/` and never invoke `/my-interface-agent-native`.

## Outputs

The Skill execution result and status: per-phase outcome, Findings raised, resolved, and open with their evidence; the Log Entry `id`s; and any Open Questions or Blockers.
