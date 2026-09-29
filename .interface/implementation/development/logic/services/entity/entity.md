# Entity Service Definition

Entity Service is the fixed public Logic Service that provides Behaviour for every Entity published by Model.

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

Entity Service is one of the two fixed Services of every Logic Component. It gives each Entity published by Model a Service through which consumers use the Database capabilities that concern that Entity. Its Service Interface is published unchanged through Logic Interface.

### Purpose

Entity-bound Behaviour needs one owner between a consumer and persistence. Without Entity Service, consumers would call Database Service Actions directly, repeat application rules, and handle the same Entity differently. Entity Service keeps that Behaviour beside the Entity-specific Service that owns it while using Model Interface for Entity meaning and Database Service Interface for persistence.

### How It Works

Entity Service reads the Entity classes published by Model Interface. It carries one shared private base that implements the Entity-facing Actions corresponding to the Entity-bound Actions published by Database Service Interface, then creates one child Service for every published Entity. A child inherits the shared Actions and changes or extends them only when its Entity needs additional Behaviour.

Every Action accepts an optional Database Instance. Entity Service passes the request and selected Instance to the corresponding `<service>_<action>` Action on Database Service Interface, such as `database_add` or `database_list`. Database Service then forwards them to Database Interface; when the Instance is omitted, Database chooses its configured default. Entity Service Interface publishes the child Services and their capabilities, never the private base.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity Service Interface** — this Service's outward gateway, published unchanged under the Entity Service name by Logic Interface.
- **EntityServiceBase** — the private shared implementation of Entity Actions that use the corresponding Database Service Actions.
- **Entity Child Service** — the Service belonging to one Entity published by Model, inheriting the shared Operations and owning any Entity-specific Behaviour.
- **Entity-bound Action** — an Entity Service Action whose request names or carries an Entity and uses the corresponding Database Service Action: Add, Get by ID, Update, Delete, Enable, Disable, List, Count, Sum, Min, Max, or Truncate.
- **Database Instance** — an active destination published through Database Service Interface and optionally selected for one Entity Action.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Service
├── interface
├── base
└── entities/
    └── <entity>
