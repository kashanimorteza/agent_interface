# Model Definition

Model defines and publishes the project's data-model Entities.

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

Model defines flat, technology-independent Entities. Each Entity carries its own meaning, Fields, and explicit Relationships without nesting another Entity.

### Purpose

Model provides standard, shared Entity definitions for use through its published surface.

### How It Works

Each Entity stands alone in its own unit. Declaration records technology-independent meaning, while Foundation provides shared behaviour. Every Model layer is public; Interface is the standard entry point for published Entities.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity** — the authoritative logical definition of one meaningful concept in the Target's domain, with an Identity that distinguishes one instance from another.
- **Field** — one named value of an Entity, with its domain meaning, logical type, and applicable constraints.
- **Type** — the technology-independent category of values a Field may hold.
- **Field Rule** — a declared rule for a Field's presence, default, sensitivity marker, immutability, length, or constraint.
- **Sensitivity Marker** — optional Field metadata whose value is either `password` or `sensitive`. It identifies a value category; Model records and publishes the marker but does not inspect, transform, or otherwise handle the value.
- **Relationship** — an explicit domain reference from one Entity to another, with declared cardinality and without nesting either Entity inside the other.
- **Identity** — the `id` Field that distinguishes one Entity from every other Entity of the same kind.
- **Primary Key** — the `id` Field used to identify an Entity.
- **Uniqueness Constraint** — a condition requiring one Field or a declared combination of Fields to have no duplicate value within its Entity.
- **Reference** — the Field-level expression of a Relationship that holds another Entity's `id`.
- **Index** — a declared access intention for one Field or a declared combination of Fields.
- **Default Value** — a fixed value applied when a Field is omitted.
- **Value Generation** — a declared way to supply a Field value automatically when an Entity is created, including Auto Increment or a generated identifier.
- **Declaration** — a public Model layer that records an Entity's technology-independent data meaning and metadata without defining Entity behaviour.
- **Foundation** — a public Model layer that defines shared capabilities, including conversion of an Entity to JSON and construction of an Entity from JSON, without defining domain meaning.
- **Interface** — the public Model surface that publishes Entities for standard use.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
├── Interface
├── Entity
├── Declaration
└── Foundation
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Logic** — uses Model Interface to obtain Entities for application programming.
- **Database** — uses Entities to create its storage structure, and uses Model Interface for other Model use.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The public Model surface that publishes Entities for standard use.

### Entity

A public layer containing one separate unit for each Entity.

### Declaration

A public layer that records Entity meaning and metadata without Entity behaviour:

```text
Declaration
├── Types
├── Field Rules
│   ├── Required and Nullability
│   ├── Default Values
│   ├── Sensitivity Marker
│   ├── Immutability
│   ├── Length
│   └── Constraints
├── Primary Key
├── Relationships
│   ├── References
│   └── Cardinality
├── Unique Constraints
├── Indexes
└── Value Generation
    ├── Auto Increment
    └── Generated Identifier
```

### Foundation

A public layer that defines shared conversion capabilities:

```text
Foundation
├── Entity-to-JSON conversion
└── JSON-to-Entity construction
```

Technical choices, names, and layout for these layers belong to Model Preferences. Declaration meaning remains independent of language, package, database, and Engine.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Model Definition Principles are mandatory. Model Preferences provide configurable defaults and conventions for unstated Model choices, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Model documentation explains its domain surface

**Rule:** Documentation has an Overview with one concise example using one Entity. Its Interface section lists every public Entity separately and shows that Entity's Fields in a table without usage examples. Its Foundation section gives an example for each Foundation capability, then one complete example that uses all Foundation capabilities with one Entity.

**Why:** Consumers can understand and use a Model without depending on internal implementation details.

**Boundary:** Documentation does not make Model responsible for persistence, workflow, or application behaviour.

<br>

### Each domain concept has one authoritative published Entity

**Rule:** Every meaningful Target concept has exactly one authoritative, published Entity in Model, originating in domain meaning rather than a tool or consumer and never independently redefined elsewhere.

**Why:** One authority prevents competing Entities from drifting apart.

**Boundary:** Implementation-only structures without domain meaning do not require an Entity.

<br>

### Model preserves explicit Target meaning

**Rule:** Model preserves every Target-declared Entity, Field, constraint, default, and sensitivity marker. Preferences may complete only missing choices of existing Fields; they never create, rename, remove, or override explicit Target meaning.

**Why:** The Target remains authoritative while unstated realization details can still be resolved consistently.

**Boundary:** Model does not own project records, Initial Data, storage treatment, or protection mechanisms.

<br>

### Logical Model meaning is independent of implementation technology

**Rule:** Every Entity, Field, and declared rule remains understandable independently of language, package, tool, version, runtime, and platform.

**Why:** Technology can change without redefining the Target's domain.

**Boundary:** Model Preferences select compatible technical realization details without changing logical meaning.

<br>

### Foundation provides shared Model behaviour

**Rule:** Foundation provides conversion of an Entity to JSON and construction of an Entity from JSON, without injecting Fields, constraints, or domain meaning.

**Why:** The library has one consistent implementation of its common behaviour without imposing a shared domain structure.

**Boundary:** Foundation supplies behaviour only. Declaration remains the owner of every Entity's meaning and metadata.

<br>

### Declaration records complete Entity meaning

**Rule:** Every Entity has a Declaration that records and exposes its `id` Identity and Primary Key, Fields and applicable Types, Field Rules, Uniqueness Constraints, Relationships and their cardinality, Index intentions, and Value Generation. A Reference identifies its target Entity and `id`; every Relationship uses Model Preferences' configured `on_delete` behaviour. A many-to-many Relationship requires an intermediary Entity declared by Target. A Uniqueness Constraint or Index may cover one Field or a declared combination of Fields. Declaration provides no runtime behaviour.

