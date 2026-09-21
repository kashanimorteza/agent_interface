---
name: my-interface-reset
description: Bridge to the Reset Operation Component of the Agent Project Interface. Reconciles operational records and outputs for exactly one authorized reset scope (explicit phases, all phases with generated work, config, or complete) after a preview and explicit Human confirmation. Use ONLY when the Human explicitly invokes /my-interface-reset with one scope.
argument-hint: <phase ...|config|complete>
disable-model-invocation: true
---

# Reset (Agent Interface Skill)

This Skill is the Claude Code bridge to the **Reset** Operation Component. The Component owns the Skill's meaning; this file owns only its invocation and Runtime boundary. It was constructed by Agent Native Sync and is a synchronized Runtime realization, never a second authority.

## Invocation boundary

- **Human:** `/my-interface-reset <scope>` — exactly one reset scope. Scope received: `$ARGUMENTS`
- **Coordinator invocation:** disabled. No other Skill or Agent Instance may invoke this Skill.
- **Autonomous activation:** disabled (Claude Code: `disable-model-invocation: true`). Only the Human starts this Skill.

## Before executing

1. Read the synchronized Runtime Rules in `.claude/rules/interface-skill-policy.md` and `.claude/rules/interface-bootstrap.md`. They are your Agent-side contract.
2. Read the owning Component, in this order:
   - Definition: `.interface/implementation/operations/reset/reset.md` (meaning, mandatory Principle, Operation Contract)
   - Preferences: `.interface/implementation/operations/reset/reset.yaml` (follow its `policy`, `resolution`, `read_order`, and `content_map`)
3. Establish any further Understanding the Reset Definition itself requires, from the sources it names.

## Execute

Follow the Reset Definition and Preferences exactly. They own scope semantics, the mandatory preview, the explicit Human confirmation, protected content, and stopping conditions. This file does not restate, narrow, or extend them. A Reset never runs without the Human's explicit confirmation of the exact previewed targets.

## Authority

- Write only through the Operation the Reset Component defines, on the exact confirmed targets inside its authorized scope. Interface and Target sources, protected content, and unselected phases are preserved. Every other Interface path is read-only.
- Never read, search, resolve, or use `.interface/agent/` or any Agent Module source. If a required Runtime Rule, Skill, mapping, or capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`. Never invoke it yourself.
- Never invoke another workflow Operation Skill. Supporting Skills may be used within the active role and requested scope.
- Report what was removed and what was retained with current observable evidence, and expose unfinished work, blockers, and required Human actions before claiming completion.

## Realization

- Realization kind: **Constructed** from the owning Component's Definition and Preferences.
- Claude Code supplies invocation and Runtime mechanics only.
