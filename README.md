# Agent Interface

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

Use this document as the entry point and follow its sections in this order:

1. **Introduction** — understand the purpose, operation, independence, and boundaries of Agent Interface.
2. **Terminology** — learn the shared vocabulary used throughout the Interface.
3. **Architecture** — see the complete conceptual hierarchy and the relationships between its parts.
4. **Interface** — understand the canonical document, its responsibility, and its boundaries.
5. **Target** — understand what is being built through its non-technical and technical definitions.
6. **Developer** — understand the engineering philosophy through Principles, Preferences, Components, State, and Mode.
7. **Agent** — understand the executing system, its capabilities, restrictions, and Skills.
8. **Operations** — understand Configure, Plan, Develop, Review, and Reset independently from their execution mechanisms.
9. **Understanding** — learn how each Skill discovers the context required for its own responsibility.
10. **Config** — understand the mutable State, Plan, and Review operational records.
11. **Foundation Files** — locate Config and the shared Schema definitions.
12. **Workflow** — follow the path from defining a Target through configuration, planning, development, review, and reset.
13. **Concept Relationships** — understand the boundaries between Target, Developer, Agent, Operations, and Skills.
14. **Important Architectural Decisions** — review the decisions that shape the current design.
15. **Implementation Neutrality** — understand which implementation mechanisms remain optional.
16. **Guiding Principle** — see the central rule guiding context discovery and execution.
17. **Summary** — review the complete Interface at a glance.


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

The long-term implementation may eventually use technologies such as skills, MCP, hooks, plugins, memory systems, agent instances, tools, or other future agent capabilities.

Those technologies are implementation mechanisms.

The primary concern of the Interface is the **conceptual contract** between the Developer, Agent, and Target.

<!-------------------------- Purpose -->
### Purpose

Agent Interface is an independent interface between **Humans** and **AI Agents** for establishing a common protocol, structure, and standard for software development.

Its purpose is to let a Human define a target project in natural language and give Agents common Principles and Preferences for understanding, planning, and developing it.

<!-------------------------- Operation -->
### Operation

The Human supplies the project definition. Operations that need project meaning read it and the applicable Principles and Preferences to establish their own Understanding. Planning records activities as Tasks; Development implements and verifies those Tasks. Mechanical operations such as Config initialization do not interpret the project.

Config contains only the mutable operational records used to coordinate this work. Schemas define their storage format. Understanding is formed by each operation and is not stored in Config.

<!-------------------------- Independence -->
### Independence

The core Interface Structure is independent of any specific AI model, Agent, or external execution capability. Agent Skills are cataloged as integrations, not as parts of the Structure.

Human project definitions remain flexible, while the Interface gives Agents stable responsibilities, rules, defaults, and operational records. Agent Interface is the communication boundary between those two forms.

<!-------------------------- Core Idea -->
### Core Idea

Modern AI coding agents can generate and modify software, but an agent still needs to understand several independent things before it can reliably act:

1. **What is being built?**
2. **How does the developer want software to be built?**
3. **What agent is performing the work and what capabilities or restrictions does it have?**
4. **What operation is currently being performed?**

Agent Interface gives these concerns explicit structure.

Conceptually:

