# Authority and Ownership

This section defines record ownership, write authority, and the read-only boundary of Agent Interface.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Overview](#overview)**
2. **[Ownership](#ownership)**
3. **[Write Authority](#write-authority)**
4. **[Boundaries](#boundaries)**

<br>

<!--------------------------------------------------------------------------------- Overview --->
## Overview

Explicit Target intent and applicable Implementation Principles guide operational Skills. Implementation Preferences supply engineering defaults where the Target leaves a choice unstated. Agent Preferences declare desired portable execution capabilities solely for Agent Sync, which learns Native-specific mappings and materializes the synchronized Runtime rules and capabilities consumed by every other Skill. Operational Schemas define the shape of operational records, authored-source Schemas define Principles, Implementation Preferences, and Agent Preferences, and the general YAML Schema supplies their common YAML frame together with Config files. Schema definition files use their own formats. Config stores operational records and does not define the Target.

Target: Human-defined intent.

Principles: Mandatory philosophy, responsibilities, and boundaries.

Implementation Preferences: Engineering defaults for unspecified Target choices.

Agent Preferences: Current Agent Module selections, resources, portable realization requirements, and explicit empty categories.

Schema: Common YAML frame for Implementation Preferences, Agent Preferences, and Config, authored-source structure, and the storage structure of every operational record.

Config: Mutable operational records.

<br>

<!--------------------------------------------------------------------------------- Ownership --->
## Ownership

Ownership answers who a record belongs to, and it belongs to the Human or to a Component:

Human: Owns Interface, Target, Principles, Implementation Preferences, Agent Preferences, and Schema sources.

Plan: Owns Plans, Groups, Tasks, their status, and their history.

State: Owns active Workflow position, aggregate phase progress, Implement and Launch results, operational History, Blockers, and Open Questions.

Review: Owns recorded Findings and their state.

<br>

<!--------------------------------------------------------------------------------- Write Authority --->
## Write Authority

Write authority answers which Skill may change a record, and every write happens under the rules of the Component that owns it:

Configure: Creates and reconciles the persistent Application Manifest, writes every operational Config, synchronizes phase records, and records its State outcome.

Planning: Writes Plans, Groups, and Tasks under Plan, and Planning progress and History under State.

Developing: Writes implementation and Task status and history under Plan, and Development progress and History under State.

Reviewer: Writes Findings under Review, and Review progress and History under State.

Configure, Planning, and Developing: Write the active Workflow position under State.

Launch: Changes runtime state through Platform and writes Launch State, access points, and History under State.

Implement: Coordinates operation Skills and writes only Implementation State and its History under State.

Reset: After Human confirmation of the preview, removes or resets explicit-phase outputs, every generated phase when no phase is supplied, Config only, or the complete set of Config and all-phase implementation outputs, including reconciliation of the Workflow position, under the owning Components' rules.

Agent Native Sync: On explicit Human invocation, exclusively reads the Agent Module and reconciles its declarations with self-contained project-scoped Native artifacts outside Interface sources.

Reviewing, Launch, Implement, and Agent Native Sync: Do not directly change the active Workflow mode.

Every Skill: May record its own Blockers and Open Questions under State's rules when applicable.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

Each Skill writes only the records it has authority over, and always under the rules of the Component that owns them. Operational records follow their source authorities and must not redefine them.

The complete `.interface/` tree is read-only to every Agent Role and Skill by default. The only mutable exception is `.interface/config/`, and a Skill may change files there only within the write authority stated above and the owning Component's rules. No other Interface path becomes writable because it is added later, discovered by a Tool, or named by a Plan.
