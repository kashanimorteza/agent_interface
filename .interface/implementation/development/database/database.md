# Database Definition

Database is the Development Component that persists Model data and provides standard data operations to Logic.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Layering](#layering)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Database is the Development Component that persists Model data and publishes data Operations to Logic. It contains Configuration, Operations, and the Public Interface, Mapping, and Engine layers.

### Purpose

Database keeps persistence knowledge in one Component. Without that separation, Engine selection, storage behavior, and data-operation handling spread into Logic and become inconsistent.

### How It Works

Logic sends an Operation request through Public Interface. Mapping resolves the applicable Instance and Engine, passes the request to that Engine, standardizes the result when needed, and returns it through Public Interface.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Engine** — a supported database technology and its implementation.
- **Instance** — a named database connection and storage identity using one Engine.
- **Database Configuration** — the declared Engines, Instances, Settings, and Operations available to Database.
- **Settings** — component-wide choices such as the default Instance, purpose-to-Instance assignments, and secret references.
- **Core Operation** — a fixed public operation that works with one Model, such as add, edit, update, list, delete, enable, disable, or get by ID.
- **Extra Operation** — an optional public operation with its own request and result shape, such as a report.
- **Public Interface** — the boundary through which Logic requests configured Operations.
- **Mapping** — the internal layer that routes a request to its Instance and Engine and standardizes its result when needed.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Database
├── Configuration
├── Operations
│   ├── Core Operations
│   └── Extra Operations
└── Layers
    ├── Public Interface
    ├── Mapping
    └── Engine
```

**Configuration** declares the Database resources and Operation catalogue.

**Operations** separates fixed Core Operations for one Model from optional Extra Operations for other purposes.

**Layers** contains the Public Interface that receives requests, Mapping that resolves and handles them, and Engine implementations that perform storage work.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — persists the Models and their declared data shapes.
- **Provides to Logic** — exposes configured Operations through its Public Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

- **Public Interface** — receives Operation requests from Logic and returns their results.
- **Mapping** — resolves the requested Instance and Engine, routes the Operation, and standardizes returned data when required.
- **Engine** — performs the storage behavior for its Engine-specific implementation.

Database's technical selections, defaults, and layout belong to Database Preferences. The structure of its generated configuration belongs to its Schema. This Definition states only the conceptual layers and the rules that govern them.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Database Principle is mandatory. Database Preferences may provide defaults and stricter conventions, but never weaken or override a Principle. An explicit Target requirement and an applicable Principle take precedence over a Preference.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Database configuration declares its available resources

**Rule:** Database Configuration declares every supported Engine, its engine-specific parameters, every named Instance and its connection parameters, and component Settings such as the default Instance, purpose assignments, secret references, and other shared parameters. Every Instance names one declared Engine, and every configured Instance reference resolves to a declared Instance.

**Why:** One configuration source makes the available storage resources and their selection explicit.

**Boundary:** Preferences define technical defaults and conventions; Database Configuration records the current resources and settings.

<br>

### Database exposes explicit public Operations

**Rule:** Public Interface publishes only the enabled Operations declared in Database Configuration. Core Operations are the fixed operations that work with one Model and use their shared request and result standard. Extra Operations are optional and define the request and result shape appropriate to their own purpose. Every Operation accepts optional filters and optional ordering by field.

**Why:** An explicit operation catalogue keeps the public data surface stable and understandable.

**Boundary:** Public Interface receives and returns requests; it does not select an Engine or implement database-specific behavior.

<br>

### Mapping routes requests and handles results

**Rule:** Mapping receives each request from Public Interface, resolves the requested Instance and its Engine, forwards the Operation to that Engine implementation, and standardizes the returned data when required before returning it to Public Interface. Mapping provides one mapping action for each published Operation.

**Why:** A single routing layer keeps selection, translation, and result handling consistent across Engines.

**Boundary:** Mapping coordinates an operation; each Engine implementation owns the Engine-specific execution of that operation.

<br>

### Each Engine implements the published Operations

**Rule:** Every declared Engine has an implementation isolated from the other Engines. It implements the published Operations with the Engine's own packages, parameters, and mechanisms while preserving the applicable operation request and result standard.

**Why:** Separate Engine implementations make support for each database technology clear and independently maintainable.

**Boundary:** Engine implementations perform storage behavior; the Operation catalogue, routing, and public boundary remain outside them.

<br>

### Database connects Model to Logic

**Rule:** Database uses Model declarations to persist Model data and provides its configured Operations to Logic through Public Interface.

**Why:** This keeps persistence aligned with domain data while giving Logic one consistent data boundary.

**Boundary:** Model owns domain declarations; Logic owns application behavior; Database owns the persistence implementation between them.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Database configuration declares its available resources**

- **Must** — declare every supported Engine, its parameters, named Instances, and component Settings in Database Configuration.
- **Must** — make every Instance name a declared Engine and every configured Instance reference resolve to a declared Instance.

**Database exposes explicit public Operations**

- **Must** — publish only enabled Operations declared in Database Configuration.
- **Must** — use the shared Core-operation standard for Core Operations.
- **Must** — give every Extra Operation the request and result shape required by its own purpose.
- **Must** — accept optional filters and optional field ordering for every Operation.

**Mapping routes requests and handles results**

- **Must** — route every Public Interface request to the resolved Instance and Engine.
- **Must** — provide one Mapping function for each published Operation.
- **Must** — standardize returned data whenever that Operation requires it.

**Each Engine implements the published Operations**

- **Must** — keep an isolated implementation for every declared Engine.
- **Must** — implement published Operations with the selected Engine's packages, parameters, and mechanisms.
- **Must** — preserve each Operation's applicable request and result standard.

**Database connects Model to Logic**

- **Must** — use Model declarations when persisting Model data.
- **Must** — provide configured Database Operations to Logic through Public Interface.