```text
Target
   │
   │  What should be built?
   │
Developer
   │
   │  How should it be built?
   │
Agent
   │
   │  Who/what performs the work?
   │
Operations
   │
   │  What should be done now?
   ▼
Implementation
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

- **Interface** — the complete system described by this document; it connects Target, Developer, Agent, Operations, Config, Foundation Files, and Workflow, and is their container rather than a sibling entity.
- **Human** — the person who defines the Target and owns every authored Interface source.
- **Target** — the application, platform, service, API, module, package, subsystem, or other development subject the Interface works on. The term is preferred over Target Project because the subject does not have to be an entire project.
- **Developer** — the developer's reusable programming philosophy and engineering perspective, independent of a particular Target or Agent.
- **Agent** — the AI coding system that interacts with the Interface and maps its concepts to native capabilities.
- **Agent Instance** — an individual execution unit, worker, sub-agent, parallel agent, or isolated runtime context created by an Agent.
- **Component** — one named part of the Developer perspective that owns a responsibility and is described through its Principles and Preferences; some Components also own operational records.
- **Principles** — mandatory philosophy, responsibilities, rules, and boundaries that describe how the Developer believes software should fundamentally be designed.
- **Preferences** — preferred choices and defaults used when multiple valid implementations exist and the Target leaves the choice unspecified.
- **Layer** — a distinct architectural responsibility. In the previous Interface it also described Principles, Preferences, and Config as three forms; the new architecture places those concepts according to their actual responsibilities.
- **Schema** — the structure a file follows: either a standard for a Human-authored file or an operational format and initial template for a generated record.
- **Config** — mutable operational records that coordinate the Workflow and record where work stands; Config does not store what the Target means.
- **Phase** — an ordered stage of the Target, associated with a target Component, on which Planning, Development, and Review can operate.
- **Plan** — the high-level organization of work for a phase, containing Groups, activities, dependencies, and individual Tasks.
- **Task** — one bounded, understandable, and verifiable unit of work within a Plan.
- **Workflow** — the ordered path from the Human's Target definition to developed software: Define Target, Configure, Plan, and Develop, together with supporting operations.
- **Mode** — the current operational position of the Workflow, recorded by State.
- **Operation** — one bounded action performed on the Interface or Target. An Operation may have a Mode or may support the Workflow without one.
- **Skill** — an external Agent capability that performs an Operation or provides a supporting utility; it is cataloged by the Interface but is not part of the Interface Structure.
- **Supporting Agent** — a read-only external capability that reports on the Interface without performing a Workflow Operation.
- **Understanding** — the context an Operation establishes for itself from current sources when it runs. *Agent Interface Understanding* concerns the Interface and resource locations; *Target Understanding* concerns what the Target is and requires.

<br><br>
<!--------------------------------------------------------------------------------- Architecture --->

## Architecture

<!-------------------------- Conceptual Architecture -->
### Conceptual Architecture

The current conceptual architecture is:

```text
Architecture
│
├── Interface
│
├── Target
│   ├── Non-Technical Definition
│   └── Technical Definition
│
├── Developer
│   ├── Principles
│   ├── Preferences
│   └── Components
│       ├── Development
│       ├── Model
│       ├── Database
│       ├── Backend
│       ├── Frontend
│       ├── Platform
│       ├── Plan
│       ├── Review
│       └── State
│           └── Mode
│               ├── Not Set
│               ├── Configuring
│               ├── Planning
│               ├── Development
│               └── Reset
│                   ├── Configure
│                   ├── Plan
│                   └── Develop
│
├── Agent
│   ├── Instances
│   ├── Rules
│   ├── MCP
│   ├── Hooks
│   ├── Plugins
│   ├── Tools
│   ├── Memory
│   ├── Permissions
│   ├── Sandbox
│   ├── Network
│   ├── Sessions
│   ├── Logs
│   └── Skills
│       ├── Configure
│       ├── Plan
│       ├── Develop
│       ├── Review
│       ├── Reset
│       └── Install Skills
│
├── Foundation Files
│   ├── Config
│   │   ├── State
│   │   ├── Plan
│   │   └── Review
│   └── Schema
│       ├── YAML Schema
│       ├── Principles Schema
│       ├── Preferences Schema
│       ├── State Schema
│       ├── Plan Schema
│       └── Review Schema
│
├── Operations
│   ├── Configure
│   ├── Plan
│   ├── Develop
│   ├── Review
│   └── Reset
│
└── Workflow
    ├── Define Target
    ├── Configure
    ├── Plan
    └── Develop
