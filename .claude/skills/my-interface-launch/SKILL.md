---
name: my-interface-launch
description: Interface Launch Operation: activate a completed implementation and record the observable runtime result. Invoke only as /my-interface-launch by the Human; never auto-invoke.
disable-model-invocation: true
---

<!-- Synchronized by /my-interface-agent-native from the Agent Skill catalog entry `skills.launch`. Native realization only; do not edit by hand. -->

# my-interface-launch — Launch Operation Skill

This Skill is the Claude Code bridge to the **Launch Operation Component**. It does not define Launch behavior. The owning Component is authoritative for behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions.

## Owning Operation Component

- Definition: `.interface/implementation/operations/launch/launch.md`
- Preferences: `.interface/implementation/operations/launch/launch.yaml`

Read both completely before execution and execute them as written. Do not copy, reinterpret, or redefine their workflow here.

## Invocation

- Human (`/my-interface-launch`) or a declared coordinator whose allowed Skills include launch. No declared coordinator currently includes it, so model invocation is disabled until one does.
- Never invoke autonomously.
- Arguments: `$ARGUMENTS` (as declared by the owning Component; none are declared here).

## Bridge

- **Purpose:** Bridge the Agent Skill to the Launch Operation Component.
- **Inputs:** Use the inputs declared by the Launch Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Launch Component Definition and Preferences.
- **Responsibility:** Read and execute the Launch Component without redefining its meaning or workflow.
- **Trigger:** Activate explicitly or when end-to-end orchestration establishes the current Launch prerequisites.
- **Required Understanding:** Read the Launch Component Definition and Preferences before execution.
- **Authority:** Follow the Launch Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Boundaries

- Follow the project Rules `interface-bootstrap`, `interface-skill-policy`, `interface-agent-capabilities`, and `git-discipline` from the start of the Workflow.
- Never read, search, or use `.interface/agent/`. If a needed Runtime capability is missing, report Runtime drift and ask the Human to run `/my-interface-agent-native`.
- Write only through the Operation the owning Component defines. Every other `.interface/` path stays read-only.
