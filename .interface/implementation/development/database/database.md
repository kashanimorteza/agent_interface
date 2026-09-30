# Database Definition

Database is the structured Development Component that persists public Entity data and provides one stable data-access gateway.

<br>

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

## Introduction

### Overview

Database enumerates every Entity through the Entity Collection published by Model Interface, derives storage structure from each actual Entity and the Declaration it exposes, and persists Entity instances through a selected active DatabaseInstance. Interface is its only public boundary. Core routes every request, and one isolated Engine file implements the contract for each active Instance.

### Purpose

Database keeps persistence, Instance selection, and Engine integration behind one reusable boundary. Consumers select an Instance and use the published contracts without accessing configuration, Core, Engine files, connection details, or storage paths.

### How It Works

A consumer imports Interface, selects a DatabaseInstance or accepts the default, and calls an Entity Operation, Database-wide Operation, or Lifecycle Command. Core resolves the complete Instance configuration and forwards the request to that Instance's Engine file. The result returns through Core and Interface in the published form.

<br>

## Terms

- **Engine** — a declared database technology used by one or more Instances.
- **Instance** — one named database connection and storage identity, including its Engine, active state, database identity, connection values, and options.
- **DatabaseInstance** — the public enum whose members identify exactly the active configured Instances; it contains no connection credentials.
- **Database Configuration** — generated `config.yaml`, the sole runtime source for Engines, Instances, Settings, and Initial Data.
- **Interface** — the only public Database file.
- **Entity Operation** — an Operation scoped to one Entity: Add, Update, List, Delete, Enable, Disable, GetById, Count, Sum, Min, Max, or Truncate.
- **Database-wide Operation** — an Operation scoped to the selected Instance rather than one Entity; currently ExecuteCommand.
- **Lifecycle Command** — an explicit preparation command with a generated manual script: CreateTables or InsertInitialData.
- **Filter** — an immutable condition containing `field`, `operator`, and a value when the selected operator requires one.
- **FilterOperator** — the public enum containing EQUALS, NOT_EQUALS, GREATER_THAN, GREATER_OR_EQUAL, LESS_THAN, LESS_OR_EQUAL, IN, CONTAINS, STARTS_WITH, ENDS_WITH, IS_NULL, and IS_NOT_NULL.
- **FilterCombination** — the public enum containing AND and OR.
- **Order** — an immutable ordering instruction containing `field` and `direction`.
- **OrderDirection** — the public enum containing ASCENDING and DESCENDING.
- **CommandResult** — the public result of ExecuteCommand.
- **LifecycleResult** — the public result of a Lifecycle Command.
- **Data** — the Engine-independent Core file that validates, resolves, routes, and normalizes requests and results.

<br>

## Architecture

```text
Database
├── interface
├── core/
│   ├── data
│   ├── tables
│   └── initial_data
├── engine/
│   └── <active-instance>
├── db/
├── config.yaml
└── README.md
```

<br>

## Relationships

- **Consumes Model** — imports Model Interface and uses its Schema-defined Entity Collection and Entity Exports only. It uses each actual Entity and the Declaration that Entity exposes without interpreting Model internals. Model remains read-only and independently owned.
- **Provides through Interface** — publishes Database contracts for any authorized consumer without naming or treating one consumer specially.

<br>

## Layering

### Interface

Interface publishes the Database access surface, DatabaseInstance, all Entity Operations, all Database-wide Operations, all Lifecycle Commands, Filter, FilterOperator, FilterCombination, Order, OrderDirection, CommandResult, and LifecycleResult. Consumers do not recreate these contracts. Interface declares and forwards behavior; it does not implement Engine work.

#### Entity Operations

- **Add** — accepts a complete new Entity instance and returns the stored Entity with generated values.
- **Update** — accepts a complete Entity instance, uses `id` only to locate the record, replaces every mutable Field, preserves immutable Fields, and returns the stored Entity or `null`.
- **List** — accepts an Entity class, optional Filters, optional FilterCombination, optional ordered Orders, and optional limit; returns matching Entity instances.
- **Delete** — accepts an Entity class and `id`; returns the last deleted Entity or `null`.
- **Enable** — accepts an Entity class and `id`, sets only `is_active` to `true`, and returns the final Entity or `null`.
- **Disable** — accepts an Entity class and `id`, sets only `is_active` to `false`, and returns the final Entity or `null`.
- **GetById** — accepts an Entity class and `id`; returns the Entity or `null`.
- **Count** — accepts an Entity class, optional Filters, and optional FilterCombination; returns the matching count.
- **Sum** — accepts an Entity class, Field name, optional Filters, and optional FilterCombination; ignores `null` and returns the total or `0`.
- **Min** — accepts an Entity class, Field name, optional Filters, and optional FilterCombination; ignores `null` and returns the minimum or `null`.
- **Max** — accepts an Entity class, Field name, optional Filters, and optional FilterCombination; ignores `null` and returns the maximum or `null`.
- **Truncate** — accepts an Entity class, removes all of its records without removing its Table, and returns the deleted count.

