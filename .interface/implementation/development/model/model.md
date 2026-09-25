# Model Definition

Model defines and handles the project's data-model Definitions.

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

Model defines flat, technology-independent Domain Definitions. Definitions are grouped as Entities, Value Objects, and Enumerations; each carries its own meaning, Fields, and explicit Relationships without nesting another Definition.

### Purpose

Model gives Database and Logic one shared, technology-independent definition of each domain concept.

### How It Works

Each Definition stands alone in the private Definitions layer. Declaration records technology-independent meaning, while Foundation provides shared behaviour. Interface is Model's only public layer and presents the capabilities that other Components may use. Logic uses those capabilities in programming; Database uses them to create its Tables.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Domain Definition** — the authoritative logical definition of one meaningful concept in the Target's domain.
- **Definitions** — the Model layer that contains every Entity, Value Object, and Enumeration in a separate unit.
- **Entity** — a Domain Definition with an Identity that distinguishes one instance from another.
- **Value Object** — a Domain Definition identified by its declared value rather than an independent Identity.
- **Enumeration** — a Domain Definition whose complete allowed values are declared explicitly.
- **Field** — one named value of a Domain Definition, with its domain meaning, logical type, and applicable constraints.
- **Type** — the technology-independent category of values a Field may hold.
- **Field Rule** — a declared rule for a Field's presence, default, sensitivity, immutability, length, or constraint.
- **Relationship** — an explicit domain reference from one Domain Definition to another, without nesting either Definition inside the other.
- **Identity** — the Field or Fields that distinguish one Entity from every other Entity of the same Definition.
- **Primary Key** — the storage-facing expression of an Entity's declared Identity.
- **Uniqueness Constraint** — a condition requiring one Field or a declared combination of Fields to have no duplicate value within its Definition.
- **Reference** — the Field-level expression of a Relationship that identifies a value belonging to another Definition.
- **Index** — a declared access intention for one Field or a declared combination of Fields.
- **Value Generation** — a declared way to supply a Field value automatically, including Auto Increment, generated identifier, or generated timestamp.
- **Declaration** — the private class that records a Definition's technology-independent data meaning and metadata without providing runtime behaviour.
- **Foundation** — the private class that provides shared validation, `to_json()`, and `from_json()` behaviour without defining domain meaning.
- **Intrinsic Rule** — a rule evaluated only from the data of the Domain Definition it governs.
- **Interface** — Model's only public layer. It presents the Definitions and capabilities that consuming Components may import and use without accessing any internal Model class or layer.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
├── Interface
├── Definitions
├── Declaration
└── Foundation
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Database** — uses the Definitions and Declaration meaning published through Interface to create Tables and their applicable keys, relationships, constraints, defaults, and indexes.
- **Logic** — imports and uses Model capabilities published through Interface in application programming.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The only public layer. It presents the Definitions and capabilities available to other Components.

### Definitions

A private layer containing separate units:

```text
Definitions
├── Entities
├── Value Objects
└── Enumerations
```

### Declaration

A private layer that records Definition meaning and metadata without runtime behaviour:

