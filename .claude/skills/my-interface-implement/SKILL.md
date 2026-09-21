---
name: my-interface-implement
description: Bridge to the Implement Operation Component of the Agent Project Interface. The coordinating Skill that runs Configure, then the Plan, Develop, Review cycle across selected phases, invoking the child Operation Skills through the Skill tool. Use ONLY when the Human explicitly invokes /my-interface-implement with zero or more phase selections.
argument-hint: [phase ...]
disable-model-invocation: true
---

# Implement (Agent Interface Skill)

This Skill is the Claude Code bridge to the **Implement** Operation Component and the selected coordinating Skill of this project. The Component owns the Skill's meaning; this file owns only its invocation, coordination boundary, and Runtime boundary. It was constructed by Agent Native Sync and is a synchronized Runtime realization, never a second authority.

## Invocation boundary

- **Human:** `/my-interface-implement [phase ...]` — zero or more phase selections. Selection received: `$ARGUMENTS`
- **Coordinator invocation:** disabled. No other Skill or Agent Instance may invoke this Skill.
- **Autonomous activation:** disabled (Claude Code: `disable-model-invocation: true`). Only the Human starts this Skill.

## Before executing

1. Read the synchronized Runtime Rules in `.claude/rules/interface-skill-policy.md`, `.claude/rules/interface-bootstrap.md`, and `.claude/rules/interface-agent-capabilities.md`. They are your Agent-side contract and the map of the synchronized child Skills.
2. Establish current **Interface Understanding**: read `.interface/interface.md` and the Foundation section files it links.
3. Establish current **Target Understanding** from the Target definitions the Interface locates, under the precedence the Interface declares.
4. Read the owning Component, in this order:
   - Definition: `.interface/implementation/operations/implement/implement.md` (meaning, mandatory Principle, Operation Contract)
   - Preferences: `.interface/implementation/operations/implement/implement.yaml` (follow its `policy`, `resolution`, `read_order`, and `content_map`)

## Coordination

Implement is the only primary Operation that invokes another primary Operation Skill. It may invoke exactly these synchronized Skills, and only through Claude Code's own Skill mechanism (the `Skill` tool):

| Child Skill | Claude Code name |
|---|---|
| Configure | `my-interface-configure` |
| Plan | `my-interface-plan` |
| Develop | `my-interface-develop` |
| Review | `my-interface-review` |
| Launch | `my-interface-launch` |

Delegated invocation grants no ownership: each Operation Component retains ownership of its records and outputs, and each child writes its own operation log. Before coordinating, prove each child Skill is discoverable and invocable in Claude Code; a missing or unusable child is Runtime drift to report, never something to resolve from the Agent Module. Never invoke `my-interface-reset` or `/my-interface-agent-native`.

## Execute

Follow the Implement Definition and Preferences exactly. They own the sequence, gates, stopping conditions, and what Implement records. This file does not restate, narrow, or extend them.

## Authority

- Write only Implement's own status and step-by-step run log through the Operation the Implement Component defines. Every delegated mutation remains owned by the invoked Operation Component.
- Never read, search, resolve, or use `.interface/agent/` or any Agent Module source. If a required Runtime Rule, Skill, mapping, or capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`. Never invoke it yourself.
- Never bypass Human approval, combine operation ownership, or change Target intent.
- Report the outcome with current observable evidence, and expose unfinished work, blockers, and required Human actions before claiming completion.

## Realization

- Realization kind: **Constructed** from the owning Component's Definition and Preferences.
- Claude Code supplies invocation and Runtime mechanics only.
