---
name: my-interface-implement
description: Core Skill `implement` — the single entry point that coordinates the full Operations workflow (Configure only when needed, then Plan, Develop, and Review per phase) for one or more Target phases and reports the aggregate result, including Open Question and Blocker counts. Optional phase identifiers; with none, coordinates every Target phase in Target order.
argument-hint: "[phase-id ...]"
---

# Implement — Core Skill `implement`

Required Core Skill. Stable key: `implement`. Skill name: `my-interface-implement`.

Synchronized Native realization. The governing authority is the current Implement Operation Definition and Preferences in the Implementation Module; this Skill realizes their meaning and never overrides them.

## Invocation and inputs

- May be invoked directly by the Human or by an Agent.
- Inputs: an invocation request and an optional phase selection — one or more Target phase identifiers.

## Start

1. Apply the loaded Runtime Rules first: `interface-skill-policy`, `interface-bootstrap`, `agent-conduct`, `git-discipline`.
2. Locate through `.interface/interface.md` (Implementation Module → Operations → Implement) and read in full the current Implement Definition and Implement Preferences (last synchronized at `.interface/implementation/operations/implement/implement.md` and `implement.yaml`), plus the State Definition and Schema needed to write records. If they contradict this Skill, follow them and report Runtime drift so the Human can run `/my-interface-agent-native`.
3. Never read, search, or use `.interface/agent/`.
4. Implement does not establish Target or Interface Understanding for the coordinated work; each coordinated Operation establishes the Understanding its own responsibility requires.

## Coordinated Core Skills

| Operation | Native Skill | Invoke with |
|---|---|---|
| Configure | `my-interface-configure` | `parent_id=<this Log Entry ID>` |
| Plan | `my-interface-plan` | `<phase-id> parent_id=<this Log Entry ID>` |
| Develop | `my-interface-develop` | `<phase-id> parent_id=<this Log Entry ID>` |
| Review | `my-interface-review` | `<phase-id> parent_id=<this Log Entry ID>` |

Invoke each through the Skill tool. Each keeps its own work, records, and outcome; Implement never does their work itself.

## Workflow

1. **Log Entry.** Create this execution's State Log Entry when a valid State Config exists (see Execution Log). Its ID is the `parent_id` passed to every coordinated Skill.
2. **Config, once.** Check once whether the required Config records exist and are structurally valid. Only when they are absent or invalid, coordinate `my-interface-configure` (once). If Config is still absent or invalid afterwards, stop before Plan, Develop, or Review.
3. **Phases.** Use the selected phase identifiers, or every Target phase in Target order when none is selected. Take the ordered stable phase identifiers from their current owners (the State Config's phase records, or the Target phase list located through the Interface) without establishing Target Understanding.
4. **Per phase, in order:** coordinate `my-interface-plan`, then `my-interface-develop`, then `my-interface-review`.
   - A blocked Develop does not by itself skip Review: when generated Source is available, Review runs its own passes until its result is satisfied or a Blocker prevents continuation.
   - Unresolved Blockers or Open Questions may make the final outcome blocked, but never prevent an applicable Review.
5. **Aggregate.** Record each coordinated Operation's outcome (with its Log Entry ID) in this Entry's `data`. Determine the unique counts of associated Open Questions and Blockers across this execution and its coordinated executions, counting each distinct item once.
6. **Outcome.** Completed, blocked, or stopped — derived from the coordinated outcomes without overstating any of them.

## Execution Log (mandatory)

- Create exactly one Log Entry in the State Config for this execution: next project-wide sequential zero-padded `id`, the Skill, the event, start time, and an in-progress outcome, following the current State Definition and Schema. The active Phase stays null when coordination spans multiple phases. If the State Config does not yet exist, create the Entry as soon as Configure has produced a valid one.
- When work completes, stops, or is blocked, update that same Entry with outcome, report, `data` (coordinated outcomes and the unique counts of associated Open Questions and Blockers), Open Questions, Blockers, and `duration` when timing is known.
- If no valid State Config exists, report the unrecorded Entry as a Blocker in the output.
- Never copy Task histories, transcripts, secrets, or Target content into the Log.

## Boundaries

- Implement owns coordination only. It never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component, and never takes ownership of another Operation's records or results.
- Never invokes Launch or Reset. Never edits `.interface/`. Never commits or pushes.

## Output

The Skill execution result and status: per-phase outcomes of Configure (if run), Plan, Develop, and Review with their Log Entry IDs; the aggregate counts of associated Open Questions and Blockers; this execution's Log Entry ID.