```

<!-------------------------- Repository Structure -->
### Repository Structure

The repository structure maps the conceptual Interface to physical locations. This is the intended structure of the new architecture; existing files can be migrated to it separately without changing the conceptual responsibilities.

```text
project-root/
├── README.md                         # Interface Document
│
├── .interface/                       # Human-owned Interface sources
│   ├── target/
│   │   ├── non-technical/            # Concept, purpose, behavior, and expectations
│   │   └── technical/                # Architecture, Models, constraints, and phases
│   │
│   ├── developer/
│   │   ├── principles/
│   │   │   ├── development.md
│   │   │   ├── model.md
│   │   │   ├── database.md
│   │   │   ├── backend.md
│   │   │   ├── frontend.md
│   │   │   ├── platform.md
│   │   │   ├── plan.md
│   │   │   ├── review.md
│   │   │   └── state.md
│   │   └── preferences/
│   │       ├── development.yaml
│   │       ├── model.yaml
│   │       ├── database.yaml
│   │       ├── backend.yaml
│   │       ├── frontend.yaml
│   │       ├── platform.yaml
│   │       ├── plan.yaml
│   │       ├── review.yaml
│   │       └── state.yaml
│   │
│   └── foundation/
│       ├── config/
│       │   ├── state.yaml
│       │   ├── plan.yaml
│       │   └── review.yaml
│       └── schema/
│           ├── yaml.yaml
│           ├── principles.md
│           ├── preferences.yaml
│           ├── state.yaml
│           ├── plan.yaml
│           └── review.yaml
│
├── .claude/                          # Current Agent integration; outside .interface
│   ├── rules/                        # Shared Agent rules
│   ├── agents/                       # Agent-specific supporting roles
│   ├── skills/                       # Operation and supporting Skills
│   └── settings.json                 # Agent-environment settings
│
├── model/                            # Developed Target package
├── database/                         # Developed Target package
├── backend/                          # Developed Target package
├── frontend/                         # Developed Target package
└── application.yaml                  # Target application composition
```

The tree intentionally omits generated dependencies, virtual environments, build output, caches, and version-control internals. Those files are implementation artifacts rather than Interface architecture.

<!-------------------------- Structure Boundaries -->
### Structure Boundaries

- `README.md` is the Interface Document and the entry point to the architecture.
- `.interface/` contains the Human-owned Target, Developer, and Foundation sources.
- `.claude/` is outside `.interface/`. It is the current Agent-specific implementation of Rules, Skills, supporting Agents, and settings. Another Agent may map the same concepts to different native paths.
- `model/`, `database/`, `backend/`, and `frontend/` are developed Target packages, not definitions of Agent Interface.
- `application.yaml` coordinates the developed application and belongs to the Target implementation rather than Interface Config.
- Operations and Workflow are conceptual responsibilities represented in this document and executed through Agent capabilities; they do not require matching physical directories.



<br><br>
<!--------------------------------------------------------------------------------- Interface --->

## Interface

```text
name = Interface
path = README.md
responsibility = Canonical definition, navigation entry point, and complete file map of Agent Interface
```


<br><br>
<!--------------------------------------------------------------------------------- Target --->

## Target

The Target describes **what the Interface is working on**.

The Target definition is intentionally separated into two levels.

<!-------------------------- Non-Technical Definition -->
### Non-Technical Definition

The Non-Technical Definition explains the Target without requiring detailed software engineering knowledge.

It describes the idea from a conceptual or product perspective.

It may describe:

- purpose,
- expected behavior,
- features,
- user expectations,
- business concepts,
- workflows,
- high-level requirements.

The goal is to answer:

> What are we trying to build?

without requiring implementation decisions.


<!-------------------------- Technical Definition -->
### Technical Definition

The Technical Definition is the professional interpretation of the Target.

A developer converts the initial non-technical concept into a technical representation suitable for implementation by an AI coding agent.

It may describe concepts such as:

- architecture,
- modules,
- data models,
- APIs,
- database responsibilities,
- backend responsibilities,
- frontend responsibilities,
- platform requirements,
- dependencies,
- technical constraints,
- development phases.

The Technical Definition can grow into many files.

There is no requirement that the complete Target understanding live in one document.



<br><br>

## Developer
<!--------------------------------------------------------------------------------- Developer --->
The Developer section describes **how the developer thinks software should be built**.

The goal is not merely to store coding conventions.

It represents the developer's broader engineering personality.

Two developers should be able to use the same Target while producing implementations consistent with their own principles and preferences.

The Developer currently contains three major concepts:

```text
Developer
├── Principles
├── Preferences
└── Components
```


<!-------------------------- Principles -->
### Principles

**Principles** represent the developer's philosophy, engineering beliefs, structural rules, and fundamental expectations.

Principles answer questions such as:

> What does this developer believe good software should look like?

Examples may include ideas such as:

- separation of responsibilities,
- explicit architecture,
- clear boundaries,
- maintainability,
- deterministic behavior,
- testability,
- modularity.

Principles are stronger than Preferences.

They describe how the developer believes the system **should fundamentally behave or be structured**.


<!-------------------------- Preferences -->
### Preferences

**Preferences** describe choices where multiple valid implementations may exist.

They answer:

> When several solutions are acceptable, which one does this developer prefer?

Examples can include:

- framework choices,
- naming preferences,
- organizational patterns,
- coding conventions,
- preferred technologies,
- implementation style.


<!-------------------------- Components -->
### Components

Components divide the developer's programming perspective into specific domains.

```text
Components
├── Development
├── Model
├── Database
├── Backend
├── Frontend
├── Platform
├── Plan
├── Review
└── State
```

A Component can participate in both Principles and Preferences.

Conceptually:

```text
Component × Principle
Component × Preference
```

For example:

```text
Database
├── Principles
└── Preferences
```

or:

```text
Backend
├── Principles
└── Preferences
```

This means Components and Principles/Preferences should be treated as concepts that interact rather than unnecessarily forcing everything into artificial architectural layers.

The design therefore prefers a **concept/object-oriented view** over unnecessary layer-based categorization.


<!-------------------------- Development Component -->
#### Development Component

The Development component represents general software-development philosophy and structure.

It can describe broad rules that affect multiple technical domains.

For example, a developer may define that:

```text
Model
Database
Backend
Frontend
```

must remain conceptually separated.

The more specialized components can then provide rules for each specific area.


<!-------------------------- Model Component -->
#### Model Component

Represents principles and preferences related to application/domain models.


<!-------------------------- Database Component -->
#### Database Component

Represents principles and preferences related to persistence, schemas, queries, migrations, repositories, database design, and related concerns.


<!-------------------------- Backend Component -->
#### Backend Component

Represents principles and preferences related to server-side implementation.


<!-------------------------- Frontend Component -->
#### Frontend Component

Represents principles and preferences related to user-facing applications and UI implementation.


<!-------------------------- Platform Component -->
#### Platform Component

Represents platform-level considerations such as operating environment, deployment target, runtime expectations, or platform-specific development decisions.


<!-------------------------- Plan Component -->
#### Plan Component

The Plan component describes how development work should be represented and organized.

Earlier versions of the Interface used the term `Task` more heavily.

The current conceptual direction prefers **Plan** as the primary concept.

A Plan may still contain individual tasks or execution units internally.

Therefore:

```text
Plan
└── Tasks
```

may remain a valid internal model.

The decision to rename the high-level component from Task to Plan does **not necessarily eliminate the concept of an individual Task**.


<!-------------------------- Review Component -->
#### Review Component

The Review component represents the developer's standards and preferences for evaluating implementation quality.

It is different from the `Review` Operation.

```text
Developer → Review
```

defines **how the developer believes reviews should be performed**.

```text
Operations → Review
```

represents **the actual act of performing a review**.


<!-------------------------- State Component -->
#### State Component

State describes the runtime or workflow state of the Interface.

It contains the Mode concept.

```text
State
└── Mode
```


<!-------------------------- Mode -->
##### Mode

Mode represents the current operational stage of the Interface.

```text
Mode
├── Not Set
├── Configuring
├── Planning
├── Development
└── Reset
    ├── Configure
    ├── Plan
    └── Develop
