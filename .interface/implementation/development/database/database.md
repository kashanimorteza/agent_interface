# Database Definition

Database is the structured Development Component that persists Entity data and provides one stable data-access gateway independently of Agent, programming language, and package.

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

Database persists Model Entity data and publishes one simple public access surface for Database Operations and active Instances. Other Components use this gateway to store and retrieve data without depending on Database internals or the selected implementation technology. Its internal flow is Interface, Core Data, and one Engine file per active Instance.

### Purpose

Database keeps persistence knowledge in one reusable Component. Its Architecture and observable behavior remain stable across Agents, programming languages, packages, and database technologies. Without that separation, consumers become coupled to Engine selection, storage behavior, and implementation details.

### How It Works

A consumer imports Database through Interface, selects an active Instance or accepts the default, and calls an Operation. Core's Data file forwards that request to the Engine file owned by the selected Instance. That file performs the Operation and returns the result through Data and Interface. Database also publishes commands for creating Tables and inserting Initial Data on a selected Instance.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Engine** — a declared database technology used by one or more Instances.
- **Instance** — a named database connection and storage identity using one Engine; its active state determines whether Interface publishes it.
- **Instance Implementation** — the file under `engine` owned by one active Instance, which implements every Database Operation for that Instance through its selected Engine.
- **Instance Enum** — the public enum whose members identify the active Instances available through Interface.
- **Database Configuration** — the generated `config.yaml` record declaring the Engines, Instances, and Settings available to Database.
- **Settings** — component-wide choices such as the default Instance and other shared parameters.
- **Interface** — the only public Database file, through which consumers import Database, discover active Instances, and request Database Operations.
- **Operation** — one public Database action published through Interface.
- **Filter** — one condition with an Entity Field name string, a Filter Operator enum member, and a value.
- **Filter Operator** — an enum selecting one supported comparison: `equals`, `not_equals`, `greater_than`, `greater_or_equal`, `less_than`, `less_or_equal`, `in`, `contains`, `starts_with`, `ends_with`, `is_null`, or `is_not_null`.
- **Filter Combination** — an enum selecting how List combines Filters: `AND` or `OR`.
- **Order** — one ordering instruction with an Entity Field name string and an Order Direction enum member.
- **Order Direction** — an enum selecting `ascending` or `descending`.
- **Command Result** — the standard result of Execute Command, with `rows` and `affected_count`; either value is `null` when it does not apply. Each row is a mapping from column name to value.
- **Execute Command** — an Operation that receives a SQL command and bound parameters, executes it through the selected Engine, and returns a Command Result.
- **Create Tables** — a public command that receives an Instance and creates or migrates its Tables from the Entity declarations published by Model.
- **Insert Initial Data** — a public command that receives an Instance and inserts the declared Initial Data after its Tables exist.
- **Data** — the Engine-independent file inside `core` that defines the shared Database Operations, resolves the requested Instance, and forwards each request to that Instance's implementation.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Database
├── interface
├── core/
│   ├── data
│   ├── tables
│   └── initial_data
├── engine/
│   └── <instance>
├── db/
├── config.yaml
└── README.md
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — uses the Entity classes and their public declarations from Model Interface to derive storage structure and recognize Entity-form data. Model is a read-only dependency; Database does not import Model internals or write, generate, build, test, or otherwise create output in Model's Component directory.
- **Provides to Logic** — exposes Database Operations through Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The only public Database file. It publishes Database as the consumer access surface, the Instance Enum for every active configured Instance, every Database Operation, Create Tables, and Insert Initial Data. Operations use an Entity class or Entity instance directly, as appropriate; they never select data by a Model name or identity. Every Operation and command accepts an optional Instance Enum member; when omitted, Database uses its configured default Instance.

#### Operations

