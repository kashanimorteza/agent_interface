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

Model gives every consumer one reusable public representation of the Target's data meaning without prescribing who consumes it or how it is used.

### How It Works

Interface follows the fixed Model Interface Schema and publishes one stable EntityCatalog. The Catalog contains one EntityEntry for every Target Entity in Target order; each Entry references the actual public Entity and its actual public Declaration. Foundation supplies shared Entity-to-JSON Object and JSON Object-to-Entity conversion. Consumers use the Catalog contract and never interpret Model files, package exports, or implementation details.

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
- **Sensitivity Marker** — optional Field metadata equal to password or sensitive; it records value meaning but causes no Model-side protection or transformation.
- **Primary Key** — Entity Metadata that names id.
- **Relation** — Entity Metadata connecting one local Field to a target Entity and target Field by logical name.
- **Uniqueness Constraint** — Entity Metadata requiring one Field or an ordered combination of Fields to be unique.
- **Index** — Entity Metadata recording an access intention for one Field or an ordered combination of Fields.
- **Entity Metadata** — Primary Key, Relations, Uniqueness Constraints, and Indexes owned by an Entity rather than one Field.
- **Entity Declaration** — the complete structured public record of one Entity's name, description, ordered Fields, and Entity Metadata.
- **Field Declaration** — the complete structured public record of one Field's name, description, Type, presence meaning, Default Value, sensitivity, immutability, constraints, and Value Generation.
- **Declaration** — the public Core contract that represents Entity and Field Declarations without defining Entity behaviour.
- **Foundation** — the public Core contract that supplies shared conversion capabilities without defining domain meaning.
- **JSON Object** — the decoded, JSON-compatible key-and-value representation of one Entity; it is not encoded JSON text.
- **EntityCatalog** — the stable ordered immutable public collection through which consumers discover every current Entity.
- **EntityEntry** — one immutable Catalog member containing exact logical name, actual public Entity, and that Entity's actual public Declaration.
- **Model Interface Schema** — the Foundation structure standard that fixes EntityCatalog, EntityEntry, their capabilities, and the boundary consumers may rely on.
- **Interface** — the standard public entrypoint that realizes the Model Interface Schema and publishes EntityCatalog.
- **Deterministic Generation** — generation in which unchanged authorities and resolved technical selections produce no source or documentation difference.
- **Conformance Validation** — verification that Model input and output preserve every applicable authority and public contract.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

    Model
    ├── interface
    ├── entity/
    │   └── <entity>
    ├── core/
    │   ├── declaration
    │   └── foundation
    └── README.md

The names shown are defaults selected by Model Preferences. Responsibilities and ownership remain fixed when a selected language changes their physical casing, extension, symbol, or package representation.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes no Development Component** — Model depends on no Database, Logic, API, Presentation, or other generated Development Component.
- **Provides reusable public Entities** — any consumer discovers and uses every Entity and Declaration through the stable EntityCatalog without interpreting Model internals.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Persistence and storage** — Tables, queries, migrations, Instances, records, and storage lifecycle belong outside Model.
- **Application Behaviour** — Actions, decisions, workflows, authorization, quotas, and orchestration belong outside Model.
- **Transport** — Endpoints, requests, responses, protocols, and transport schemas belong outside Model.
- **Sensitive-value handling** — encryption, hashing, masking, redaction, authorization, and secret storage belong outside Model; Model preserves only the marker and actual value.
- **Initial and runtime data** — Initial Data and runtime records are not Model-owned meaning.
- **Consumer usage** — Model publishes reusable contracts but does not prescribe how a consumer realizes or uses them.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Model Preferences own configurable names, language, package, platform, naming, symbols, method names, technical realization, Field defaults, and documentation choices. These selections realize the following responsibilities without changing them.

### Interface

The standard package-root entrypoint that conforms to `.interface/foundation/schema/model-interface.yaml`. It publishes one ready-to-use EntityCatalog value and the immutable EntityEntry value contract. It does not publish one root symbol per Entity. Catalog membership contains every actual Entity exactly once in Target order, while the outer Interface structure remains unchanged when Entity membership or implementation changes.

### Entity

