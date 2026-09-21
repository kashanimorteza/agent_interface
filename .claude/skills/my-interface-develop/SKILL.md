---
name: my-interface-develop
description: Interface Develop Operation: execute authorized planned Tasks for selected phases and record the results. Invoke only as /my-interface-develop or by my-interface-implement; never auto-invoke.
argument-hint: "[phase ...]"
disable-model-invocation: false
---

<!-- Synchronized by /my-interface-agent-native from the Agent Skill catalog entry `skills.develop`. Native realization only; do not edit by hand. -->

# my-interface-develop — Develop Operation Skill

This Skill is the Claude Code bridge to the **Develop Operation Component**. It does not define Develop behavior. The owning Component is authoritative for behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions.

## Owning Operation Component

- Definition: `.interface/implementation/operations/develop/develop.md`
- Preferences: `.interface/implementation/operations/develop/develop.yaml`

Read both completely before execution and execute them as written. Do not copy, reinterpret, or redefine their workflow here.

## Invocation

- Human (`/my-interface-develop [phase ...]`) or the declared coordinator `my-interface-implement`.
- Only `/my-interface-implement` may invoke this Skill as a coordinator, through Claude Code's Skill tool. Never invoke it autonomously.
- Arguments: `$ARGUMENTS` (as declared by the owning Component; zero or more phase selections).

## Bridge

- **Purpose:** Bridge the Agent Skill to the Develop Operation Component.
- **Inputs:** Use the inputs declared by the Develop Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Develop Component Definition and Preferences.
- **Responsibility:** Read and execute the Develop Component without redefining its meaning or workflow.
- **Trigger:** Activate explicitly for zero or more phase selections after a valid current Plan exists and prerequisites are ready, or when skills.implement requires Development.
- **Required Understanding:** Establish current Interface Understanding and Target Understanding, then read the Develop Component Definition and Preferences before execution.
- **Authority:** Follow the Develop Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Boundaries

- Follow the project Rules `interface-bootstrap`, `interface-skill-policy`, `interface-agent-capabilities`, and `git-discipline` from the start of the Workflow.
- Never read, search, or use `.interface/agent/`. If a needed Runtime capability is missing, report Runtime drift and ask the Human to run `/my-interface-agent-native`.
- Write only through the Operation the owning Component defines. Every other `.interface/` path stays read-only.