```

<!-------------------------- Not Set -->
###### Not Set

No active operational mode has been established.

<!-------------------------- Configuring -->
###### Configuring

The Interface is currently performing configuration-related work.

<!-------------------------- Planning -->
###### Planning

The Interface is currently producing or modifying a Plan.

<!-------------------------- Development -->
###### Development

The Interface is currently executing development work.

<!-------------------------- Reset -->
###### Reset

The Interface is currently resetting part of its operational state.

Reset must identify which area is being reset:

```text
Reset
├── Configure
├── Plan
└── Develop
```

This allows the state representation to distinguish different reset operations.



<br><br>

## Agent
<!--------------------------------------------------------------------------------- Agent --->
The Agent section models the execution capabilities and constraints of AI coding agents.

The architecture should work with different agents without being redesigned for each one.

Conceptually:

```text
Agent
├── Instances
├── Rules
├── MCP
├── Hooks
├── Plugins
├── Tools
├── Memory
├── Permissions
├── Sandbox
├── Network
├── Sessions
├── Logs
└── Skills
```

These concepts provide a common abstraction over capabilities that modern coding agents may expose differently.


<!-------------------------- Agent Instances -->
### Agent Instances

Represents one or more execution instances.

An Agent may be able to:

- create sub-agents,
- execute workers,
- perform tasks in parallel,
- delegate work,
- run isolated contexts.

The exact implementation is agent-specific.


<!-------------------------- Agent Rules -->
### Agent Rules

Rules define restrictions, instructions, behavioral expectations, and boundaries applied to the Agent.

Rules are separate from Developer Principles.

Developer Principles describe the developer's engineering philosophy.

Agent Rules govern the **behavior of the executing agent**.


<!-------------------------- MCP -->
### MCP

Represents Model Context Protocol integrations available to the Agent.


<!-------------------------- Hooks -->
### Hooks

Represents lifecycle or execution hooks supported by the Agent environment.


<!-------------------------- Plugins -->
### Plugins

Represents extensible packaged capabilities available to the Agent.

Plugins should remain conceptually independent because different agent platforms may implement plugins differently.


<!-------------------------- Tools -->
### Tools

Represents tools that can be called directly by the Agent.

Tools are not assumed to be identical to Skills, MCP servers, or Plugins.


<!-------------------------- Memory -->
### Memory

Represents agent memory mechanisms and persistent or reusable context.

The Interface does not assume one specific memory implementation.

Future systems may use:

- persistent memory,
- memory graphs,
- contextual memory,
- project memory,
- or other mechanisms.


<!-------------------------- Permissions -->
### Permissions

Defines what the Agent is allowed to access or execute.

It may include:

- filesystem permissions,
- execution permissions,
- approval requirements,
- external-service permissions.


<!-------------------------- Sandbox -->
### Sandbox

Represents execution isolation and environmental restrictions.


<!-------------------------- Network -->
### Network

Represents network-access capabilities and restrictions.


<!-------------------------- Sessions -->
### Sessions

Represents Agent execution sessions or persistent interaction contexts.


<!-------------------------- Logs -->
### Logs

Represents execution history, traceability, debugging information, or audit data generated by Agent activity.


<!-------------------------- Skills -->
### Skills

Skills are executable Agent capabilities.

They can implement Interface Operations or provide supporting utilities.

Current primary Skills are:

```text
Skills
├── Configure
├── Plan
├── Develop
├── Review
├── Reset
└── Install Skills
```

Not every Skill must correspond to an Operation.

For example:

```text
Install Skills
```

is a supporting Agent capability rather than a primary Interface Operation.



<br><br>

## Operations
<!--------------------------------------------------------------------------------- Operations --->
Operations define **what actions the Interface can perform**.

```text
Operations
├── Configure
├── Plan
├── Develop
├── Review
└── Reset
```

Operations are conceptual actions.

Skills are one possible mechanism used by the Agent to execute those actions.

For example:

```text
Operation: Plan
        │
        ▼
