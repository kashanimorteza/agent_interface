# Agent Interface


<!--------------------------------------------------------------------------------- Map --->
<br > <br>

## Map

Use this document as the entry point and follow its sections in this order:

1. **Introduction** — understand the purpose, operation, and boundaries of Agent Interface.
2. **Foundational Files** — locate the Interface document, human project definition, and Schema foundation.
3. **Layers** — understand how Principles, Preferences, and Config represent each Component.
4. **Component** — locate every Component's Principle and Preference files, plus Task and State Schema and Config files.
5. **Modes** — understand the operating states used to configure, plan, and develop a project.
6. **Core Interface Skills** — locate the external capabilities that perform Interface operations.
7. **Workflow** — follow the ordered human-facing path from project definition to development.




<!--------------------------------------------------------------------------------- Introduction --->
<br > <br>

## Introduction

<!-------------------------- Purpose -->
### Purpose

Agent Interface is an independent interface between **Developers** and **AI Agents** for establishing a common protocol, structure, and standard for software development.

Its purpose is to let a Developer define a target project in natural language and give Agents common Principles and Preferences for understanding, planning, and developing it.

<!-------------------------- Operation -->
### Operation

The Developer supplies the human project definition. Each operation reads it and the applicable Principles and Preferences to establish its own Understanding. Planning records activities as Tasks; Development implements and verifies those Tasks.

Config contains only the mutable Task and State files used to coordinate this work. Schemas define their storage format. Understanding is formed by each operation and is not stored in Config.

<!-------------------------- Independence -->
### Independence

The core Interface Structure is independent of any specific AI model, Agent, or external execution capability. Agent Skills are cataloged as integrations, not as parts of the Structure.

Human project definitions remain flexible, while the Interface gives Agents stable responsibilities, rules, defaults, and operational records. Agent Interface is the communication boundary between those two forms.

<!-------------------------- Document -->
### Document

`interface.md` is the canonical introduction and navigation entry point of Agent Interface. It explains the system and locates every current resource, Component, Layer, Agent Skill, Mode, and Workflow step.

Agent Interface operations and supporting Agents must not edit this file. If an operation determines that it should change, the operation reports the required change to the human and leaves the file untouched. Live Workflow position belongs to the State Component; this document only explains and locates it.



<!--------------------------------------------------------------------------------- Foundational files --->
<br > <br>

## Foundational files

### Interface

```text
name = Interface
path = .interface/interface.md
responsibility = Canonical definition, navigation entry point, and complete file map of Agent Project Interface
```

### Project

```text
name = Project
path = .interface/project.md
responsibility = Human-managed natural-language definition of the target project being built
```

### Schema

```text
name = Schema
path = .interface/schema/
responsibility = Common YAML file frame and the operational storage formats for Task and State; contains no project description or stored Understanding
```

### File Schema

```text
name = File Schema
path = .interface/schema/file.yaml
responsibility = Common structural frame used by Interface YAML Preferences and Config files
```


<!--------------------------------------------------------------------------------- Layers --->
<br > <br>

## Layers

Every Component has Principles and Preferences. The Config layer contains only Task and State operational records; other Components have no Interface Config or dedicated Schema. An empty Preference file contributes no defaults, so consumers use the other applicable sources.

Application runtime settings, such as database connections and service configuration, remain part of the target application's implementation under Development and Platform. They are distinct from the Interface Config layer.

### Principles

```text
name = Principles
path = .interface/principles/
responsibility = Mandatory philosophy, responsibilities, and boundaries, independent of tools and versions
answers = Why and under what rules
```

### Preferences

```text
name = Preferences
path = .interface/preferences/
responsibility = Supported technical choices and defaults used when the target project leaves a choice unstated; an explicit project choice wins
answers = With what
```

### Config

```text
name = Config
path = .interface/config/
responsibility = Stores task.yaml and state.yaml: mutable planning records, execution progress, active Workflow position, Blockers, and Open Questions
answers = What work is recorded and where the Workflow currently stands
initialization = Copy the initial template from each of the two operational Schemas; later operations update the stored values
```


<!--------------------------------------------------------------------------------- Authority and Ownership --->
<br > <br>

