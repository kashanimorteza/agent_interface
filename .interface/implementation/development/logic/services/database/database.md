# Database Service Definition

Database Service is the fixed public Logic Service through which Logic uses every Operation published by Database.

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

Database Service is one of the two fixed Services of every Logic Component. It is Logic's complete gateway to Database: every Operation published by Database Interface has one corresponding Action in Database Service, and the active Database Instances available to those Actions are published through its Interface. Its Service Interface is published unchanged through Logic Interface.

### Purpose

Logic Services need one controlled route to persistence. Database Service gives every Database Operation one Logic-owned Action, so Entity Service and any other Logic Service can use Database without calling the Database Component directly or depending on its implementation.

### How It Works

Database Service carries an Interface and an Actions directory. For every Operation Database Interface publishes, the Actions directory contains one corresponding Action. Each Action accepts the request defined by Database, including its optional Database Instance, forwards it through Database Interface, and returns the result through Database Service Interface. Every published Action and its file are named `<service>_<action>`, so their owner remains visible wherever another Logic Service uses them. With the default Service name, Execute Command is published as `database_execute_command`.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Database Service Interface** — this Service's outward gateway, published unchanged under the Database Service name by Logic Interface.
- **Action** — one capability implemented and provided by Database Service from its Actions directory.
- **Database Operation Action** — the one Database Service Action corresponding to one Operation published by Database Interface.
- **Published Action Name** — the Action identifier formed as `<service>_<action>`, using the configured Service name and Action name in implementation naming form.
- **Execute Command** — the Database capability that accepts a command string and optional parameters and returns Database's published command result.
- **Database Instance** — an active destination published by Database Interface and optionally selected for Execute Command.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Database Service
├── interface
└── actions/
    └── <service>_<action>
```

The names shown are defaults selected by Database Service Preferences. Changing a name changes the realization path, not the responsibility represented by that member.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Belongs to Logic** — is a fixed Service whose Interface Logic Interface always publishes.
- **Consumes Database** — uses every Database Operation and active Database Instance only through Database Interface.
- **Consumed by Entity Service** — provides the Database Operation Actions Entity Service uses while applying Entity Behaviour.
- **Consumed by other Logic Services** — provides their only route to Database whenever their Behaviour requires persistence.
- **Consumed by Logic consumers** — is reached only through Database Service Interface as published by Logic Interface.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Entity-specific application Behaviour** — belongs to Entity Service; Database Service supplies its Database Actions but does not absorb that Behaviour.
- **Operation execution, engine selection, connections, transactions, and result production** — belong to Database; Database Service only requests the published capability.
- **Operation meaning and validity** — are defined and interpreted by Database, not redefined by Database Service.
- **Logic's root publication of Services** — belongs to Logic Interface; Database Service owns only its own Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The outward gateway of Database Service. It publishes the Actions the Service provides and the active Database Instances those Actions accept, without exposing a private implementation detail. Logic Interface publishes this Service Interface unchanged under the Database Service name.

### Actions

The directory containing one Action for every Operation published by Database Interface. Database Service currently carries Add, Update, List, Delete, Enable, Disable, Get by ID, Count, Sum, Min, Max, Truncate, Execute Command, Create Tables, and Insert Initial Data. Each Action preserves Database's request and result contract and is published through Database Service Interface.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Database Service. Database Service Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and applicable Logic and Database Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Database Service is fixed and public through its Interface

**Rule:** Every Logic contains Database Service and publishes Database Service Interface unchanged through Logic Interface. Consumers reach its capabilities through that published Interface; its implementation remains private.
**Why:** Whole-database Behaviour has one stable and discoverable gateway in every Logic without exposing implementation files.
**Boundary:** Public means the Service Interface is reachable; it does not make the Service implementation or Logic Core public.

<br>

#### Database Service is Logic's only route to Database

**Rule:** Every Service inside Logic uses Database Service Interface whenever it needs Database. No other Logic Service calls Database Interface or a Database implementation detail directly.
**Why:** One internal gateway keeps Database access consistent, discoverable, and replaceable across all Logic Services.
**Boundary:** Database Service owns the route and its Actions, while the calling Service continues to own its application Behaviour and Database continues to own persistence.

<br>

### Interface

#### Database Service Interface publishes every Database Operation Action and active Instance

**Rule:** Database Service Interface publishes exactly one Action corresponding to every Operation published by Database Interface: Add, Update, List, Delete, Enable, Disable, Get by ID, Count, Sum, Min, Max, Truncate, Execute Command, Create Tables, and Insert Initial Data. It also publishes the active Database Instances accepted by those Actions, using the Instance identities published by Database Interface without redefining them.
**Why:** Every Logic Service can reach the complete Database contract through one stable Logic-owned gateway.
**Boundary:** Publishing Instance identities does not expose Database engines, connections, sessions, mappings, configuration, or another private Database detail.

<br>

#### Published Action names identify Database Service

**Rule:** Every Action published by Database Service Interface and every corresponding Action file is named `<service>_<action>`. The Service and Action names come from Database Service Preferences and are normalized to the implementation's identifier convention; the separator is one underscore. With the defaults, the names include `database_add`, `database_update`, and `database_execute_command`.
**Why:** An Action remains visibly owned by Database Service when another Logic Service imports or calls it.
**Boundary:** The prefixed name identifies the Logic Service Action; it does not rename or alter the corresponding Operation published by Database Interface.

<br>

### Actions

#### Every Action preserves its Database Operation contract

**Rule:** Every Operation published by Database Interface is implemented as one corresponding Action in the Actions directory. The Action accepts the Operation's request, forwards that request and the selected Database Instance unchanged through Database Interface, and returns the resulting outcome. When the Instance is omitted, Database chooses its configured default.
**Why:** Database remains the single authority for persistence while Logic provides one consistent Service gateway for every Database request.
**Boundary:** Database Service never redefines or interprets an Operation, selects an engine or default Instance, or exposes Database internals. Execute Command is never classified as safe to retry.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Database Service is fixed and public through its Interface**

- **Must** — Include Database Service in every Logic and publish its Interface unchanged.
- **Never** — Expose its private implementation as part of the public Service.

**Database Service is Logic's only route to Database**

- **Must** — Require every Logic Service needing Database to use Database Service Interface.
- **Never** — Let another Logic Service call Database Interface or Database internals directly.

### Interface

**Database Service Interface publishes every Database Operation Action and active Instance**

- **Must** — Publish exactly one Action for every Operation and every active Instance identity published by Database Interface.
- **Never** — Publish private Database details.

**Published Action names identify Database Service**

- **Must** — Name every published Action and Action file `<service>_<action>` with one underscore and identifier normalization.
- **Never** — Rename the corresponding Database Interface Operation.

### Actions

**Every Action preserves its Database Operation contract**

- **Must** — Forward every Operation request and selected Database Instance unchanged through Database Interface and return the resulting outcome.
- **Never** — Redefine or interpret a Database Operation, expose Database internals, select an engine or default Instance, or retry Execute Command as safe.
