# Model Definition

Model defines and publishes the project's reusable data-model Entities and their complete public meaning.

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

Model defines flat, technology-independent Entities. Every Entity carries its own Fields, Entity Metadata, and public Declaration without nesting another Entity.

### Purpose

The meaning of the application's data needs one owner, written once in a technology-independent form and read by everyone through one published surface, so that it never drifts.

### How It Works

Each Entity lives in its own unit and exposes its Declaration and the shared JSON conversion; Interface publishes every Entity by name and as one ordered Entity Collection.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity** — the authoritative logical definition of one meaningful Target concept, with an Identity that distinguishes one instance from another.
- **Field** — one named Entity value with its meaning, declared or resolved Type, value rules, and optional Value Generation.
- **Type** — the Target-declared value category of a Field, or the compatible Model Preference used only when an allowed property is unstated.
- **Required Field** — a non-nullable Field with neither a Default Value nor Value Generation.
- **Identity** — the mandatory id Field that distinguishes one Entity instance from another instance of the same Entity.
- **Activity Field** — the mandatory is_active Field that represents whether an Entity is active.
- **Default Value** — a fixed value used when a Field is omitted.
- **Value Generation** — the declared way to supply a Field value automatically, including Auto Increment or a Generated Identifier.
- **Sensitivity Marker** — optional Field metadata naming one of the recognized markers; it records value meaning but causes no Model-side protection or transformation.
- **Primary Key** — Entity Metadata that names id.
- **Relation** — Entity Metadata connecting one local Field to a target Entity and target Field by logical name.
- **Uniqueness Constraint** — Entity Metadata requiring one Field or an ordered combination of Fields to be unique.
- **Index** — Entity Metadata recording an access intention for one Field or an ordered combination of Fields.
- **Entity Metadata** — Primary Key, Relations, Uniqueness Constraints, and Indexes owned by an Entity rather than one Field.
- **Entity Declaration** — the complete structured public record of one Entity's name, description, ordered Fields, and Entity Metadata.
- **Field Declaration** — the complete structured public record of one Field's name, description, Type, presence meaning, Default Value, sensitivity, immutability, constraints, and Value Generation.
- **JSON Object** — the representation of one Entity as JSON text conforming to the JSON standard, with one object at its root whose keys are the Entity's Fields.
- **Entity Export** — the explicit named export through which one actual Entity is imported directly by its own name.
- **Entity Collection** — the ordered immutable public collection of every actual Entity, in Target order.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
├── Interface       ← every Entity by name and the Entity Collection, in the shape the Model Interface Schema defines
├── Entity          ← one unit per Target Entity
└── Core
    ├── Declaration ← the public logical contract
    └── Foundation  ← the shared JSON conversion
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Queries, migrations, Instances, and storage lifecycle** — are not Model's, because they describe how data is stored and handled, not what it means. A language profile may realize Entities in a table-ready form, but Model never runs storage.
- **Actions, decisions, workflows, authorization, quotas, and orchestration** — are not Model's, because they depend on an operation and its application context rather than on one Entity's own data.
- **Endpoints, requests, responses, protocols, and transport schemas** — are not Model's, because they are properties of a transport, not of what the data means.
- **Encryption, hashing, masking, and secret storage** — are not Model's, because they protect a value rather than define it.
- **Initial Data and runtime records** — are not Model's, because they are data rather than the meaning of data.
- **How an Entity is used** — is not Model's, because Model publishes a contract, not a usage.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Model Preferences own configurable names, language, package, naming, symbols, method names, layout, technical realization, Field defaults, and documentation choices; these selections realize the responsibilities in Architecture without changing them. The shape of Interface belongs to the Model Interface Schema.

### Interface

The package-root entrypoint through which every Entity is published, in the shape the Model Interface Schema defines. It meets these needs:

1. **Complete** — exactly one Entity Export for every Target Entity, and the Entity Collection holding every Target Entity in Target order, changing when the Target changes.
2. **Actual** — each export and each Collection item is the actual Entity, exposing its own actual Declaration, never a copy.
3. **Nothing else** — nothing beyond these is published, and loading Interface has no side effect.