Every Entity Operation also accepts an optional DatabaseInstance. Add and Update receive Entity instances; the other Entity Operations receive the public Entity class. No Operation selects an Entity by a Model name or other string identity.

#### Database-wide Operations

- **ExecuteCommand** — accepts a SQL command and bound parameters, runs any valid command supported by the selected Engine, and returns CommandResult.

#### Lifecycle Commands

- **CreateTables** — creates or safely aligns all Tables required by current public Entity Declarations on the selected Instance.
- **InsertInitialData** — inserts missing configured Initial Data on the selected Instance after its Tables exist.

Both commands accept an optional DatabaseInstance, default to the configured default Instance, return LifecycleResult, and are callable through Interface or their generated manual scripts. A script is only an invocation entry point; Core and the selected Engine own the work.

### Core

`data` owns shared validation, default resolution, Instance selection, routing, and result normalization for all public requests. `tables` coordinates CreateTables. `initial_data` coordinates InsertInitialData. Core contains no Instance-specific connection or storage implementation.

### Engine

`engine` contains exactly one file for every active Instance, named from that Instance. Each file implements all Entity Operations, ExecuteCommand, and the Engine capabilities required by both Lifecycle Commands. Two Instances using the same Engine still have separate files.

### Storage

`db` contains Database-owned persistent files and no source code. A file-backed Instance resolves its configured relative path from this Database-owned storage root, never from an installed package, a virtual environment, or a consuming Component.

<br>

## Authority

Every Database Principle is mandatory. Database Preferences may complete unstated realization choices but never weaken or replace a Principle. Explicit compatible Target values take precedence over defaults.

<br>

## Principles

Every Principle below is mandatory.

### General

#### Database owns one canonical Architecture

**Rule:** The Component root contains one Interface file, `core`, `engine`, `db`, generated `config.yaml`, and root `README.md`. Core contains `data`, `tables`, `initial_data`, and every additional internal source file. Engine contains one file per active Instance. Storage files belong only in `db`.

**Boundary:** Fixed Architecture members are not renamed or relocated. No additional internal source file is placed at the Component root, beside an Engine file, or inside `db`.

#### Database preserves one observable contract

**Rule:** Architecture, public contracts, Instance selection, request meaning, result meaning, routing, and ownership remain stable across languages, packages, libraries, and database technologies.

**Boundary:** Syntax, drivers, ORMs, migration tools, query builders, sessions, connection pools, transactions, and SQL rendering are realization details. An incompatible technology fails generation rather than changing Database meaning.

#### Database consumes Model without owning it

**Rule:** Database imports Model Interface and reaches Entities only through its Schema-defined Entity Collection and Entity Exports. It iterates the Entity Collection and uses each actual public Entity and the complete public Declaration it exposes. It never uses wildcard or attribute discovery, scans Model directories, imports Entity-unit paths, builds another Model registry, or creates, edits, builds, tests, documents, or generates an artifact inside Model.

**Boundary:** A missing or incompatible Model capability is reported; Database does not repair or redefine Model.

#### Database stores values without interpreting domain meaning

**Rule:** Database persists declared Entity values and realizes declared Fields, Primary Keys, Relations, Uniqueness Constraints, Indexes, defaults, and Value Generation without adding behavior based on application meaning. Sensitivity markers and at-rest security instructions never remove, postpone, or block a Target Initial Data record.

**Boundary:** Database does not mask, hash, encrypt, authorize, hide, or otherwise treat an Entity Field specially because it represents a password or sensitive value. It stores the concrete value supplied to it unchanged; any security transformation belongs outside Database and its absence does not block Database generation or insertion.

#### Generation verifies Database without changing dependencies

**Rule:** Generation verifies exact Architecture, one Engine file and one DatabaseInstance member per active Instance, complete Interface publication, valid config against its Schema, an active default Instance, Database-owned file storage resolution, complete Engine contracts, Documentation, and zero-diff regeneration.

**Boundary:** Verification reads dependencies as needed but changes, generates, builds, tests, and documents only Database output.

<br>

### Interface

#### Interface is the only public Database boundary

