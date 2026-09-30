# Database Definition

Database is the structured Development Component that persists public Entity data and provides one stable data-access gateway.

<br>

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

## Introduction

### Overview

Database enumerates every Entity through the Entity Collection published by Model Interface, derives storage structure from each actual Entity and the Declaration it exposes, and persists Entity instances through a selected active DatabaseInstance. Interface is its only public boundary. Core routes every request, and one isolated Engine unit implements the contract for each Engine used by at least one active Instance.

### Purpose

Database keeps persistence, Instance selection, and Engine integration behind one reusable boundary. Consumers select an Instance and use the published contracts without accessing configuration, Core, Engine units, connection details, or storage paths.

### How It Works

A consumer imports Interface, selects a DatabaseInstance or accepts the default, and calls an Entity Operation, Database-wide Operation, or Lifecycle Command. Core resolves the complete Instance configuration and forwards the request, with that Instance's connection, to its Engine's unit. The result returns through Core and Interface in the published form.

<br>

## Terms

- **Engine** — a declared database technology used by one or more Instances.
- **Instance** — one named database connection and storage identity, including its Engine, active state, database identity, connection values, and options.
- **DatabaseInstance** — the public enumeration whose members identify exactly the active configured Instances; it contains no connection credentials.
- **Database Configuration** — the generated runtime configuration, the sole runtime source for Engines, Instances, Settings, and Initial Data.
- **Database Interface Schema** — the versioned structure that fixes every public Database contract: the Operations and Lifecycle Commands with their inputs, effects, and results, the query vocabulary, values, results, and error meanings.
- **Database Configuration Schema** — the versioned structure that fixes the shape of the Database Configuration.
- **Interface** — the only public Database entry point.
- **Entity Operation** — an Operation scoped to one Entity.
- **Database-wide Operation** — an Operation scoped to the selected Instance rather than one Entity.
- **Lifecycle Command** — an explicit preparation command with a generated manual entry point: CreateTables, InsertInitialData, or Prepare, which runs the first two in order.
- **Filter** and **Order** — immutable condition and ordering values built from the public query vocabulary.
- **CommandResult** and **LifecycleResult** — the public results of a Database-wide Operation and of a Lifecycle Command.
- **Data** — the Engine-independent Core unit that validates, resolves, routes, and normalizes requests and results.

<br>

## Architecture

```text
Database
├── Interface         ← the only public entry point, in the shape the Database Interface Schema defines
├── Core
│   ├── Data          ← shared validation, resolution, routing, and normalization
│   ├── Tables        ← coordinates CreateTables
│   └── Initial Data  ← coordinates InsertInitialData
├── Engine            ← one unit per Engine in use
├── Entry Points      ← one manual entry point per Lifecycle Command
├── Storage           ← Database-owned persistent data, no source
├── Configuration     ← the generated Database Configuration
└── Documentation     ← the public explanation of the surface above
```

**Interface** — Interface publishes exactly the contracts the Database Interface Schema defines: the Database access surface, DatabaseInstance, every Entity Operation, Database-wide Operation, and Lifecycle Command, the query vocabulary and values, and the results. Consumers do not recreate these contracts. Interface declares and forwards behavior; it does not implement Engine work. Each Lifecycle Command is callable through Interface or its generated manual entry point; an entry point only invokes the command, and Core and the selected Engine own the work.

**Core** — Data owns shared validation, default resolution, Instance selection, routing, and result normalization for all public requests. Tables coordinates CreateTables. Initial Data coordinates InsertInitialData. Core contains no Instance-specific connection or storage implementation.

**Engine** — Engine contains exactly one unit for every Engine used by at least one active Instance, named from that Engine. Each unit implements all Entity Operations, ExecuteCommand, and the Engine capabilities required by the Lifecycle Commands, and returns raw results. Instances that use the same Engine share its unit and differ only in their connection.

**Entry Points** — one manual entry point for each Lifecycle Command. Each only invokes its command through Interface and holds no logic of its own.

**Storage** — Storage contains Database-owned persistent data and no source code. A file-backed Instance resolves its configured relative path from this Database-owned storage root, never from an installed package, a virtual environment, or a consuming Component.