Agent Skill: Plan
```

This distinction is important.

The Interface owns the concept of **Plan**.

The Agent owns the mechanism used to perform it.


<!-------------------------- Configure Operation -->
### Configure Operation

Prepares and validates operational configuration required before planning or development.


<!-------------------------- Plan Operation -->
### Plan Operation

Interprets the current Target and Developer context and creates an actionable development plan.

A Plan may contain groups, activities, tasks, dependencies, statuses, or other execution units.


<!-------------------------- Develop Operation -->
### Develop Operation

Executes implementation work based on the Target, Developer rules, current configuration, and Plan.


<!-------------------------- Review Operation -->
### Review Operation

Reviews generated or existing work according to the relevant Target requirements and Developer review principles.


<!-------------------------- Reset Operation -->
### Reset Operation

Resets operational data associated with supported parts of the workflow.

Examples include:

```text
Reset Configure
Reset Plan
Reset Develop
```

Reset is therefore both an Operation and something reflected in State/Mode.



<br><br>

## Understanding
<!--------------------------------------------------------------------------------- Understanding --->
An important design decision was made regarding **Understanding**.

Initially, the architecture considered:

```text
Operation
└── Understand
```

and:

```text
Skill
└── Understand
```

The idea was to create a shared understanding of:

```text
Interface
Developer
Agent
Target
```

and potentially store it for reuse by Plan, Develop, Review, and other operations.

After evaluating this approach, the decision was made **not to make Understanding a mandatory standalone Operation or Skill**.


<!-------------------------- Why Understanding Is Not a Primary Operation -->
### Why Understanding Is Not a Primary Operation

Every operation needs a somewhat different context.

For example:

```text
Plan
```

may require deeper understanding of requirements and decomposition.

```text
Develop
```

may require deeper understanding of implementation files and current code.

```text
Review
```

may require deeper understanding of rules, requirements, and generated changes.

A single summarized Shared Understanding could:

- lose important details,
- become stale,
- consume tokens to generate and maintain,
- or unintentionally constrain operation-specific reasoning.

Therefore, each Skill is responsible for obtaining the context needed for its own role.


<!-------------------------- Context Discovery -->
### Context Discovery

The Interface should still **help the Agent understand the environment**.

Instead of performing Understanding for the Agent, the Interface provides clear navigation and entry points.

For example:

```text
Need Interface context?
    → Start from the Interface Document

