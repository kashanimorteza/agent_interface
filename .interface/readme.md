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

The core of Agent Interface is located in the `.interface/` directory.

The `.interface/` directory contains five main parts:

- **`readme.md`** — Introduces the Interface, its structure, workflow, and Quick Start.
- **`root.yaml`** — The entry point. Maps the folders and files of the Interface, the Agent Skills, and the working modes.
- **`project.md`** — The project definition and the Developer's requirements, in natural language.
- **`schema/`** — Defines generated-file shapes. Each item Schema also owns that item's Policy and Preferences.
- **`config/`** — Represents and maintains the project's Understanding according to the Schema. `definition.yaml` describes the project, `model.yaml` defines its shared domain models, and `development.yaml` defines its technical composition and delivery.

Technical composition is intentionally separate from the human project description. `development.yaml` selects the technical components the project needs from the item types currently mapped by `root.yaml`, connects their contracts, and defines how they run and deploy.

Project phases are the primary units of work. `project.md` defines each phase's identity, order, target, and intended outcome. The target selects the technical item whose configuration supplies the relevant Policy, contracts, verification context, and code boundary; Development configuration independently describes how the project's selected technical items connect, run, and deploy.

Each item keeps two kinds of guidance beside its own Schema:

- **Policy** is mandatory and cannot be overridden by a project preference.
- **Preferences** supply supported technical choices when `project.md` leaves a corresponding choice unstated. Explicit project values win. Outside those values, Agents use professional judgment for ordinary technical decisions and continue; only critical decisions become open questions or blockers.

There is no global Preferences or Rules layer. Interface-wide authority remains in `root.yaml`, the State contract, and the workflow Skills; item-specific rules live in the Policy of the item that owns them.


<br > <br>

## Agent Skills

### `my-interface-interpreter`

`.claude/skills/my-interface-interpreter/SKILL.md`

Transforms the human-managed definition in `project.md` into the generated project Understanding. It preserves project intent, ordered phases, and their targets, resolves technical composition through the current Schemas, validates the result, and autonomously resolves ordinary technical gaps without inventing project intent.

### `my-interface-tasker`

`.claude/skills/my-interface-tasker/SKILL.md`

Transforms one requested project phase from the generated Understanding into an implementation-ready plan, resolving its technical target from Definition configuration.

### `my-interface-developer`

`.claude/skills/my-interface-developer/SKILL.md`

Executes eligible planned Tasks for one requested project phase, implements changes only within the code boundary selected by its target, verifies the result, and records each Task's actual outcome.

### `my-interface-reviewer`

`.claude/skills/my-interface-reviewer/SKILL.md`

Reviews one requested project phase against the generated Understanding, authorized Tasks, target-item Policy and contracts, and verification evidence, then reports findings without modifying the implementation.

### `my-interface-clear`

`.claude/skills/my-interface-clear/SKILL.md`

Runs its bundled script to clear the generated project configuration and the fixed generated-code targets owned by that Skill.

### `my-interface-reset`

`.claude/skills/my-interface-reset/SKILL.md`

Resets the whole generated workflow to the stage before development or before planning while preserving project code and generated Understanding.

`/my-interface-reset development`

`/my-interface-reset planning`


<br > <br>


## Quick Start

### 1. Define the Project

`.interface/project.md`

### 2. Interpret the Project

`/my-interface-interpreter`

### 3. Generate Tasks

`/my-interface-tasker <phase-id>`

### 4. Develop the Tasks

`/my-interface-developer <phase-id>`

`<phase-id>` is a phase already defined in `project.md`, such as `P1`, `P2`, or `P3`. Its technical target is defined with the phase in `project.md` and preserved in the generated Definition configuration.
