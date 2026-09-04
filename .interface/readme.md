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
- **`root.yaml`** — The entry point. Maps the folders, files, and working modes of the Interface.
- **`project.md`** — The project definition and the Developer's requirements, in natural language.
- **`schema/`** — Defines generated-file shapes. Each item Schema also owns that item's Policy and Preferences.
- **`config/`** — Represents and maintains the project's Understanding according to the Schema. `definition.yaml` describes the project, `model.yaml` defines its shared domain models, and `development.yaml` defines its technical composition and delivery.

Technical composition is intentionally separate from the human project description. `development.yaml` selects the technical components the project needs from the item types currently mapped by `root.yaml`, connects their contracts, and defines how they run and deploy.

Project phases are the primary units of work. `project.md` defines each phase's identity, order, target, and intended outcome. The target selects the technical item whose configuration supplies the relevant Policy, contracts, verification context, and code boundary; Development configuration independently describes how the project's selected technical items connect, run, and deploy.

Each item keeps two kinds of guidance beside its own Schema:

- **Policy** is mandatory and cannot be overridden by a project preference.
- **Preferences** supply supported technical choices when `project.md` leaves a corresponding choice unstated. Explicit project values win. Outside those values, Agents use professional judgment for ordinary technical decisions and continue; only critical decisions become open questions or blockers.

There is no global Preferences layer. Interface-wide authority remains in `root.yaml` and the State contract; item-specific rules live in the Policy of the item that owns them. Agent-specific integrations and workflows remain outside `.interface/`.


<br > <br>

## Workflow

### 1. Define the Project

The Developer describes the project, its models, and its ordered phases in the human project definition mapped by `root.yaml`.

### 2. Interpret the Project

The human definition is transformed into the generated project Understanding according to the current Schemas.

### 3. Generate Tasks

One implementation-ready plan is generated for a requested project phase.

### 4. Develop the Tasks

Eligible Tasks for the requested phase are implemented and verified within the target item's authorized boundary.
