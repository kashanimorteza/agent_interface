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
- **Instance** — a named database connection and storage identity using one Engine.
- **Database Configuration** — the declared Engines, Instances, and Settings available to Database.
- **Settings** — component-wide choices such as the default Instance, purpose-to-Instance assignments, and other shared parameters.
- **Interface** — the only public Database layer, through which consumers request Database Operations.
- **Operation** — one public Database action published through Interface.
- **Filter** — one condition with a `field`, an `operator`, and a `value`.
- **Order** — one ordering instruction with a `field` and a `direction` of `ascending` or `descending`.
- **Command Result** — the standard result of Execute Command, with `rows` and `affected_count`; either value is `null` when it does not apply. Each row is a mapping from column name to value.
- **Execute Command** — an Operation that receives a SQL command and optional parameters, executes it through the selected Engine, and returns a Command Result.
- **Data** — the internal layer that routes Database Operations, resolves a request's Instance and Engine, and calls that Engine's implementation.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Database
├── Interface
├── Data
└── Engine
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — uses Entity classes to derive storage structure and recognize Entity-form data; uses Model Interface for other Model use.
- **Provides to Logic** — exposes Database Operations through Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The only public Database layer. It makes Database Operations available to consumers. Operations use an Entity class or Entity instance directly, as appropriate; they never select data by a Model name or identity. Every Operation accepts an optional Instance; when omitted, Database uses its configured default Instance.

#### Operations

- **Add** — accepts an Entity instance for a new record; applies every declared Value Generation, otherwise applies Default Values for omitted Fields, then enforces required and nullability Rules; returns the created Entity instance.
- **Update** — accepts an Entity instance containing its `id` and changed values; uses `id` only to locate the record, never changes it, updates only supplied mutable Fields, preserves omitted or immutable Fields, treats an explicitly supplied `null` as a value, and returns the updated Entity instance or `null` when no record has that `id`.
- **List** — accepts an Entity class, optional Filters, an optional `filter_combination` of `AND` or `OR`, an optional ordered list of Orders, and an optional limit; uses the configured default filter combination and Order when either is omitted, returns every matching Entity when limit is omitted, and returns matching Entity instances.
- **Delete** — accepts an Entity class and record `id`; returns `true` when it deletes a record and `false` when no record has that `id`.
- **Enable** — accepts an Entity class and record `id`; sets its `is_active` Field to `true` and returns the Entity instance or `null` when no record has that `id`.
- **Disable** — accepts an Entity class and record `id`; sets its `is_active` Field to `false` and returns the Entity instance or `null` when no record has that `id`.
- **Get by ID** — accepts an Entity class and record `id`; returns the matching Entity instance or `null` when no record has that `id`.
- **Count** — accepts an Entity class; returns the number of records.
- **Sum** — accepts an Entity class and one numeric field; ignores `null` values and returns that field's total, or `0` when no usable value exists.
- **Min** — accepts an Entity class and one comparable field; ignores `null` values and returns the smallest value, or `null` when no usable value exists.
- **Max** — accepts an Entity class and one comparable field; ignores `null` values and returns the largest value, or `null` when no usable value exists.
- **Truncate** — accepts an Entity class; removes all of its records while keeping its Table structure and returns the number of deleted records.
- **Execute Command** — accepts a SQL command and optional parameters; executes it through the selected Engine and returns a Command Result. Its purpose need not concern one Model.

### Data

The internal layer that routes every Database Operation. It resolves the requested Instance and Engine, calls the matching Engine implementation, and returns that result according to the published Operation's contract.

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

### Database configuration declares its available resources

**Rule:** Database Configuration declares every Engine and its engine-specific parameters, every named Instance and its connection parameters, and component Settings such as the default Instance, purpose assignments, and other shared parameters. Every Instance names one declared Engine, every configured Instance reference resolves to a declared Instance, and the default Instance names an Engine marked for implementation. Database Preferences identify which Engines are implemented in generated source.

**Why:** One configuration source makes the available storage resources and their selection explicit.

<br>

### Database exposes explicit Interface Operations

**Rule:** Interface publishes the Operations described in this Component. Each applicable Operation receives an Entity class or Entity instance directly, never a Model name or identity, and accepts an optional Instance that otherwise resolves to the configured default Instance. A Filter has a field, operator, and value; supported operators are `equals`, `not_equals`, `greater_than`, `greater_or_equal`, `less_than`, `less_or_equal`, `in`, `contains`, `starts_with`, `ends_with`, `is_null`, and `is_not_null`. List accepts an optional `filter_combination` of `AND` or `OR`; when it is omitted, Filters combine with the configured default, without complex grouping. Each Order has a field and ascending or descending direction; List alone accepts Filters, an ordered list of Orders or the configured default Order, and an optional limit; it returns every matching Entity when limit is omitted. Count returns `0` for no records; Sum ignores `null` values and returns `0` when no usable value exists; Min and Max ignore `null` values and return `null` when no usable value exists. Add applies every Entity Value Generation or Default Value according to Model Declaration. Update never changes `id` or an immutable Field. Execute Command receives a SQL command and optional parameters, executes it through the selected Engine, and returns a Command Result. Database documentation gives each published Interface Operation one complete example.

