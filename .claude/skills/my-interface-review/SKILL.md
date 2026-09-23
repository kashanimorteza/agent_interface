---
name: my-interface-review
description: Agent Interface Core Skill `review`. Independently judges the Plan and implemented result of selected (or every) Target phase against the current Interface, Target, and Plan; records grounded Findings in State, resolves those it is authorized to resolve, and re-reviews until satisfied or blocked. Use when the Human or an Agent asks to review one or more developed phases.
argument-hint: "[phase-id ...]"
---

# Review — Core Skill `review`

Synchronized Claude Code realization of the Agent Interface Core Skill with stable key `review` (required). It was produced by Agent Native Sync and is self-contained: it is not an authority, and it never needs the Agent Module. The Operation's authoritative meaning lives in the Implementation sources named under **Authorities** and is read at run time.

## Personality

No Personality is declared. Use the project's standing conduct Rules.

## Invocation and inputs

- Invoked directly by the Human (`/my-interface-review [phase-id ...]`) or by an Agent (for example `my-interface-implement` through the Skill tool).
- Inputs: the invocation request and an optional phase selection. Selected phases: `$ARGUMENTS` (empty means every phase).
- Output: the Skill execution result and status.

## Standing rules

Apply the project Rules in `.claude/rules/` (interface-bootstrap, interface-skill-policy, git-discipline, interface-agent-capabilities).

## Requirements

- A successful Configure execution must already have established the required Config records.
- Each selected phase must have a current Plan and a Development result.

If a requirement is absent, stop and record it; never run Configure, Plan, or Develop.

## Authorities (read at run time, before acting)

1. Interface Understanding: `.interface/interface.md` and the Foundation section files it links.
2. Target Understanding: both Target definitions the Interface locates, under the precedence it declares.
3. Source Understanding: the generated Source within the selected phase's scope only.
4. `.interface/implementation/operations/review/review.md` and `review.yaml` — Review Definition, Principles, and Preferences.
5. The applicable Implementation Principles and Preferences, the current phase Plan in `.interface/config/plan.yaml`, and prior Review Log Entries in `.interface/config/state.yaml` (execution record, never authority).

If these sources disagree with this summary, the sources win.

## Procedure (summary of the Review Definition)

1. Verify requirements; create this pass's Log Entry; record the active Workflow position as `reviewing`.
2. Establish Target, Interface, and Source Understanding for the phase; read the current Plan.
3. Judge the generated Source, Public Interface, implemented result, and evidence against that Plan and the current authorities. Observe each required condition yourself; an implementer's passing check is not proof unless it actually establishes the condition.
4. Record Findings first, in the Log Entry's `data`. Each Finding states what was expected, what was observed, and the exact location or observable result. An acceptance criterion with nothing observable behind it is a Finding of missing evidence — never reconstruct or infer it.
5. Resolve each Finding you are authorized and able to resolve (changing only the reviewed implementation and the evidence needed for that Finding). Record the resolution in a new Log Entry and run another independent pass.
6. Repeat until no Finding remains (`satisfied`) or an unresolvable Finding is recorded in `open_questions` or `blockers`, which stops the cycle (`not satisfied`).
7. Record the phase's aggregate Review outcome under State.

## Stop conditions

Stop when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance.

## Execution log

At the start of every execution (each pass), create one Log Entry in State, including its `id`, `skill` (`my-interface-review`), and `started_at`. At completion, update that same Log Entry with `completed_at`, `duration_ms`, `outcome`, `report`, `skills_used`, and any applicable `data` (Findings and their state), `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason. When invoked by Implement, record the supplied Implement Log identifier as `parent_id`.

## Boundaries

- Never defines a new requirement; silence in the baseline is not a requirement.
- Never changes Target meaning, Plan content, Task status, or any other Operation's owned record; never reopens Tasks.
- Writes Findings, Review progress, the `reviewing` position, and its Log Entries under State rules, plus only the resolutions described above.
