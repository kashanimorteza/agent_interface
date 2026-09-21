---
name: my-interface-develop
description: Bridge to the Develop Operation Component of the Agent Project Interface. Executes planned Tasks for selected phases and records evidence. Use ONLY when the Human invokes /my-interface-develop (with zero or more phase selections) after a valid current Plan exists, or when the my-interface-implement coordinator requires Development. Never activate on your own.
argument-hint: [phase ...]
---

# Develop (Agent Interface Skill)

This Skill is the Claude Code bridge to the **Develop** Operation Component. The Component owns the Skill's meaning; this file owns only its invocation and Runtime boundary. It was constructed by Agent Native Sync and is a synchronized Runtime realization, never a second authority.

## Invocation boundary

- **Human:** `/my-interface-develop [phase ...]` — zero or more phase selections, after a valid current Plan exists and prerequisites are ready. Selection received: `$ARGUMENTS`
- **Coordinator:** only `my-interface-implement`, through Claude Code's own Skill mechanism, when it requires Development.
- **Autonomous activation:** disabled. Do not activate this Skill because a task seems to need it. If it was not invoked by the Human or by `my-interface-implement`, stop and say so.

## Before executing

1. Read the synchronized Runtime Rules in `.claude/rules/interface-skill-policy.md` and `.claude/rules/interface-bootstrap.md`. They are your Agent-side contract.
2. Establish current **Interface Understanding**: read `.interface/interface.md` and the Foundation section files it links.
3. Establish current **Target Understanding** from the Target definitions the Interface locates, under the precedence the Interface declares.
4. Read the owning Component, in this order:
   - Definition: `.interface/implementation/operations/develop/develop.md` (meaning, mandatory Principle, Operation Contract)
   - Preferences: `.interface/implementation/operations/develop/develop.yaml` (follow its `policy`, `resolution`, `read_order`, and `content_map`)

## Execute

Follow the Develop Definition and Preferences exactly. They own responsibility, phase selection semantics, inputs, outputs, authority, verification, and stopping conditions. This file does not restate, narrow, or extend them.

## Authority

- Write only through the Operation the Develop Component defines: authorized Development results within the resolved Plan and Component boundaries, plus the exact Config records it owns. Every other Interface path is read-only.
- Never read, search, resolve, or use `.interface/agent/` or any Agent Module source. If a required Runtime Rule, Skill, mapping, or capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`. Never invoke it yourself.
- Never invoke another Operation Skill; stop and report when another Operation is required. Supporting Skills may be used within the active role and requested scope.
- Report the outcome with current observable evidence, and expose unfinished work, blockers, and required Human actions before claiming completion.

## Realization

- Realization kind: **Constructed** from the owning Component's Definition and Preferences.
- Claude Code supplies invocation and Runtime mechanics only.
