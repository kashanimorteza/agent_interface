# Agent Interface


<!--------------------------------------------------------------------------------- Map --->
<br > <br>

## Map

Use this document as the entry point and follow its sections in this order:

1. **Introduction** — understand the purpose, operation, and boundaries of Agent Interface.
2. **Terms** — learn the vocabulary the rest of this document and every Component use.
3. **Foundational Files** — locate the Interface document, human project definition, and Schema foundation.
4. **Layers** — understand how Principles, Preferences, and Config represent each Component.
5. **Authority and Ownership** — know which record belongs to whom, and which operation may write it.
6. **Component** — locate every Component's Principle and Preference files, plus the Schema and Config files of the Components that keep operational records.
7. **Modes** — understand the operating states used to configure, plan, and develop a project.
8. **Core Interface Skills** — locate the external capabilities that perform Interface operations.
9. **Workflow** — follow the ordered human-facing path from project definition to development.
10. **Supporting Operations** — locate Review, Reset, and Skill Installation, which support the Workflow without adding a step.




<!--------------------------------------------------------------------------------- Introduction --->
<br > <br>

## Introduction

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

<!-------------------------- Document -->
### Document

`interface.md` is the canonical introduction and navigation entry point of Agent Interface. It explains the system and locates every current resource, Component, Layer, Agent Skill, Mode, and Workflow step.

Agent Interface operations and supporting Agents must not edit this file. If an operation determines that it should change, the operation reports the required change to the human and leaves the file untouched. Live Workflow position belongs to the State Component; this document only explains and locates it.



<!--------------------------------------------------------------------------------- Terms --->
<br > <br>

## Terms

- **Human** — the person who defines the target project and owns every authored Interface source.
- **Target Project** — the software the Human defines and the Agents build; it is described by the project definition and never by the Interface itself.
- **Component** — one named part of the Interface that holds a responsibility and describes itself through its own Principles and Preferences; some Components also keep an operational record.
- **Layer** — one of the three forms a Component takes: Principles for what is mandatory, Preferences for what is chosen when the project is silent, and Config for what is currently recorded.
- **Schema** — the structure a file follows: a structure standard for a file the Human authors, or an operational format for a file an operation generates, together with the initial template it starts from.
- **Config** — the mutable operational records that coordinate the Workflow; they hold where things stand, never what the project means.
- **Phase** — one stage of the target project as the Human defines it, each targeting one Component; the unit that Planning, Development, and Review act on.
- **Workflow** — the ordered path from the Human's project definition to a developed project — Define, Configure, Plan, Develop — together with the operations that support it without adding a step.
- **Mode** — the position the Workflow currently occupies, drawn from a fixed set of values and recorded by State.
- **Operation** — one bounded piece of work performed on the Interface or the project. An operation may execute a Mode, or support the Workflow without one.
- **Skill** — the external capability that performs an operation; catalogued by the Interface but not part of its structure.
- **Supporting Agent** — a read-only external capability that reports on the Interface and performs no operation.
- **Understanding** — what an operation establishes for itself at the moment it runs, by reading the current sources; it is never stored. *Agent Interface Understanding* is knowing how the Interface is organized and where each resource is; *Target Project Understanding* is knowing what the target project is and requires.



<!--------------------------------------------------------------------------------- Foundational files --->
<br > <br>

## Foundational files

### Interface

```text
name = Interface
path = .interface/foundation/interface.md
responsibility = Canonical definition, navigation entry point, and complete file map of Agent Project Interface
```

### Project

```text
name = Project
path = .interface/target/non-technical.md
responsibility = Human-managed natural-language definition of the target project being built
```

### Schema

```text
name = Schema
path = .interface/foundation/schema/
responsibility = The structure of every Interface file: the common YAML frame, the structure standards for the Principles and Preferences layers, and the operational storage format of every Component that keeps a record; contains no project description or stored Understanding
```

Schema holds two kinds of document. A **structure standard** defines the shape of a file a human authors, so that every Component writes the same kind of file the same way. An **operational format** defines the shape of a file an operation generates, and carries the initial template that operation copies. Each is listed below.

