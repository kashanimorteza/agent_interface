---
name: my-interface-review
description: Bridge to the Review Operation Component of the Agent Project Interface. Independently judges selected-phase Plans and available implementation against current authorities and records Findings. Use ONLY when the Human invokes /my-interface-review (with zero or more phase selections) after implementation exists, or when the my-interface-implement coordinator requires Review. Never activate on your own.
argument-hint: [phase ...]
---

# Review (Agent Interface Skill)

This Skill is the Claude Code bridge to the **Review** Operation Component. The Component owns the Skill's meaning; this file owns only its invocation and Runtime boundary. It was constructed by Agent Native Sync and is a synchronized Runtime realization, never a second authority.

## Invocation boundary

- **Human:** `/my-interface-review [phase ...]` — zero or more phase selections, after implementation exists. Selection received: `$ARGUMENTS`
- **Coordinator:** only `my-interface-implement`, through Claude Code's own Skill mechanism, when it requires Review.
- **Autonomous activation:** disabled. Do not activate this Skill because a task seems to need it. If it was not invoked by the Human or by `my-interface-implement`, stop and say so.

## Before executing

1. Read the synchronized Runtime Rules in `.claude/rules/interface-skill-policy.md` and `.claude/rules/interface-bootstrap.md`. They are your Agent-side contract.
2. Establish current **Interface Understanding**: read `.interface/interface.md` and the Foundation section files it links.
3. Establish current **Target Understanding** from the Target definitions the Interface locates, under the precedence the Interface declares.
4. Read the owning Component, in this order:
   - Definition: `.interface/implementation/operations/review/review.md` (meaning, mandatory Principles, Operation Contract)
   - Preferences: `.interface/implementation/operations/review/review.yaml` (follow its `policy`, `resolution`, `read_order`, and `content_map`; it defines no generated Review record)
5. Read the latest relevant State History items for Plan, Develop, and prior Review executions before judging.

## Execute

Follow the Review Definition and Preferences exactly. They own responsibility, phase selection semantics, inputs, outputs, authority, verification, and stopping conditions. This file does not restate, narrow, or extend them.

## Authority

- Write only through the Operation the Review Component defines: one State History item containing Review's Findings, assurance data, report, and the execution metadata it owns. Every other Interface path is read-only. Review never repairs what it judges.
- Never read, search, resolve, or use `.interface/agent/` or any Agent Module source. If a required Runtime Rule, Skill, mapping, or capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`. Never invoke it yourself.
- Never invoke another Operation Skill. Supporting Skills may be used within the active role and requested scope.
- Report the outcome with current observable evidence, and expose unfinished work, blockers, and required Human actions before claiming completion.

## Realization

- Realization kind: **Constructed** from the owning Component's Definition and Preferences.
- Claude Code supplies invocation and Runtime mechanics only.
