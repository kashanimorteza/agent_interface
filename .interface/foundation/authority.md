# Authority and Ownership

This file carries the Authority and Ownership section of the Interface, moved here verbatim from `interface.md` on 2026-09-17. It is part of Interface Understanding: every Skill reads `interface.md` and this file before acting. The Interface file remains the canonical entry point; this file is one of its sections.

<br>

Explicit Target intent and applicable Implementation Principles guide operational Skills. Implementation Preferences supply engineering defaults where the Target leaves a choice unstated. Agent Preferences declare desired portable execution capabilities solely for Agent Sync, which learns Native-specific mappings and materializes the synchronized Runtime rules and capabilities consumed by every other Skill. Operational Schemas define the shape of operational records, authored-source Schemas define Principles, Implementation Preferences, and Agent Preferences, and the general YAML Schema supplies their common YAML frame together with Config files. Schema definition files use their own formats. Config stores operational records and does not define the Target.

```text
Target = human-defined intent
Principles = mandatory philosophy, responsibilities, and boundaries
Implementation Preferences = engineering defaults for unspecified Target choices
Agent Preferences = current Agent Module selections, resources, portable realization requirements, and explicit empty categories
Schema = common YAML frame for Implementation Preferences, Agent Preferences, and Config, authored-source structure, and the storage structure of every operational record
Config = the mutable operational records
```

Ownership answers who a record belongs to, and it belongs to the Human or to a Component:

```text
Human = owns Interface, Target, Principles, Implementation Preferences, Agent Preferences, and Schema sources
Plan = owns Plans, Groups, Tasks, their status, and their history
State = owns active Workflow position, aggregate phase progress, Implement and Launch results, operational History, Blockers, and Open Questions
Review = owns recorded Findings and their state
```

Write authority answers which Skill may change a record, and every write happens under the rules of the Component that owns it:

```text
Configure = creates and reconciles the persistent Application Manifest, writes every operational Config, synchronizes phase records, and records its State outcome
Planning = writes Plans, Groups, and Tasks under Plan, and Planning progress and History under State
Developing = writes implementation and Task status and history under Plan, and Development progress and History under State
Reviewer = writes Findings under Review, and Review progress and History under State
Configure, Planning, and Developing = write the active Workflow position under State
Launch = changes runtime state through Platform and writes Launch State, access points, and History under State
Implement = coordinates operation Skills and writes only Implementation State and its History under State
Reset = after human confirmation of the preview, removes or resets explicit-phase outputs, every generated phase when no phase is supplied, Config only, or the complete set of Config and all-phase implementation outputs, including reconciliation of the Workflow position, under the owning Components' rules
Agent Native Sync = on explicit Human invocation, exclusively reads the Agent Module and reconciles its declarations with self-contained project-scoped Native artifacts outside Interface sources
Reviewing, Launch, Implement, and Agent Native Sync = do not directly change the active Workflow mode
Every Skill = may record its own Blockers and Open Questions under State's rules when applicable
```

Each Skill writes only the records it has authority over, and always under the rules of the Component that owns them. Operational records follow their source authorities and must not redefine them.

The complete `.interface/` tree is read-only to every Agent Role and Skill by default. The only mutable exception is `.interface/foundation/config/`, and a Skill may change files there only within the write authority stated above and the owning Component's rules. No other Interface path becomes writable because it is added later, discovered by a Tool, or named by a Plan.
