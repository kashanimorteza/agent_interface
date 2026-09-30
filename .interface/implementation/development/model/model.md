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

Model owns what each Entity means and how that meaning is published. It does not own how Entities are stored, what the application does with them, or how they travel over a transport.

### Purpose

Every part of an application ends up carrying an opinion about what its data means — what a User is, which of its Fields may be empty, what makes two of them the same one. When no Component owns that meaning, each forms its own: storage decides a Field's Type from its column, the API from its payload, the interface from its form, and the answers drift until the same record is valid in one place and rejected in another.

Model exists so that meaning is written once, in one technology-independent form, and read by everyone through one published surface. Every other Component reads it instead of inventing its own, which is what makes them agree without coordinating — and a Component behind it can change without the data being renegotiated.

### How It Works

Interface follows the fixed Model Interface Schema. It exports every Entity by its own name, so a consumer that works with one Entity imports that Entity directly, and it publishes one ordered Entity Collection of every Entity, so a consumer that works with all of them enumerates them without knowing their names. Every Entity exposes its own actual Declaration. Foundation supplies shared Entity-to-JSON Object and JSON Object-to-Entity conversion. Consumers use these published exports and never interpret Model files, internal paths, or implementation details.

### Decisions

**Serialization**

1. Foundation's conversion produces JSON text conforming to the JSON standard, with one object at its root whose keys are the Entity's Fields in Declaration order, and accepts that text back. How a language decodes the text afterward is that language's concern. This replaces the earlier decision that conversion produce a decoded structure and leave text encoding to the consumer: a decoded structure is a language concept, and only JSON text is independent of every language.

**Relations**

1. A Relation records its target Entity and target Field by logical name, and one Entity never imports another. This replaces the earlier rule that a Relation carry the referred definition itself. The risk that rule guarded against — a misspelled or renamed target going unnoticed — is covered by Principle "Entity Metadata resolves completely", which resolves every name during generation.

**Interface**

1. Interface exports every Entity by its own explicit name, so a consumer imports the Entity it works with directly, and publishes one ordered Entity Collection of every Entity for a consumer that works with all of them. This replaces EntityCatalog, EntityEntry, and their lookup capabilities: a lookup by name hides an Entity's real type from the consumer, and each Entity already exposes its own Declaration. Removing the Catalog without a collection was rejected, because a consumer working with all Entities would then have no way to enumerate them except scanning Model or reading the Target.

**Activity**

1. is_active is a Model contract on every Entity: any record can be taken out of use and restored without being deleted. It is Model's own contract, imposed by no consumer.

**Generation rules**

1. The general generation rules — writing only inside the Component, determinism, atomic failure, and source standard — are stated once in the Develop Operation, so every Component shares one statement of them. Every check is made by the Review Operation, which reads this file's Review category; Plan and Develop check nothing.

**Sensitive values**