## Authority and Ownership

Explicit project intent and applicable Principles guide each operation. Preferences supply defaults where the project leaves a choice unstated. Task and State Schemas define the shape of operational records; the general File Schema supplies their common YAML frame. Config stores those records and does not define the target project.

```text
Project = human-defined intent
Principles = mandatory philosophy, responsibilities, and boundaries
Preferences = technical defaults for unspecified choices
Schema = general YAML frame and Task/State storage structure
Config = mutable Task and State records
```

```text
Human = owns Interface, Project, Principles, Preferences, and Schema sources
Interpreter = initializes the mapped Config files from their Schema templates, preserving existing operational data
Tasker = owns Plans, Groups, and Tasks
Developer = owns implementation and execution progress
Reviewer = owns verification findings and reports
State = owns active Workflow position, Blockers, and Open Questions
```

Each operation may change only the information owned by its current authority. Operational records follow their source authorities and must not redefine them.


<!--------------------------------------------------------------------------------- Component --->
<br > <br>

## Component

<!-------------------------- Development -->
### Development

```text
name = Development
responsibility = Independent Model, Database, Backend, and Frontend layers; centralized runtime configuration; declared-interface connections; cross-cutting capabilities; and Platform composition
principle = .interface/principles/development.md
preference = .interface/preferences/development.yaml
```

<!-------------------------- Model -->
### Model

```text
name = Model
responsibility = Independent shared Model package and logical domain Models, including fields, relationships, rules, validation, and initial data
principle = .interface/principles/model.md
preference = .interface/preferences/model.yaml
```

<!-------------------------- Database -->

### Database

```text
name = Database
responsibility = Independent package with typed Model operations, supported Engines, selectable Instances, Model-driven mapping, and Storage Adapters
principle = .interface/principles/database.md
preference = .interface/preferences/database.yaml
```
<!-------------------------- Backend -->

### Backend

```text
name = Backend
responsibility = Application and Model Logic, Database communication through Data Access, and the external API
principle = .interface/principles/backend.md
preference = .interface/preferences/backend.yaml
```

<!-------------------------- Frontend -->

### Frontend

```text
name = Frontend
responsibility = Component-based Presentation, user Interaction Logic, and application access through the Backend API
principle = .interface/principles/frontend.md
preference = .interface/preferences/frontend.yaml
```

<!-------------------------- State -->

### State

```text
name = State
responsibility = Current Workflow position, repeatable Modes, critical Blockers, and Open Questions
principle = .interface/principles/state.md
preference = .interface/preferences/state.yaml
schema = .interface/schema/state.yaml
config = .interface/config/state.yaml
```

<!-------------------------- Task -->

### Task