The public directory containing exactly one unit for every Entity. Each Entity exposes its own complete Declaration and the shared Foundation capabilities while remaining flat and independent of other Entity implementations.

### Core

The shared area containing public Declaration and Foundation contracts plus any private base definitions and helpers shared across Entities. Core never depends on Interface or one specific Entity.

### Declaration

The public structured contract for Entity and Field meaning. It contains no runtime behaviour and chooses no table, query, storage engine, transport, or consumer realization.

### Foundation

The public shared conversion contract for Entity-to-JSON Object and JSON Object-to-Entity construction. Text encoding and decoding remain outside Model.

### Documentation

The root README.md explains Interface, every public Entity, Declaration, Foundation, setup, use, verification, and Model-specific troubleshooting. Its filename, location, format, order, and sections are selected by Model Preferences.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Model Principle is mandatory. Model Preferences may complete an unstated compatible choice or make a rule stricter, but never override or weaken a Principle. Explicit compatible Target meaning takes precedence over a Preference.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the Architecture or Layering category that owns it.

### General

#### Model preserves authoritative meaning

**Rule:** Model preserves every Target-declared Entity, Field, parameter, explicit false, explicit null, Type, constraint, Default Value, sensitivity marker, Value Generation, Primary Key, Relation, Uniqueness Constraint, and Index. It additionally supplies only the mandatory id and is_active contract and compatible Preference defaults approved by this Definition. A Preference completes only an unstated allowed property and never removes, renames, or overrides explicit compatible Target meaning.
**Why:** One authority prevents generated convenience and package defaults from changing the domain.
**Boundary:** An explicit Target change may add, modify, rename, or remove Target-owned meaning; Model applies that change without inventing another one.

#### Model is independent and owns only its Component

**Rule:** Model depends on no other Development Component and generates, changes, verifies, documents, and removes artifacts only inside its own Component directory. Consumers use its public surface and never gain authority to change Model because their implementation lacks a capability.
**Why:** Independent ownership keeps the same Model reusable and prevents one consumer from rewriting another Component's contract.
**Boundary:** Model may use the language and package selected by its Preferences; those are Model-owned realization dependencies, not Development Component dependencies.

#### Technology never redefines Model

**Rule:** Entity and Field meaning remains understandable independently of language, package, tool, version, runtime, platform, database, and Engine. Preferences select technical realization only. Concrete dependency versions are stabilized, explicit Model meaning overrides package defaults, and a missing native capability is implemented privately only when meaning remains exact.
**Why:** Technology can change without redefining the Target's data.
**Boundary:** If selected technology cannot preserve a contract, generation reports incompatibility instead of weakening or omitting meaning.

#### Model has one canonical Architecture

**Rule:** Every realization contains the root Interface, Entity directory, Core directory, Declaration, Foundation, one unit per Entity, and root Documentation with the ownership shown in Architecture. Dependencies flow from Interface to Entity units and from Entity units to shared Core contracts; Core depends on neither Interface nor a specific Entity, and one Entity never imports another to declare a Relation.
**Why:** Stable ownership makes implementations comparable and prevents cycles.
**Boundary:** Language-required manifests, package entrypoints, annotations, inheritance from a shared private base, and similar technical files may exist without creating another conceptual layer or moving an owned responsibility.

#### Generation and evolution are deterministic

**Rule:** Unchanged Target, Definition, Preferences, and resolved technical selections produce the same ordered Model with no source or documentation difference. Regeneration classifies authoritative additions, modifications, explicit renames, and removals; updates every affected public surface together; preserves unaffected and still-declared meaning; removes only Model-owned obsolete output; and never infers rename or removal from name similarity, missing understanding, or generator limitation.
**Why:** Determinism makes reviews meaningful and protects existing meaning during evolution.
**Boundary:** Runtime-generated Entity values are not source nondeterminism. Compatibility aliases or historical versions exist only when explicit authority requires them, and Model owns no data migration.

#### Generation verifies complete conformance