- **Add** — accepts a complete Entity instance for a new record, persists it, and returns the created Entity instance with any Engine-generated values.
- **Update** — accepts a complete Entity instance; uses `id` only to locate the record, never changes it, updates every mutable Field, preserves immutable Fields, and returns the updated Entity instance or `null` when no record has that `id`.
- **List** — accepts an Entity class, optional Filters, an optional Filter Combination enum member, an optional ordered list of Orders, and an optional limit; uses the configured default filter combination, Order, and limit when omitted. A limit of `0` or any negative value means no limit. It returns matching Entity instances.
- **Delete** — accepts an Entity class and record `id`; returns `true` when it deletes a record and `false` when no record has that `id`.
- **Enable** — accepts an Entity class and record `id`; sets its `is_active` Field to `true` and returns the Entity instance or `null` when no record has that `id`.
- **Disable** — accepts an Entity class and record `id`; sets its `is_active` Field to `false` and returns the Entity instance or `null` when no record has that `id`.
- **Get by ID** — accepts an Entity class and record `id`; returns the matching Entity instance or `null` when no record has that `id`.
- **Count** — accepts an Entity class, optional Filters, and an optional Filter Combination enum member; returns the number of matching records.
- **Sum** — accepts an Entity class, one Field name string, optional Filters, and an optional Filter Combination enum member; ignores `null` values and returns that Field's total, or `0` when no usable value exists.
- **Min** — accepts an Entity class, one Field name string, optional Filters, and an optional Filter Combination enum member; ignores `null` values and returns the smallest value, or `null` when no usable value exists.
- **Max** — accepts an Entity class, one Field name string, optional Filters, and an optional Filter Combination enum member; ignores `null` values and returns the largest value, or `null` when no usable value exists.
- **Truncate** — accepts an Entity class; removes all of its records while keeping its Table structure and returns the number of deleted records.
- **Execute Command** — accepts a SQL command and bound parameters; executes it through the selected Engine and returns a Command Result. Schema changes remain the responsibility of migrations.
- **Create Tables** — accepts an optional Instance; creates or migrates every Table required by the Entity declarations published through Model Interface for the selected or default Instance.
- **Insert Initial Data** — accepts an optional Instance; inserts the declared Initial Data into the selected or default Instance after its Tables exist.

### Core

The internal directory for Database files that are independent of any Engine. Its `data` file defines the shared behavior of every Database Operation, resolves the requested Instance, calls that Instance's implementation, materializes returned rows as Model Entity instances where an Operation publishes Entities, and returns the result according to the published Operation's contract. Core also owns the Engine-independent Create Tables and Insert Initial Data command coordination.

### Engine

The internal directory that keeps every active Instance isolated in one file. Each Instance file implements all Database Operations for that Instance through its configured Engine and connection parameters. Two active Instances using the same Engine still have separate files.

Database's technical selections and defaults belong to Database Preferences. Its fixed Architecture names are recorded there for generation but are not customizable choices. The structure of generated `config.yaml` belongs to the Database Configuration Schema.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Database Principle is mandatory. Database Preferences may provide defaults and stricter conventions, but never weaken or override a Principle. An explicit Target requirement and an applicable Principle take precedence over a Preference.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Database is implementation-independent

**Rule:** Database Architecture, ownership, Interface Operations, Instance selection, request and result meaning, Core routing, and Instance implementation responsibilities remain the same regardless of the Agent that generates it, the programming language, the package, or the selected database technology. Database Preferences may select a concrete realization, but that realization neither adds, removes, nor changes Database meaning.

**Why:** Other Components need one dependable persistence gateway without knowing how Database is generated or implemented.

**Boundary:** Language syntax, package APIs, drivers, and migration tools are realization details. If a selected technology cannot preserve a Database contract, generation reports the incompatibility instead of changing the contract.

<br>

### Database consumes Model without owning it

**Rule:** Database imports Model only through Model Interface and treats the published Entity classes and their public declarations as its complete Model input. Database may derive Tables, foreign keys, and runtime Entity values from that input, but it never changes Model meaning or implementation. Database creates, generates, builds, tests, and documents only its own Component output; it never writes, generates, builds, tests, or creates an artifact under Model's Component directory.