**Why:** An explicit operation catalogue keeps the public data surface stable and understandable.

**Boundary:** Interface receives and returns requests; it does not select an Engine or implement database-specific behavior.

<br>

### Database treats every Entity value as storage data

**Rule:** Database treats every Entity Field according to its declared logical Type, constraints, relationships, indexes, Default Values, Value Generation, and other persistence metadata. Database realizes that logical Type through the selected Engine's storage mechanisms. It realizes every Reference against its target Entity `id`, declared cardinality, and Model Preferences' configured `on_delete` behaviour. A Field with a sensitivity marker, credential, secret, or any other value is ordinary storage data to Database: it stores and returns the Entity value it receives without applying special handling because of that value's meaning.

**Why:** Persistence remains general-purpose and can apply one consistent storage structure to every Entity value.

**Boundary:** Logic owns any application Behaviour that needs special value handling. Database owns only the declared storage structure and constraints of the received Entity values.

<br>

### Database publishes Interface only

**Rule:** Interface is the only public Database layer. Data and Engine are internal implementation layers; consumers use Database only through Interface.

**Why:** One public boundary keeps Engine selection, routing, and shared implementation details out of consumers.

**Boundary:** Interface publishes Database Operations; it does not make a consumer responsible for Data routing or Engine-specific storage behavior.

<br>

### Data routes requests and handles results

**Rule:** Data receives each request from Interface, resolves the requested Instance and its Engine, forwards the Operation to that Engine implementation, and returns that Engine result according to the published Operation's contract.

**Why:** One Data layer keeps selection, routing, and result handling consistent across Engines.

**Boundary:** Data coordinates an Operation; each Engine implementation owns the Engine-specific execution of that Operation.

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

### Database provisions the default Instance

**Rule:** Database provisions its configured default Instance from Entity metadata and verifies that the Instance contains the required structure for every Entity.

**Why:** A Database Component must leave a usable default Instance, not only source code and a command that could create it later.

**Boundary:** This provisions only the configured default Instance. Other Instances are provisioned when their own configuration is requested.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Database configuration declares its available resources**

- **Must** — declare every Engine, its parameters, named Instances, and component Settings in Database Configuration.
- **Must** — identify implemented Engines in Database Preferences.
- **Must** — make every Instance name a declared Engine and every configured Instance reference resolve to a declared Instance.
- **Must** — make the default Instance use an Engine marked for implementation.

**Database exposes explicit Interface Operations**

- **Must** — publish the Operations described by Interface.
- **Must** — receive an Entity class or Entity instance directly, never a Model name or identity.
- **Must** — accept an optional Instance and use the configured default Instance when it is omitted.
- **Must** — apply every declared Value Generation, then Default Value, then required and nullability Rule during Add.
- **Must** — use `id` only to locate an update; never change it or an immutable Field; update only supplied mutable Fields and preserve omitted Fields.
- **Must** — return `null` when an id-based update, Enable, Disable, or Get by ID finds no record.
- **Must** — set `is_active` to `true` for Enable and `false` for Disable.
- **Must** — let Delete return `true` when it deletes a record and `false` when it finds none; let Truncate return its deleted-record count.
- **Must** — let List accept optional Filters, an optional `filter_combination` of `AND` or `OR`, an ordered list of Orders, and an optional limit; use the configured defaults when either combination or Orders are omitted and return all matches when limit is omitted.
- **Must** — use `field`, `operator`, and `value` Filters; support the declared operator vocabulary without complex grouping.
- **Must** — use Orders with a Field and ascending or descending direction, in supplied order.
- **Must** — return `0` for empty Count or Sum and `null` for empty Min or Max; ignore `null` aggregate values.
- **Must** — let Execute Command receive a SQL command and optional parameters, execute it through the selected Engine, and return rows and affected count as a Command Result.
- **Must** — give every published Interface Operation one complete documentation example.

**Database treats every Entity value as storage data**

- **Must** — apply each Entity Field's declared logical Type, constraints, relationships, indexes, defaults, and persistence metadata through the selected Engine's storage mechanisms.
- **Must** — treat Fields with sensitivity markers, credentials, secrets, and other values as ordinary storage data.
- **Never** — apply special storage behaviour because of a value's meaning.

**Database publishes Interface only**

- **Must** — publish Database Operations through Interface only.
- **Never** — expose Data or Engine as a consumer surface.

**Data routes requests and handles results**

- **Must** — route every Interface request to the resolved Instance and Engine.
- **Must** — return each Engine result according to the published Operation's contract.

**Each Engine implements the published Operations**

- **Must** — keep an isolated implementation for every Engine marked for implementation.
- **Must** — implement published Operations with the selected Engine's parameters and mechanisms.
- **Must** — preserve each Operation's applicable request and result standard.

**Database persists changes atomically**

- **Must** — persist every successful data-changing Operation atomically in its selected Instance.
- **Never** — leave a partial change when a data-changing Operation fails.

**Database provisions the default Instance**

- **Must** — provision the configured default Instance from Entity metadata.
- **Must** — verify required storage structure for every Entity.
