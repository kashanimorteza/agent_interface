---
name: my-interface-reset
description: Interface Reset Operation: reconcile authorized operational records and outputs with one explicit reset scope. Invoke only as /my-interface-reset by the Human; never auto-invoke.
argument-hint: "<reset scope>"
disable-model-invocation: true
---

<!-- Synchronized by /my-interface-agent-native from the Agent Skill catalog entry `skills.reset`. Native realization only; do not edit by hand. -->

# my-interface-reset — Reset Operation Skill

This Skill is the Claude Code bridge to the **Reset Operation Component**. It does not define Reset behavior. The owning Component is authoritative for behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions.

## Owning Operation Component

- Definition: `.interface/implementation/operations/reset/reset.md`
- Preferences: `.interface/implementation/operations/reset/reset.yaml`

Read both completely before execution and execute them as written. Do not copy, reinterpret, or redefine their workflow here.

## Invocation

- Explicit Human invocation only (`/my-interface-reset <reset scope>`). No coordinator or autonomous invocation.
- Never invoke autonomously.
- Arguments: `$ARGUMENTS` (as declared by the owning Component; exactly one reset scope).

## Bridge

- **Purpose:** Bridge the Agent Skill to the Reset Operation Component.
- **Inputs:** Use the inputs declared by the Reset Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Reset Component Definition and Preferences.
- **Responsibility:** Read and execute the Reset Component without redefining its meaning or workflow.
- **Trigger:** Activate only through explicit Human invocation with one reset scope.
- **Required Understanding:** Read the Reset Component Definition and Preferences before execution.
- **Authority:** Follow the Reset Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Boundaries

- Follow the project Rules `interface-bootstrap`, `interface-skill-policy`, `interface-agent-capabilities`, and `git-discipline` from the start of the Workflow.
- Never read, search, or use `.interface/agent/`. If a needed Runtime capability is missing, report Runtime drift and ask the Human to run `/my-interface-agent-native`.
- Write only through the Operation the owning Component defines. Every other `.interface/` path stays read-only.