**Rule:** Before publication, generation validates input completeness, uniqueness, compatibility, naming, metadata resolution, and technology support; then verifies exact Entity and Field membership and order, every parameter and explicit value, Entity Metadata, Architecture, dependencies, conformance to the Model Interface Schema, exact Catalog membership and order, actual Entity and Declaration references, Catalog capabilities and immutability, public Declarations, Foundation round trips, Documentation, source quality, and zero-diff regeneration. Disabled persistent testing requires transient verification rather than skipping it.
**Why:** Generation is complete only when observable output proves it preserved every authority and public contract.
**Boundary:** Verification observes and rejects mismatch; it never repairs ambiguity by invention or changes another Component.

#### Failure is explicit and atomic

**Rule:** Generation collects independent actionable failures when safe, identifies the affected Entity, Field, metadata item, or artifact without exposing a sensitive value, and publishes candidate output only after every required check passes. Failure preserves the last valid Model and publishes no partial result.
**Why:** A failed generation must not look complete or destroy a usable Model.
**Boundary:** Warnings are limited to meaning-neutral issues; omission, coercion, fallback, invention, or partial publication never hides an error.

#### Generated source meets the selected technology standard

**Rule:** Generated Model is installable and importable and passes applicable format, import, compile, build, lint, static type, dependency, and runtime checks without a fixable Model-owned warning. It declares only necessary dependencies and contains no dead, duplicate, incomplete, cached, compiled, machine-specific, Agent-identifying, timestamped, or narratively generated artifact.
**Why:** Correct meaning must be delivered as clean, usable source.
**Boundary:** Language-required technical artifacts do not create Model meaning, and disabled persistent testing prevents a permanent test suite rather than verification.

### Interface

#### Model Interface follows one stable Schema

**Rule:** Every realization of Interface conforms to the versioned Model Interface Schema. EntityCatalog, EntityEntry, and their capability meanings remain structurally fixed across Target Entity additions, modifications, renames, removals, languages, packages, and internal implementations. Changing that structure requires an explicit Schema version change and consumer review.
**Why:** Consumers can depend on one contract instead of reinterpreting each generated Model realization.
**Boundary:** Entity membership and Entity meaning may change under Target authority without becoming an Interface-structure change.

#### EntityCatalog publishes every actual Entity

**Rule:** Interface publishes one ready-to-use immutable EntityCatalog value that consumers never construct or populate. It contains exactly one immutable EntityEntry for every Target Entity in Target order and no other Entry. Each Entry's name is the exact logical Entity name, its entity is the actual public Entity, and its declaration is that Entity's actual public Declaration. Catalog supports entries, get by exact logical name returning Entry or null, contains by actual Entity, and declaration_of returning the actual Declaration or null.
**Why:** Complete actual references let generic consumers discover Model membership and meaning without building another registry.
**Boundary:** EntityEntry never copies, wraps, aliases, reconstructs, or translates an Entity or Declaration.

#### Interface is the only Entity discovery path and has no side effect

**Rule:** Consumers discover Entities only through EntityCatalog. Interface does not publish one root symbol per Entity. Consumers do not use wildcard exports, `__all__`, package reflection, dynamic attribute discovery, directory scanning, Entity-unit paths, or another consumer-owned registry. Loading Interface creates no Entity instance and performs no network, storage, runtime-configuration, data-creation, or other external side effect.
**Why:** One explicit discovery path remains portable and predictable for every consumer.
**Boundary:** Declaration and Foundation remain public through actual Entities and their public Core contracts. Model publishes no consumer behaviour or realization.

### Entity

#### Every Entity follows one complete structural contract

**Rule:** Every Target domain concept produces exactly one uniquely named Entity in Target order. Each Entity preserves its description and ordered Fields, carries complete Entity Metadata, has exactly one id named by its Primary Key, and has exactly one is_active. When Target leaves their properties unstated, id resolves to non-nullable immutable integer with Auto Increment and is_active resolves to non-nullable mutable Boolean with Default Value true.
**Why:** One structural contract prevents generators from reshaping domain concepts or producing unusable Entity identities.
**Boundary:** Explicit compatible Target properties take precedence. Model adds no universal Field other than id and is_active.

#### Fields preserve a complete value contract

