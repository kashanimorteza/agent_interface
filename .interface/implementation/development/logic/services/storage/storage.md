# Storage Service Definition

Storage Service is the fixed internal Logic Service whose public Interface gives Logic consumers and Services access to every Operation published by Database.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Storage Service is one of the two fixed internal Services of every Logic Component. It is Logic's complete gateway to Database: for every Operation currently published by Database Interface, Storage Service provides one corresponding Action. Its public Interface also republishes the exact active Database Instance Enum accepted by those Actions. Its implementation remains internal, while Logic Interface publishes Storage Service Interface unchanged under its configured name.

### Purpose

Logic Services need one controlled route to persistence, while consumers may also need direct access to raw Database capabilities. Storage Service provides both through one public Service Interface without exposing Database internals. Entity Service and every other internal Logic Service use it whenever they need Database; a consumer may use it directly when it intentionally needs raw persistence or Database-wide commands.

### How It Works

Storage Service carries an Interface and an Actions directory. It reads the authoritative Operation catalogue and Instance Enum from Database Interface. For every published Operation, it creates one corresponding Action file. That Action accepts the request defined by Database, forwards the request and selected Instance Enum member unchanged through Database Interface, and returns Database's declared result without adding a wrapper.

Every Action and its file are named `<service>_<action>`. The configured Service name is normalized, followed by exactly one underscore and the configured Action base name. With the default Service name, examples include `storage_add`, `storage_update`, and `storage_execute_command`. An Action-name override may replace an Operation's derived base name, but it never changes the Operation's identity or contract.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Storage Role** — the fixed identity of this Service inside Logic, independent of its configurable public name.
- **Storage Service Interface** — this Service's outward gateway, published unchanged under the configured Service name by Logic Interface.
- **Action** — one Storage Service capability corresponding to one Operation published by Database Interface.
- **Operation Identity** — the stable identity by which an Action and any configured override are matched to a Database Operation.
- **Published Action Name** — the identifier formed as `<service>_<action>` from the configured Service name and derived or overridden Action base name.
- **Database Instance Enum** — the exact enum published by Database Interface for its active Instances and republished unchanged by Storage Service Interface.
- **Execute Command** — the Database capability that accepts a SQL command and bound parameters and returns Database's published Command Result.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Storage Service
├── interface
└── actions/
    └── <service>_<action>