**Configuration** — the generated Database Configuration, the only source Core reads at runtime.

**Documentation** — the root documentation explaining every public contract, Instance selection, the Lifecycle Commands, Initial Data, setup, use, verification, and Database-specific troubleshooting.

<br>

## Relationships

- **Consumes Model** — imports Model Interface and uses its Schema-defined Entity Collection and Entity Exports only. It uses each actual Entity and the Declaration that Entity exposes without interpreting Model internals. Model remains read-only and independently owned.

<br>

## Boundaries

- **The meaning of data — Entities, Fields, Types, and constraints** — is not Database's, because Database stores data rather than defining what it means.
- **Hashing, encryption, masking, and secret storage** — are not Database's, because they change a value rather than store it.
- **Business rules, workflows, authorization, and orchestration** — are not Database's, because they depend on how data is used, not on how it is stored.
- **Changing the structure of existing Tables** — is not Database's, because Database only creates Tables from the current Entities and stops on any difference.
- **Endpoints, requests, responses, and protocols** — are not Database's, because they are properties of moving data, not of storing it.

<br>

## Layering

Database Preferences own configurable names, language, packages, Engines, type mapping, Instance defaults, query defaults, layout, technical realization, and documentation choices; these selections realize the responsibilities in Architecture without changing them. The shape of Interface belongs to the Database Interface Schema, and the shape of the Database Configuration belongs to the Database Configuration Schema. Implementation applies them to the current Target.

<br>

## Authority

Every Database Principle is mandatory. Database Preferences may complete unstated realization choices but never weaken or replace a Principle. Explicit compatible Target values take precedence over defaults.

<br>

## Principles

Every Principle below is mandatory.

### General

#### Database owns one canonical Architecture

**Rule:** The Component contains one Interface, Core, Engine, Entry Points, Storage, the generated Database Configuration, and Documentation. Core contains Data, Tables, Initial Data, and every additional internal source unit. Engine contains one unit per Engine used by at least one active Instance. Persistent data belongs only in Storage.
**Why:** A fixed layout lets every generation place each file in the same place, so an Agent never decides structure and consumers always find the same parts.
**Boundary:** Fixed Architecture members are not renamed or relocated. No additional internal source unit is placed at the Component root, beside an Engine unit, or inside Storage.

#### Database never decides by judgment

**Rule:** Every choice that changes Database's structure, public surface, names, technology, types, or data comes only from the Target, Database Preferences, or this Definition. When none of them supplies it, Database stops and reports the missing choice through State.
**Why:** When no decision is guessed, every generation yields the same result.
**Boundary:** Internal details that change none of these are not governed by this Principle.

#### Database preserves one observable contract

**Rule:** Architecture, public contracts, Instance selection, request meaning, result meaning, routing, and ownership remain stable across languages, packages, libraries, and database technologies.
**Why:** Consumers depend on meaning, not technology; if a package or Engine could change behaviour, every technology change would break its consumers.
**Boundary:** Syntax, drivers, ORMs, query builders, sessions, connection pools, transactions, and query rendering are realization details. An incompatible technology fails generation rather than changing Database meaning.

#### Database consumes Model without owning it

**Rule:** Database imports Model Interface and reaches Entities only through its Schema-defined Entity Collection and Entity Exports. It iterates the Entity Collection and uses each actual public Entity and the complete public Declaration it exposes. It never uses wildcard or attribute discovery, scans Model directories, imports Entity-unit paths, builds another Model registry, or creates, edits, builds, tests, documents, or generates an artifact inside Model.
**Why:** One path to Entities keeps Database in step with Model and prevents a second, drifting copy of Model's meaning.
**Boundary:** A missing or incompatible Model capability is reported; Database does not repair or redefine Model.

#### Database stores values without interpreting domain meaning

**Rule:** Database persists declared Entity values and realizes declared Fields, Primary Keys, Relations, Uniqueness Constraints, Indexes, defaults, and Value Generation without adding behavior based on application meaning. Sensitivity markers and at-rest security instructions never remove, postpone, or block a Target Initial Data record.
**Why:** Storage that interprets meaning would hide or change data unpredictably; storing exactly what it receives keeps results repeatable and leaves meaning to its owner.
**Boundary:** Database does not mask, hash, encrypt, authorize, hide, or otherwise treat an Entity Field specially because it represents a password or sensitive value. It stores the concrete value supplied to it unchanged; any security transformation belongs outside Database and its absence does not block Database generation or insertion.

