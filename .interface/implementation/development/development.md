# Development Definition

Development is the Implementation Subsystem that coordinates the Components of one application through shared defaults and direct Connections.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Components](#components)**
5. **[Relationships](#relationships)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Development coordinates independent Components into one application. It owns their shared defaults and direct Connections. Each Component owns its own meaning, implementation, technical choices, documentation, and Public Interface.

### Purpose

Components need one place for the defaults and relationships they genuinely share. Development supplies that common context without duplicating a Component's own configuration.

### How It Works

Each Component resolves its own Preferences first, then uses a Development Default only when its own Preference leaves a shared choice unstated. A declared Connection permits its consumer to use the provider's public classes and layers.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Component** — one peer part of the Development Subsystem with its own Definition, Preferences, and Public Interface.
- **Development Default** — a shared value a Component may use only when its own Preferences do not select that value.
- **Public Interface** — the Component-owned surface through which another Component uses it; each Component explains its own public contents.
- **Connection** — one direct dependency from a consumer Component to a provider Component.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

Development owns only shared coordination: defaults and Connections. Each Component owns its own content, technical choices, documentation, and Public Interface. Platform owns runtime and launch details.

<br>

<!--------------------------------------------------------------------------------- Components --->
## Components

```text
Components
├── Model
├── Database
├── Logic
├── API
├── Presentation
└── Platform
```

### Model

The reusable data library of the application.

→ [Definition of Model](model/model.md)<br>
→ [Preferences of Model](model/model.yaml)

### Database

Storage, offered through its Public Interface.

→ [Definition of Database](database/database.md)<br>
→ [Preferences of Database](database/database.yaml)

### Logic

The application's Behaviour, held in its Services.

→ [Definition of Logic](logic/logic.md)<br>
→ [Preferences of Logic](logic/logic.yaml)

### API

API exposes application capabilities through its external Public Interface.

→ [Definition of API](api/api.md)<br>
→ [Preferences of API](api/api.yaml)

### Presentation

Presentation provides the user-facing application through its Public Interface.

→ [Definition of Presentation](presentation/presentation.md)<br>
→ [Preferences of Presentation](presentation/presentation.yaml)

### Platform

The runtime and deployment foundation of the application.

→ [Definition of Platform](platform/platform.md)<br>
→ [Preferences of Platform](platform/platform.yaml)

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

Development consumes no Component.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Development Definition Principles are mandatory.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Components own their own content and technical choices

**Rule:** Each Component owns its Definition, Preferences, technical selections, implementation, and Public Interface. Development does not duplicate or redefine those details.

**Why:** Ownership stays clear and a Component can change internally without maintaining a second configuration elsewhere.

**Boundary:** Development retains only values that are genuinely shared defaults or relationships across Components.

<br>

### Cross-Component use follows declared Connections

**Rule:** Every cross-Component interaction uses public classes or layers from its provider and requires one declared direct Connection. Each provider defines and documents the public concepts it offers; a Connection records only consumer and provider. A consumer locates the provider's Interface only from the provider's own Preferences and knows its contracts only through that Interface.

**Why:** Consumers can use the provider's available public surface without creating hidden dependencies.

**Boundary:** Public availability does not create an undeclared Connection, and a consumer never reads, changes, or depends on another Component's private resources.

<br>

### The declared Connection graph is direct, explicit, and acyclic

**Rule:** Every permitted direct dependency is declared exactly once as a Connection in Development Preferences. Connection direction runs from consumer to provider, is direct and non-transitive, and forms no cycle.

**Why:** One directed graph makes dependency ownership visible and prevents hidden or circular coupling.

**Boundary:** A provider response creates no reverse Connection, and an indirect path never grants direct access.

<br>

### Component packages are project-internal

**Rule:** Every Component package is used only inside this project. Each declared Connection is realized as a local path dependency on the provider's directory within the repository; no Component package is published, pinned to a package index, or installed outside the project directory.

**Why:** The Components form one application, so their dependencies resolve from the repository itself.

**Boundary:** A built package that names a provider by its plain name is expected and is not an Open Question. Third-party packages still resolve from their package index.

<br>

### The project has one ignore file

**Rule:** The project root holds the only version-control ignore file. No Component or package creates an ignore file of its own; when a Component needs a path ignored, generation adds that entry to the root file, scoped to the Component's directory where it applies only there, and never adds an entry that is already present.

**Why:** One ignore file shows in one place everything the repository leaves out, so no Component's rule hides or contradicts another's.

**Boundary:** Generation only adds the entries a Component needs; it never removes or rewrites an existing entry of the root file.

<br>

### Unstated shared decisions follow one precedence order

**Rule:** Resolve every unstated choice in this order: explicit Component Preference, Development Default, then the executor's own proposal. The executor never stops or asks for an unstated choice: it proceeds with its own proposal and records the decision.

**Why:** Work never stalls on a gap, and the Human sees every decision in one place and changes Preferences when needed.

**Boundary:** The executor's own proposal never overrides Target meaning, an applicable Principle, or an explicit Preference. A Default never creates, replaces, or changes a Component-owned decision.

<br>

### Public surface changes propagate through direct consumers

**Rule:** A provider may change non-public implementation without consumer changes while its public surface remains compatible. When a public class, layer, or Interface changes, each direct consumer in the declared Connection graph is reviewed and updated or regenerated when affected.

**Why:** Change follows actual dependencies without rebuilding unrelated Components.

**Boundary:** A non-public change with no public-surface effect triggers no consumer work, and a public change authorizes no change outside the affected dependency path.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Components own their own content and technical choices**

- **Must** — Keep Component Definition, Preferences, technical choices, implementation, and Public Interface with its owner.
- **Never** — Duplicate or redefine Component-owned details in Development.

**Cross-Component use follows declared Connections**

- **Must** — Use only public classes or layers from a provider with a declared direct Connection.
- **Never** — Treat public availability as an undeclared Connection or depend on another Component's private resources.

**The declared Connection graph is direct, explicit, and acyclic**

- **Must** — Declare every direct dependency once in Development.
- **Never** — Infer direct access from an indirect path or create a dependency cycle.

**Component packages are project-internal**

- **Must** — Realize every Connection as a local path dependency within the repository.
- **Never** — Publish or install a Component package outside the project.

**The project has one ignore file**

- **Must** — Add every needed ignore entry to the root ignore file, once.
- **Never** — Create an ignore file inside a Component or package, or remove an existing root entry.

**Unstated shared decisions follow one precedence order**

- **Must** — Resolve an unstated choice by Component Preference, Development Default, then own proposal, and record the decision.
- **Never** — Stop or ask for an unstated choice, or let a proposal override Target meaning, a Principle, or an explicit Preference.

**Public surface changes propagate through direct consumers**

- **Must** — Review and update or regenerate every affected direct consumer when a public surface changes.
- **Never** — Trigger consumer work for a non-public change or change anything outside the affected dependency path.
