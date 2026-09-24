---
name: my-interface-plan
description: Core Interface Skill "plan" — turns selected (or every active and plannable) Target phases into bounded Plans of Groups and atomic, verifiable Tasks in the Plan Config, reconciling existing work and recording one State Log Entry. Use when phases need planning or replanning after Target, Interface, Principle, or Preference changes.
argument-hint: "[phase-id ...]"
---

<!-- Synchronized by /my-interface-agent-native from the Plan Skill Contract and its Sources. Do not edit here; this Skill is a Runtime realization, never an authority. -->

# Plan

The Core Skill for planning. Stable key: `plan`. Required. No Personality is declared.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-plan [phase-id ...]`) or by an Agent (for example the Implement coordinator).
- Inputs: an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers). When a coordinator supplies a parent Log identifier, record it as `parent_id`.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs. Planning starts only when the Plan Config and State Config exist and are structurally valid. If either is missing or invalid, stop and record the unmet prerequisite; never create, repair, initialize, or replace a Config record, and never run Configure.

## Before acting

1. Apply the project Rules `interface-bootstrap`, `interface-skill-policy`, and `git-discipline` (`.claude/rules/`). Never read `.interface/agent/`.
2. Read the current Operation authorities in full — they govern over this summary if they differ:
   - `.interface/implementation/operations/plan/plan.md` (Definition and mandatory Principles)
   - `.interface/implementation/operations/plan/plan.yaml` (Preferences; currently no defaults — an empty section is an absence of defaults, not a wildcard)
   - the Plan Schema the Plan Config follows (`.interface/foundation/schema/plan.yaml`)
3. Establish current Interface Understanding and Target Understanding from `.interface/interface.md` and the sources it locates.
4. Read State only as an execution record: prior Planning Log Entries, Blockers, Open Questions, and aggregate phase progress — never duplicating Task records and never as authority.

## Workflow

1. Resolve phases: the selected Target phase identifiers, or every active and plannable Target phase when none is selected. Process them in Target order.
2. Once required Config is valid, record the active Workflow position as `planning` in State.
3. For each applicable phase, in order:
   - A selected inactive or unplannable phase is recorded as skipped, with its reason as a Blocker in the State Log.
   - An open Blocker for an earlier applicable phase stops Planning before a later phase begins.
   - Produce or reconcile the phase's Plan once against current Understanding (never treat a previous Plan as current without comparing it).
4. Record the outcome, unresolved conditions, every addition/change/removal/preservation/replacement with its reason, and the Skills actually used in this invocation's single State Log Entry. Update aggregate phase `planning` progress in State.

Planning may use any suitable available Skill but never invokes another Core Operation (Configure, Develop, Review, Implement). Stop when required Config or prerequisites are unavailable, coverage is contradictory, ownership is unresolved, or a required decision remains open.

## Principles (all mandatory)

- **Every phase has its own Plan.** A Plan preserves the phase's identity, order, target, and intended outcome, holds phase-wide context (targeted Component, work-specific constraints not defined elsewhere), and decomposes the outcome into Groups and Tasks. Never invent a phase or silently change an existing phase's meaning. Language and technology choices are resolved from their owning sources, never copied into the Plan.
- **Groups organize related work.** Every Task belongs to one Group; a Group explains its coherent implementation area, what it accomplishes, and where within the target Component it belongs. A Group never absorbs one Task's activity, result, or verification.
- **A Task is one atomic action** with one independently observable result. Divide large work into as many precise Tasks as needed; never combine unrelated changes or hide several outcomes behind one title.
- **Context is written once and inherited.** Store each piece of context exactly once at the highest level where it holds (Plan → Group → Task). A Task never stores its phase or Group, never repeats or contradicts inherited context, and the same statement never appears in more than one Task of a Plan — move it to the common Group or Plan.
- **Every Task is understandable in its context.** Read with its Group and Plan, a Task explains what, why, the result, its phase/Group, target Component and area, governing authorities and constraints, inputs, dependencies, Task Skills, and how completion is accepted and verified. The Task carries only its own content. Record every Skill identified as useful in Task Skills (guidance for Develop, not a limit, and distinct from `source_id`).
- **A Task is independent of the implementation structure.** Planning content uses responsibilities, behaviour, and observable results; it never names a file, folder, path, module, package layout, class, function, symbol, or command, never asserts an artifact's location, and carries no list of sources to consult. Task logs (execution history) may record actual checks, locations, and outcomes, without secrets.
- **Task defines the activity; Development defines the implementation.** A Task states what, why, where the responsibility belongs, and what proves completion; it never makes a technical decision.
- **Dependencies are explicit.** A Task names every Task whose completed result it requires; readiness is never guessed from file order or proximity.
- **Completion must be demonstrable.** Every Task has acceptance and verification stated as observable behaviour, naming no command, tool, path, or code. The concrete check is built and run at implementation time and logged; the applicable testing authority decides whether evidence is persisted or transient — never widen the testing scope.
- **Task progress and Workflow State remain separate.** Plan owns Plans, Groups, and Task planning content and provides the status, blocker, and log fields, but never updates execution progress (Develop does). State owns the Workflow position, aggregate phase progress, Blockers, and Open Questions; never duplicate them in Tasks.
- **Existing work is never silently destroyed.** Preserve still-valid work and add newly required work. A Task Develop has not begun may be removed and replaced; a begun or completed Task is never removed or rewritten — create a new Task with `replaces` pointing to it. Every created or materially changed Task records this invocation's State Log Entry id in `source_id`.
- **The record holds work and progress, not project meaning.** Never store project concepts, resolved technical choices, Component rules, or explanations the authorities already hold; record a constraint only when specific to the work and derivable from no other source. Keep `task_count` values correct at every level.

## Execution Log

At the start of every execution, create one Log Entry in State with its `id` (next project-wide sequential identifier, zero-padded to at least three digits), `skill: plan`, and `started_at`. At completion, update that same entry with `completed_at`, `duration_ms`, `outcome`, `report`, `skills_used`, and any applicable `data`, `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Boundaries

Write only Plan Config planning content and this Skill's State records (Workflow position, aggregate planning progress, its Log Entry). Never modify any `.interface/` path outside `.interface/config/`.

## Output

The Skill execution result and status: phases planned, reconciled, or skipped; Task changes with reasons; Blockers and Open Questions; and the Log Entry id.
