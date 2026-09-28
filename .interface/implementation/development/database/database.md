# Database Definition

Database is the Development Component that persists Entity data and provides standard data Operations.

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

Database persists Entity data and publishes standard data Operations. Its layers are Interface, Data, and Engine.

### Purpose

Database keeps persistence knowledge in one Component. Without that separation, Engine selection, storage behavior, and data-operation handling become inconsistent.

### How It Works

A consumer uses Interface to access Database. Interface exposes the public Operations, then passes each request to Data. Data resolves the applicable Instance and Engine, calls that Engine's implementation, and returns the result through Interface.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Engine** — a declared database technology and, when marked for implementation, its implementation.
- **Instance** — a named database connection and storage identity using one Engine; its active state determines whether Interface publishes it.
- **Instance Enum** — the public enum whose members identify the active Instances available through Interface.
- **Database Configuration** — the generated `config.yaml` record declaring the Engines, Instances, and Settings available to Database.
- **Settings** — component-wide choices such as the default Instance and other shared parameters.
- **Interface** — the only public Database layer, through which consumers discover active Instances and request Database Operations.
- **Operation** — one public Database action published through Interface.
- **Filter** — one condition with an Entity Field name string, a Filter Operator enum member, and a value.
- **Filter Operator** — an enum selecting one supported comparison: `equals`, `not_equals`, `greater_than`, `greater_or_equal`, `less_than`, `less_or_equal`, `in`, `contains`, `starts_with`, `ends_with`, `is_null`, or `is_not_null`.
- **Filter Combination** — an enum selecting how List combines Filters: `AND` or `OR`.
- **Order** — one ordering instruction with an Entity Field name string and an Order Direction enum member.
- **Order Direction** — an enum selecting `ascending` or `descending`.
- **Command Result** — the standard result of Execute Command, with `rows` and `affected_count`; either value is `null` when it does not apply. Each row is a mapping from column name to value.
- **Execute Command** — an Operation that receives a SQL command and bound parameters, executes it through the selected Engine, and returns a Command Result.
- **Data** — the internal layer that routes Database Operations, resolves a request's Instance and Engine, and calls that Engine's implementation.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Database
├── interface
├── core/
│   └── data
├── engine/
│   └── <engine>
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

The only public Database layer. It publishes the Instance Enum for every active configured Instance and makes Database Operations available to consumers. Operations use an Entity class or Entity instance directly, as appropriate; they never select data by a Model name or identity. Every Operation accepts an optional Instance Enum member; when omitted, Database uses its configured default Instance.

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

### Core

The internal directory for Database files that are independent of any Engine. Its `data` file defines every Database Operation, resolves the requested Instance and Engine, calls the matching Engine implementation, materializes returned rows as Model Entity instances where an Operation publishes Entities, and returns the result according to the published Operation's contract.

### Engine

The internal layer that keeps each implemented Engine isolated. Each Engine implementation carries out Database Operations with its own parameters and mechanisms.

Database's technical selections, defaults, and layout belong to Database Preferences. The structure of its generated configuration belongs to its Schema. This Definition states only the conceptual layers and the rules that govern them.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Database Principle is mandatory. Database Preferences may provide defaults and stricter conventions, but never weaken or override a Principle. An explicit Target requirement and an applicable Principle take precedence over a Preference.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Database consumes Model without owning it

**Rule:** Database imports Model only through Model Interface and treats the published Entity classes and their public declarations as its complete Model input. Database may derive Tables, foreign keys, and runtime Entity values from that input, but it never changes Model meaning or implementation. Database creates, generates, builds, tests, and documents only its own Component output; it never writes, generates, builds, tests, or creates an artifact under Model's Component directory.

**Why:** Model owns Entity meaning and its own realization. Database needs that meaning as input, while remaining independently owned and realizable.

**Boundary:** A missing Model capability, incompatible Entity definition, or required change to Model is reported to Model's owner. Database does not work around it by importing Model internals or modifying Model.

<br>

### Database has one canonical Architecture

**Rule:** The Database Component root contains one Interface file, one `core` directory, one `engine` directory, one `db` directory, its generated `config.yaml`, and its `README.md`. `core` contains `data` as one of its files and every other Database unit shared across Engines. `data` defines and routes every Database Operation but implements no Engine-specific storage behavior. `engine` contains exactly one implementation file for each Engine marked for implementation. `db` contains the database storage files. The Interface file and README remain at the Component root; only Interface is public. These names and ownership locations are fixed Database Architecture, not configurable preferences.

