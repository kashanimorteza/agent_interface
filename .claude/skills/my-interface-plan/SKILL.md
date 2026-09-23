---
name: my-interface-plan
description: Agent Interface Core Skill `plan`. Turns each selected (or every active and plannable) Target phase into a bounded Plan of Groups and atomic, verifiable Tasks in the Plan Config, reconciling existing Plans without destroying begun work. Use when the Human or a coordinating Agent asks to plan or replan one or more phases.
argument-hint: "[phase-id ...]"
---

# Plan (`plan`)

The Core Skill for planning. Required. Stable key: `plan`. Skill name: `my-interface-plan`.

This Skill is a synchronized, self-contained Runtime realization. Its meaning comes from the Plan Operation Definition and Preferences, read fresh on every run; this file never replaces them. Never read or search `.interface/agent/`. If something this Skill needs is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Personality

No Personality is declared. Work under the global Rules and the active Output Style.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-plan [phase-id ...]`) or by an Agent (Skill tool), including a coordinating Skill.
- Inputs: an invocation request and an optional phase selection — zero or more Target phase identifiers in `$ARGUMENTS`. With none, consider every active and plannable Target phase.
- When invoked by a coordinator, the coordinator supplies its reserved Log identifier; record it as this Log Entry's `parent_id`.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs. If the Plan Config or State Config is missing or structurally invalid, stop and record the unmet prerequisite. Never create, repair, initialize, or replace a Config record, and never run Configure yourself.

## Workflow

1. **Execution Log — start.** Create one Log Entry in the State Config (`.interface/config/state.yaml`) for this execution with its `id`, `skill: plan`, and `started_at`. This `id` is the `source_id` of every Task this invocation creates or materially changes.
2. **Establish Understanding.** Read `.interface/interface.md` and the Foundation section files it links, as the global `interface-bootstrap` Rule requires; then establish Target Understanding from the Target definitions the Interface locates, under the precedence it declares. Read the State Config and prior Planning Log Entries as execution records, never as authority.
3. **Read the Plan Operation completely** — `.interface/implementation/operations/plan/plan.md` (Definition and every mandatory Principle) and `.interface/implementation/operations/plan/plan.yaml` (Preferences). Read the Plan Schema `.interface/foundation/schema/plan.yaml` for the record shape. These are authoritative; if they differ from anything in this file, they win.
4. **Validate prerequisites** as stated under Requirements. Once valid, record the active Workflow position as `planning`.
5. **Plan each applicable phase in Target order.** Produce or reconcile its Plan once against current Understanding, following every Plan Principle — one Plan per phase, Groups for shared context, atomic Tasks, context stated once at the highest level, no paths or code in planning content, explicit dependencies, behavioural acceptance and verification, Task Skills recorded, and existing begun or completed work never removed or rewritten (use `replaces`). Stop before a later phase while an earlier applicable phase has an open Blocker. Record a selected inactive or unplannable phase as skipped with its reason as a Blocker.
6. **Update aggregate planning progress** for each phase in State, without duplicating Task status or Task logs.
7. **Use any suitable available Skill** for the work, but never invoke another Core Operation.
8. **Execution Log — completion.** Update the same Log Entry with `completed_at`, `duration_ms`, `outcome`, a concise `report`, the Skills actually used, every Task addition, change, removal, preservation, or replacement with its reason, and any applicable `data`, Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Stop conditions

Stop when required Config records or prerequisites are unavailable, coverage is contradictory, ownership is unresolved, or a required decision remains open — and record why.

## Boundaries

- Write only the Plan Config's planning content and this execution's State records (Workflow position, aggregate planning progress, own Log Entry) inside `.interface/config/`. Every other `.interface/` path is read-only.
- Never update Task execution progress (that belongs to Develop), never invent or redefine a phase, and never copy project meaning or technical choices into the Plan.
- Never read `.interface/agent/` and never invoke `/my-interface-agent-native`.

## Outputs

The Skill execution result and status: phases planned, reconciled, skipped, or blocked; Task counts; the Log Entry `id`; and any Open Questions or Blockers.
