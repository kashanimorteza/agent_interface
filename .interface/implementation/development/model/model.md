# Model Definition

Model defines the logical data concepts of the Target and publishes its explicitly public Definitions through one technology-independent Public Interface.

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

Model defines independent, flat Domain Definitions: their names, descriptions, Fields, logical types, constraints, defaults, and kinds. Storage and application behaviour belong to other Components.

### Purpose

Model gives every consumer one shared, technology-independent description of each domain concept without turning the description into a storage or workflow design.

### How It Works

Each Definition stands alone in the Definitions layer. A Definition that is explicitly public is published through the Public Interface and its Registry, where consumers can import it, construct an instance, convert an instance to JSON, or construct an instance from JSON.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Domain Definition** — the authoritative logical definition of one meaningful concept in the Target's domain.
- **Definitions** — the Model layer that contains one separate unit for each Domain Definition.
- **Field** — one named value of a Domain Definition, with its domain meaning, logical type, and applicable constraints.
- **Model Foundation** — the shared, technology-independent mechanisms used by concrete Model realizations without supplying domain structure.
- **Intrinsic Rule** — a rule evaluated only from the data of the Domain Definition it governs.
- **Declaration Vocabulary** — the technology-independent vocabulary in which each Domain Definition declares its meaning and Fields.
- **Public Interface** — the stable surface through which an explicitly public Domain Definition can be imported, constructed, and converted to or from JSON.
- **Public Registry** — the public index of explicitly public Domain Definitions, showing each Definition's public identity, kind, and description.
- **Supporting Content** — the shared Declaration Vocabulary, Model Foundation, and other common mechanisms supporting Definitions and the Public Interface.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
└── Layers
    ├── Public Interface       ← publishes explicitly public Definitions
    ├── Definitions            ← one independent unit per Domain Definition
    └── Supporting Content     ← shared mechanisms and vocabulary
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumed by Database** — provides the independent Domain Definitions that Database realizes as storage.
- **Consumed by Logic** — provides the Domain Definitions that Logic receives and returns through its Services.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

- **Public Interface** — publishes only explicitly public Definitions and their Registry.
- **Definitions** — contains each independent Domain Definition and its own content.
- **Supporting Content** — provides the shared Declaration Vocabulary, Model Foundation, and other common mechanisms.

Technical choices, defaults, and directory names for these layers belong to Model Preferences. The structure of a Model declaration belongs to the Model Declaration Schema.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Model Definition Principles are mandatory. Model Preferences provide configurable defaults and conventions for unstated Model choices, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Model documentation explains its public domain surface

**Rule:** Documentation gives every Domain Definition and Field a description. It documents each explicitly public Definition's public identity, kind, import, direct construction, JSON conversion, and any necessary usage example.

**Why:** Consumers can understand and use a public Definition without depending on internal implementation details.

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

### Concrete Model realizations share one Model Foundation

**Rule:** Concrete realizations use one shared Model Foundation for common construction, validation, conversion, and metadata mechanisms. The Foundation never injects domain Fields or domain meaning.

**Why:** Shared mechanisms remain consistent without imposing a shared domain structure.

**Boundary:** The selected technology realizes the Foundation; it does not redefine a Domain Definition.

<br>

### Model exposes an explicit and stable Public Interface

**Rule:** Only a Domain Definition explicitly marked public is published through the Public Interface and Public Registry. Every published Definition has one stable, domain-oriented public identity; the Registry shows that identity, its kind, and its description.

**Why:** Consumers can discover the supported surface without coupling to internal Definitions.

**Boundary:** Consumers do not depend on private resources, and internal Definitions are not published implicitly.

<br>

### Model validates intrinsic data meaning

**Rule:** Model validates only Intrinsic Rules: rules evaluable from the data of one Domain Definition. Construction applies declared defaults when an input omits a Field and validates the resulting instance.

**Why:** A Definition remains reliable without taking responsibility for application-wide behaviour.

**Boundary:** Cross-definition, stored-data, workflow, authorization, and external-context rules remain outside Model.

<br>

### Model names express domain meaning

**Rule:** Every public Model name expresses Target meaning, never an implementation tool or consumer-specific representation.

**Why:** Domain-oriented names keep the Model understandable without technical context.

**Boundary:** Preferences define realization naming and layout; this Principle defines only domain meaning.

<br>

### Model remains separate from external concerns

**Rule:** Model owns logical Definitions only; project records, storage operations, transport, workflow orchestration, technical selection, and platform operation belong to their respective Components.

**Why:** A narrow boundary keeps Model reusable and protects domain meaning.

**Boundary:** Other Components may use Model data without transferring ownership of their concerns to Model.

<br>

### Model declares every Definition in one standard vocabulary

**Rule:** Every Domain Definition declares its public identity, name, description, kind, public status, Fields, Intrinsic Rules, and enumeration literals when applicable. Every Field declares its name, description, logical type, presence semantics, default when one exists, and applicable constraints. Logical types use the standard technology-independent vocabulary fixed by the Model Declaration Schema.

**Why:** One vocabulary gives consumers a complete shared description without importing storage or technology decisions.

**Boundary:** The vocabulary remains limited to each independent Definition and its own Fields; operational and storage decisions remain outside Model.

<br>

### Definitions are flat and independent

**Rule:** Every Domain Definition is self-contained, flat, and independently understandable.

**Why:** Independent flat Definitions prevent hidden coupling and keep each concept understandable on its own.

**Boundary:** An Enumeration is itself an independent Domain Definition with its own public status and identity.

<br>

### Each Domain Definition stands in its own unit

**Rule:** Every Domain Definition has one unit of its own in the Definitions layer. Content used by exactly one Definition remains with it; shared content belongs to Supporting Content.

**Why:** One Definition per unit keeps domain boundaries visible and independently changeable.

**Boundary:** Preferences define the technical layout; this Principle defines ownership only.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Model documentation explains its public domain surface**

- **Must** — Describe every Domain Definition and Field; document the public surface of every published Definition.
- **Never** — Describe Model as storage, workflow, or application behaviour.

**Each domain concept has one authoritative Domain Definition**

- **Must** — Define each meaningful Target concept once.
- **Never** — Create competing or implementation-only domain definitions.

**Model preserves explicit Target meaning**

- **Must** — Preserve explicit Target Fields, constraints, defaults, and sensitivity classification.
- **Never** — Invent or override Target meaning.

**Concrete Model realizations share one Model Foundation**

- **Must** — Use shared mechanisms without injecting shared domain Fields.
- **Never** — Let the Foundation define domain meaning.

**Model exposes an explicit and stable Public Interface**

- **Must** — Publish only explicitly public Definitions through a stable Registry.
- **Never** — Expose internal Definitions implicitly.

**Model validates intrinsic data meaning**

- **Must** — Validate local Definition data and apply declared defaults during construction.
- **Never** — Own cross-definition, stored-data, or workflow rules.

**Model declares every Definition in one standard vocabulary**

- **Must** — Use the standard logical type vocabulary and fully describe every Field.
- **Never** — Include operational or storage decisions in the Definition vocabulary.

**Definitions are flat and independent**

- **Must** — Keep every Definition independent and flat.
- **Never** — Let a Definition depend on another Definition for its meaning.
