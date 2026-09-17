# Agent Interface

<br><br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

Use this document as the entry point and follow its sections in this order:

1. **[Introduction](#introduction)** — understand the purpose, workflow, independence, and boundaries of Agent Interface.
2. **[Terminology](#terminology)** — learn the shared vocabulary used throughout the Interface.
3. **[Architecture](#architecture)** — see the high-level structure and its primary sections.
4. **[Modules](#modules)** — locate the three primary conceptual boundaries of the Interface.
   - **[Target](#target)** — understand what is being built through its non-technical and technical definitions.
   - **[Implementation](#implementation)** — understand the engineering philosophy through Components and their Principles and Implementation Preferences.
   - **[Agent](#agent)** — understand the executing system, its capabilities, restrictions, and Skills.
5. **[Foundation Files](#foundation-files)** — locate the Interface document, Config, and shared Schema definitions.
6. **[Understanding](#understanding)** — distinguish knowledge of Agent Interface from knowledge of the current Target.
7. **[Operations](#operations)** — understand the one-to-one actions performed through every Interface-owned Skill.
8. **[Modes](#modes)** — understand the operational positions recorded by State.
9. **[Authority and Ownership](#authority-and-ownership)** — understand who owns each record and which Skill may change it.
10. **[Workflow](#workflow)** — choose Default, Normal, or Detailed control while following the path from Target definition through launch.


<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction
<!-------------------------- Overview -->
### Overview

**Agent Interface** is a implementation-oriented interface for AI-assisted software development.

The core idea is to create a structured layer between a **Implementation**, an **AI Agent**, and a **Target** so that software can be understood, planned, developed, configured, and reviewed according to a consistent set of concepts.

The Interface is not intended to be tied to:

- one specific AI model,
- one specific coding agent,
- one specific implementation,
- or one specific software project.

Instead, these concepts are intentionally separated.

A different **Target** can be provided without changing the Implementation or Agent definitions.

A different **Implementation** can provide a different programming philosophy without changing the Target.

A different **Agent** can execute the same Interface using its own native capabilities.

The long-term implementation may eventually use technologies such as skills, MCP, hooks, plugins, memory systems, multiple agents, tools, or other future agent capabilities.

Those technologies are implementation mechanisms.

The primary concern of the Interface is the **conceptual contract** between the Implementation, Agent, and Target.

<!-------------------------- Purpose -->
### Purpose

Agent Interface is an independent interface between **Humans** and **AI Agents** for establishing a common protocol, structure, and standard for software development.

Its purpose is to let a Human define a Target in natural language, provide common Implementation Principles and Preferences for planning and developing it, and define a portable Agent Module that explicit Agent Sync realizes in the active Runtime.

<!-------------------------- How It Works -->
### How It Works

The Human states the Target in the Non-Technical Definition. Acting as the implementation, the Human translates that intent into the Technical Definition without changing its meaning. Skills then read the current sources required by their role before acting. Planning records activities as Tasks; Development implements and verifies those Tasks; Review evaluates the result; and Launch brings the completed Target online. Mechanical actions such as Config initialization do not interpret the Target.

Config contains only the mutable operational records used to coordinate this work. Schemas define their storage format.

<!-------------------------- Independence -->
### Independence

The core Interface Structure is independent of any specific AI model, Agent Native, or external execution capability. Portable Contracts for Interface-owned Skills belong to the Agent Module, while their self-contained native implementations remain outside `.interface/` as synchronized Runtime adapters. External Skills remain provider-owned capabilities declared by the Agent Profile. Only explicit Agent Sync reads Agent Module sources; every other Runtime operation consumes their last synchronized realization.

Human project definitions remain flexible, while the Interface gives Agents stable responsibilities, rules, defaults, and operational records. Agent Interface is the communication boundary between those two forms.

<!-------------------------- Core Idea -->
### Core Idea

Modern AI coding agents can generate and modify software, but an agent still needs to understand several independent things before it can reliably act:

1. **What is being built?**
2. **How does the implementation want software to be built?**
3. **What agent is performing the work and what capabilities or restrictions does it have?**
4. **What Mode or supporting action is currently active?**

Agent Interface gives these concerns explicit structure.

Conceptually:

```text
Target ─────┐
Implementation ──┼── together with Understanding, Modes, and Workflow ──> Implementation
Agent ──────┘
```

The resulting software is therefore influenced by all three primary entities:

```text
Target
   +
Implementation
   +
Agent
   ↓
Execution
```


<!-------------------------- Design Goals -->
### Design Goals

The Interface should make the following substitutions possible without redesigning the entire system:

```text
Target A     → Target B
Implementation A  → Implementation B
Agent A      → Agent B
```

Changing one should not unnecessarily redefine the others.

This separation is one of the central architectural principles of the project.





<br><br>

<!--------------------------------------------------------------------------------- Terminology --->
## Terminology

- **Interface** — the complete system described by this document; it contains the Target, Implementation, and Agent Modules together with Understanding, Operations, Foundation Files, Modes, Authority, and Workflow.
- **Human** — the person who defines the Target and owns every authored Interface source.
- **Module** — a primary conceptual boundary with a distinct responsibility inside the Interface. Target, Implementation, and Agent are the Interface Modules.
- **Target** — the application, platform, service, API, module, package, subsystem, or other development subject the Interface works on. The term is preferred over Target Project because the subject does not have to be an entire project.
- **Implementation** — the implementation's reusable programming philosophy and engineering perspective, independent of a particular Target or Agent.
- **Agent** — an AI coding system or execution unit that interacts with the Interface and maps its concepts to native capabilities.
- **Component** — one named part of the Implementation or Agent Module perspective that owns a responsibility and is described through Principles together with Implementation Preferences or an Agent Profile; some Implementation Components also own operational records.
- **Implementation Module** — the Module that defines the reusable programming philosophy, Principles, Preferences, and Component composition applied to a Target.
- **Implementation Component** — one independent Component inside the Implementation Module with a defined responsibility, Public Interface, Principles, and Implementation Preferences.
- **Logic Component** — the reusable library Component that implements application Behaviour and publishes a Public Logic Interface.
- **API Component** — the executable Component that starts the API process, owns transport concerns, and invokes Logic through its Public Interface.
- **Presentation Component** — the executable Component that presents the application to users and consumes the API Component.
- **Public Logic Interface** — the provider-owned public library surface through which API invokes application Behaviour.
- **API Contract** — the public description of API operations, transport schemas, versions, and approved outcomes.
- **Technical Purpose** — a language-level use such as modeling, API delivery, database access, ORM, or migration that may be shared by compatible Components.
- **Principles** — mandatory portable philosophy, responsibilities, rules, and boundaries owned by an Implementation or Agent Component.
- **Implementation Preferences** — preferred engineering choices, defaults, packages, implementation conventions, and optional Agent Skill associations used when the Target leaves a choice unspecified.
- **Schema** — the structure a file follows: either a standard for a Human-authored file or an operational format and initial template for a generated record.
- **Config** — mutable operational records that coordinate the Workflow and record where work stands; Config does not store what the Target means.
- **Plan** — the high-level organization of work, containing Groups, dependencies, and individual Tasks.
- **Task** — one bounded, understandable, and verifiable unit of work within a Plan.
- **Understanding** — the current context an Agent Native or Agent Instance establishes from authoritative sources before performing a Skill's role; it is either about Agent Interface itself or about the active Target.
- **Operation** — one defined action performed through an Agent Skill to configure, plan, develop, review, launch, implement, or reset work.
- **Workflow** — the ordered path from the Human's Target definition to running software: Define Target, Configure, Plan, Develop, Review, and Launch.
- **Workflow Path** — the Human's selected level of direct orchestration over that same Workflow: Default, Normal, or Detailed; it is an invocation style, not a State Mode.
- **Mode** — an operational position in the Workflow, recorded by State.
- **Skill** — an Agent capability that performs a Workflow action or provides a supporting utility; it is part of the Agent Module's integration surface, while its implementation remains outside `.interface/`.
- **Agent Module** — the Human-owned, Runtime-independent declaration of how an Agent Native and its Agent Instances must operate. Bare `Agent` is never used as a substitute for this term.
- **Agent Native** — the core operational Agent supplied by the selected Agent Runtime and currently responsible for receiving the Human's request, applying synchronized Agent Module behavior, and hosting or coordinating Agent Instances.
- **Agent Instance** — one primary or specialized executable identity operating within an Agent Native, with an assigned Agent Role and bounded capabilities. One Agent Native may expose several Agent Instances.
- **Agent Profile** — the complete portable declaration of Agent Components and their current selections, resources, empty categories, portable realization requirements, and validation expectations; Native-specific paths and formats are resolved by Agent Sync.
- **Agent Role** — one bounded execution responsibility within the Agent Profile, including the primary role and specialized delegated roles.
- **Capability** — one declared Agent facility, such as a Skill, Rule, Command, Tool, Hook, Integration, or Extension, with an owning Component and bounded contract.
- **Capability Realization Kind** — how a declared Agent capability becomes usable in the active Runtime: **Constructed**, built by the Agent Native from a portable specification such as a Skill Contract; **Prepared**, transferred into the Runtime unchanged from a complete Human-authored artifact; or **Installed**, provisioned by the Agent Native's own native mechanism from an external source such as a marketplace, package registry, or MCP server, using per-Agent-Native identity so the Native can find and install it.





<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

The current conceptual architecture is:

```text
Architecture
│
├── Modules
│   ├── Target
│   ├── Implementation
│   └── Agent
├── Foundation Files
├── Understanding
├── Operations
├── Modes
├── Authority and Ownership
└── Workflow
```

Each Module owns one Structure that shows its concepts together with their repository files. Understanding establishes the context used by a Skill, Operations define the actions Skills perform, Foundation Files remain shared resources, Modes record operational position, Authority and Ownership control writes, and Workflow defines execution order.



<br><br>

<!--------------------------------------------------------------------------------- Modules --->
## Modules

Target, Implementation, and Agent are the three primary Modules of Agent Interface. Each Module owns a distinct responsibility and documents one combined conceptual and repository Structure.

<!-------------------------- Target -->
### Target

The Target describes **what the Interface is working on**, through a Human Definition and a Technical Definition that takes precedence on conflict.

```yaml
name: Target Module Guide
path: .interface/target/guide.md
responsibility: Explains the Target Module and maps its files; the Understanding sources remain the two definition files it points to
```

→ [Target Module Guide](target/guide.md)

<!-------------------------- Implementation -->
### Implementation

The Implementation Module defines the reusable programming personality, standards, and engineering perspective applied to a Target through its ten Components.

```yaml
name: Implementation Module Guide
path: .interface/implementation/guide.md
responsibility: Explains the Implementation Module and maps every Component's Principles and Preferences; each Component's Principles remain the authority
```

→ [Implementation Module Guide](implementation/guide.md)

<!-------------------------- Agent -->
### Agent

The Agent Module is the Human-owned, Runtime-independent declaration of how an Agent Native and its Agent Instances must operate, realized in the selected Runtime only through explicit Agent Sync; only Agent Sync and Skill Installer enter it, and every other role uses the synchronized Runtime realization.

```yaml
name: Agent Module Guide
path: .interface/agent/guide.md
responsibility: Explains the Agent Module and maps every Component's Principles, Profile, and definition files; read only within an explicit Agent Sync or Skill Installer invocation
```

→ [Agent Module Guide](agent/guide.md)



<br><br>

<!--------------------------------------------------------------------------------- Foundation Files --->
## Foundation Files

Foundation Files are the shared resources every Module and Skill depends on: the section files of this Interface, the Config records that coordinate the Workflow, and the Schemas that shape authored and generated files. They are not a Module.

```yaml
name: Foundation Guide
path: .interface/foundation/guide.md
responsibility: Explains the Foundation directory and maps the Interface section files, every Config record, and every Schema; Config records remain owned by Plan, State, and Review
```

→ [Foundation Guide](foundation/guide.md)



<br><br>

<!--------------------------------------------------------------------------------- Understanding --->
## Understanding

Understanding is the current context an Agent Native or Agent Instance establishes from authoritative sources before performing a Skill's role: Interface Understanding starts from this file and its linked Foundation files, Target Understanding from the two Target definitions, and only Agent Sync may enter the Agent Module.

```yaml
name: Understanding
path: .interface/foundation/understanding.md
responsibility: Defines Interface Understanding and Target Understanding, their sources, precedence, and the Agent Module exception; part of every Skill's required Interface Understanding
```

→ [Understanding](foundation/understanding.md)



<br><br>

<!--------------------------------------------------------------------------------- Operations --->
## Operations

Operations are the defined actions performed through the nine Interface-owned Skills — Configure, Planning, Developing, Reviewing, Launch, Implement, Reset, Skill Installer, and Agent Sync — each with exactly one Skill and one summarized outcome.

```yaml
name: Operations
path: .interface/foundation/operations.md
responsibility: Defines every Operation, its Skill entry point, and the outcome that Skill is responsible for; part of every Skill's required Interface Understanding
```

→ [Operations](foundation/operations.md)



<br><br>

<!--------------------------------------------------------------------------------- Modes --->
## Modes

Modes are the operational positions recorded by State — Not Set, Configuring, Planning, Development — each with its responsibility, inputs, and output.

```yaml
name: Modes
path: .interface/foundation/modes.md
responsibility: Defines every Mode State may record, with its responsibility, inputs, and output; part of every Skill's required Interface Understanding
```

→ [Modes](foundation/modes.md)



<br><br>

<!--------------------------------------------------------------------------------- Authority and Ownership --->
## Authority and Ownership

Authority and Ownership state who owns each record (Human, Plan, State, Review) and which Skill may change it; the complete `.interface/` tree is read-only except for authorized Config records.

```yaml
name: Authority and Ownership
path: .interface/foundation/authority.md
responsibility: Defines record ownership and every Skill's write authority, including the read-only rule for the Interface tree; part of every Skill's required Interface Understanding
```

→ [Authority and Ownership](foundation/authority.md)



<br><br>

<!--------------------------------------------------------------------------------- Workflow --->
## Workflow

Workflow is the ordered path from Target definition to running software — Define Target, Configure, Plan, Develop, Review, Launch — followed through the Default, Normal, or Detailed path.

```yaml
name: Workflow
path: .interface/foundation/workflow.md
responsibility: Defines the Workflow and the Default, Normal, and Detailed invocation paths; part of every Skill's required Interface Understanding
```

→ [Workflow](foundation/workflow.md)



<br><br>

