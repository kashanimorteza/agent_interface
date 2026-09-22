---
name: my-interface-configure
description: Configure Operation of the Agent Project Interface — creates and reconciles the structural Config records from their Schemas. Use only when the Human explicitly runs /my-interface-configure or when the my-interface-implement coordinator invokes it; never activate autonomously.
argument-hint: (no arguments)
---

# my-interface-configure

Agent-side bridge to the **Configure** Operation Component. This Skill is a synchronized Claude Code realization; the owning Operation Component is the sole authority for what Configure does.

## Invocation boundary

- **Human:** enabled — the Human runs `/my-interface-configure`.
- **Coordinator:** enabled only for `my-interface-implement`.
- **Autonomous:** disabled. Do not activate this Skill on your own initiative, from another Skill, or from any coordinator other than `my-interface-implement`. If none of the allowed invokers started it, stop and report.
- **Primary Operation:** yes. This Skill never invokes another primary Operation Skill (`my-interface-plan`, `my-interface-develop`, `my-interface-review`, `my-interface-implement`).
- **Required:** yes.

## Source of meaning

Read these in full before execution; they own Configure's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions:

- Definition: `.interface/implementation/operations/configure/configure.md`
- Preferences: `.interface/implementation/operations/configure/configure.yaml`

Do not restate, redefine, or replace their workflow here or in your own reasoning.

## Bridge

- **Purpose:** Bridge the Agent Skill to the Configure Operation Component.
- **Inputs:** Use the inputs declared by the Configure Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Configure Component Definition and Preferences.
- **Responsibility:** Read and execute the Configure Component without redefining its meaning or workflow.
- **Trigger:** Activate when invoked by the Human or `my-interface-implement`.
- **Required Understanding:** Read the Configure Component Definition and Preferences and the three Config Schemas they name before execution; no independent Target or Interface Understanding is required.
- **Authority:** Follow the Configure Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Runtime boundaries

- Follow the project Rules in `.claude/rules/` (Interface bootstrap, Interface Skill policy, Git discipline, Agent capabilities).
- Never read, search, or resolve anything under `.interface/agent/`. If a required Runtime capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- The `.interface/` tree is read-only except exact records under `.interface/config/` that the Configure Component grants this Skill authority to write.
