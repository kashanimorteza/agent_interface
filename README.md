# Agent Interface

An independent interface between **Developers** and **AI Agents** for creating a common protocol, structure, and standard for software development.

The goal of Agent Interface is to allow Developers to express project requirements and definitions in natural language and transform that information into a standardized structure that Agents can understand, plan against, and ultimately use to develop the project.

<br > <br>

## Overview

Agent Interface provides a standardized layer between a Developer and an AI Agent.

Instead of requiring an Agent to understand an entire project directly from conversations, the project is progressively transformed into a structured representation.

The Developer defines the project in natural language, the Interface standardizes the project's understanding, the Planner converts that understanding into Tasks, and the Developer Agent implements those Tasks.

The Interface is designed to remain independent of any specific AI model or Agent.

<br > <br>

## Concept

Developers typically describe their projects and requirements using human language and in a flexible form.

AI Agents, on the other hand, work more reliably when project information is structured, explicit, and predictable.

Agent Interface provides the communication layer between these two worlds.

In this architecture:

- The Developer defines the project and its requirements in `project.md`.
- `Schema` defines the structure and standard for the required information.
- `Configure` reads and understands the project and produces Config according to the Schema.
- `Planner` uses the structured project information to create Tasks and a development plan.
- `Developer` uses the generated Tasks to develop the project.

<br > <br>

## Main Goal

The main goal of Agent Interface is to create a common language and structure between Developers and Agents.

The project aims to reduce the gap between:

**Human Requirements**

and

**Information Consumable by Agents**

Agent Interface does not replace the Developer's project definition. Instead, it transforms the human definition of the project into a structured and standardized representation that Agents can reliably use.

<br > <br>

## Features

- **Human-readable project definition**  
  Developers can describe their project and requirements using natural language.

- **Schema-driven structure**  
  Project information follows a defined and consistent structure.

- **Project Understanding**  
  The project definition is interpreted before being transformed into structured configuration.

- **Standardized Configuration**  
  Project Understanding is represented in a predictable format through Config.

- **Task Planning**  
  The Planner converts structured project information into actionable Tasks and a development plan.

- **Agent-independent interface**  
  The interface is not tied to a specific AI model or Agent.

- **Separation of responsibilities**  
  Understanding, configuration, planning, and development are handled as separate stages.

- **Extensible architecture**  
  Schemas, Configs, and instructions can evolve as the standard develops.

<br > <br>

## Quick Start

### 1. Define the Project

Start by describing the project and its requirements in:

`agent/project.md`

Write the project in natural language from the Developer's perspective.


### 2. Configure the Project

Use:

`agent/configure.md`

The Configure process reads `project.md`, develops an Understanding of the project, reads the relevant Schemas, and produces the corresponding Config.


### 3. Plan the Project

Use:

`agent/planner.md`

The Planner reads the structured project information and creates the Tasks and development plan required to implement the project.


### 4. Develop the Project

Use:

`agent/developer.md`

The Developer Agent uses the Tasks and project information produced by the previous stages to implement the project.


<br > <br>

## Project Structure

The core of Agent Interface is located in the `agent/` directory.

The `agent/` directory contains three main parts:

- **`schema/`** — Defines the standard structure and format of information.
- **`config/`** — Represents and maintains the project's Understanding according to the Schema.
- **Instruction Files** — Define the instructions for the different stages of working with the project.

### `project.md`

Contains the overall project definition and the Developer's requirements in natural language.

### `configure.md`

Defines how to understand `project.md` and transform the project's Understanding into Config.

### `planner.md`

Creates Tasks and a development plan based on the project's Config.

### `developer.md`

Develops the project based on the Tasks created by the Planner.

<br > <br>

## Agent Interface Workflow

The overall process is:

**Developer**

→ Define the project in `project.md`

→ **Configure**

→ Understand the project and transform it according to the `Schema`

→ **Config**

→ **Planner**

→ Create Tasks and a development plan

→ **Developer**

→ Implement the Tasks

→ **Software Project**

This process transforms project information from a human definition into a standardized structure, then into an executable development plan and code.

<br > <br>

## Responsibilities

Each part of Agent Interface has a specific responsibility:

| Component | Responsibility |
|<br > <br>|<br > <br>|
| `project.md` | Defines the project and requirements from the Developer |
| `schema/` | Defines the structure and information standard |
| `configure.md` | Understands the project and produces Config according to the Schema |
| `config/` | Maintains the structured representation of the project |
| `planner.md` | Transforms the project's Understanding into Tasks and a Plan |
| `developer.md` | Executes the Tasks and develops the project |

This separation keeps the Interface simple, understandable, and extensible.

<br > <br>

## Why Agent Interface?

In a conventional workflow, the Developer communicates directly with an Agent, and the Agent must derive the project's meaning from conversations and various files.

This can cause different Agents to understand the same project differently.

Agent Interface aims to solve this problem by introducing a common standard.

In this model, the Developer defines the project once, and the Interface transforms it into a structure that different Agents can use.

The goal is not to make Agents identical.

The goal is to make **the information Agents work with standardized and predictable**.

<br > <br>

## Project Philosophy

Agent Interface is based on a simple principle:

> **The Developer defines what the project is.**
>
> **The Schema defines how that information is structured.**
>
> **Configure understands the project and transforms it into the standardized structure.**
>
> **Planner defines what needs to be done.**
>
> **The Developer Agent defines how those tasks are implemented.**

This separation transforms the communication between humans and Agents from a free-form, model-dependent conversation into a structured and repeatable process.

<br > <br>

## Project Status

Agent Interface is an evolving standard.

The current structure defines the following core concepts:

- Project Definition
- Schema
- Project Understanding
- Configuration
- Planning
- Tasks
- Development

As the project evolves, the Schemas, Configs, and instructions can evolve as well without changing the fundamental concept of the Interface.

<br > <br>

## Final Goal

The ultimate goal of Agent Interface is to create a **lightweight, standardized, and Agent-independent protocol** for communication between Developers and AI Agents.

A project should be able to provide its information in a defined format, allowing different Agents to:

- Understand the project
- Understand its structure
- Create a development plan
- Create Tasks
- Develop the project
- Manage the project state in future stages

Ultimately, Agent Interface aims to become a standardized layer between **Humans, Projects, and Agents**.