<br>

### Interface

#### Interface conforms to the Database Interface Schema

**Rule:** Every realization of Interface conforms to the versioned Database Interface Schema, which fixes every public contract, each Operation's and Lifecycle Command's input, effect, and result, the query vocabulary, values, results, error meanings, and what Interface never publishes. Consumers pass Entities, Fields, Instances, and vocabulary as imported values, never as strings.
**Why:** Consumers depend on one contract instead of reinterpreting each realization, and typed values are checked before any storage is touched.
**Boundary:** Interface declares and forwards public behavior; it does not select a driver or implement Engine work. Changing the structure itself requires a Schema version change.

#### Query defaults are deterministic

**Rule:** List, Count, Sum, Min, and Max accept Filters and a FilterCombination; List alone also accepts ordered Orders and a limit. An omitted FilterCombination, Order set, or limit resolves from Database Preferences; an Order without a direction uses ASCENDING. A zero or negative limit means no limit; a positive limit is the maximum returned count.
**Why:** Fixed defaults make the same call return the same result on every Instance and every generation.
**Boundary:** Supplied Orders replace the default and are applied in supplied order. Aggregate Operations do not accept Order.

<br>

### Lifecycle Commands

#### Lifecycle Commands are separate from Operations

**Rule:** CreateTables, InsertInitialData, and Prepare are public Lifecycle Commands, each with a generated manual entry point and a LifecycleResult. Prepare runs CreateTables and then InsertInitialData on the selected Instance and stops when CreateTables fails. They are not Entity Operations or Database-wide Operations.
**Why:** Preparing storage is a different act from using it; keeping them apart prevents an everyday call from changing schema or seeding data.
**Boundary:** Manual and after-generation execution invoke the same public commands and do not duplicate their logic inside an entry point.

#### CreateTables builds Tables only from Model Entities

**Rule:** CreateTables uses only the actual Entities of the Model Entity Collection and their Declarations to create the required Tables, Fields, Primary Keys, Relations, Uniqueness Constraints, and Indexes. It never reads the Target. Re-execution on matching Tables succeeds without change. A difference between an existing Table and its Declaration stops the command and is reported; it is never resolved by judgment.
**Why:** The generated Entities already carry every structural fact, so Tables follow them exactly and the same Entities always yield the same Tables.
**Boundary:** It does not copy runtime records between Instances, invent Relation cascade behavior, or alter a Declaration. Cross-Instance transfer requires a future explicit command.

#### InsertInitialData is repeatable

**Rule:** Generation copies every Target-defined Initial Data record into the shared Database Configuration. A Target value that is not concrete, including `Generate securely`, is copied as an empty string and generation continues; Database never produces a value itself, and the user fills such values later. InsertInitialData reads that complete collection, validates each record through its public Entity contract, inserts missing records, skips already-present identical records, and returns success with zero affected items only when the Target declares no Initial Data.
**Why:** Running it again must never duplicate or lose records, so preparation can be repeated safely on any Instance.
**Boundary:** A sensitivity marker, hash or encryption instruction, credential Field, or missing security processor never causes a record to be omitted or held. Database inserts the value unchanged. It does not silently update, delete, duplicate, or overwrite an existing record; conflicting Initial Data fails clearly.

#### After-generation preparation uses the default Instance

**Rule:** When enabled, generation runs Prepare on the active default Instance. Failure identifies the Instance and command and fails preparation.
**Why:** One predictable target keeps generation from touching Instances nobody asked it to prepare.
**Boundary:** Other active Instances are prepared only by explicit selection.

<br>

### Core

#### Core owns shared routing

**Rule:** Data receives each Interface request, validates public input, resolves defaults and the selected DatabaseInstance, loads its complete configuration, forwards work with that Instance's connection to its Engine unit, materializes published Entity results, and normalizes every result. Each stored row becomes an Entity through that Entity's own construction, after every stored value is converted back to its Model Type; a row that does not satisfy the Entity contract is an error and is never repaired.
**Why:** Shared validation and routing in one place make every Engine receive the same checked request and return the same normalised result.
**Boundary:** Core does not contain driver calls or Instance-specific storage behavior.

