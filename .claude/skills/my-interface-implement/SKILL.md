---
name: my-interface-implement
description: Interface Implement Operation: coordinate Configure, Plan, Develop, and Review across the selected phases. Invoke only as /my-interface-implement by the Human; never auto-invoke.
argument-hint: "[phase ...]"
disable-model-invocation: true
---

<!-- Synchronized by /my-interface-agent-native from the Agent Skill catalog entry `skills.implement`. Native realization only; do not edit by hand. -->

# my-interface-implement — Implement Operation Skill

This Skill is the Claude Code bridge to the **Implement Operation Component**. It does not define Implement behavior. The owning Component is authoritative for behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions.

## Owning Operation Component

- Definition: `.interface/implementation/operations/implement/implement.md`
- Preferences: `.interface/implementation/operations/implement/implement.yaml`

Read both completely before execution and execute them as written. Do not copy, reinterpret, or redefine their workflow here.

## Invocation

- Explicit Human invocation only (`/my-interface-implement [phase ...]`). No coordinator or autonomous invocation.
- Coordination: may invoke only `my-interface-configure`, `my-interface-plan`, `my-interface-develop`, and `my-interface-review`, and only through Claude Code's own Skill tool. Each Operation Component keeps ownership of its records and outputs.
- Arguments: `$ARGUMENTS` (as declared by the owning Component; zero or more phase selections).

## Bridge

- **Purpose:** Bridge the Agent Skill to the Implement Operation Component.
- **Inputs:** Use the inputs declared by the Implement Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Implement Component Definition and Preferences.
- **Responsibility:** Read and coordinate the Implement Component without redefining its meaning or workflow.
- **Trigger:** Activate only through explicit Human invocation for zero or more phase selections.
- **Required Understanding:** Read the Implement Component Definition and Preferences before execution; Implement has no independent Target or Interface Understanding.
- **Authority:** Follow the Implement Component authority and invoke child Operation Skills only through the Runtime's own Skill mechanism.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Boundaries

- Follow the project Rules `interface-bootstrap`, `interface-skill-policy`, `interface-agent-capabilities`, and `git-discipline` from the start of the Workflow.
- Never read, search, or use `.interface/agent/`. If a needed Runtime capability is missing, report Runtime drift and ask the Human to run `/my-interface-agent-native`.
- Write only through the Operation the owning Component defines. Every other `.interface/` path stays read-only.