Need Target context?
    → Read Target Definitions

Need Developer context?
    → Read Principles, Preferences, Components

Need Agent context?
    → Read Agent Rules and relevant Agent capabilities
```

The goal is:

> Help the Agent find the right context without dictating the Agent's entire reasoning process.

A Skill may then read additional source files whenever necessary.


<!-------------------------- Understanding Principle -->
### Understanding Principle

The resulting rule is:

```text
Each Skill
    ↓
Read relevant entry points
    ↓
Discover required context
    ↓
Read additional sources when needed
    ↓
Perform its role
```

Understanding is therefore a **responsibility of execution**, not a standalone workflow stage.



<br><br>

## Config
<!--------------------------------------------------------------------------------- Config --->
Config contains operational information required by the Interface.

Current high-level configuration concepts are:

```text
Config
├── State
├── Plan
└── Review
```

Config should not be confused with Developer Preferences.

Developer Preferences describe how the developer prefers software to be built.

Config stores operational information used while executing the Interface.


<!-------------------------- State Config -->
### State Config

Stores current execution and workflow state.


<!-------------------------- Plan Config -->
### Plan Config

Stores information related to the generated or active Plan.


<!-------------------------- Review Config -->
### Review Config

Stores operational information related to reviews.



<br><br>

## Foundation Files
<!--------------------------------------------------------------------------------- Foundation Files --->
Foundation Files provide foundational definitions and schemas required by the Interface.

```text
Foundation Files
├── Config
│   ├── State
│   ├── Plan
│   └── Review
└── Schema
    ├── YAML Schema
    ├── Principles Schema
    ├── Preferences Schema
    ├── State Schema
    ├── Plan Schema
    └── Review Schema
```

Target Definitions are intentionally **not** considered Foundation Files because they belong to the Target concept itself.


<!-------------------------- Schema Foundation Files -->
### Schema Foundation Files

Schemas define the structural expectations for machine-readable Interface files.

Their purpose is to ensure that information written by a Developer, Agent, Skill, or Operation follows predictable and valid structures.

```text
Schema
├── YAML Schema
├── Principles Schema
├── Preferences Schema
├── State Schema
├── Plan Schema
└── Review Schema
```


<!-------------------------- YAML Schema -->
#### YAML Schema

The YAML Schema defines shared structural conventions for YAML-based files used by the Interface.

It can define common concepts such as:

- identifiers,
- titles,
- descriptions,
- references,
- versions,
- metadata,
- validation rules,
- extension fields.

Other specialized schemas may build upon these shared conventions.


<!-------------------------- Principles Schema -->
#### Principles Schema

The Principles Schema defines how Developer Principles are represented.

A principle may include information such as:

- identifier,
- component,
- statement,
- rationale,
- scope,
- priority,
- examples,
- related principles.

The final schema should remain flexible enough for different developers to express different engineering philosophies.


<!-------------------------- Preferences Schema -->
#### Preferences Schema

The Preferences Schema defines how Developer Preferences are represented.

A preference may include:

- identifier,
- component,
- preferred choice,
- alternatives,
- rationale,
- conditions,
- priority,
- related preferences.

Preferences should remain distinguishable from mandatory Principles.


<!-------------------------- State Schema -->
#### State Schema

The State Schema defines how current Interface state and Mode are represented.

Conceptually:

```text
State
└── Mode
    ├── Not Set
    ├── Configuring
    ├── Planning
    ├── Development
    └── Reset
        ├── Configure
        ├── Plan
        └── Develop
