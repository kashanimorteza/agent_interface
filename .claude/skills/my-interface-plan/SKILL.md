---
name: my-interface-plan
description: Interface Plan Operation: turn selected Target phases into bounded Plans of Groups and Tasks. Invoke only as /my-interface-plan or by my-interface-implement; never auto-invoke.
argument-hint: "[phase ...]"
disable-model-invocation: false
---

<!-- Synchronized by /my-interface-agent-native from the Agent Skill catalog entry `skills.plan`. Native realization only; do not edit by hand. -->

# my-interface-plan — Plan Operation Skill

This Skill is the Claude Code bridge to the **Plan Operation Component**. It does not define Plan behavior. The owning Component is authoritative for behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions.

## Owning Operation Component

- Definition: `.interface/implementation/operations/plan/plan.md`
- Preferences: `.interface/implementation/operations/plan/plan.yaml`

Read both completely before execution and execute them as written. Do not copy, reinterpret, or redefine their workflow here.

## Invocation

- Human (`/my-interface-plan [phase ...]`) or the declared coordinator `my-interface-implement`.
- Only `/my-interface-implement` may invoke this Skill as a coordinator, through Claude Code's Skill tool. Never invoke it autonomously.
- Arguments: `$ARGUMENTS` (as declared by the owning Component; zero or more phase selections).

## Bridge

- **Purpose:** Bridge the Agent Skill to the Plan Operation Component.
- **Inputs:** Use the inputs declared by the Plan Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Plan Component Definition and Preferences.
- **Responsibility:** Read and execute the Plan Component without redefining its meaning or workflow.
- **Trigger:** Activate explicitly for zero or more phase selections, or when skills.implement requires a current Plan.
- **Required Understanding:** Establish current Interface Understanding and Target Understanding, then read the Plan Component Definition and Preferences before execution.
- **Authority:** Follow the Plan Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Boundaries

- Follow the project Rules `interface-bootstrap`, `interface-skill-policy`, `interface-agent-capabilities`, and `git-discipline` from the start of the Workflow.
- Never read, search, or use `.interface/agent/`. If a needed Runtime capability is missing, report Runtime drift and ask the Human to run `/my-interface-agent-native`.
- Write only through the Operation the owning Component defines. Every other `.interface/` path stays read-only.
