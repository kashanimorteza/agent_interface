# Agent Interface

### Description

An independent interface between **Developers** and **AI Agents** for creating a common protocol, structure, and standard for software development.

The goal of Agent Interface is to allow Developers to express project requirements and definitions in natural language and transform that information into a standardized structure that Agents can understand, plan against, and ultimately use to develop the project.

### Overview

Agent Interface provides a standardized layer between a Developer and an AI Agent.

Instead of requiring an Agent to understand an entire project directly from conversations, the project is progressively transformed into a structured representation.

The Developer defines the project in natural language, and the Interface standardizes the project's understanding into a structured representation that an Agent can use.

The Interface is designed to remain independent of any specific AI model or Agent.

### Concept

Developers typically describe their projects and requirements using human language and in a flexible form.

AI Agents, on the other hand, work more reliably when project information is structured, explicit, and predictable.

Agent Interface provides the communication layer between these two worlds.




<br > <br>

## Structure

The internal structure of Agent Interface lives in the `.interface/` directory. It has foundational files, three descriptive layers, a set of components, and the generated project configuration.

Agent Skills and Workflow use this structure, but they are not part of it.

### Foundational Files

- **`map.yaml`** — The entry point and map of the Interface. It locates the current files and explains their responsibilities.
- **`project.md`** — The human-managed definition of the project being built.
- **`readme.md`** — The human-readable introduction to Agent Interface, its structure, Agent Skills, and Workflow.

### Layers

The three layers describe each component from a different point of view:

- **Principles** (`principles/`) — The mandatory philosophy, responsibilities, and boundaries of a component. Principles explain *why and under what rules* it works and remain independent of tools and versions.
- **Preferences** (`preferences/`) — Supported technical choices and defaults used when the project leaves a choice unstated. Preferences explain *with what* a component is commonly realized. An explicit project choice always wins.
- **Schemas** (`schema/`) — The shape and validation rules of generated files. Schemas explain *in what form* the resolved information is written.

Not every component needs all three layers. A component has only the Principle, Preference, or Schema files that are meaningful for it. There is no global Preferences file.

### Components

Components are the subjects described through the layers:

| Component | Responsibility |
| --- | --- |
| **Definition** | Structured project identity, intended outcomes, and ordered phases |
| **Model** | Shared domain models, fields, relationships, rules, and initial data |
| **Development** | Technical component selection, connections, runtime, and deployment |
| **State** | Current workflow state, working modes, and transition authority |
| **Task** | Plans, groups, tasks, progress, and task history |
| **Backend** | Application behaviour and the HTTP API |
| **Frontend** | User interface and access to application data through the backend API |
| **Database** | Persistence, storage mapping, migrations, and the generic data-access interface |

For example, understanding the Backend component means combining its Principle, its optional technical Preferences, and its Schema. The same reading model applies to every component, using only the layers that component owns.

### Behaviours

Behaviours describe what is done with the structure:

- **Interpretation** — Transforms the human project definition into the standardized generated project Understanding.
- **Planning** — Transforms the generated Understanding for a requested project phase into implementation-ready Tasks.
- **Development** — Executes and verifies the planned Tasks to produce the project implementation.

Behaviours are part of the Interface's operating model. Agent Skills are external capabilities that perform these behaviours, while Workflow describes the order in which the behaviours are used.

### Generated Configuration

The `config/` directory is not a fourth descriptive layer. It is the generated project Understanding: the project-specific result produced from `project.md` using the applicable Principles and Preferences and written in the forms defined by the Schemas.

Each generated configuration belongs to one component. Definition preserves the project's phases and their targets; Model provides the shared domain language; the technical components define their own resolved configuration; Development connects the selected technical components and explains how they run and deploy; Task holds executable plans; and State records where the Workflow currently stands.

Project phases are the units of planning and development. A phase target selects the component developed by that phase, while Development independently describes how all selected technical components connect and operate together.


<br > <br>

## Agent Skills

Agent Skills are external executors of Agent Interface behaviours. They use the Interface, but they do not define its structure and are not part of its project model.

### `my-interface-interpreter`

Transforms the human project definition into the generated project Understanding required by downstream operations.

### `my-interface-tasker`

Creates or reconciles an implementation-ready plan for one requested project phase without implementing it.

### `my-interface-developer`

Implements and verifies eligible planned Tasks for one requested project phase within its authorized boundaries.

### `my-interface-reviewer`

Reviews the implemented result for one requested project phase and reports evidence-based findings without repairing it.

### `my-interface-clear`

Clears generated Interface configuration and the fixed generated project directories through its bundled script.

### `my-interface-reset`

Resets either planning output or developed code through a fixed two-stage script. A planning reset clears every Plan's Groups and Tasks and clears active State; a development reset returns Tasks to `todo`, returns active State to planning, and removes the root backend, frontend, and database directories.

### `my-interface-skill-installer`

Discovers and installs compatible Claude Skills for technologies detected in the configured target project.


<br > <br>

## Workflow

### 1. Define the Project

Define the project, its models, and its ordered phases in `project.md`.

### 2. Interpret the Project

`/my-interface-interpreter`

### 3. Generate Tasks

`/my-interface-tasker <phase-id>`

### 4. Develop the Tasks

`/my-interface-developer <phase-id>`