```

The schema should make state transitions explicit and machine-readable.


<!-------------------------- Plan Schema -->
#### Plan Schema

The Plan Schema defines how a development Plan is represented.

A Plan may contain:

- goals,
- groups,
- phases,
- activities,
- tasks,
- dependencies,
- priorities,
- statuses,
- acceptance criteria,
- references,
- review information.

The exact internal structure may evolve, but the high-level concept remains Plan.


<!-------------------------- Review Schema -->
#### Review Schema

The Review Schema defines how review results are represented.

A Review may include:

- scope,
- criteria,
- findings,
- severity,
- evidence,
- recommendations,
- decisions,
- status,
- references to affected work.

The schema should support both human-readable and agent-readable review output.



<br><br>

## Workflow
<!--------------------------------------------------------------------------------- Workflow --->
The high-level workflow is:

```text
Define Target
      │
      ▼
Configure
      │
      ▼
Plan
      │
      ▼
Develop
```

Review and Reset can be performed when required during this workflow.

A more complete conceptual view is:

```text
Define Target
      │
      ▼
Configure
      │
      ▼
Plan
      │
      ▼
Develop
      │
      ▼
Review
      │
      ├── Approved
      │      │
      │      ▼
      │   Continue
      │
      └── Changes Required
             │
             ▼
          Plan / Develop
```

Reset may act on operational state when part of the workflow needs to be restarted.


<!-------------------------- Define Target -->
### Define Target

The Target begins with a Non-Technical Definition.

A developer then converts or expands that definition into a Technical Definition.

```text
Non-Technical Definition
            │
            ▼
Technical Definition
```

Both definitions belong to the Target.

They should remain independent from the Developer's general programming philosophy and from the capabilities of a particular Agent.


<!-------------------------- Configure -->
### Configure

Configure prepares the Interface for planning and development.

It may determine:

- which Target is active,
- which Developer definition is active,
- which Agent capabilities are available,
- which schemas apply,
- which operational files are present,
- and whether required configuration is valid.

During this operation, the Mode becomes:

```text
Configuring
```


<!-------------------------- Plan -->
### Plan

Plan interprets the relevant Target and Developer context and produces an actionable implementation plan.

During this operation, the Mode becomes:

```text
Planning
```

The Agent performing the Plan operation should discover and read the context required for planning instead of relying on a mandatory pre-generated Understanding document.


<!-------------------------- Develop -->
### Develop

Develop performs implementation work based on the active Plan and relevant Target, Developer, and Agent context.

During this operation, the Mode becomes:

```text
Development
```

Development may be performed sequentially or through multiple Agent Instances when supported.


<!-------------------------- Review -->
### Review

Review evaluates work according to:

```text
Target Requirements
        +
Developer Review Principles
        +
Current Plan
        +
Implementation
```

The Review Operation should produce structured results that can be stored using the Review Config and Review Schema.


<!-------------------------- Reset -->
### Reset

Reset clears or restores operational data for a specific part of the workflow.

```text
Reset
├── Configure
├── Plan
└── Develop
```

Reset should identify its target explicitly so that unrelated information is not unnecessarily removed.





<br><br>

## Concept Relationships
<!--------------------------------------------------------------------------------- Concept Relationships --->
The primary concepts interact as follows:

```text
Interface
│
├── Target
│      Defines what should be built
│
├── Developer
│      Defines how it should be built
│
├── Agent
│      Defines who or what performs the work
│
├── Operations
│      Define what actions can be performed
│
├── Config
│      Stores operational information
│
├── Foundation Files
│      Define shared concepts and structures
│
└── Workflow
       Defines the high-level execution sequence
```


<!-------------------------- Developer and Target Separation -->
### Developer and Target Separation

The Target describes the software subject.

The Developer describes the engineering philosophy used to implement it.

```text
Target
   │
   │  Independent from
   │
Developer
```

The same Target should be usable with different Developer definitions.

Likewise, one Developer definition should be reusable across multiple Targets.


<!-------------------------- Agent and Interface Separation -->
### Agent and Interface Separation

The Interface defines conceptual capabilities.

The Agent maps those concepts to its native mechanisms.

For example:

```text
Interface Concept     Agent-Specific Mechanism
─────────────────     ────────────────────────
Skill                 Native skill system
Tool                  Native tool invocation
Instance              Sub-agent or worker
Memory                Agent memory mechanism
Rule                  Agent instruction system
Plugin                Native extension system
```

This mapping may differ between Codex, Claude Code, or future agents.

The Interface should therefore describe required concepts without requiring one native implementation.


<!-------------------------- Operation and Skill Separation -->
### Operation and Skill Separation

An Operation is an action recognized by the Interface.

A Skill is an Agent capability that may execute that action.

```text
Interface Operation
        │
        ▼
