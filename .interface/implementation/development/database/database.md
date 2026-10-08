# Database Definition

Database is the structured Development Component that persists public Entity data and provides one stable data-access gateway.

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

<!-------------------------- Overview -->
### Overview

Database enumerates every Entity through the Entity Collection published by Model Interface, derives storage structure from each actual Entity and the Declaration it exposes, and persists Entity instances through a selected active DatabaseInstance. Interface is its only public boundary. Core routes every request, and one isolated Engine unit implements the contract for each Engine used by at least one active Instance.

<!-------------------------- Purpose -->
### Purpose

Database keeps persistence, Instance selection, and Engine integration behind one reusable boundary. Consumers select an Instance and use the published contracts without accessing configuration, Core, Engine units, connection details, or storage paths.

<!-------------------------- How It Works -->
### How It Works

A consumer imports Interface, selects a DatabaseInstance or accepts the default, and calls an Entity Operation, Command Operation, or Setup Operation. Core resolves the complete Instance configuration and forwards the request, with that Instance's connection, to its Engine's unit. The result returns through Core and Interface in the published form.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Engine** — a declared database technology used by one or more Instances.
- **Instance** — one named database connection and storage identity, including its Engine, active state, database identity, connection values, and options.
- **DatabaseInstance** — the public enumeration whose members identify exactly the active configured Instances; it contains no connection credentials.
- **Database Configuration** — the generated runtime configuration, the sole runtime source for Engines, Instances, Settings, and Initial Data.
- **Database Interface Schema** — the versioned structure that fixes every public Database contract: the Operations and Setup Operations with their inputs, effects, and results, the query vocabulary, values, results, and error meanings.
- **Database Configuration Schema** — the versioned structure that fixes the shape of the Database Configuration.
- **Entity Operation** — an Operation scoped to one Entity.
- **Command Operation** — an Operation scoped to the selected Instance rather than one Entity.
- **Setup Operation** — an explicit preparation command with a generated manual entry point: `create_tables`, `insert_initial_data`, or `prepare`, which runs the first two in order.
- **Filter** and **Order** — immutable condition and ordering values built from the public query vocabulary.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Directory Structure
└── database/
    ├── database/
    │   ├── interface
    │   ├── core/
    │   └── engine/
    ├── scripts/
    ├── db/
    ├── config
    └── README
