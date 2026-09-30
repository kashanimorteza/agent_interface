---
name: my-interface-plan
description: Core Skill for planning (stable key `plan`). Turns each selected (or every active and plannable) Target phase into a bounded Plan of Groups and atomic Tasks in the Plan Config, with explicit dependencies, acceptance, and verification, and reconciles existing Plans without destroying begun work. Use when a phase needs a Plan or its Plan must be reconciled with current Understanding. Invocable by the Human (/my-interface-plan [phase-id ...]) or by an Agent.
argument-hint: "[phase-id ...]"
---

<!-- Synchronized by Agent Native Sync (/my-interface-agent-native) from the Plan Skill Contract and the Plan Operation Definition and Preferences it names. Change those Human-owned sources and re-run that synchronization; do not edit this copy. -->

# Plan

The Core Skill for planning. Required. Stable key: `plan`. Skill name: `my-interface-plan`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection: zero or more Target phase identifiers (`$ARGUMENTS`). When a coordinating Skill supplies a `parent_id`, record it on this execution's Log Entry.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs. The Plan Config and State Config must exist and be structurally valid; if either is missing or invalid, stop. A missing Config prerequisite never authorizes this Skill to create, repair, initialize, or replace that record, and this Skill never runs Configure.

## Sources

Read these current Operation sources in full before acting. They are the authority for Planning; this Skill never copies their facts and never writes to them.

- `.interface/implementation/operations/plan/plan.md` — Plan Definition and its mandatory Principles.
- `.interface/implementation/operations/plan/plan.yaml` — Plan Preferences (currently no defaults; an empty section is an absence of defaults, not a wildcard).

The generated record follows the Plan Schema; State records follow the State Definition and State Schema. Locate them through `.interface/interface.md`.

## Workflow

1. Apply the project Rules (`interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`). If one is missing, report Runtime drift.
2. Verify the Requirements. Execution Log: create one Log Entry in State for this execution, including its ID and Skill, following the current State Definition and Schema.
3. Establish current Interface Understanding and Target Understanding, then read the Sources above.
4. Resolve the phases: the selected phase identifiers, or every active and plannable Target phase when none is selected, processed in Target order. Skip a selected inactive or unplannable phase. Do not begin a later phase while an earlier applicable phase has an open Blocker.
5. For each applicable phase, produce or reconcile its Plan once against current Understanding, applying every obligation below. Record State's planning position and the phase's aggregate planning progress as the State Definition prescribes.
6. Use any suitable available Skill; never invoke another Core Skill (Configure, Develop, Review, Implement).
7. Update the same Log Entry with the outcome, a concise report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. Record every Task addition, change, removal, preservation, or replacement with its reason in that Entry.

## Planning obligations

- Every planned phase has one Plan holding its identity, order, target, intended outcome, and the phase-wide context (the targeted Component and work-specific constraints not defined by another source). Never invent a phase or silently change an existing phase's meaning.
- Every Task belongs to one Group; a Group holds the coherent work area and the context its Tasks share, never one Task's activity, result, or verification.
- Each Task is one small, concrete activity with one independently observable result; divide large work into as many precise Tasks as necessary.
- Context is recorded exactly once, at the highest level where it holds, and inherited downward. A Task never stores its phase or Group, never repeats or contradicts inherited context, and the same statement never appears in more than one Task of a Plan.
- A Task, read with its Group and Plan, explains what, why, the result, its context, its target and work area, governing authorities and constraints, inputs, dependencies, Task Skills, and how completion is accepted and verified. Record every Skill identified as useful for the Task in Task Skills; that is guidance for Develop, not a limit.
- Planning content is expressed in responsibilities, behaviour, and observable results. It never names a file, folder, path, module, package layout, class, function, symbol, or command, never asserts an artifact's location, and carries no list of sources to consult.
- A Task defines what must be achieved, why, where its responsibility belongs, and what proves completion; it never takes ownership of its implementation or makes a technical decision.
- A Task names every other Task whose completed result it requires; readiness is never guessed from order or proximity.
- Every Task states acceptance and a verification condition as observable behaviour, without naming the command, tool, path, or code that observes it. The applicable testing authority decides whether evidence is persisted or transient; never widen testing scope.
- Plan owns Plans, Groups, and Task planning content and provides the Task status, Blocker reference, and Task Log fields, but never updates execution progress.
- Replanning preserves still-valid work and adds newly required work. A Task Develop has not begun may be removed and replaced. A begun or completed Task is never removed or rewritten: create a new Task whose `replaces` points to it. Every created or materially changed Task records this execution's State Log Entry identifier in `source_id`.
- The record holds work and progress, not project meaning: never store project concepts, resolved technical choices, Component rules, or explanations the sources already hold, and never record a constraint derivable from the project definition, the Principles, or the Preferences.

## Stop conditions

Stop and report the exact reason, recording it on the Log Entry, when required Config records or prerequisites are unavailable, coverage is contradictory, ownership is unresolved, or a required decision remains open.

## Outputs

The Skill execution result and status.
