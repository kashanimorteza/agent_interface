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

## Directories and files

The core of Agent Interface is located in the `.interface/` directory.

The `.interface/` directory contains four main parts:

- **`root.yaml`** — The entry point. Maps the folders and files of the Interface, the Agent Skills, and the working modes.
- **`project.md`** — The project definition and the Developer's requirements, in natural language.
- **`schema/`** — Defines generated-file shapes. Each item Schema also owns that item's Policy and Preferences.
- **`config/`** — Represents and maintains the project's Understanding according to the Schema.

The project currently has three independent items:

- **Database** — owns the database engine, storage, schema, migrations, and database contract.
- **Backend** — consumes the database contract and publishes the HTTP API contract.
- **Frontend** — consumes the backend API contract and publishes the user interface.

Their directed relationship is:

`Database → Backend → Frontend`

Each item keeps two kinds of guidance beside its own Schema:

- **Policy** is mandatory and cannot be overridden by a project preference.
- **Preferences** supply supported technical choices only when `project.md` leaves the corresponding choice unstated. Explicit project values win; ambiguity or conflict becomes an open question.

There is no global Preferences or Rules layer. Interface-wide authority remains in `root.yaml`, the State contract, and the workflow Skills; item-specific rules live in the Policy of the item that owns them.


<br > <br>

## Agent Skills

### `my-interface-interpreter`

Reads `project.md`, resolves each item's local Policy and Preferences, and generates the project configuration according to the Schema.

### `my-interface-tasker`

Reads the project configuration and generates Tasks and the development plan.

### `my-interface-developer`

Executes the planned Tasks and implements the required changes.

### `my-interface-reviewer`

Reviews the implementation against the Tasks and project specifications.

### `my-interface-reset`

Removes the generated Config and the exact project code directories resolved from it, returning the repository to a clean state ready for the Interpreter to run again.


<br > <br>


## Modes and State

Exactly one mode is active at a time — `planning`, `development`, or `review` — named in `.interface/config/state.yaml` under `content.active.mode`, together with the item in play.

A mode is entered by invoking the Skill that owns it. The invocation is the Developer's decision, and the Skill records it: `/my-interface-tasker backend` sets the mode to `planning` and the item to `backend`. Nothing is hand-edited into `state.yaml` first.

A Skill may write only the mode it owns, only on an invocation of itself, and only an item the configuration indexes. Where the invocation leaves the item ambiguous, the Skill stops and asks rather than choosing.

The single source of truth for all of it — every state field, its owner, the allowed transitions, which Skill may perform each, and what stays the Developer's alone — is the State contract itself: `.interface/config/state.yaml` under `content.state_authority`, seeded from the default in `.interface/schema/state.schema.yaml` whenever a new State is created, and the Developer's alone after that seed. `root.yaml` maps the Interface and defines the modes; it references the State Authority and does not own it. Every other file defers to the State contract.


<br > <br>


## Quick Start

### 1. Understand the Project

Read the project definition:

`.interface/project.md`

Understand the project requirements and overall definition.

### 2. Configure the Project

Use the `my-interface-interpreter` Skill:

`.claude/skills/my-interface-interpreter/SKILL.md`

Use `project.md` together with the item-local Policy and Preferences in `schema/` to generate `database.yaml`, `backend.yaml`, `frontend.yaml`, and the shared project configuration in `config/`.

### 3. Plan the Project

Use the `my-interface-tasker` Skill:

`.claude/skills/my-interface-tasker/SKILL.md`

Read the generated Config and create the required Tasks according to the defined Task structure.

### 4. Develop the Project

Use the `my-interface-developer` Skill:

`.claude/skills/my-interface-developer/SKILL.md`

Execute the planned Tasks and implement the required changes.