**Rule:** Interface publishes Database, DatabaseInstance, every member of the three public capability groups, Filter, FilterOperator, FilterCombination, Order, OrderDirection, CommandResult, and LifecycleResult. The groups are mandatory conceptual organization and do not require language-specific wrapper objects. Core, Engine, configuration details, and storage paths remain internal.

**Boundary:** Interface declares and forwards public behavior; it does not select a driver or implement Engine work.

#### Public query vocabulary is typed and canonical

**Rule:** Public requests use FilterOperator, FilterCombination, and OrderDirection members, never free runtime strings. Serialized configuration stores canonical member names and resolves them during loading; an unknown name fails loading. Filter and Order are immutable values. IS_NULL and IS_NOT_NULL take no value; IN takes a compatible collection; textual operators require textual Fields; comparisons require compatible Field values.

**Boundary:** Field names remain strings because they refer to public Entity Fields, and each is validated against the selected Entity before an Instance is accessed.

#### Query defaults are deterministic

**Rule:** List, Count, Sum, Min, and Max accept Filters and FilterCombination; omitted combination resolves from configuration and defaults to AND. List alone accepts ordered Orders and limit. Omitted Orders resolve to `id` ASCENDING. An Order missing direction uses ASCENDING. Omitted limit resolves to `-1`; `0` and every negative value normalize to `-1`, meaning no limit. Positive limit is the maximum returned count.

**Boundary:** Supplied Orders replace the default and are applied in supplied order. Aggregate Operations do not accept Order.

#### Entity Operations have one request and result contract

**Rule:** Add and Update receive complete Entity instances. GetById, Delete, Enable, and Disable receive an Entity class and `id`; List, Count, and Truncate receive an Entity class; Sum, Min, and Max additionally receive one valid Field name. Update never changes `id` or another immutable Field. GetById, Update, Delete, Enable, and Disable return `null` when no record exists. Delete returns the final deleted Entity. Enable and Disable change only `is_active` and return the final Entity, including when it already has the requested state.

**Boundary:** A missing record is not an Engine failure. Invalid input, configuration, connection, or execution remains an error.

#### ExecuteCommand is the Database-wide Operation

**Rule:** ExecuteCommand accepts a SQL command, bound parameters, and optional DatabaseInstance; it executes any valid command supported by the selected Engine and returns CommandResult with `rows`, `affected`, `columns`, `success`, `message`, and `instance`.

**Boundary:** CreateTables remains the standard schema-preparation path, but ExecuteCommand is not prohibited from changing schema.

#### Public errors preserve common meaning

**Rule:** Realizations make configuration or Instance invalidity, inactive Instance selection, invalid input or Field, Declaration incompatibility, connection failure, execution failure, and incomplete Lifecycle execution distinguishable without exposing credentials.

**Boundary:** A language may realize these meanings through its normal error mechanism; the Definition imposes no language-specific Exception hierarchy.

<br>

### Lifecycle Commands

#### Lifecycle Commands are separate from Operations

**Rule:** CreateTables and InsertInitialData are public Lifecycle Commands with generated manual scripts and LifecycleResult containing `command`, `instance`, `success`, `affected`, and `message`. They are not Entity Operations or Database-wide Operations.

**Boundary:** Manual and after-generation execution invoke the same public commands and do not duplicate their logic inside scripts.

#### CreateTables safely realizes current Declarations

**Rule:** CreateTables uses the actual Declaration of every Entity in the Model Entity Collection to create or safely align required Tables, Fields, Primary Keys, Relations, Uniqueness Constraints, and Indexes. Re-execution on an aligned schema succeeds without destructive change. An incompatible or destructive implicit change stops with a clear failure unless the selected migration mechanism has an explicit safe plan.

**Boundary:** It does not copy runtime records between Instances, invent Relation cascade behavior, or silently alter a Declaration. Cross-Instance transfer requires a future explicit command.

#### InsertInitialData is repeatable

**Rule:** Generation copies every Target-defined Initial Data record into the shared Database Configuration. A Target instruction requesting a generated initial value, including `Generate securely`, is resolved during generation to a concrete value before config is emitted. InsertInitialData reads that complete collection, validates each record through its public Entity contract, inserts missing records, skips already-present identical records, and returns success with zero affected items only when the Target declares no Initial Data.

**Boundary:** A sensitivity marker, hash or encryption instruction, credential Field, or missing security processor never causes a record to be omitted or held. Database inserts the resolved value unchanged. It does not silently update, delete, duplicate, or overwrite an existing record; conflicting Initial Data fails clearly.

#### After-generation preparation uses the default Instance

