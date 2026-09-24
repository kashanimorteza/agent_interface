# Develop Definition

Develop is the Operation Component that executes authorized planned Tasks and produces the resulting Development work.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Develop is the Operation Component that executes planned implementation Tasks and produces the authorized Development results. It does not redefine the Plan or own the product meaning it realizes.

### Purpose

Planned work needs a bounded operation that turns Tasks into observable implementation results while preserving the authorities that made those Tasks understandable and verifiable.

### How It Works

Develop accepts one or more Target phase identifiers, or considers every active and developable Target phase when none is selected, in Target order. It establishes current Interface and Target Understanding, reads the current Plan for each applicable phase, and performs its authorized unfinished Tasks. A phase is developable only when the required Config records are valid and its current Plan exists. If either condition is absent, Develop stops; it does not run Configure or Plan.

For each eligible Task, Develop considers the Task Skills identified by Planning and may use any other suitable available Skill. It does not invoke another Core Operation. Develop claims the Task before work begins, preserves valid existing work, records evidence and progress in that Task's Task Log, and updates its status. If no eligible Task exists, it completes without changing implementation work. It stops when a dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Development Result** — the authorized Source, interface, configuration, or evidence produced by a completed development Task.
- **Task Evidence** — the observable information showing what a Develop operation produced and verified.
- **Developable Phase** — an active Target phase whose required Config records are valid and whose current Plan exists.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Plan** — takes the selected Groups, Tasks, context, dependencies, and completion conditions.
- **Consumes Interface and Target** — applies their current authorities while performing the selected Tasks.
- **Consumes Development authorities** — realizes the product under the Development Components' Definitions and Preferences.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Develop owns Task execution. Technical choices and defaults belong to the owning Development Component Preferences; Plan owns the work definition, Development owns product meaning, Task Logs own Task evidence and progress, and State owns Operation Logs and aggregate progress.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principle in this Definition governs Develop. Develop Preferences can supply execution defaults only where the Plan and owning Development authorities are silent.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Develop executes planned work within its authority

**Rule:** Develop accepts one or more Target phase identifiers, or considers every active and developable Target phase when none is selected, in Target order. It starts only when required Config records are valid and the current Plan for each applicable phase exists. Develop executes only selected eligible Tasks whose authority, scope, inputs, outputs, and completion conditions are understood. It considers each Task's Task Skills, may use any other suitable available Skill, and never invokes another Core Operation.

Before changing a Task's result, Develop claims that eligible Task. It preserves valid existing work, records Task-specific evidence, progress transitions, verification results, and any Task-specific Blocker in the Task Log, and updates the Task status accordingly. When a new Task identifies an earlier developed Task through `replaces`, Develop marks that earlier Task as `replaced` and records the relationship in its Task Log before executing the new Task. If Config or Plan is unavailable, Develop stops; it does not execute Configure or Plan.

**Why:** Bounded execution keeps implementation traceable to the Plan and prevents an execution operation from becoming an unplanned design authority.

**Boundary:** Develop never changes Target meaning, Plan authority, Development Principles, or another Component's owned record without explicit authority. It does not design or change Tasks, does not run another Core Operation, and stops and reports when another Operation is required.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Develop executes planned work within its authority**

- **Must** — select one or more Target phases, or every active and developable phase when none is selected, in Target order.
- **Must** — require valid Config and a current Plan before development, and stop when either is absent.
- **Must** — execute only understood, claimed, eligible Tasks; consider their Task Skills and record Task evidence and progress in their Task Logs.
- **Must** — mark an earlier developed Task as `replaced` and record the relationship before executing a new Task that identifies it through `replaces`.
- **Never** — invoke another Core Operation, expand Task scope, or replace Target, Plan, or Development authority.
