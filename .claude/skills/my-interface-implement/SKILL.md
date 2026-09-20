---
name: my-interface-implement
description: Coordinate the workflow across Configure, Plan, Develop, Review, and Launch through the Implement Process Component. Invoke only when the Human explicitly runs /my-interface-implement; never invoke it from another Skill, coordinator, or automatically.
disable-model-invocation: true
argument-hint: "[phase selection ...]"
---

# my-interface-implement

Synchronized Claude Code realization of a Human-owned Agent Skill declaration (Constructed). It is a bridge only: the owning Implementation Process Component is authoritative for this Skill's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions. This file never redefines them.

## Bridge
- Purpose: Coordinate the workflow across Configure, Plan, Develop, Review, and Launch through the Implement Process Component.
- Owning Process Component: `.interface/implementation/process/implement/definition.md` and `.interface/implementation/process/implement/preferences.yaml`
- Invocation: explicit Human only. Coordinator invocation: disabled. Autonomous invocation: disabled.
- Trigger: Activate only through explicit Human invocation for zero or more phase selections.
- Inputs and outputs: exactly those the Implement Component Definition and Preferences declare.
- Authority: Follow the Implement Component authority and invoke child Process Skills only through the Runtime's own Skill mechanism.
- Runtime realization: Claude Code supplies invocation and Runtime mechanics only.

## Procedure
1. Establish Interface Understanding as the synchronized Rule `interface-bootstrap` requires: read `.interface/interface.md` and the Foundation section files it links, before acting.
2. Read the Implement Component Definition and Preferences listed above completely, then read every further authority they require. Do not rely on memory or prior summaries.
3. Read the synchronized Rule `interface-skill-policy` and apply it (Interface protection, project scope, delegation, conduct, decision policy).
4. Arguments (`$ARGUMENTS`): treat as the phase selection (zero or more) the Component defines; if the Component defines no meaning for them, report that instead of guessing.
5. Coordinate the Implement Component as defined, without redefining its meaning or workflow. Repeating this Skill preserves valid work and never destructively replaces meaningful work.
6. Report the outcome only with current observable evidence, and expose unfinished work, blockers, and required Human actions.

## Coordination
- Allowed child Skills: `/my-interface-configure`, `/my-interface-plan`, `/my-interface-develop`, `/my-interface-review`, `/my-interface-launch`.
- Invoke a child Skill only through the Skill tool. Each Process Component keeps ownership of its own records and outputs; this Skill never writes them itself.
- Delegation carries no more authority than this Skill's Process Component grants.

## Boundaries
- Never read, search, or use the Agent Module or any Agent Module source (the agent directory under `.interface/`). Its content reaches you only through the synchronized Native artifacts. If a required Rule, Skill, or capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never invoke it yourself.
- The whole `.interface/` tree is read-only except exact Config records this Skill's Process Component gives it authority over.
- This Skill owns executable capability only, not Target meaning, Implementation policy, or another Component's records.