<!-------------------------- YAML Schema -->
#### YAML Schema

```text
name = YAML Schema
path = .interface/foundation/schema/yaml.yaml
kind = structure standard
responsibility = The common structural frame every YAML Interface file follows: meta, policy, read_order, content_map, content
applies_to = Every Interface YAML file, including Preferences and Config
note = It defines the outer sections only. What goes inside content belongs to the schema of that kind of file, and every other YAML schema inherits this frame rather than redefining it
```

<!-------------------------- Principles Schema -->
#### Principles Schema

```text
name = Principles Schema
path = .interface/foundation/schema/principles.md
kind = structure standard
responsibility = The common Markdown structure every Principles file follows: Introduction, Terms, Relationships, Layering, Authority, the numbered Principles, and At a Glance
applies_to = Every file under .interface/developer/
note = Each Principle carries Rule, Why, and Boundary. A Principle number is permanent once assigned. A Principles file names no tool, version, package, file, or path, states no technical default, and refers to no Skill, operation, or usage condition
```

<!-------------------------- Preferences Schema -->
#### Preferences Schema

```text
name = Preferences Schema
path = .interface/foundation/schema/preferences.yaml
kind = structure standard
responsibility = The structure of the content section of every Preferences file, and the meta and policy expectations a Preferences file adds to the common YAML frame
applies_to = Every file under .interface/developer/
note = Content is always selected, options, and settings, present even when empty. Selected holds the choices, options the supported alternatives, and settings the configuration of what was chosen, grouped by the Component's own layers
```

<!-------------------------- State Schema -->
#### State Schema

```text
name = State Schema
path = .interface/foundation/schema/state.yaml
kind = operational format
responsibility = The stored shape of the State Config file, and the initial template Configure copies to create it
generates = .interface/foundation/config/state.yaml
note = It records Workflow position, Blockers, and Open Questions only. Project concepts, resolved technical choices, and Task content are excluded and resolved from their own sources
```

<!-------------------------- Task Schema -->
#### Task Schema

```text
name = Task Schema
path = .interface/foundation/schema/plan.yaml
kind = operational format
responsibility = The stored shape of the Task Config file, and the initial template Configure copies to create it
generates = .interface/foundation/config/plan.yaml
note = It records which work exists, what each activity must produce, what it depends on, where it stands, and its history. Context is stored once at the highest level where it holds, no record names a file or path, and nothing derivable from the project definition, the Principles, or the Preferences is stored here
```

<!-------------------------- Review Schema -->
#### Review Schema

```text
name = Review Schema
path = .interface/foundation/schema/review.yaml
kind = operational format
responsibility = The stored shape of the Review Config file, and the initial template Configure copies to create it
generates = .interface/foundation/config/review.yaml
note = It records which phases were reviewed, the outcome of each, and every Finding with what was expected, what was observed, the evidence for it, and where it stands. A Finding refers to what it judged and never restates it
```


<!--------------------------------------------------------------------------------- Layers --->
<br > <br>

## Layers

Every Component has Principles and Preferences. The Config layer contains only the operational records of the Components that keep one, and the Component section lists them; other Components have no Interface Config or dedicated Schema. An empty Preference file contributes no defaults, so consumers use the other applicable sources.

Application runtime settings, such as database connections and service configuration, remain part of the target application's implementation under Development and Platform. They are distinct from the Interface Config layer.

### Principles

```text
name = Principles
path = .interface/developer/
responsibility = Mandatory philosophy, responsibilities, and boundaries, independent of tools and versions
answers = Why and under what rules
```

### Preferences

```text
name = Preferences
path = .interface/developer/
responsibility = Supported technical choices and defaults used when the target project leaves a choice unstated; an explicit project choice wins
answers = With what
```

### Config

```text
name = Config
path = .interface/foundation/config/
responsibility = Stores the operational record of every Component that keeps one: planned work and its progress, the active Workflow position, Blockers and Open Questions, and recorded review Findings
answers = What work is recorded, where the Workflow currently stands, and what review has established
initialization = Copy the initial template from each operational Schema; later operations update the stored values
```