**Rule:** When enabled, generation runs CreateTables and then InsertInitialData for the active default Instance. InsertInitialData does not run after CreateTables fails. Failure identifies the Instance and command and fails preparation.

**Boundary:** Other active Instances are prepared only by explicit selection.

<br>

### Core

#### Core owns shared routing

**Rule:** Data receives each Interface request, validates public input, resolves defaults and the selected DatabaseInstance, loads its complete configuration, forwards work to that Instance file, materializes published Entity results, and normalizes every result.

**Boundary:** Core does not contain driver calls or Instance-specific storage behavior.

#### Changes are atomic

**Rule:** Every changing Operation and InsertInitialData completes atomically in its selected Instance or leaves no partial data change. CreateTables is atomic when supported; otherwise an incomplete state is explicitly reported as failure. Separate calls do not share a hidden transaction.

**Boundary:** Libraries and Engines choose the technical transaction mechanism.

<br>

### Engine

#### Every active Instance owns one complete implementation

**Rule:** Generation creates exactly one Engine file per active Instance and none for an inactive Instance. Each file implements all Entity Operations, ExecuteCommand, and the capabilities required by both Lifecycle Commands while preserving public request, result, error, and atomicity meaning.

**Boundary:** An Instance file implements storage behavior but never defines a new public contract or shared routing.

#### Libraries own technical database mechanics

**Rule:** The selected Library and Engine own type mapping, query construction, connection management, transaction mechanics, schema tooling, and driver integration.

**Boundary:** Database Definition contains no Engine-specific SQL map, session algorithm, pool algorithm, or ORM API.

#### Relations add no undeclared behavior

**Rule:** An Engine realizes a declared Relation as a compatible foreign key or equivalent constraint. A conflicting change is rejected atomically.

**Boundary:** No cascade, nested persistence, eager loading, or related-Entity mutation is invented from a Relation.

<br>

### Configuration and Storage

#### Configuration has one runtime source

**Rule:** `database.yaml` defines the Component contract and generation defaults. Generation produces `config.yaml`; after generation, config is the sole runtime source for Engines, complete Instances, Settings, and Initial Data. Runtime never reads `database.yaml`, and runtime configuration never writes back to it.

**Boundary:** Regeneration may rebuild config from current Target input and Preferences; no hidden merge or second runtime source exists.

#### Every Instance is complete and valid

**Rule:** Each Instance has a unique key, name, active state, Engine, host, port, database, username, password, and options. Engine-specific validation requires applicable values and allows inapplicable values to remain empty. The default Instance exists, is active, and is published through DatabaseInstance. Updating an Instance replaces and revalidates its complete definition.

**Boundary:** Consumers select a DatabaseInstance member; Core resolves connection values. Credentials are never members of DatabaseInstance or repeated in Operation requests.

#### Active Instances determine generated and public resources

**Rule:** Exactly active Instances become DatabaseInstance members and Engine files. Configuration loading rejects an unknown, inactive, colliding, or unresolved Instance selection.

**Boundary:** Changing active membership takes effect through resolved configuration and the next generation where files must change.

#### File storage remains Database-owned and persistent

**Rule:** A file-backed Instance resolves its configured database path from Database's `db` storage root. The resolved path never depends on package installation, site-packages, a virtual environment, process working directory, or a consuming Component.

**Boundary:** An invalid or escaping path fails before connection. Only Database creates and manages its storage files.

#### Initial Data is shared configuration

**Rule:** Configuration contains one complete shared Initial Data collection keyed by public Entity identity. It contains every Target-defined Initial Data record, including records with credential or sensitive Fields. The same collection may be applied to any active Instance; Instance selection changes only its destination.

**Boundary:** Initial Data is not Model-owned and is not duplicated in Engine files or per-Instance definitions. Generation must not replace a non-empty Target Initial Data set with an empty collection.

<br>

### Documentation

#### Documentation explains the complete public contract

**Rule:** Root README documents active Instance selection, every public capability group, all query vocabulary, defaults, result contracts, both manual Lifecycle Commands, Initial Data, persistent storage resolution, setup, verification, and Database-specific troubleshooting with complete examples.

**Boundary:** Documentation does not create behavior absent from this Definition and does not expose credentials or Engine internals.

<br>

## At a Glance

### General

**Database owns one canonical Architecture**

- **Must** — preserve the canonical root, Core, Engine, storage, configuration, and Documentation ownership.
- **Never** — place an internal source file outside Core or its owning Engine file, or place source code in `db`.

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

**Generation verifies Database without changing dependencies**

