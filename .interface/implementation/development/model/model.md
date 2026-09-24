# Model Definition

Model defines the Target's logical data concepts as a reusable library for Database and Logic.

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

Model gives Database and Logic one shared, technology-independent definition of each domain concept.

### How It Works

Each Definition stands alone in the Definitions layer. Database and Logic reach the library through its Public Interface, which provides the tools to import Models. Model Foundation gives every Model shared validation and conversion to and from JSON.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Domain Definition** — the authoritative logical definition of one meaningful concept in the Target's domain.
- **Definitions** — the Model layer that contains one separate unit for each Domain Definition.
- **Field** — one named value of a Domain Definition, with its domain meaning, logical type, and applicable constraints.
- **Model Foundation** — the shared, technology-independent mechanisms through which Model realizations validate their data and convert to or from JSON.
- **Intrinsic Rule** — a rule evaluated only from the data of the Domain Definition it governs.
- **Declaration Vocabulary** — the technology-independent vocabulary in which each Domain Definition declares its meaning and Fields.
- **Public Interface** — the only surface through which another Component imports and uses Model Definitions.
- **Supporting Content** — the shared Declaration Vocabulary, Model Foundation, and other common mechanisms supporting Definitions and the Public Interface.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
└── Layers
    ├── Public Interface
    ├── Definitions
    └── Supporting Content
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Database** — imports Model Definitions through the Public Interface to realize storage.
- **Logic** — imports Model Definitions through the Public Interface to use validated domain data.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

- **Public Interface** — provides Model import tools to consuming Components.
- **Definitions** — contains each independent Domain Definition and its own content.
- **Supporting Content** — provides Model Foundation, Declaration Vocabulary, and other shared content.

Technical choices, defaults, and directory names for these layers belong to Model Preferences. The structure of a Model declaration belongs to the Model Declaration Schema.

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

### Model Foundation provides common validation and JSON conversion

**Rule:** Every Model uses Model Foundation for shared validation and for converting an instance to JSON or creating an instance from JSON. Foundation never injects domain Fields or domain meaning.

**Why:** The library has one consistent implementation of its common functions without imposing a shared domain structure.

**Boundary:** Foundation supplies only these common mechanisms; each Model retains its own Definition and validation rules.

<br>

### Model exposes one Public Interface

**Rule:** Database and Logic use Model only through its Public Interface. The Public Interface provides the tools required to import Model Definitions; JSON conversion functions remain on the imported Model and come from Foundation.

**Why:** One surface keeps consumption consistent while Model implementations remain free to change internally.

**Boundary:** Consumers do not depend on private Model resources or reimplement Model conversion functions.

<br>

### Model validates intrinsic data meaning

**Rule:** Model validates Field constraints and Intrinsic Rules evaluable from the data of one Model. Construction applies declared defaults when an input omits a Field and validates the resulting instance.

**Why:** Each instance entering or leaving a consuming Component has data that conforms to its Model Definition.

**Boundary:** Cross-Model, stored-data, workflow, authorization, and external-context rules remain outside Model.

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

### Model declares every Definition in one standard vocabulary

**Rule:** Every Domain Definition declares its name, description, kind, Fields, Intrinsic Rules, and enumeration literals when applicable. Every Field declares its name, description, logical type, presence semantics, default when one exists, and applicable constraints. The Model Declaration Schema supplies the common structure without limiting the logical types a Model may declare.

**Why:** One vocabulary gives consumers a complete shared description without importing storage or technology decisions.

**Boundary:** The vocabulary remains limited to each independent Definition and its own Fields; operational and storage decisions remain outside Model.

<br>

### Definitions are flat and independent

**Rule:** Every Domain Definition is self-contained, flat, and independently understandable.

**Why:** Independent flat Definitions prevent hidden coupling and keep each concept understandable on its own.

**Boundary:** An Enumeration is itself an independent Domain Definition with its own content.

<br>

### Each Domain Definition stands in its own unit

**Rule:** Every Domain Definition has one unit of its own in the Definitions layer. Content used by exactly one Definition remains with it; shared content belongs to Supporting Content.

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

**Model Foundation provides common validation and JSON conversion**

- **Must** — Use Foundation for validation and conversion to and from JSON.
- **Never** — Let Foundation define domain meaning.

**Model exposes one Public Interface**

- **Must** — Import Model Definitions through the Public Interface.
- **Never** — Depend on private Model resources or duplicate conversion functions.

**Model validates intrinsic data meaning**

- **Must** — Validate Field constraints and local Model rules; apply declared defaults during construction.
- **Never** — Own stored-data, workflow, or external-context rules.

**Model declares every Definition in one standard vocabulary**

- **Must** — Describe every Definition and Field through the common Schema structure.
- **Never** — Restrict a Model to a fixed list of logical types.

**Definitions are flat and independent**

- **Must** — Keep every Definition independent and flat.
- **Never** — Let a Definition depend on another Definition for its meaning.