<!--------------------------------------------------------------------------------- Authority and Ownership --->
<br > <br>

## Authority and Ownership

Explicit project intent and applicable Principles guide each operation. Preferences supply defaults where the project leaves a choice unstated. The operational Schemas define the shape of operational records, the Principles and Preferences Schemas define the shape of the authored layers, and the general YAML Schema supplies the common frame every YAML file shares. Config stores those records and does not define the target project.

```text
Project = human-defined intent
Principles = mandatory philosophy, responsibilities, and boundaries
Preferences = technical defaults for unspecified choices
Schema = general YAML frame, authored-layer structure, and the storage structure of every operational record
Config = the mutable operational records
```

Ownership answers who a record belongs to, and it belongs to the Human or to a Component:

```text
Human = owns Interface, Project, Principles, Preferences, and Schema sources
Task = owns Plans, Groups, Tasks, their status, and their history
State = owns the active Workflow position, Blockers, and Open Questions
Review = owns recorded Findings and their state
```

Write authority answers which operation may change a record, and every write happens under the rules of the Component that owns it:

```text
Configure = writes every operational Config, creating it from its Schema template or bringing it to the current structure
Planning = writes Plans, Groups, and Tasks under Task's rules
Development = writes implementation, and Task status and history under Task's rules
Review = writes Findings under Review's rules
Every operation = writes the active Workflow position and its own Blockers and Open Questions under State's rules
```

Each operation writes only the records it has authority over, and always under the rules of the Component that owns them. Operational records follow their source authorities and must not redefine them.


<!--------------------------------------------------------------------------------- Component --->
<br > <br>

## Component

<!-------------------------- Development -->
### Development

```text
name = Development
responsibility = Independent Model, Database, Backend, and Frontend layers; centralized runtime configuration; declared-interface connections; cross-cutting capabilities; and Platform composition
principle = .interface/developer/development/principles.md
preference = .interface/developer/development/preferences.yaml
```

<!-------------------------- Model -->
### Model

```text
name = Model
responsibility = Independent shared Model package and logical domain Models, including fields, relationships, rules, validation, and initial data
principle = .interface/developer/model/principles.md
preference = .interface/developer/model/preferences.yaml
```

<!-------------------------- Database -->

### Database

```text
name = Database
responsibility = Independent package with typed Model operations, supported Engines, selectable Instances, Model-driven mapping, and Storage Adapters
principle = .interface/developer/database/principles.md
preference = .interface/developer/database/preferences.yaml
```
<!-------------------------- Backend -->

### Backend

```text
name = Backend
responsibility = Application and Model Logic, Database communication through Data Access, and the external API
principle = .interface/developer/backend/principles.md
preference = .interface/developer/backend/preferences.yaml
```

<!-------------------------- Frontend -->

### Frontend

```text
name = Frontend
responsibility = Component-based Presentation, user Interaction Logic, and application access through the Backend API
principle = .interface/developer/frontend/principles.md
preference = .interface/developer/frontend/preferences.yaml
```

<!-------------------------- State -->

### State

```text
name = State
responsibility = Current Workflow position, repeatable Modes, critical Blockers, and Open Questions
principle = .interface/developer/state/principles.md
preference = .interface/developer/state/preferences.yaml
schema = .interface/foundation/schema/state.yaml
config = .interface/foundation/config/state.yaml
```

<!-------------------------- Task -->

### Task

```text
name = Task
responsibility = Phase Plans, coherent Groups, atomic Tasks, progress, and Task-local history
principle = .interface/developer/plan/principles.md
preference = .interface/developer/plan/preferences.yaml
schema = .interface/foundation/schema/plan.yaml
config = .interface/foundation/config/plan.yaml
```

<!-------------------------- Review -->

### Review

