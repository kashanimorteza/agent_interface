# Entity Service Definition

Entity Service is the fixed internal Logic Service whose public Interface provides one Entity-oriented Child Service for every Entity published by Model.

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

Entity Service is one of the two fixed internal Services of every Logic Component. It gives each Entity published by Model one Child Service through which consumers can add, update, retrieve, delete, list, aggregate, enable, disable, or truncate that Entity. The Child Service supplies its own Entity identity and uses the corresponding Actions published by Storage Service Interface. Entity Service remains internal, while Logic Interface publishes Entity Service Interface unchanged under its configured name.

### Purpose

Storage Service is Logic's public raw Database gateway. Entity Service adds an Entity-oriented surface over that gateway: selecting a Child Service selects the Entity, so a consumer does not repeatedly pass the Entity class for every request. A Child Service may also add Behaviour specific to its Entity. Entity Service is a convenience and extension surface, not the exclusive route to raw persistence; consumers may intentionally use Storage Service directly when they need its contract.

### How It Works

Entity Service reads the authoritative Entity classes published by Model Interface. It carries one private shared Base Entity capability implementing the Entity-facing Actions corresponding to Add, Update, List, Delete, Enable, Disable, Get by ID, Count, Sum, Min, Max, and Truncate. Execute Command, Create Tables, and Insert Initial Data remain Database-wide Storage Actions and are not Entity Actions.

Entity Service creates exactly one Child Service file and public structure for every Model Entity inside its configured Entities directory. Each Child Service receives the shared Base Entity capability and binds itself to its own authoritative Model Entity class. In a language that supports class inheritance, the preferred realization is a child class inheriting the configured Base Entity class. Another language uses its equivalent mechanism, such as composition, embedding, or traits, without changing the public Behaviour.

For Add and Update, a Child Service accepts only an instance of its bound Entity and rejects a mismatched Entity before reaching Storage. For List, Delete, Enable, Disable, Get by ID, Count, Sum, Min, Max, and Truncate, the Child Service supplies its bound Entity class to the corresponding Storage Action. Every Entity Action may also accept the exact Database Instance Enum member republished by Storage Service Interface and passes it unchanged. When omitted, Storage delegates default selection to Database.

Entity Service imports Model Interface and Storage Service Interface directly. It never imports Logic Interface. Entity Service Interface publishes every Child Service and its shared or Entity-specific Actions, never the private Base Entity capability.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity Role** — the fixed identity of this Service inside Logic, independent of its configurable public name.
- **Entity Service Interface** — this Service's outward gateway, published unchanged under the configured Service name by Logic Interface.
- **Base Entity** — the private shared capability that implements Entity Actions through corresponding Storage Service Actions; `BaseEntity` is its default Python class name.
- **Entity Child Service** — the public Service structure bound to one authoritative Entity published by Model and receiving the shared Base Entity capability.
- **Entity-bound Action** — Add, Update, List, Delete, Enable, Disable, Get by ID, Count, Sum, Min, Max, or Truncate as exposed for one bound Entity.
- **Database-wide Action** — Execute Command, Create Tables, or Insert Initial Data, which remains available from Storage Service and is not added to Base Entity.
- **Database Instance Enum** — the exact active-Instance enum republished by Storage Service Interface and optionally selected for one Entity Action.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Service
├── interface
├── base_entity
└── entity/
    └── <entity>
