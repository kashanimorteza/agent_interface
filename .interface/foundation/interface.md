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

The Target describes **what the Interface is working on**, through a Human Definition and a Technical Definition that takes precedence on conflict. Its structure and files are in the [Target Module Guide](../target/guide.md).

```yaml
name: Target Module Guide
path: .interface/target/guide.md
responsibility: Explains the Target Module and maps its files; the Understanding sources remain the two definition files it points to
```

<!-------------------------- Implementation -->
### Implementation

The Implementation Module defines the reusable programming personality, standards, and engineering perspective applied to a Target through its ten Components. Its philosophy, Component structure, and every Component's files are in the [Implementation Module Guide](../implementation/guide.md).

```yaml
name: Implementation Module Guide
path: .interface/implementation/guide.md
responsibility: Explains the Implementation Module and maps every Component's Principles and Preferences; each Component's Principles remain the authority
```

<!-------------------------- Agent -->
### Agent

The Agent Module is the Human-owned, Runtime-independent declaration of how an Agent Native and its Agent Instances must operate, realized in the selected Runtime only through explicit Agent Sync; only Agent Sync and Skill Installer enter it, and every other role uses the synchronized Runtime realization. Its philosophy, Component structure, and every Component's files are in the [Agent Module Guide](../agent/guide.md).

```yaml
name: Agent Module Guide
path: .interface/agent/guide.md
responsibility: Explains the Agent Module and maps every Component's Principles, Profile, and definition files; read only within an explicit Agent Sync or Skill Installer invocation
```



<br><br>

<!--------------------------------------------------------------------------------- Foundation Files --->
## Foundation Files

Foundation Files are the shared resources every Module and Skill depends on: this Interface file, the Config records that coordinate the Workflow, and the Schemas that shape authored and generated files. They are not a Module. Their structure and every file's responsibility are in the [Foundation Guide](guide.md).

```yaml
name: Foundation Guide
path: .interface/foundation/guide.md
responsibility: Explains the Foundation directory and maps the Interface file, every Config record, and every Schema; Config records remain owned by Plan, State, and Review
```



<br><br>

<!--------------------------------------------------------------------------------- Understanding --->
## Understanding

Understanding is the current context an Agent Native or Agent Instance establishes before performing a Skill's role. Interface Understanding is required by every Skill and starts exclusively from this canonical Interface file. For every operation except Agent Sync, the Interface routes the Skill only to applicable Target, Implementation, Foundation, Config, and synchronized Runtime resources; seeing the Agent Structure in the Agent Module Guide never authorizes entry into the Agent Module. Target Understanding is separate and, when the role needs Target meaning, is established from both Human Definition and Technical Definition under Target's declared precedence. Configure uses only the phase identities and Platform selections required for its role; Reset establishes the minimum Target Understanding needed for a phase scope, omits it for Config scope, and uses only phase identity and ownership for Complete scope. Agent Sync alone may follow the Agent Structure into Agent Module sources and does so only after explicit Human invocation.

- **Interface Understanding:** Read `.interface/foundation/interface.md` as the sole Foundation Source, then follow only the non-Agent-Module routes it provides for the active role. Agent Sync is the sole explicit exception.
- **Target Understanding:** When required, read both Target definitions located by the Interface. Human Definition provides the Human's stated intent and context; Technical Definition is the primary Target authority and takes precedence wherever they conflict.

```text
Understanding Structure
├── Interface Understanding
│   └── Interface Foundation Source → .interface/foundation/interface.md
└── Target Understanding
    ├── Human Definition    → .interface/target/non-technical.md
    └── Technical Definition → .interface/target/technical.md
```

Understanding uses these authoritative sources:

- [Interface Foundation Source](interface.md)
- [Non-Technical Definition](../target/non-technical.md)
- [Technical Definition](../target/technical.md)

An empty Human Definition contributes no information. Understanding is reconstructed from both current sources under their declared precedence when required and is never copied into Config as a second project definition.

<br><br>

<!--------------------------------------------------------------------------------- Operations --->
## Operations

Operations are the defined actions performed through Interface-owned Skills. Every Interface-owned Skill has exactly one corresponding Operation; the Operation names its Skill and summarizes the outcome that Skill is responsible for. An Operation remains separate from the Mode recorded while work is in progress, and external provider Skills do not create Interface Operations.

```text
Operations
├── Configure
├── Planning
├── Developing
├── Reviewing
├── Launch
├── Implement
├── Reset
├── Skill Installer
└── Agent Sync
```

<!-------------------------- Configure Operation -->
### Configure

**Agent Skill:** `/my-interface-configure`

This Operation is performed through `/my-interface-configure` to initialize and reconcile operational Config, synchronize phase State, resolve and install applicable Implementation and Platform technical requirements with concrete versions, and prepare the selected Platform Environment.

