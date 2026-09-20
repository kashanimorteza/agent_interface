---
name: my-interface-develop
description: Execute planned implementation Tasks through the Develop Process Component. Invoke only when the Human explicitly runs /my-interface-develop or when the declared coordinator /my-interface-implement invokes it through the Skill tool; never invoke it autonomously.
argument-hint: "[phase selection ...]"
---

# my-interface-develop

Synchronized Claude Code realization of a Human-owned Agent Skill declaration (Constructed). It is a bridge only: the owning Implementation Process Component is authoritative for this Skill's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions. This file never redefines them.

## Bridge
- Purpose: Execute planned implementation Tasks through the Develop Process Component.
- Owning Process Component: `.interface/implementation/process/develop/definition.md` and `.interface/implementation/process/develop/preferences.yaml`
- Invocation: the Human, or the declared coordinator `/my-interface-implement`. Autonomous invocation: disabled — do not start this Skill on your own initiative or because a request merely resembles it.
- Trigger: Activate explicitly for zero or more phase selections after a valid current Plan exists and prerequisites are ready.
- Inputs and outputs: exactly those the Develop Component Definition and Preferences declare.
- Authority: Follow the Develop Component authority and write only through the Process operation it defines.
- Runtime realization: Claude Code supplies invocation and Runtime mechanics only.

## Procedure
1. Establish Interface Understanding as the synchronized Rule `interface-bootstrap` requires: read `.interface/interface.md` and the Foundation section files it links, before acting.
2. Read the Develop Component Definition and Preferences listed above completely, then read every further authority they require. Do not rely on memory or prior summaries.
3. Read the synchronized Rule `interface-skill-policy` and apply it (Interface protection, project scope, delegation, conduct, decision policy).
4. Arguments (`$ARGUMENTS`): treat as the phase selection (zero or more) the Component defines; if the Component defines no meaning for them, report that instead of guessing.
5. Execute the Develop Component as defined, without redefining its meaning or workflow. Repeating this Skill preserves valid work and never destructively replaces meaningful work.
6. Report the outcome only with current observable evidence, and expose unfinished work, blockers, and required Human actions.

## Boundaries
- Never read, search, or use the Agent Module or any Agent Module source (the agent directory under `.interface/`). Its content reaches you only through the synchronized Native artifacts. If a required Rule, Skill, or capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- The whole `.interface/` tree is read-only except exact Config records this Skill's Process Component gives it authority over.
- This Skill owns executable capability only, not Target meaning, Implementation policy, or another Component's records.
