# Model Definition

Model defines and handles the project's data-model Entities.

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

Model defines flat, technology-independent Domain Entities. Each Entity carries its own meaning, Fields, and explicit Relationships without nesting another Entity.

### Purpose

Model gives Logic and Database one shared Entity representation of each domain concept. Logic imports Entity classes for application programming; Database independently imports those same classes to derive its storage structure.

### How It Works

Each Entity stands alone in its own unit under the Entity directory. Declaration records technology-independent meaning, while Foundation provides shared behaviour. Every Model layer is public; Interface provides a convenient entry point for Entity classes and capabilities.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Domain Entity** — the authoritative logical definition of one meaningful concept in the Target's domain.
- **Entity Layer** — the public Model layer that contains each Entity in a separate unit.
- **Entity** — a Domain Entity with an Identity that distinguishes one instance from another.
- **Field** — one named value of a Domain Entity, with its domain meaning, logical type, and applicable constraints.
- **Type** — the technology-independent category of values a Field may hold.
- **Field Rule** — a declared rule for a Field's presence, default, sensitivity marker, immutability, length, or constraint.
- **Sensitivity Marker** — optional Field metadata that identifies a value category requiring Logic attention, such as `password` or `sensitive`. Model records the marker but does not inspect, transform, or otherwise handle the value.
- **Relationship** — an explicit domain reference from one Domain Entity to another, without nesting either Entity inside the other.
- **Identity** — the Field or Fields that distinguish one Entity from every other Entity of the same kind.
- **Primary Key** — the storage-facing expression of an Entity's declared Identity.
- **Uniqueness Constraint** — a condition requiring one Field or a declared combination of Fields to have no duplicate value within its Entity.
- **Reference** — the Field-level expression of a Relationship that identifies a value belonging to another Entity.
- **Index** — a declared access intention for one Field or a declared combination of Fields.
- **Value Generation** — a declared way to supply a Field value automatically, including Auto Increment, generated identifier, or generated timestamp.
- **Declaration** — the public class that records an Entity's technology-independent data meaning and metadata without providing runtime behaviour.
- **Foundation** — the public class that provides shared `to_json()` and `from_json()` behaviour without defining domain meaning.
- **Interface** — a public Model file that presents the Entity classes and capabilities that consuming Components may import and use.

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

- **Database** — independently imports public Entity classes and uses their declared metadata to create its storage structure. It does not define a second persistence model.
- **Logic** — imports public Entity classes through Interface and uses them directly in application programming.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

A public file that presents the Entity classes and capabilities available to other Components.

### Entity

A public directory containing one separate unit for each Entity.

### Declaration

A public file that records Entity meaning and metadata without runtime behaviour:

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
├── Primary Keys
├── Relationships
├── Unique Constraints
├── Indexes
└── Value Generation
    ├── Auto Increment
    ├── Generated Identifier
    └── Generated Timestamp
```

### Foundation

A public file that provides shared conversion behaviour:

```text
Foundation
├── to_json()
└── from_json()
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

**Rule:** Documentation has an Overview with one concise example using one Entity. Its Interface section lists every public Entity separately and shows that Entity's Fields in a table without usage examples. Its Foundation section gives an example for each Foundation capability, then one complete example that uses all Foundation capabilities with one Entity. Documentation describes each Entity's kind, import, direct construction, and JSON conversion.

**Why:** Consumers can understand and use a Model without depending on internal implementation details.

**Boundary:** Documentation does not make Model responsible for persistence, workflow, or application behaviour.

<br>

### Each domain concept has one authoritative Domain Entity

**Rule:** Every meaningful Target concept has exactly one authoritative Domain Entity in Model, originating in domain meaning rather than a tool or consumer and never independently redefined elsewhere.

**Why:** One authority prevents competing Domain Entities from drifting apart.

**Boundary:** Implementation-only structures without domain meaning do not require a Domain Entity.

<br>

### Model preserves explicit Target meaning

**Rule:** Model preserves every Target-declared Domain Entity, Field, constraint, default, and sensitivity marker. Preferences may complete only missing choices of existing Fields; they never create, rename, remove, or override explicit Target meaning.

**Why:** The Target remains authoritative while unstated realization details can still be resolved consistently.

**Boundary:** Model does not own project records, Initial Data, storage treatment, or protection mechanisms.

<br>

### Logical Model meaning is independent of implementation technology

**Rule:** Every Domain Entity, Field, and declared rule remains understandable independently of language, package, tool, version, runtime, and platform.

**Why:** Technology can change without redefining the Target's domain.

**Boundary:** Model Preferences select compatible technical realization details without changing logical meaning.

<br>

### Foundation provides shared Model behaviour

**Rule:** Foundation converts an Instance to JSON through `to_json()` or creates an Instance from JSON through `from_json()`, without injecting Fields, constraints, or domain meaning.

**Why:** The library has one consistent implementation of its common behaviour without imposing a shared domain structure.

**Boundary:** Foundation supplies behaviour only. Declaration remains the owner of every Entity's meaning and metadata.

