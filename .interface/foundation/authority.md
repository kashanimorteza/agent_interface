# Authority and Ownership

This section defines record ownership and the human-owned boundary of Agent Interface.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Overview](#overview)**
2. **[Ownership](#ownership)**
3. **[Config Files](#config-files)**
4. **[Boundaries](#boundaries)**

<br>

<!--------------------------------------------------------------------------------- Overview --->
## Overview

Authority identifies which records belong to the Human or to an Interface Component. It also establishes the single editable area inside the otherwise human-owned Interface: generated operational Config files.

<br>

<!--------------------------------------------------------------------------------- Ownership --->
## Ownership

Ownership answers who a record belongs to, and it belongs to the Human or to a Component:

Human: Owns Interface, Target, Principles, Implementation Preferences, Agent Preferences, and Schema sources.

Plan: Owns Plans, Groups, Tasks, their status, and their history.

State: Owns active Workflow position, aggregate phase progress, and the operational Log in which every Skill records results, Blockers, and Open Questions.

Review: Owns recorded Findings and their state.

<br>

<!----------------------------------------------------------------------------------- Config Files --->
## Config Files

Configure creates and reconciles the generated Application Manifest, Plan, and State Config files.

After generation, files inside `.interface/config/` are mutable operational records. Agent and Skills may edit them; Authority does not allocate a separate file-level write permission to each Skill.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

Operational records follow their source authorities and must not redefine them.

Every file and directory in `.interface/` is human-owned and read-only to Agent and Skills, except files inside `.interface/config/`. No other Interface path becomes writable because it is added later, discovered by a Tool, or named by a Plan.