```text
name = Review
responsibility = Independent judgement of an implemented phase against what was asked, and the recorded Findings and their state
principle = .interface/developer/review/principles.md
preference = .interface/developer/review/preferences.yaml
schema = .interface/foundation/schema/review.yaml
config = .interface/foundation/config/review.yaml
```





<!--------------------------------------------------------------------------------- Modes --->
<br > <br>

## Modes

State records the active Mode. Agent Skills are external capabilities that perform the operations represented by Modes. These Modes are distinct from target-project Behaviours, which describe what the target application must do.

<!-------------------------- Not Set -->
### Not Set

- **State value:** `not set`
- **Phase-specific:** no
- **Responsibility:** represents the initial Workflow position before an operation has been recorded, or the position restored by an applicable reset.
- **Inputs:** none.
- **Output:** active State with no phase.

<!-------------------------- Configuring -->
### Configuring

- **State value:** `configuring`
- **Phase-specific:** no
- **Responsibility:** initializes the mutable Config files from their Schema templates.
- **Inputs:** every operational Schema, the common YAML Schema, and any existing operational records.
- **Initialization:** copy each Schema's `initial` mapping into its mapped Config file when that file is absent. Copy the template values, not the Schema definitions.
- **Preservation:** keep every operational record a Config file already holds; the owning Schema states what those are. An existing valid file needs no rewrite. A Schema mismatch requires a data-preserving update; a conflict must be surfaced rather than resolved by resetting work.
- **Validation:** check each Config file against the common file frame and its operational Schema.
- **Output:** `.interface/foundation/config/plan.yaml`, `.interface/foundation/config/state.yaml`, and `.interface/foundation/config/review.yaml`.

Configuring does not produce project descriptions, technical Component configurations, or phase Plan shells. Planning creates actual Plans for requested phases. State's initial template is `not set`; a running operation records its actual mode, provenance, and time according to the State Component.

<!-------------------------- Planning -->
### Planning

- **State value:** `planning`
- **Phase-specific:** yes
- **Responsibility:** uses current Target Project Understanding for one requested phase to create bounded, verifiable activities without prescribing implementation.
- **Inputs:** the requested phase in `.interface/target/non-technical.md`, applicable Principles and Preferences, current Task and State records, and the gap Findings recorded for that phase.
- **Scope:** the requested phase; its target selects the Component being planned.
- **Output:** `.interface/foundation/config/plan.yaml`.

<!-------------------------- Development -->
### Development

- **State value:** `development`
- **Phase-specific:** yes
- **Responsibility:** executes and verifies eligible planned Tasks to produce project implementation.
- **Inputs:** `.interface/target/non-technical.md`, applicable Principles and Preferences, the current implementation, and Task and State records.
- **Scope:** the requested phase; its target selects the Component being developed.
- **Output:** implementation inside the selected Component's resolved code boundary.






<!--------------------------------------------------------------------------------- Agent Skills --->
<br > <br>

## Core Interface Skills

Core Interface Skills are the fixed external capabilities that execute Interface Modes or supporting operations. Their integration metadata does not define the Interface Structure, grant authority, or replace the instructions and shared rules owned by the Claude configuration layer. Technology-specific or third-party Skills are discovered dynamically from the current target project and are not part of this fixed catalog; adding or removing one must not require an Interface change.

### Shared Skill Rules

```text
name = Interface Bootstrap
path = .claude/rules/interface-bootstrap.md
responsibility = Defines shared entry points and the separation between Agent Skills and the Interface Structure
```

```text
name = Interface Skill Policy
path = .claude/rules/interface-skill-policy.md
responsibility = Defines human-owned file boundaries and the decision policy shared by every Skill
```


<!-------------------------- Configure -->
### Configure

```text
name = my-interface-configure
path = .claude/skills/my-interface-configure/SKILL.md
invocation = /my-interface-configure
responsibility = Initialize every operational Config from its Schema template and bring an existing one to the current structure, preserving existing records
mode = configuring
```
<!-------------------------- Tasker -->
### Tasker