#### Changes are atomic

**Rule:** Every changing Operation and InsertInitialData completes atomically in its selected Instance or leaves no partial data change. CreateTables is atomic when supported; otherwise an incomplete state is explicitly reported as failure. Separate calls do not share a hidden transaction.
**Why:** A half-applied change leaves data that no contract describes; all-or-nothing keeps storage always in a known state.
**Boundary:** Libraries and Engines choose the technical transaction mechanism.

<br>

### Engine

#### Every Engine in use owns one complete implementation

**Rule:** Generation creates exactly one Engine unit for every Engine used by at least one active Instance and none for any other Engine. Instances of the same Engine share its unit and differ only in the connection Core passes to it. Each unit implements all Entity Operations, ExecuteCommand, and the capabilities required by the Lifecycle Commands while preserving public request, result, error, and atomicity meaning.
**Why:** Instances of one Engine work the same way, so one complete unit serves them all without duplicated code, and an Engine nobody uses leaves nothing behind.
**Boundary:** An Engine unit implements storage behavior but never defines a new public contract or shared routing.

#### Libraries own technical database mechanics

**Rule:** The selected Library and Engine own query construction, connection management, transaction mechanics, schema tooling, and driver integration. Column types are those the Model Entities produce; Database Preferences list them per Engine as the reference Review compares against.
**Why:** Proven libraries already solve these mechanics correctly; restating them here would tie the Definition to one technology.
**Boundary:** Database Definition contains no Engine-specific query map, session algorithm, pool algorithm, or ORM API.

#### Relations add no undeclared behavior

**Rule:** An Engine realizes a declared Relation as a compatible foreign key or equivalent constraint. A conflicting change is rejected atomically.
**Why:** Invented cascades or loading would change or remove data nobody asked to touch.
**Boundary:** No cascade, nested persistence, eager loading, or related-Entity mutation is invented from a Relation.

<br>

### Configuration and Storage

#### Configuration has one runtime source

**Rule:** Database Preferences define the Component contract and generation defaults. Generation produces the Database Configuration; after generation, it is the sole runtime source for Engines, complete Instances, Settings, and Initial Data. Runtime never reads Database Preferences, and runtime configuration never writes back to them.
**Why:** With one source, every run reads the same settings, and nothing changes behind the consumer's back.
**Boundary:** Regeneration may rebuild config from current Target input and Preferences; no hidden merge or second runtime source exists.

#### Every Instance is complete and valid

**Rule:** Each Instance has a unique key, name, active state, Engine, host, port, database, username, password, and options. Engine-specific validation requires applicable values and allows inapplicable values to remain empty. The default Instance exists, is active, and is published through DatabaseInstance. When an Instance definition changes in Configuration, its complete definition is replaced and revalidated; no hidden partial merge occurs.
**Why:** An incomplete Instance fails late and unclearly; validating each one fully makes failure immediate and exact.
**Boundary:** Consumers select a DatabaseInstance member; Core resolves connection values. Credentials are never members of DatabaseInstance or repeated in Operation requests.

#### Active Instances determine generated and public resources

**Rule:** Exactly active Instances become DatabaseInstance members, and exactly the Engines they use receive Engine units. Configuration loading rejects an unknown, inactive, colliding, or unresolved Instance selection.
**Why:** Public members and Engine units that match active use exactly mean every offered choice works and none is dead.
**Boundary:** Changing active membership takes effect through resolved configuration and the next generation where units must change.

#### File storage remains Database-owned and persistent

**Rule:** A file-backed Instance resolves its configured database path from Database's Storage root. The resolved path never depends on package installation, site-packages, a virtual environment, process working directory, or a consuming Component.
**Why:** A path that depends on how or where code runs would lose or scatter data; one fixed root keeps data in one place.
**Boundary:** An invalid or escaping path fails before connection. Only Database creates and manages its storage files.

#### Initial Data is shared configuration

