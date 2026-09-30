# Storage Service Definition

Storage Service is the fixed internal Logic Service whose Interface gives other Logic Services access to every public capability published by Database.

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

Storage Service is one of the two fixed internal Services of every Logic Component. It is Logic's complete gateway to Database: for every Entity Operation, Database-wide Operation, and Lifecycle Command currently published by Database Interface, Storage Service provides one corresponding Action. Its Interface also republishes the exact DatabaseInstance, request Vocabulary, and result contracts required by those Actions. Its implementation remains internal, its Interface is not published through Logic Interface by default, and API Group generation is disabled by default.

### Purpose

Logic Services need one controlled route to persistence. Storage Service provides that route through its own Service Interface without exposing Database internals. Entity Service and every other internal Logic Service use it whenever they need Database. Its publication setting may explicitly expose that Interface through Logic Interface, but the default keeps raw persistence and Lifecycle capabilities internal.

### How It Works

Storage Service carries an Interface and an Actions directory. It reads the three authoritative capability groups and DatabaseInstance from Database Interface. For every published Entity Operation, Database-wide Operation, and Lifecycle Command, it creates one corresponding Action file. That Action accepts the request defined by Database, forwards the request and selected DatabaseInstance member unchanged through Database Interface, and returns Database's declared result without adding a wrapper.

Every Action and its file are named `<service>_<action>`. The configured Service name is normalized, followed by exactly one underscore and the configured Action base name. With the default Service name, examples include `storage_add`, `storage_execute_command`, and `storage_create_tables`. An Action-name override may replace a capability's derived base name, but it never changes that capability's identity, group, or contract.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Storage Role** — the fixed identity of this Service inside Logic, independent of its configurable public name.
- **Storage Service Interface** — this Service's outward gateway for internal Logic collaboration, exposed unchanged through Logic Interface only when `publish_in_logic_interface` is enabled.
- **API Generation Setting** — the Service-level `generate_api` value that may request one Storage API Group only when root publication is also enabled; its default is `false`.
- **Action** — one Storage Service capability corresponding to one Entity Operation, Database-wide Operation, or Lifecycle Command published by Database Interface.
- **Database Capability Identity** — the stable identity and group by which an Action and any configured override are matched to a Database capability.
- **Published Action Name** — the identifier formed as `<service>_<action>` from the configured Service name and derived or overridden Action base name.
- **DatabaseInstance** — the exact enum published by Database Interface for its active Instances and republished unchanged by Storage Service Interface.
- **Database Request Vocabulary** — the exact Filter, FilterOperator, FilterCombination, Order, and OrderDirection types published by Database Interface and republished unchanged by Storage Service Interface.
- **Database Result Contracts** — the exact CommandResult and LifecycleResult types published by Database Interface and republished unchanged by Storage Service Interface.
- **ExecuteCommand** — the Database-wide Operation that accepts a SQL command and bound parameters and returns CommandResult.

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

- **Belongs to Logic** — is a fixed Service whose Interface always exists but is published through Logic Interface only when configured.
- **Consumes Database** — discovers and uses every member of Database's three public capability groups, DatabaseInstance, request Vocabulary, and result contracts only through Database Interface.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Entity-oriented convenience and Entity-specific Behaviour** — belong to Entity Service; Storage Service remains the raw Database gateway and does not absorb them.
- **Operation execution, Engine selection, connections, transactions, and result production** — belong to Database; Storage Service only requests published capabilities.
- **Capability meaning, group, identity, membership, and validity** — belong to Database Interface; Storage Service mirrors them without redefining them.
- **Logic's root publication of Services** — belongs to Logic Interface and follows this Service's publication setting; Storage Service owns only its own Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The outward gateway of Storage Service. It presents every derived Storage Action and republishes the exact DatabaseInstance, Database Request Vocabulary, and Database Result Contracts without recreating, renaming, converting, or copying them. Internal Logic Services may import it directly. Logic Interface exposes it unchanged under the configured Service name only when `publish_in_logic_interface` is enabled.

### Actions

The directory containing one Action file for every Entity Operation, Database-wide Operation, and Lifecycle Command currently published by Database Interface. Each file uses the published Action name, preserves its capability group and request and result contract, delegates to Database Interface, and contains no persistence implementation. A newly published Database capability receives a derived Action automatically even when no override exists.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Storage Service. Storage Service Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and applicable Logic and Database Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Storage Service is fixed and internal with its own Interface

**Rule:** Every Logic contains the fixed Storage Role as an internal Service and always creates Storage Service Interface. Its configured name may change, but its Role and responsibilities do not. Logic Interface publishes Storage Service Interface only when `publish_in_logic_interface` is `true`; the default is `false`. Its implementation remains internal in every case.
**Why:** Logic needs one stable and discoverable Database gateway without confusing the Service with the Database Component or exposing implementation files.
**Boundary:** Disabling root publication never disables the Service Interface for internal Logic collaboration. Enabling publication exposes only the Interface, never the Service implementation, Logic Core, or Database internals.

#### Storage API generation is disabled by default

**Rule:** Storage Service defaults both `publish_in_logic_interface` and `generate_api` to `false`. API may create a Storage Group only when Target explicitly enables both settings. Every callable Storage Action is API-enabled by default once the Service becomes eligible and may explicitly set `generate_api: false` in Storage Service Preferences.
**Why:** Raw persistence capabilities remain internal unless Target deliberately publishes and exposes the complete Service boundary.
**Boundary:** These settings declare eligibility only. Storage Service owns no HTTP route, method, schema, or transport Behaviour.

#### Storage Service is every internal Logic Service's only route to Database

