---
name: my-interface-launch
description: Bridge to the Launch Operation Component of the Agent Project Interface. Activates a completed implementation for one scope (api, presentation, logic, or complete) and records the observable runtime result. Use ONLY when the Human invokes /my-interface-launch, or when a declared coordinator (my-interface-implement) has established the current Launch prerequisites. Never activate on your own.
argument-hint: [api|presentation|logic|complete]
---

# Launch (Agent Interface Skill)

This Skill is the Claude Code bridge to the **Launch** Operation Component. The Component owns the Skill's meaning; this file owns only its invocation and Runtime boundary. It was constructed by Agent Native Sync and is a synchronized Runtime realization, never a second authority.

## Invocation boundary

- **Human:** `/my-interface-launch [scope]` — one optional scope. Scope received: `$ARGUMENTS`
- **Coordinator:** declared coordinators only; in this project that is `my-interface-implement`, through Claude Code's own Skill mechanism, when end-to-end orchestration has established the current Launch prerequisites.
- **Autonomous activation:** disabled. Do not activate this Skill because a task seems to need it. If it was not invoked by the Human or by a declared coordinator, stop and say so.

## Before executing

1. Read the synchronized Runtime Rules in `.claude/rules/interface-skill-policy.md` and `.claude/rules/interface-bootstrap.md`. They are your Agent-side contract.
2. Read the owning Component, in this order:
   - Definition: `.interface/implementation/operations/launch/launch.md` (meaning, mandatory Principle, Operation Contract)
   - Preferences: `.interface/implementation/operations/launch/launch.yaml` (follow its `policy`, `resolution`, `read_order`, and `content_map`)
3. Establish any further Understanding the Launch Definition itself requires, from the sources it names.

## Execute

Follow the Launch Definition and Preferences exactly. They own responsibility, scope semantics, inputs, outputs, authority, readiness verification, and stopping conditions. This file does not restate, narrow, or extend them.

## Authority

- Write only through the Operation the Launch Component defines, into the exact records it owns. Every other Interface path is read-only. Never expose secret values.
- Never read, search, resolve, or use `.interface/agent/` or any Agent Module source. If a required Runtime Rule, Skill, mapping, or capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`. Never invoke it yourself.
- Never invoke another Operation Skill. Supporting Skills may be used within the active role and requested scope.
- Report the outcome with current observable evidence, and expose unfinished work, blockers, and required Human actions before claiming completion.

## Realization

- Realization kind: **Constructed** from the owning Component's Definition and Preferences.
- Claude Code supplies invocation and Runtime mechanics only.
