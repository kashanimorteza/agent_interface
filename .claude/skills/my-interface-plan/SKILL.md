---
name: my-interface-plan
description: Core Interface Skill for planning. Turns each selected (or every active and plannable) Target phase into a bounded Plan of Groups and atomic, verifiable Tasks in the Plan Config, reconciling existing Plans without destroying begun work, and records one State Log Entry. Use when the Human asks to plan a phase or when Implement coordinates Planning.
argument-hint: "[phase-id ...]"
---

<!--
Native realization (Claude Code) of the Core Skill Contract `plan`, synchronized by
/my-interface-agent-native. The Human-owned Agent Module remains authoritative; this Skill is
not a second authority. Its operational meaning is owned by the Plan Operation Component,
which this Skill reads from its current location at run time.
-->

# Plan (`my-interface-plan`)

Stable key: `plan`. Required. Invocable directly by the Human (`/my-interface-plan [phase-id ...]`) or by an Agent.

- **Input:** an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).
- **Output:** the Skill execution result and status.
- **Requirement:** a successful Configure execution must have established the required Config records before this Skill runs.

## Before acting

1. Apply the synchronized project Rules (`.claude/rules/`), especially *Agent Interface Skill policy* and *Agent Interface bootstrap*.
2. Establish Interface Understanding from `.interface/interface.md` and its linked Foundation section files, then Target Understanding from the Target definitions the Interface locates.
3. Through the Interface, locate and read the Plan Operation Component Definition (currently `.interface/implementation/operations/plan/plan.md`) and Preferences (`plan.yaml`), plus the Plan and State Config Schemas. They own this Skill's meaning and every Principle; when they differ from the summary below, they win.

## Prerequisites

- Plan Config and State Config must exist and be structurally valid. If either is missing or invalid, stop and record the unmet prerequisite. **Never** create, repair, initialize, or replace a Config record, and never run Configure.

## What Planning does

- Considers the selected phases, or every active and plannable Target phase when none is selected, **in Target order**. Records the Workflow position `planning` once Config is valid.
- A selected inactive or unplannable phase is recorded as skipped, with its reason, as a Blocker in the State Log. An open Blocker for an earlier applicable phase stops Planning before a later phase begins. Never invent a phase or change a phase's meaning.
- Produces or reconciles each applicable Plan **once** against current Understanding: one Plan per phase → Groups (one coherent work area each) → atomic Tasks (one observable result each).
- Context is written once at the highest level where it holds (Plan → Group → Task) and inherited; a Task never repeats its phase, Group, or a statement present in another Task.
- Each Task carries only its own: activity, reason, inputs, explicit dependencies (other Tasks), Task Skills (every Skill identified as useful), expected result, acceptance and verification stated as observable behaviour, progress fields, and any constraint unique to it.
- Planning content never names a file, folder, path, module, layout, class, function, symbol, or command; never stores project concepts, resolved technical choices, or Component rules; never lists sources to consult.
- Replanning preserves valid work. A Task Develop has not begun may be removed and replaced; a begun or completed Task is never removed or rewritten — create a new Task with `replaces`. Every created or materially changed Task records this invocation's State Log Entry id in `source_id`.
- Records one State Log Entry with the outcome, every addition/change/removal/preservation/replacement and its reason, unresolved conditions, and the Skills actually used.

## Boundaries

- May use any suitable available Skill; **never** invokes another Core Operation (Configure, Develop, Review, Implement).
- Provides Task status, Blocker reference, and Task Log fields but never updates execution progress (Develop owns it).
- Write authority: Plan content in the Plan Config, and Plan's own Workflow position, aggregate planning progress, and Log Entry in State. Every other `.interface/` path is read-only.

## Stop conditions

Required Config or prerequisites unavailable, contradictory coverage, unresolved ownership, or an open required decision. Always report the reason.