```

The names shown are defaults selected by Storage Service Preferences. Changing a name changes the realization path, not the responsibility represented by that member.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Belongs to Logic** — is a fixed Service whose Interface Logic Interface always publishes.
- **Consumes Database** — discovers and uses every Database Operation and the active Database Instance Enum only through Database Interface.
- **Consumed by Entity Service** — provides the Entity-bound Database Actions and Instance Enum that Entity Service uses.
- **Consumed by other Logic Services** — provides their only route to Database whenever their Behaviour requires persistence.
- **Consumed by Logic consumers** — provides direct raw Database capabilities through Storage Service Interface as published by Logic Interface.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Entity-oriented convenience and Entity-specific Behaviour** — belong to Entity Service; Storage Service remains the raw Database gateway and does not absorb them.
- **Operation execution, Engine selection, connections, transactions, and result production** — belong to Database; Storage Service only requests published capabilities.
- **Operation meaning, identity, membership, and validity** — belong to Database Interface; Storage Service mirrors the catalogue without redefining it.
- **Logic's root publication of Services** — belongs to Logic Interface; Storage Service owns only its own Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The outward gateway of Storage Service. It publishes every derived Storage Action and republishes the exact Database Instance Enum without recreating, renaming, converting, or copying its members. Logic Interface publishes this Service Interface unchanged under the configured Service name.

### Actions

The directory containing one Action file for every Operation currently published by Database Interface. Each file uses the published Action name, preserves its Operation's request and result contract, delegates to Database Interface, and contains no persistence implementation. A newly published Database Operation receives a derived Action automatically even when no override exists.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Storage Service. Storage Service Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and applicable Logic and Database Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Storage Service is fixed and internal with a public Interface

**Rule:** Every Logic contains the fixed Storage Role as an internal Service and publishes Storage Service Interface unchanged through Logic Interface. Its configured public name may change, but its Role and responsibilities do not. Consumers reach its raw Database capabilities through that public Interface; its implementation remains internal.
**Why:** Logic needs one stable and discoverable Database gateway without confusing the Service with the Database Component or exposing implementation files.
**Boundary:** Public means the Service Interface is reachable. It does not make the Service implementation, Logic Core, or Database internals public.

#### Storage Service is every internal Logic Service's only route to Database

**Rule:** Entity Service and every other Service inside Logic use Storage Service Interface whenever they need Database. No other internal Logic Service calls Database Interface or a Database implementation detail directly.
**Why:** One internal gateway keeps Database access consistent, discoverable, and replaceable across Logic Services.
**Boundary:** A Logic consumer may intentionally use the public Storage Service Interface directly. Storage Service owns the route and its raw Actions, while a calling Service continues to own any Behaviour it adds and Database continues to own persistence.

<br>

### Interface

#### Storage Service Interface follows Database's complete Operation catalogue

**Rule:** Storage Service reads Database Interface as the authority for Operation membership and publishes exactly one corresponding Action for every Operation currently published there. A missing Action-name override never removes an Action; its name is derived from the Operation identity.
**Why:** Storage Service remains complete when Database adds or removes an Operation without maintaining a second manual catalogue.
**Boundary:** Storage Service neither adds an Operation absent from Database Interface nor treats a display label as a new Operation identity.

#### Storage Service Interface republishes the exact Database Instance Enum

**Rule:** Storage Service Interface republishes the same Instance Enum object or type published by Database Interface. Every Action accepts a member of that Enum and passes it unchanged; Storage Service creates no alternate Instance enum, identity, name, or value.
**Why:** A copied Enum may look identical while remaining incompatible with the Database request contract.
**Boundary:** Republishing the Enum exposes no Engine, connection, credential, session, mapping, configuration, or other private Database detail.

#### Published Action names identify Storage Service

**Rule:** Every Storage Action and corresponding Action file is named `<service>_<action>`. The configured Service name comes first, followed by exactly one underscore and the derived or overridden Action base name. Values are normalized only by the selected language's declared identifier convention.
**Why:** An Action remains visibly owned by Storage Service wherever another Service imports or calls it.
**Boundary:** The prefixed name identifies the Logic Service Action; it neither renames nor alters the corresponding Database Operation identity.

#### Public Storage identifiers are valid and unique

**Rule:** The configured Service name, every Action base name, every final Action name, and every public Interface export are valid for the selected language and unique after declared normalization. An Action name never collides with the Database Instance Enum or another Interface export.
**Why:** Two Operations cannot share one callable Action and an invalid identifier cannot be realized safely.
**Boundary:** An invalid, reserved, or colliding value stops generation with a clear configuration error. The generator never invents a suffix, number, or silent rename.

<br>

### Actions

#### Every Action preserves its Database Operation contract

**Rule:** Every Storage Action accepts its Database Operation's request, forwards that request and the selected Database Instance Enum member unchanged through Database Interface, and returns the declared result unchanged. When the Instance is omitted, Database chooses its configured default. Storage Service adds no result envelope or persistence interpretation.
**Why:** Database remains the single authority for persistence while Logic provides one consistent gateway for every Database request.
**Boundary:** Storage Service never selects an Engine or default Instance, exposes Database internals, or classifies Execute Command as safe to retry.

#### Action overrides match stable Database Operations

**Rule:** Each configured Action-name override names one existing Database Operation by its stable identity. An Operation without an override uses a derived base name. An override for an unknown or removed Operation is a configuration error and is never ignored.
**Why:** Overrides remain deliberate naming choices instead of a stale second catalogue of Database capabilities.
**Boundary:** An override changes only the Storage Action's published name; it never changes Operation membership, identity, request, or result meaning.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Storage Service is fixed and internal with a public Interface**

- **Must** — Include the Storage Role internally in every Logic and publish its Interface unchanged under its configured name.
- **Never** — Expose its private implementation or confuse its configurable name with its fixed Role.

**Storage Service is every internal Logic Service's only route to Database**

- **Must** — Require every internal Logic Service needing Database to use Storage Service Interface.
- **Never** — Let another internal Logic Service call Database Interface or Database internals directly.

### Interface

**Storage Service Interface follows Database's complete Operation catalogue**

- **Must** — Derive exactly one Action for every Operation currently published by Database Interface.
- **Never** — Maintain a second authoritative Operation catalogue or omit an Operation because no override exists.

**Storage Service Interface republishes the exact Database Instance Enum**

- **Must** — Republish and pass the exact Database Instance Enum unchanged.
- **Never** — Recreate, rename, convert, or copy Database Instance identities.

**Published Action names identify Storage Service**

- **Must** — Name every Action and Action file `<service>_<action>` with exactly one underscore.
- **Never** — Rename or alter the corresponding Database Operation identity.

**Public Storage identifiers are valid and unique**

- **Must** — Validate every public identifier for the selected language and uniqueness after normalization.
- **Never** — Resolve an invalid or colliding identifier with an invented or silent rename.

### Actions

**Every Action preserves its Database Operation contract**

- **Must** — Forward every Operation request and selected Instance Enum member unchanged and return Database's declared result unchanged.
- **Never** — Add a result wrapper, reinterpret a Database Operation, expose Database internals, select an Engine or default Instance, or retry Execute Command as safe.

**Action overrides match stable Database Operations**

- **Must** — Match every override to an existing stable Operation identity and derive the name when no override exists.
- **Never** — Ignore a stale override or let an override change an Operation contract.
