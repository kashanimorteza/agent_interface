# Develop Definition

Develop is the Operation Component that executes authorized planned Tasks and produces the resulting Development work.

Responsibility: The execution of planned implementation Tasks and production of authorized Development results.

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

Develop reads the selected Plan and current Interface and Target authorities, performs the authorized unfinished Tasks, preserves existing valid work, and records evidence and outcomes in State Log. If no eligible Task exists, Develop records that no development was required. It stops when the Plan is missing or stale, a dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Development Result** — the authorized Source, interface, configuration, or evidence produced by a completed development Task.
- **Task Evidence** — the observable information showing what a Develop operation produced and verified.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Plan** — takes the selected Groups, Tasks, context, dependencies, and completion conditions.
- **Consumes Development authorities** — realizes the product under the Development Components' Definitions and Preferences.
- **Consumed by State** — supplies results, evidence, and aggregate progress for recording.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Develop owns execution conventions. Technical choices and defaults belong to the owning Development Component Preferences; Plan owns the work definition, Development owns product meaning, and State and Review own their respective records and judgments.

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

**Rule:** Develop executes only selected Tasks whose authority, scope, inputs, outputs, and completion conditions are understood. It preserves valid existing work and records evidence for each result.

**Why:** Bounded execution keeps implementation traceable to the Plan and prevents an execution operation from becoming an unplanned design authority.

**Boundary:** Develop never changes Target meaning, Plan authority, Development Principles, or another Component's owned record without explicit authority. It stops and reports when another Operation is required.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Develop executes planned work within its authority**

- **Must** — execute only understood Tasks and record evidence for their results.
- **Never** — expand Task scope or replace Target, Plan, or Development authority.
