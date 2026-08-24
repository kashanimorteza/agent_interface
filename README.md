<!--------------------------------------------------------------------------------- Agent Interface -->
# Agent Interface

An agent-independent interface between software projects and AI agents.

<!--------------------------------------------------------------------------------- Diagram -->
<br><br>

## Diagram*

<!--------------------------------------------------------------------------------- Modules -->
<br><br>

## Modules

### Root

Defines the entry point, reading protocol, working modes, and write protocol for AI agents.

### Project

Defines what the product is, its purpose, architecture, and project-level context.

### Rules

Defines the rules, constraints, priorities, and development principles that agents must follow.

### Structure

Defines the project map and the location and organization of the different layers and resources.

### State

Defines the current operational state of the project, including active mode, blockers, questions, and other runtime information.

### Develop

Defines the development layer, including work items, their boundaries, plans, rules, and implementation scope.

### History

Records sessions, decisions, and other historical information required to preserve project context across agents and sessions.

<!--------------------------------------------------------------------------------- Concept -->
<br><br>

## Concept

Developer ↔ Project ↔ AI Agent**

The project is the source of truth.  
AI agents interact with the project through a structured and agent-independent interface.

<!--------------------------------------------------------------------------------- Link -->

[Agent Interface]: https://github.com/kashanimorteza/agent_interface/blob/main/readme.md