---
name: my-interface-configure
description: Interface Configure Operation: create and structurally reconcile the Config records from their Schemas. Invoke only as /my-interface-configure or by my-interface-implement; never auto-invoke.
disable-model-invocation: false
---

<!-- Synchronized by /my-interface-agent-native from the Agent Skill catalog entry `skills.configure`. Native realization only; do not edit by hand. -->

# my-interface-configure — Configure Operation Skill

This Skill is the Claude Code bridge to the **Configure Operation Component**. It does not define Configure behavior. The owning Component is authoritative for behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions.

## Owning Operation Component

- Definition: `.interface/implementation/operations/configure/configure.md`
- Preferences: `.interface/implementation/operations/configure/configure.yaml`

Read both completely before execution and execute them as written. Do not copy, reinterpret, or redefine their workflow here.

## Invocation

- Human (`/my-interface-configure`) or the declared coordinator `my-interface-implement`.
- Only `/my-interface-implement` may invoke this Skill as a coordinator, through Claude Code's Skill tool. Never invoke it autonomously.
- Arguments: `$ARGUMENTS` (as declared by the owning Component; none are declared here).

## Bridge

- **Purpose:** Bridge the Agent Skill to the Configure Operation Component.
- **Inputs:** Use the inputs declared by the Configure Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Configure Component Definition and Preferences.
- **Responsibility:** Read and execute the Configure Component without redefining its meaning or workflow.
- **Trigger:** Activate when invoked by the Human or skills.implement.
- **Required Understanding:** Read the Configure Component Definition and Preferences and the three Config Schemas before execution; no independent Target or Interface Understanding is required.
- **Authority:** Follow the Configure Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Boundaries

- Follow the project Rules `interface-bootstrap`, `interface-skill-policy`, `interface-agent-capabilities`, and `git-discipline` from the start of the Workflow.
- Never read, search, or use `.interface/agent/`. If a needed Runtime capability is missing, report Runtime drift and ask the Human to run `/my-interface-agent-native`.
- Write only through the Operation the owning Component defines. Every other `.interface/` path stays read-only.
