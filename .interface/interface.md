# Agent Interface

Agent Interface is the Human-defined structure that coordinates Target, Implementation, Agent, Config, and the shared operational workflow.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terminology](#terminology)**
3. **[Architecture](#architecture)**
4. **[Modules](#modules)**
5. **[Config](#config)**
6. **[Foundation Files](#foundation-files)**
7. **[Understanding](#understanding)**
8. **[Authority and Ownership](#authority-and-ownership)**
9. **[Workflow](#workflow)**


<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

The Introduction states what Agent Interface is: an implementation-oriented interface for AI-assisted software development that separates Target, Implementation, and Agent so any one can be replaced without redesigning the others, its purpose, how it works, its independence, its core idea, and its design goals.

Responsibility: Overview, purpose, how it works, independence, core idea, and design goals of Agent Interface; part of every Skill's required Interface Understanding.

→ [Read more about Introduction](foundation/introduction.md)



<br>

<!--------------------------------------------------------------------------------- Terminology --->
## Terminology

Terminology defines the shared vocabulary used throughout the Interface — Interface, Human, Module, Target, Implementation, Agent, Component, Principles, Preferences, Schema, Config, Plan, Task, Understanding, Operation, Workflow, Mode, Skill, the Agent Module and its Native, Instances, Preferences, Roles, and capabilities, Agent Native Sync, and Capability Realization Kinds.

Responsibility: Defines every capitalized term the Interface uses; read before any other section; part of every Skill's required Interface Understanding.

→ [Read more about Terminology](foundation/terminology.md)



<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

Architecture shows the high-level shape of Agent Interface as one tree, including the principal Modules, the Config boundary, and the main Foundation resources with their immediate parts.

Responsibility: The conceptual architecture tree of Agent Interface and one sentence on what each part contributes; part of every Skill's required Interface Understanding.

→ [Read more about Architecture](foundation/architecture.md)



<br>

<!--------------------------------------------------------------------------------- Modules --->
## Modules

Target, Implementation, and Agent are the three primary Modules of Agent Interface. Each Module owns a distinct responsibility and documents one combined conceptual and repository Structure.

<!-------------------------- Target -->
### Target

The Target describes **what the Interface is working on**, through a Human Definition and a Technical Definition that takes precedence on conflict.

Responsibility: Explains the Target Module and maps its files; the Understanding sources remain the two definition files it points to.

→ [Read more about the Target Module](target/target.md)

<!-------------------------- Implementation -->
### Implementation

The Implementation Module defines the reusable programming personality, standards, and engineering perspective applied to a Target through its Development and Operations Subsystems.

Responsibility: Explains the Implementation Module and maps its Development and Operations Subsystems and their Components.

The Operations defined by this Interface are realized by the corresponding Operation Components under `implementation/operations/`; their Definitions and Preferences are the source for the operational Skills that perform them.

→ [Read more about the Implementation Module](implementation/implementation.md)

<!-------------------------- Agent -->
### Agent

The Agent Module is the Human-owned, Runtime-independent declaration of how an Agent Native and its Agent Instances must operate, realized in the selected Runtime only through explicit Agent Native Sync; only Agent Native Sync enters it, and every other role uses the synchronized Runtime realization.

Responsibility: Explains the Agent Module and maps every Component's Definition and Preferences files; read only within an explicit Agent Native Sync invocation.

→ [Read more about the Agent Module](agent/agent.md)



<br>

<!--------------------------------------------------------------------------------- Config --->
## Config

Config is the separate shared operational boundary for the generated records that coordinate the Workflow. It is outside the Foundation directory and is the only writable area of the Interface for authorized Skills.

Responsibility: Holds the generated Application, State, Plan, and Review records; each record remains owned and writable only under its owning Component's authority.

- **Application Config** — shared public metadata that lets Components discover and compose one another. [Read more about Application Config](config/application.yaml)
- **State Config** — current Workflow position, phase progress, outcomes, Blockers, Open Questions, and History. [Read more about State Config](config/state.yaml)
- **Plan Config** — Plans, Groups, Tasks, dependencies, completion conditions, and planning progress. [Read more about Plan Config](config/plan.yaml)
- **Review Config** — review outcomes, Findings, evidence, assurance results, and Finding status. [Read more about Review Config](config/review.yaml)

<br>

<!--------------------------------------------------------------------------------- Foundation Files --->
## Foundation Files

Foundation Files are the shared resources every Module and Skill depends on: the section files of this Interface and the Schemas that shape authored and generated files. The Config records that coordinate the Workflow are a separate shared operational boundary, not part of the Foundation directory and not a Module.

Responsibility: Explains the Foundation directory and maps the Interface section files, shared Config records, and every Schema; Config records remain owned by Plan, State, and Review.

→ [Read more about Foundation Files](foundation/foundation.md)



<br>

<!--------------------------------------------------------------------------------- Understanding --->
## Understanding

Understanding is the current context an Agent Native or Agent Instance establishes from authoritative sources before performing a Skill's role: Interface Understanding starts from this file and its linked Foundation files, Target Understanding from the two Target definitions, and only Agent Sync may enter the Agent Module.

Responsibility: Defines Interface Understanding and Target Understanding, their sources, precedence, and the Agent Module exception; part of every Skill's required Interface Understanding.

→ [Read more about Understanding](foundation/understanding.md)



<br>

<!--------------------------------------------------------------------------------- Authority and Ownership --->
## Authority and Ownership

Authority and Ownership state who owns each record (Human, Plan, State, Review) and which Skill may change it; the complete `.interface/` tree is read-only except for authorized Config records.

Responsibility: Defines record ownership and every Skill's write authority, including the read-only rule for the Interface tree; part of every Skill's required Interface Understanding.

→ [Read more about Authority and Ownership](foundation/authority.md)



<br>

<!--------------------------------------------------------------------------------- Workflow --->
## Workflow

Workflow is the ordered path from Target definition to running software — Define Target, Configure, Plan, Develop, Review, Launch — followed through the Default, Normal, or Detailed path.

Responsibility: Defines the Workflow and the Default, Normal, and Detailed invocation paths; part of every Skill's required Interface Understanding.

→ [Read more about Workflow](foundation/workflow.md)