**Why:** Model owns Entity meaning and its own realization. Database needs that meaning as input, while remaining independently owned and realizable.

**Boundary:** A missing Model capability, incompatible Entity definition, or required change to Model is reported to Model's owner. Database does not work around it by importing Model internals or modifying Model.

<br>

### Database has one canonical Architecture

**Rule:** The Database Component root contains one Interface file, one `core` directory, one `engine` directory, one `db` directory, its generated `config.yaml`, and its `README.md`. `core` contains `data`, `tables`, `initial_data`, and every other internal source file Database needs beyond the fixed root files and Instance implementations. `data` defines and routes every Database Operation but implements no Instance-specific storage behavior. `tables` coordinates Create Tables, and `initial_data` coordinates Insert Initial Data. `engine` contains exactly one implementation file for each active Instance, named from that Instance; two Instances using the same Engine remain separate files. `db` contains database storage files. The Interface file and README remain at the Component root; only Interface is public. These names and ownership locations are fixed Database Architecture, not configurable preferences.

**Why:** A fixed ownership structure makes Database independently realizable while keeping public access, shared routing, and Engine-specific work separate.

**Boundary:** An Instance implementation does not define public Operations or shared routing. Core does not contain Instance-specific implementation. `db` does not contain source files. No additional internal source file is generated at the Component root or beside an Instance implementation; every additional internal source file belongs in `core` without exception.

<br>

### Database configuration declares its available resources

**Rule:** Database Configuration declares every Engine and its engine-specific parameters, every named Instance and its connection parameters, and component Settings such as the default Instance and other shared parameters. Every active Instance names one declared Engine, every configured Instance reference resolves to a declared Instance, and the default Instance is active. Database publishes exactly the active Instances through its Instance Enum and generates one implementation file for each of them.

**Why:** One configuration source makes the available storage resources and their selection explicit.

**Boundary:** This Definition does not choose configured Instance membership, connection values, or the default Instance. Target and Database Preferences provide those realization values under this contract.

<br>

### Database exposes explicit Interface Operations

**Rule:** Interface publishes Database, the Operations described in this Component, the Instance Enum for active configured Instances, Create Tables, and Insert Initial Data. Each applicable Operation receives an Entity class or Entity instance directly, never a Model name or identity, and accepts an optional Instance Enum member that otherwise resolves to the configured default Instance. A Filter receives an Entity Field name string, a Filter Operator enum member, and a value; supported operators are `equals`, `not_equals`, `greater_than`, `greater_or_equal`, `less_than`, `less_or_equal`, `in`, `contains`, `starts_with`, `ends_with`, `is_null`, or `is_not_null`. List, Count, Sum, Min, and Max accept optional Filters and an optional Filter Combination enum member of `AND` or `OR`; when it is omitted, Filters combine with the configured default, without complex grouping. Each Order receives an Entity Field name string and an Order Direction enum member of `ascending` or `descending`. List alone accepts an ordered list of Orders or the configured default Order, and an optional limit; it uses the configured default limit when omitted, while `0` and every negative limit mean no limit. Interface validates each supplied Field name against the selected Entity. Public Database Actions reject an enum value or Filter Combination supplied as a string; serialized Configuration values are resolved to those runtime values before an Action is called. Count returns `0` for no records; Sum ignores `null` values and returns `0` when no usable value exists; Min and Max ignore `null` values and return `null` when no usable value exists. Add persists the complete supplied Entity instance. Update never changes `id` or an immutable Field and replaces every mutable Field from the complete supplied Entity instance. Execute Command receives a SQL command and bound parameters, executes it through the selected Instance, returns a Command Result, and does not change schema. Create Tables and Insert Initial Data each accept a selected Instance and are usable both through Interface and as a manual command.

**Why:** An explicit operation catalogue keeps the public data surface stable and understandable.