**Rule:** Configuration contains one complete shared Initial Data collection keyed by public Entity identity. It contains every Target-defined Initial Data record, including records with credential or sensitive Fields. The same collection may be applied to any active Instance; Instance selection changes only its destination.
**Why:** One shared collection gives every Instance the same starting data and prevents copies from drifting apart.
**Boundary:** Initial Data is not Model-owned and is not duplicated in Engine units or per-Instance definitions. Generation must not replace a non-empty Target Initial Data set with an empty collection.

<br>

### Documentation

#### Documentation explains the complete public contract

**Rule:** Documentation explains active Instance selection, every public capability group, all query vocabulary, defaults, result contracts, every Lifecycle Command and its manual entry point, Initial Data, persistent storage resolution, setup, verification, and Database-specific troubleshooting with complete examples.
**Why:** Consumers use Database through its documentation; a gap or an invented feature there leads directly to wrong use.
**Boundary:** Documentation does not create behavior absent from this Definition and does not expose credentials or Engine internals.

<br>

### Review

#### Database conformance covers every Database contract

**Rule:** Database output is conformant only when it shows exact Architecture, one DatabaseInstance member per active Instance, one Engine unit per Engine in use, complete Interface publication conforming to the Database Interface Schema, valid config against its Schema, an active default Instance, Database-owned file storage resolution, complete Engine contracts, Documentation, and zero-diff regeneration.
**Why:** These are the contracts consumers rely on; a check that omits one lets a broken Database look complete.
**Boundary:** Review reads dependencies as needed but changes, generates, builds, tests, and documents only Database output. The Review Operation establishes this; Plan and Develop check nothing.

#### Review observes Database through a fixed set of checks

**Rule:** Review establishes Database conformance through these observations, every one of them on every review:

- Interface publishes exactly the public contracts of the Database Interface Schema and nothing else.
- Every Entity Operation, Database-wide Operation, and Lifecycle Command has the signature and result the Schema states, including the optional DatabaseInstance.
- Each enumeration holds exactly its Schema members.
- DatabaseInstance holds exactly one member per active configured Instance and none for an inactive one.
- A call without a DatabaseInstance runs on the configured default Instance.
- No Operation accepts an Entity name, a Field name, or any other string in place of an imported value.
- CreateTables uses only the Entities of the Model Entity Collection and their Declarations, and stops on a difference with an existing Table.
- Each Table name is exactly its Entity name, and each column name exactly its Field name.
- Each column type is the one its Engine lists for the Field's Model Type; an unlisted Type stops generation.
- Each auto-increment identity column and each constraint and index name takes exactly the form Preferences list.
- Every returned Entity is built through its own construction, and a row that breaks the Entity contract is an error.
- Prepare runs CreateTables and then InsertInitialData, and stops when CreateTables fails.
- A Target Initial Data value that is not concrete is copied as an empty string, and no value is generated.
- A missing record returns null, never an error.
- Loading Interface opens no connection and creates no data or file.

**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

## At a Glance

### General

**Database owns one canonical Architecture**

- **Must** — preserve the canonical root, Core, Engine, Entry Points, storage, configuration, and Documentation ownership.
- **Never** — place an internal source unit outside Core or its owning Engine unit, or place source code in Storage.

**Database never decides by judgment**

- **Must** — take every structural, public, naming, technology, type, or data choice from the Target, Preferences, or this Definition, and stop and report when none supplies it.
- **Never** — fill such a choice by judgment.

**Database preserves one observable contract**

- **Must** — keep Database meaning stable across languages, packages, libraries, and Engines.
- **Never** — change public behavior to accommodate a selected technology.

**Database consumes Model without owning it**

- **Must** — consume actual Entity and Declaration references only through Model Interface's Entity Collection and Entity Exports.
- **Never** — use wildcard or attribute discovery, directories, internal paths, or construct another Entity registry.
- **Never** — change, generate, build, test, or document Model output.

**Database stores values without interpreting domain meaning**

- **Must** — persist declared Entity meaning and metadata without adding application behavior.
- **Must** — keep Target Initial Data eligible for insertion regardless of sensitivity or at-rest metadata.
- **Never** — mask, hash, encrypt, authorize, or otherwise reinterpret an Entity Field because of its meaning.

<br>

### Interface

**Interface conforms to the Database Interface Schema**