A Skill named by an `agent_skills` association reaches the Runtime through its ecosystem's own provisioning mechanism when the environment is prepared, and through Configure when Configure prepares the project. Planning, Developing, and every other operation use such a Skill when it is discoverable and usable, and never install it. The separation exists because a package-provided Skill cannot exist before its package does, and because provisioning one never makes it an Agent Module declaration.

<!-------------------------- Planning Operation -->
### Planning

**Agent Skill:** `/my-interface-planning`

This Operation is performed through `/my-interface-planning` to convert the current Target and applicable Implementation guidance into bounded, understandable, and verifiable Tasks.

<!-------------------------- Developing Operation -->
### Developing

**Agent Skill:** `/my-interface-developing`

This Operation is performed through `/my-interface-developing [phase-number ...]` to implement and verify eligible Tasks from a valid current Plan. Review evaluates the resulting implementation afterward.

<!-------------------------- Reviewing Operation -->
### Reviewing

**Agent Skill:** `/my-interface-reviewer`

This Operation is performed through `/my-interface-reviewer [phase-number ...]` to assure each selected phase's Plan against current Interface and Target Understanding, coordinate Planning and independently recheck it when reconciliation is required, and then evaluate existing implementation without repairing it. With no phase input, it reviews every enabled phase.

<!-------------------------- Launch Operation -->
### Launch

**Agent Skill:** `/my-interface-launch`

This Operation is performed through `/my-interface-launch [api|logic|presentation|complete|all]` to read the selected Launch definition and its Component Runtime Requirements, start only the requested scope (or all developed parts for `complete`/`all`), verify readiness, and report access points. When no scope is supplied, the Launch Skill asks the Human to choose one.

<!-------------------------- Implement Operation -->
### Implement

**Agent Skill:** `/my-interface-implement`

This Operation is performed through `/my-interface-implement [phase-number ...]` to execute Configure once, then Planning, Developing, and Review for each selected phase in Target order, advancing only after the phase is satisfied, and finally perform eligible Launch. With no phase input, it processes every enabled and ready phase.

<!-------------------------- Reset Operation -->
### Reset

**Agent Skill:** `/my-interface-reset`

This Operation is performed through `/my-interface-reset [phase-number ...]` to reset selected phases; with no phase input it resets every phase with generated work. `/my-interface-reset config` physically removes only operational Config files, while `/my-interface-reset complete` physically removes those Config files and the implementation outputs of all phases. Emptying or reinitializing a Config file is not removal. Every mode previews its exact impact and requires separate Human confirmation before mutation.

<!-------------------------- Skill Installer Operation -->
### Skill Installer

**Agent Skill:** `/my-interface-skill-installer`

This Operation is performed through `/my-interface-skill-installer` to derive Agent capability needs, discover compatible project-scoped candidates, obtain Human approval, provision only approved capabilities, and verify their activation.

<!-------------------------- Agent Sync Operation -->
### Agent Sync

**Agent Skill:** `/my-interface-agent-sync <self | module>`

This Operation is performed only through explicit Human invocation of `/my-interface-agent-sync` in one of two modes: `self` realizes the Agent Sync adapter itself from its current Contract, and `module` realizes every other declaration. It is the sole operation permitted to inspect Agent Module sources, understands the complete Module and the selected Agent Native's own conventions, translates the Module into that Native Runtime, and certifies synchronization only after all required declarations pass post-change verification and no non-Sync Runtime instruction routes back into the Agent Module.

Agent Sync works only between the Agent Module and the Agent Native, so it needs no Target Understanding and no other Interface Module: it never decides what the product should do, only how the selected Agent Native must be shaped to match the Human's declared view of the Agent. It realizes its own adapter before the rest of the Module because a running adapter cannot load a definition it did not start with.

<br><br>

<!--------------------------------------------------------------------------------- Modes --->
## Modes

State records the active Mode. Modes describe the current operational position and remain distinct from the behaviour required from the Target.

<!-------------------------- Not Set -->
### Not Set

```text
state = not set
responsibility = Represents the initial Workflow position before a Skill action is recorded, or the position restored by Reset
inputs = none
output = Active State with no selected work scope
```

<!-------------------------- Configuring -->
### Configuring

```text
state = configuring
responsibility = Create and reconcile the persistent Application Manifest, reconcile operational Config, synchronize phase State, resolve technical requirements, and prepare the selected Platform requirements
inputs = Operational Schemas, existing Config, Target phase identities, Implementation Preferences, Platform selections, and Platform authorities
output = Persistent Application Manifest, current operational Config, resolved technical selections, and a prepared selected Platform runtime
```

<!-------------------------- Planning -->
### Planning

```text
state = planning
responsibility = Create bounded and verifiable Tasks without prescribing implementation
inputs = Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, and operational records
output = Updated Plan Config
```

<!-------------------------- Development -->
### Development

