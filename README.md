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

In this architecture:

- The Developer defines the project and its requirements in `project.md`.
- `Schema` defines the structure and standard for the required information.
- The `my-interface-configurator` Skill reads and understands the project and produces Config according to the Schema.




<br > <br>

## Directories and files

The core of Agent Interface is located in the `.interface/` directory.

The `.interface/` directory contains four main parts:

- **`root.yaml`** — The entry point. Maps the folders and files of the Interface, the Agent Skills, and the working modes.
- **`project.md`** — The project definition and the Developer's requirements, in natural language.
- **`schema/`** — Defines the standard structure and format of information.
- **`config/`** — Represents and maintains the project's Understanding according to the Schema.


<br > <br>

## Agent Skills

### `my-interface-configurator`

Reads `project.md` and generates the project configuration according to the Schema.

### `my-interface-planner`

Reads the project configuration and generates Tasks and the development plan.

### `my-interface-developer`

Executes the planned Tasks and implements the required changes.

### `my-interface-reviewer`

Reviews the implementation against the Tasks and project specifications.

### `my-interface-clear`

Removes the generated Config and Tasks and returns the project to a clean state, ready for the Configurator to run again.


<br > <br>


## Modes and State

Exactly one mode is active at a time — `planning`, `development`, or `review` — named in `.interface/config/state.yaml` under `content.active.mode`, together with the item in play.

A mode is entered by invoking the Skill that owns it. The invocation is the Developer's decision, and the Skill records it: `/my-interface-planner backend` sets the mode to `planning` and the item to `backend`. Nothing is hand-edited into `state.yaml` first.

A Skill may write only the mode it owns, only on an invocation of itself, and only an item the configuration indexes. Where the invocation leaves the item ambiguous, the Skill stops and asks rather than choosing.

The single source of truth for all of it — every state field, its owner, the allowed transitions, which Skill may perform each, and what stays the Developer's alone — is the State contract itself: `.interface/config/state.yaml` under `content.state_authority`, seeded from the default in `.interface/schema/state.schema.yaml` whenever a new State is created, and the Developer's alone after that seed. `root.yaml` maps the Interface and defines the modes; it references the State Authority and does not own it. Every other file defers to the State contract.


<br > <br>


## Quick Start

### 1. Understand the Project

Read the project definition:

`.interface/project.md`

Understand the project requirements and overall definition.

### 2. Configure the Project

Use the `my-interface-configurator` Skill:

`.claude/skills/my-interface-configurator/SKILL.md`

Use the project Understanding and the `schema/` structure to generate the project configuration files in `config/`.

### 3. Plan the Project

Use the `my-interface-planner` Skill:

`.claude/skills/my-interface-planner/SKILL.md`

Read the generated Config and create the required Tasks according to the defined Task structure.

### 4. Develop the Project

Use the `my-interface-developer` Skill:

`.claude/skills/my-interface-developer/SKILL.md`

Execute the planned Tasks and implement the required changes.