**Rule:** Every Field name is unique within its Entity and preserves its description, declared or resolved Type, nullability, explicit Default Value presence and value, sensitivity, immutability, applicable constraints, and optional Value Generation in Target order. Absence of a Default Value differs from explicit null; one Field never has both a Default Value and Value Generation; every default and generated value satisfies the Field contract.
**Why:** Explicit value semantics prevent languages and packages from interpreting omission, null, defaults, or generation differently.
**Boundary:** Preferences complete only allowed missing properties. Invalid, incompatible, or internally contradictory values and constraints fail instead of being ignored, coerced, or replaced.

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

**Rule:** An omitted Auto Increment Field remains in an explicit pending state without becoming nullable, rejects a caller-supplied value unless Target explicitly permits one, receives its value from the owning persistence realization, and becomes immutable after assignment. A Generated Identifier such as the default uuid4 is produced during Entity creation when declared and may use another explicitly selected algorithm.
**Why:** Generation ownership prevents callers from choosing values that another realization is responsible for assigning.
**Boundary:** The pending representation may use JSON null solely to represent not-yet-generated Auto Increment state; it does not change the Field's nullability.

#### Entity state adds no undeclared semantics

**Rule:** Entity state is mutable except for immutable Fields, with id immutable after assignment or generation. Model defines no portable equality, ordering, hashing, copy, clone, merge, or reconstruction mechanism beyond its declared JSON Object round trip, and mutable Entities are not made hashable.
**Why:** Model must not invent domain behaviour from language object conventions.
**Boundary:** Language-required diagnostic representation may exist internally but is not a portable Model contract or reconstruction format.

#### Sensitivity remains metadata

**Rule:** password and sensitive are the only recognized sensitivity markers. Model preserves the actual value unchanged in Entity state and JSON Object, exposes the marker through Declaration, never encrypts, hashes, masks, redacts, authorizes, inspects, ignores, or remaps a value because of it, and never echoes a sensitive value in validation or generation diagnostics.
**Why:** Model preserves sensitivity meaning without taking ownership of protection.
**Boundary:** Generated source, Documentation, fixtures, and examples use no real credential or secret. A new marker requires explicit authority.

#### Logical names remain exact and physical names remain deterministic

**Rule:** Logical Entity and Field names, including Relation names, preserve exact case-sensitive Target spelling. Generation never translates, abbreviates, pluralizes, respells, prefixes, suffixes, or aliases them. Physical names apply the selected language's naming rules deterministically and reject unresolvable reserved-word or normalization collisions.
**Why:** Domain names remain understandable without technical context while source follows its language.
**Boundary:** Language-specific naming belongs to that language's Preferences and never changes names stored in Declaration.

### Core

#### Declaration exposes one canonical logical contract

**Rule:** Every Entity Declaration publicly exposes name, description, ordered fields, primary_key, relations, unique_constraints, and indexes. Every Field Declaration exposes name, optional description, Type, nullability, explicit Default Value presence and value, optional sensitivity, immutability, applicable constraints, and optional Value Generation. Primary Key names one Field; Relation records local_field, target_entity, and target_field; Uniqueness Constraints and Indexes preserve ordered participating Field names.
**Why:** One complete logical shape makes independent implementations semantically comparable.
**Boundary:** Declaration contains no runtime behaviour and chooses no technical type, table, query, index implementation, storage-specific generation, transport, or consumer behaviour.

#### Foundation converts Entities through JSON Objects

**Rule:** Foundation converts an Entity to a JSON Object whose keys are exactly its Field names in Declaration order and reconstructs an Entity from that decoded Object without loss. Values preserve declared Type semantics and distinguish null, false, zero, and empty string. Construction rejects malformed Objects, unknown Fields, missing Required Fields, and incompatible values without implicit coercion.
**Why:** Consumers need one portable, lossless value representation.
**Boundary:** Foundation does not encode or parse JSON text, add Declaration metadata, nest Entities, add keys, transform sensitive values, or define domain meaning.

#### Public Core contracts are separate from private helpers

**Rule:** Declaration and Foundation are public Core contracts available through their own units and through the capabilities each Entity exposes. Optional base definitions, validation mechanisms, compatibility adapters, and other helpers remain private unless this Definition explicitly promotes them.
**Why:** Consumers receive complete Model meaning without depending on realization internals.
**Boundary:** A language may realize these contracts with classes, records, functions, annotations, or another native construct; language-specific symbol and method names belong only to that language's Preferences.

