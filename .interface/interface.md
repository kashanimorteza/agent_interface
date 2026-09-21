# Agent Interface

Agent Interface is the Human-defined structure that coordinates Target, Implementation, Agent, Config, and the shared operational workflow.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Modules](#modules)**
5. **[Config](#config)**
6. **[Foundation Files](#foundation-files)**
7. **[Understanding](#understanding)**
8. **[Authority and Ownership](#authority-and-ownership)**
9. **[Workflow](#workflow)**


<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

Introduction explains the purpose and design of Agent Interface.

→ [Read more about Introduction](foundation/introduction.md)



<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

Terms defines the shared vocabulary used throughout Agent Interface.

→ [Read more about Terms](foundation/terms.md)



<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

Architecture maps the high-level structure of Agent Interface.

→ [Read more about Architecture](foundation/architecture.md)



<br>

<!--------------------------------------------------------------------------------- Modules --->
## Modules

### Target

Target defines what the Interface is working on.

→ [Read more about the Target Module](target/target.md)

### Implementation

Implementation defines how a Target is built and how that work is controlled.

→ [Read more about the Implementation Module](implementation/implementation.md)

### Agent

Agent defines how the selected Agent Native operates.

→ [Read more about the Agent Module](agent/agent.md)



<br>

<!--------------------------------------------------------------------------------- Config --->
## Config

Config is the shared operational boundary for generated Workflow records.

- **Application Config** — shared public metadata that lets Components discover and compose one another. [Read more about Application Config](config/application.yaml)
- **State Config** — current Workflow position, phase progress, outcomes, and History containing Operation and Skill records. [Read more about State Config](config/state.yaml)
- **Plan Config** — Plans, Groups, Tasks, dependencies, completion conditions, and planning progress. [Read more about Plan Config](config/plan.yaml)

<br>

<!--------------------------------------------------------------------------------- Foundation Files --->
## Foundation Files

Foundation Files are the shared resources used by every Module and Skill.

→ [Read more about Foundation Files](foundation/foundation.md)



<br>

<!--------------------------------------------------------------------------------- Understanding --->
## Understanding

Understanding defines how an Agent establishes the context required for its role.

→ [Read more about Understanding](foundation/understanding.md)



<br>

<!--------------------------------------------------------------------------------- Authority and Ownership --->
## Authority and Ownership

Authority and Ownership define record ownership, write authority, and the read-only Interface boundary.

→ [Read more about Authority and Ownership](foundation/authority.md)



<br>

<!--------------------------------------------------------------------------------- Workflow --->
## Workflow

Workflow defines the paths from Target definition to running software.

→ [Read more about Workflow](foundation/workflow.md)