1. Which Component applies a Target-declared hashing or encryption requirement is not yet decided. Until it is, Model preserves only the Sensitivity Marker and the actual value.

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
- **Declaration** — the public Core contract that represents Entity and Field Declarations without defining Entity behaviour.
- **Foundation** — the public Core contract that supplies shared conversion capabilities without defining domain meaning.
- **JSON Object** — the representation of one Entity as JSON text conforming to the JSON standard, with one object at its root whose keys are the Entity's Fields.
- **Entity Export** — the explicit named export through which one actual Entity is imported directly by its own name.
- **Entity Collection** — the ordered immutable public collection of every actual Entity, in Target order.
- **Interface** — the standard public entrypoint that realizes the Model Interface Schema and publishes every Entity Export and the Entity Collection.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
├── Interface       ← the only public entry point: Entity Exports and Entity Collection
├── Entity          ← one unit per Target Entity
├── Core
│   ├── Declaration ← the public logical contract
│   └── Foundation  ← the shared JSON conversion
└── Documentation   ← the public explanation of the surface above
```

**Interface** is the package-root entrypoint through which every Entity is published, in the shape the Model Interface Schema defines.

**Entity** is the public area containing exactly one unit for every Entity. Each Entity exposes its own complete Declaration and the shared Foundation capabilities.

**Core** is the shared area containing public Declaration and Foundation contracts plus any private base definitions and helpers shared across Entities. Core never depends on Interface or one specific Entity.

**Declaration** is the public structured contract for Entity and Field meaning.

**Foundation** is the public shared conversion contract between an Entity and its JSON Object.

**Documentation** is the root documentation explaining Interface, every public Entity, Declaration, Foundation, setup, use, verification, and Model-specific troubleshooting.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development** — takes the shared language standards, quality tools, and platform defaults it does not choose for itself, and its place in the Connection graph.
- **Consumes no other Component** — Model depends on no peer Component; the language and packages its Preferences select are realization dependencies, not Component dependencies.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Tables, queries, migrations, Instances, and storage lifecycle** — are not Model's, because they describe how data is stored, not what it means; Model records an Index or a Uniqueness Constraint as meaning only, never how it is stored.
- **Actions, decisions, workflows, authorization, quotas, and orchestration** — are not Model's, because they depend on an operation and its application context rather than on one Entity's own data.
- **Endpoints, requests, responses, protocols, and transport schemas** — are not Model's, because they are properties of a transport, not of what the data means.
- **Encryption, hashing, masking, and secret storage** — are not Model's, because they protect a value rather than define it.
- **Initial Data and runtime records** — are not Model's, because they are data rather than the meaning of data.
- **How an Entity is realized or used** — is not Model's, because Model publishes a contract, not a usage.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Model Preferences own configurable names, language, package, naming, symbols, method names, layout, technical realization, Field defaults, and documentation choices; these selections realize the responsibilities in Architecture without changing them. The shape of Interface belongs to the Model Interface Schema. Implementation applies both to the current Target.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory; the claim is about the Principles, not about every sentence in the file. Model Preferences may complete an unstated compatible choice but never override or weaken a Principle, and explicit compatible Target meaning takes precedence over a Preference. A project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the Architecture or Layering category that owns it.

### General

#### Model preserves authoritative meaning

**Rule:** Model preserves every Target-declared Entity, Field, parameter, explicit false, explicit null, Type, constraint, Default Value, Sensitivity Marker, Value Generation, Primary Key, Relation, Uniqueness Constraint, and Index. It additionally supplies only the mandatory id and is_active contract and compatible Preference defaults approved by this Definition. A Preference completes only an unstated allowed property and never removes, renames, or overrides explicit compatible Target meaning.
**Why:** One authority prevents generated convenience and package defaults from changing the domain.
**Boundary:** An explicit Target change may add, modify, rename, or remove Target-owned meaning; Model applies that change without inventing another one. Model's contract changes only under Target authority, never to fit what a consumer can or cannot do.

#### Technology never redefines Model

**Rule:** Entity and Field meaning remains understandable independently of language, package, tool, version, runtime, platform, database, and Engine. Preferences select technical realization only. Explicit Model meaning overrides package defaults, and a missing native capability is implemented privately only when meaning remains exact.
**Why:** Technology can change without redefining the Target's data.
**Boundary:** If selected technology cannot preserve a contract, generation reports incompatibility instead of weakening or omitting meaning.

#### Model has one canonical Architecture

**Rule:** Every realization contains the root Interface, Entity directory, Core directory, Declaration, Foundation, one unit per Entity, and root Documentation with the ownership shown in Architecture. Dependencies flow from Interface to Entity units and from Entity units to shared Core contracts; Core depends on neither Interface nor a specific Entity.
**Why:** Stable ownership makes implementations comparable and prevents cycles.
**Boundary:** Language-required manifests, package entrypoints, annotations, inheritance from a shared private base, and similar technical files may exist without creating another conceptual layer or moving an owned responsibility.

<br>

### Interface

#### Interface conforms to the Model Interface Schema

**Rule:** Every realization of Interface conforms to the versioned Model Interface Schema, which fixes the Entity Exports, the Entity Collection, each Entity's exposed Declaration, and what Interface never publishes or does. Model's own part is membership: exactly the current Target Entities, in Target order, each the actual public Entity.
**Why:** Consumers depend on one contract instead of reinterpreting each realization, and can both import one Entity's real type and enumerate all of them.
**Boundary:** Entity membership and meaning change under Target authority without being an Interface-structure change; changing the structure itself requires a Schema version change.

<br>

### Entity

#### Every Entity follows one complete structural contract

**Rule:** Every Target domain concept produces exactly one uniquely named Entity in Target order. Each Entity preserves its description and ordered Fields, carries complete Entity Metadata, has exactly one Identity, id, named by its Primary Key, and exactly one Activity Field, is_active. id is always non-nullable and immutable once assigned; is_active is always a non-nullable, mutable Boolean. Where the Target leaves their remaining properties unstated, Model Preferences supply them.
**Why:** One structural contract prevents generators from reshaping domain concepts. Every Entity needs id so each instance can be identified, and is_active so any record can be taken out of use and restored without being deleted, keeping its history and every Relation that points to it intact.
**Boundary:** Model adds no universal Field other than id and is_active.

#### Fields preserve a complete value contract

**Rule:** Every Field name is unique within its Entity and preserves its description, declared or resolved Type, nullability, explicit Default Value presence and value, sensitivity, immutability, applicable constraints, and optional Value Generation in Target order. Absence of a Default Value differs from explicit null; one Field never has both a Default Value and Value Generation; every default and generated value satisfies the Field contract.
**Why:** Explicit value semantics prevent languages and packages from interpreting omission, null, defaults, or generation differently.
**Boundary:** Invalid, incompatible, or internally contradictory values and constraints fail instead of being ignored, coerced, or replaced.

#### Entity Metadata resolves completely

**Rule:** Primary Key, Relations, Uniqueness Constraints, and Indexes belong to Entity Metadata outside Field Declarations. Every local Field reference resolves within the Entity; every Relation target Entity and Field resolves within Model; Relation endpoint Types are compatible; participating Fields are not repeated; and duplicate metadata declarations are invalid.
**Why:** Consumers can realize structure only from complete, unambiguous metadata.
**Boundary:** A Relation records local Field, target Entity name, and target Field name only; it adds no target class, cardinality, cascade, deletion, or other undeclared behaviour.

#### Entities remain flat and independent

**Rule:** An Entity contains only its own Fields and metadata. Cross-Entity meaning is recorded by Relation names rather than nesting, inheriting, or copying another Entity, and one Entity never imports another to establish that Relation.
**Why:** Flat Entities avoid hidden structural coupling.
**Boundary:** An Entity may use a shared private base or helper from Core without inheriting domain meaning from another Entity.

#### Each Entity owns one public unit

**Rule:** Every Entity has exactly one public unit directly inside the Entity directory. Entity-private content remains in that unit, while infrastructure shared across Entities belongs under Core.
**Why:** One unit per Entity keeps domain ownership visible and independently changeable.
**Boundary:** Preferences select physical casing and extension without moving an Entity into Core, Interface, or another Entity's unit.

#### Construction and mutation enforce Field contracts

**Rule:** Direct and JSON Object construction accept only declared Fields and identically enforce required values, nullability, Types, defaults, generation, and constraints without implicit coercion. Explicit false, zero, empty string, and null remain supplied values. Assignment to a mutable Field revalidates atomically; failed assignment preserves the prior value; an immutable Field cannot change.
**Why:** One runtime contract prevents package-specific construction and mutation semantics from changing data.
**Boundary:** Construction and mutation perform no storage, network, application, workflow, or orchestration operation.

#### Generated identities follow their declared owner

**Rule:** An omitted Auto Increment Field remains in an explicit pending state without becoming nullable, rejects a caller-supplied value unless Target explicitly permits one, receives its value from the owning persistence realization. A Generated Identifier is produced during Entity creation when declared, using the algorithm Model Preferences select unless the Target names another.
**Why:** Generation ownership prevents callers from choosing values that another realization is responsible for assigning.
**Boundary:** The pending representation may use JSON null solely to represent not-yet-generated Auto Increment state; it does not change the Field's nullability.

#### Entity state adds no undeclared semantics

**Rule:** Entity state is mutable except for immutable Fields. Model defines no portable equality, ordering, hashing, copy, clone, merge, or reconstruction mechanism beyond its declared JSON Object round trip, and mutable Entities are not made hashable.
**Why:** Model must not invent domain behaviour from language object conventions.
**Boundary:** Language-required diagnostic representation may exist internally but is not a portable Model contract or reconstruction format.

#### Sensitivity remains metadata

**Rule:** Only the Sensitivity Markers that Model Preferences recognize are accepted. Model preserves the actual value unchanged in Entity state and JSON Object, exposes the marker through Declaration, never encrypts, hashes, masks, redacts, authorizes, inspects, ignores, or remaps a value because of it, and never echoes a sensitive value in validation or generation diagnostics.
**Why:** Model preserves sensitivity meaning without taking ownership of protection.
**Boundary:** Generated source, Documentation, fixtures, and examples use no real credential or secret. A new marker requires an explicit addition to Model Preferences.

#### Logical names remain exact and physical names remain deterministic

**Rule:** Logical Entity and Field names, including Relation names, preserve exact case-sensitive Target spelling. Generation never translates, abbreviates, pluralizes, respells, prefixes, suffixes, or aliases them. Physical names apply the selected language's naming rules deterministically and reject unresolvable reserved-word or normalization collisions.
**Why:** Domain names remain understandable without technical context while source follows its language.
**Boundary:** Language-specific naming belongs to that language's Preferences and never changes names stored in Declaration.

<br>

### Core

#### Declaration exposes one canonical logical contract

**Rule:** Every Entity Declaration publicly exposes its name, description, ordered Fields, Primary Key, Relations, Uniqueness Constraints, and Indexes. Every Field Declaration exposes name, optional description, Type, nullability, explicit Default Value presence and value, optional Sensitivity Marker, immutability, applicable constraints, and optional Value Generation. Primary Key names one Field; a Relation records its local Field, target Entity, and target Field; Uniqueness Constraints and Indexes preserve ordered participating Field names. The physical member names are selected by Model Preferences.
**Why:** One complete logical shape makes independent implementations semantically comparable.
**Boundary:** Declaration contains no runtime behaviour and chooses no technical type, table, query, index implementation, storage-specific generation, transport, or consumer behaviour.

#### Foundation converts Entities through JSON Objects

**Rule:** Foundation converts an Entity to a JSON Object — JSON text conforming to the JSON standard, with one object at its root whose keys are exactly the Entity's Field names in Declaration order — and reconstructs an Entity from that text without loss. Values preserve declared Type semantics and distinguish null, false, zero, and empty string. Reconstruction rejects malformed text and otherwise applies Principle "Construction and mutation enforce Field contracts".
**Why:** Consumers need one portable, lossless value representation.
**Boundary:** Foundation does not add Declaration metadata, nest Entities, add keys, transform sensitive values, or define domain meaning. How a consumer's language represents the decoded text is that consumer's concern.

#### Public Core contracts are separate from private helpers

**Rule:** Declaration and Foundation are public Core contracts available through their own units and through the capabilities each Entity exposes. Optional base definitions, validation mechanisms, compatibility adapters, and other helpers remain private unless this Definition explicitly promotes them.
**Why:** Consumers receive complete Model meaning without depending on realization internals.
**Boundary:** A language may realize these contracts with classes, records, functions, annotations, or another native construct; language-specific symbol and method names belong only to that language's Preferences.

<br>

### Documentation

#### Model documentation explains the complete public surface

**Rule:** Root documentation explains the complete public surface — Interface, every public Entity with its Fields and Entity Metadata, Declaration, and Foundation — together with setup, use, and verification, so that a consumer can use and verify Model without reading its source. Its order and the content of each section are selected by Model Preferences.
**Why:** Consumers can understand and verify Model without relying on private implementation.
**Boundary:** Documentation defines no other Component, exposes no private helper as contract, retains no stale meaning, and contains no real credential or secret.

<br>

### Review

#### Model conformance covers every Model contract

**Rule:** Model output is conformant only when it shows exact Entity and Field membership and order, every parameter and explicit value, complete Entity Metadata, conformance to the Model Interface Schema — Entity Export membership, Entity Collection membership, order, and correspondence, actual Entity and Declaration references, and immutability — public Declarations, lossless JSON Object round trips, and Documentation.
**Why:** These are the contracts consumers rely on; a check that omits one lets a broken Model look complete.
**Boundary:** The Review Operation establishes this; Plan and Develop check nothing. This Principle names only what Model conformance means.

#### Review observes Model through a fixed set of checks

**Rule:** Review establishes Model conformance through these observations, every one of them on every review:

- Every Target Entity has exactly one Entity Export, in Target order.
- The Entity Collection holds exactly the Entities that are exported, in the same order.
- Each Entity's Declaration matches the Target — Fields, order, Types, nullability, defaults, and metadata.
- Every Entity has an immutable id and a Boolean is_active.
- Each Entity constructs from valid values and rejects an unknown Field, a wrong Type, and a missing required value.
- Converting any Entity to its JSON Object and back returns an equal Entity.
- Decimal and datetime values keep their exact value through JSON.
- Loading Interface has no side effect.
- An unknown Type in the Target stops generation.

**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation below derives from the Principle with the same title.

### General

**Model preserves authoritative meaning**

- **Must** — preserve every explicit Target item and add only mandatory Entity Fields and approved compatible defaults.
- **Never** — remove, rename, override, or invent Target meaning without authority.

**Technology never redefines Model**

- **Must** — realize technology only while preserving exact logical meaning.
- **Never** — weaken or omit a contract because selected technology lacks native support.

**Model has one canonical Architecture**

- **Must** — preserve canonical ownership and one-way dependencies.
- **Never** — create a dependency cycle or a replacement conceptual layer.

### Interface

**Interface conforms to the Model Interface Schema**

- **Must** — conform every realization to the Model Interface Schema, with membership exactly the current Target Entities in Target order, each the actual Entity.
- **Never** — change Interface structure because Entity membership, language, package, or internal implementation changed.

### Entity

**Every Entity follows one complete structural contract**

- **Must** — preserve each Entity and supply exactly one non-nullable immutable id and one non-nullable mutable Boolean is_active, taking their remaining unstated properties from Preferences.
- **Never** — add another universal Field or reshape a Target concept.

**Fields preserve a complete value contract**

- **Must** — preserve every Field property, explicit value, constraint, order, and generation rule.
- **Never** — combine Default Value with Value Generation or silently coerce an incompatible value.

**Entity Metadata resolves completely**

- **Must** — keep structural metadata outside Fields and resolve every local and target reference.
- **Never** — accept unresolved, incompatible, repeated, or duplicate metadata or invent relationship behaviour.

**Entities remain flat and independent**

- **Must** — represent cross-Entity meaning by explicit Relation metadata.
- **Never** — nest, inherit, copy, or import another Entity's domain definition.

**Each Entity owns one public unit**

- **Must** — keep one public unit per Entity and shared infrastructure in Core.
- **Never** — place an Entity in Interface, Core, or another Entity's unit.

**Construction and mutation enforce Field contracts**

- **Must** — apply identical strict Field rules to direct construction, JSON Object construction, and mutation.
- **Never** — accept unknown Fields, implicit coercion, invalid mutation, or external Component behaviour.

**Generated identities follow their declared owner**

- **Must** — keep Auto Increment pending until its owner assigns it.
- **Never** — accept caller-supplied Auto Increment values unless Target explicitly permits them.

**Entity state adds no undeclared semantics**

- **Must** — preserve declared mutability and use JSON Object round trip as the portable reconstruction contract.
- **Never** — invent equality, ordering, hashing, copying, cloning, or merging.

**Sensitivity remains metadata**

- **Must** — preserve recognized markers and actual values while excluding sensitive values from diagnostics and artifacts.
- **Never** — protect, transform, authorize, inspect, or remap values inside Model because of a marker.

**Logical names remain exact and physical names remain deterministic**

- **Must** — preserve logical Target names and apply language-specific physical naming deterministically.
- **Never** — silently translate, pluralize, alias, or repair a collision.

### Core

**Declaration exposes one canonical logical contract**

- **Must** — expose every canonical Entity, Field, and metadata member as structured public meaning.
- **Never** — put runtime behaviour or another Component's realization choice in Declaration.

**Foundation converts Entities through JSON Objects**

- **Must** — provide lossless Entity-to-Object and Object-to-Entity conversion with exact keys and values.
- **Must** — produce and accept JSON text conforming to the JSON standard.
- **Never** — add keys or metadata, nest Entities, coerce values, or transform sensitive data.

**Public Core contracts are separate from private helpers**

- **Must** — keep Declaration and Foundation public and realization helpers private.
- **Never** — force every language to use a class or expose a helper as public contract.

### Documentation

**Model documentation explains the complete public surface**

- **Must** — document the complete public surface together with setup, use, and verification.
- **Never** — define another Component, expose private implementation, retain stale meaning, or contain a real secret.

### Review

**Model conformance covers every Model contract**

- **Must** — show every Model contract — membership, order, values, metadata, Interface Schema conformance, actual references, Declarations, round trips, and Documentation — before Model is conformant.

**Review observes Model through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