```

The names shown are defaults selected by Entity Service Preferences. Changing a name changes the realization path, not the responsibility represented by that member.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Belongs to Logic** — is a fixed Service whose Interface Logic Interface always publishes.
- **Consumes Model** — discovers and imports authoritative Entity classes only through Model Interface.
- **Consumes Database Service** — performs persistence only through the Actions and Instances accepted by Database Service Interface.
- **Consumed by Logic consumers** — is reached only through the Entity Service Interface published by Logic Interface.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Domain meaning and Entity declarations** — belong to Model; Entity Service imports and uses them without copying them.
- **Database Actions and routing to Database Interface** — belong to Database Service; Entity Service uses them without redefining them.
- **Tables, engines, sessions, mappings, migrations, and storage guarantees** — belong to Database; neither Entity Service nor Database Service reimplements them.
- **Logic's root publication of Services** — belongs to Logic Interface; Entity Service owns only its own Interface.
- **Transport and presentation** — belong to their consuming Components; Entity Service returns transport-independent outcomes.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The outward gateway of Entity Service. It publishes every Entity Child Service and the capabilities those Services offer. It does not publish EntityServiceBase or another private implementation file.

### Base

The private shared implementation of the Entity Actions corresponding to Entity-bound Database Service Actions. It holds Behaviour common to every Entity Child Service, calls Database Service Interface for persistence, and is never a consumer dependency.

### Entities

One file and one child Service per Entity published by Model Interface. A child inherits shared Behaviour and contains only Behaviour specific to its Entity.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Entity Service. Entity Service Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and applicable Logic, Model, and Database Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Entity Service is fixed and public through its Interface

**Rule:** Every Logic contains Entity Service and publishes Entity Service Interface unchanged through Logic Interface. Consumers reach its capabilities through that published Interface; its implementation remains private.
**Why:** Entity Behaviour has one stable and discoverable gateway in every Logic without exposing implementation files.
**Boundary:** Public means the Service Interface is reachable; it does not make EntityServiceBase, child implementation files, or Core public.

<br>

### Interface

#### Entity Service Interface publishes Entity Child Services only

**Rule:** Entity Service Interface publishes one Entity Child Service for every Entity published by Model Interface and never publishes EntityServiceBase. Each published child exposes its inherited and Entity-specific capabilities.
**Why:** Consumers can select the Entity they need without depending on the mechanism shared among Entities.
**Boundary:** Logic Interface references and publishes Entity Service Interface unchanged; it does not copy these capabilities.

<br>

### Base

#### Shared Entity Actions are implemented once

**Rule:** EntityServiceBase implements every Entity Action corresponding to an Entity-bound Action published by Database Service Interface. Every Entity Child Service inherits those Actions and overrides one or adds another only when its Entity requires distinct Behaviour.
**Why:** One shared implementation prevents Entity Behaviour and use of Database Service from drifting across Entity Services.
**Boundary:** EntityServiceBase implements Entity Behaviour around a Database Service call; it never implements persistence or redefines a Database Service Action.

<br>

### Entities

#### Every Model Entity receives one child Service

**Rule:** Entity Service creates exactly one child Service and one corresponding implementation file for every Entity published by Model Interface. No child copies or redefines its Entity.
**Why:** The set of Entity Services stays complete and synchronized with Model's authoritative publication.
**Boundary:** An Entity-specific child may add Behaviour but cannot change the Entity declaration owned by Model.

<br>

### Database

#### Every Entity Action preserves the selected Database Instance

**Rule:** Every Entity Service Action accepts an optional Database Instance and passes it unchanged with every Database Service Interface call made for that Action. Database Service forwards it to Database Interface; omitting it delegates default selection to Database.
**Why:** A consumer can use the same Entity Behaviour against any active Database Instance without bypassing Logic or duplicating a Service.
**Boundary:** Entity Service neither calls Database Interface directly nor selects an engine, connection, table, or default Instance.

<br>

### Sensitive Values

#### Entity Service owns application-sensitive treatment

**Rule:** Entity Service uses Model's declared sensitivity meaning to apply any application-required encryption, decryption, hashing, credential handling, or withholding before or after a Database call. It never exposes an original sensitive value through its Interface, logs, errors, or outcomes.
**Why:** Sensitive-value Behaviour belongs to the application Service using the Entity, not to general-purpose persistence.
**Boundary:** Database Service forwards treated values without interpreting their sensitivity, Database stores and returns the values it receives, and Platform supplies runtime secrets.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Entity Service is fixed and public through its Interface**

- **Must** — Include Entity Service in every Logic and publish its Interface unchanged.
- **Never** — Expose its private implementation as part of the public Service.

### Interface

**Entity Service Interface publishes Entity Child Services only**

- **Must** — Publish one child Service for every Entity Model Interface publishes.
- **Never** — Publish EntityServiceBase or copy the Service capabilities into Logic Interface.

### Base

**Shared Entity Actions are implemented once**

- **Must** — Implement every Entity Action corresponding to an Entity-bound Database Service Action once in EntityServiceBase and inherit it in each child.
- **Never** — Implement persistence or redefine a Database Service Action in Entity Service.

### Entities

**Every Model Entity receives one child Service**

- **Must** — Create exactly one child Service and implementation file for every Entity published by Model Interface.
- **Never** — Copy or redefine the Model Entity in its child Service.

### Database

**Every Entity Action preserves the selected Database Instance**

- **Must** — Accept an optional Database Instance and pass it unchanged with every applicable Database Service call.
- **Never** — Call Database Interface directly or select or interpret an engine, connection, table, or default Instance.

### Sensitive Values

**Entity Service owns application-sensitive treatment**

- **Must** — Apply application-required sensitive-value treatment around Database calls.
- **Never** — Expose an original sensitive value or transfer sensitivity interpretation to Database.