- **Must** — conform every realization to the Database Interface Schema and accept only imported values where the Schema forbids strings.
- **Never** — expose Core, Engine, configuration, credentials, or storage paths, or change Interface structure without a Schema version change.

**Query defaults are deterministic**

- **Must** — resolve omitted combination, Orders, and limit from Preferences and treat a zero or negative limit as no limit.
- **Must** — preserve supplied Order sequence and restrict Order to List.

<br>

### Lifecycle Commands

**Lifecycle Commands are separate from Operations**

- **Must** — keep CreateTables, InsertInitialData, and Prepare separate from Operations and callable through Interface and manual entry points.
- **Must** — return LifecycleResult from either invocation path.

**CreateTables builds Tables only from Model Entities**

- **Must** — build Tables only from the Entities of the Model Entity Collection and their Declarations, and stop on any difference with an existing Table.
- **Never** — read the Target, alter an existing Table by judgment, copy records between Instances, or invent relationship behavior.

**InsertInitialData is repeatable**

- **Must** — copy every Target Initial Data record into config and insert the complete collection repeatably without silent overwrite, deletion, or duplication.
- **Must** — validate every Initial Data record through its public Entity contract.
- **Never** — omit or hold credential-bearing Initial Data because a security transformation is absent.
- **Never** — produce an Initial Data value itself; a value that is not concrete in the Target is copied as an empty string.

**After-generation preparation uses the default Instance**

- **Must** — run Prepare on the default Instance when enabled.
- **Never** — prepare other Instances implicitly.

<br>

### Core

**Core owns shared routing**

- **Must** — validate, resolve, route, materialize, and normalize through Core Data.
- **Must** — build every returned Entity through its own construction.
- **Never** — repair a row that does not satisfy the Entity contract.
- **Never** — put Instance-specific driver behavior in Core.

**Changes are atomic**

- **Must** — keep changing requests atomic and report incomplete schema work explicitly.
- **Never** — create a hidden transaction across separate public calls.

<br>

### Engine

**Every Engine in use owns one complete implementation**

- **Must** — generate one complete implementation unit for every Engine used by at least one active Instance and none for any other Engine.
- **Never** — define public contracts or shared routing in an Engine unit, or duplicate a unit for another Instance of the same Engine.

**Libraries own technical database mechanics**

- **Must** — delegate database mechanics to the selected Library and Engine while preserving the public contract, and keep column types equal to each Engine's listed types.
- **Never** — define an Engine-specific query, session, pool, or ORM algorithm in the general contract.

**Relations add no undeclared behavior**

- **Must** — realize declared Relations as compatible constraints.
- **Never** — invent cascade, eager loading, nested persistence, or related-Entity mutation.

<br>

### Configuration and Storage

**Configuration has one runtime source**

- **Must** — use generated config as the sole runtime source.
- **Never** — read Database Preferences at runtime or maintain a hidden second source.

**Every Instance is complete and valid**

- **Must** — validate the complete Instance definition and replace it as one unit whenever it changes in Configuration.
- **Never** — require a consumer to resend connection values with an Operation.

**Active Instances determine generated and public resources**

- **Must** — publish and generate resources from active Instances only and keep the default Instance active.
- **Never** — accept an unknown, inactive, colliding, or unresolved Instance selection.

**File storage remains Database-owned and persistent**

- **Must** — resolve file storage from the Database-owned Storage root.
- **Never** — resolve persistent storage from a package, virtual environment, working directory, or consumer.

**Initial Data is shared configuration**

- **Must** — keep one complete shared Initial Data collection containing every Target-defined record and usable by every active Instance.
- **Never** — emit an empty collection when the Target declares Initial Data.
- **Never** — put Initial Data in Model, an Instance definition, or an Engine unit.

<br>

### Documentation

**Documentation explains the complete public contract**

- **Must** — explain every public contract and its use with complete examples.
- **Never** — define new behavior or expose secrets and Engine internals.

<br>

### Review

**Database conformance covers every Database contract**

- **Must** — show Architecture, active Instance resources, Interface, config, storage, Engine completeness, Documentation, and zero-diff regeneration before Database is conformant.
- **Never** — mutate another Component during review.

**Review observes Database through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
