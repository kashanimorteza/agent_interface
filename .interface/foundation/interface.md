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
   - **[Developer](#developer)** — understand the engineering philosophy through Components and their Principles and Developer Preferences.
   - **[Agent](#agent)** — understand the executing system, its capabilities, restrictions, and Skills.
5. **[Understanding](#understanding)** — distinguish knowledge of Agent Interface from knowledge of the current Target.
6. **[Operations](#operations)** — understand the one-to-one actions performed through every Interface-owned Skill.
7. **[Modes](#modes)** — understand the operational positions recorded by State.
8. **[Authority and Ownership](#authority-and-ownership)** — understand who owns each record and which Skill may change it.
9. **[Foundation Files](#foundation-files)** — locate the Interface document, Config, and shared Schema definitions.
10. **[Workflow](#workflow)** — choose Default, Normal, or Detailed control while following the path from Target definition through launch.


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

Its purpose is to let a Human define a Target in natural language and give Agents common Developer Principles and Preferences together with an explicit Agent Profile for planning and developing it.

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
- **Component** — one named part of the Developer or Agent perspective that owns a responsibility and is described through Principles together with Developer Preferences or an Agent Profile; some Developer Components also own operational records.
- **Principles** — mandatory portable philosophy, responsibilities, rules, and boundaries owned by a Developer or Agent Component.
- **Developer Preferences** — preferred engineering choices, defaults, packages, implementation conventions, and optional Agent Skill associations used when the Target leaves a choice unspecified.
- **Schema** — the structure a file follows: either a standard for a Human-authored file or an operational format and initial template for a generated record.
- **Config** — mutable operational records that coordinate the Workflow and record where work stands; Config does not store what the Target means.
- **Plan** — the high-level organization of work, containing Groups, dependencies, and individual Tasks.
- **Task** — one bounded, understandable, and verifiable unit of work within a Plan.
- **Understanding** — the current context an Agent establishes from authoritative sources before performing a Skill's role; it is either about Agent Interface itself or about the active Target.
- **Operation** — one defined action performed through an Agent Skill to configure, plan, develop, review, launch, implement, or reset work.
- **Workflow** — the ordered path from the Human's Target definition to running software: Define Target, Configure, Plan, Develop, Review, and Launch.
- **Workflow Path** — the Human's selected level of direct orchestration over that same Workflow: Default, Normal, or Detailed; it is an invocation style, not a State Mode.
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
The Agent module defines the execution side of Agent Interface through Components. Each Agent Component owns one responsibility and has Principles for its mandatory portable contract and a Profile for its current choices, resources, native mappings, and explicit empty categories.

Together, these Components form the Agent Profile. A different Agent Runtime reads the same Profile and maps it to native capabilities without requiring the Target or Developer modules to be redesigned.

#### Structure

```text
Agent
└── Components
    ├── Runtime
    │   ├── Principles  → .interface/agent/runtime/principles.md
    │   └── Profile     → .interface/agent/runtime/profile.yaml
    ├── Settings
    │   ├── Principles  → .interface/agent/settings/principles.md
    │   └── Profile     → .interface/agent/settings/profile.yaml
    ├── Context
    │   ├── Principles  → .interface/agent/context/principles.md
    │   └── Profile     → .interface/agent/context/profile.yaml
    ├── Role
    │   ├── Principles  → .interface/agent/role/principles.md
    │   └── Profile     → .interface/agent/role/profile.yaml
    ├── Agent
    │   ├── Principles  → .interface/agent/agent/principles.md
    │   └── Profile     → .interface/agent/agent/profile.yaml
    ├── Coordination
    │   ├── Principles  → .interface/agent/coordination/principles.md
    │   └── Profile     → .interface/agent/coordination/profile.yaml
    ├── Skill
    │   ├── Principles  → .interface/agent/skill/principles.md
    │   ├── Profile     → .interface/agent/skill/profile.yaml
    │   └── Contracts   → .interface/agent/skill/contracts/<interface-owned-skill>.md
    ├── Command
    │   ├── Principles  → .interface/agent/command/principles.md
    │   └── Profile     → .interface/agent/command/profile.yaml
    ├── Rule
    │   ├── Principles  → .interface/agent/rule/principles.md
    │   └── Profile     → .interface/agent/rule/profile.yaml
    ├── Tool
    │   ├── Principles  → .interface/agent/tool/principles.md
    │   └── Profile     → .interface/agent/tool/profile.yaml
    ├── Hook
    │   ├── Principles  → .interface/agent/hook/principles.md
    │   └── Profile     → .interface/agent/hook/profile.yaml
    ├── Integration
    │   ├── Principles  → .interface/agent/integration/principles.md
    │   └── Profile     → .interface/agent/integration/profile.yaml
    ├── Extension
    │   ├── Principles  → .interface/agent/extension/principles.md
    │   └── Profile     → .interface/agent/extension/profile.yaml
    ├── Interaction
    │   ├── Principles  → .interface/agent/interaction/principles.md
    │   └── Profile     → .interface/agent/interaction/profile.yaml
    ├── Permission
    │   ├── Principles  → .interface/agent/permission/principles.md
    │   └── Profile     → .interface/agent/permission/profile.yaml
    ├── Session
    │   ├── Principles  → .interface/agent/session/principles.md
    │   └── Profile     → .interface/agent/session/profile.yaml
    └── Observability
        ├── Principles  → .interface/agent/observability/principles.md
        └── Profile     → .interface/agent/observability/profile.yaml
```

The Agent Components are read in the order shown. When the active role uses an Interface-owned Skill, its portable Contract is read after Skill Principles and Profile. An external Skill is read from its declared provider resource under the active Role and applicable Agent Principles. A later Component may consume an earlier one but never becomes its second authority. Every supported category remains represented even when its Profile entries are empty, so absence is explicit rather than indistinguishable from omission. Runtime-specific implementation remains outside the Interface and is only an adapter and evidence that the Profile has been realized.


#### Components

```text
Runtime        = Runtime identity, provider, model, compatibility, and native capability mapping
Settings       = Configuration sources, scopes, precedence, merge behavior, environment, and reconciliation
Context        = Persistent instructions, Understanding, Memory, imports, loading, and compaction
Role           = Primary and specialized Agent Role contracts
Agent          = General and specialized executable Agent identities that realize declared Roles
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

Every Agent Component's Principles and Profile are authoritative for that Component only. A runtime artifact not declared in the owning Profile is an optional runtime capability; a required declaration not usable by the selected runtime is an Agent Profile gap.

<br><br>

<!--------------------------------------------------------------------------------- Understanding --->
## Understanding

Understanding is the current context an Agent establishes before performing a Skill's role. Interface Understanding is required by every Skill and starts exclusively from this canonical Interface file. The Interface then routes the Skill to the Component authorities required by its role; the Agent never needs prior knowledge of the Interface's internal directory structure. Target Understanding is separate and, when the role needs Target meaning, is established from both Human Definition and Technical Definition under Target's declared precedence. Configure uses only the phase identities and Platform selections required for its role; Reset establishes the minimum Target Understanding needed for a phase scope, omits it for Config scope, and uses only phase identity and ownership for Complete scope.

- **Interface Understanding:** Read `.interface/foundation/interface.md` as the sole Foundation Source, then follow only the routes it provides for the active role.
- **Target Understanding:** When required, read both Target definitions located by the Interface. Human Definition provides the Human's stated intent and context; Technical Definition is the primary Target authority and takes precedence wherever they conflict.

<!-------------------------- Understanding Structure -->
### Structure

```text
Understanding
├── Interface Understanding
│   └── Interface Foundation Source → .interface/foundation/interface.md
└── Target Understanding
    ├── Human Definition    → .interface/target/non-technical.md
    └── Technical Definition → .interface/target/technical.md
```

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

This Operation is performed through `/my-interface-configure` to initialize and reconcile operational Config, synchronize phase State, and prepare the selected Platform Environment.

<!-------------------------- Planning Operation -->
### Planning

**Agent Skill:** `/my-interface-planning`

This Operation is performed through `/my-interface-planning` to convert the current Target and applicable Developer guidance into bounded, understandable, and verifiable Tasks.

<!-------------------------- Developing Operation -->
### Developing

**Agent Skill:** `/my-interface-developing`

This Operation is performed through `/my-interface-developing [phase-number ...]` to implement and verify eligible planned Tasks only after current Review proves Plan Assurance for the exact current Plan Revision.

<!-------------------------- Reviewing Operation -->
### Reviewing

**Agent Skill:** `/my-interface-reviewer`

This Operation is performed through `/my-interface-reviewer [phase-number ...]` to assure each selected phase's Plan against current Interface and Target Understanding, coordinate Planning and independently recheck it when reconciliation is required, and then evaluate existing implementation without repairing it. With no phase input, it reviews every enabled phase.

<!-------------------------- Launch Operation -->
### Launch

**Agent Skill:** `/my-interface-launch`

This Operation is performed through `/my-interface-launch` to verify the selected Environment prepared by Configure, start the developed parts through the selected Launch, verify readiness, and report access points.

<!-------------------------- Implement Operation -->
### Implement

**Agent Skill:** `/my-interface-implement`

This Operation is performed through `/my-interface-implement [phase-number ...]` to execute Configure once, then Planning, Plan Review, Developing, and final Review for each selected phase in Target order, advancing only after the phase is satisfied, and finally perform eligible Launch. With no phase input, it processes every enabled and ready phase.

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

**Agent Skill:** `/my-interface-agent-sync`

This Operation is performed through `/my-interface-agent-sync` to dynamically inspect every current Agent Component, reconcile its complete declared Profile with the selected Runtime, and certify synchronization only after all required capabilities pass post-change verification.

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
inputs = Current Target, applicable Developer Principles and Preferences, Agent Profile, and operational records
output = Updated Plan Config
```

<!-------------------------- Development -->
### Development

```text
state = development
responsibility = Implement and verify eligible planned Tasks
inputs = Current Target, applicable Developer Principles and Preferences, Agent Profile, Plan, State, and existing implementation
output = Verified implementation and updated operational records
```


<br><br>

<!--------------------------------------------------------------------------------- Authority and Ownership --->
## Authority and Ownership

Explicit Target intent and applicable Principles guide each Skill. Developer Preferences supply engineering defaults where the Target leaves a choice unstated, while Agent Profiles declare the current execution capabilities and mappings. Operational Schemas define the shape of operational records, authored-source Schemas define Principles, Developer Preferences, and Agent Profiles, and the general YAML Schema supplies their common YAML frame together with Config files. Schema definition files use their own formats. Config stores operational records and does not define the Target.

```text
Target = human-defined intent
Principles = mandatory philosophy, responsibilities, and boundaries
Developer Preferences = engineering defaults for unspecified Target choices
Agent Profiles = current Agent selections, resources, mappings, and explicit empty categories
Schema = common YAML frame for Developer Preferences, Agent Profiles, and Config, authored-source structure, and the storage structure of every operational record
Config = the mutable operational records
```

Ownership answers who a record belongs to, and it belongs to the Human or to a Component:

```text
Human = owns Interface, Target, Principles, Developer Preferences, Agent Profiles, and Schema sources
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
Reset = after human confirmation of the preview, removes or resets explicit-phase outputs, every generated phase when no phase is supplied, Config only, or the complete set of Config and all-phase implementation outputs, including reconciliation of the Workflow position, under the owning Components' rules
Skill Installer = discovers Agent capabilities and, after approval, provisions only approved project-scoped capabilities outside Interface sources
Agent Sync = reconciles declared Agent Profile choices with project-scoped native Runtime artifacts outside Interface sources
Reviewing, Launch, Implement, Skill Installer, and Agent Sync = do not directly change the active Workflow mode
Every Skill = may record its own Blockers and Open Questions under State's rules when applicable
```

Each Skill writes only the records it has authority over, and always under the rules of the Component that owns them. Operational records follow their source authorities and must not redefine them.

The complete `.interface/` tree is read-only to every Agent Role and Skill by default. The only mutable exception is `.interface/foundation/config/`, and a Skill may change files there only within the write authority stated above and the owning Component's rules. No other Interface path becomes writable because it is added later, discovered by a Tool, or named by a Plan.

<br><br>

<!--------------------------------------------------------------------------------- Foundation Files --->
## Foundation Files
Foundation Files provide foundational definitions and schemas required by the Interface.

<!-------------------------- Foundation Structure -->
### Structure

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
├── developer-preferences.yaml
├── agent-profile.yaml
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
responsibility = Defines the common outer structure followed by Developer Preferences, Agent Profiles, and Config files
scope = Schema definition files use their own formats and do not follow this outer structure
```


#### Principles Schema

```text
name = Principles Schema
path = .interface/foundation/schema/principles.md
kind = Structure standard
responsibility = Defines the common Markdown structure followed by every Developer and Agent Component principles.md file
```


#### Developer Preferences Schema

```text
name = Developer Preferences Schema
path = .interface/foundation/schema/developer-preferences.yaml
kind = Structure standard
responsibility = Defines the four-section structure followed by every Developer Component preferences.yaml file
```


#### Agent Profile Schema

```text
name = Agent Profile Schema
path = .interface/foundation/schema/agent-profile.yaml
kind = Structure standard
responsibility = Defines the three-section structure followed by every Agent Component profile.yaml file
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
Repeat Planning, Plan Review, Developing, and final Review for each remaining phase
/my-interface-launch
```

The first Reviewing pass assures the current Plan Revision before Development. The second re-assures that Plan and judges the existing implementation. A phase is reconciled before advancing, and Launch runs only after all required phases satisfy both gates.
