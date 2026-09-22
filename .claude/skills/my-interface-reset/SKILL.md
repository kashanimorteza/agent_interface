---
name: my-interface-reset
description: Reset Operation of the Agent Project Interface — previews and, after explicit Human confirmation, reconciles operational records and outputs for exactly one scope (phases, all phases, config, or complete). Invoked only by the Human via /my-interface-reset.
argument-hint: "[phase ... | config | complete]"
disable-model-invocation: true
---

# my-interface-reset

Agent-side bridge to the **Reset** Operation Component. This Skill is a synchronized Claude Code realization; the owning Operation Component is the sole authority for what Reset does.

Reset scope for this invocation: `$ARGUMENTS` (exactly one scope, as defined by the Reset Component Definition).

## Invocation boundary

- **Human:** enabled — only through the Human's explicit `/my-interface-reset [scope]`.
- **Coordinator:** disabled — no Skill or Agent Instance may invoke this Skill (enforced by `disable-model-invocation`).
- **Autonomous:** disabled.
- **Primary Operation:** no (supporting Operation Skill).
- **Required:** yes.

## Source of meaning

Read these in full before execution; they own Reset's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions:

- Definition: `.interface/implementation/operations/reset/reset.md`
- Preferences: `.interface/implementation/operations/reset/reset.yaml`

Do not restate, redefine, or replace their workflow here or in your own reasoning.

## Bridge

- **Purpose:** Bridge the Agent Skill to the Reset Operation Component.
- **Inputs:** Use the inputs declared by the Reset Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Reset Component Definition and Preferences.
- **Responsibility:** Read and execute the Reset Component without redefining its meaning or workflow.
- **Trigger:** Activate only through explicit Human invocation with one reset scope.
- **Required Understanding:** Read the Reset Component Definition and Preferences before execution.
- **Authority:** Follow the Reset Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Runtime boundaries

- Follow the project Rules in `.claude/rules/` (Interface bootstrap, Interface Skill policy, Git discipline, Agent capabilities).
- Never read, search, or resolve anything under `.interface/agent/`. If a required Runtime capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- The `.interface/` tree is read-only except exact records under `.interface/config/` that the Reset Component grants this Skill authority to write. Never delete or alter Interface or Target sources.