**Why:** A fixed ownership structure makes Database independently realizable while keeping public access, shared routing, and Engine-specific work separate.

**Boundary:** An Engine implementation does not define public Operations or shared routing. Core does not contain Engine-specific implementation. `db` does not contain source files. Language-specific extensions and package entrypoint files may follow their normal conventions without changing these ownership boundaries.

<br>

### Database configuration declares its available resources

**Rule:** Database Configuration declares every Engine and its engine-specific parameters, every named Instance and its connection parameters, and component Settings such as the default Instance and other shared parameters. Every active Instance names one declared Engine, every configured Instance reference resolves to a declared Instance, and the default Instance is active and names an Engine marked for implementation. Database publishes exactly the active Instances through its Instance Enum. Database Preferences identify which Engines are implemented in generated source.

**Why:** One configuration source makes the available storage resources and their selection explicit.

<br>

### Database exposes explicit Interface Operations

**Rule:** Interface publishes the Operations described in this Component and the Instance Enum for active configured Instances. Each applicable Operation receives an Entity class or Entity instance directly, never a Model name or identity, and accepts an optional Instance Enum member that otherwise resolves to the configured default Instance. A Filter receives an Entity Field name string, a Filter Operator enum member, and a value; supported operators are `equals`, `not_equals`, `greater_than`, `greater_or_equal`, `less_than`, `less_or_equal`, `in`, `contains`, `starts_with`, `ends_with`, `is_null`, and `is_not_null`. List, Count, Sum, Min, and Max accept optional Filters and an optional Filter Combination enum member of `AND` or `OR`; when it is omitted, Filters combine with the configured default, without complex grouping. Each Order receives an Entity Field name string and an Order Direction enum member of `ascending` or `descending`. List alone accepts an ordered list of Orders or the configured default Order, and an optional limit; it uses the configured default limit when omitted, while `0` and every negative limit mean no limit. Interface validates each supplied Field name against the selected Entity. Public Database Actions reject an enum value or Filter Combination supplied as a string; serialized Configuration values are resolved to those runtime values before an Action is called. Count returns `0` for no records; Sum ignores `null` values and returns `0` when no usable value exists; Min and Max ignore `null` values and return `null` when no usable value exists. Add persists the complete supplied Entity instance. Update never changes `id` or an immutable Field and replaces every mutable Field from the complete supplied Entity instance. Execute Command receives a SQL command and bound parameters, executes it through the selected Engine, returns a Command Result, and does not change schema. Database documentation gives each published Interface Operation one complete example.

**Why:** An explicit operation catalogue keeps the public data surface stable and understandable.

**Boundary:** Interface receives and returns requests; it does not select an Engine or implement database-specific behavior.

<br>

### Database treats every Entity value as storage data

**Rule:** Database treats every Entity Field according to its declared Type, constraints, indexes, Default Values, Value Generation, and other persistence metadata. Database realizes that Type through the selected Engine's storage mechanisms. It realizes every declared Relation as a foreign key from the Relation's local Field to its target Entity and target Field; Model declares neither relationship cardinality nor deletion behaviour. A Field with a sensitivity marker, credential, secret, or any other value is ordinary storage data to Database: it stores and returns the Entity value it receives without applying special handling because of that value's meaning.

**Why:** Persistence remains general-purpose and can apply one consistent storage structure to every Entity value.

**Boundary:** Logic owns any application Behaviour that needs special value handling. Database owns only the declared storage structure and constraints of the received Entity values.

<br>

### Database publishes Interface only

**Rule:** Interface is the only public Database layer. Core and Engine are internal implementation layers; consumers use Database only through Interface.

**Why:** One public boundary keeps Engine selection, routing, and shared implementation details out of consumers.

**Boundary:** Interface publishes Database Operations; it does not make a consumer responsible for Data routing or Engine-specific storage behavior.

<br>

### Core routes requests and handles results

**Rule:** Core's Data file receives each request from Interface, resolves the requested Instance and its Engine, forwards the Operation to that Engine implementation, materializes Engine rows as Model Entity instances whenever an Operation publishes Entities, and returns the result according to the published Operation's contract.

