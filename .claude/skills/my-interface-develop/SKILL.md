---
name: my-interface-develop
description: Develop Operation of the Agent Project Interface — executes eligible planned Tasks for selected phases and records evidence. Use only when the Human explicitly runs /my-interface-develop or when the my-interface-implement coordinator requires Development; never activate autonomously.
argument-hint: "[phase ...]"
---

# my-interface-develop

Agent-side bridge to the **Develop** Operation Component. This Skill is a synchronized Claude Code realization; the owning Operation Component is the sole authority for what Develop does.

Phase selection for this invocation: `$ARGUMENTS` (zero or more phases; an empty selection is interpreted by the Develop Component Definition).

## Invocation boundary

- **Human:** enabled — the Human runs `/my-interface-develop [phase ...]`.
- **Coordinator:** enabled only for `my-interface-implement`.
- **Autonomous:** disabled. Do not activate this Skill on your own initiative, from another Skill, or from any coordinator other than `my-interface-implement`. If none of the allowed invokers started it, stop and report.
- **Primary Operation:** yes. This Skill never invokes another primary Operation Skill (`my-interface-configure`, `my-interface-plan`, `my-interface-review`, `my-interface-implement`).
- **Required:** yes.

## Source of meaning

Read these in full before execution; they own Develop's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions:

- Definition: `.interface/implementation/operations/develop/develop.md`
- Preferences: `.interface/implementation/operations/develop/develop.yaml`

Do not restate, redefine, or replace their workflow here or in your own reasoning.

## Bridge

- **Purpose:** Bridge the Agent Skill to the Develop Operation Component.
- **Inputs:** Use the inputs declared by the Develop Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Develop Component Definition and Preferences.
- **Responsibility:** Read and execute the Develop Component without redefining its meaning or workflow.
- **Trigger:** Activate explicitly for zero or more phase selections after a valid current Plan exists and prerequisites are ready, or when `my-interface-implement` requires Development.
- **Required Understanding:** Establish current Interface Understanding and Target Understanding (see the Interface bootstrap Rule), then read the Develop Component Definition and Preferences before execution.
- **Authority:** Follow the Develop Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Runtime boundaries

- Follow the project Rules in `.claude/rules/` (Interface bootstrap, Interface Skill policy, Git discipline, Agent capabilities).
- Never read, search, or resolve anything under `.interface/agent/`. If a required Runtime capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- The `.interface/` tree is read-only except exact records under `.interface/config/` that the Develop Component grants this Skill authority to write.