### Documentation

#### Model documentation explains the complete public surface

**Rule:** Root Documentation follows the order selected by Model Preferences. Overview gives one concise Entity example; Interface explains EntityCatalog and EntityEntry and documents every Catalog member once in Target order with a complete Field table and separate Entity Metadata; Declaration shows metadata access through a Catalog Entry; Foundation shows each capability and one complete JSON Object round trip; Setup contains selected-technology steps; Use follows the Catalog public surface; Verify checks Schema conformance, membership, order, actual references, capabilities, immutability, side-effect freedom, construction, Declaration access, and round trip; Troubleshooting covers Model concerns only.
**Why:** Consumers can understand and verify Model without relying on private implementation.
**Boundary:** Documentation defines no other Component, exposes no private helper as contract, retains no stale meaning, and contains no real credential or secret.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation below derives from the Principle with the same title.

### General

**Model preserves authoritative meaning**

- **Must** — preserve every explicit Target item and add only mandatory Entity Fields and approved compatible defaults.
- **Never** — remove, rename, override, or invent Target meaning without authority.

**Model is independent and owns only its Component**

- **Must** — keep Model free of Development Component dependencies and mutate only Model-owned output.
- **Never** — let a consumer's needs authorize changes outside its own responsibility.

**Technology never redefines Model**

- **Must** — stabilize compatible technical realization while preserving exact logical meaning.
- **Never** — weaken or omit a contract because selected technology lacks native support.

**Model has one canonical Architecture**

- **Must** — preserve canonical ownership and one-way dependencies.
- **Never** — create a dependency cycle, Entity-to-Entity import, or replacement conceptual layer.

**Generation and evolution are deterministic**

- **Must** — produce zero diff from unchanged authorities and reconcile explicit changes across all affected surfaces.
- **Never** — guess a rename or removal, retain obsolete generated duplication, or own data migration.

**Generation verifies complete conformance**

- **Must** — verify meaning, metadata, Architecture, public surfaces, source quality, round trips, Documentation, and repeatability.
- **Never** — skip verification because persistent testing is disabled.

**Failure is explicit and atomic**

- **Must** — report actionable non-secret failures and publish only a fully valid candidate.
- **Never** — hide an error or replace the last valid Model with partial output.

**Generated source meets the selected technology standard**

- **Must** — produce a clean, installable, importable package that passes applicable technology checks.
- **Never** — emit unnecessary, dead, duplicate, cached, compiled, machine-specific, Agent-identifying, or timestamped output.

### Interface

**Model Interface follows one stable Schema**

- **Must** — conform every realization to the versioned Model Interface Schema while allowing Catalog membership to follow Target.
- **Never** — change Interface structure because Entity membership, language, package, or internal implementation changed.

**EntityCatalog publishes every actual Entity**

- **Must** — publish one ready immutable Catalog and one exact immutable Entry per Target Entity in Target order with its actual Entity and Declaration.
- **Never** — copy, wrap, alias, reconstruct, translate, omit, or add an Entity or Declaration.

**Interface is the only Entity discovery path and has no side effect**

- **Must** — require every consumer to discover Entities through EntityCatalog and load it without external side effects.
- **Never** — publish per-Entity root symbols or require wildcard exports, `__all__`, reflection, attribute discovery, directory scanning, internal paths, or a consumer-owned registry.

### Entity

**Every Entity follows one complete structural contract**

- **Must** — preserve each Entity and supply exactly one id and one is_active with approved defaults when unstated.
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

- **Must** — keep Auto Increment pending until its owner assigns it and make id immutable afterward.
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
- **Never** — encode text, add keys or metadata, nest Entities, coerce values, or transform sensitive data.

**Public Core contracts are separate from private helpers**

- **Must** — keep Declaration and Foundation public and realization helpers private.
- **Never** — force every language to use a class or expose a helper as public contract.

### Documentation

**Model documentation explains the complete public surface**

- **Must** — document every required section, Entity, Field, metadata contract, capability, and verification example.
- **Never** — define another Component, expose private implementation, retain stale meaning, or contain a real secret.
