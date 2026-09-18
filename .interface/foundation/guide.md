# Foundation Files

This document explains the Foundation directory: what it holds, why those files are shared by the whole Interface, and who may change them. It is Human-owned and explains; it does not redefine. The canonical definition remains `interface.md`, one level above this directory, which describes the complete system; this document describes only this directory and its contents.

Foundation is not one of the three Modules (Target, Implementation, Agent). It is the set of shared resources those Modules and every Skill depend on.

<br>

## Navigation

1. **[Purpose](#purpose)**
2. **[Structure](#structure)**
3. **[Interface file](#interface-file)**
4. **[Interface sections kept as separate files](#interface-sections-kept-as-separate-files)**
   - **[Introduction](#introduction)**
   - **[Terminology](#terminology)**
   - **[Architecture](#architecture)**
   - **[Understanding](#understanding)**
   - **[Operations](#operations)**
   - **[Modes](#modes)**
   - **[Authority and Ownership](#authority-and-ownership)**
   - **[Workflow](#workflow)**
5. **[Config](#config)**
   - **[Application Manifest](#application-manifest-config)**
   - **[State](#state-config)**
   - **[Plan](#plan-config)**
   - **[Review](#review-config)**
6. **[Schema](#schema)**
   - **[Structure standards](#structure-standards)**
     - **[YAML](#yaml-schema)**
     - **[Principles](#principles-schema)**
     - **[Preferences](#preferences-schema)**
     - **[Agent Preferences](#agent-preferences-schema)**
     - **[Skill Contract](#skill-contract-schema)**
     - **[Personality](#personality-schema)**
     - **[Database Configuration](#database-configuration-schema)**
   - **[Operational formats](#operational-formats)**
     - **[Application Manifest](#application-manifest-schema)**
     - **[State](#state-schema)**
     - **[Plan](#plan-schema)**
     - **[Review](#review-schema)**
7. **[Ownership](#ownership)**
8. **[Understanding record](#understanding-record)**
9. **[Open decisions](#open-decisions)**

<br>

## Purpose

Foundation Files provide the foundational definitions and schemas required by the Interface: the canonical Interface document that every Understanding starts from, the Schemas that define how authored and generated files are shaped, and the Config records that coordinate the Workflow.

<br>

## Structure

```text
.interface/interface.md          ← the Interface file, one level above
.interface/foundation/
├── guide.md
├── introduction.md
├── terminology.md
├── architecture.md
├── understanding.md
├── operations.md
├── modes.md
├── authority.md
├── workflow.md
├── config/
│   ├── application.yaml
│   ├── state.yaml
│   ├── plan.yaml
│   └── review.yaml
└── schema/
    ├── application.yaml
    ├── yaml.yaml
    ├── principles.md
    ├── preferences.yaml
    ├── agent-preferences.yaml
    ├── skill-contract.md
    ├── personality.md
    ├── state.yaml
    ├── plan.yaml
    └── review.yaml
```

<br>

## Interface file

[`interface.md`](../interface.md), one level above this directory, is the canonical definition, navigation entry point, and complete file map of Agent Interface. Interface Understanding — required by every Skill — starts exclusively from this file and follows only the routes it provides for the active role. For every operation except Agent Sync, those routes lead to Target, Implementation, Foundation, Config, and synchronized Runtime resources; seeing the Agent Structure in this file never authorizes entry into the Agent Module.

```yaml
name: Interface
path: .interface/interface.md
responsibility: Canonical definition, navigation entry point, and entry point to the complete file map of Agent Interface; each Module's own files are mapped in its guide
```

→ [Interface](../interface.md)

<br>

## Interface sections kept as separate files

Eight sections of the Interface were moved out of `interface.md` verbatim — five on 2026-09-17; Introduction, Terminology, and Architecture on 2026-09-18 — so that the entry file stays a map. Each is part of Interface Understanding: a Skill reads `interface.md` and then these files before acting.

### Introduction

What Agent Interface is, its purpose, independence, core idea, and design goals.

```yaml
name: Introduction
path: .interface/foundation/introduction.md
responsibility: States what Agent Interface is, its purpose, independence, core idea, and design goals
```

→ [Introduction](introduction.md)

### Terminology

The shared vocabulary of the Interface.

```yaml
name: Terminology
path: .interface/foundation/terminology.md
responsibility: Defines the shared vocabulary of the Interface
```

→ [Terminology](terminology.md)

### Architecture

The conceptual architecture tree and what each part contributes.

```yaml
name: Architecture
path: .interface/foundation/architecture.md
responsibility: Presents the conceptual architecture tree and what each part contributes
```

→ [Architecture](architecture.md)

### Understanding

Interface Understanding and Target Understanding, their sources and precedence, and the Agent Module exception.

```yaml
name: Understanding
path: .interface/foundation/understanding.md
responsibility: Defines Interface Understanding and Target Understanding, their sources and precedence, and the Agent Module exception
```

→ [Understanding](understanding.md)

### Operations

The nine Operations and the Skill that performs each.

```yaml
name: Operations
path: .interface/foundation/operations.md
responsibility: Lists the nine Operations and the Skill that performs each
```

→ [Operations](operations.md)

### Modes

The Modes State may record.

```yaml
name: Modes
path: .interface/foundation/modes.md
responsibility: Defines the Modes State may record
```

→ [Modes](modes.md)

### Authority and Ownership

Record ownership and each Skill's write authority.

```yaml
name: Authority and Ownership
path: .interface/foundation/authority.md
responsibility: Defines record ownership and each Skill's write authority
```

→ [Authority and Ownership](authority.md)

### Workflow

The Workflow and its Default, Normal, and Detailed paths.

```yaml
name: Workflow
path: .interface/foundation/workflow.md
responsibility: Defines the Workflow and its Default, Normal, and Detailed paths
```

→ [Workflow](workflow.md)

<br>

## Config

Config stores the mutable operational records used while executing the Interface. It coordinates the Workflow and records where work stands; it does not store what the Target means and never becomes a second project definition.

```text
.interface/foundation/config/
├── application.yaml
├── state.yaml
├── plan.yaml
└── review.yaml
```

`config/` is the only mutable exception in the otherwise read-only `.interface/` tree. Configure creates these files from their Schemas; afterwards each Skill writes only the records it has authority over, always under the rules of the owning Component (Plan, Review, or State). Until Configure has run, the files below may not exist yet.

### Application Manifest Config

One public metadata section for every Implementation Component; sections may remain empty until their owners publish metadata.

```yaml
name: Application Manifest Config
path: .interface/foundation/config/application.yaml
schema: .interface/foundation/schema/application.yaml
responsibility: Stores one public metadata section for every Implementation Component; sections may remain empty until their owners publish metadata
```

→ [Application Manifest Config](config/application.yaml)

### State Config

Active Workflow position, aggregate phase progress, Implement and Launch results, access points, History, Blockers, and Open Questions.

```yaml
name: State Config
path: .interface/foundation/config/state.yaml
schema: .interface/foundation/schema/state.yaml
responsibility: Stores active Workflow position, aggregate phase progress, Implement and Launch results, access points, History, Blockers, and Open Questions
```

→ [State Config](config/state.yaml)

### Plan Config

Plans, Groups, Tasks, their dependencies, status, and history.

```yaml
name: Plan Config
path: .interface/foundation/config/plan.yaml
schema: .interface/foundation/schema/plan.yaml
responsibility: Stores Plans, Groups, Tasks, their dependencies, status, and history
```

→ [Plan Config](config/plan.yaml)

### Review Config

Reviewed phases, outcomes, Findings, evidence, and Finding status.

```yaml
name: Review Config
path: .interface/foundation/config/review.yaml
schema: .interface/foundation/schema/review.yaml
responsibility: Stores reviewed phases, outcomes, Findings, evidence, and Finding status
```

→ [Review Config](config/review.yaml)

<br>

## Schema

Schemas define the structure followed by authored Interface files and generated operational records. Two kinds exist: **Structure standards**, the shape a Human-authored file follows, and **Operational formats**, the stored structure and initial template of a generated record. Schema definition files use their own formats and do not follow the outer YAML frame they define.

```text
.interface/foundation/schema/
├── yaml.yaml
├── principles.md
├── preferences.yaml
├── agent-preferences.yaml
├── skill-contract.md
├── personality.md
├── database.yaml
├── application.yaml
├── state.yaml
├── plan.yaml
└── review.yaml
```

### Structure standards

The shape a Human-authored file follows.

#### YAML Schema

The common outer frame (meta, policy, read_order, content_map, content) followed by Implementation Preferences, Agent Preferences, and Config files.

```yaml
name: YAML Schema
path: .interface/foundation/schema/yaml.yaml
kind: Structure standard
responsibility: Defines the common outer structure followed by Implementation Preferences, Agent Preferences, and Config files
scope: Schema definition files use their own formats and do not follow this outer structure
```

→ [YAML Schema](schema/yaml.yaml)

#### Principles Schema

The common Markdown structure of every Implementation and Agent Component `principles.md`.

```yaml
name: Principles Schema
path: .interface/foundation/schema/principles.md
kind: Structure standard
responsibility: Defines the common Markdown structure followed by every Implementation and Agent Component principles.md file
```

→ [Principles Schema](schema/principles.md)

#### Preferences Schema

The four-section structure of every Implementation `preferences.yaml`.

```yaml
name: Preferences Schema
path: .interface/foundation/schema/preferences.yaml
kind: Structure standard
responsibility: Defines the four-section structure followed by every Implementation Component preferences.yaml file
```

→ [Preferences Schema](schema/preferences.yaml)

#### Agent Preferences Schema

The three-section structure of every Agent `preferences.yaml`.

```yaml
name: Agent Preferences Schema
path: .interface/foundation/schema/agent-preferences.yaml
kind: Structure standard
responsibility: Defines the three-section structure followed by every Agent Component preferences.yaml file
```

→ [Agent Preferences Schema](schema/agent-preferences.yaml)

#### Skill Contract Schema

The portable, runtime-independent structure of every Agent Skill Contract.

```yaml
name: Skill Contract Schema
path: .interface/foundation/schema/skill-contract.md
kind: Structure standard
responsibility: Defines the portable, runtime-independent structure followed by every declared Agent Skill Contract
```

→ [Skill Contract Schema](schema/skill-contract.md)

#### Personality Schema

The structure of every Personality definition file under `agent/personality/definitions/`.

```yaml
name: Personality Schema
path: .interface/foundation/schema/personality.md
kind: Structure standard
responsibility: Defines the structure followed by every Personality definition file under agent/personality/definitions/
```

→ [Personality Schema](schema/personality.md)

#### Database Configuration Schema

The structure of the Database Component's runtime configuration file — supported Engines, selectable Instances with their connection settings and credentials, and the default Instance. It is conditional: it applies when the Implementation declares a Database Component, and an Implementation without one ignores it.

```yaml
name: Database Configuration Schema
path: .interface/foundation/schema/database.yaml
kind: Structure standard (conditional)
generates: <database component path>/database.yaml
responsibility: Defines the shape of the Database Component's runtime configuration file, so that adding an Instance or changing a credential is one edit in one file and no value is hardcoded in source
```

→ [Database Configuration Schema](schema/database.yaml)

### Operational formats

The stored structure and initial template of a generated record.

#### Application Manifest Schema

Generates `config/application.yaml`.

```yaml
name: Application Manifest Schema
path: .interface/foundation/schema/application.yaml
kind: Operational format
generates: .interface/foundation/config/application.yaml
responsibility: Defines the shared Component metadata sections and their empty initial structure
```

→ [Application Manifest Schema](schema/application.yaml)

#### State Schema

Generates `config/state.yaml`.

```yaml
name: State Schema
path: .interface/foundation/schema/state.yaml
kind: Operational format
generates: .interface/foundation/config/state.yaml
responsibility: Defines the stored structure and initial values of State Config
```

→ [State Schema](schema/state.yaml)

#### Plan Schema

Generates `config/plan.yaml`.

```yaml
name: Plan Schema
path: .interface/foundation/schema/plan.yaml
kind: Operational format
generates: .interface/foundation/config/plan.yaml
responsibility: Defines the stored structure and initial values of Plan Config
```

→ [Plan Schema](schema/plan.yaml)

#### Review Schema

Generates `config/review.yaml`.

```yaml
name: Review Schema
path: .interface/foundation/schema/review.yaml
kind: Operational format
generates: .interface/foundation/config/review.yaml
responsibility: Defines the stored structure and initial values of Review Config
```

→ [Review Schema](schema/review.yaml)

The Interface file's own statement of the Foundation Files — "Foundation Files provide foundational definitions and schemas required by the Interface." — was moved here verbatim on 2026-09-17 and merged into the entries above on 2026-09-18. Its earlier structure tree listed `interface.md` inside `foundation/`; the Structure tree at the top of this document supersedes it.


## Ownership

The Human owns `interface.md`, this document, the eight section files, and every Schema. Config records belong to the Components that own them — Plan, State, and Review — and are written only by the Skills the Interface authorizes for each record. Target definitions are intentionally **not** considered Foundation Files because they belong to the Target concept itself; they live in the Target Module.

<br>

## Understanding record

Not yet recorded. The Human's own explanation of Foundation — why the Interface file is the single entry point, how Schemas are meant to evolve, and what Config must never become — will be captured here in a later session, in the same form as the Agent Module Guide.

<br>

## Open decisions

None recorded yet.