<br>

### Declaration records complete Entity meaning

**Rule:** Every Entity has a Declaration that records and exposes its Fields and applicable Types, Field Rules, Primary Keys, Uniqueness Constraints, Relationships, Index intentions, and Value Generation. A Reference identifies its target Entity and the identity it refers to; a Uniqueness Constraint or Index may cover one Field or a declared combination of Fields. Declaration provides no runtime behaviour.

**Why:** Logic and Database can consume one complete data meaning without coupling that meaning to a language, package, database, or Engine.

**Boundary:** Declaration does not choose a technical type, table name, query syntax, index implementation, or database-specific value-generation behaviour.

<br>

### Model publishes all layers

**Rule:** Interface, Entity, Declaration, and Foundation are public Model layers. Interface presents Entity classes and capabilities as a convenient entry point; consumers may use any public Model layer without treating another layer as private.

**Why:** Every Model concern remains directly available while Interface still provides one convenient entry point for common use.

**Boundary:** Public access does not transfer ownership of Entity meaning to a consumer or authorize a consumer to duplicate Foundation behaviour.

<br>

### Declaration preserves structured Field meaning

**Rule:** Declaration preserves each Field's logical Type, presence semantics, default, optional sensitivity marker, immutability, and every Target-declared restriction as usable structured meaning, including applicable value range, length, pattern, precision, scale, allowed values, or comparable constraint.

**Why:** Consumers and storage realization need more than descriptive prose to use the same domain restriction consistently.

**Boundary:** Declaration does not impose a fixed vocabulary or representation for a constraint that the Target does not declare.

<br>

### One Entity definition serves programming and persistence

**Rule:** Each Entity is the single class used by Logic in application programming and by Database for storage derivation. Database independently imports the public Entity classes and derives persistence metadata from them; it does not create or require a second persistence model.

**Why:** One Entity definition prevents application and persistence structures from drifting apart while allowing Database to build storage independently.

**Boundary:** Model declares the Entity. Database remains responsible for storage realization and operations.

<br>

### Model names express domain meaning

**Rule:** Every Model name expresses Target meaning, never an implementation tool or consumer-specific representation.

**Why:** Domain-oriented names keep the library understandable without technical context.

**Boundary:** Preferences define realization naming and layout; this Principle defines only domain meaning.

<br>

### Model remains separate from external concerns

**Rule:** Model owns logical Entities only; project records, storage operations, transport, workflow orchestration, technical selection, and platform operation belong to their respective Components.

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

**Each domain concept has one authoritative Domain Entity**

- **Must** — Define each meaningful Target concept once.
- **Never** — Create competing or implementation-only Domain Entities.

**Model preserves explicit Target meaning**

- **Must** — Preserve explicit Target Fields, constraints, defaults, and sensitivity markers.
- **Never** — Invent or override Target meaning.

**Logical Model meaning is independent of implementation technology**

- **Must** — Keep Entity meaning understandable without a language, package, database, Engine, runtime, or platform.
- **Never** — Let a technical realization redefine logical meaning.

**Foundation provides shared Model behaviour**

- **Must** — Use Foundation for `to_json()` and `from_json()` conversion.
- **Never** — Let Foundation define domain meaning or Fields.

**Declaration records complete Entity meaning**

- **Must** — record and expose every Entity's Fields, Types, Field Rules, Primary Keys, Uniqueness Constraints, Relationships, Index intentions, and Value Generation in Declaration.
- **Must** — identify every Reference target and allow declared composite Uniqueness Constraints and Indexes.
- **Never** — put runtime behaviour or technology-specific storage choices in Declaration.

**Model publishes all layers**

- **Must** — Keep Interface, Entity, Declaration, and Foundation public; present Entity classes and capabilities through Interface as a convenient entry point.
- **Never** — Let public access duplicate Foundation behaviour or transfer Entity ownership to a consumer.

**Declaration preserves structured Field meaning**

- **Must** — Keep each declared Field Type, rule, default, sensitivity marker, immutability, and restriction usable by consumers and storage realization.
- **Never** — Invent a constraint or force one constraint representation.

**One Entity definition serves programming and persistence**

- **Must** — Make each Entity available for Logic programming and Database storage derivation.
- **Must** — Let Database independently import the public Entity classes and derive persistence metadata from them.
- **Never** — Create or require a second persistence model.

**Model names express domain meaning**

- **Must** — Name every Model from Target domain meaning.
- **Never** — Name a Model after an implementation tool or consumer representation.

**Model remains separate from external concerns**

- **Must** — Keep Model focused on logical Entities.
- **Never** — Own records, storage operations, transport, workflow orchestration, technical selection, or platform operation.

**Entities are flat and explicitly related**

- **Must** — Keep every Entity flat and record every Target-declared cross-Entity connection explicitly.
- **Never** — Nest, inherit, or copy one Entity into another.

**Each Entity stands in its own unit**

- **Must** — Keep each Entity in its own public unit under the Entity layer.
- **Never** — Put Entity-specific content in Declaration or Foundation.
