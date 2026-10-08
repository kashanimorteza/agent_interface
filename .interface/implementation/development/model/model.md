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
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

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
- **Foundation** — the public shared contract every Entity extends, giving it Conversion to and from its JSON Object.
- **Entity Export** — the explicit named export through which one actual Entity is imported directly by its own name.
- **Entity Collection** — the ordered immutable public collection of every actual Entity, in Target order.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
├── Entity
├── Interface
└── Documentation
```

Every entity below is declared in `architecture` in Model Preferences, which also own the configurable names, language, package, naming, symbols, method names, technical realization, Field defaults, and documentation choices; these selections realize the responsibilities below without changing them.

<!-------------------------- Entity -->
### Entity

```text
Entity
├── Declaration
├── Validation
├── Conversion
└── Storage Mapping
```

The public area containing exactly one unit for every Entity. Each Entity exposes its own complete Declaration and the shared Foundation capabilities. Every Entity carries the mandatory Identity (`id`) and Activity Field (`is_active`), whose default properties come from Model Preferences.

Every Entity is realized in the same layers, from the most general to the most specific:

1. **Base** — private and shared: realizes Validation for every Entity on top of the selected modeling package.
2. **Foundation** — public and shared: extends Base with Conversion.
3. **Entity unit** — one per Entity: holds its Declaration as a read-only member of its type, and that type, which extends Foundation and declares every Field in Declaration order.

Each Field of the type is realized from its Field Declaration and its Entity's Metadata through Storage Mapping, so value rules are written once, in the Declaration, and never repeated beside it. When an Entity type is defined, Base checks that its type name and table name equal the Entity's physical name and that its Fields are exactly the Declaration's Fields in the same order; a mismatch fails loading.

#### Declaration

```text
Declaration
├── Entity Declaration
│   ├── name
│   ├── description
│   ├── fields
│   ├── primary_key
│   ├── relations
│   ├── uniqueness_constraints
│   └── indexes
├── Field Declaration
│   ├── name
│   ├── type
│   ├── nullable
│   ├── description
│   ├── default
│   ├── sensitivity
│   ├── immutable
│   ├── constraints
│   └── value_generation
├── Field Constraints
├── Relation
├── Uniqueness Constraint
├── Index
├── Field Type
├── Value Generation
└── Sensitivity
```

The public structured contract for Entity and Field meaning. An Entity Declaration records one Entity's name, description, ordered Fields, and Entity Metadata; a Field Declaration records one Field's name, description, Type, presence meaning, Default Value, sensitivity, immutability, constraints, and Value Generation. Primary Key, Relations, Uniqueness Constraints, and Indexes are Entity Metadata outside the Field Declarations.

Every Declaration is an immutable record with ordered immutable collections and no runtime behavior. Its structural rules are checked when it is created, and an invalid or contradictory Declaration fails instead of being repaired:

- Field names are unique within the Entity.
- The Primary Key names `id`, which is non-nullable and immutable; `is_active` is a non-nullable, mutable boolean.
- A Field Declaration distinguishes an absent Default Value from an explicit null default; a default matches the Field's Type and nullability, and never coexists with Value Generation.
- A size constraint is a positive length and applies only to a string Field.
- Every Relation names a known local Field, and one local Field has at most one Relation.
- Every Uniqueness Constraint and Index names a non-empty ordered set of known Fields, without repeating a Field or duplicating another entry.

##### Field Type

```text
Field Type
├── string
├── integer
├── float
├── decimal
├── boolean
├── datetime
├── date
├── time
└── uuid
```

The closed set of Field Types; any other Type is refused, and an unknown Type stops generation instead of being guessed. The realization of each Type in the selected language and in a JSON Object belongs to that language's profile in Model Preferences.

A float is always finite, because a JSON Object has no form for NaN or infinity; a datetime is always timezone-aware.

##### Value Generation

```text
Value Generation
├── auto_increment
└── generated_identifier
```

The declared ways a Field value is supplied automatically. Auto Increment leaves the value pending until storage assigns it; a Generated Identifier is produced during Entity creation with the algorithm Model Preferences select, unless the Target names another.

Auto Increment requires an integer Field, and a Generated Identifier requires a uuid or string Field. A caller-supplied value for an Auto Increment Field is refused at construction and at assignment, unless the Target explicitly permits one.

##### Sensitivity

```text
Sensitivity
├── password
└── sensitive
```

The recognized Sensitivity Markers, listed in Model Preferences. A marker records what a value means and changes nothing about it.

Its only effect is in Validation: the input of a marked Field is replaced in every validation message, and the original message holding the value is never chained or exposed.

#### Validation

```text
Validation
├── Strict
├── Construction
├── Assignment
└── Identity
```

The shared private behavior every Entity inherits: direct construction, JSON Object construction, and assignment accept only declared Fields and enforce each Field's contract, and a sensitive value never appears in a validation message.

- **Strict** — no implicit coercion, no undeclared Field, and every default is itself validated against its Field.
- **Construction** — direct construction validates the whole Entity before any value is set.
- **Assignment** — assigning an immutable Field, or an Auto Increment Field the Target does not open to callers, is refused; any other assignment validates the whole Entity with the new value first, so a failed assignment keeps the prior value.
- **Identity** — a mutable Entity is not hashable.

#### Conversion

```text
Conversion
├── to_json
└── from_json
```

Foundation, the public shared conversion contract between an Entity and its JSON Object, giving every Entity a lossless round trip through JSON text.

- **to_json** — returns JSON text with one root object whose keys are exactly the Entity's Field names, in Declaration order.
- **from_json** — rejects malformed text, a repeated key, a non-standard constant, and a root that is not one object; decodes the text forms of decimal, datetime, date, time, and uuid by each Field's Type; then builds the Entity with the same rules as direct construction.

#### Storage Mapping

```text
Storage Mapping
├── Names
├── Keys and constraints
├── Identity
└── Exact values
```

The private, table-ready realization every Entity always has when the selected language profile defines one: physical table and column names, column types, and the constraints and indexes its Declaration states. The table forms of all Entities are registered in one shared table metadata, which a consumer such as Database reaches through the Entities themselves, so that it creates exactly their Tables and no other. Model only declares this form; it never runs storage.

Every storage option is derived only from the Declaration:

- **Names** — the table is named by the Entity's physical name and each column by its Field name; a name that cannot be resolved fails generation.
- **Keys and constraints** — the Primary Key column, a foreign key for each Relation to the target Entity's table and Field, uniqueness and an index on the column for a single-Field entry, and at table level for a combination; every constraint and index is named by one convention in Model Preferences.
- **Identity** — an Auto Increment Field becomes a generated identity column.
- **Exact values** — a decimal is stored as its exact text and read back as a decimal; a datetime is stored in UTC and read back timezone-aware.

<!-------------------------- Interface -->
### Interface

```text
Interface
├── Entity Export
└── Entity Collection
```

The package-root entrypoint through which every Entity is published. It always publishes both forms, and nothing else:

- **Entity Export** — every Entity on its own, by its own name, for a consumer that works with one specific Entity.
- **Entity Collection** — every Entity together, once each, in Target order, for a consumer that works with all Entities without knowing their names.

For a Target with User and Account, Interface publishes `User`, `Account`, and the Entity Collection holding them in that order, under the symbol name Model Preferences set. A consumer that needs another name gives it on its own side when it imports.

Its Interface contract is these needs, with the symbol names and `contract_version` in Model Preferences:

1. **Complete** — exactly one Entity Export for every Target Entity, and the Entity Collection holding every Target Entity in Target order, changing when the Target changes.
2. **Explicit** — each Entity is exported by an explicit named export, named by the Entity's physical name under the selected language's naming rules; no wildcard or dynamically generated export publishes an Entity.
3. **Actual** — each export and each Collection item is the actual Entity, exposing its own actual Declaration, never a copy, wrapper, alias, or reconstruction.
4. **Nothing else** — no other Entity registry, lookup table, or discovery mechanism is published beside the exports and the Collection.
5. **Publication only** — Interface holds only the imports, the Entity Exports, and the Entity Collection; it runs no check, because the Principles are met at generation and their conformance belongs to Review.
6. **No side effect** — loading Interface creates no Entity instance, data, connection, file, or process, and performs no network, storage, runtime-configuration, or other external side effect.
7. **Versioned** — changing the meaning of the exports, the Collection, or an Entity's exposed Declaration requires raising `contract_version` and a consumer review.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Interface
├── Declaration
├── Foundation
├── Setup
├── Use
├── Verify
└── Troubleshooting
```