**Rule:** Entity Service and every other Service inside Logic use Storage Service Interface whenever they need Database. No other internal Logic Service calls Database Interface or a Database implementation detail directly.
**Why:** One internal gateway keeps Database access consistent, discoverable, and replaceable across Logic Services.
**Boundary:** A Logic consumer may use Storage Service Interface directly only when its root publication is enabled. Storage Service owns the route and its raw Actions, while a calling Service continues to own any Behaviour it adds and Database continues to own persistence.

<br>

### Interface

#### Storage Service Interface follows Database's complete capability catalogue

**Rule:** Storage Service reads Database Interface as the authority for membership in Entity Operations, Database-wide Operations, and Lifecycle Commands and publishes exactly one corresponding Action for every member currently published there. A missing Action-name override never removes an Action; its name is derived from the stable capability identity.
**Why:** Storage Service remains complete when Database adds, removes, or regroups a public capability without maintaining a second manual catalogue.
**Boundary:** Storage Service neither adds a capability absent from Database Interface nor moves one to another group or treats a display label as a new identity.

#### Storage Service Interface republishes exact Database supporting contracts

**Rule:** Storage Service Interface republishes the same DatabaseInstance, Filter, FilterOperator, FilterCombination, Order, OrderDirection, CommandResult, and LifecycleResult objects or types published by Database Interface. Actions accept, pass, and return these values unchanged; Storage Service creates no alternate request or result type, identity, name, or value.
**Why:** A copied type may look identical while remaining incompatible with the Database request contract.
**Boundary:** Republishing supporting contracts exposes no Engine, connection, credential, session, mapping, configuration, storage path, or other private Database detail.

#### Published Action names identify Storage Service

**Rule:** Every Storage Action and corresponding Action file is named `<service>_<action>`. The configured Service name comes first, followed by exactly one underscore and the derived or overridden Action base name. Values are normalized only by the selected language's declared identifier convention.
**Why:** An Action remains visibly owned by Storage Service wherever another Service imports or calls it.
**Boundary:** The prefixed name identifies the Logic Service Action; it neither renames nor alters the corresponding Database capability identity or group.

#### Storage Interface identifiers are valid and unique

**Rule:** The configured Service name, every Action base name, every final Action name, and every public Interface export are valid for the selected language and unique after declared normalization. An Action name never collides with DatabaseInstance or another Interface export.
**Why:** Two Database capabilities cannot share one callable Action and an invalid identifier cannot be realized safely.
**Boundary:** An invalid, reserved, or colliding value stops generation with a clear configuration error. The generator never invents a suffix, number, or silent rename.

<br>

### Actions

#### Every Action preserves its Database capability contract

**Rule:** Every Storage Action accepts its Database capability's request, forwards that request and the selected DatabaseInstance member unchanged through Database Interface, and returns the declared result unchanged. When the Instance is omitted, Database chooses its configured default. Storage Service adds no result envelope or persistence interpretation.
**Why:** Database remains the single authority for persistence while Logic provides one consistent gateway for every Database request.
**Boundary:** Storage Service never selects an Engine or default Instance, exposes Database internals, or classifies ExecuteCommand or a Lifecycle Command as safe to retry.

#### Action overrides match stable Database capabilities

**Rule:** Each configured Action-name override names one existing Database capability by its stable identity. A capability without an override uses a derived base name. An override for an unknown, removed, or regrouped identity is a configuration error and is never ignored.
**Why:** Overrides remain deliberate naming choices instead of a stale second catalogue of Database capabilities.
**Boundary:** An override changes only the Storage Action's published name; it never changes capability membership, group, identity, request, or result meaning.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Storage Service is fixed and internal with its own Interface**

- **Must** — Include the Storage Role and its Interface internally in every Logic and apply its root-publication setting.
- **Never** — Publish it through Logic Interface when publication is disabled, expose its private implementation, or confuse its configurable name with its fixed Role.

**Storage API generation is disabled by default**

- **Must** — Require explicit root publication and API generation before a Storage API Group can exist.
- **Never** — Generate a Storage API Group while either setting is disabled or define HTTP details inside Storage Service.

**Storage Service is every internal Logic Service's only route to Database**

- **Must** — Require every internal Logic Service needing Database to use Storage Service Interface.
- **Never** — Let another internal Logic Service call Database Interface or Database internals directly.

<br>

### Interface

**Storage Service Interface follows Database's complete capability catalogue**

- **Must** — Derive exactly one Action for every Entity Operation, Database-wide Operation, and Lifecycle Command currently published by Database Interface.
- **Never** — Maintain a second authoritative catalogue, omit a capability because no override exists, or change its group.

**Storage Service Interface republishes exact Database supporting contracts**

- **Must** — Republish and pass the exact DatabaseInstance, request Vocabulary, CommandResult, and LifecycleResult unchanged.
- **Never** — Recreate, rename, convert, or copy Database request or result contracts or identities.

**Published Action names identify Storage Service**

- **Must** — Name every Action and Action file `<service>_<action>` with exactly one underscore.
- **Never** — Rename or alter the corresponding Database capability identity or group.

**Storage Interface identifiers are valid and unique**

- **Must** — Validate every public identifier for the selected language and uniqueness after normalization.
- **Never** — Resolve an invalid or colliding identifier with an invented or silent rename.

<br>

### Actions

**Every Action preserves its Database capability contract**

- **Must** — Forward every Database capability request and selected DatabaseInstance member unchanged and return Database's declared result unchanged.
- **Never** — Add a result wrapper, reinterpret a Database capability, expose Database internals, select an Engine or default Instance, or retry ExecuteCommand or a Lifecycle Command as safe.

**Action overrides match stable Database capabilities**

- **Must** — Match every override to an existing stable Database capability identity and group and derive the name when no override exists.
- **Never** — Ignore a stale override or let an override change a capability's group or contract.
