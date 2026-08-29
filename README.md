# Agent Interface

An independent interface between **Developers** and **AI Agents** for creating a common protocol, structure, and standard for software development.

The goal of Agent Interface is to allow Developers to express project requirements and definitions in natural language and transform that information into a standardized structure that Agents can understand, plan against, and ultimately use to develop the project.

<br > <br>

## Overview

Agent Interface provides a standardized layer between a Developer and an AI Agent.

Instead of requiring an Agent to understand an entire project directly from conversations, the project is progressively transformed into a structured representation.

The Developer defines the project in natural language, and the Interface standardizes the project's understanding into a structured representation that an Agent can use.

The Interface is designed to remain independent of any specific AI model or Agent.

<br > <br>

## Concept

Developers typically describe their projects and requirements using human language and in a flexible form.

AI Agents, on the other hand, work more reliably when project information is structured, explicit, and predictable.

Agent Interface provides the communication layer between these two worlds.

In this architecture:

- The Developer defines the project and its requirements in `project.md`.
- `Schema` defines the structure and standard for the required information.
- The `my-interface-configurator` Skill reads and understands the project and produces Config according to the Schema.




<br > <br>

## Project Structure : Directories and files

The core of Agent Interface is located in the `.interface/` directory.

The `.interface/` directory contains three main parts:

- **`schema/`** — Defines the standard structure and format of information.
- **`config/`** — Represents and maintains the project's Understanding according to the Schema.
- **Instruction Files** — Define the instructions for the different stages of working with the project.

### `project.md`

Contains the overall project definition and the Developer's requirements in natural language.


<br > <br>

## Project Structure : Agent Skills

Agent Interface defines four Skills for the main stages of the development workflow.

### `my-interface-configurator`

Reads `project.md` and generates the project configuration according to the Schema.

### `my-interface-planner`

Reads the project configuration and generates Tasks and the development plan.

### `my-interface-developer`

Executes the planned Tasks and implements the required changes.

### `my-interface-reviewer`

Reviews the implementation against the Tasks and project specifications.


<br > <br>


## Quick Start

### 1. Understand the Project

Read the project definition:

`.agent/project.md`

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