# Foundation Files

This guide explains what Foundation Files contain, why they are shared, and who owns them.

Foundation is not one of the three Modules (Target, Implementation, Agent). It is the set of shared resources those Modules and every Skill depend on.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

This guide maps Foundation Files to their authoritative sources.

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Agent Native Sync](#agent-native-sync)**
5. **[Schema](#schema)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

This document explains the Foundation directory: what it holds, why those files are shared by the whole Interface, and who may change them. It is Human-owned and explains; it does not redefine. The canonical definition remains `interface.md`, one level above this directory, which describes the complete system; this document describes only this directory and its contents.

Foundation Files provide the foundational definitions and schemas required by the Interface: the canonical Interface document that every Understanding starts from and the Schemas that define how authored and generated files are shaped. Config is a separate operational boundary that uses some of these Schemas.

Config contains the generated Application, State, Plan, and Review records. It is outside the Foundation directory and is the only writable area of the Interface for authorized Skills; each record remains owned and writable only under its owning Component's authority.

### Purpose

Foundation keeps shared Interface resources separate from the Target, Implementation, and Agent Modules.

### How It Works

The Interface routes an Agent to the relevant Foundation source or Schema. Config records use the applicable Foundation Schemas and remain owned by their declared operational authority.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Foundation** — shared resources required by the Modules and Skills.
- **Schema** — the structure of an authored source or operational record.
- **Config** — an operational record used by the Workflow.
- **Interface file** — the canonical navigation entry point for Agent Interface.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
.interface/
└── foundation/
    ├── foundation.md
    ├── introduction.md
    ├── terms.md
    ├── architecture.md
    ├── understanding.md
    ├── authority.md
    ├── workflow.md
    ├── agent-native-sync.md
    └── schema/
        ├── application.yaml
        ├── yaml.yaml
        ├── <component>.md
        ├── <component>.yaml
        ├── personality.md
        ├── state.yaml
        ├── plan.yaml
        └── review.yaml
```

<br>

<!--------------------------------------------------------------------------------- Agent Native Sync --->
## Agent Native Sync

The Foundation instruction that creates and updates the `/my-interface-agent-native` Skill and uses it to synchronize the complete Agent Module with the selected Agent Native.

Responsibility: Defines the Agent Native Sync Skill and its read-only Agent Module synchronization procedure.

→ [Read more about Agent Native Sync](agent-native-sync.md)

<br>

<!--------------------------------------------------------------------------------- Schema --->
## Schema

Schemas define the structure followed by authored Interface files and generated operational records. Two kinds exist: **Structure standards**, the shape a Human-authored file follows, and **Operational formats**, the stored structure and initial template of a generated record. Schema definition files use their own formats and do not follow the outer YAML frame they define.

```text
.interface/foundation/schema/
├── yaml.yaml
├── <component>.md
├── <component>.yaml
├── personality.md
├── database.yaml
├── application.yaml
├── state.yaml
├── plan.yaml
└── review.yaml
```

### YAML Schema

The common outer frame (meta, policy, read_order, content_map, content) followed by Component Preferences and Config files.

Responsibility: Defines the common outer structure followed by Component Preferences and Config files. Schema definition files use their own formats and do not follow this outer structure.

→ [Read more about YAML Schema](schema/yaml.yaml)

### Definition Schema

The common Markdown structure of every Implementation and Agent Component `<component>.md`.

Responsibility: Defines the common Markdown structure followed by every Implementation and Agent Component `<component>.md` file.

→ [Read more about Definition Schema](schema/schema.md)

### Preferences Schema

The common structure of every Component `<component>.yaml` file.

Responsibility: Defines the common Preferences structure followed by every Component `<component>.yaml` file.

→ [Read more about Preferences Schema](schema/schema.yaml)

#### Personality Schema

The structure of every Personality Contract file under `agent/personality/contracts/`.

Responsibility: Defines the structure followed by every Personality Contract file under `agent/personality/contracts/`.

→ [Read more about Personality Schema](schema/personality.md)

#### Database Configuration Schema

The structure of the Database Component's runtime configuration file — supported Engines, selectable Instances with their connection settings and credentials, and the default Instance. It is conditional: it applies when the Implementation declares a Database Component, and an Implementation without one ignores it.

Responsibility: Defines the conditional shape of the Database Component's runtime configuration file so that adding an Instance or changing a credential is one edit in one file and no value is hardcoded in source.

→ [Read more about Database Configuration Schema](schema/database.yaml)

### Operational formats

The stored structure and initial template of a generated record.

### Application Manifest Schema

Generates `config/application.yaml`.

Responsibility: Defines the shared Component metadata sections and their empty initial structure for `config/application.yaml`.

→ [Read more about Application Manifest Schema](schema/application.yaml)

### State Schema

Generates `config/state.yaml`.

Responsibility: Defines the stored structure and initial values of State Config for `config/state.yaml`.

→ [Read more about State Schema](schema/state.yaml)

### Plan Schema

Generates `config/plan.yaml`.

Responsibility: Defines the stored structure and initial values of Plan Config for `config/plan.yaml`.

→ [Read more about Plan Schema](schema/plan.yaml)

### Review Schema

Generates `config/review.yaml`.

Responsibility: Defines the stored structure and initial values of Review Config for `config/review.yaml`.

→ [Read more about Review Schema](schema/review.yaml)