```

The Package holds only importable source. Configuration, Storage, Entry Points, and Documentation sit beside it at the Component root, because configuration changes with the environment, stored data changes at runtime, and entry points are run by hand rather than imported.

Database Preferences own the physical names in `architecture`, and the language, packages, Engines, Instance defaults, query defaults, technical realization, and documentation choices; these selections realize the responsibilities below without changing them, and implementation applies them to the current Target.

<!-------------------------- Interface -->
### Interface — `interface`

The only public entry point, in the shape the Database Interface Schema that Database Preferences reference defines. It publishes exactly five groups, declared in the Interface section of Database Preferences, each importable by a consumer, and nothing else:

- **Database** — the class a consumer creates once to call every Entity Operation and Command Operation.
- **Setup** — the class a consumer creates to call every Setup Operation.
- **Value** — what a consumer passes to an Operation: the values of Condition, Sort, and Instance.
- **Result** — what a consumer reads back: every Result.
- **Error** — every Error, so a consumer can catch it.

It declares and forwards behavior and implements no Engine work.

<!-------------------------- Core -->
### Core — `core/`

Core owns shared validation, default resolution, Instance selection, routing, and result normalization for all public requests, and holds the entities of the Conceptual Structure. It loads and validates the Database Configuration and resolves each Instance's connection from it; an invalid Configuration or an unresolved Instance selection fails loading before any connection is opened. It contains no Instance-specific connection or storage implementation.

<!-------------------------- Engine -->
### Engine — `engine/`

Engine contains exactly one unit for every Engine used by at least one active Instance, named from that Engine. Instances that use the same Engine share its unit and differ only in their connection.

Each unit implements every Entity Operation and Command Operation, and the Engine capabilities the Setup Operations require, and returns raw results. Its driver, connection arguments, and storage kind come from the Engine's entry in Database Preferences.

<!-------------------------- Entry Points -->
### Entry Points — `scripts/`

Entry Points holds exactly three scripts, one for each Setup Operation — `create_tables`, `insert_initial_data`, and `prepare` — so a person can prepare storage by hand. Each runs its Setup Operation through Interface on the default Instance, reports its result, and holds no logic of its own. When after-generation preparation is enabled in Database Preferences, generation runs `prepare` the same way.

<!-------------------------- Storage -->
### Storage — `db/`

The place where a file-backed database keeps its files. The database file of one file-backed Instance is named by that Instance's database value.

<!-------------------------- Configuration -->
### Configuration — `config`

The generated Database Configuration, the sole runtime source for Engines, Instances, Settings, and Initial Data. Its structure is fixed by the Database Configuration Schema that Database Preferences reference.

<!-------------------------- Documentation -->
### Documentation — `README`

The root documentation explaining every public contract, Instance selection, the Setup Operations, Initial Data, setup, use, verification, and Database-specific troubleshooting.

Its sections, in this order:

1. **Overview** — Give one short introduction and one simple example: create Database, then one add and one list.
2. **Interface** — For each of the five groups Interface publishes, and every member and Operation in it with each of its parameters, explain what it is for and how to use it, with one example each. Cover every enumeration member, defaults, results, and errors.
3. **Instances** — Explain active DatabaseInstance members, default selection, and Database-owned storage without exposing credentials.
4. **Setup** — Give the setup steps for the selected technology.
5. **Use** — Show every capability group used only through Interface, with Field references and enumeration members and never strings.
6. **Setup Operations** — Explain manual `create_tables`, `insert_initial_data`, and `prepare` use, and that generation runs `prepare` automatically.
7. **Initial Data** — List every Target-defined Initial Data record and state that Database inserts its values unchanged without security-based omission.
8. **Verify** — Verify public import, Instance selection, query vocabulary, each capability group, persistent file location, and repeatable Setup Operations.
9. **Troubleshooting** — Cover Database concerns only, including an inactive Instance, a difference between an existing Table and its Entity, and empty Initial Data values.


<br>

```text
Conceptual Structure
├── Operation
│   ├── Entity Operation
│   │   ├── add
│   │   ├── update
│   │   ├── list
│   │   ├── get_by_id
│   │   ├── delete
│   │   ├── enable
│   │   ├── disable
│   │   ├── count
│   │   ├── sum
│   │   ├── min
│   │   ├── max
│   │   └── truncate
│   ├── Setup Operation
│   │   ├── create_tables
│   │   ├── insert_initial_data
│   │   └── prepare
│   └── Command Operation
│       └── execute_command
├── Query
│   ├── Condition
│   ├── Sort
│   └── Limit
├── Instance
├── Result
└── Error
```

Every entity below is declared in `architecture` in Database Preferences.

<!-------------------------- Operation -->
### Operation

#### Entity Operation

Operations scoped to one Entity. Each receives the Entity itself — an Entity instance or the Entity class imported from Model — never an Entity name or other string identity.

#### Setup Operation

Explicit preparation operations, callable through the Setup group of Interface and through the Entry Points. Core coordinates each of them: `create_tables` creates every Table, `insert_initial_data` inserts the Initial Data, and `prepare` does both, in that order.

#### Command Operation

Operations scoped to an Instance rather than one Entity.

<!-------------------------- Query -->
### Query

Query is how a consumer narrows, orders, and bounds what an Operation reads: a Condition, a Sort, and a Limit. Its enumerations are closed member sets; a consumer imports and passes their members and values, and a string is never accepted in their place. A Field's declared Type is the Type its Field Declaration in Model carries, such as integer, string, or datetime. No checked form is published.

#### Condition

The immutable Filter a consumer builds, with its operator and its combination. Core checks each Filter into a checked Filter: the Field's name and declared Type, its operator, and its normalized value.

#### Sort

The immutable Order a consumer builds, with its direction. Core checks each Order into a checked Order: the Field's name and declared Type, and whether it descends.

#### Limit

A positive limit is the maximum returned count; zero or a negative limit means no limit.

<!-------------------------- Instance -->
### Instance

Which Instance a call runs on. Every Operation accepts an optional DatabaseInstance; when none is given, the call runs on the configured default Instance. DatabaseInstance has one member for every active configured Instance and none for an inactive one.

<!-------------------------- Result -->
### Result

The immutable results a consumer reads, each with its fields.

<!-------------------------- Error -->
### Error

The failure kinds declared in `architecture` in Database Preferences. Every realization keeps each kind distinguishable through the language's own error mechanism: each is published as its own error, derived from one base error, and its name belongs to the selected language profile. No error carries a connection value or credential.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — uses the Entity Collection and Entity Exports Model Interface publishes, found from Model's own Preferences.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **The meaning of data — Entities, Fields, Types, and constraints** — is not Database's, because Database stores data rather than defining what it means.
- **Hashing, encryption, masking, and secret storage** — are not Database's, because they change a value rather than store it.
- **Business rules, workflows, authorization, and orchestration** — are not Database's, because they depend on how data is used, not on how it is stored.
- **Changing the structure of existing Tables** — is not Database's, because Database only creates Tables from the current Entities and stops on any difference.
- **Endpoints, requests, responses, and protocols** — are not Database's, because they are properties of moving data, not of storing it.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Database Principle is mandatory. Database Preferences may complete unstated realization choices but never weaken or replace a Principle. Explicit compatible Target values take precedence over defaults.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<!-------------------------- General -->
### General

#### Database owns one canonical Architecture

**Rule:** The Component has exactly the parts Architecture shows, each with the responsibility stated there.
**Why:** A fixed layout lets every generation place each file in the same place, so an Agent never decides structure and consumers always find the same parts.
**Boundary:** Fixed Architecture members are renamed only through `architecture` in Database Preferences and never relocated. No additional internal source unit is placed at the Component root, beside an Engine unit, or inside Storage.

#### Database consumes Model without owning it

**Rule:** Database imports Model Interface and reaches Entities only through its Schema-defined Entity Collection and Entity Exports. It iterates the Entity Collection and uses each actual public Entity and the complete public Declaration it exposes. It never uses wildcard or attribute discovery, scans Model directories, imports Entity-unit paths, builds another Model registry, or creates, edits, builds, tests, documents, or generates an artifact inside Model.
**Why:** One path to Entities keeps Database in step with Model and prevents a second, drifting copy of Model's meaning.
**Boundary:** A missing or incompatible Model capability is reported; Database does not repair or redefine Model.

#### Database stores values without interpreting domain meaning

**Rule:** Database persists Entity values without adding behavior based on application meaning. Sensitivity markers and at-rest security instructions never remove, postpone, or block a Target Initial Data record.
**Why:** Storage that interprets meaning would hide or change data unpredictably; storing exactly what it receives keeps results repeatable and leaves meaning to its owner.
**Boundary:** Database stores each value exactly as it receives it.

<br>

<!-------------------------- Interface -->
### Interface

#### Interface conforms to the Database Interface Schema

**Rule:** Every realization of Interface conforms to the versioned Database Interface Schema, which fixes every public contract, each Operation's and Setup Operation's input, effect, and result, the query vocabulary, values, results, error meanings, and what Interface never publishes. Consumers pass Entities, Fields, Instances, and vocabulary as imported values, never as strings.
**Why:** Consumers depend on one contract instead of reinterpreting each realization, and typed values are checked before any storage is touched.
**Boundary:** Interface declares and forwards public behavior; it does not select a driver or implement Engine work. The Database Interface Schema is built from the Architecture and Interface sections of Database Preferences and this Definition; when either changes a public contract, the Schema is rebuilt from them and its version is raised.

#### Interface contracts keep one fixed shape

**Rule:** Every Operation and Setup Operation takes exactly its listed parameters, by those names and in that order, with every parameter after entity, id, field, and command optional and instance always last. Every Field in a Filter, Order, or aggregate is validated against the given Entity before any Instance is accessed. Database holds the Entity Operations and Command Operations, and Setup holds the Setup Operations; no other wrapper is added. Stored enumeration defaults use canonical member names, and an unknown name fails loading.
**Why:** A consumer calls the same shape on every Instance, Engine, and language, and a bad Field fails before any storage is touched.
**Boundary:** Changing Entities, Instances, Engines, languages, packages, or internal implementation never changes this shape; an incompatible technology fails generation rather than changing Database meaning.

#### Query defaults are deterministic

**Rule:** List, Count, Sum, Min, and Max accept Filters and a FilterCombination; List alone also accepts ordered Orders and a limit. An omitted FilterCombination, Order set, or limit resolves from Database Preferences; an Order without a direction uses ASCENDING. A zero or negative limit means no limit; a positive limit is the maximum returned count.
**Why:** Fixed defaults make the same call return the same result on every Instance and every generation.
**Boundary:** Supplied Orders replace the default and are applied in supplied order. Aggregate Operations do not accept Order.

<br>

<!-------------------------- Setup Operations -->
### Setup Operations

#### Setup Operations are separate from Operations

**Rule:** `create_tables`, `insert_initial_data`, and `prepare` are public Setup Operations, each with a generated manual entry point and a SetupResult. `prepare` runs `create_tables` and then `insert_initial_data` on the selected Instance and stops when `create_tables` fails. They are not Entity Operations or Command Operations.
**Why:** Preparing storage is a different act from using it; keeping them apart prevents an everyday call from changing schema or seeding data.
**Boundary:** Manual and after-generation execution invoke the same public commands and do not duplicate their logic inside an entry point.

#### `create_tables` builds Tables only from Model Entities

**Rule:** `create_tables` uses only the actual Entities of the Model Entity Collection and their Declarations to create the required Tables, Fields, Primary Keys, Relations, Uniqueness Constraints, and Indexes. It never reads the Target. Re-execution on matching Tables succeeds without change. A difference between an existing Table and its Declaration stops the command and is reported; it is never resolved by judgment.
**Why:** The generated Entities already carry every structural fact, so Tables follow them exactly and the same Entities always yield the same Tables.
**Boundary:** It does not copy runtime records between Instances, invent Relation cascade behavior, or alter a Declaration. Cross-Instance transfer requires a future explicit command.

#### `insert_initial_data` is repeatable

**Rule:** Generation copies every Target-defined Initial Data record into the shared Database Configuration. A Target value that is not concrete, including `Generate securely`, is copied as an empty string and generation continues; Database never produces a value itself, and the user fills such values later. `insert_initial_data` reads that complete collection, validates each record through its public Entity contract, inserts missing records, skips already-present identical records, and returns success with zero affected items only when the Target declares no Initial Data.
**Why:** Running it again must never duplicate or lose records, so preparation can be repeated safely on any Instance.
**Boundary:** Database inserts each value unchanged. It does not silently update, delete, duplicate, or overwrite an existing record; conflicting Initial Data fails clearly.

#### After-generation preparation uses the default Instance

**Rule:** When enabled, generation runs `prepare` on the active default Instance. Failure identifies the Instance and command and fails preparation.
**Why:** One predictable target keeps generation from touching Instances nobody asked it to prepare.
**Boundary:** Other active Instances are prepared only by explicit selection.

<br>

<!-------------------------- Core -->
### Core

#### Core owns shared routing

**Rule:** Data receives each Interface request, validates public input, resolves defaults and the selected DatabaseInstance, loads its complete configuration, forwards work with that Instance's connection to its Engine unit, materializes published Entity results, and normalizes every result. Each stored row becomes an Entity through that Entity's own construction; a row that does not satisfy the Entity contract is an error and is never repaired.
**Why:** Shared validation and routing in one place make every Engine receive the same checked request and return the same normalised result.
**Boundary:** Core does not contain driver calls or Instance-specific storage behavior.

#### Changes are atomic

**Rule:** Every changing Operation and `insert_initial_data` completes atomically in its selected Instance or leaves no partial data change. `create_tables` is atomic when supported; otherwise an incomplete state is explicitly reported as failure. Separate calls do not share a hidden transaction.
**Why:** A half-applied change leaves data that no contract describes; all-or-nothing keeps storage always in a known state.
**Boundary:** Libraries and Engines choose the technical transaction mechanism.

<br>

<!-------------------------- Engine -->
### Engine

#### Every Engine in use owns one complete implementation

**Rule:** Generation creates exactly one Engine unit for every Engine used by at least one active Instance and none for any other Engine. Instances of the same Engine share its unit and differ only in the connection Core passes to it. Each unit implements all Entity Operations, `execute_command`, and the capabilities required by the Setup Operations while preserving public request, result, error, and atomicity meaning.
**Why:** Instances of one Engine work the same way, so one complete unit serves them all without duplicated code, and an Engine nobody uses leaves nothing behind.
**Boundary:** An Engine unit implements storage behavior but never defines a new public contract or shared routing.

<br>

<!-------------------------- Configuration -->
### Configuration

#### Configuration conforms to the Database Configuration Schema

**Rule:** Generation produces the Database Configuration in the shape the versioned Database Configuration Schema defines, and every rule of that Schema holds: one runtime source, complete and valid Instances, active membership, Database-owned storage, and one shared Initial Data collection.
**Why:** Every run reads the same checked settings, and a consumer never supplies or sees connection values.
**Boundary:** Database Preferences supply generation defaults only; runtime reads only the Database Configuration. Changing the Configuration's structure requires a Schema version change.

<br>

<!-------------------------- Documentation -->
### Documentation

#### Documentation explains the complete public contract

**Rule:** Documentation explains every public contract and how to use it, with examples, in the sections Architecture lists for Documentation.
**Why:** Consumers use Database through its documentation; a gap or an invented feature there leads directly to wrong use.
**Boundary:** Documentation does not create behavior absent from this Definition and does not expose credentials or Engine internals.

<br>

<!-------------------------- Review -->
### Review

#### Database conformance covers every Database contract

**Rule:** Database output is conformant only when it shows exact Architecture, one DatabaseInstance member per active Instance, one Engine unit per Engine in use, complete Interface publication conforming to the Database Interface Schema, valid config against its Schema, an active default Instance, Database-owned file storage resolution, complete Engine contracts, Documentation, and zero-diff regeneration.
**Why:** These are the contracts consumers rely on; a check that omits one lets a broken Database look complete.
**Boundary:** Review reads dependencies as needed but changes, generates, builds, tests, and documents only Database output. The Review Operation establishes this; Plan and Develop check nothing.

#### Review observes Database through a fixed set of checks

**Rule:** Review establishes Database conformance through these observations, every one of them on every review:

- Interface publishes exactly the public contracts of the Database Interface Schema and nothing else.
- Every Entity Operation, Command Operation, and Setup Operation has the signature and result the Schema states, including the optional DatabaseInstance.
- Each enumeration holds exactly its Schema members.
- DatabaseInstance holds exactly one member per active configured Instance and none for an inactive one.
- A call without a DatabaseInstance runs on the configured default Instance.
- No Operation accepts an Entity name, a Field name, or any other string in place of an imported value.
- `create_tables` uses only the Entities of the Model Entity Collection and their Declarations, and stops on a difference with an existing Table.
- Every returned Entity is built through its own construction, and a row that breaks the Entity contract is an error.
- `prepare` runs `create_tables` and then `insert_initial_data`, and stops when `create_tables` fails.
- A Target Initial Data value that is not concrete is copied as an empty string, and no value is generated.
- A missing record returns null, never an error.
- Loading Interface opens no connection and creates no data or file.

**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

<!-------------------------- General -->
### General

**Database owns one canonical Architecture**

- **Must** — preserve the canonical Interface, Core, Engine, Entry Points, Storage, Configuration, and Documentation, and rename a member only through `architecture` in Preferences.
- **Never** — place an internal source unit outside Core or its owning Engine unit, or place source code in Storage.

**Database consumes Model without owning it**

- **Must** — consume actual Entity and Declaration references only through Model Interface's Entity Collection and Entity Exports.
- **Never** — use wildcard or attribute discovery, directories, internal paths, or construct another Entity registry.
- **Never** — change, generate, build, test, or document Model output.

**Database stores values without interpreting domain meaning**

- **Must** — persist Entity values without adding application behavior.
- **Must** — keep Target Initial Data eligible for insertion regardless of sensitivity or at-rest metadata.
- **Never** — change or treat a value differently because of what it means.

<br>

<!-------------------------- Interface -->
### Interface

**Interface conforms to the Database Interface Schema**

- **Must** — conform every realization to the Database Interface Schema and accept only imported values where the Schema forbids strings.
- **Never** — expose Core, Engine, configuration, credentials, or storage paths, or change Interface structure without a Schema version change.

**Interface contracts keep one fixed shape**

- **Must** — take exactly the listed parameters in order, with instance last, and validate every Field before any Instance is accessed.
- **Never** — let a change of Entity, Instance, Engine, language, or package change the Interface shape.

**Query defaults are deterministic**

- **Must** — resolve omitted combination, Orders, and limit from Preferences and treat a zero or negative limit as no limit.
- **Must** — preserve supplied Order sequence and restrict Order to List.

<br>

<!-------------------------- Setup Operations -->
### Setup Operations

**Setup Operations are separate from Operations**

- **Must** — keep `create_tables`, `insert_initial_data`, and `prepare` separate from Operations and callable through Interface and manual entry points.
- **Must** — return SetupResult from either invocation path.

**`create_tables` builds Tables only from Model Entities**

- **Must** — build Tables only from the Entities of the Model Entity Collection and their Declarations, and stop on any difference with an existing Table.
- **Never** — read the Target, alter an existing Table by judgment, copy records between Instances, or invent relationship behavior.

**`insert_initial_data` is repeatable**

- **Must** — copy every Target Initial Data record into config and insert the complete collection repeatably without silent overwrite, deletion, or duplication.
- **Must** — validate every Initial Data record through its public Entity contract.
- **Never** — produce an Initial Data value itself; a value that is not concrete in the Target is copied as an empty string.

**After-generation preparation uses the default Instance**

- **Must** — run `prepare` on the default Instance when enabled.
- **Never** — prepare other Instances implicitly.

<br>

<!-------------------------- Core -->
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

<!-------------------------- Engine -->
### Engine

**Every Engine in use owns one complete implementation**

- **Must** — generate one complete implementation unit for every Engine used by at least one active Instance and none for any other Engine.
- **Never** — define public contracts or shared routing in an Engine unit, or duplicate a unit for another Instance of the same Engine.

<br>

<!-------------------------- Configuration -->
### Configuration

**Configuration conforms to the Database Configuration Schema**

- **Must** — produce the Database Configuration in the Schema's shape and keep every Schema rule.
- **Never** — read Database Preferences at runtime or expose connection values to a consumer.

<br>

<!-------------------------- Documentation -->
### Documentation

**Documentation explains the complete public contract**

- **Must** — explain every public contract and how to use it, with examples, in the sections Architecture lists.
- **Never** — define new behavior or expose secrets and Engine internals.

<br>

<!-------------------------- Review -->
### Review

**Database conformance covers every Database contract**

- **Must** — show Architecture, active Instance resources, Interface, config, storage, Engine completeness, Documentation, and zero-diff regeneration before Database is conformant.
- **Never** — mutate another Component during review.

**Review observes Database through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