**Boundary:** Interface receives and returns requests; it does not select an Engine or implement database-specific behavior.

<br>

### Database stores Entity values without interpreting their domain meaning

**Rule:** Database derives storage structure from the Entity declarations published by Model and stores and returns the Entity values it receives. It realizes declared Fields, constraints, indexes, Value Generation, and Relations through the selected Instance's Engine. Database does not add behavior based on the application meaning of a Field or value.

**Why:** Persistence remains general-purpose and can apply one consistent storage structure to every Entity value.

**Boundary:** Any application behavior based on the meaning of a Field or value belongs outside Database. Database owns only persistence and the declared storage structure.

<br>

### Database publishes Interface only

**Rule:** Interface is the only public Database layer. Core and Engine are internal implementation layers; consumers use Database only through Interface.

**Why:** One public boundary keeps Engine selection, routing, and shared implementation details out of consumers.

**Boundary:** Interface publishes Database Operations; it does not make a consumer responsible for Data routing or Engine-specific storage behavior.

<br>

### Core routes requests and handles results

**Rule:** Core's Data file implements the shared form of every Database Operation, receives each request from Interface, resolves the requested Instance, forwards the Operation to that Instance's file under `engine`, materializes returned rows as Model Entity instances whenever an Operation publishes Entities, and returns the result according to the published Operation's contract.

**Why:** One Core Data file keeps selection, routing, and result handling consistent across Engines.

**Boundary:** Data coordinates an Operation; each Instance implementation owns execution through its configured Engine. Core contains no Instance-specific storage behavior.

<br>

### Each active Instance implements the published Operations

**Rule:** Every active Instance has one implementation file isolated from every other Instance. That file implements all published Database Operations through the Instance's configured Engine and connection parameters while preserving the applicable request and result standard.

**Why:** Separate Instance implementations make each configured database independently selectable and maintainable, including when multiple Instances use the same Engine.

**Boundary:** Instance implementations perform storage behavior; the Operation catalogue, routing, and public boundary remain outside them.

<br>

### Database persists changes atomically

**Rule:** Every successful Operation that changes data persists its complete change atomically in the selected Instance. If such an Operation fails, it leaves no partial change in that Instance.

**Why:** Each data change has one reliable result regardless of the selected Engine.

**Boundary:** This applies to data-changing Operations, including a changing Execute Command; it does not restrict the commands Execute Command may receive.

<br>

### Database publishes Table and Initial Data commands

**Rule:** Database publishes separate Create Tables and Insert Initial Data commands. Each command accepts an active Instance, uses that Instance's implementation, and can be run manually for any active Instance. Create Tables creates or migrates the Tables required by the Entity declarations published through Model Interface. Insert Initial Data inserts the declared Initial Data after the required Tables exist.

**Why:** The same explicit commands can prepare any selected Instance without changing Database's public contract.

**Boundary:** The selected modeling and migration tools provide the implementation mechanism. Database owns the commands and their observable result, not a particular tool's internal workflow.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Database configuration declares its available resources**

- **Must** — declare every Engine, its parameters, named Instances, and component Settings in Database Configuration.
- **Must** — make every active Instance name a declared Engine, every configured Instance reference resolve to a declared Instance, and the default Instance active.
- **Must** — publish exactly the active Instances through the Instance Enum.
- **Must** — generate one implementation file for every active Instance, including separate files for Instances that use the same Engine.

**Database is implementation-independent**

- **Must** — preserve Database Architecture, Interface Operations, Instance selection, request and result meaning, routing, and ownership across Agents, languages, packages, and database technologies.
- **Must** — treat language, package, driver, and migration-tool choices as realization details only.
- **Never** — change Database meaning to accommodate an Agent or selected technology.

**Database consumes Model without owning it**

- **Must** — consume published Entity classes and public declarations through Model Interface only.
- **Must** — create, generate, build, test, and document only Database's own Component output.
- **Never** — import Model internals or write, generate, build, test, or create an artifact under Model's Component directory.

