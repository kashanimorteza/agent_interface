---
name: my-interface-plan
description: Agent Interface Core Skill `plan`. Turns selected (or every active and plannable) Target phases into bounded Plans of Groups and atomic, verifiable Tasks in .interface/config/plan.yaml, records the `planning` Workflow position, and logs its execution in State. Use when the Human or an Agent asks to plan one or more phases.
argument-hint: "[phase-id ...]"
---

# Plan — Core Skill `plan`

Synchronized Claude Code realization of the Agent Interface Core Skill with stable key `plan` (required). It was produced by Agent Native Sync and is self-contained: it is not an authority, and it never needs the Agent Module. The Operation's authoritative meaning lives in the Implementation sources named under **Authorities** and is read at run time.

## Personality

No Personality is declared. Use the project's standing conduct Rules.

## Invocation and inputs

- Invoked directly by the Human (`/my-interface-plan [phase-id ...]`) or by an Agent (for example `my-interface-implement` through the Skill tool).
- Inputs: the invocation request and an optional phase selection. Selected phases: `$ARGUMENTS` (empty means every active and plannable Target phase, in Target order).
- Output: the Skill execution result and status.

## Standing rules

Apply the project Rules in `.claude/rules/` (interface-bootstrap, interface-skill-policy, git-discipline, interface-agent-capabilities).

## Requirements

A successful Configure execution must already have established the required Config records. Planning starts only when the Plan Config and State Config exist and are structurally valid. If either is missing or invalid, stop and record the unmet prerequisite; never create, repair, initialize, or replace a Config record (that is Configure's work).

## Authorities (read at run time, before acting)

1. Interface Understanding: `.interface/interface.md` and the Foundation section files it links.
2. Target Understanding: both Target definitions the Interface locates, under the precedence it declares.
3. `.interface/implementation/operations/plan/plan.md` — Plan Definition and its mandatory Principles.
4. `.interface/implementation/operations/plan/plan.yaml` — Plan Preferences.
5. The Plan Config Schema and State Config Schema the Interface locates, for record shapes.
6. Current `.interface/config/state.yaml` and `.interface/config/plan.yaml` as execution records (never as authority).

If these sources disagree with this summary, the sources win.

## Procedure (summary of the Plan Definition)

1. Verify the Config prerequisite; create this execution's Log Entry; record the active Workflow position as `planning`.
2. Establish current Interface and Target Understanding.
3. Process applicable phases in Target order. A selected inactive or unplannable phase is recorded as skipped with its reason as a Blocker. An open Blocker on an earlier applicable phase stops Planning before a later phase.
4. For each phase, produce or reconcile its one Plan once against current Understanding: Plan → Groups → atomic Tasks. State context once at the highest level where it holds and let lower levels inherit it; never repeat the same statement in several Tasks.
5. Every Task: one atomic activity with one observable result; explicit `depends_on`; acceptance and verification as observable behaviour; Task Skills listing every Skill identified as useful; `source_id` = this Planning Log Entry id for created or materially changed Tasks.
6. Planning content never names files, folders, paths, modules, classes, functions, symbols, or commands, never lists sources to consult, and never stores project meaning or technical choices.
7. Replanning preserves valid work. Unstarted Tasks may be replaced; begun or completed Tasks are never removed or rewritten — create a new Task with `replaces`. Record every addition, change, removal, preservation, or replacement with its reason in the Log Entry.
8. Maintain `task_count` values. Do not update Task execution progress (Develop owns it).

## Stop conditions

Stop when required Config records or prerequisites are unavailable, coverage is contradictory, ownership is unresolved, or a required decision remains open. Record the reason.

## Execution log

At the start of every execution, create one Log Entry in State for that execution, including its `id`, `skill` (`my-interface-plan`), and `started_at`. At completion, update that same Log Entry with `completed_at`, `duration_ms`, `outcome`, `report`, `skills_used`, and any applicable `data`, `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason. When invoked by Implement, record the supplied Implement Log identifier as `parent_id`.

## Boundaries

- Writes Plans, Groups, and Tasks under Plan rules, and Planning progress, the `planning` position, and its Log Entry under State rules — all inside `.interface/config/`.
- May use any suitable available Skill; never invokes another Core Operation (Configure, Develop, Review, Implement).
- Never invents a phase or silently changes an existing phase's meaning.