The root documentation, in the file, location, and format Model Preferences name. Its sections, in this order:

1. **Overview** — Give one concise introduction and one simple example using one Entity.
2. **Interface** — Explain the Entity Exports and the Entity Collection, then list every Entity once in Target order with its description, complete Field table, and Entity Metadata outside that table. Show one consumer importing an Entity directly and one enumerating the Entity Collection, rather than using wildcard exports, __all__, reflection, directory scanning, or internal paths.
3. **Declaration** — Show how a consumer reads one Entity's public Declaration, including Fields, Primary Key, Relations, Uniqueness Constraints, and Indexes, through the Entity itself.
4. **Foundation** — Give one example for each Foundation capability, then one complete Entity-to-JSON-text-to-Entity round trip.
5. **Setup** — Give the setup steps for the selected technology.
6. **Use** — Show use that follows the Entity Exports and the Entity Collection.
7. **Verify** — Verify Interface-contract-conformant shape, exact Entity Export membership, Entity Collection membership and order and its correspondence with the Exports, actual Entity and Declaration references, immutability, side-effect freedom, representative Entity construction, Declaration access, and a lossless JSON text round trip.
8. **Troubleshooting** — Cover Model concerns only.

Every section follows these rules:

- Define no other Component.
- Expose no private helper as contract.
- Retain no stale meaning.
- Contain no real credential or secret.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── model/
│   ├── interface
│   ├── entity/
│   └── core/
└── README
```

Entity holds one unit per Entity, named by the Entity's name under the selected language's module naming, such as `user` and `account_group`. The names in this tree, and the files named under Core, are the physical names of Model; the root of this tree is the Component directory, and it and the package directory take their names from `settings` in Model Preferences.

#### Core

The shared area holding every file that serves all Entities rather than one: the public Declaration and Foundation contracts, plus the private system files behind them: the base definitions, Field Type realization, and Storage Mapping. The two public contracts are the files `declaration` and `foundation`; the private files are `base` for Validation, `types` for Field Type realization, and `storage` for Storage Mapping, each marked private in the selected language's own way. No other file is placed in Core. Declaration is the public structured contract for Entity and Field meaning; Foundation is the public shared conversion contract between an Entity and its JSON Object.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Queries, migrations, Instances, and storage lifecycle** — are not Model's, because they describe how data is stored and handled, not what it means. The selected language profile, when it defines one, always realizes Entities in a table-ready form, but Model never runs storage.
- **Actions, decisions, workflows, authorization, quotas, and orchestration** — are not Model's, because they depend on an operation and its application context rather than on one Entity's own data.
- **Endpoints, requests, responses, protocols, and transport schemas** — are not Model's, because they are properties of a transport, not of what the data means.
- **Encryption, hashing, masking, and secret storage** — are not Model's, because they protect a value rather than define it.
- **Initial Data and runtime records** — are not Model's, because they are data rather than the meaning of data.
- **How an Entity is used** — is not Model's, because Model publishes a contract, not a usage.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Model. Model Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning retains its authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the Architecture category that owns it.

### General

#### Model meaning comes only from the Target

**Rule:** Model preserves every Target-declared Entity, Field, parameter, explicit false, explicit null, Type, constraint, Default Value, Sensitivity Marker, Value Generation, Primary Key, Relation, Uniqueness Constraint, and Index, and adds only id, is_active, and compatible Preference defaults for unstated allowed properties. This meaning stays independent of language, package, tool, version, runtime, platform, database, and Engine: technology selects realization only, and a missing native capability is implemented privately only when meaning stays exact.
**Why:** One authority keeps convenience, package defaults, and technology from changing the domain.
**Boundary:** Model's contract changes only under Target authority, never to fit a consumer. If the selected technology cannot preserve a contract, generation reports the incompatibility instead of weakening meaning.

#### Model has one canonical structure

**Rule:** Every realization contains Interface, the Entity directory, and Core with Declaration and Foundation, with the ownership shown in Architecture. Every Entity has exactly one public unit directly inside the Entity directory, holding everything private to that Entity; infrastructure shared across Entities belongs under Core. Declaration and Foundation are public; `base`, `types`, and `storage` stay private. Dependencies flow from Interface to Entity units and from Entity units to Core; Core depends on neither Interface nor a specific Entity.
**Why:** Stable ownership keeps each Entity independently changeable, prevents cycles, and gives consumers Model's meaning without its internals.
**Boundary:** Language-required files, entrypoints, annotations, and native constructs may exist without creating another conceptual layer; physical casing, extensions, and symbol and method names belong to the language's Preferences.

<br>

### Interface

#### Interface conforms to the Interface contract

**Rule:** Every realization of Interface conforms to the versioned Interface contract, which fixes the Entity Exports, the Entity Collection, each Entity's exposed Declaration, and what Interface never publishes or does.
**Why:** Consumers depend on one contract instead of reinterpreting each realization, and can both import one Entity's real type and enumerate all of them.
**Boundary:** Entity membership and meaning change under Target authority without being an Interface-structure change; changing the structure itself requires raising `contract_version`.

<br>

### Entity

#### Every Entity follows one complete structural contract

**Rule:** Every Target domain concept produces exactly one uniquely named Entity. Each Entity preserves its description, has exactly one Identity, id, named by its Primary Key, and exactly one Activity Field, is_active. id is always non-nullable and immutable once assigned; is_active is always a non-nullable, mutable Boolean. Where the Target leaves their remaining properties unstated, Model Preferences supply them.
**Why:** One structural contract prevents generators from reshaping domain concepts. Every Entity needs id so each instance can be identified, and is_active so any record can be taken out of use and restored without being deleted, keeping its history and every Relation that points to it intact.
**Boundary:** Model adds no universal Field other than id and is_active.

#### Entity Metadata is complete and Entities stay flat

**Rule:** Primary Key, Relations, Uniqueness Constraints, and Indexes belong to Entity Metadata outside Field Declarations. Every local Field reference resolves within the Entity; every Relation target Entity and Field resolves within Model; Relation endpoint Types are compatible; participating Fields are not repeated; duplicate metadata is invalid. An Entity contains only its own Fields and metadata: cross-Entity meaning is recorded only by Relation names, never by nesting, inheriting, copying, or importing another Entity.
**Why:** Consumers realize structure only from complete, unambiguous metadata, and flat Entities avoid hidden coupling.
**Boundary:** A Relation records local Field, target Entity name, and target Field name only, with no cardinality, cascade, deletion, or other undeclared behaviour. An Entity may use a shared private base from Core without inheriting another Entity's meaning. These rules are met at generation and observed by Review; no runtime check is generated for them.

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
**Boundary:** Language-specific naming belongs to that language's Preferences and never changes names stored in Declaration. Collisions are rejected at generation and observed by Review; no runtime check is generated for them.

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

**Rule:** Model is conformant only when its Interface contract and its real output match one another, and every observation below holds.
**Why:** A gap here lets a broken Model look complete to every consumer.
**Boundary:** Review reads the Target only to compare; it changes nothing.

#### Review observes Model through a fixed set of checks

**Rule:** Review establishes Model conformance through these observations, every one of them on every review:

- Interface publishes every need of its Interface contract and nothing beyond them.
- Every Target Entity has exactly one Entity Export.
- The Entity Collection holds exactly the exported Entities, in Target order.
- Every Relation reaches a Field of an Entity in Model with a compatible Type, and no two Entities collide in name, before or after physical naming.
- Interface runs no check.
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

**Interface conforms to the Interface contract**

- **Must** — Conform every realization to the Interface contract.
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

**Fields and Declarations carry one complete value contract**

- **Must** — Preserve and publicly expose every Field and Entity property, explicit value, constraint, order, and generation rule.
- **Never** — Combine a Default Value with Value Generation, coerce an incompatible value, or put runtime or technical choices in Declaration.

**Foundation converts Entities through JSON Objects**

- **Must** — provide lossless Entity-to-Object and Object-to-Entity conversion with exact keys and values.
- **Must** — produce and accept JSON text conforming to the JSON standard.
- **Never** — add keys or metadata, nest Entities, coerce values, or transform sensitive data.

### Review

**Model conformance covers every Model contract**

- **Must** — show that the Interface contract and the real output match and every observation holds before Model is conformant.
- **Never** — change anything during review.

**Review observes Model through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
