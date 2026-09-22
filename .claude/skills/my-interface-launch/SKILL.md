---
name: my-interface-launch
description: Launch Operation of the Agent Project Interface — verifies readiness, activates the completed implementation for one scope (api, presentation, logic, complete/all), and records the runtime result. Use only when the Human explicitly runs /my-interface-launch or when a declared coordinator invokes it; never activate autonomously.
argument-hint: "[api|presentation|logic|complete|all]"
---

# my-interface-launch

Agent-side bridge to the **Launch** Operation Component. This Skill is a synchronized Claude Code realization; the owning Operation Component is the sole authority for what Launch does.

Scope for this invocation: `$ARGUMENTS` (one optional scope; behavior with no scope is defined by the Launch Component Definition).

## Invocation boundary

- **Human:** enabled — the Human runs `/my-interface-launch [scope]`.
- **Coordinator:** enabled for declared coordinators (a Skill whose synchronized declaration names Launch among the Skills it may invoke). No currently synchronized coordinator lists Launch.
- **Autonomous:** disabled. Do not activate this Skill on your own initiative or from a Skill that is not a declared coordinator for it. If none of the allowed invokers started it, stop and report.
- **Primary Operation:** no (supporting Operation Skill).
- **Required:** yes.

## Source of meaning

Read these in full before execution; they own Launch's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions:

- Definition: `.interface/implementation/operations/launch/launch.md`
- Preferences: `.interface/implementation/operations/launch/launch.yaml`

Do not restate, redefine, or replace their workflow here or in your own reasoning.

## Bridge

- **Purpose:** Bridge the Agent Skill to the Launch Operation Component.
- **Inputs:** Use the inputs declared by the Launch Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Launch Component Definition and Preferences.
- **Responsibility:** Read and execute the Launch Component without redefining its meaning or workflow.
- **Trigger:** Activate explicitly or when end-to-end orchestration establishes the current Launch prerequisites.
- **Required Understanding:** Read the Launch Component Definition and Preferences before execution (the Definition then states the further Understanding it requires).
- **Authority:** Follow the Launch Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Runtime boundaries

- Follow the project Rules in `.claude/rules/` (Interface bootstrap, Interface Skill policy, Git discipline, Agent capabilities).
- Never read, search, or resolve anything under `.interface/agent/`. If a required Runtime capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- Never print, log, or record secret values.
- The `.interface/` tree is read-only except exact records under `.interface/config/` that the Launch Component grants this Skill authority to write.
