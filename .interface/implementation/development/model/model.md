# Model Definition

Model is the Development Component that owns the logical domain definitions and publishes them through one technology-independent Public Interface.

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

Model defines the Target's authoritative domain meaning through reusable Domain Definitions. It owns identity, Fields, relationships, defaults, constraints, and behavior determinable from each definition's own data, organizes each definition in the configured Entity directory, and publishes them through one Public Interface.

### Purpose

Model prevents external concerns from forming competing definitions by making domain meaning one shared, technology-independent vocabulary.

### How It Works

A Domain Definition authoritatively carries one Target concept's Fields, relationships, and Intrinsic Rules in the shared vocabulary. Consumers reach the definition and declaration through the Public Interface; Database and Logic read them without redefining them.

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Domain Definition** — the authoritative logical definition of one meaningful concept in the Target's domain.
- **Entity Directory** — the configurable Model directory that contains one separate module for each Domain Definition.
- **Field** — one named property of a Domain Definition, with its domain meaning and applicable constraints.
- **Model Foundation** — the technology-independent common foundation through which concrete Model realizations receive shared mechanisms without inheriting domain Fields or relationships.
- **Intrinsic Rule** — a domain rule that can be evaluated entirely from the data of the Domain Definition it governs.
- **Domain Relationship** — a logical association between Domain Definitions whose meaning and constraints come from the Target.
- **Declaration Vocabulary** — the one standard, technology-independent vocabulary in which every Domain Definition states its Fields, properties, relationships, and constraints.
- **Plain Representation** — a Domain Definition's data expressed as simple named values, carrying no behavior and no technology of its own.
- **Serialization** — the pair of symmetric conversions between a Domain Definition and its Plain Representation.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
├── Entity Directory           ← one separate module per Domain Definition
│   └── Domain Definition      ← one authoritative definition per domain concept
├── Declaration Vocabulary     ← the one language every definition is stated in
├── Model Foundation           ← the mechanisms every definition shares
└── Public Interface           ← the only surface a consumer reaches
```

**Entity Directory** contains one separate module for each **Domain Definition**, which holds one Target concept, its Fields, relationships, and Intrinsic Rules.

**Declaration Vocabulary** defines the shared technology-independent vocabulary.

**Model Foundation** supplies shared mechanisms without owning domain meaning.

**Public Interface** exposes definitions and declarations to consumers.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development** — takes from it what Model does not choose for itself: its identity and technology.
- **Consumed by Database** — provides the Declaration Vocabulary from which Database derives and enforces physical storage structure.
- **Consumed by Logic** — provides the Domain Definitions Logic reasons about and passes between its Services.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Model owns logical domain meaning, intrinsic behavior, declarations, and serialization. Development supplies the Component's shared technical selections; Database and Logic consume Model through its Public Interface without moving their concerns into Model.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Model Definition Principles are mandatory. Model Preferences provide configurable defaults and conventions for unstated Model choices, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Model documentation explains its published domain surface

**Rule:** Model documentation explains every published Domain Definition, its meaning, Fields, properties, persistence status, import and construction, conversion to and from Plain Representation, and runnable examples. It also states that Model stores nothing, performs no application behavior, and offers no stored-data operations.

**Why:** Consumers need a complete description of the domain surface without mistaking Model for persistence or application Behaviour.

**Boundary:** This Principle governs consumer-facing Model documentation; it does not add storage, workflow, or application responsibilities to Model.

<br>

### Each domain concept has one authoritative Domain Definition

**Rule:** Every meaningful Target concept has exactly one authoritative Domain Definition in Model, originating in domain meaning rather than a tool or consumer and never independently redefined elsewhere.

**Why:** One authority prevents competing domain definitions from drifting apart.

**Boundary:** Implementation-only structures without domain meaning do not require a Domain Definition.

<br>

### Model preserves explicit Target meaning

**Rule:** Model preserves every Target-declared Domain Definition, Field, property, relationship, constraint, sensitive or credential meaning, and Intrinsic Rule. Preferences may complete only missing properties of existing Fields; they never create, rename, remove, override explicit values such as `false` or `null`, or invent relationships or behavior. Model resolves unstated realization details through Model Preferences under its applicable Principles and preserves credential classification and at-rest treatment without inferring either from a Field name.

**Why:** The Target remains authoritative while unstated realization details can still be resolved without changing domain meaning.

**Boundary:** Model does not own project records or Initial Data.

<br>

### Logical Model meaning is independent of implementation technology

**Rule:** Every Domain Definition and Intrinsic Rule remains understandable independently of language, package, tool, version, runtime, and platform; selected technology may realize it only while preserving its meaning.

**Why:** Technology can change without redefining the Target's domain.

**Boundary:** Development selects the compatible technical and Platform references used to realize Model.

<br>

### Concrete Model realizations share one Model Foundation

**Rule:** Every concrete realization receives shared validation, serialization, and metadata mechanisms through one Model Foundation, which never owns, injects, or requires Fields or relationships; each Domain Definition declares its complete Target-derived set.

**Why:** One foundation keeps shared mechanisms consistent without imposing domain meaning.

**Boundary:** The selected technology determines the Foundation's realization, which never supplies shared domain Fields.

<br>

### Model exposes an explicit and stable Public Interface

**Rule:** Model exposes all authoritative Domain Definitions through one explicit, stable Public Interface; consumers use no private resources, and each definition has one unambiguous public identity.

**Why:** A stable boundary preserves reuse while allowing internal change.

**Boundary:** The Public Interface remains explicit and stable; its concrete realization follows the applicable Development and Model Preferences.

<br>

### Intrinsic validation and domain behavior are deterministic and side-effect free

**Rule:** Model validates only Intrinsic Rules, and all validation, derived values, serialization, and domain behavior depend only on Model data, are deterministic, perform no external I/O, and create no unrelated side effect.

**Why:** Deterministic local behavior keeps Model predictable and reusable.

**Boundary:** External or operation-specific rules and application workflows remain outside Model.

<br>

### Model names express domain meaning

**Rule:** Every public Model name expresses Target meaning, never an implementation tool or consumer-specific representation.

**Why:** Domain-oriented names keep the model understandable without technical context.

**Boundary:** Model Preferences define realization naming and layout; this Principle defines only domain meaning.

<br>

### Model remains separate from external concerns

**Rule:** Model never owns Initial Data, persistence, transport, workflow orchestration, technical selection, platform operation, or other external concerns.

**Why:** A narrow boundary keeps Model reusable and protects domain meaning.

**Boundary:** Other Components may use Model data without transferring ownership of their concerns to Model.

<br>

### Model declares every definition in one standard, technology-independent vocabulary

**Rule:** Model expresses every Domain Definition in one technology-independent vocabulary: logical type, declared length and precision, nullability, default, identity, generated identity, uniqueness, and single-field or composite constraints. The Model Declaration Schema fixes the vocabulary's meanings. The same Domain Definition carries the vocabulary used by application code; Database and Logic read it through the Public Interface, and each realization maps it to its technology. Model preserves required, nullable, defaulted, generated, and absence semantics, invents none, and defines no partial-update behavior.

**Why:** One technology-independent vocabulary preserves shared meaning and Target-declared presence semantics.

**Boundary:** Database owns physical storage and multi-record enforcement; Model only declares logical meaning and nullability.

<br>

### A Domain Relationship carries the definition it refers to

**Rule:** Every Domain Relationship carries the referenced Domain Definition itself and declares its cardinality and optionality from the Target. It is resolved when declared, never through a later name lookup; technology independence does not justify an untyped reference, and the realization carries the definition where it can.

**Why:** Carrying the definition makes relationships verifiable where they are declared.

**Boundary:** Database decides how relationships are stored, constrained, and indexed.

<br>

### Every Domain Definition converts to and from a Plain Representation

**Rule:** Every Domain Definition exposes `serialize` to produce its Plain Representation and `deserialize` to produce a validated instance from one. Model Foundation provides both once. Serialization returns named values rather than encoded text; the consumer chooses the wire format. Deserialization applies the same Intrinsic Rules, and both operations are deterministic, data-only, and free of external I/O.

Conceptual example:

```text
instance      -> serialize   -> { field: value, ... }
{ field: ... } -> deserialize -> instance
```

**Why:** Symmetric validated conversion prevents consumers from duplicating domain meaning.

**Boundary:** Serialization publishes the Model Fields and leaves relationship nesting and output filtering to consuming Components.

<br>

### Every Domain Definition declares whether it is persistent

**Rule:** Every Domain Definition declares itself `persistent` or `non-persistent`. The declaration is explicit: Model never leaves it to be read from a Domain Definition's existence, name, or the presence of an identity Field. What Database does with that declaration is Database's to enforce, under its own Principles.

**Why:** An explicit declaration prevents other Components from guessing what must be stored.

**Boundary:** Model declares persistence; Database decides its physical realization.

<br>

### Each Domain Definition stands in its own module

**Rule:** Every Domain Definition is declared in its own module with only what belongs to it. Those modules live in the configured Entity Directory, never gather several definitions, and are published by the Public Interface under an unambiguous identity independent of their modules.

**Why:** One definition per module keeps domain boundaries visible and independently changeable.

**Boundary:** Preferences name the Entity Directory and define module layout, while shared mechanisms remain in Model Foundation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Model documentation explains its published domain surface**

- **Must** — document every published Domain Definition, its properties, persistence status, representations, and runnable usage.
- **Never** — imply that Model stores data or owns application Behaviour or stored-data operations.

**Each domain concept has one authoritative Domain Definition**

- **Must** — Give every meaningful Target domain concept exactly one authoritative Domain Definition in Model.
- **Never** — Create a Domain Definition solely for an implementation need or independently redefine the same domain identity.

**Model preserves explicit Target meaning**

- **Must** — Preserve every explicit Target definition, property, relationship, constraint, sensitive meaning, and Intrinsic Rule.
- **Must** — Apply Model defaults only to missing properties of existing Fields, property by property.
- **Never** — Let a default add a Field, override an explicit value, change meaning, or invent a relationship or behavior.
- **Never** — Treat Initial Data or another project record as a Model-owned Domain Definition.
- **Must** — Take what the domain is — which Domain Definitions and Fields exist, their names, and their relationships — only from the Target.
- **Must** — Resolve an unstated technical modelling parameter of an existing Field through Model Preferences under the applicable Principles.
- **Never** — Let such a choice add, remove, or rename a Field or relationship, override an explicit Target value, or change what a Field means.
- **Must** — Preserve each Target-declared credential classification and its required at-rest treatment.
- **Never** — Infer a credential classification or its at-rest treatment from a Field's name.

**Logical Model meaning is independent of implementation technology**

- **Must** — Keep Domain Definitions and Intrinsic Rules understandable independently of implementation technology.
- **Must** — Require every selected technology to preserve logical Model meaning.
- **Must** — Take every technical and platform choice from Development; Model never selects one itself.

**Concrete Model realizations share one Model Foundation**

- **Must** — Give every concrete Model realization applicable shared mechanisms through one Model Foundation without imposing Fields or relationships.
- **Never** — Require one particular realization mechanism for Model Foundation.

**Model exposes an explicit and stable Public Interface**

- **Must** — Expose every authoritative Domain Definition with one unambiguous identity through Model's explicit, stable Public Interface.
- **Never** — Let consumers depend on Model's private internal resources.
- **Never** — Treat the conceptual example as fixed technical syntax or evolve the Public Interface outside Development's change-propagation rules.

**Intrinsic validation and domain behavior are deterministic and side-effect free**

- **Must** — Keep Intrinsic validation and domain behavior deterministic, dependent only on Model data, and free of external I/O and unrelated side effects.
- **Never** — Treat an externally contextual rule as intrinsic or let Model orchestrate a workflow.

**Model names express domain meaning**

- **Must** — Name Model concepts from Target domain meaning.
- **Never** — Name a Model concept after an implementation tool or consumer-specific representation unless that name is itself a Target concept.

**Model remains separate from external concerns**

- **Never** — Let Model own Initial Data, persistence, transport, workflow orchestration, technical selection, platform operation, or another concern outside its logical boundary.
- **Must** — Keep external realization outside Model ownership even when another Component consumes Model data or its Public Interface.

**Model declares every definition in one standard, technology-independent vocabulary**

- **Must** — Express every Domain Definition in one standard, technology-independent vocabulary: type, length and precision, nullability, default, identity, uniqueness, constraints, and relationships.
- **Must** — Resolve unstated technical modelling parameters through Model Preferences without changing Target meaning.
- **Must** — Carry that vocabulary in the same Domain Definition that application code uses, so every Component — Database among them — reads it through the Model Public Interface.
- **Never** — Maintain a separate schema artifact beside the Domain Definition as Database's source.
- **Must** — Preserve each Target Field's declared required, nullable, default, generated, and absence semantics.
- **Never** — Invent an absence state, default, generation mechanism, or partial-update semantics.
- **Never** — Put tables, indexes, migrations, SQL, ORM mappings, or Engine-specific constraints in Model.

**A Domain Relationship carries the definition it refers to**

- **Must** — Carry the referenced Domain Definition itself in a relationship, so an unresolvable reference fails where it is written.
- **Never** — Stand a name in for a referenced Domain Definition, or treat technology independence as a reason to leave a reference untyped.
- **Must** — State each relationship's cardinality and optionality from the Target rather than leaving either to a default.

**Every Domain Definition converts to and from a Plain Representation**

- **Must** — Offer `serialize` and `deserialize` on every Domain Definition, provided once through Model Foundation.
- **Must** — Return simple named values from `serialize`, leaving the wire format to the consumer.
- **Must** — Evaluate the Domain Definition's Intrinsic Rules during `deserialize` and fail when they are not satisfied.
- **Never** — Nest a related Domain Definition in a Plain Representation; a Domain Relationship appears only as its declared reference value.
- **Never** — Withhold a Field inside Serialization; output policy belongs to the consuming Component.

**Every Domain Definition declares whether it is persistent**

- **Must** — Declare every Domain Definition as `persistent` or `non-persistent`, explicitly.
- **Never** — Decide in Model how, where, or under what structure a persistent Domain Definition is stored.

**Each Domain Definition stands in its own module**

- **Must** — Declare every Domain Definition in a module of its own inside the configured Entity Directory, carrying that definition and what belongs to it alone.
- **Never** — Gather several Domain Definitions into one module.
- **Must** — Publish each Domain Definition through the Public Interface under its own identity, independent of the module it was declared in.
