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
8. **[Generation Acceptance](#generation-acceptance)**
9. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Model defines flat, technology-independent Entities. Each Entity carries its own meaning, Fields, and explicit Relations without nesting another Entity.

### Purpose

Model provides standard, shared Entity definitions for use through its published surface.

### How It Works

Each Entity stands alone in its own unit. Declaration records technology-independent meaning, while Foundation provides shared behaviour. Every Model layer is public; Interface is the standard entry point for published Entities.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity** — the authoritative logical definition of one meaningful concept in the Target's domain, with an Identity that distinguishes one instance from another.
- **Field** — one named value of an Entity, with only its domain meaning, Target-declared Type, value rules, and value-generation meaning.
- **Type** — a Target-defined category of values a Field may hold.
- **Field Rule** — a declared rule for a Field value's presence, default, sensitivity marker, immutability, length, or value constraint.
- **Required Field** — a non-nullable Field with neither a Default Value nor Value Generation, whose value must therefore be supplied when an Entity is created.
- **Sensitivity Marker** — optional Field metadata whose value is either `password` or `sensitive`. It identifies a value category; generated Model runtime behaviour records and publishes the marker but does not transform or protect the value because of it.
- **Identity** — the `id` Field that distinguishes one Entity from every other Entity of the same kind.
- **Activity Field** — the required `is_active` Field on every Entity, which represents whether that Entity is active.
- **Primary Key** — Entity metadata that names the `id` Field used to identify an Entity.
- **Uniqueness Constraint** — a condition requiring one Field or a declared combination of Fields to have no duplicate value within its Entity.
- **Relation** — Entity metadata that connects one local Field to a target Field by recording the target Entity name and target Field name.
- **Index** — a declared access intention for one Field or a declared combination of Fields.
- **Entity Metadata** — structural meaning owned by an Entity rather than by one Field, including its Primary Key, Relations, Uniqueness Constraints, and Indexes.
- **Entity Declaration** — the canonical logical record of one Entity, containing its name, description, ordered Field Declarations, Primary Key, Relations, Uniqueness Constraints, and Indexes.
- **Field Declaration** — the canonical logical record of one Field's name, optional description, Type, presence semantics, Default Value, sensitivity marker, immutability, value constraints, and Value Generation.
- **Default Value** — a fixed value applied when a Field is omitted.
- **Value Generation** — a declared way to supply a Field value automatically when an Entity is created, including Auto Increment or a generated identifier.
- **Declaration** — a public Model layer that records an Entity's technology-independent data meaning and metadata without defining Entity behaviour.
- **Foundation** — a public Model layer that defines shared capabilities, including conversion of an Entity to JSON and construction of an Entity from JSON, without defining domain meaning.
- **Interface** — the public Model surface that publishes Entities for standard use.
- **Deterministic Generation** — generation in which the same Target, applicable Definitions, Preferences, and resolved technical selections produce the same ordered logical structure and no source difference when regenerated.
- **Conformance Validation** — verification before and after generation that Model input and output satisfy Target meaning, Model Principles, resolved Preferences, and the canonical public contracts.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Model
├── Interface
├── Entity
├── Core
│   ├── Declaration
│   ├── Foundation
│   └── optional shared base and helper units
└── Documentation
```

Interface and Entity are public Model layers at the package root and Entity directory respectively. Core is the shared source area containing the public Declaration and Foundation layers plus optional shared base and helper units. Documentation is the Component's explanatory artifact, not a runtime layer.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Other Components** — may use Model's public layers according to their own Definitions; Model publishes its meaning but does not prescribe how another Component consumes or realizes it.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The public Model surface that publishes Entities for standard use. The Architecture section defines the Model's canonical structure; file extensions and language-required package files follow the selected technology.

`interface` is the single standard Entity entrypoint at the Model package root. `entity/` owns only Entity-specific source, with every Entity in its own file. `core/` owns shared Model infrastructure: Declaration, Foundation, optional base Entity definitions, and any later source shared across Entities. A technical package entrypoint or manifest may also exist at the root when required by the selected language, but it does not replace `interface` or create Model meaning.

The Architecture and ownership of these layers are fixed. Model Preferences select their language-specific physical realization, such as casing, file extensions, and package entrypoints, without changing that Architecture. Declaration meaning remains independent of language, package, database, and Engine.

### Entity

A public layer containing one separate unit for each Entity.

### Declaration

A public layer that records Entity meaning and metadata without Entity behaviour:

```text
Declaration
└── Entity Declaration
    ├── Name
    ├── Description
    ├── Field Declarations
    │   └── Field Declaration
    │       ├── Name
    │       ├── Description
    │       ├── Type
    │       ├── Required and Nullability
    │       ├── Default Presence and Default Value
    │       ├── Sensitivity Marker
    │       ├── Immutability
    │       ├── Value Constraints
    │       │   ├── Length
    │       │   ├── Range
    │       │   ├── Pattern
    │       │   ├── Precision and Scale
    │       │   └── Allowed Values
    │       └── Value Generation
    │           ├── Auto Increment
    │           └── Generated Identifier
    └── Entity Metadata
        ├── Primary Key
        │   └── Field Name
        ├── Relations
        │   └── Relation
        │       ├── Local Field Name
        │       ├── Target Entity Name
        │       └── Target Field Name
        ├── Uniqueness Constraints
        │   └── Ordered Field Names
        └── Indexes
            └── Ordered Field Names
```

### Foundation

A public layer that defines shared conversion capabilities:

```text
Foundation
├── Entity-to-JSON conversion
└── JSON-to-Entity construction
```

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Model Definition Principles are mandatory. Model Preferences provide configurable defaults and conventions for unstated Model choices, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Model documentation explains its domain surface

**Rule:** Model documentation lives at the Component root in the section order selected by Model Preferences. Overview gives a concise introduction and one simple Entity example. Interface documents every Entity once in Target order, with its name, description, complete Field table, and Entity Metadata outside that table. A Field table shows name, Type, required and nullable meaning, Default Value, sensitivity marker, immutability, value constraints, Value Generation, and description. Entity Metadata shows Primary Key, each Relation's local Field and target names, Uniqueness Constraints, and Indexes. Declaration has one metadata-reading example. Foundation has one example for each capability and one complete JSON round trip. Setup contains only selected-technology steps; Use follows the standard Model public surface; Troubleshooting covers Model concerns only.

**Why:** Consumers can understand and use a Model without depending on internal implementation details.

**Boundary:** Documentation does not define another Component's behaviour, expose internal implementation as public contract, retain stale generated meaning, or contain a real credential or secret. Example syntax may vary by language while coverage and meaning remain stable.

<br>

### Each domain concept has one authoritative published Entity

**Rule:** Every meaningful Target concept has exactly one authoritative, published Entity in Model, originating in domain meaning rather than a tool or consumer and never independently redefined elsewhere.

**Why:** One authority prevents competing Entities from drifting apart.

**Boundary:** Implementation-only structures without domain meaning do not require an Entity.

<br>

### Entities follow one complete structural contract

**Rule:** Every Target-declared domain concept produces exactly one Entity, every Entity name is unique within Model, and Entity order follows Target declaration order. Each Entity preserves its name and description, contains its Field Declarations in Target order, and carries its complete Entity Metadata. Every Entity has exactly one Identity Field named `id`, and its Primary Key metadata names that Field. Every Entity also has exactly one non-nullable `is_active` Field that represents its active state through `true` and `false` values. An Entity contains only its own data meaning and metadata; shared Model behaviour remains in Foundation.

**Why:** A fixed Entity contract prevents generators from merging, splitting, reordering, or reshaping domain concepts according to a language, package, or Agent preference.

**Boundary:** A language or package may choose native syntax for the Entity but may not add, omit, merge, split, rename, or reorder Entities or move shared behaviour into their domain definitions.

<br>

### Entity metadata must resolve completely

**Rule:** Every local Field name used by Primary Key, Relation, Uniqueness Constraint, or Index metadata resolves to a Field declared by the same Entity. Every Relation target Entity name resolves to an Entity declared by Model, and its target Field name resolves within that Entity. Relation source and target Fields are compatible under the Target's Type definition. Each participating Field appears at most once within one Primary Key, Relation endpoint, Uniqueness Constraint, or Index, and duplicate metadata declarations are invalid. A generator rejects unresolved, incompatible, or duplicate Entity Metadata rather than silently changing or omitting it.

**Why:** Consumers can safely realize Entity structure only when every metadata link is complete, unambiguous, and internally consistent.

**Boundary:** Resolution validates declared structure without importing a target Entity class into a Field or adding cardinality, deletion behaviour, or other undeclared relationship meaning.

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

**Rule:** Foundation provides conversion of an Entity to JSON and construction of an Entity from JSON, without injecting Fields, metadata, constraints, or domain meaning. JSON is an object whose keys are exactly the Entity's Field names in Declaration order and whose values are current Entity values. It contains no Declaration metadata, nested Entity, or undeclared key. `null`, `false`, zero, and an empty string remain distinct. Serialization preserves each value according to the Target's declared Type semantics. An unresolved Auto Increment Field uses JSON `null` solely as its generation-pending representation and reconstructs to the same pending state; this does not redefine the Field as nullable. Sensitivity markers do not alter JSON values.

**Why:** The library has one consistent implementation of its common behaviour without imposing a shared domain structure.

**Boundary:** Foundation supplies conversion only. Declaration remains the owner of every Entity's meaning and metadata. JSON construction rejects malformed input, unknown Fields, values incompatible with Target-declared Types, and missing Required Fields; it applies the same omission, Default Value, Value Generation, nullability, and validation contract as direct Entity construction without implicit coercion. Method names and syntax come from Preferences, but round trips preserve every declared value and Type.

<br>

### Declaration records complete Entity meaning

**Rule:** Every Entity has a Declaration that records and exposes its Fields with their applicable Types, Field Rules, and Value Generation, plus the Entity Metadata that names its Primary Key, Relations, Uniqueness Constraints, and Index intentions. Each Relation associates one local Field with a target identified only by the target Entity name and target Field name; it never requires the target Entity class. A Uniqueness Constraint or Index may cover one Field or a declared combination of Fields. Declaration provides no runtime behaviour.

**Why:** One complete data meaning remains usable by consumers without coupling that meaning to a language, package, database, or Engine.

**Boundary:** Declaration does not choose a technical type, table name, query syntax, index implementation, or database-specific value-generation behaviour.

<br>

### Declaration has one canonical logical contract

**Rule:** Every implementation represents the same canonical Declaration contract regardless of language or package. An Entity Declaration contains `name`, `description`, `fields`, `primary_key`, `relations`, `unique_constraints`, and `indexes`. Each Field Declaration contains `name`, optional `description`, `type`, `nullable`, explicit Default Value presence and value, optional `sensitivity`, `immutable`, all applicable value constraints, and optional `value_generation`. A Primary Key names its local Field. Each Relation contains `local_field`, `target_entity`, and `target_field`. Each Uniqueness Constraint and Index contains its ordered participating Field names. A language or package may realize these records with its native constructs but may not omit, merge, reinterpret, or relocate their meaning.

**Why:** One logical shape makes independently generated implementations semantically comparable and exposes one complete Model contract.

**Boundary:** This Principle fixes logical members and ownership, not language syntax, class names, serialization format, or package-specific representation. An inapplicable optional value remains explicitly absent; it is not replaced with invented meaning.

<br>

### Declaration preserves every defined parameter

**Rule:** Generation and regeneration preserve every Target-declared Entity, Field, parameter, explicit `false`, explicit `null`, constraint, Default Value, sensitivity marker, Value Generation, Primary Key, Relation, Uniqueness Constraint, and Index. Reorganizing Declaration ownership or changing its technical realization never removes or changes existing meaning.

**Why:** Structural improvement must not cause data-model information to disappear or silently change.

**Boundary:** A parameter may be removed or semantically changed only by an explicit Target change; implementation preference, package limitation, or generator convenience is not authority to do so.

<br>

### Structural metadata belongs to the Entity

**Rule:** Primary Key, Relation, Uniqueness Constraint, and Index declarations belong to Entity Metadata outside Field declarations. A Field declaration contains only information about the value that Field stores. Entity Metadata refers to participating local Fields by name; a Relation additionally records only its target Entity name and target Field name. Model exposes this metadata as structured public meaning without prescribing how another Component uses or realizes it.

**Why:** Separating value meaning from Entity structure keeps Fields focused, avoids coupling a Field to another Entity class, and gives Model one explicit structural contract.

**Boundary:** Value-specific rules such as Type, nullability, Default Value, sensitivity marker, immutability, length, range, pattern, precision, scale, allowed values, and Value Generation remain with the Field. Structural metadata may name Fields but is never embedded in them.

<br>

### Model publishes all layers

**Rule:** Interface, Entity, Declaration, and Foundation are public Model layers. Interface is the standard Entity entry point and publishes exactly the actual definitions of every Target-declared Entity in Target order, with no missing, additional, copied, string-named, aliased, helper, or internal symbol. Declaration and Foundation remain available from their own public units and are not re-exported through Interface. Loading Interface creates no Entity instance and performs no network, storage, runtime-configuration, data-creation, or other external side effect.

**Why:** Every Model concern remains available while Interface provides one consistent route for standard Entity use.

**Boundary:** Preferences select the physical Interface name and path. When a language lacks explicit exports, generation uses its conventional public entrypoint while preserving the same published set. Internal Entity implementation may change without changing Interface while its public contract remains unchanged.

<br>

### Declaration preserves structured Field meaning

**Rule:** Declaration preserves each Field's Target-declared Type, presence semantics, Default Value, optional sensitivity marker (`password` or `sensitive`), immutability, and every Target-declared restriction as usable structured meaning, including applicable value range, length, pattern, precision, scale, allowed values, or comparable constraint. A Default Value is fixed; Value Generation creates a value when an Entity is created. One Field never declares both.

**Why:** Structured meaning preserves the same domain restriction more reliably than descriptive prose alone.

**Boundary:** Declaration does not impose a fixed vocabulary or representation for a constraint that the Target does not declare.

<br>

### Fields follow one complete value contract

**Rule:** Every Field has a name unique within its Entity and preserves its description, Target-declared Type, nullability, explicit Default Value presence and value, optional sensitivity marker, immutability, applicable value constraints, and optional Value Generation. Nullability states only whether the Field may hold `null`. Absence of a Default Value is distinct from a Default Value explicitly equal to `null`. A Field is required when it is non-nullable and has neither a Default Value nor Value Generation. One Field never has both a Default Value and Value Generation. Field order follows Target declaration order.

**Why:** Explicit and separate value semantics prevent languages and packages from interpreting omission, `null`, defaults, or generated values differently.

**Boundary:** A language or package may express the contract with its native syntax but may not add, remove, rename, reorder, or change a Field's meaning. Primary Key, Relation, Uniqueness Constraint, and Index information is Entity Metadata and never part of a Field Declaration.

<br>

### Field constraints preserve Target meaning

**Rule:** Every Default Value and value constraint preserves the Target-declared value and conforms to the Target's Field definition. An explicit `null` Default Value requires a nullable Field, and every non-null Default Value satisfies the Field's declared Type and value constraints. A generator rejects an incompatible or internally invalid default or constraint rather than silently ignoring, coercing, or replacing it.

**Why:** A constraint has portable meaning only when its accepted value domain is clear and consistent.

**Boundary:** This Principle validates declared constraints; it does not invent a constraint, normalize a domain value, or prescribe package-specific validation syntax.

<br>

### Entity and Relation identifiers express domain meaning

**Rule:** Every logical Entity and Field name, including names recorded by a Relation, is the exact case-sensitive Target name. Generation never translates, abbreviates, pluralizes, respells, prefixes, suffixes, or aliases that name unless Target explicitly declares the change. Physical symbols, files, and modules deterministically apply the casing standard selected by Preferences without changing names stored in Declaration. A reserved word uses the language's standard escaping; if no meaning-preserving escape exists, generation reports the conflict. Distinct logical names that collide after physical naming are invalid.

**Why:** Domain-oriented names keep Entity meaning understandable without technical context.

**Boundary:** Preferences define physical casing and the configured names of Interface, Declaration, Foundation, their paths, and Foundation methods. Package, framework, table, or consumer terminology never enters a logical name. Internal helpers describe their private responsibility and never leak through the public surface.

<br>

### Model remains separate from external concerns

**Rule:** Model owns logical Entities only; project records, storage operations, transport, workflow orchestration, and platform operation belong to their respective Components.

**Why:** A narrow boundary keeps Model reusable and protects domain meaning.

**Boundary:** Other Components may use Model data without transferring ownership of their concerns to Model.

<br>

### Entities are flat and use explicit Relations

**Rule:** Every Entity remains flat and independently understandable. When one of its Fields relates to another Entity, Model records that connection as an explicit Relation in Entity Metadata rather than nesting either Entity inside the other or attaching the target Entity class to the Field.

**Why:** Flat Entities prevent hidden structural coupling while explicit Relations preserve the Target's domain connections.

**Boundary:** A Relation does not create nesting, inheritance, copied Fields, shared ownership, or an object-valued Field between Entities.

<br>

### Each Entity stands in its own unit

**Rule:** Every Entity has exactly one public file of its own inside the `entity` directory. Content used by exactly one Entity remains in that Entity file. No Entity definition is placed in `core`, `interface`, or another Entity file.

**Why:** One Entity per unit keeps domain boundaries visible and independently changeable.

**Boundary:** Preferences define language casing and extensions; this Principle fixes the minimum directories, root Interface location, one-file-per-Entity structure, and ownership.

<br>

### Model has one canonical Architecture

**Rule:** Every implementation contains a root `interface` file, a `core` directory, an `entity` directory, and Model documentation at the Component root. `core` contains the Declaration file, Foundation file, every optional base Entity definition, and every additional unit shared across Entities. `entity` contains exactly one file per Entity and no shared infrastructure. This Architecture and ownership remain constant across languages and packages. Model Preferences select language casing, extensions, concrete class names, and language-required package entrypoints without moving these responsibilities.

**Why:** A stable Architecture makes generated Model Components recognizable and comparable without forcing one language's filesystem conventions onto another.

**Boundary:** Language-required package, build, manifest, or entrypoint files are allowed at their conventional locations but do not replace root `interface`, create a conceptual Model layer, or relocate owned meaning. Private helpers used by one Entity remain in its Entity file. Shared metadata helpers, shared behaviour helpers, base classes, and other cross-Entity infrastructure remain under `core` with the most specific owner available.

<br>

### Model dependencies flow in one direction

**Rule:** Root `interface` depends on and publishes files from `entity`. Entity files may depend on units from `core`. Relation metadata uses names, so Entity files never depend on or import one another to declare a Relation. No `core` unit depends on or imports `interface` or a specific Entity. No Model dependency forms a cycle. Interface publishes only Entities; Declaration and Foundation remain directly available through their public files under `core`.

**Why:** One dependency direction prevents import cycles, keeps Relations technology-independent, and lets every Entity remain independently understandable.

**Boundary:** A language may use inheritance, composition, annotations, decorators, code generation, or another native mechanism to realize an allowed dependency, but the ownership and direction do not change.

<br>

### Model generation is deterministic and idempotent

**Rule:** The same Target, applicable Definitions, Preferences, and resolved language, package, and version selections produce the same ordered Model structure. Regenerating from unchanged inputs produces no source or documentation difference and no duplicate declaration or artifact. Entities, Entity units, Interface exports, and documentation entries follow Target Entity order. Fields follow Target Field order. Relations are ordered by local Field position, then target Entity name and target Field name. Uniqueness Constraints and Indexes preserve participating Field order and are ordered by their participating local Field positions, with Field names as a stable tie-breaker. Sections within a generated artifact use one stable order.

**Why:** Stable generation makes reviews meaningful, prevents Agent-specific churn, and lets unchanged understanding reproduce unchanged output.

**Boundary:** Formatting follows the resolved language standard without changing logical order. Runtime-generated Entity values are not generated-source nondeterminism. Generated source and documentation never contain an execution timestamp, random source identifier, machine-specific path, Agent identity, or other environment-dependent content unless the Target explicitly requires that content.

<br>

### Regeneration reconciles without losing meaning

**Rule:** Regeneration compares the current generated Model with current authorities, updates only affected realization, and preserves every still-declared parameter and meaning. It neither accumulates obsolete duplicates nor rewrites unaffected logical structure. A generated artifact may be removed only when current authority explicitly removes its owned meaning or relocates that meaning within the canonical Architecture, and the resulting Model must still expose every currently declared item. Changing a language, package, or physical layout changes realization only, never Declaration meaning.

**Why:** Reconciliation keeps generated output current while protecting existing Model information from accidental loss.

**Boundary:** An explicit authoritative removal is applied; preservation does not retain meaning that the Target intentionally removed. Unowned human content is not treated as generated content or silently overwritten.

<br>

### Model generation validates input and output conformance

**Rule:** Before generation, Model validates that every input Entity, Field, Target-declared Type, value rule, and Entity Metadata item is complete, compatible, uniquely identifiable, and resolvable. After generation, Model compares the output with Target and verifies exact Entity membership and order; every Entity and Field name, description, order, parameter, explicit value, and rule; Identity and Primary Key integrity; Relation, Uniqueness Constraint, and Index resolution; Target Type and constraint compatibility; canonical Architecture and dependency direction; exact Interface publication; readable public Declarations; and documentation agreement with the public Model. Missing, additional, reordered, unresolved, incompatible, or changed meaning fails conformance.

**Why:** Generation is complete only when the result proves that it preserves its authorities and public contracts.

**Boundary:** Conformance validation observes and verifies generated output; it does not repair ambiguous Target meaning by invention or weaken a rule to accommodate a package.

<br>

### Model verifies realization and repeatability

**Rule:** Model uses the resolved language and package tools to format and perform every applicable import, compile, build, lint, or static type check required to establish that generated source is usable. It verifies Entity-to-JSON and JSON-to-Entity reconstruction without loss for every Entity and declared value kind. It then regenerates from unchanged inputs and verifies zero source and documentation difference. Verification may run transiently when Model Preferences disable a persistent test suite, and transient verification does not add testing files or capabilities to generated source.

**Why:** Logical comparison alone cannot reveal unusable source, broken public access, conversion loss, or nondeterministic regeneration.

**Boundary:** Only checks applicable to the resolved technology are required. Disabled persistent testing prevents generated test artifacts, not conformance verification.

<br>

### Entity construction and mutation enforce Field contracts

**Rule:** Direct Entity construction accepts only declared Fields and applies the same validation as JSON construction. It rejects unknown Fields, missing Required Fields, `null` for a non-nullable Field, values incompatible with Target-declared Types, and violated value constraints. Omitted nullable Fields without a Default Value become `null`; an omitted Field with a Default Value receives that exact value; an omitted Field with Value Generation follows its declared generation. Explicit `false`, zero, empty string, and `null` are supplied values and are never replaced by a default. Generated Identifier is produced at Entity creation. Auto Increment is not required as construction input and may remain in an explicit not-yet-generated state until its selected realization assigns it, without redefining the Field as nullable. A supplied value for a generated Field is accepted unless Target explicitly forbids it, and every supplied or generated value still satisfies the Target-declared Field definition and constraints.

**Why:** One construction contract prevents package-specific omission, coercion, and default behaviour from changing Entity values.

**Boundary:** Entity construction performs no storage, network, business, workflow, or orchestration operation. A package may use native validation machinery, but validation outcome and preserved values follow this contract.

<br>

### Entity state adds no undeclared domain semantics

**Rule:** An Entity is mutable except for Fields declared immutable. An immutable Field, including `id` after its value is assigned or generated, cannot change. Assignment to a mutable Field revalidates Type, nullability, and value constraints; a failed assignment leaves the previous value unchanged. Model defines no portable domain equality, ordering, hashing, copy, clone, or merge semantics unless Target explicitly declares them. Mutable Entities are not made hashable by generation. JSON is Model's only portable value representation; package `repr`, `toString`, or equivalent diagnostic representation is not a Model contract and is never used for reconstruction.

**Why:** Model enforces declared state rules without inventing identity comparison or utility behaviour that belongs to no Target meaning.

**Boundary:** Language-required object behaviour may exist internally but does not become declared domain meaning or a public cross-language guarantee.

<br>

### Sensitivity remains metadata without value handling

**Rule:** `password` and `sensitive` remain structured Field markers. Generated Model runtime code does not encrypt, hash, mask, redact, authorize, inspect, or transform a value because of its marker, and the marker does not alter Type, nullability, defaults, equality, or validation. JSON preserves the actual value unchanged. Declaration publicly exposes the marker. Runtime validation and generator diagnostics identify the Entity and Field but never echo a sensitive value; generated source, documentation, fixtures, and examples contain no real credential or secret and use non-secret placeholders when a value is necessary. An unknown marker fails validation rather than being ignored or converted.

**Why:** Model preserves sensitivity meaning without taking ownership of protection mechanisms, while its own generation process avoids embedding sensitive values.

**Boundary:** Model produces no dedicated logging capability or security guarantee for package-native diagnostic representations. A new marker requires explicit Target meaning and an updated Model contract.

<br>

### Technology realizes Model without redefining it

**Rule:** Model Preferences alone select language, package, version policy, casing, paths, and package-specific realization. A `latest-compatible` or ranged selection resolves to a concrete compatible version and is stabilized in the selected technology's dependency or lock metadata; unchanged generation reuses that resolution. Generation checks package capabilities against every Model contract. Missing native capability may be supplied by private Model-owned implementation when meaning is preserved exactly; otherwise generation reports incompatibility. Explicit Model meaning overrides package defaults. Native Types, annotations, decorators, base classes, adapters, and helpers remain realization details and do not replace Declaration meaning or leak as new public Model concepts.

**Why:** Preferences allow technology to vary while Definition keeps generated Models semantically equivalent.

**Boundary:** Generation adds only necessary dependencies and uses the technical Skill named by Preferences only to guide realization. A noncritical unstated choice follows stable professional judgment and is recorded with implementation; a missing choice that changes public Model meaning requires Human direction.

<br>

### Generation failures are explicit and atomic

**Rule:** Generation validates as much independent input as practical before publication and reports actionable issues with the affected Entity, Field, metadata item, and violated rule. Duplicate names, unsupported Types, incompatible constraints or defaults, unresolved or invalid Entity Metadata, naming collisions, dependency cycles, inability to preserve meaning, output mismatch, and failed realization checks are errors. Generation never hides an error by omission, coercion, fallback, or invented meaning. Warnings are limited to issues that cannot affect Model meaning or public contract. Independent errors are collected in one run when safe, and sensitive values never appear in diagnostics.

**Why:** Explicit diagnostics make incompatibility correctable without leaving a deceptively successful Model.

**Boundary:** Generation stages candidate output and publishes it only after every acceptance check succeeds. Failure preserves the last valid output and publishes no partial artifact. A disabled runtime error-handling capability does not disable generator diagnostics or conformance failure.

<br>

### Model evolution follows explicit authority

**Rule:** Regeneration classifies current authoritative changes as additions, modifications, explicit renames, or removals. Absence caused by incomplete understanding or generator limitation is never treated as removal. Rename is recognized only when authority states it; otherwise removal and addition are separate changes. A change to Type, nullability, Default Value, Value Generation, constraint, sensitivity, or Entity Metadata is a public meaning change. Every affected Entity, Declaration, Interface publication, Foundation behaviour, and documentation entry updates together, and dependent metadata is re-resolved. Compatibility aliases or historical versions are created only by explicit authority.

**Why:** Explicit evolution prevents guessed renames, accidental deletion, and mixed old and new contracts.

**Boundary:** Physical casing, path, language, or package changes are realization changes only. Model owns no data or storage migration and keeps no undeclared historical contract. Explicit removal eliminates the owned generated meaning everywhere only after the replacement output passes acceptance.

<br>

### Generated source and package meet selected technology standards

**Rule:** Generated source is formatted and passes every applicable import, compile, build, lint, and static type check of the selected technology without a fixable warning in Model-owned code. The package installs and imports by the language-standard mechanism, declares only necessary dependencies, exposes public Type information, and uses valid manifest, lock, entrypoint, and package-marker files. Source contains no unused import, dead or duplicate code, incomplete artifact, generated cache, bytecode, build output, absolute machine path, Agent identity, execution timestamp, or narrative comment about generation. Public and private symbols are explicit, internal documentation agrees with Declaration, encoding and line endings are consistent, and source runs on the selected runtime version.

**Why:** A semantically correct Model must also be a clean, usable package in its chosen technology.

**Boundary:** Language-required technical files do not create Model meaning. When persistent testing is disabled, generation creates no permanent test suite but still runs transient acceptance checks. An unavoidable external dependency warning is distinguished from a warning caused by generated Model source.

<br>

<!--------------------------------------------------------------------------------- Generation_Acceptance --->
## Generation Acceptance

Model generation is complete only when every applicable gate passes:

1. **Authority** — current Target, Model Definition, and Model Preferences were used; memory, old output, and Agent preference did not replace them.
2. **Preservation** — no declared Entity, Field, parameter, explicit value, constraint, or Entity Metadata was lost, and no undeclared meaning was added.
3. **Entities** — Entity membership, order, names, descriptions, `id` identities, required `is_active` Fields, Field ownership, and exactly one file per Entity under `entity/` match Target.
4. **Fields** — Field membership, order, Type, nullability, required meaning, Default Value presence and value, sensitivity, immutability, constraints, Value Generation, and description match Target.
5. **Entity Metadata** — Primary Keys, Relations, Uniqueness Constraints, and Indexes are outside Fields, complete, unique, compatible, and fully resolved.
6. **Declaration** — every canonical member is publicly readable and no language or package limitation removed or changed meaning.
7. **Interface** — exactly the Target Entities are published in Target order with no helper, alias, copy, internal symbol, or load side effect.
8. **Foundation** — direct construction and JSON round trips preserve all Entity values and their Target-declared Type semantics, including `null`, `false`, zero, and empty string.
9. **Architecture** — root `interface`, `core/`, `entity/`, Declaration, Foundation, optional base definitions, helpers, Entity files, and documentation have canonical ownership with no Entity-to-Entity import or dependency cycle.
10. **Naming** — logical names match Target, physical names match Preferences, and no reserved-word or casing collision remains.
11. **Technology** — language, package, concrete version resolution, runtime, dependencies, and realization match Preferences without semantic loss.
12. **Documentation** — generated documentation matches Interface and Declaration, contains no stale or additional meaning, and contains no real secret.
13. **Source quality** — applicable format, import, compile, build, lint, static type, installation, and runtime checks pass with no fixable Model-owned warning.
14. **Repeatability** — unchanged regeneration produces zero source and documentation diff and leaves no duplicate or stale generated artifact.
15. **Publication** — candidate output replaces prior output only after all gates pass; failure leaves the prior valid Model intact and is never reported as completion.
16. **Evidence** — a concise result identifies every check group and actionable failure location without exposing a sensitive value.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Model documentation explains its domain surface**

- **Must** — keep root documentation in configured section order; document every Entity once in Target order with a complete Field table and separate Entity Metadata.
- **Must** — give the required Overview, Declaration, Foundation, Setup, Use, and Troubleshooting content with technology-appropriate syntax and stable meaning.
- **Never** — define another Component, expose internals as public contract, retain stale meaning, or include a real credential or secret.

**Each domain concept has one authoritative published Entity**

- **Must** — Define and publish each meaningful Target concept once.
- **Never** — Create competing or implementation-only Entities.

**Entities follow one complete structural contract**

- **Must** — create exactly one uniquely named Entity for each Target domain concept and preserve Entity and Field order from Target.
- **Must** — preserve each Entity's name, description, Fields, complete Entity Metadata, exactly one `id` Identity named by its Primary Key metadata, and exactly one non-nullable `is_active` Field representing its active state.
- **Must** — keep shared Model behaviour in Foundation.
- **Never** — add, omit, merge, split, rename, or reorder Entities because of a language, package, or Agent preference.

**Entity metadata must resolve completely**

- **Must** — resolve every local metadata Field within its Entity and every Relation target Entity and target Field within Model.
- **Must** — require compatible Relation endpoint Types and reject repeated participating Fields or duplicate metadata declarations.
- **Never** — silently change or omit unresolved, incompatible, or duplicate Entity Metadata.

**Model preserves explicit Target meaning**

- **Must** — Preserve explicit Target Fields, constraints, defaults, and sensitivity markers.
- **Never** — Invent or override Target meaning.

**Logical Model meaning is independent of implementation technology**

- **Must** — Keep Entity meaning understandable without a language, package, database, Engine, runtime, or platform.
- **Never** — Let a technical realization redefine logical meaning.

**Foundation provides shared Model behaviour**

- **Must** — use Foundation for Entity-to-JSON conversion and JSON-to-Entity construction with exact Field keys in Declaration order and the Target-declared Type semantics.
- **Must** — preserve `null`, `false`, zero, empty string, and every Target-declared value across round trips.
- **Must** — reject malformed input, unknown Fields, values incompatible with Target-declared Types, and missing Required Fields while applying the direct-construction omission contract.
- **Never** — let Foundation define domain meaning, Fields, Entity Metadata, nested Entities, undeclared keys, or implicit coercion.

**Declaration records complete Entity meaning**

- **Must** — record and expose every Entity's Fields, Types, Field Rules, Value Generation, Primary Key, Relations, Uniqueness Constraints, and Index intentions in Declaration.
- **Must** — identify each Relation's local Field, target Entity name, and target Field name without requiring a target Entity class; allow declared composite Uniqueness Constraints and Indexes.
- **Never** — put runtime behaviour or technology-specific storage choices in Declaration.

**Declaration has one canonical logical contract**

- **Must** — expose `name`, `description`, `fields`, `primary_key`, `relations`, `unique_constraints`, and `indexes` for every Entity Declaration.
- **Must** — expose every Field's name, description, Type, nullability, Default Value presence and value, sensitivity marker, immutability, value constraints, and Value Generation.
- **Must** — represent each Relation with `local_field`, `target_entity`, and `target_field`; represent each Primary Key, Uniqueness Constraint, and Index with participating Field names.
- **Never** — omit, merge, reinterpret, or relocate canonical Declaration meaning because of a language or package realization.

**Declaration preserves every defined parameter**

- **Must** — preserve every existing Target-declared Entity, Field, parameter, explicit value, rule, and Entity Metadata item during generation and regeneration.
- **Never** — remove or change declared meaning without an explicit Target change.

**Structural metadata belongs to the Entity**

- **Must** — keep Primary Key, Relations, Uniqueness Constraints, and Indexes in Entity Metadata and refer to their participating Fields by name.
- **Must** — expose Entity Metadata as complete structured public meaning without prescribing consumer realization.
- **Never** — embed structural metadata or a target Entity class in a Field declaration.

**Model publishes all layers**

- **Must** — keep Interface, Entity, Declaration, and Foundation public; publish exactly the actual Target Entity definitions in Target order through Interface.
- **Must** — keep Declaration and Foundation available through their own units and keep Interface loading free of external side effects or instance creation.
- **Never** — publish copied, string-named, aliased, helper, internal, additional, or non-Entity symbols through Interface.

**Declaration preserves structured Field meaning**

- **Must** — Keep each Target-declared Field Type, rule, Default Value, Value Generation, sensitivity marker (`password` or `sensitive`), immutability, and restriction available as structured public meaning.
- **Must** — Keep Default Value and Value Generation mutually exclusive for one Field.
- **Never** — Invent a constraint or force one constraint representation.

**Fields follow one complete value contract**

- **Must** — keep every Field name unique within its Entity and preserve description, Type, nullability, Default Value presence and value, sensitivity marker, immutability, value constraints, and Value Generation in Target order.
- **Must** — distinguish absence of a Default Value from an explicit `null` Default Value; treat a non-nullable Field without a Default Value or Value Generation as required.
- **Never** — give one Field both a Default Value and Value Generation, or put Primary Key, Relation, Uniqueness Constraint, or Index metadata in its declaration.
- **Never** — add, remove, rename, reorder, or change a Field because of language or package conventions.

**Field constraints preserve Target meaning**

- **Must** — require every Default Value to satisfy nullability, the Target-declared Type, and value constraints.
- **Must** — reject incompatible or internally invalid defaults and constraints.
- **Never** — silently ignore, coerce, replace, or invent a Default Value or Field constraint.

**Entity and Relation identifiers express domain meaning**

- **Must** — preserve exact case-sensitive logical names and apply configured physical casing deterministically without changing Declaration names.
- **Must** — use standard language escaping for reserved words and reject unresolvable reserved-word or physical-name collisions.
- **Never** — translate, abbreviate, pluralize, respell, prefix, suffix, or alias a logical name without explicit Target authority.
- **Never** — use package, framework, table, consumer, or tool terminology in a logical Entity, Field, or Relation identifier.

**Model remains separate from external concerns**

- **Must** — Keep Model focused on logical Entities.
- **Never** — Own records, storage operations, transport, workflow orchestration, or platform operation.

**Entities are flat and use explicit Relations**

- **Must** — Keep every Entity flat and record every Target-declared cross-Entity connection as Entity-level Relation metadata.
- **Never** — Nest, inherit, or copy one Entity into another.

**Each Entity stands in its own unit**

- **Must** — keep each Entity in exactly one public file under `entity` and keep its private content in that file.
- **Never** — put an Entity definition in `core`, `interface`, or another Entity file.

**Model has one canonical Architecture**

- **Must** — provide root `interface`, `core/`, `entity/`, and root documentation; keep Declaration, Foundation, optional base Entity definitions, and cross-Entity infrastructure in `core`.
- **Must** — keep exactly one Entity file per Entity in `entity`, Entity-private helpers in that file, and shared helpers under their most specific owner in `core`.
- **Never** — let technical files replace `interface`, create a conceptual layer, move shared infrastructure into `entity`, or move Entity definitions into `core`.

**Model dependencies flow in one direction**

- **Must** — direct dependencies from root `interface` to `entity` files and from `entity` files to `core` units only.
- **Must** — keep `core` independent of root `interface` and specific Entities and keep Interface limited to publishing Entities.
- **Never** — import one Entity from another to declare a Relation or create a dependency cycle.

**Model generation is deterministic and idempotent**

- **Must** — produce no source or documentation difference when unchanged authorities and resolved technical selections are regenerated.
- **Must** — order Entities, units, Interface exports, documentation entries, Fields, Relations, Uniqueness Constraints, Indexes, and artifact sections by the declared canonical rules.
- **Never** — duplicate generated content or emit timestamps, random source identifiers, machine paths, Agent identity, or other undeclared environment-dependent content.

**Regeneration reconciles without losing meaning**

- **Must** — update affected realization while preserving every still-declared parameter and leaving unaffected logical structure unchanged.
- **Must** — remove generated artifacts only after an authoritative removal or canonical relocation and verify that all current meaning remains exposed.
- **Never** — let a language, package, version, or layout change alter Declaration meaning or silently overwrite unowned human content.

**Model generation validates input and output conformance**

- **Must** — validate input completeness, uniqueness, compatibility, and resolution before generation.
- **Must** — compare generated Entities, Fields, parameters, metadata, Architecture, dependencies, Interface, public Declarations, and documentation with current authorities after generation.
- **Never** — accept missing, additional, reordered, unresolved, incompatible, or changed Model meaning.

**Model verifies realization and repeatability**

- **Must** — run every applicable formatter, import, compile, build, lint, or static type check supplied by the resolved technology.
- **Must** — verify lossless JSON reconstruction for every Entity and declared value kind and verify zero diff after unchanged regeneration.
- **Must** — use transient verification without generating a persistent test suite when testing capability is disabled.
- **Never** — treat disabled persistent testing as permission to skip conformance verification.

**Entity construction and mutation enforce Field contracts**

- **Must** — apply identical direct and JSON construction rules for declared Fields, required values, nullability, defaults, generation, Types, and constraints.
- **Must** — preserve explicit false-like and null values; generate omitted values only as declared; represent unresolved Auto Increment without redefining nullability.
- **Never** — accept unknown Fields, invalid values, implicit coercion, or perform external Component behaviour during construction.

**Entity state adds no undeclared domain semantics**

- **Must** — enforce immutable Fields and revalidate mutable assignment atomically; make `id` immutable after assignment or generation.
- **Must** — use JSON as the only portable Model value representation.
- **Never** — invent domain equality, ordering, hashing, copy, clone, merge, or reconstruction semantics.

**Sensitivity remains metadata without value handling**

- **Must** — expose only the recognized sensitivity marker and keep its actual value unchanged in Model and JSON.
- **Must** — omit sensitive values from runtime validation and generator diagnostics and use no real credential or secret in generated artifacts or examples.
- **Never** — encrypt, hash, mask, redact, authorize, transform, ignore, or remap a value or marker inside generated Model runtime behaviour.

**Technology realizes Model without redefining it**

- **Must** — select technology only from Preferences, stabilize concrete dependency versions, verify capability coverage, and let explicit Model meaning override package defaults.
- **Must** — keep package constructs and private compatibility helpers as realization details and add only necessary dependencies.
- **Never** — change public meaning, expose a package detail as a Model concept, or continue when selected technology cannot preserve the contract.

**Generation failures are explicit and atomic**

- **Must** — report actionable, non-secret diagnostics for every safely collectible independent error and reserve warnings for meaning-neutral issues.
- **Must** — stage and validate candidate output before publication and preserve the last valid Model on failure.
- **Never** — hide failure through omission, coercion, fallback, invention, partial publication, or false completion.

**Model evolution follows explicit authority**

- **Must** — distinguish authoritative additions, modifications, explicit renames, and removals; update all affected Model surfaces together and re-resolve metadata.
- **Must** — treat Type, presence, default, generation, constraint, sensitivity, and Entity Metadata changes as public meaning changes.
- **Never** — infer removal or rename from incomplete understanding, generator limitation, or name similarity; create compatibility aliases without authority; or own data migration.

**Generated source and package meet selected technology standards**

- **Must** — produce an installable and importable package that passes applicable format, compile, build, lint, static type, dependency, and runtime checks without fixable Model-owned warning.
- **Must** — keep manifests, locks, entrypoints, markers, public Types, encoding, line endings, dependencies, and internal documentation valid and consistent.
- **Never** — emit dead, duplicate, incomplete, cached, compiled, environment-dependent, Agent-identifying, timestamped, or narratively generated source content.
