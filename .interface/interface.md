# Agent Interface


<!--------------------------------------------------------------------------------- Map --->
<br > <br>

## Map

Use this document as the entry point and follow its sections in this order:

1. **Introduction** — understand the purpose, operation, and boundaries of Agent Interface.
2. **Foundational Files** — locate the Interface document, human project definition, and Schema foundation.
3. **Layers** — understand how Principles, Preferences, and Config represent each Component.
4. **Component** — locate every Component's Principle, Preference, Schema, and Config files.
5. **Modes** — understand the operating states used to configure, plan, and develop a project.
6. **Agent Skills** — locate the external capabilities that perform Interface operations.
7. **Workflow** — follow the ordered human-facing path from project definition to development.




<!--------------------------------------------------------------------------------- Introduction --->
<br > <br>

## Introduction

<!-------------------------- Purpose -->
### Purpose

Agent Interface is an independent interface between **Developers** and **AI Agents** for establishing a common protocol, structure, and standard for software development.

Its purpose is to let a Developer define a target project in natural language and turn that definition into explicit, predictable project Understanding that Agents can plan against and develop.

<!-------------------------- Operation -->
### Operation

The Developer supplies the human project definition. Agent Interface resolves it through shared Principles, Preferences, and Schemas into generated Component Config. Planning turns that generated Understanding into Tasks, and Development implements and verifies those Tasks.

Agents therefore consume stable, structured information instead of reconstructing the entire target project from conversation during every operation.

<!-------------------------- Independence -->
### Independence

The core Interface Structure is independent of any specific AI model, Agent, or external execution capability. Agent Skills are cataloged as integrations, not as parts of the Structure.

Human project definitions remain flexible, while the Interface gives Agents stable responsibilities, rules, defaults, formats, and generated outputs. Agent Interface is the communication boundary between those two forms.

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
responsibility = Foundational shapes and validation rules for generated Component configuration; contains no Component philosophy or technical preference
```


<!--------------------------------------------------------------------------------- Layers --->
<br > <br>

## Layers

Each Component has one stable file in every Layer. Principles and Preferences describe the Component; Config records its generated project-specific result in the form defined by the foundational Schema. A Layer file may contain only its standard empty shape when the Component has no Layer-specific content; consumers then continue with the other applicable sources.

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
responsibility = Generated target-project Understanding resolved from Project through the applicable Principles and Preferences and written in the forms defined by Schema
answers = What has been resolved for the target project
generated = true
```


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
schema = .interface/schema/development.yaml
config = .interface/config/development.yaml
```

<!-------------------------- Model -->
### Model

```text
name = Model
responsibility = Independent shared Model package and logical domain Models, including fields, relationships, rules, validation, and initial data
principle = .interface/principles/model.md
preference = .interface/preferences/model.yaml
schema = .interface/schema/model.yaml
config = .interface/config/model.yaml
```

<!-------------------------- Database -->

### Database

```text
name = Database
responsibility = Independent package with typed Model operations, supported Engines, selectable Instances, Model-driven mapping, and Storage Adapters
principle = .interface/principles/database.md
preference = .interface/preferences/database.yaml
schema = .interface/schema/database.yaml
config = .interface/config/database.yaml
```
<!-------------------------- Backend -->

### Backend

```text
name = Backend
responsibility = Application and Model Logic, Database communication through Data Access, and the external API
principle = .interface/principles/backend.md
preference = .interface/preferences/backend.yaml
schema = .interface/schema/backend.yaml
config = .interface/config/backend.yaml
```

<!-------------------------- Frontend -->

### Frontend

```text
name = Frontend
responsibility = Component-based Presentation, user Interaction Logic, and application access through the Backend API
principle = .interface/principles/frontend.md
preference = .interface/preferences/frontend.yaml
schema = .interface/schema/frontend.yaml
config = .interface/config/frontend.yaml
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
- **Responsibility:** generates complete and consistent target-project Understanding for downstream Planning and Development.
- **Inputs:** `.interface/project.md`, existing `.interface/config/`, and the applicable Component Layers located in the file map.
- **Resolution:** for every current Component, resolve target-project Understanding through its Principles and Preferences and express it in the form required by its Schema.
- **Completeness:** produce one structurally valid current configuration for every Component; an empty Layer never removes a required Component output.
- **Refresh:** rebuild a complete candidate from current sources on every run and reconcile it with existing generated configuration.
- **Preservation:** remove stale interpreter-owned information while preserving information owned by the human, runtime, or another operation according to current authorities.
- **Validation:** validate each candidate against its Schema and the complete set for cross-Component consistency before writing.
- **Idempotency:** unchanged inputs and owned generated information produce no change on another run.
- **Output:** `.interface/config/`.

The generated Understanding must allow Planning and Development to work without independently reinterpreting `.interface/project.md`.

<!-------------------------- Planning -->
### Planning

- **State value:** `planning`
- **Phase-specific:** yes
- **Responsibility:** transforms generated Understanding for one requested phase into bounded, verifiable activities without prescribing implementation.
- **Inputs:** the requested phase resolved from the generated Understanding under `.interface/config/`, together with the Task Component authorities.
- **Scope:** the requested phase; its target selects the Component being planned.
- **Output:** `.interface/config/task.yaml`.

<!-------------------------- Development -->
### Development

- **State value:** `development`
- **Phase-specific:** yes
- **Responsibility:** executes and verifies eligible planned Tasks to produce project implementation.
- **Inputs:** generated Understanding under `.interface/config/` and planned Tasks in `.interface/config/task.yaml`.
- **Scope:** the requested phase; its target selects the Component being developed.
- **Output:** implementation inside the selected Component's resolved code boundary.






<!--------------------------------------------------------------------------------- Agent Skills --->
<br > <br>

## Agent Skills

Agent Skills are external capabilities that execute Interface Modes or supporting operations. Their integration metadata does not define the Interface Structure, grant authority, or replace the instructions and shared rules owned by the Claude configuration layer.


<!-------------------------- Interpreter -->
### Interpreter

```text
name = my-interface-interpreter
path = .claude/skills/my-interface-interpreter/SKILL.md
invocation = /my-interface-interpreter
responsibility = Generate or refresh complete target-project Understanding for every current Component and reconcile it for Planning and Development
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
responsibility = Discover and install compatible Agent Skills for technologies detected in configured target-project Understanding
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
### Interpret the Project

```text
order = 2
name = Interpret the Project
skill = /my-interface-interpreter
action = Generate or refresh target-project Understanding in .interface/config/
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
