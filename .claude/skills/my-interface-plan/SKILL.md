---
name: my-interface-plan
description: Core Skill `plan` — turns one or more Target phases into a Plan of Groups and atomic, verifiable Tasks, or reconciles the existing Plan with current Understanding. Use to plan or replan phases. Optional phase identifiers; with none, plans every active and plannable phase in Target order.
argument-hint: "[phase-id ...] [parent_id=<id>]"
---

# Plan — Core Skill `plan`

Required Core Skill. Stable key: `plan`. Skill name: `my-interface-plan`.

Synchronized Native realization. The governing authority is the current Plan Operation Definition and Preferences in the Implementation Module; this Skill realizes their meaning and never overrides them.

## Invocation and inputs

- May be invoked directly by the Human or by an Agent (including a coordinating Core Skill).
- Inputs: an invocation request and an optional phase selection — one or more Target phase identifiers. When a coordinating Core Skill invokes it, the request carries `parent_id=<that Skill's Log Entry ID>`.

## Start

1. Apply the loaded Runtime Rules first: `interface-skill-policy`, `interface-bootstrap`, `agent-conduct`, `git-discipline`.
2. Locate through `.interface/interface.md` (Implementation Module → Operations → Plan) and read in full the current Plan Definition and Plan Preferences (last synchronized at `.interface/implementation/operations/plan/plan.md` and `plan.yaml`), plus the Plan Schema and the State Definition and Schema needed to write records. If they contradict this Skill, follow them and report Runtime drift so the Human can run `/my-interface-agent-native`.
3. Never read, search, or use `.interface/agent/`.

## Workflow

1. **Config prerequisite.** Start only when the Plan Config and State Config exist and are structurally valid. Otherwise stop. Never create, repair, initialize, or replace a Config record, and never run Configure.
2. **Log Entry.** Create this execution's State Log Entry (see Execution Log). Its ID is this invocation's `source_id`.
3. **Understanding.** Establish current Interface Understanding and Target Understanding. Read State as an execution record (prior Planning results, Blockers, Open Questions, aggregate phase progress), never as authority.
4. **Phase selection.** Use the selected phase identifiers, or every active and plannable Target phase when none is selected; process them in Target order. Skip a selected inactive or unplannable phase. If an earlier applicable phase has an open Blocker, stop before a later phase begins. Never invent a phase or silently change an existing phase's meaning.
5. **Produce or reconcile once per phase.** Compare the existing Plan with current Understanding and produce or reconcile it once. A previous Plan is never current without that comparison.
6. **Plan.** One Plan per phase, preserving the phase's identity, order, target, and intended outcome, plus phase-wide context: the targeted Component and work-specific constraints that hold throughout and are defined by no other source.
7. **Groups.** Every Task belongs to exactly one Group. A Group is one coherent implementation area: what it is, what it accomplishes, and where within the phase's target Component its work belongs, plus constraints its Tasks share. A Group never absorbs one Task's activity, result, or acceptance.
8. **Tasks.** Each Task is one small, concrete, atomic activity with one independently observable result; divide large work into as many precise Tasks as needed. Never combine unrelated changes or hide several outcomes behind one title. A Task carries only what is its own: activity, reason, inputs, dependencies (every other Task whose completed result it requires), Task Skills (every Skill identified as useful — guidance, not a limit), expected result, acceptance, progress fields (status, Blocker reference, Task Log), and any constraint specific to it alone.
9. **Context written once.** Record every piece of context exactly once, at the highest level where it holds (Plan → Group → Task). A Task never stores its phase or Group, never repeats or contradicts inherited context, and the same statement never appears in more than one Task of a Plan — move it to the common Group or Plan.
10. **Independent of implementation structure.** Planning content speaks in responsibilities, behaviour, and observable results. It never names a file, folder, path, module, package layout, class, function, symbol, or command, never asserts that an artifact exists at a location, and carries no list of sources to consult.
11. **Acceptance.** Every Task states acceptance as observable behaviour of the interfaces and behaviour the result publishes, never naming the command, tool, path, or code that would observe it, and never doubling as a procedure or a check. Plan checks nothing; Review establishes acceptance.
12. **Record holds work and progress, not meaning.** Do not store project concepts, resolved technical choices, Component rules, or explanations the sources already hold. Record a constraint only when it is specific to the work and derivable from no other source. Language and technology choices stay in their owning sources.
13. **Replanning never silently destroys work.** Preserve still-valid work and add newly required work. A Task Develop has not begun may be removed and replaced. A begun or completed Task is never removed or rewritten: create a new Task with `replaces` pointing to it (Develop marks the earlier Task `replaced`; Plan never changes its status). Set `source_id` to this invocation's Log Entry ID on every created or materially changed Task. Record every addition, change, removal, preservation, and replacement with its reason in this Log Entry's `data`.
14. **Progress separation.** Plan provides Task status, Blocker reference, and Task Log fields but never updates execution progress. Update only the aggregate Planning progress and Active State as the State Definition assigns to planning.
15. **Stop** when required Config records or prerequisites are unavailable, coverage is contradictory, or ownership is unresolved; report the exact reason.

May use any other suitable available Skill. Never invokes another Core Operation (no other `my-interface-*` Core Skill).

## Execution Log (mandatory)

- At start (after the Config prerequisite holds), create exactly one Log Entry in the State Config: next project-wide sequential zero-padded `id`, the Skill, `parent_id` when supplied, the Phase when phase-specific, the event, start time, and an in-progress outcome, following the current State Definition and Schema.
- When work completes, stops, or is blocked, update that same Entry with outcome, report, `data` (including the per-Task change record above), Open Questions, Blockers, and `duration` when timing is known.
- If the State Config is missing or invalid, do not create or repair it; report the stop and the unrecorded Entry as a Blocker in the output.
- Never copy Task histories, transcripts, secrets, or Target content into the Log.

## Boundaries

- Writes only Plan content in the Plan Config and its own State records. Never edits `.interface/`, Target, Development output, or another Operation's records.
- Never commits or pushes.

## Output

The Skill execution result and status: phases planned, skipped, or stopped; Task additions, changes, removals, preservations, and replacements; the Log Entry ID; and any Blockers and Open Questions.
