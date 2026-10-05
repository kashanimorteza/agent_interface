---
name: my-interface-develop
description: Core Skill `develop` — executes the eligible planned Tasks of one or more Target phases and produces the resulting Development work, recording evidence and progress in each Task's Task Log. Optional phase identifiers; with none, develops every active and developable phase in Target order.
argument-hint: "[phase-id ...] [parent_id=<id>]"
---

# Develop — Core Skill `develop`

Required Core Skill. Stable key: `develop`. Skill name: `my-interface-develop`.

Synchronized Native realization. The governing authority is the current Develop Operation Definition and Preferences in the Implementation Module; this Skill realizes their meaning and never overrides them.

## Invocation and inputs

- May be invoked directly by the Human or by an Agent (including a coordinating Core Skill).
- Inputs: an invocation request and an optional phase selection — one or more Target phase identifiers. When a coordinating Core Skill invokes it, the request carries `parent_id=<that Skill's Log Entry ID>`.

## Start

1. Apply the loaded Runtime Rules first: `interface-skill-policy`, `interface-bootstrap`, `agent-conduct`, `git-discipline`.
2. Locate through `.interface/interface.md` (Implementation Module → Operations → Develop) and read in full the current Develop Definition and Develop Preferences (last synchronized at `.interface/implementation/operations/develop/develop.md` and `develop.yaml`), plus the State Definition and Schema needed to write records. If they contradict this Skill, follow them and report Runtime drift so the Human can run `/my-interface-agent-native`.
3. Never read, search, or use `.interface/agent/`.

## Workflow

1. **Understanding.** Establish current Interface Understanding and Target Understanding.
2. **Prerequisites.** Start only when the required Config records are valid and the current Plan exists for each applicable phase. If Config or Plan is unavailable, stop — never run Configure or Plan.
3. **Log Entry.** Create this execution's State Log Entry (see Execution Log).
4. **Phase selection.** Use the selected phase identifiers, or every active and developable Target phase when none is selected, in Target order.
5. **Eligibility.** Execute only selected eligible Tasks whose authority, scope, inputs, outputs, and completion conditions are understood and whose dependencies are complete. Readiness comes from declared dependencies, never from file order. If no eligible Task exists, complete without changing implementation work.
6. **Replacement first.** When a new Task identifies an earlier developed Task through `replaces`, mark that earlier Task `replaced` and record the relationship in its Task Log before executing the new Task.
7. **Claim, then execute.** Claim each eligible Task before changing its result. Consider its Task Skills; any other suitable available Skill may also be used. Realize the work under the owning Development Components' Definitions and Preferences; Develop Preferences supply defaults only where the Plan and those authorities are silent. Preserve valid existing work.
8. **Task Log (append-only).** Record Task-specific evidence, progress transitions, and any Task-specific Blocker, and update the Task status. A choice made on Develop's own proposal is recorded as a decision in that Task's Task Log, and the Task is listed under `decisions` in this execution's State Log Entry `data`. Execution history may record what was done, relevant locations, and observed outcomes — never secret values, and never as an authority for future technical choices.
9. **Blocker resolution.** Only when a blocking condition is verified as resolved: record the resolution evidence and transition in the Task Log, clear the obsolete Blocker reference, return unfinished blocked work to its initial pending status, and recheck dependencies and remaining conditions before claiming it again. Resolution never marks work complete. If another condition still blocks, the reference names that current condition. Coordinate removal of the State Blocker with these updates. A missing Blocker record alone is not evidence of resolution.
10. **Generation rules.**
    - Write, change, document, and remove artifacts only inside the Component a Task realizes. Never change a Component's contract because another Component lacks a capability.
    - Deterministic: unchanged Target, Definitions, Preferences, and resolved technical selections produce the same ordered output with zero source or documentation difference. Classify authoritative additions, modifications, explicit renames, and removals; update every affected public surface together; preserve unaffected and still-declared meaning; remove only the Component's own obsolete output. Never infer a rename or removal from name similarity, missing understanding, or generator limitation. Add compatibility aliases or historical versions only under explicit authority. Develop owns no data migration.
    - Failure is explicit and atomic: collect independent actionable failures when safe, identify the affected item without exposing a sensitive value, publish only complete output, and preserve the last valid output on failure. Never hide an error through omission, coercion, fallback, invention, or partial publication.
    - Technology standard: write to the selected technology's standard, declare only necessary dependencies with concrete stabilized versions, and emit no dead, duplicate, incomplete, cached, compiled, machine-specific, Agent-identifying, timestamped, or narratively generated artifact.
    - Develop checks nothing beyond completing its own output; conformance and acceptance are established by Review.
11. **Stop** when a dependency or prerequisite is unmet, verification fails, or an unresolved condition other than an unset choice prevents completion; report the exact reason.
12. **State.** Update only the aggregate Development progress and Active State as the State Definition assigns to development, including clearing a phase's completion time when new or replacement development work reopens it.

Never invokes another Core Operation (no other `my-interface-*` Core Skill); stops and reports when another Operation is required.

## Execution Log (mandatory)

- At start (after prerequisites hold), create exactly one Log Entry in the State Config: next project-wide sequential zero-padded `id`, the Skill, `parent_id` when supplied, the Phase when phase-specific, the event, start time, and an in-progress outcome, following the current State Definition and Schema.
- When work completes, stops, or is blocked, update that same Entry with outcome, report, `data` (including `decisions`), Open Questions, Blockers, and `duration` when timing is known.
- If the State Config is missing or invalid, do not create or repair it; report the stop and the unrecorded Entry as a Blocker in the output.
- Never copy Task histories, transcripts, secrets, or Target content into the Log.

## Boundaries

- Never changes Target meaning, Plan authority (never designs or changes Tasks), Development Principles, or another Component's owned record without explicit authority; never expands Task scope.
- Never edits `.interface/`. Never commits or pushes.

## Output

The Skill execution result and status: Tasks claimed, completed, replaced, blocked, or skipped with their evidence; decisions made; the Log Entry ID; and any Blockers and Open Questions.
