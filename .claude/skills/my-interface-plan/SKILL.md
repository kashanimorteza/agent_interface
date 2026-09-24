---
name: my-interface-plan
description: Core Skill for planning. Turns each selected (or every active and plannable) Target phase into a bounded Plan of Groups and atomic, verifiable Tasks, reconciling existing Plans without destroying begun or completed work. Use when phase work must be planned or replanned.
argument-hint: "[phase-id ...]"
---

# Plan (Core Skill)

The Core Skill for planning. Required. Stable key: `plan`. Skill name: `my-interface-plan`.

This Skill is the Claude Code realization of the Plan Operation. The current Plan Operation Definition and Preferences, located through the Interface, remain the authority for Plan's meaning; this Skill restates them so it can run. If they disagree with this Skill, follow the current owning source and report Runtime drift so the Human can run Agent Native Sync. Plan Preferences, when present, cannot add technical or project meaning; they currently declare no defaults (an empty section is an absence of defaults, not a wildcard).

## Personality

No Personality is declared.

## Invocation and inputs

- May be invoked directly by a Human (`/my-interface-plan [phase-id ...]`) or by an Agent (for example, coordinated by `my-interface-implement`).
- Inputs: an invocation request and an optional phase selection (one or more Target phase identifiers). When coordinated by Implement, the request carries the coordinator's Log Entry ID as `parent_id`; record it on this execution's Log Entry.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Planning starts only when the Plan Config and State Config exist and are structurally valid. If either is missing or invalid, stop. A missing Config prerequisite never authorizes Plan to create, repair, initialize, or replace that record.

## Terms

- **Plan** — the work required by one project phase, holding the context that applies to the whole phase and decomposing its outcome into Groups.
- **Group** — one coherent implementation area within a Plan, holding the context its Tasks share.
- **Task** — one small, concrete activity with one independently observable result.
- **Phase** — the project stage a Plan represents, identified by its stable identifier and carrying its order and target.
- **Plannable Phase** — an active Target phase whose Target-defined prerequisites permit Planning to begin.
- **Dependency** — another Task whose completed result this Task requires before it can begin.
- **Acceptance** — the observable criterion that determines whether a Task's result is correct.
- **Verification** — the condition that must be observed to prove acceptance, stated as behaviour rather than as a command.
- **Task Skills** — the Skills Planning identifies as useful for completing one Task, distinct from that Task's Source ID.
- **Status** — the current progress value of a Task, updated by Develop and distinct from the aggregate Workflow State.
- **State Log** — State's ordered record of an Operation execution and its result.
- **Task Log** — the append-only history of progress, evidence, and verified transitions for one Task, distinct from the State Log.
- **Task Source ID** — the State Log Entry identifier of the Planning invocation that last created or materially changed a Task.

## Procedure

1. Apply the project Rules loaded as project memory (Interface bootstrap, Interface Skill policy, Git discipline).
2. **Execution Log — start.** Create one Log Entry in State for this execution, with its ID, Skill (`my-interface-plan`), `started_at`, and `parent_id` when supplied.
3. Verify the Plan Config and State Config exist and are structurally valid against their Schemas; otherwise stop (see Requirements).
4. Establish current Interface Understanding and Target Understanding from their current sources.
5. Select phases: the given Target phase identifiers, or every active and plannable Target phase when none is selected, processed in Target order. Skip a selected inactive or unplannable phase. Do not proceed to a later phase until Planning of every earlier applicable phase has concluded without an open Blocker.
6. For each applicable phase, produce or reconcile its Plan once against the current Understanding (never treat a previous Plan as current without comparing it to current Understanding), following every Principle below. The generated record follows the Plan Schema.
7. Read State Log Entries (prior Planning results, Blockers, Open Questions, aggregate phase progress) as execution records only, never duplicating Task records.
8. Use any suitable available Skill; never invoke another Core Operation (Configure, Develop, Review, Implement).
9. **Stop** when required Config records or prerequisites are unavailable, coverage is contradictory, ownership is unresolved, or a required decision remains open. Report the exact reason and record Blockers or Open Questions in this execution's Log Entry.
10. **Execution Log — completion.** Update the same Log Entry with `completed_at`, `duration_ms`, readable `duration`, outcome, report, and any applicable data, Open Questions, or Blockers — including every Task addition, change, removal, preservation, or replacement with its reason. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Principles (all mandatory)

### Every phase has its own Plan
- A Plan represents the work required by one applicable phase. It preserves the phase's identity, order, target, and intended outcome, then decomposes that outcome into Groups and Tasks.
- The Plan holds the planning context shared by the whole phase: the Component it targets and work-specific constraints that apply throughout and are not already defined by another source. Language and technology choices are resolved from their owning sources and are not copied into the Plan.
- Never invent a new phase or silently change the meaning of an existing one. The phase remains the unit selected for planning and development.

