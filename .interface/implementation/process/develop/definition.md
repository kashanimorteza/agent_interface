# Develop Definition

Develop is the Process Component that executes authorized planned Tasks and produces the resulting Development work.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[Process Contract](#process-contract)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Develop is the Process Component that executes planned implementation Tasks and produces the authorized Development results. It does not redefine the Plan or own the product meaning it realizes.

### Purpose

Planned work needs a bounded operation that turns Tasks into observable implementation results while preserving the authorities that made those Tasks understandable and verifiable.

### How It Works

Develop reads the selected Plan and applicable authorities, performs the authorized Tasks, preserves existing valid work, and records evidence and outcomes for Review and State.

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
- **Consumed by Review and State** — supplies results, evidence, and aggregate progress for assurance and recording.

<br>

Technical choices and defaults belong to the owning Development Component Preferences. Develop owns execution conventions only; it does not select product architecture or technical items.

Every Principle in this file is mandatory. A Process Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Develop owns execution. Plan owns the work definition, Development owns product meaning and technical choices, and State and Review own their respective records and judgments.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principle and Process Contract in this Definition govern Develop. Develop Preferences can supply execution defaults only where the Plan and owning Development authorities are silent.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Develop executes planned work within its authority

**Rule:** Develop executes only selected Tasks whose authority, scope, inputs, outputs, and completion conditions are understood. It preserves valid existing work and records evidence for each result.

**Why:** Bounded execution keeps implementation traceable to the Plan and prevents an execution operation from becoming an unplanned design authority.

**Boundary:** Develop never changes Target meaning, Plan authority, Development Principles, or another Component's owned record without explicit authority.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
<!--------------------------------------------------------------------------------- Process Contract --->
## Process Contract

Develop accepts zero or more phase selections. An empty selection means every phase eligible under its current Plan. It resolves stable phase identities, removes duplicates, and preserves Target order.

Develop consumes current Interface and Target Understanding, applicable Implementation Components, selected Plans and State, public interfaces, existing implementation, Review Findings, and the Agent parameters recorded for the work. It must establish the current authorities before mutation.

Develop executes only eligible planned Tasks. It may create authorized Source, tests, executable documentation, dependencies, and configuration within the resolved Plan and Component boundaries, and records truthful Task progress, evidence, aggregate Development State, History, Blockers, Open Questions, and applied Agent parameters.

Develop never creates or changes Plan content, Target intent, Review Findings, unrelated work, or another operation's records. It resolves declared technical requirements from owning Implementation Preferences, verifies or installs only what is missing, and records concrete versions and verification results.

Every Task is claimed before mutation, its acceptance and verification conditions are checked, and its evidence is recorded. Components outside the declared testing scope do not acquire tests, test configuration, or test dependencies as a side effect. Existing valid work is preserved and repeated execution is idempotent.

Develop stops on invalid selection, missing or stale Plan, unmet dependency, unavailable prerequisite, failed verification, unresolved Blocker, unavailable required Skill, or a required Human decision.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Develop executes planned work within its authority**

- **Must** — execute only understood Tasks and record evidence for their results.
- **Never** — expand Task scope or replace Target, Plan, or Development authority.