The exact shape of these needs is fixed by the Model Interface Schema, which is built from them. These needs are the reference: when the two differ, the Schema is corrected to match them.

### Entity

The public area containing exactly one unit for every Entity. Each Entity exposes its own complete Declaration and the shared Foundation capabilities.

### Core

The shared area containing the public Declaration and Foundation contracts plus any private base definitions and helpers shared across Entities. Declaration is the public structured contract for Entity and Field meaning; Foundation is the public shared conversion contract between an Entity and its JSON Object.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Model. Model Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning retains its authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the Architecture or Layering category that owns it.

### General

#### Model meaning comes only from the Target

**Rule:** Model preserves every Target-declared Entity, Field, parameter, explicit false, explicit null, Type, constraint, Default Value, Sensitivity Marker, Value Generation, Primary Key, Relation, Uniqueness Constraint, and Index, and adds only id, is_active, and compatible Preference defaults for unstated allowed properties. This meaning stays independent of language, package, tool, version, runtime, platform, database, and Engine: technology selects realization only, and a missing native capability is implemented privately only when meaning stays exact.
**Why:** One authority keeps convenience, package defaults, and technology from changing the domain.
**Boundary:** Model's contract changes only under Target authority, never to fit a consumer. If the selected technology cannot preserve a contract, generation reports the incompatibility instead of weakening meaning.

#### Model has one canonical structure

**Rule:** Every realization contains Interface, the Entity directory, and Core with Declaration and Foundation, with the ownership shown in Architecture. Every Entity has exactly one public unit directly inside the Entity directory, holding everything private to that Entity; infrastructure shared across Entities belongs under Core. Declaration and Foundation are public; base definitions, validation mechanisms, adapters, and other helpers stay private. Dependencies flow from Interface to Entity units and from Entity units to Core; Core depends on neither Interface nor a specific Entity.
**Why:** Stable ownership keeps each Entity independently changeable, prevents cycles, and gives consumers Model's meaning without its internals.
**Boundary:** Language-required files, entrypoints, annotations, and native constructs may exist without creating another conceptual layer; physical casing, extensions, and symbol and method names belong to the language's Preferences.

<br>

### Interface

#### Interface conforms to the Model Interface Schema

**Rule:** Every realization of Interface conforms to the versioned Model Interface Schema, which fixes the Entity Exports, the Entity Collection, each Entity's exposed Declaration, and what Interface never publishes or does.
**Why:** Consumers depend on one contract instead of reinterpreting each realization, and can both import one Entity's real type and enumerate all of them.
**Boundary:** Entity membership and meaning change under Target authority without being an Interface-structure change; changing the structure itself requires a Schema version change.

<br>

### Entity

#### Every Entity follows one complete structural contract

**Rule:** Every Target domain concept produces exactly one uniquely named Entity. Each Entity preserves its description, has exactly one Identity, id, named by its Primary Key, and exactly one Activity Field, is_active. id is always non-nullable and immutable once assigned; is_active is always a non-nullable, mutable Boolean. Where the Target leaves their remaining properties unstated, Model Preferences supply them.
**Why:** One structural contract prevents generators from reshaping domain concepts. Every Entity needs id so each instance can be identified, and is_active so any record can be taken out of use and restored without being deleted, keeping its history and every Relation that points to it intact.
**Boundary:** Model adds no universal Field other than id and is_active.

#### Entity Metadata is complete and Entities stay flat

**Rule:** Primary Key, Relations, Uniqueness Constraints, and Indexes belong to Entity Metadata outside Field Declarations. Every local Field reference resolves within the Entity; every Relation target Entity and Field resolves within Model; Relation endpoint Types are compatible; participating Fields are not repeated; duplicate metadata is invalid. An Entity contains only its own Fields and metadata: cross-Entity meaning is recorded only by Relation names, never by nesting, inheriting, copying, or importing another Entity.
**Why:** Consumers realize structure only from complete, unambiguous metadata, and flat Entities avoid hidden coupling.
**Boundary:** A Relation records local Field, target Entity name, and target Field name only, with no cardinality, cascade, deletion, or other undeclared behaviour. An Entity may use a shared private base from Core without inheriting another Entity's meaning.

#### Entity runtime behaviour enforces Field contracts only