Agent Skill
        │
        ▼
Execution
```

This distinction allows the Interface to remain stable even if different Agents implement operations differently.


<!-------------------------- Principles and Preferences Across Components -->
### Principles and Preferences Across Components

Principles and Preferences apply across Components.

```text
                 Development
                 Model
Principles  ×    Database
Preferences ×    Backend
                 Frontend
                 Platform
                 Plan
                 Review
                 State
```

This relationship should remain flexible.

The architecture should avoid duplicating entire Component structures unnecessarily under both Principles and Preferences when references or structured relationships can express the same information more clearly.





<br><br>


## Important Architectural Decisions
<!--------------------------------------------------------------------------------- Important Architectural Decisions --->
The current design includes the following decisions:

1. **Interface is the complete container.**

   It should not be modeled as a sibling of Target, Developer, or Agent.

2. **Target is preferred over Project.**

   The term avoids ambiguity and supports subjects smaller or larger than a traditional project.

3. **Developer, Agent, and Target remain independent.**

   Each should be replaceable without unnecessarily redesigning the others.

4. **Developer includes Principles, Preferences, and Components.**

   These concepts represent the developer's engineering personality.

5. **Model, Database, Backend, Frontend, and Platform are direct Components.**

   They are not nested under Development.

6. **State is a Developer Component.**

   Mode is located under State.

7. **Mode includes reset-specific states.**

   Reset identifies Configure, Plan, or Develop.

8. **Plan is the primary high-level concept.**

   Individual Tasks may still exist inside a Plan.

9. **Review Component and Review Operation are different concepts.**

   One defines review philosophy; the other performs a review.

10. **Operations come after Agent in the architecture.**

    The Agent provides the capabilities used to execute Interface Operations.

11. **Understanding is not a mandatory standalone Operation or Skill.**

    Each Skill discovers and reads the context required for its own responsibility.

12. **Target Definitions are not Foundation Files.**

    They belong to the Target.

13. **Agent technologies remain independent concepts.**

    Skills, Tools, Plugins, MCP, Hooks, Memory, Rules, and Instances should not be treated as interchangeable.

14. **The architecture favors concepts and relationships over artificial layers.**

    The goal is to model the system clearly without forcing every idea into a rigid hierarchy.





<br><br>

## Implementation Neutrality
<!--------------------------------------------------------------------------------- Implementation Neutrality --->
This document intentionally describes the conceptual Interface rather than committing to one technical implementation.

Possible implementation mechanisms include:

- Markdown files,
- YAML configuration,
- JSON Schema,
- agent skills,
- MCP servers,
- plugins,
- hooks,
- command-line tools,
- local or persistent memory,
- multiple Agent Instances,
- validation tools.

The implementation may change as agent technology evolves.

The conceptual relationships should remain stable.





<br><br>

## Guiding Principle
<!--------------------------------------------------------------------------------- Guiding Principle --->
The Interface should give an Agent enough structure to reliably discover:

```text
What is being built?
How should it be built?
What capabilities are available?
What operation should be performed?
Where is the required context?
```

It should guide execution without unnecessarily controlling the Agent's complete reasoning process.





<br><br>

## Summary
<!--------------------------------------------------------------------------------- Summary --->
Agent Interface is a reusable conceptual environment connecting:

```text
Developer
Agent
Target
Operations
Config
Foundation Files
Workflow
```

The Target defines the subject.

The Developer defines the engineering philosophy.

The Agent provides execution capabilities and operates within its rules and restrictions.

Operations define the actions the Interface supports.

Config stores operational state and results.

Foundation Files define shared concepts and schemas.

Workflow connects these concepts into an executable development process.

The resulting Interface should be:

- agent-independent,
- developer-independent,
- target-independent,
- structured,
- discoverable,
- extensible,
- machine-readable,
- and understandable by both humans and AI coding agents.