```

The names shown are defaults selected by Entity Service Preferences. Changing a name changes the realization path, not the responsibility represented by that member.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Belongs to Logic** — is a fixed Service whose Interface Logic Interface always publishes.
- **Consumes Model** — discovers and imports authoritative Entity classes only through Model Interface.
- **Consumes Storage Service** — performs persistence only through the Actions and exact Database Instance Enum published by Storage Service Interface.
- **Consumed by Logic consumers** — is reached through Entity Service Interface as published by Logic Interface.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Domain meaning and Entity declarations** — belong to Model; Entity Service imports and binds them without copying them.
- **Raw Database Actions and routing to Database Interface** — belong to Storage Service; Entity Service uses the Entity-bound subset without redefining it.
- **Execute Command, Create Tables, and Insert Initial Data** — remain Database-wide Storage Actions and are never Base Entity capabilities.
- **Tables, Engines, sessions, mappings, migrations, and storage guarantees** — belong to Database; neither Entity Service nor Storage Service reimplements them.
- **Logic's root publication of Services** — belongs to Logic Interface; Entity Service owns only its own Interface.
- **Transport and presentation** — belong to consuming Components; Entity Service returns transport-independent Action results.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The outward gateway of Entity Service. It publishes every Entity Child Service together with the Actions supplied by Base Entity and any Action owned by that child. A consumer first selects the Child Service and then calls one of its Actions. Interface does not flatten every Entity Action into one surface, publish Base Entity, import Logic Interface, or duplicate a Storage Action.

### Base Entity

The private shared capability held in the configured Base Entity file. It implements the Entity Actions corresponding to the Entity-bound Storage Actions. `BaseEntity` in `base_entity` is the default Python realization; another language uses its equivalent reuse mechanism. Base Entity contains no persistence implementation and is never a consumer dependency.

### Entities

One file and one public Child Service structure per Entity published by Model Interface. The default file pattern is `<entity>` and the default public structure pattern is `<entity><child_suffix>`, normalized according to the selected language. Every child binds its Model Entity class, receives all shared Entity Actions, and contains only Behaviour or Actions specific to that Entity.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Entity Service. Entity Service Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and applicable Logic, Model, Storage Service, and Database Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Entity Service is fixed and internal with a public Interface

**Rule:** Every Logic contains the fixed Entity Role as an internal Service and publishes Entity Service Interface unchanged through Logic Interface. Its configured public name may change, but its Role and responsibilities do not. Its implementation remains internal.
**Why:** Entity-oriented access has one stable and discoverable gateway without exposing shared or child implementation files.
**Boundary:** Entity Service is not the exclusive public persistence route. A consumer may intentionally use Storage Service Interface directly for raw Database capabilities.

<br>

### Interface

#### Entity Service Interface publishes Entity Child Services only

**Rule:** Entity Service Interface publishes one Entity Child Service for every Entity published by Model Interface. Each child exposes its shared and Entity-specific Actions. Interface publishes neither Base Entity nor a flat duplicate of Child Actions, Storage Actions, or Database Instance identities.
**Why:** Consumers select an Entity once and use its capabilities without depending on the mechanism shared among Entities.
**Boundary:** Logic Interface references and publishes Entity Service Interface unchanged. Consumers obtain the exact Database Instance Enum from Storage Service Interface when they want to select an Instance explicitly.

#### Entity Service never imports Logic Interface

**Rule:** Entity Service imports Model Interface and Storage Service Interface directly and never imports Logic Interface. Logic Interface imports Entity Service Interface only to publish it.
**Why:** One-way imports prevent a dependency cycle between Logic Interface and its internal Services.
**Boundary:** External consumers continue to enter through Logic Interface; the direct Storage Service Interface import is internal Service collaboration.

<br>

### Base Entity

#### Base Entity provides shared Entity Actions once

**Rule:** Base Entity implements the shared form of every Entity-bound Action once, and every Entity Child Service receives that capability. Class inheritance is preferred where the selected language supports it; another language must use an equivalent reuse mechanism without changing the public Behaviour.
**Why:** One shared capability prevents Entity Action Behaviour and use of Storage Service from drifting across Child Services while preserving language independence.
**Boundary:** Base Entity implements Entity-oriented coordination around a Storage Service call. It never implements persistence, exposes Database-wide Actions, or redefines a Storage Action.

<br>

### Entities

#### Every Model Entity receives one bound Child Service

**Rule:** Entity Service creates exactly one Child Service file and public structure for every Entity published by Model Interface. Each child binds the authoritative Model Entity class, receives Base Entity capabilities, and never copies or redefines the Entity.
**Why:** The Child Service set remains complete and synchronized with Model while each request carries an unambiguous Entity identity.
**Boundary:** An Entity-specific child may add Behaviour or Actions but cannot change the Entity declaration or detach itself from the shared Base Entity capability.

#### Each Child Service enforces its bound Entity

**Rule:** Add and Update accept only an instance of the Child Service's bound Entity and reject a mismatch before calling Storage Service. Every Entity-bound Action that requires an Entity class receives the bound Model Entity class from the Child Service rather than requiring the consumer to pass it again.
**Why:** Selecting a Child Service must reliably select the Entity on which the Action operates.
**Boundary:** This validates Entity identity only; it neither constrains Entity Field types nor duplicates Model's domain declarations.

#### Entity realization identifiers are valid and unique

**Rule:** The configured Base Entity file and structure names and every generated Child file and public structure name are valid for the selected language and unique after declared normalization. A Child file follows `<entity>` and its public structure follows `<entity><child_suffix>` using configured values and the selected language's conventions.
**Why:** Base Entity and every Model Entity need unambiguous realizations without overwriting, shadowing, or using a name rejected by the selected language.
**Boundary:** An invalid, reserved, or colliding value stops generation with a clear error. The generator never adds a number, suffix, or silent rename beyond the configured pattern.

<br>

### Storage

#### Storage Service is Entity Service's only persistence route

**Rule:** Every persistence request from Entity Service uses the corresponding Action published by Storage Service Interface. Entity Service never calls Database Interface, Logic Interface, or a Database implementation directly.
**Why:** One route preserves Storage Service as Logic's internal Database gateway and keeps Entity-oriented Behaviour independent of Database realization.
**Boundary:** Entity Service may add Entity-specific Behaviour around a Storage call, but does not transfer that Behaviour to Storage Service.

#### Every Entity Action preserves the selected Database Instance

**Rule:** Every Entity Action accepts an optional member of the exact Database Instance Enum republished by Storage Service Interface and passes it unchanged with every applicable Storage call. Omitting it delegates default selection through Storage Service to Database.
**Why:** A consumer can use the same Entity-oriented capability against any active Database Instance without bypassing Logic or creating an incompatible Instance identity.
**Boundary:** Entity Service creates no Instance enum and selects no Engine, connection, table, or default Instance.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Entity Service is fixed and internal with a public Interface**

- **Must** — Include the Entity Role internally in every Logic and publish its Interface unchanged under its configured name.
- **Never** — Expose its private implementation or claim exclusive ownership of raw persistence access.

### Interface

**Entity Service Interface publishes Entity Child Services only**

- **Must** — Publish one Child Service for every Entity Model Interface publishes.
- **Never** — Publish Base Entity, flatten Child Actions, or republish Storage Actions or Database Instance identities.

**Entity Service never imports Logic Interface**

- **Must** — Import Model Interface and Storage Service Interface directly.
- **Never** — Import Logic Interface from Entity Service.

### Base Entity

**Base Entity provides shared Entity Actions once**

- **Must** — Provide all Entity-bound Actions once and reuse them in every Child Service with the selected language's appropriate mechanism.
- **Never** — Implement persistence, expose Database-wide Actions, or require class inheritance from a language that does not support it.

### Entities

**Every Model Entity receives one bound Child Service**

- **Must** — Create exactly one bound Child file and public structure for every Entity published by Model Interface.
- **Never** — Copy or redefine the Model Entity or detach a child from Base Entity capability.

**Each Child Service enforces its bound Entity**

- **Must** — Validate Add and Update instances and supply the bound Entity class for every class-based Storage request.
- **Never** — Let a Child Service operate on a different Entity or require the consumer to repeat its selected Entity class.

**Entity realization identifiers are valid and unique**

- **Must** — Validate Base Entity names and derive valid, unique Child file and public structure names using the configured patterns and language normalization.
- **Never** — Resolve an invalid or colliding identity with an invented or silent rename.

### Storage

**Storage Service is Entity Service's only persistence route**

- **Must** — Use the corresponding Action from Storage Service Interface for every persistence request.
- **Never** — Call Logic Interface, Database Interface, or a Database implementation directly.

**Every Entity Action preserves the selected Database Instance**

- **Must** — Accept and pass the exact optional Database Instance Enum member unchanged.
- **Never** — Recreate an Instance identity or select an Engine, connection, table, or default Instance.