**Rule:** Direct and JSON Object construction accept only declared Fields and identically enforce required values, nullability, Types, defaults, generation, and constraints without implicit coercion; explicit false, zero, empty string, and null remain supplied values. Assignment to a mutable Field revalidates atomically, a failed assignment keeps the prior value, and an immutable Field cannot change. Model defines no equality, ordering, hashing, copy, clone, merge, or reconstruction beyond the JSON Object round trip, and mutable Entities are not hashable.
**Why:** One runtime contract stops package-specific construction, mutation, and object conventions from changing data or inventing behaviour.
**Boundary:** Construction and mutation perform no storage, network, application, or workflow operation. A language-required diagnostic representation may exist internally but is not a portable contract.

#### Generated identities follow their declaration

**Rule:** An omitted Auto Increment Field remains in an explicit pending state without becoming nullable, rejects a caller-supplied value unless Target explicitly permits one, and is never assigned by Model. A Generated Identifier is produced during Entity creation when declared, using the algorithm Model Preferences select unless the Target names another.
**Why:** Generation ownership prevents callers from choosing values that another realization is responsible for assigning.
**Boundary:** The pending representation may use JSON null solely to represent not-yet-generated Auto Increment state; it does not change the Field's nullability.

#### Sensitivity remains metadata

**Rule:** Only the Sensitivity Markers that Model Preferences recognize are accepted. Model preserves the actual value unchanged in Entity state and JSON Object, exposes the marker through Declaration, never encrypts, hashes, masks, redacts, authorizes, inspects, ignores, or remaps a value because of it, and never echoes a sensitive value in validation or generation diagnostics.
**Why:** Model preserves sensitivity meaning without taking ownership of protection.
**Boundary:** Generated source, fixtures, and examples use no real credential or secret. A new marker requires an explicit addition to Model Preferences.

#### Logical names remain exact and physical names remain deterministic

**Rule:** Logical Entity and Field names, including Relation names, preserve exact case-sensitive Target spelling. Generation never translates, abbreviates, pluralizes, respells, prefixes, suffixes, or aliases them. Physical names apply the selected language's naming rules deterministically and reject unresolvable reserved-word or normalization collisions.
**Why:** Domain names remain understandable without technical context while source follows its language.
**Boundary:** Language-specific naming belongs to that language's Preferences and never changes names stored in Declaration.

<br>

### Core

#### Fields and Declarations carry one complete value contract

**Rule:** Every Field name is unique within its Entity and preserves, in Target order, its description, declared or resolved Type, nullability, explicit Default Value presence and value, Sensitivity Marker, immutability, applicable constraints, and optional Value Generation. Absence of a Default Value differs from explicit null; no Field has both a Default Value and Value Generation; every default and generated value satisfies the Field contract. Every Entity Declaration publicly exposes its name, description, ordered Fields, Primary Key, Relations, Uniqueness Constraints, and Indexes, and every Field Declaration exposes exactly the Field properties above; physical member names are selected by Model Preferences.
**Why:** One complete logical shape stops languages and packages from reading omission, null, defaults, or generation differently, and makes independent implementations comparable.
**Boundary:** Invalid, incompatible, or contradictory values and constraints fail instead of being ignored, coerced, or replaced. Declaration holds no runtime behaviour and chooses no technical type, table, query, index implementation, transport, or consumer behaviour.

#### Foundation converts Entities through JSON Objects

**Rule:** Foundation converts an Entity to a JSON Object — JSON text conforming to the JSON standard, with one object at its root whose keys are exactly the Entity's Field names in Declaration order — and reconstructs an Entity from that text without loss. Values preserve declared Type semantics and distinguish null, false, zero, and empty string. Reconstruction rejects malformed text and otherwise applies Principle "Entity runtime behaviour enforces Field contracts only".
**Why:** Consumers need one portable, lossless value representation.
**Boundary:** Foundation does not add Declaration metadata, nest Entities, add keys, transform sensitive values, or define domain meaning. How a consumer's language represents the decoded text is that consumer's concern.

<br>

### Review

#### Model conformance covers every Model contract

