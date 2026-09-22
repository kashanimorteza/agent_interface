---
name: my-interface-review
description: Review Operation of the Agent Project Interface — independently assures selected phase Plans and implemented results and records Findings. Use only when the Human explicitly runs /my-interface-review or when the my-interface-implement coordinator requires Review; never activate autonomously.
argument-hint: "[phase ...]"
---

# my-interface-review

Agent-side bridge to the **Review** Operation Component. This Skill is a synchronized Claude Code realization; the owning Operation Component is the sole authority for what Review does.

Phase selection for this invocation: `$ARGUMENTS` (zero or more phases; an empty selection is interpreted by the Review Component Definition).

## Invocation boundary

- **Human:** enabled — the Human runs `/my-interface-review [phase ...]`.
- **Coordinator:** enabled only for `my-interface-implement`.
- **Autonomous:** disabled. Do not activate this Skill on your own initiative, from another Skill, or from any coordinator other than `my-interface-implement`. If none of the allowed invokers started it, stop and report.
- **Primary Operation:** yes. This Skill never invokes another primary Operation Skill (`my-interface-configure`, `my-interface-plan`, `my-interface-develop`, `my-interface-implement`).
- **Required:** yes.

## Source of meaning

Read these in full before execution; they own Review's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions:

- Definition: `.interface/implementation/operations/review/review.md`
- Preferences: `.interface/implementation/operations/review/review.yaml`

Do not restate, redefine, or replace their workflow here or in your own reasoning.

## Bridge

- **Purpose:** Bridge the Agent Skill to the Review Operation Component.
- **Inputs:** Use the inputs declared by the Review Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Review Component Definition and Preferences.
- **Responsibility:** Read and execute the Review Component without redefining its meaning or workflow.
- **Trigger:** Activate explicitly for zero or more phase selections after implementation exists, or when `my-interface-implement` requires Review.
- **Required Understanding:** Establish current Interface Understanding and Target Understanding (see the Interface bootstrap Rule), then read the Review Component Definition and Preferences before execution.
- **Authority:** Follow the Review Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Runtime boundaries

- Follow the project Rules in `.claude/rules/` (Interface bootstrap, Interface Skill policy, Git discipline, Agent capabilities).
- Never read, search, or resolve anything under `.interface/agent/`. If a required Runtime capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- The `.interface/` tree is read-only except exact records under `.interface/config/` that the Review Component grants this Skill authority to write.