```text
name = my-interface-tasker
path = .claude/skills/my-interface-tasker/SKILL.md
invocation = /my-interface-tasker <phase-number>
responsibility = Create or reconcile an activity Plan with expected results and verification without prescribing implementation
mode = planning
```
<!-------------------------- Developer -->
### Developer

```text
name = my-interface-developer
path = .claude/skills/my-interface-developer/SKILL.md
invocation = /my-interface-developer <phase-number>
responsibility = Implement and verify eligible planned Tasks for one requested phase
mode = development
```
<!-------------------------- Reviewer -->
### Reviewer

```text
name = my-interface-reviewer
path = .claude/skills/my-interface-reviewer/SKILL.md
invocation = /my-interface-reviewer <phase-number>
responsibility = Review one implemented phase, record evidence-based Findings in the Review Config, and report them without repairing the result
mode = none
```
<!-------------------------- Reset -->
### Reset

```text
name = my-interface-reset
path = .claude/skills/my-interface-reset/SKILL.md
invocation = /my-interface-reset <1|2|3>
responsibility = Preview and, after human confirmation, reset Configure output, Task output, or developed implementation
mode = none
```
<!--------------------------  Skill Installer -->
### Skill Installer

```text
name = my-interface-skill-installer
path = .claude/skills/my-interface-skill-installer/SKILL.md
invocation = /my-interface-skill-installer
responsibility = Discover and install compatible Agent Skills for technologies identified from the current project sources and implementation
mode = none
```

### Supporting Agents

A supporting Agent is a read-only capability invoked by another operation or by the human. It executes no Workflow Mode and writes nothing.

```text
name = interface-reader
path = .claude/agents/interface-reader.md
responsibility = Report where the build stands from the current operational Config records: active mode and phase, phase plans and counts, eligible work, Blockers, Open Questions, and open review Findings, each cited to its source
mode = none
writes = none
```


The reset stages are:

1. **Configure:** remove root implementation directories when present and clear every entry inside `.interface/foundation/config/`.
2. **Task:** remove root implementation directories, clear Groups and Tasks while preserving phase Plan shells, clear the recorded Findings for the affected phases, set active State to `not set`, and clear the active phase.
3. **Develop:** remove root implementation directories, preserve Tasks and their history while returning every Task to `todo`, clear the recorded Findings for the affected phases, set active State to `planning`, and clear the active phase.

Reset resolves the implementation directories it may remove from the code path each Component records in its own Preferences. It removes no directory that no Component claims, and this document holds no list of its own.




<!--------------------------------------------------------------------------------- Workflow --->
<br > <br>

## Workflow

<!-------------------------- Define the Project -->
### Define the Project

```text
order = 1
name = Define the Project
actor = Human
action = Define the target project, its Models, and its ordered phases in .interface/target/non-technical.md
```
<!-------------------------- Configure -->
### Configure

```text
order = 2
name = Configure
skill = /my-interface-configure
action = Initialize every operational Config file under .interface/foundation/config/ from the initial template in its Schema; preserve existing operational records
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


<!--------------------------------------------------------------------------------- Supporting Operations --->
<br > <br>

## Supporting Operations

These operations support the main Define → Configure → Plan → Develop Workflow without adding a new Workflow Mode or changing the ordered path.

### Review

```text
skill = /my-interface-reviewer <phase-number>
when = After Development, when the implemented result needs independent verification
action = Inspect the requested phase against the current project definition, applicable Principles and Preferences, and Plan, then record evidence-based Findings in .interface/foundation/config/review.yaml and report them without repairing the result
state = Does not enter or change a Workflow Mode
```

### Reset

```text
skill = /my-interface-reset <1|2|3>
when = On explicit human request, whenever a selected Workflow stage must be reset
action = Preview and, after confirmation, reset the selected Configure, Task, or Development output
state = Does not add a new Workflow Mode; it restores State according to the selected reset stage
```

### Skill Installation

```text
skill = /my-interface-skill-installer
when = When the target project requires a compatible technology Skill
action = Discover and, after approval, install or refresh the matching external Skill
state = Does not enter or change a Workflow Mode
```