- **Must** — verify Architecture, active Instance resources, Interface, config, storage, Engine completeness, Documentation, and zero-diff regeneration.
- **Never** — mutate another Component during Database generation or verification.

<br>

### Interface

**Interface is the only public Database boundary**

- **Must** — publish DatabaseInstance, every member of the three conceptual capability groups, query vocabulary, CommandResult, and LifecycleResult through Interface.
- **Never** — expose Core, Engine, connection configuration, credentials, or storage paths as public surfaces.

**Public query vocabulary is typed and canonical**

- **Must** — use canonical enum members at runtime and validate every referenced Entity Field before Instance access.
- **Never** — accept a free runtime string for FilterOperator, FilterCombination, or OrderDirection.

**Query defaults are deterministic**

- **Must** — apply AND, `id` ASCENDING, and unlimited `-1` defaults as defined.
- **Must** — preserve supplied Order sequence and restrict Order to List.

**Entity Operations have one request and result contract**

- **Must** — preserve every Entity Operation's exact Entity input, immutable Field, missing-record, and result meaning.
- **Must** — let Enable and Disable change only `is_active` and let Delete return the final deleted Entity.

**ExecuteCommand is the Database-wide Operation**

- **Must** — run any valid command supported by the selected Engine and return CommandResult.
- **Never** — impose the removed schema-change restriction on ExecuteCommand.

**Public errors preserve common meaning**

- **Must** — distinguish public configuration, selection, validation, compatibility, connection, execution, and incomplete-Lifecycle failures.
- **Never** — expose credentials in an error.

<br>

### Lifecycle Commands

**Lifecycle Commands are separate from Operations**

- **Must** — keep CreateTables and InsertInitialData separate from Operations and callable through Interface and manual scripts.
- **Must** — return LifecycleResult from either invocation path.

**CreateTables safely realizes current Declarations**

- **Must** — create or safely align schema without hidden destructive change.
- **Never** — copy runtime records between Instances or invent relationship behavior.

**InsertInitialData is repeatable**

- **Must** — copy every Target Initial Data record into config and insert the complete collection repeatably without silent overwrite, deletion, or duplication.
- **Must** — validate every Initial Data record through its public Entity contract.
- **Never** — omit or hold credential-bearing Initial Data because a security transformation is absent.

**After-generation preparation uses the default Instance**

- **Must** — prepare the default Instance in CreateTables-then-InsertInitialData order when enabled.
- **Never** — run InsertInitialData after CreateTables fails or prepare other Instances implicitly.

<br>

### Core

**Core owns shared routing**

- **Must** — validate, resolve, route, materialize, and normalize through Core Data.
- **Never** — put Instance-specific driver behavior in Core.

**Changes are atomic**

- **Must** — keep changing requests atomic and report incomplete schema work explicitly.
- **Never** — create a hidden transaction across separate public calls.

<br>

### Engine

**Every active Instance owns one complete implementation**

- **Must** — generate one complete implementation file for every active Instance and none for an inactive Instance.
- **Never** — define public contracts or shared routing in an Instance file.

**Libraries own technical database mechanics**

- **Must** — delegate database mechanics to the selected Library and Engine while preserving the public contract.
- **Never** — define an Engine-specific SQL, session, pool, or ORM algorithm in the general contract.

**Relations add no undeclared behavior**

- **Must** — realize declared Relations as compatible constraints.
- **Never** — invent cascade, eager loading, nested persistence, or related-Entity mutation.

<br>

### Configuration and Storage

**Configuration has one runtime source**

- **Must** — use generated config as the sole runtime source.
- **Never** — read Database Preferences at runtime or maintain a hidden second source.

**Every Instance is complete and valid**

- **Must** — validate the complete Instance definition and replace it as one unit during Update.
- **Never** — require a consumer to resend connection values with an Operation.

**Active Instances determine generated and public resources**

- **Must** — publish and generate resources from active Instances only and keep the default Instance active.
- **Never** — accept an unknown, inactive, colliding, or unresolved Instance selection.

**File storage remains Database-owned and persistent**

- **Must** — resolve file storage from Database-owned `db`.
- **Never** — resolve persistent storage from a package, virtual environment, working directory, or consumer.

**Initial Data is shared configuration**

- **Must** — keep one complete shared Initial Data collection containing every Target-defined record and usable by every active Instance.
- **Never** — emit an empty collection when the Target declares Initial Data.
- **Never** — put Initial Data in Model, an Instance definition, or an Engine file.

<br>

### Documentation

**Documentation explains the complete public contract**

- **Must** — explain every public contract and its use with complete examples.
- **Never** — define new behavior or expose secrets and Engine internals.