```text
name = Task
responsibility = Phase Plans, coherent Groups, atomic Tasks, progress, and Task-local history
principle = .interface/principles/task.md
preference = .interface/preferences/task.yaml
schema = .interface/schema/task.yaml
config = .interface/config/task.yaml
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
- **Responsibility:** initializes the two mutable Config files from their Schema templates.
- **Inputs:** the Task and State Schemas, the common File Schema, and any existing operational records.
- **Initialization:** copy each Schema's `initial` mapping into its mapped Config file when that file is absent. Copy the template values, not the Schema definitions.
- **Preservation:** keep existing Tasks, progress, active State, Blockers, and questions. An existing valid file needs no rewrite. A Schema mismatch requires a data-preserving update; a conflict must be surfaced rather than resolved by resetting work.
- **Validation:** check each Config file against the common file frame and its operational Schema.
- **Output:** `.interface/config/task.yaml` and `.interface/config/state.yaml`.

Configuring does not produce project descriptions, technical Component configurations, or phase Plan shells. Planning creates actual Plans for requested phases. State's initial template is `not set`; a running operation records its actual mode, provenance, and time according to the State Component.

<!-------------------------- Planning -->
### Planning

- **State value:** `planning`
- **Phase-specific:** yes
- **Responsibility:** uses current Target Project Understanding for one requested phase to create bounded, verifiable activities without prescribing implementation.
- **Inputs:** the requested phase in `.interface/project.md`, applicable Principles and Preferences, and current Task and State records.
- **Scope:** the requested phase; its target selects the Component being planned.
- **Output:** `.interface/config/task.yaml`.

<!-------------------------- Development -->
### Development

- **State value:** `development`
- **Phase-specific:** yes
- **Responsibility:** executes and verifies eligible planned Tasks to produce project implementation.
- **Inputs:** `.interface/project.md`, applicable Principles and Preferences, the current implementation, and Task and State records.
- **Scope:** the requested phase; its target selects the Component being developed.
- **Output:** implementation inside the selected Component's resolved code boundary.






<!--------------------------------------------------------------------------------- Agent Skills --->
<br > <br>

## Core Interface Skills

Core Interface Skills are the fixed external capabilities that execute Interface Modes or supporting operations. Their integration metadata does not define the Interface Structure, grant authority, or replace the instructions and shared rules owned by the Claude configuration layer. Technology-specific or third-party Skills are discovered dynamically from the configured target project and are not part of this fixed catalog; adding or removing one must not require an Interface change.

### Shared Skill Rules

```text
name = Interface Bootstrap
path = .claude/rules/interface-bootstrap.md
responsibility = Defines shared Understanding and the separation between Agent Skills and the Interface Structure
```

```text
name = Interface Skill Policy
path = .claude/rules/interface-skill-policy.md
responsibility = Defines shared file boundaries, Workflow, decision policy, and Development authority
```


<!-------------------------- Interpreter -->
### Interpreter

```text
name = my-interface-interpreter
path = .claude/skills/my-interface-interpreter/SKILL.md
invocation = /my-interface-interpreter
responsibility = Initialize Task and State Config from their Schema templates, preserving existing records
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
responsibility = Review one implemented phase and report evidence-based findings without repairing it
mode = none
```
<!-------------------------- Reset -->
### Reset

```text
name = my-interface-reset
path = .claude/skills/my-interface-reset/SKILL.md
invocation = /my-interface-reset <1|2|3>
responsibility = Preview and, after human confirmation, reset Interpreter output, Task output, or developed implementation
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


The reset stages are:

1. **Interpreter:** remove root implementation directories when present and clear every entry inside `.interface/config/`.
2. **Task:** remove root implementation directories, clear Groups and Tasks while preserving phase Plan shells, set active State to `not set`, and clear the active phase.
3. **Develop:** remove root implementation directories, preserve Tasks and their history while returning every Task to `todo`, set active State to `planning`, and clear the active phase.

The fixed root implementation directories currently recognized by Reset are `model/`, `database/`, `backend/`, `frontend/`, and `developer/`.




<!--------------------------------------------------------------------------------- Workflow --->
<br > <br>

## Workflow

<!-------------------------- Define the Project -->
### Define the Project

```text
order = 1
name = Define the Project
actor = Developer
action = Define the target project, its Models, and its ordered phases in .interface/project.md
```
<!-------------------------- Interpret the Project -->
### Initialize Config

```text
order = 2
name = Initialize Config
skill = /my-interface-interpreter
action = Initialize .interface/config/task.yaml and .interface/config/state.yaml from the initial templates in their Schemas; preserve existing operational records
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

These operations support the main Define → Initialize → Plan → Develop Workflow without adding a new Workflow Mode or changing the ordered path.

### Review

```text
skill = /my-interface-reviewer <phase-number>
when = After Development, when the implemented result needs independent verification
action = Inspect the requested phase against the current project definition, applicable Principles and Preferences, and Plan, then report evidence-based findings without repairing it
state = Does not enter or change a Workflow Mode
```

### Reset

```text
skill = /my-interface-reset <1|2|3>
when = On explicit human request, whenever a selected Workflow stage must be reset
action = Preview and, after confirmation, reset the selected Interpreter, Task, or Development output
state = Does not add a new Workflow Mode; it restores State according to the selected reset stage
```

### Skill Installation

```text
skill = /my-interface-skill-installer
when = When the target project requires a compatible technology Skill
action = Discover and, after approval, install or refresh the matching external Skill
state = Does not enter or change a Workflow Mode
```
