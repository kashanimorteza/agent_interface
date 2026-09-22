---
name: my-interface-plan
description: Plan Operation of the Agent Project Interface — turns selected Target phases into bounded, verifiable Plans of Groups and Tasks. Use only when the Human explicitly runs /my-interface-plan or when the my-interface-implement coordinator requires a current Plan; never activate autonomously.
argument-hint: "[phase ...]"
---

# my-interface-plan

Agent-side bridge to the **Plan** Operation Component. This Skill is a synchronized Claude Code realization; the owning Operation Component is the sole authority for what Plan does.

Phase selection for this invocation: `$ARGUMENTS` (zero or more phases; an empty selection is interpreted by the Plan Component Definition).

## Invocation boundary

- **Human:** enabled — the Human runs `/my-interface-plan [phase ...]`.
- **Coordinator:** enabled only for `my-interface-implement`.
- **Autonomous:** disabled. Do not activate this Skill on your own initiative, from another Skill, or from any coordinator other than `my-interface-implement`. If none of the allowed invokers started it, stop and report.
- **Primary Operation:** yes. This Skill never invokes another primary Operation Skill (`my-interface-configure`, `my-interface-develop`, `my-interface-review`, `my-interface-implement`).
- **Required:** yes.

## Source of meaning

Read these in full before execution; they own Plan's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions:

- Definition: `.interface/implementation/operations/plan/plan.md`
- Preferences: `.interface/implementation/operations/plan/plan.yaml`

Do not restate, redefine, or replace their workflow here or in your own reasoning.

## Bridge

- **Purpose:** Bridge the Agent Skill to the Plan Operation Component.
- **Inputs:** Use the inputs declared by the Plan Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Plan Component Definition and Preferences.
- **Responsibility:** Read and execute the Plan Component without redefining its meaning or workflow.
- **Trigger:** Activate explicitly for zero or more phase selections, or when `my-interface-implement` requires a current Plan.
- **Required Understanding:** Establish current Interface Understanding and Target Understanding (see the Interface bootstrap Rule), then read the Plan Component Definition and Preferences before execution.
- **Authority:** Follow the Plan Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Runtime boundaries

- Follow the project Rules in `.claude/rules/` (Interface bootstrap, Interface Skill policy, Git discipline, Agent capabilities).
- Never read, search, or resolve anything under `.interface/agent/`. If a required Runtime capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- The `.interface/` tree is read-only except exact records under `.interface/config/` that the Plan Component grants this Skill authority to write.