**Why:** One Core Data file keeps selection, routing, and result handling consistent across Engines.

**Boundary:** Data coordinates an Operation; each Engine implementation owns the Engine-specific execution of that Operation. Core contains no Engine-specific storage behavior.

<br>

### Each Engine implements the published Operations

**Rule:** Every Engine marked for implementation has an implementation isolated from the other Engines. It implements the published Operations with the Engine's own parameters and mechanisms while preserving the applicable operation request and result standard.

**Why:** Separate Engine implementations make support for each database technology clear and independently maintainable.

**Boundary:** Engine implementations perform storage behavior; the Operation catalogue, routing, and public boundary remain outside them.

<br>

### Database persists changes atomically

**Rule:** Every successful Operation that changes data persists its complete change atomically in the selected Instance. If such an Operation fails, it leaves no partial change in that Instance.

**Why:** Each data change has one reliable result regardless of the selected Engine.

**Boundary:** This applies to data-changing Operations, including a changing Execute Command; it does not restrict the commands Execute Command may receive.

<br>

### Database provisions active Instances

**Rule:** Database provisions every active Instance from Entity metadata and verifies that each contains the required structure for every Entity.

**Why:** An Instance published through Interface must be usable, not only configured.

**Boundary:** SQLModel and Alembic provide the selected Engine's implementation mechanism; Database defines only which active Instances must be usable.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Database configuration declares its available resources**

- **Must** — declare every Engine, its parameters, named Instances, and component Settings in Database Configuration.
- **Must** — identify implemented Engines in Database Preferences.
- **Must** — make every active Instance name a declared Engine, every configured Instance reference resolve to a declared Instance, and the default Instance active.
- **Must** — publish exactly the active Instances through the Instance Enum.

**Database consumes Model without owning it**

- **Must** — consume published Entity classes and public declarations through Model Interface only.
- **Must** — create, generate, build, test, and document only Database's own Component output.
- **Never** — import Model internals or write, generate, build, test, or create an artifact under Model's Component directory.

**Database has one canonical Architecture**

- **Must** — provide one root Interface file, `core/`, `engine/`, `db/`, generated `config.yaml`, and root `README.md`.
- **Must** — keep `data` and every Engine-independent Database unit in `core/`; keep exactly one implementation file for each implemented Engine in `engine/`.
- **Must** — keep database storage files in `db/`.
- **Never** — rename or relocate a canonical Architecture member; put Engine-specific storage behavior in Core, shared routing or public Operations in an Engine file, source files in `db/`, or a public Database surface outside Interface.

**Database exposes explicit Interface Operations**

- **Must** — publish the Operations described by Interface.
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
- **Must** — let Execute Command receive a SQL command and bound parameters, execute it through the selected Engine without changing schema, and return rows and affected count as a Command Result.
- **Must** — give every published Interface Operation one complete documentation example.

**Database treats every Entity value as storage data**

- **Must** — apply each Entity Field's declared Type, constraints, indexes, defaults, and persistence metadata through the selected Engine's storage mechanisms.
- **Must** — realize every declared Relation as a foreign key from its local Field to the target Entity and target Field.
- **Must** — treat Fields with sensitivity markers, credentials, secrets, and other values as ordinary storage data.
- **Never** — apply special storage behaviour because of a value's meaning.

**Database publishes Interface only**

- **Must** — publish Database Operations through Interface only.
- **Never** — expose Core or Engine as a consumer surface.

**Core routes requests and handles results**

- **Must** — use Core's Data file to route every Interface request to the resolved Instance and Engine.
- **Must** — materialize Engine rows as Model Entity instances when an Operation publishes Entities, and return each Engine result according to the published Operation's contract.

**Each Engine implements the published Operations**

- **Must** — keep an isolated implementation for every Engine marked for implementation.
- **Must** — implement published Operations with the selected Engine's parameters and mechanisms.
- **Must** — preserve each Operation's applicable request and result standard.

**Database persists changes atomically**

- **Must** — persist every successful data-changing Operation atomically in its selected Instance.
- **Never** — leave a partial change when a data-changing Operation fails.

**Database provisions active Instances**

- **Must** — provision every active Instance from Entity metadata.
- **Must** — verify required storage structure for every Entity on each active Instance.
