---
name: my-interface-implement
description: Implement Operation of the Agent Project Interface — the coordinating Skill that runs Configure (when needed), then Plan, Develop, and Review across the selected phases. Invoked only by the Human via /my-interface-implement.
argument-hint: "[phase ...]"
disable-model-invocation: true
---

# my-interface-implement

Agent-side bridge to the **Implement** Operation Component. This is the project's selected coordinating Skill. It is a synchronized Claude Code realization; the owning Operation Component is the sole authority for what Implement does.

Phase selection for this invocation: `$ARGUMENTS` (zero or more phases; an empty selection is interpreted by the Implement Component Definition).

## Invocation boundary

- **Human:** enabled — only through the Human's explicit `/my-interface-implement [phase ...]`.
- **Coordinator:** disabled — no Skill or Agent Instance may invoke this Skill (enforced by `disable-model-invocation`).
- **Autonomous:** disabled.
- **Primary Operation:** yes.
- **Required:** yes.

## Coordination

- **Allowed child Skills:** `my-interface-configure`, `my-interface-plan`, `my-interface-develop`, `my-interface-review`. No other Skill may be invoked as a child; in particular never `my-interface-reset`, `my-interface-agent-native`, or `my-interface-launch`.
- **Mechanism:** invoke each child only through Claude Code's own Skill mechanism (the Skill tool with the child's name and phase arguments). Never execute a child's workflow inline in place of invoking it.
- **Authority:** delegated invocation only; each Operation Component retains ownership of its records and outputs.

## Source of meaning

Read these in full before execution; they own Implement's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions:

- Definition: `.interface/implementation/operations/implement/implement.md`
- Preferences: `.interface/implementation/operations/implement/implement.yaml`

Do not restate, redefine, or replace their workflow here or in your own reasoning.

## Bridge

- **Purpose:** Bridge the Agent Skill to the Implement Operation Component.
- **Inputs:** Use the inputs declared by the Implement Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Implement Component Definition and Preferences.
- **Responsibility:** Read and coordinate the Implement Component without redefining its meaning or workflow.
- **Trigger:** Activate only through explicit Human invocation for zero or more phase selections.
- **Required Understanding:** Read the Implement Component Definition and Preferences before execution; Implement has no independent Target or Interface Understanding.
- **Authority:** Follow the Implement Component authority and invoke child Operation Skills only through the Runtime's own Skill mechanism.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Runtime boundaries

- Follow the project Rules in `.claude/rules/` (Interface bootstrap, Interface Skill policy, Git discipline, Agent capabilities).
- Never read, search, or resolve anything under `.interface/agent/`. If a required child Skill or Runtime capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- The `.interface/` tree is read-only except exact records under `.interface/config/` that the Implement Component grants this Skill authority to write.
