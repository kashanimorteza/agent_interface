---
name: my-interface-plan
description: Core Interface Skill "Plan" (stable key `plan`). Turns each selected (or every active and plannable) Target phase into a bounded Plan of Groups and atomic, verifiable Tasks in the Plan Config, reconciling existing Plans against current Interface and Target Understanding, and records one State Log Entry. Use when a phase needs planning or replanning. Optional argument - one or more Target phase identifiers.
argument-hint: "[phase-id ...]"
---

# Plan

The Core Skill for planning. Required. Stable key: `plan`. Skill name: `my-interface-plan`.

This Skill is a synchronized Runtime realization. It never reads, searches, or resolves the Agent Module; a missing or unusable Runtime capability is reported as Runtime drift and the Human is asked to run Agent Native Sync.

## Contract

- **Inputs:** an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).
- **Invocation:** may be invoked directly by a Human (`/my-interface-plan`) or by an Agent (Skill tool).
- **Requirements:** a successful Configure execution must have established the required Config records before this Skill runs.
- **Outputs:** the Skill execution result and status.

## Start of workflow

1. Apply the Runtime Rules `interface-bootstrap` and `interface-skill-policy` (`.claude/rules/`) before anything else.
2. Establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, then Target Understanding from both Target definitions the Interface locates, under the precedence it declares.
3. Locate through the Interface, then read completely, the current **Plan Operation Component** Definition and Preferences (currently `.interface/implementation/operations/plan/plan.md` and `plan.yaml`), plus the Plan and State Schemas. They are the authority; this file only summarizes them, and on any difference the current sources win.

## Procedure

1. **Prerequisites.** Plan Config and State Config must exist and be structurally valid. If either is missing or invalid, stop and record the unmet prerequisite. Never create, repair, initialize, or replace a Config record, and never run Configure.
2. Record the active Workflow position as `planning`.
3. **Phases.** Use the selected phase identifiers, or every active and plannable Target phase when none is selected, in Target order. A selected inactive or unplannable phase is recorded as skipped, with its reason, as a Blocker in the State Log. An open Blocker for an earlier applicable phase stops Planning before a later phase begins.
4. **Produce or reconcile once** each applicable Plan against current Understanding (never treat a previous Plan as current without comparing).
5. Record one State Log Entry: outcome, every addition / change / removal / preservation / replacement with its reason, unresolved conditions, and the Skills actually used.

## Plan content rules

- **One Plan per phase**, preserving the phase's identity, order, target, and intended outcome; never invent a phase or silently change one's meaning.
- **Plan → Groups → Tasks.** Every Task belongs to one Group; a Group holds one coherent work area and the context its Tasks share, never a single Task's activity, result, or verification.
- **Atomic Tasks:** one small, concrete activity with one independently observable result; never combine unrelated changes.
- **Context once, inherited:** record each piece of context exactly once, at the highest level where it holds. A Task never stores its phase or Group, never repeats or contradicts inherited context; the same statement never appears in more than one Task of a Plan.
- A Task carries only its own: activity, reason, inputs, dependencies, **Task Skills** (every Skill useful for completing it — guidance, not a limit), expected result, acceptance, verification, progress fields, and constraints unique to it.
- **Implementation-independent:** planning content uses responsibilities, behaviour, and observable results. It never names a file, folder, path, module, package layout, class, function, symbol, or command, never asserts an artifact's location, and carries no list of sources to consult.
- **Explicit dependencies:** name every Task whose completed result is required; readiness is never guessed from order or proximity.
- **Demonstrable completion:** every Task states acceptance and verification as observable behaviour, never naming the command, tool, path, or code that observes it. The testing authority decides persisted vs. transient evidence; Plan never widens testing scope.
- **Record holds work and progress, not project meaning:** no project concepts, resolved technical choices, Component rules, or anything derivable from the project definition, Principles, or Preferences.
- **Progress stays with Develop:** Plan provides status, Blocker reference, and Task Log fields but never updates execution progress. Active Workflow position, aggregate progress, Blockers, and Open Questions belong to State.
- **Never silently destroy work:** preserve still-valid work. A Task not yet begun may be removed and replaced; a begun or completed Task is never removed or rewritten — create a new Task with `replaces` pointing to it. Every created or materially changed Task records this invocation's State Log Entry identifier in `source_id`.

## Stop when

Required Config or prerequisites are unavailable, coverage is contradictory, ownership is unresolved, or a required decision remains open. Always report the reason.

## Never

Invoke another Core Operation (Configure, Develop, Review, Implement). Any other suitable available Skill may be used.