**Rule:** Model is conformant only when its Interface needs in this Definition, the Model Interface Schema, and its real output all match one another, and every observation below holds.
**Why:** A gap here lets a broken Model look complete to every consumer.
**Boundary:** Review reads the Target only to compare; it changes nothing.

#### Review observes Model through a fixed set of checks

**Rule:** Review establishes Model conformance through these observations, every one of them on every review:

- Every need of the Interface layer in this Definition appears in the Model Interface Schema, and the Schema holds nothing beyond them.
- Every Target Entity has exactly one Entity Export.
- The Entity Collection holds exactly the exported Entities, in Target order.
- Each Entity's Declaration matches the Target — Fields, order, Types, nullability, defaults, and metadata.
- Every Entity has an immutable id and a Boolean is_active.
- Each Entity constructs from valid values and rejects an unknown Field, a wrong Type, and a missing required value.
- Converting any Entity to its JSON Object and back returns an equal Entity.
- Decimal and datetime values keep their exact value through JSON.
- Loading Interface has no side effect.
- An unknown Type in the Target stops generation.
- Each Entity's storage mapping — Table and column names, constraint and index names, and the identity column — takes exactly the form Model Preferences list.

**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation below derives from the Principle with the same title.

### General

**Model meaning comes only from the Target**

- **Must** — Preserve every explicit Target item, add only id, is_active, and approved defaults, and realize technology without changing meaning.
- **Never** — Remove, rename, override, or invent Target meaning, or weaken a contract for a technology.

**Model has one canonical structure**

- **Must** — Keep one public unit per Entity, shared infrastructure and public contracts in Core, helpers private, and dependencies one-way.
- **Never** — Create a dependency cycle or another conceptual layer, or expose a helper as contract.

### Interface

**Interface conforms to the Model Interface Schema**

- **Must** — Conform every realization to the Model Interface Schema.
- **Never** — change Interface structure because Entity membership, language, package, or internal implementation changed.

### Entity

**Every Entity follows one complete structural contract**

- **Must** — preserve each Entity and supply exactly one non-nullable immutable id and one non-nullable mutable Boolean is_active, taking their remaining unstated properties from Preferences.
- **Never** — add another universal Field or reshape a Target concept.

**Entity Metadata is complete and Entities stay flat**

- **Must** — Keep metadata outside Fields, resolve every reference, and record cross-Entity meaning only by Relation names.
- **Never** — Accept unresolved or duplicate metadata, invent relationship behaviour, or nest, inherit, copy, or import another Entity.

**Entity runtime behaviour enforces Field contracts only**

- **Must** — Apply identical strict Field rules to direct construction, JSON Object construction, and mutation.
- **Never** — Accept unknown Fields, coerce values, allow invalid mutation, or invent equality, ordering, hashing, copying, or merging.

**Generated identities follow their declaration**

- **Must** — keep an omitted Auto Increment Field pending and never assign it inside Model.
- **Never** — accept caller-supplied Auto Increment values unless Target explicitly permits them.

**Sensitivity remains metadata**

- **Must** — preserve recognized markers and actual values while excluding sensitive values from diagnostics and artifacts.
- **Never** — protect, transform, authorize, inspect, or remap values inside Model because of a marker.

**Logical names remain exact and physical names remain deterministic**

- **Must** — preserve logical Target names and apply language-specific physical naming deterministically.
- **Never** — silently translate, pluralize, alias, or repair a collision.

### Core

**Fields and Declarations carry one complete value contract**

- **Must** — Preserve and publicly expose every Field and Entity property, explicit value, constraint, order, and generation rule.
- **Never** — Combine a Default Value with Value Generation, coerce an incompatible value, or put runtime or technical choices in Declaration.

**Foundation converts Entities through JSON Objects**

- **Must** — provide lossless Entity-to-Object and Object-to-Entity conversion with exact keys and values.
- **Must** — produce and accept JSON text conforming to the JSON standard.
- **Never** — add keys or metadata, nest Entities, coerce values, or transform sensitive data.

### Review

**Model conformance covers every Model contract**

- **Must** — show that the Interface needs, the Model Interface Schema, and the real output all match and every observation holds before Model is conformant.
- **Never** — change anything during review.

**Review observes Model through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
