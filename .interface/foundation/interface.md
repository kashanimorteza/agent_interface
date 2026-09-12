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
   - **[Developer](#developer)** — understand the engineering philosophy through Components and their Principles and Preferences.
   - **[Agent](#agent)** — understand the executing system, its capabilities, restrictions, and Skills.
5. **[Understanding](#understanding)** — distinguish knowledge of Agent Interface from knowledge of the current Target.
6. **[Operations](#operations)** — understand the actions performed through Configure, Planning, Developing, Reviewing, Launch, Implement, and Reset.
7. **[Modes](#modes)** — understand the operational positions recorded by State.
8. **[Authority and Ownership](#authority-and-ownership)** — understand who owns each record and which Skill may change it.
9. **[Foundation Files](#foundation-files)** — locate the Interface document, Config, and shared Schema definitions.
10. **[Workflow](#workflow)** — follow the path from defining a Target through configuration, planning, development, review, and launch.


<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction
<!-------------------------- Overview -->
### Overview

**Agent Interface** is a developer-oriented interface for AI-assisted software development.

The core idea is to create a structured layer between a **Developer**, an **AI Agent**, and a **Target** so that software can be understood, planned, developed, configured, and reviewed according to a consistent set of concepts.

The Interface is not intended to be tied to:

- one specific AI model,
- one specific coding agent,
- one specific developer,
- or one specific software project.

Instead, these concepts are intentionally separated.

A different **Target** can be provided without changing the Developer or Agent definitions.

A different **Developer** can provide a different programming philosophy without changing the Target.

A different **Agent** can execute the same Interface using its own native capabilities.

The long-term implementation may eventually use technologies such as skills, MCP, hooks, plugins, memory systems, multiple agents, tools, or other future agent capabilities.

Those technologies are implementation mechanisms.

The primary concern of the Interface is the **conceptual contract** between the Developer, Agent, and Target.

<!-------------------------- Purpose -->
### Purpose

Agent Interface is an independent interface between **Humans** and **AI Agents** for establishing a common protocol, structure, and standard for software development.

Its purpose is to let a Human define a Target in natural language and give Agents common Principles and Preferences for planning and developing it.

<!-------------------------- How It Works -->
### How It Works

The Human states the Target in the Non-Technical Definition. Acting as the developer, the Human translates that intent into the Technical Definition without changing its meaning. Skills then read the current sources required by their role before acting. Planning records activities as Tasks; Development implements and verifies those Tasks; Review evaluates the result; and Launch brings the completed Target online. Mechanical actions such as Config initialization do not interpret the Target.

Config contains only the mutable operational records used to coordinate this work. Schemas define their storage format.

<!-------------------------- Independence -->
### Independence

The core Interface Structure is independent of any specific AI model, Agent, or external execution capability. Portable Contracts for Interface-owned Skills belong to the Agent Module, while their native implementations remain outside `.interface/` as runtime adapters. External Skills remain provider-owned capabilities declared by the Agent Profile.

Human project definitions remain flexible, while the Interface gives Agents stable responsibilities, rules, defaults, and operational records. Agent Interface is the communication boundary between those two forms.

<!-------------------------- Core Idea -->
### Core Idea

Modern AI coding agents can generate and modify software, but an agent still needs to understand several independent things before it can reliably act:

1. **What is being built?**
2. **How does the developer want software to be built?**
3. **What agent is performing the work and what capabilities or restrictions does it have?**
4. **What Mode or supporting action is currently active?**

Agent Interface gives these concerns explicit structure.

Conceptually:

```text
Target ─────┐
Developer ──┼── together with Understanding, Modes, and Workflow ──> Implementation
Agent ──────┘
```

The resulting software is therefore influenced by all three primary entities:

```text
Target
   +
Developer
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
Developer A  → Developer B
Agent A      → Agent B
```

Changing one should not unnecessarily redefine the others.

This separation is one of the central architectural principles of the project.





<br><br>

<!--------------------------------------------------------------------------------- Terminology --->
## Terminology

- **Interface** — the complete system described by this document; it contains the Target, Developer, and Agent Modules together with Understanding, Operations, Foundation Files, Modes, Authority, and Workflow.
- **Human** — the person who defines the Target and owns every authored Interface source.
- **Module** — a primary conceptual boundary with a distinct responsibility inside the Interface. Target, Developer, and Agent are the Interface Modules.
- **Target** — the application, platform, service, API, module, package, subsystem, or other development subject the Interface works on. The term is preferred over Target Project because the subject does not have to be an entire project.
- **Developer** — the developer's reusable programming philosophy and engineering perspective, independent of a particular Target or Agent.
- **Agent** — an AI coding system or execution unit that interacts with the Interface and maps its concepts to native capabilities.
- **Component** — one named part of the Developer or Agent perspective that owns a responsibility and is described through its Principles and Preferences; some Developer Components also own operational records.
- **Principles** — mandatory philosophy, responsibilities, rules, and boundaries that describe how the Developer believes software should fundamentally be designed.
- **Preferences** — preferred choices and defaults used when multiple valid implementations exist and the Target leaves the choice unspecified.
- **Schema** — the structure a file follows: either a standard for a Human-authored file or an operational format and initial template for a generated record.
- **Config** — mutable operational records that coordinate the Workflow and record where work stands; Config does not store what the Target means.
- **Plan** — the high-level organization of work, containing Groups, dependencies, and individual Tasks.
- **Task** — one bounded, understandable, and verifiable unit of work within a Plan.
- **Understanding** — the current context an Agent establishes from authoritative sources before performing a Skill's role; it is either about Agent Interface itself or about the active Target.
- **Operation** — one defined action performed through an Agent Skill to configure, plan, develop, review, launch, implement, or reset work.
- **Workflow** — the ordered path from the Human's Target definition to running software: Define Target, Configure, Plan, Develop, Review, and Launch.
- **Mode** — an operational position in the Workflow, recorded by State.
- **Skill** — an Agent capability that performs a Workflow action or provides a supporting utility; it is part of the Agent Module's integration surface, while its implementation remains outside `.interface/`.
- **Agent Profile** — the complete portable declaration of Agent Components and their current selections, resources, empty categories, native mappings, and validation expectations.
- **Agent Role** — one bounded execution responsibility within the Agent Profile, including the primary role and specialized delegated roles.
- **Capability** — one declared Agent facility, such as a Skill, Rule, Command, Tool, Hook, Integration, or Extension, with an owning Component and bounded contract.





<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

The current conceptual architecture is:

```text
Architecture
│
├── Modules
│   ├── Target
│   ├── Developer
│   └── Agent
├── Understanding
├── Operations
├── Modes
├── Authority and Ownership
├── Foundation Files
└── Workflow
```

Each Module owns one Structure that shows its concepts together with their repository files. Understanding establishes the context used by a Skill, Operations define the actions Skills perform, Foundation Files remain shared resources, Modes record operational position, Authority and Ownership control writes, and Workflow defines execution order.



<br><br>

<!--------------------------------------------------------------------------------- Modules --->
## Modules

Target, Developer, and Agent are the three primary Modules of Agent Interface. Each Module owns a distinct responsibility and documents one combined conceptual and repository Structure.

<!-------------------------- Target -->
### Target

The Target describes **what the Interface is working on**.

The Target is defined through two complementary, human-owned sources:

- **Non-Technical Definition:** The Human's initial statement of intent, context, and requirements without requiring technical formulation; an empty file contributes no information.
- **Technical Definition:** The Human, acting as the developer, translates the Non-Technical Definition into this technical form. It is the primary authority for the Target and takes precedence wherever the two definitions conflict.

#### Structure

```text
Target
├── Non-Technical Definition
│   └── .interface/target/non-technical.md
└── Technical Definition
    └── .interface/target/technical.md
```

#### Phase Control

The Technical Definition divides the Target into ordered phases. Every phase has a stable `id`, a `status` controlling scope, and a `readiness` controlling whether its design is ready to implement:

```text
Enabled  = the phase is in scope; it is planned, developed, and reviewed in its defined order
Disabled = the phase is out of scope; no Plan, Task, or Finding is created for it, while its
           aggregate State identity may remain available without implying progress
Ready = the phase may be implemented
Designing = the phase is still being designed and is not yet implementable
Not Designed = the phase has not entered design and is not implementable
```

A phase is implementable only when it is both `Enabled` and `Ready`. These values express human intent, never operational progress. Planning, Development, and Review progress is recorded in State and never written into Target.

<!-------------------------- Developer -->
### Developer

The Developer module defines the reusable programming personality, standards, and engineering perspective applied to a Target. It expresses them through the Development, Model, Database, Backend, Frontend, Platform, Plan, Review, and State Components.

Each Component states its mandatory philosophy, responsibilities, and boundaries through Principles, and its preferred technical choices and defaults through Preferences.

#### Structure

```text
Developer
└── Components
    ├── Development
    │   ├── Principles  → .interface/developer/development/principles.md
    │   └── Preferences → .interface/developer/development/preferences.yaml
    ├── Model
    │   ├── Principles  → .interface/developer/model/principles.md
    │   └── Preferences → .interface/developer/model/preferences.yaml
    ├── Database
    │   ├── Principles  → .interface/developer/database/principles.md
    │   └── Preferences → .interface/developer/database/preferences.yaml
    ├── Backend
    │   ├── Principles  → .interface/developer/backend/principles.md
    │   └── Preferences → .interface/developer/backend/preferences.yaml
    ├── Frontend
    │   ├── Principles  → .interface/developer/frontend/principles.md
    │   └── Preferences → .interface/developer/frontend/preferences.yaml
    ├── Platform
    │   ├── Principles  → .interface/developer/platform/principles.md
    │   └── Preferences → .interface/developer/platform/preferences.yaml
    ├── Plan
    │   ├── Principles  → .interface/developer/plan/principles.md
    │   └── Preferences → .interface/developer/plan/preferences.yaml
    ├── Review
    │   ├── Principles  → .interface/developer/review/principles.md
    │   └── Preferences → .interface/developer/review/preferences.yaml
    └── State
        ├── Principles  → .interface/developer/state/principles.md
        └── Preferences → .interface/developer/state/preferences.yaml
```

<!-------------------------- Developer Components -->
#### Components

```text
Development = Defines the layered architecture and how independent layers are composed into one system
Model       = Describes the domain entities and provides one shared logical meaning for domain data
Database    = Owns the persistence layer and publishes one generic interface for reading and writing
Backend     = Executes application Behaviour and publishes the application's API
Frontend    = Presents the application to users and consumes the capabilities Backend publishes
Platform    = Prepares a completed Target for operation and brings it online
Plan        = Turns phases into bounded, verifiable activities organized as Plans, Groups, and Tasks
Review      = Establishes whether implemented work satisfies what was asked, and records what it found
State       = Records active position, aggregate phase progress, implementation, launch, History, Blockers, and Open Questions
```

Each line names a Component so that a phase target can be resolved to its owner. The Component's own Principles remain the authority: when this summary and a Component's Principles disagree, the Principles are correct.


<!-------------------------- Agent -->
### Agent
The Agent module defines the execution side of Agent Interface through Components. Each Agent Component owns one responsibility and has Principles for its mandatory portable contract and Preferences for its current choices, resources, native mappings, and explicit empty categories.

Together, these Components form the Agent Profile. A different Agent Runtime reads the same Profile and maps it to native capabilities without requiring the Target or Developer modules to be redesigned.

#### Structure

```text
Agent
├── Runtime
│   ├── Principles  → .interface/agent/runtime/principles.md
│   └── Preferences → .interface/agent/runtime/preferences.yaml
├── Settings
│   ├── Principles  → .interface/agent/settings/principles.md
│   └── Preferences → .interface/agent/settings/preferences.yaml
├── Context
│   ├── Principles  → .interface/agent/context/principles.md
│   └── Preferences → .interface/agent/context/preferences.yaml
├── Role
│   ├── Principles  → .interface/agent/role/principles.md
│   └── Preferences → .interface/agent/role/preferences.yaml
├── Coordination
│   ├── Principles  → .interface/agent/coordination/principles.md
│   └── Preferences → .interface/agent/coordination/preferences.yaml
├── Skill
│   ├── Principles  → .interface/agent/skill/principles.md
│   ├── Preferences → .interface/agent/skill/preferences.yaml
│   └── Contracts   → .interface/agent/skill/contracts/<interface-owned-skill>.md
├── Command
│   ├── Principles  → .interface/agent/command/principles.md
│   └── Preferences → .interface/agent/command/preferences.yaml
├── Rule
│   ├── Principles  → .interface/agent/rule/principles.md
│   └── Preferences → .interface/agent/rule/preferences.yaml
├── Tool
│   ├── Principles  → .interface/agent/tool/principles.md
│   └── Preferences → .interface/agent/tool/preferences.yaml
├── Hook
│   ├── Principles  → .interface/agent/hook/principles.md
│   └── Preferences → .interface/agent/hook/preferences.yaml
├── Integration
│   ├── Principles  → .interface/agent/integration/principles.md
│   └── Preferences → .interface/agent/integration/preferences.yaml
├── Extension
│   ├── Principles  → .interface/agent/extension/principles.md
│   └── Preferences → .interface/agent/extension/preferences.yaml
├── Interaction
│   ├── Principles  → .interface/agent/interaction/principles.md
│   └── Preferences → .interface/agent/interaction/preferences.yaml
├── Permission
│   ├── Principles  → .interface/agent/permission/principles.md
│   └── Preferences → .interface/agent/permission/preferences.yaml
├── Session
│   ├── Principles  → .interface/agent/session/principles.md
│   └── Preferences → .interface/agent/session/preferences.yaml
└── Observability
    ├── Principles  → .interface/agent/observability/principles.md
    └── Preferences → .interface/agent/observability/preferences.yaml
```

The Agent Components are read in the order shown. When the active role uses an Interface-owned Skill, its portable Contract is read after Skill Principles and Preferences. An external Skill is read from its declared provider resource under the active Role and applicable Agent Principles. A later Component may consume an earlier one but never becomes its second authority. Every supported category remains represented even when its Preferences entries are empty, so absence is explicit rather than indistinguishable from omission. Runtime-specific implementation remains outside the Interface and is only an adapter and evidence that the Profile has been realized.


#### Agent Components

```text
Runtime        = Runtime identity, provider, model, compatibility, and native capability mapping
Settings       = Configuration sources, scopes, precedence, merge behavior, environment, and reconciliation
Context        = Persistent instructions, Understanding, Memory, imports, loading, and compaction
Role           = Primary and specialized Agent Role contracts
Coordination   = Delegation, teams, tasks, messaging, concurrency, and worktree isolation
Skill          = Reusable knowledge and workflows, including core, supporting, and contextual Skills
Command        = Named and slash invocation entry points, arguments, aliases, and routing
Rule           = Persistent global and scoped behavioral instructions
Tool           = Atomic built-in and externally provided executable capabilities
Hook           = Deterministic event-driven lifecycle automation
Integration    = MCP, LSP, channels, application connectors, and external services
Extension      = Plugins, marketplaces, capability packages, monitors, and extension lifecycle
Interaction    = Output Styles, progress, prompts, status presentation, artifacts, themes, and UI behavior
Permission     = Authorization, allow/ask/deny, sandboxing, trust, authentication, and secrets
Session        = Lifecycle, resume, history, background work, isolation, checkpoints, and termination
Observability  = Validation, status, diagnostics, evidence, logs, telemetry, health, and usage
```

Every Agent Component's Principles and Preferences are authoritative for that Component only. A runtime artifact not declared in the owning Preferences is optional runtime capability; a required declaration not usable by the selected runtime is an Agent Profile gap.

<br><br>

<!--------------------------------------------------------------------------------- Understanding --->
## Understanding

Understanding is the current context an Agent establishes before performing a Skill's role. Interface Understanding is required by every Skill and starts exclusively from this canonical Interface file. The Interface then routes the Skill to the Component authorities required by its role; the Agent never needs prior knowledge of the Interface's internal directory structure. Target Understanding is separate and is established from the Target Technical Definition only when the role needs Target meaning. Configure uses only the phase identities and Platform selections required for its role; Reset may omit Target Understanding when its fixed scope does not require it.

- **Interface Understanding:** Read `.interface/foundation/interface.md` as the sole Foundation Source, then follow only the routes it provides for the active role.
- **Target Understanding:** When required, read the Technical Definition located by the Interface to understand the Target's current intent, scope, phases, and project-specific decisions.

<!-------------------------- Understanding Structure -->
### Structure

```text
Understanding
├── Interface Understanding
│   └── Interface Foundation Source → .interface/foundation/interface.md
└── Target Understanding
    └── Target Technical Definition → .interface/target/technical.md
```

The Non-Technical Definition is the Human's input to defining the Technical Definition; it is not a direct operational Understanding source for Skills. Understanding is reconstructed from current sources when required and is never copied into Config as a second project definition.

<br><br>

<!--------------------------------------------------------------------------------- Operations --->
## Operations

Operations are the defined actions that Skills perform through Agent Interface. Each Operation has a distinct responsibility and remains separate from the Mode recorded while work is in progress.

```text
Operations
├── Configure
├── Planning
├── Developing
├── Reviewing
├── Launch
├── Implement
└── Reset
```

<!-------------------------- Configure Operation -->
### Configure

**Agent Skill:** `configure`

Initializes and reconciles operational Config, synchronizes phase State, and prepares the selected Platform Environment.

<!-------------------------- Planning Operation -->
### Planning

**Agent Skill:** `planning`

Converts the current Target and applicable Developer guidance into bounded, understandable, and verifiable Tasks.

<!-------------------------- Developing Operation -->
### Developing

**Agent Skill:** `developing`

Implements and verifies eligible planned Tasks through the applicable Target and Developer context.

<!-------------------------- Reviewing Operation -->
### Reviewing

**Agent Skill:** `reviewing`

Evaluates implemented work independently and records evidence-based Findings without repairing the result.

<!-------------------------- Launch Operation -->
### Launch

**Agent Skill:** `launch`

Verifies the selected Environment prepared by Configure, starts the developed parts through the selected Launch, verifies readiness, and reports access points.

<!-------------------------- Implement Operation -->
### Implement

**Agent Skill:** `implement`

Coordinates Configure, baseline Review of existing work, Planning, Development, independent final Review, Finding reconciliation, and eligible Launch for selected phases or every enabled and ready phase.

<!-------------------------- Reset Operation -->
### Reset

**Agent Skill:** `reset`

Previews and, after human confirmation, resets the outputs and operational records covered by the selected reset stage.

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
responsibility = Reconcile operational Config, synchronize phase State, and prepare the selected Environment
inputs = Operational Schemas, existing Config, Target phase identities and Platform selections, and Platform authorities
output = Current operational Config and a prepared selected Environment
```

<!-------------------------- Planning -->
### Planning

```text
state = planning
responsibility = Create bounded and verifiable Tasks without prescribing implementation
inputs = Current Target, applicable Principles and Preferences, and operational records
output = Updated Plan Config
```

<!-------------------------- Development -->
### Development

```text
state = development
responsibility = Implement and verify eligible planned Tasks
inputs = Current Target, applicable Principles and Preferences, Plan, State, and existing implementation
output = Verified implementation and updated operational records
```


<br><br>

<!--------------------------------------------------------------------------------- Authority and Ownership --->
## Authority and Ownership

Explicit Target intent and applicable Principles guide each Skill. Preferences supply defaults where the Target leaves a choice unstated. The operational Schemas define the shape of operational records, the Principles and Preferences Schemas define the shape of the authored sources, and the general YAML Schema supplies the common frame for Preferences and Config files. Schema definition files use their own formats. Config stores operational records and does not define the Target.

```text
Target = human-defined intent
Principles = mandatory philosophy, responsibilities, and boundaries
Preferences = technical defaults for unspecified choices
Schema = common YAML frame for Preferences and Config, authored-source structure, and the storage structure of every operational record
Config = the mutable operational records
```

Ownership answers who a record belongs to, and it belongs to the Human or to a Component:

```text
Human = owns Interface, Target, Principles, Preferences, and Schema sources
Plan = owns Plans, Groups, Tasks, their status, and their history
State = owns active Workflow position, aggregate phase progress, Implement and Launch results, operational History, Blockers, and Open Questions
Review = owns recorded Findings and their state
```

Write authority answers which Skill may change a record, and every write happens under the rules of the Component that owns it:

```text
Configure = writes every operational Config, synchronizes phase records, records its State outcome, and prepares the selected Environment
Planning = writes Plans, Groups, and Tasks under Plan, and Planning progress and History under State
Developing = writes implementation and Task status and history under Plan, and Development progress and History under State
Reviewer = writes Findings under Review, and Review progress and History under State
Configure, Planning, and Developing = write the active Workflow position under State
Launch = changes runtime state through Platform and writes Launch State, access points, and History under State
Implement = coordinates operation Skills and writes only Implementation State and its History under State
Reset = after human confirmation of the preview, removes or resets the outputs and operational records covered by the selected reset stage, including the Workflow position, under the owning Components' rules
Reviewer, Launch, Implement, and Skill Installer = do not directly change the active Workflow mode
Every Skill = may record its own Blockers and Open Questions under State's rules when applicable
```

Each Skill writes only the records it has authority over, and always under the rules of the Component that owns them. Operational records follow their source authorities and must not redefine them.

The complete `.interface/` tree is read-only to every Agent Role and Skill by default. The only mutable exception is `.interface/foundation/config/`, and a Skill may change files there only within the write authority stated above and the owning Component's rules. No other Interface path becomes writable because it is added later, discovered by a Tool, or named by a Plan.

<br><br>

<!--------------------------------------------------------------------------------- Foundation Files --->
## Foundation Files
Foundation Files provide foundational definitions and schemas required by the Interface.

<!-------------------------- Foundation Repository Structure -->
### Repository Structure

```text
.interface/foundation/
├── interface.md
├── config/
└── schema/
```

Target Definitions are intentionally **not** considered Foundation Files because they belong to the Target concept itself.


<!-------------------------- Interface Foundation File -->
### Interface File

```text
name = Interface
path = .interface/foundation/interface.md
responsibility = Canonical definition, navigation entry point, and complete file map of Agent Interface
```


<!-------------------------- Config Foundation Files -->
### Config Files

Config stores mutable operational information used while executing the Interface.

```text
.interface/foundation/config/
├── state.yaml
├── plan.yaml
└── review.yaml
```


#### State Config

```text
name = State Config
path = .interface/foundation/config/state.yaml
responsibility = Stores active Workflow position, aggregate phase progress, Implement and Launch results, access points, History, Blockers, and Open Questions
```


#### Plan Config

```text
name = Plan Config
path = .interface/foundation/config/plan.yaml
responsibility = Stores Plans, Groups, Tasks, their dependencies, status, and history
```


#### Review Config

```text
name = Review Config
path = .interface/foundation/config/review.yaml
responsibility = Stores reviewed phases, outcomes, Findings, evidence, and Finding status
```


<!-------------------------- Schema Foundation Files -->
### Schema Files

Schemas define the structure followed by authored Interface files and generated operational records.

```text
.interface/foundation/schema/
├── yaml.yaml
├── principles.md
├── preferences.yaml
├── skill-contract.md
├── state.yaml
├── plan.yaml
└── review.yaml
```


#### YAML Schema

```text
name = YAML Schema
path = .interface/foundation/schema/yaml.yaml
kind = Structure standard
responsibility = Defines the common outer structure followed by Interface Preferences and Config files
scope = Schema definition files use their own formats and do not follow this outer structure
```


#### Principles Schema

```text
name = Principles Schema
path = .interface/foundation/schema/principles.md
kind = Structure standard
responsibility = Defines the common Markdown structure followed by every Developer and Agent Component principles.md file
```


#### Preferences Schema

```text
name = Preferences Schema
path = .interface/foundation/schema/preferences.yaml
kind = Structure standard
responsibility = Defines the common structure followed by every Developer and Agent Component preferences.yaml file
```


#### Skill Contract Schema

```text
name = Skill Contract Schema
path = .interface/foundation/schema/skill-contract.md
kind = Structure standard
responsibility = Defines the portable, runtime-independent structure followed by every declared Agent Skill Contract
```


#### State Schema

```text
name = State Schema
path = .interface/foundation/schema/state.yaml
kind = Operational format
responsibility = Defines the stored structure and initial values of State Config
generates = .interface/foundation/config/state.yaml
```


#### Plan Schema

```text
name = Plan Schema
path = .interface/foundation/schema/plan.yaml
kind = Operational format
responsibility = Defines the stored structure and initial values of Plan Config
generates = .interface/foundation/config/plan.yaml
```


#### Review Schema

```text
name = Review Schema
path = .interface/foundation/schema/review.yaml
kind = Operational format
responsibility = Defines the stored structure and initial values of Review Config
generates = .interface/foundation/config/review.yaml
```



<br><br>

<!--------------------------------------------------------------------------------- Workflow --->
## Workflow
<!-------------------------- Define the Target -->
### Define the Target

```text
order = 1
name = Define the Target
actor = Human
action = State the Target in .interface/target/non-technical.md, then translate it as the Human developer into .interface/target/technical.md without changing its intent
```


<!-------------------------- Configure -->
### Configure

```text
order = 2
name = Configure
skill = configure
command routing = Agent Command Preferences
action = Reconcile operational Config, synchronize Target phase identities in State, and prepare the selected Platform Environment
```

<!-------------------------- Generate Tasks -->
### Generate Tasks

```text
order = 3
name = Generate Tasks
skill = planning
command routing = Agent Command Preferences
action = Create or reconcile the Plan for the requested phase
```

<!-------------------------- Develop the Tasks -->
### Develop the Tasks

```text
order = 4
name = Develop the Tasks
skill = developing
command routing = Agent Command Preferences
action = Implement and verify eligible Tasks for the requested phase
```

<!-------------------------- Review the Result -->
### Review the Result

```text
order = 5
name = Review the Result
skill = reviewing
command routing = Agent Command Preferences
action = Evaluate the implemented result for the requested phase and record evidence-based Findings
```

<!-------------------------- Launch the Target -->
### Launch the Target

```text
order = 6
name = Launch the Target
skill = launch
command routing = Agent Command Preferences
action = Verify the prepared Environment, start the completed parts through the selected Launch, verify readiness, and report access points
```
