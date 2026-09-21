---
name: my-interface-review
description: Interface Review Operation: independently judge selected-phase Plans and implementation against their authorities. Invoke only as /my-interface-review or by my-interface-implement; never auto-invoke.
argument-hint: "[phase ...]"
disable-model-invocation: false
---

<!-- Synchronized by /my-interface-agent-native from the Agent Skill catalog entry `skills.review`. Native realization only; do not edit by hand. -->

# my-interface-review — Review Operation Skill

This Skill is the Claude Code bridge to the **Review Operation Component**. It does not define Review behavior. The owning Component is authoritative for behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions.

## Owning Operation Component

- Definition: `.interface/implementation/operations/review/review.md`
- Preferences: `.interface/implementation/operations/review/review.yaml`

Read both completely before execution and execute them as written. Do not copy, reinterpret, or redefine their workflow here.

## Invocation

- Human (`/my-interface-review [phase ...]`) or the declared coordinator `my-interface-implement`.
- Only `/my-interface-implement` may invoke this Skill as a coordinator, through Claude Code's Skill tool. Never invoke it autonomously.
- Arguments: `$ARGUMENTS` (as declared by the owning Component; zero or more phase selections).

## Bridge

- **Purpose:** Bridge the Agent Skill to the Review Operation Component.
- **Inputs:** Use the inputs declared by the Review Component Definition and Preferences.
- **Outputs:** Use the outputs declared by the Review Component Definition and Preferences.
- **Responsibility:** Read and execute the Review Component without redefining its meaning or workflow.
- **Trigger:** Activate explicitly for zero or more phase selections after implementation exists, or when skills.implement requires Review.
- **Required Understanding:** Establish current Interface Understanding and Target Understanding, then read the Review Component Definition and Preferences before execution.
- **Authority:** Follow the Review Component authority and write only through the Operation it defines.
- **Runtime realization:** Claude Code supplies invocation and Runtime mechanics only.

## Boundaries

- Follow the project Rules `interface-bootstrap`, `interface-skill-policy`, `interface-agent-capabilities`, and `git-discipline` from the start of the Workflow.
- Never read, search, or use `.interface/agent/`. If a needed Runtime capability is missing, report Runtime drift and ask the Human to run `/my-interface-agent-native`.
- Write only through the Operation the owning Component defines. Every other `.interface/` path stays read-only.
