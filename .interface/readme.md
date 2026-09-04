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

The `.interface/` directory contains seven main parts:

- **`readme.md`** — Introduces the Interface, its structure, workflow, and Quick Start.
- **`map.yaml`** — The entry point. Maps the folders, files, and working modes of the Interface.
- **`project.md`** — The project definition and the Developer's requirements, in natural language.
- **`principles/`** — One Markdown document per layer and item holding its Principles: the mandatory, tool-independent rules that give it its personality.
- **`preferences/`** — One YAML file per technical item holding its Preferences: the supported tools, versions, and defaults used when `project.md` is silent. Layers with no technical choices (definition, model, development, task, state) have no preferences file.
- **`schema/`** — Defines generated-file shapes only.
- **`config/`** — Represents and maintains the project's Understanding according to the Schema. `definition.yaml` describes the project, `model.yaml` defines its shared domain models, and `development.yaml` defines its technical composition and delivery.

Technical composition is intentionally separate from the human project description. `development.yaml` selects the technical components the project needs from the item types currently mapped by `map.yaml`, connects their contracts, and defines how they run and deploy.

Project phases are the primary units of work. `project.md` defines each phase's identity, order, target, and intended outcome. The target selects the technical item whose configuration supplies the relevant Policy, contracts, verification context, and code boundary; Development configuration independently describes how the project's selected technical items connect, run, and deploy.

Each item keeps up to two kinds of guidance beside its own Schema, each in its own layer:

- **Principles** (`principles/<item>.md`) are mandatory and cannot be overridden by a project preference. They name no tool or version, so they travel unchanged between projects.
- **Preferences** (`preferences/<item>.yaml`) supply supported technical choices when `project.md` leaves a corresponding choice unstated. Explicit project values win. Outside those values, Agents use professional judgment for ordinary technical decisions and continue; only critical decisions become open questions or blockers.

There is no global Preferences layer. Interface-wide authority remains in `map.yaml` and the State contract; item-specific rules live in the Principles of the item that owns them. The three item layers are read together and answer different questions: Principles say *why and under what rules*, Preferences say *with what*, and the Schema says *in what form*. Agent-specific integrations and workflows remain outside `.interface/`.


<br > <br>

## Agent Skills

### `my-interface-interpreter`

Transforms the human project definition into the generated project Understanding required by downstream operations.

### `my-interface-tasker`

Creates or reconciles an implementation-ready plan for one requested project phase without implementing it.

### `my-interface-developer`

Implements and verifies eligible planned Tasks for one requested project phase within its authorized boundaries.

### `my-interface-reviewer`

Reviews the implemented result for one requested project phase and reports evidence-based findings without repairing it.

### `my-interface-clear`

Clears generated Interface configuration and mapped generated-code directories through its bundled script.

### `my-interface-reset`

Resets the generated workflow to its pre-development or pre-planning stage while preserving project code and generated Understanding.

### `my-interface-skill-installer`

Discovers and installs compatible Claude Skills for technologies detected in the configured target project.


<br > <br>

## Workflow

### 1. Define the Project

The Developer describes the project, its models, and its ordered phases in the human project definition mapped by `map.yaml`.

### 2. Interpret the Project

The human definition is transformed into the generated project Understanding according to the current Schemas.

### 3. Generate Tasks

One implementation-ready plan is generated for a requested project phase.

### 4. Develop the Tasks

Eligible Tasks for the requested phase are implemented and verified within the target item's authorized boundary.