### Groups organize related work
- Every Task belongs to one Group. A Group collects Tasks contributing to one coherent implementation area and explains what that area is, what it accomplishes, and where within the phase's target Component its work belongs.
- A Group holds the work area and work-specific constraints shared by its Tasks that apply neither to the whole phase nor through another source. Technology choices remain in their owning sources.
- A Group never absorbs the activity, expected result, or verification that belong to one Task.

### A Task is one atomic action
- Each Task is one small, concrete activity with one independently observable result. Divide large work into as many precise Tasks as necessary; clarity and executability take precedence over minimizing the number of Tasks.
- A Task never combines unrelated changes or hides several broad outcomes behind one title.

### Context is written once and inherited
- Plan → Groups → Tasks is one nested structure, and the nesting is the Task's context. A Task's phase and Group are never repeated inside the Task (the Task identifier carries the Plan and Group identifiers).
- Each piece of context the record holds (targeted Component, work area, work-specific constraint) is recorded exactly once, at the highest level where it holds. Lower levels inherit it.
- A Task or Group may add to inherited context or make it stricter; it never repeats or contradicts it. The same statement never appears in more than one Task of a Plan — move it to the common Group or Plan.

### Planning establishes current understanding and reconciles existing work
- Every invocation establishes current Interface and Target Understanding, then produces or reconciles the existing Plan once. Plan reads State as an execution record and never performs another Core Operation's responsibility.

### Every Task is understandable in its context
- Read with its Group and Plan, a Task explains: what must be done; why; what result it must produce; which phase and Group provide its planning context; which Component and work area it targets; which authorities and constraints govern it; which inputs, dependencies, constraints, and Task Skills matter; and how completion is accepted and verified.
- The Task itself carries only what is its own: activity, reason, inputs and dependencies, Task Skills, expected result, acceptance and verification, progress, and any constraint that applies to it alone.
- Record every Skill identified as useful for completing the Task in Task Skills. That list guides Develop but does not limit it, and it is not a record of the Skill that created or changed the Task.
- A Task never repeats the identity or general description of the project, its phase, or its Group.

### A Task is independent of the implementation structure
- Planning content is expressed in responsibilities, behaviour, and observable results. It never names a file, folder, path, module, package layout, class, function, symbol, or command, never asserts that an artifact exists at a location, and carries no list of sources to consult. The target and work area identify a Component and a responsibility, not a directory.
- Execution history is distinct: a Task's log records the concrete check actually performed, relevant locations, and the observed outcome, with secret values excluded, and never prescribes future implementation.

### Task defines the activity and Development defines the implementation
- A Task states what must be achieved, why, where its responsibility belongs, and what evidence demonstrates completion. It never takes ownership of its implementation or makes a new technical decision.

### Dependencies are explicit
- A Task names every other Task whose completed result it requires. Readiness is derived from dependencies, never guessed from file order or proximity. Unrelated Tasks remain independently executable.

### Completion must be demonstrable
- Every Task states an acceptance criterion and a verification condition, both as observable behaviour, in terms of the interfaces and behaviour the result publishes — never naming the command, tool, path, or code that observes it, and never doubling as a hidden implementation procedure.
- The concrete executable check is constructed and run at implementation time and recorded with its outcome in the Task's log; a Task is complete only when that check has passed.
- The applicable testing authority decides whether evidence is persisted or transient; Plan never widens the declared testing scope merely to demonstrate a Task.

### Task progress and Workflow State remain separate
- Plan owns Plans, Groups, and Task planning content. It provides the Task status, Blocker reference, and Task Log fields but does not update execution progress. Develop claims eligible work, records progress transitions, and preserves the append-only Task Log.
- Blocker resolution (performed by Develop) requires verified evidence; a missing Blocker record alone is not evidence of resolution, and resolution never marks work complete.
- State owns the active Workflow position, aggregate phase progress, and the Log Entries containing Blockers and Open Questions. A Task never duplicates those.

### Existing work is never silently destroyed
- When current Understanding requires replanning, preserve still-valid work and add newly required work.
- A Task that Develop has not begun may be removed and replaced. A Task that Develop has begun or completed is never removed or rewritten: create a new Task with `replaces` pointing to it (Develop later marks the earlier Task `replaced`).
- Every created or materially changed Task records this Planning invocation's State Log Entry identifier in `source_id`.
- Record every addition, change, removal, preservation, or replacement with its reason in this invocation's State Log Entry. Never silently overwrite meaningful Task content.

### The record holds work and progress, not project meaning
- Plans, Groups, and Tasks record which work exists, what each activity must produce, what it depends on, where it stands, and what has happened to it.
- Planning content never stores project concepts, resolved technical choices, Component rules, or explanations the project definition, Principles, and Preferences already state. A constraint is recorded only when it is specific to the work and derivable from no other source. Execution history may name concrete technologies and locations as evidence but never becomes the authority for choosing them.

## Outputs

The Skill execution result and status.