```text
Declaration
├── Types
├── Field Rules
│   ├── Required and Nullability
│   ├── Default Values
│   ├── Sensitivity
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

A private layer that provides shared validation and conversion behaviour:

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

**Rule:** Documentation gives every Domain Definition and Field a description. It documents each Model's kind, import, direct construction, JSON conversion, and any necessary usage example.

**Why:** Consumers can understand and use a Model without depending on internal implementation details.

**Boundary:** Documentation does not make Model responsible for persistence, workflow, or application behaviour.

<br>

### Each domain concept has one authoritative Domain Definition

**Rule:** Every meaningful Target concept has exactly one authoritative Domain Definition in Model, originating in domain meaning rather than a tool or consumer and never independently redefined elsewhere.

**Why:** One authority prevents competing domain definitions from drifting apart.

**Boundary:** Implementation-only structures without domain meaning do not require a Domain Definition.

<br>

### Model preserves explicit Target meaning

**Rule:** Model preserves every Target-declared Domain Definition, Field, constraint, default, and sensitivity classification. Preferences may complete only missing choices of existing Fields; they never create, rename, remove, or override explicit Target meaning.

**Why:** The Target remains authoritative while unstated realization details can still be resolved consistently.

**Boundary:** Model does not own project records, Initial Data, storage treatment, or protection mechanisms.

<br>

### Logical Model meaning is independent of implementation technology

**Rule:** Every Domain Definition, Field, and Intrinsic Rule remains understandable independently of language, package, tool, version, runtime, and platform.

**Why:** Technology can change without redefining the Target's domain.

**Boundary:** Model Preferences select compatible technical realization details without changing logical meaning.

<br>

### Foundation provides shared Model behaviour

**Rule:** Every Definition uses Foundation to verify its own data against Declaration during direct construction, `from_json()`, and `to_json()`. Foundation also converts an Instance to JSON through `to_json()` or creates an Instance from JSON through `from_json()`, without injecting Fields, constraints, or domain meaning.

**Why:** The library has one consistent implementation of its common behaviour without imposing a shared domain structure.

**Boundary:** Foundation supplies behaviour only. Declaration remains the owner of every Definition's meaning and metadata.

<br>

### Declaration records technology-independent data meaning

**Rule:** Every Definition has a Declaration that records its Fields and applicable Types, Field Rules, Primary Keys, Uniqueness Constraints, Relationships, Index intentions, and Value Generation. Declaration provides no runtime behaviour.

**Why:** Logic and Database can consume one complete data meaning without coupling that meaning to a language, package, database, or Engine.

**Boundary:** Declaration does not choose Python types, table names, SQL syntax, index implementation, or database-specific auto-increment behaviour.

<br>

### Model exposes one Interface

**Rule:** Interface is Model's only public layer. Database and Logic import and use Model only through Interface. Definitions, Declaration, Foundation, and every class within them are private implementation details; Interface alone presents the Definitions and capabilities intended for consumers. Database uses the Definitions and Declaration meaning presented through Interface to create Tables and their applicable keys, relationships, constraints, defaults, and indexes.

**Why:** One surface gives each consumer the information it needs while Model implementations remain free to change internally.

**Boundary:** Consumers do not import or depend on private Model resources, and do not reimplement Foundation behaviour.

<br>

### Model validates intrinsic data meaning

**Rule:** Each Definition validates its own Field constraints and Intrinsic Rules against its Declaration during direct construction, conversion from JSON, and conversion to JSON. Construction applies declared defaults when an input omits a Field, distinguishes an omitted value from an explicit null, ignores unknown input Fields, and validates the resulting Instance.

**Why:** Each instance entering or leaving a consuming Component has data that conforms to its Model Definition.

**Boundary:** Cross-Model, stored-data, workflow, authorization, and external-context rules remain outside Model.

<br>

### Declaration makes data structure available

**Rule:** Declaration preserves and exposes every Target-declared Identity, Uniqueness Constraint, Relationship, Index intention, and Value Generation. A Reference identifies its target Definition and the identity it refers to; a Uniqueness Constraint or Index may cover one Field or a declared combination of Fields.

**Why:** Database can derive primary keys, unique constraints, and foreign keys from domain meaning without inventing relationships or persistence rules.

**Boundary:** Declaration describes domain facts. Database decides the table, column, index implementation, foreign-key syntax, and physical enforcement used to realize them.

<br>

### Declaration preserves structured Field meaning

**Rule:** Declaration preserves each Field's logical Type, presence semantics, default, sensitivity, immutability, and every Target-declared restriction as usable structured meaning, including applicable value range, length, pattern, precision, scale, allowed values, or comparable constraint.

**Why:** Validation and storage realization need more than descriptive prose to apply the same domain restriction consistently.

**Boundary:** Declaration does not impose a fixed vocabulary or representation for a constraint that the Target does not declare.

<br>

### Foundation handles sensitive and immutable Fields safely

**Rule:** Foundation applies the sensitivity and immutability that Declaration records: a sensitive supplied value does not appear in validation diagnostics, and a declared immutable Field cannot change after construction.

**Why:** Sensitive data stays protected during normal model handling, while immutable domain facts remain stable.

**Boundary:** Foundation does not own secrets management, encryption, authorization, audit history, or storage-level protection.

<br>

### Model names express domain meaning

**Rule:** Every Model name expresses Target meaning, never an implementation tool or consumer-specific representation.

**Why:** Domain-oriented names keep the library understandable without technical context.

**Boundary:** Preferences define realization naming and layout; this Principle defines only domain meaning.

<br>

### Model remains separate from external concerns

**Rule:** Model owns logical Definitions only; project records, storage operations, transport, workflow orchestration, technical selection, and platform operation belong to their respective Components.

**Why:** A narrow boundary keeps Model reusable and protects domain meaning.

**Boundary:** Other Components may use Model data without transferring ownership of their concerns to Model.

<br>

### Definitions expose complete logical meaning

**Rule:** Every Definition preserves its Target-derived meaning through Declaration, including its Fields, Types, Field Rules, Primary Key, Uniqueness Constraints, Relationships, Index intentions, and Value Generation when applicable, in a form that Database and Logic can use through Interface.

**Why:** Consumers receive complete domain information without prescribing one storage format or implementation structure.

**Boundary:** Model does not prescribe how a realization stores that information, and Database alone decides how to realize it as storage.

<br>

### Definitions are flat and explicitly related

**Rule:** Every Domain Definition remains flat and independently understandable. When Target meaning connects two Definitions, Model records that connection as an explicit Relationship or Reference rather than nesting one Definition inside another.

**Why:** Flat Definitions prevent hidden structural coupling while explicit Relationships preserve the Target's domain connections.

**Boundary:** A Relationship does not create nesting, inheritance, copied Fields, or shared ownership between Definitions. Entities, Value Objects, and Enumerations remain separate Definition kinds.

<br>

### Each Domain Definition stands in its own unit

**Rule:** Every Domain Definition has one private unit of its own in the applicable Entities, Value Objects, or Enumerations branch of the Definitions layer. Content used by exactly one Definition remains with it; shared metadata belongs to Declaration and shared behaviour belongs to Foundation.

**Why:** One Definition per unit keeps domain boundaries visible and independently changeable.

**Boundary:** Preferences define the technical layout; this Principle defines ownership only.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Model documentation explains its domain surface**

- **Must** — Describe every Domain Definition and Field; document import, construction, and JSON conversion.
- **Never** — Describe Model as storage, workflow, or application behaviour.

**Each domain concept has one authoritative Domain Definition**

- **Must** — Define each meaningful Target concept once.
- **Never** — Create competing or implementation-only domain definitions.

**Model preserves explicit Target meaning**

- **Must** — Preserve explicit Target Fields, constraints, defaults, and sensitivity classification.
- **Never** — Invent or override Target meaning.

**Logical Model meaning is independent of implementation technology**

- **Must** — Keep Definition meaning understandable without a language, package, database, Engine, runtime, or platform.
- **Never** — Let a technical realization redefine logical meaning.

**Foundation provides shared Model behaviour**

- **Must** — Use Foundation to verify Definition data during construction, `to_json()`, and `from_json()`.
- **Never** — Let Foundation define domain meaning or Fields.

**Declaration records technology-independent data meaning**

- **Must** — Keep Definition meaning and metadata in Declaration.
- **Never** — Put runtime behaviour or technology-specific storage choices in Declaration.

**Model exposes one Interface**

- **Must** — Use Interface as Model's only public layer and present consumer-facing Definitions and capabilities there.
- **Never** — Let a consumer import a private Model resource or duplicate Foundation behaviour.

**Model validates intrinsic data meaning**

- **Must** — Let each Definition validate its own data during construction and both JSON conversion directions; apply declared defaults and ignore unknown input Fields.
- **Never** — Treat an omitted value as an explicit null or own stored-data, workflow, or external-context rules.

**Declaration makes data structure available**

- **Must** — Expose every declared Identity, Uniqueness Constraint, Relationship, Index intention, and Value Generation for Database consumption.
- **Never** — Choose physical storage details.

**Declaration preserves structured Field meaning**

- **Must** — Keep each declared Field Type, rule, default, sensitivity, immutability, and restriction usable for validation and storage realization.
- **Never** — Invent a constraint or force one constraint representation.

**Foundation handles sensitive and immutable Fields safely**

- **Must** — Apply declared sensitivity and immutability; keep sensitive input out of validation diagnostics.
- **Never** — Own encryption, secret management, authorization, or audit history.

**Model names express domain meaning**

- **Must** — Name every Model from Target domain meaning.
- **Never** — Name a Model after an implementation tool or consumer representation.

**Model remains separate from external concerns**

- **Must** — Keep Model focused on logical Definitions.
- **Never** — Own records, storage operations, transport, workflow orchestration, technical selection, or platform operation.

**Definitions expose complete logical meaning**

- **Must** — Expose each Definition's applicable Fields, Types, Field Rules, Primary Key, Uniqueness Constraints, Relationships, Index intentions, and Value Generation.
- **Never** — Prescribe one declaration format or storage realization.

**Definitions are flat and explicitly related**

- **Must** — Keep every Definition flat and record every Target-declared cross-Definition connection explicitly.
- **Never** — Nest, inherit, or copy one Definition into another.

**Each Domain Definition stands in its own unit**

- **Must** — Keep each Definition in its own private unit under the applicable Definitions branch.
- **Never** — Put Definition-specific content in Declaration or Foundation.