```text
state = development
responsibility = Implement and verify eligible planned Tasks
inputs = Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, Plan, State, and existing implementation
output = Verified implementation and updated operational records
```


<br><br>

<!--------------------------------------------------------------------------------- Authority and Ownership --->
## Authority and Ownership

Explicit Target intent and applicable Implementation Principles guide operational Skills. Implementation Preferences supply engineering defaults where the Target leaves a choice unstated. Agent Profiles declare desired portable execution capabilities solely for Agent Sync, which learns Native-specific mappings and materializes the synchronized Runtime rules and capabilities consumed by every other Skill. Operational Schemas define the shape of operational records, authored-source Schemas define Principles, Implementation Preferences, and Agent Profiles, and the general YAML Schema supplies their common YAML frame together with Config files. Schema definition files use their own formats. Config stores operational records and does not define the Target.

```text
Target = human-defined intent
Principles = mandatory philosophy, responsibilities, and boundaries
Implementation Preferences = engineering defaults for unspecified Target choices
Agent Profiles = current Agent Module selections, resources, portable realization requirements, and explicit empty categories
Schema = common YAML frame for Implementation Preferences, Agent Profiles, and Config, authored-source structure, and the storage structure of every operational record
Config = the mutable operational records
```

Ownership answers who a record belongs to, and it belongs to the Human or to a Component:

```text
Human = owns Interface, Target, Principles, Implementation Preferences, Agent Profiles, and Schema sources
Plan = owns Plans, Groups, Tasks, their status, and their history
State = owns active Workflow position, aggregate phase progress, Implement and Launch results, operational History, Blockers, and Open Questions
Review = owns recorded Findings and their state
```

Write authority answers which Skill may change a record, and every write happens under the rules of the Component that owns it:

```text
Configure = creates and reconciles the persistent Application Manifest, writes every operational Config, synchronizes phase records, resolves technical requirements, records its State outcome, and prepares the selected Platform runtime
Planning = writes Plans, Groups, and Tasks under Plan, and Planning progress and History under State
Developing = writes implementation and Task status and history under Plan, and Development progress and History under State
Reviewer = writes Findings under Review, and Review progress and History under State
Configure, Planning, and Developing = write the active Workflow position under State
Launch = changes runtime state through Platform and writes Launch State, access points, and History under State
Implement = coordinates operation Skills and writes only Implementation State and its History under State
Reset = after human confirmation of the preview, removes or resets explicit-phase outputs, every generated phase when no phase is supplied, Config only, or the complete set of Config and all-phase implementation outputs, including reconciliation of the Workflow position, under the owning Components' rules
Skill Installer = discovers Agent capabilities and, after approval, provisions only approved project-scoped capabilities outside Interface sources
Agent Sync = on explicit Human invocation, exclusively reads the Agent Module and reconciles its declarations with self-contained project-scoped native Runtime artifacts outside Interface sources
Reviewing, Launch, Implement, Skill Installer, and Agent Sync = do not directly change the active Workflow mode
Every Skill = may record its own Blockers and Open Questions under State's rules when applicable
```

Each Skill writes only the records it has authority over, and always under the rules of the Component that owns them. Operational records follow their source authorities and must not redefine them.

The complete `.interface/` tree is read-only to every Agent Role and Skill by default. The only mutable exception is `.interface/foundation/config/`, and a Skill may change files there only within the write authority stated above and the owning Component's rules. No other Interface path becomes writable because it is added later, discovered by a Tool, or named by a Plan.

<br><br>

<!--------------------------------------------------------------------------------- Workflow --->
## Workflow

### Define the Project

Define the Target before selecting a Workflow Path:

```text
Human Definition = .interface/target/non-technical.md
Technical Definition = .interface/target/technical.md
```

The Human states the intended outcome in Human Definition, then records its corresponding technical definition without changing that intent.

After the Project is defined, select Default, Normal, or Detailed. The path controls only how much of the Workflow the Human invokes directly; it does not change any operation contract or verification gate.

### Default

For the simplest complete run:

```text
/my-interface-implement
```

Implement processes all enabled and ready phases and performs Launch when every required gate is satisfied.

### Normal

For complete orchestration with phase selection:

Run phases separately:

```text
/my-interface-implement 1
/my-interface-implement 2
/my-interface-implement 3
/my-interface-launch
```

Or run several phases together:

```text
/my-interface-implement 1 2 3
/my-interface-launch
```

Launch runs after all required phases are complete.

### Detailed

For direct control over every operation:

```text
/my-interface-configure
/my-interface-planning 1
/my-interface-reviewer 1
/my-interface-developing 1
/my-interface-reviewer 1
Repeat Planning, Developing, and Review for each remaining phase
/my-interface-launch
```

Planning defines the work, Development creates and verifies the implementation, and Review evaluates the resulting Plan coverage and implementation. A phase is reconciled before advancing, and Launch runs only after all required phases satisfy Review.