**Database has one canonical Architecture**

- **Must** — provide one root Interface file, `core/`, `engine/`, `db/`, generated `config.yaml`, and root `README.md`.
- **Must** — keep `data`, `tables`, `initial_data`, and every additional internal Database source file in `core/`; keep exactly one implementation file for each active Instance in `engine/`.
- **Must** — keep database storage files in `db/`.
- **Never** — rename or relocate a canonical Architecture member; put Instance-specific storage behavior in Core, shared routing or public Operations in an Instance file, source files in `db/`, or a public Database surface outside Interface.

**Database exposes explicit Interface Operations**

- **Must** — publish the Operations described by Interface.
- **Must** — publish Database, the active Instance Enum, Create Tables, and Insert Initial Data through Interface.
- **Must** — receive an Entity class or Entity instance directly, never a Model name or identity.
- **Must** — publish the active Instance Enum, accept an optional Instance member, and use the configured default Instance when it is omitted.
- **Must** — persist a complete supplied Entity instance during Add and return it with any Engine-generated values.
- **Must** — use `id` only to locate an update; never change it or an immutable Field; update every mutable Field from the complete supplied Entity instance.
- **Must** — return `null` when an id-based update, Enable, Disable, or Get by ID finds no record.
- **Must** — set `is_active` to `true` for Enable and `false` for Disable.
- **Must** — let Delete return `true` when it deletes a record and `false` when it finds none; let Truncate return its deleted-record count.
- **Must** — let List accept optional Filters, an optional Filter Combination enum member, an ordered list of Orders, and an optional limit; use the configured defaults when omitted, and treat `0` or a negative limit as no limit.
- **Must** — use an Entity Field name string, Filter Operator enum member, and value for every Filter; validate the Field name against the selected Entity and support the declared operator vocabulary without complex grouping.
- **Must** — use an Entity Field name string and Order Direction enum member for every Order, in supplied order.
- **Never** — accept an enum value, including a Filter Combination, as a string through a public Database Action.
- **Must** — let Count, Sum, Min, and Max accept optional Filters and a Filter Combination; return `0` for empty Count or Sum and `null` for empty Min or Max; ignore `null` aggregate values.
- **Must** — let Sum, Min, and Max receive an Entity Field name string.
- **Must** — let Execute Command receive a SQL command and bound parameters, execute it through the selected Instance without changing schema, and return rows and affected count as a Command Result.
- **Must** — let Create Tables and Insert Initial Data receive an active Instance and be callable through Interface and as manual commands.

**Database stores Entity values without interpreting their domain meaning**

- **Must** — derive storage structure from Entity declarations published through Model Interface.
- **Must** — apply each Entity Field's declared Type, constraints, indexes, defaults, and persistence metadata through the selected Instance's Engine.
- **Must** — realize every declared Relation as a foreign key from its local Field to the target Entity and target Field.
- **Never** — add application behavior because of a Field or value's domain meaning.

**Database publishes Interface only**

- **Must** — provide Interface as the single gateway through which other Components store, retrieve, and operate on Database data.
- **Must** — publish Database Operations through Interface only.
- **Never** — expose Core or Engine as a consumer surface.

**Core routes requests and handles results**

- **Must** — use Core's Data file to route every Interface request to the selected Instance's implementation file.
- **Must** — materialize returned rows as Model Entity instances when an Operation publishes Entities, and return each result according to the published Operation's contract.

**Each active Instance implements the published Operations**

- **Must** — keep one isolated implementation file for every active Instance.
- **Must** — implement all published Operations with that Instance's Engine and connection parameters.
- **Must** — preserve each Operation's applicable request and result standard.

**Database persists changes atomically**

- **Must** — persist every successful data-changing Operation atomically in its selected Instance.
- **Never** — leave a partial change when a data-changing Operation fails.

**Database publishes Table and Initial Data commands**

- **Must** — provide separate Create Tables and Insert Initial Data commands for a selected active Instance.
