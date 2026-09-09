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
6. **[Operations](#operations)** — understand the actions performed through Configure, Planning, Developing, Reviewing, and Reset.
7. **[Modes](#modes)** — understand the operational positions recorded by State.
8. **[Authority and Ownership](#authority-and-ownership)** — understand who owns each record and which Skill may change it.
9. **[Foundation Files](#foundation-files)** — locate the Interface document, Config, and shared Schema definitions.
10. **[Workflow](#workflow)** — follow the path from defining a Target through configuration, planning, and development.


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

The Human states the Target in the Non-Technical Definition. Acting as the developer, the Human translates that intent into the Technical Definition without changing its meaning. Skills then read the current sources required by their role before acting. Planning records activities as Tasks; Development implements and verifies those Tasks. Mechanical actions such as Config initialization do not interpret the Target.

Config contains only the mutable operational records used to coordinate this work. Schemas define their storage format.

<!-------------------------- Independence -->
### Independence

The core Interface Structure is independent of any specific AI model, Agent, or external execution capability. Agent Skills are integrations within the Agent Module, while their implementations remain outside `.interface/` and independent of its internal structure.

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
- **Component** — one named part of the Developer perspective that owns a responsibility and is described through its Principles and Preferences; some Components also own operational records.
- **Principles** — mandatory philosophy, responsibilities, rules, and boundaries that describe how the Developer believes software should fundamentally be designed.
- **Preferences** — preferred choices and defaults used when multiple valid implementations exist and the Target leaves the choice unspecified.
- **Schema** — the structure a file follows: either a standard for a Human-authored file or an operational format and initial template for a generated record.
- **Config** — mutable operational records that coordinate the Workflow and record where work stands; Config does not store what the Target means.
- **Plan** — the high-level organization of work, containing Groups, dependencies, and individual Tasks.
- **Task** — one bounded, understandable, and verifiable unit of work within a Plan.
- **Understanding** — the current context an Agent establishes from authoritative sources before performing a Skill's role; it is either about Agent Interface itself or about the active Target.
- **Operation** — one defined action performed through an Agent Skill to configure, plan, develop, review, or reset work.
- **Workflow** — the ordered path from the Human's Target definition to developed software: Define Target, Configure, Plan, and Develop, together with supporting actions.
- **Mode** — an operational position in the Workflow, recorded by State.
- **Skill** — an Agent capability that performs a Workflow action or provides a supporting utility; it is part of the Agent Module's integration surface, while its implementation remains outside `.interface/`.





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

Each Module owns its detailed Conceptual Structure and Repository Structure. Understanding establishes the context used by a Skill, Operations define the actions Skills perform, Foundation Files remain shared resources, Modes record operational position, Authority and Ownership control writes, and Workflow defines execution order.



<br><br>

<!--------------------------------------------------------------------------------- Modules --->
## Modules

Target, Developer, and Agent are the three primary Modules of Agent Interface. Each Module owns a distinct responsibility and documents its own Conceptual Structure and Repository Structure.

<!-------------------------- Target -->
### Target

The Target describes **what the Interface is working on**.

The Target is defined through two complementary, human-owned sources:

- **Non-Technical Definition:** The Human's initial statement of intent, context, and requirements without requiring technical formulation; an empty file contributes no information.
- **Technical Definition:** The Human, acting as the developer, translates the Non-Technical Definition into this technical form. It is the primary authority for the Target and takes precedence wherever the two definitions conflict.

#### Conceptual Structure

```text
Target
├── Non-Technical Definition
└── Technical Definition
```

#### Repository Structure

```text
.interface/target/
├── non-technical.md
└── technical.md
```

#### Phase Status

The Technical Definition divides the Target into ordered phases, and each phase declares a `status`:

```text
Enabled  = the phase is in scope; it is planned, developed, and reviewed in its defined order
Disabled = the phase is out of scope; no Plan, Task, Finding, or other operational record is
           created for it, and an existing record is preserved rather than removed
```

`status` states scope, never progress. Where a phase stands is held in the operational Config that owns it, and is never recorded in the Target.

<!-------------------------- Developer -->
### Developer

The Developer module defines the reusable programming personality, standards, and engineering perspective applied to a Target. It expresses them through the Development, Model, Database, Backend, Frontend, Platform, Plan, Review, and State Components.

Each Component states its mandatory philosophy, responsibilities, and boundaries through Principles, and its preferred technical choices and defaults through Preferences.

#### Conceptual Structure

```text
Developer
└── Components
    ├── Development
    │   ├── Principles
    │   └── Preferences
    ├── Model
    │   ├── Principles
    │   └── Preferences
    ├── Database
    │   ├── Principles
    │   └── Preferences
    ├── Backend
    │   ├── Principles
    │   └── Preferences
    ├── Frontend
    │   ├── Principles
    │   └── Preferences
    ├── Platform
    │   ├── Principles
    │   └── Preferences
    ├── Plan
    │   ├── Principles
    │   └── Preferences
    ├── Review
    │   ├── Principles
    │   └── Preferences
    └── State
        ├── Principles
        └── Preferences
```


#### Repository Structure

```text
.interface/developer/
├── development/
│   ├── principles.md
│   └── preferences.yaml
├── model/
│   ├── principles.md
│   └── preferences.yaml
├── database/
│   ├── principles.md
│   └── preferences.yaml
├── backend/
│   ├── principles.md
│   └── preferences.yaml
├── frontend/
│   ├── principles.md
│   └── preferences.yaml
├── platform/
│   ├── principles.md
│   └── preferences.yaml
├── plan/
│   ├── principles.md
│   └── preferences.yaml
├── review/
│   ├── principles.md
│   └── preferences.yaml
└── state/
    ├── principles.md
    └── preferences.yaml
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
State       = Records where the Workflow stands, together with Blockers and Open Questions
```

Each line names a Component so that a phase target can be resolved to its owner. The Component's own Principles remain the authority: when this summary and a Component's Principles disagree, the Principles are correct.


<!-------------------------- Agent -->
### Agent
The Agent module defines the execution side of Agent Interface through Agents, Commands, Rules, Hooks, Output Styles, and Skills. An Agent establishes the Understanding required by its active Skill, follows the applicable Rules and Workflow, and uses its capabilities to apply the Developer perspective to the Target.

The Agent is replaceable: a different Agent may execute the same Interface through its own native capabilities without requiring the Target or Developer modules to be redesigned.

#### Conceptual Structure

```text
Agent
├── Agents
├── Commands
├── Rules
├── Hooks
├── Output Styles
└── Skills
```

These concepts provide a common abstraction over capabilities that modern coding agents may expose differently.


#### Repository Structure

```text
.claude/
├── agents/
├── commands/
├── hooks/
├── output-styles/
├── rules/
├── skills/
├── settings.json
└── settings.local.json
```

`.claude/` is outside `.interface/` because it is the current Agent-specific implementation. Another Agent may map the same concepts to different native paths.


#### Agents

```text
name = interface-reader
path = .claude/agents/interface-reader.md
responsibility = Report the current operational position, planned work, blockers, questions, and review findings without writing changes
mode = none
writes = none
```


#### Rules

```text
name = Interface Bootstrap
path = .claude/rules/interface-bootstrap.md
responsibility = Defines the shared entry point and the separation between Agent Skills and the Interface
```

```text
name = Interface Skill Policy
path = .claude/rules/interface-skill-policy.md
responsibility = Defines human-owned boundaries, project-scoped Agent capabilities, and the decision policy shared by every Interface Skill
```


#### Skills

Interface Skills are the fixed external capabilities that perform the Workflow and its supporting actions. Technology-specific or third-party Skills are discovered dynamically and are not part of this catalog.

Configure

```text
name = my-interface-configure
path = .claude/skills/my-interface-configure/SKILL.md
invocation = /my-interface-configure
responsibility = Initialize every operational Config from its Schema and reconcile existing records with the current structure
mode = configuring
```

Tasker

```text
name = my-interface-tasker
path = .claude/skills/my-interface-tasker/SKILL.md
invocation = /my-interface-tasker <phase-number>
responsibility = Create or reconcile a Task Plan without prescribing implementation
mode = planning
```

Developer

```text
name = my-interface-developer
path = .claude/skills/my-interface-developer/SKILL.md
invocation = /my-interface-developer <phase-number>
responsibility = Implement and verify eligible planned Tasks
mode = development
```

Reviewer

```text
name = my-interface-reviewer
path = .claude/skills/my-interface-reviewer/SKILL.md
invocation = /my-interface-reviewer <phase-number>
responsibility = Review implemented work, record evidence-based Findings, and report them without repairing the result
mode = none
when = When implemented work needs independent verification
```

Reset

```text
name = my-interface-reset
path = .claude/skills/my-interface-reset/SKILL.md
invocation = /my-interface-reset <1|2|3>
responsibility = Preview and, after human confirmation, reset Configure, Task, or Development output
mode = none
when = When the Human explicitly requests that selected output be reset
```

Skill Installer

```text
name = my-interface-skill-installer
path = .claude/skills/my-interface-skill-installer/SKILL.md
invocation = /my-interface-skill-installer
responsibility = Discover compatible Skills, plugins, MCP integrations, and other Agent capabilities, preview the findings, and install approved candidates at project scope
mode = none
when = When the Target may benefit from an additional Agent capability
```

<br><br>

<!--------------------------------------------------------------------------------- Understanding --->
## Understanding

Understanding is the current context an Agent establishes from authoritative sources before performing a Skill's role. Interface Understanding is required by every Skill. Target Understanding is required by roles that interpret or act on the Target; a mechanical Workflow such as Configure or Reset may omit it because it does not interpret project intent.

- **Interface Understanding:** Understand Agent Interface, locate its current resources, and place the active Skill within the Interface.
- **Target Understanding:** Understand what is being built and the Target's current intent, scope, and project-specific decisions.

<!-------------------------- Understanding Conceptual Structure -->
### Conceptual Structure

```text
Understanding
├── Interface Understanding
└── Target Understanding
```

<!-------------------------- Understanding Repository Structure -->
### Repository Structure

```text
Understanding
├── Interface Understanding
│   └── .interface/foundation/interface.md
└── Target Understanding
    └── .interface/target/
        ├── non-technical.md
        └── technical.md
```

These sources remain authoritative. Understanding is reconstructed from their current content when a Skill needs it; it is not copied into Config as a second project definition.

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
└── Reset
```

<!-------------------------- Configure Operation -->
### Configure

**Agent Skill:** `my-interface-configure`

Initializes operational Config files from their Schemas and reconciles existing records with the current structure.

<!-------------------------- Planning Operation -->
### Planning

**Agent Skill:** `my-interface-tasker`

Converts the current Target and applicable Developer guidance into bounded, understandable, and verifiable Tasks.

<!-------------------------- Developing Operation -->
### Developing

**Agent Skill:** `my-interface-developer`

Implements and verifies eligible planned Tasks through the applicable Target and Developer context.

<!-------------------------- Reviewing Operation -->
### Reviewing

**Agent Skill:** `my-interface-reviewer`

Evaluates implemented work independently and records evidence-based Findings without repairing the result.

<!-------------------------- Reset Operation -->
### Reset

**Agent Skill:** `my-interface-reset`

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
responsibility = Initialize operational Config files from their Schema templates and reconcile existing records
inputs = Operational Schemas and existing Config records
output = Current and valid operational Config files
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
State = owns the active Workflow position, Blockers, and Open Questions
Review = owns recorded Findings and their state
```

Write authority answers which Skill may change a record, and every write happens under the rules of the Component that owns it:

```text
Configure = writes every operational Config, creating it from its Schema template or bringing it to the current structure
Tasker = writes Plans, Groups, and Tasks under Plan's rules
Developer = writes implementation, and Task status and history under Plan's rules
Reviewer = writes Findings under Review's rules
Configure, Tasker, and Developer = write the active Workflow position under State's rules
Reset = after human confirmation of the preview, removes or resets the outputs and operational records covered by the selected reset stage, including the Workflow position, under the owning Components' rules
Reviewer and Skill Installer = do not change the active Workflow position
Every Skill = may record its own Blockers and Open Questions under State's rules when applicable
```

Each Skill writes only the records it has authority over, and always under the rules of the Component that owns them. Operational records follow their source authorities and must not redefine them.

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
responsibility = Stores the current Workflow position, active phase, Blockers, and Open Questions
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
responsibility = Defines the common Markdown structure followed by every Component's principles.md file
```


#### Preferences Schema

```text
name = Preferences Schema
path = .interface/foundation/schema/preferences.yaml
kind = Structure standard
responsibility = Defines the common structure followed by every Component's preferences.yaml file
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
skill = /my-interface-configure
action = Initialize every operational Config file from the initial values in its Schema while preserving existing operational records
```

<!-------------------------- Generate Tasks -->
### Generate Tasks

```text
order = 3
name = Generate Tasks
skill = /my-interface-tasker <phase-number>
action = Create or reconcile the Plan for the requested phase
```

<!-------------------------- Develop the Tasks -->
### Develop the Tasks

```text
order = 4
name = Develop the Tasks
skill = /my-interface-developer <phase-number>
action = Implement and verify eligible Tasks for the requested phase
```