**Why:** One complete data meaning remains usable by consumers without coupling that meaning to a language, package, database, or Engine.

**Boundary:** Declaration does not choose a technical type, table name, query syntax, index implementation, or database-specific value-generation behaviour.

<br>

### Model publishes all layers

**Rule:** Interface, Entity, Declaration, and Foundation are public Model layers. Interface publishes Entities as the standard Model entry point. A Component may use another public layer when its responsibility requires it.

**Why:** Every Model concern remains available while Interface provides one consistent route for standard Entity use.

**Boundary:** Public access does not transfer ownership of Entity meaning to a consumer or authorize a consumer to duplicate Foundation behaviour.

<br>

### Declaration preserves structured Field meaning

**Rule:** Declaration preserves each Field's logical Type, presence semantics, Default Value, optional sensitivity marker (`password` or `sensitive`), immutability, and every Target-declared restriction as usable structured meaning, including applicable value range, length, pattern, precision, scale, allowed values, or comparable constraint. A Default Value is fixed; Value Generation creates a value when an Entity is created. One Field never declares both.

**Why:** Consumers and storage realization need more than descriptive prose to use the same domain restriction consistently.

**Boundary:** Declaration does not impose a fixed vocabulary or representation for a constraint that the Target does not declare.

<br>

### Entity names express domain meaning

**Rule:** Every Entity, Field, and Relationship name expresses Target meaning, never an implementation tool or consumer-specific representation.

**Why:** Domain-oriented names keep Entity meaning understandable without technical context.

**Boundary:** Preferences define names for realization and layout; this Principle defines only domain names.

<br>

### Model remains separate from external concerns

**Rule:** Model owns logical Entities only; project records, storage operations, transport, workflow orchestration, and platform operation belong to their respective Components.

**Why:** A narrow boundary keeps Model reusable and protects domain meaning.

**Boundary:** Other Components may use Model data without transferring ownership of their concerns to Model.

<br>

### Entities are flat and explicitly related

**Rule:** Every Entity remains flat and independently understandable. When Target meaning connects two Entities, Model records that connection as an explicit Relationship or Reference rather than nesting one Entity inside another.

**Why:** Flat Entities prevent hidden structural coupling while explicit Relationships preserve the Target's domain connections.

**Boundary:** A Relationship does not create nesting, inheritance, copied Fields, or shared ownership between Entities.

<br>

### Each Entity stands in its own unit

**Rule:** Every Entity has one public unit of its own in the Entity layer. Content used by exactly one Entity remains with it; shared metadata belongs to Declaration and shared behaviour belongs to Foundation.

**Why:** One Entity per unit keeps domain boundaries visible and independently changeable.

**Boundary:** Preferences define the technical layout; this Principle defines ownership only.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Model documentation explains its domain surface**

- **Must** — Give one Overview example; list every public Entity and its Fields in Interface tables without examples; give Foundation capability examples and one complete Foundation example using one Entity.
- **Never** — Describe Model as storage, workflow, or application behaviour.

**Each domain concept has one authoritative published Entity**

- **Must** — Define and publish each meaningful Target concept once.
- **Never** — Create competing or implementation-only Entities.

**Model preserves explicit Target meaning**

- **Must** — Preserve explicit Target Fields, constraints, defaults, and sensitivity markers.
- **Never** — Invent or override Target meaning.

**Logical Model meaning is independent of implementation technology**

- **Must** — Keep Entity meaning understandable without a language, package, database, Engine, runtime, or platform.
- **Never** — Let a technical realization redefine logical meaning.

**Foundation provides shared Model behaviour**

- **Must** — Use Foundation for Entity-to-JSON conversion and JSON-to-Entity construction.
- **Never** — Let Foundation define domain meaning or Fields.

**Declaration records complete Entity meaning**

- **Must** — record and expose every Entity's `id` Identity and Primary Key, Fields, Types, Field Rules, Uniqueness Constraints, Relationships and cardinality, Index intentions, and Value Generation in Declaration.
- **Must** — identify every Reference target and its `id`; use the configured `on_delete` behaviour for every Relationship; require a Target-declared intermediary Entity for many-to-many Relationships; allow declared composite Uniqueness Constraints and Indexes.
- **Never** — put runtime behaviour or technology-specific storage choices in Declaration.

**Model publishes all layers**

- **Must** — Keep Interface, Entity, Declaration, and Foundation public; publish Entities through Interface as the standard entry point.
- **Never** — Let public access duplicate Foundation behaviour or transfer Entity ownership to a consumer.

**Declaration preserves structured Field meaning**

- **Must** — Keep each declared Field Type, rule, Default Value, Value Generation, sensitivity marker (`password` or `sensitive`), immutability, and restriction usable by consumers and storage realization.
- **Must** — Keep Default Value and Value Generation mutually exclusive for one Field.
- **Never** — Invent a constraint or force one constraint representation.

**Entity names express domain meaning**

- **Must** — Name every Entity, Field, and Relationship from Target domain meaning.
- **Never** — Name an Entity, Field, or Relationship after an implementation tool or consumer representation.

**Model remains separate from external concerns**

- **Must** — Keep Model focused on logical Entities.
- **Never** — Own records, storage operations, transport, workflow orchestration, or platform operation.

**Entities are flat and explicitly related**

- **Must** — Keep every Entity flat and record every Target-declared cross-Entity connection explicitly.
- **Never** — Nest, inherit, or copy one Entity into another.

**Each Entity stands in its own unit**

- **Must** — Keep each Entity in its own public unit under the Entity layer.
- **Never** — Put Entity-specific content in Declaration or Foundation.
