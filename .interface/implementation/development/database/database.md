# Database Definition

Database is the Development Component that persists Model data and provides standard data operations to Logic.

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

Database is the Development Component that persists Model data and publishes data Operations to Logic. Its layers are Interface, Data, Engine, and Core.

### Purpose

Database keeps persistence knowledge in one Component. Without that separation, Engine selection, storage behavior, and data-operation handling spread into Logic and become inconsistent.

### How It Works

Logic uses Interface to access Database. Interface exposes the public Actions, then passes each request to Data. Data resolves the applicable Instance and Engine, calls that Engine's implementation, and returns the result through Interface. Core contains the shared internal files needed by those layers.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Engine** — a declared database technology and, when marked for implementation, its implementation.
- **Instance** — a named database connection and storage identity using one Engine.
- **Database Configuration** — the declared Engines, Instances, and Settings available to Database.
- **Settings** — component-wide choices such as the default Instance, purpose-to-Instance assignments, and secret references.
- **Interface** — the only public Database layer, through which Logic imports Database classes and requests Database Operations.
- **Operation** — one public Database action published through Interface.
- **Execute Command** — an Operation that executes a declared database command whose purpose does not directly concern one Model.
- **Data** — the internal file that provides the Database Actions, resolves a request's Instance and Engine, and calls that Engine's implementation.
- **Core** — the internal directory for shared files required by Database's layers.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Database
├── Interface
├── Data
├── Engine
└── Core
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — imports Entity classes published by Model Interface and uses their SQLModel metadata to create Tables and recognize Entity-form data.
- **Provides to Logic** — exposes Database Operations through Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

### Interface

The only public Database layer. It makes Database classes and Operations available to Logic. Operations use an imported Entity class or Entity instance directly, as appropriate; they never select data by a Model name or identity.

#### Operations

- **Add** — accepts an Entity instance for a new record; returns the created record or operation outcome.
- **Edit** — accepts an imported Entity class and record identifier; returns that record in editable form or a not-found outcome.
- **Update** — accepts an Entity instance containing its record identifier and changed values; returns the updated record or operation outcome.
- **List** — accepts an imported Entity class, optional filters, and optional field ordering; returns matching records.
- **Delete** — accepts an imported Entity class and record identifier; returns the deletion outcome.
- **Enable** — accepts an imported Entity class and record identifier; returns the enabled record or operation outcome.
- **Disable** — accepts an imported Entity class and record identifier; returns the disabled record or operation outcome.
- **Get by ID** — accepts an imported Entity class and record identifier; returns the matching record or a not-found outcome.
- **Count** — accepts an imported Entity class and optional filters; returns the number of matching records.
- **Sum** — accepts an imported Entity class, one numeric field, and optional filters; returns that field's total across matching records.
- **Min** — accepts an imported Entity class, one comparable field, and optional filters; returns the smallest matching value.
- **Max** — accepts an imported Entity class, one comparable field, and optional filters; returns the largest matching value.
- **Truncate** — accepts an imported Entity class; removes all of its records while keeping its Table structure.
- **Report** — accepts report-specific selection criteria; returns the requested report without requiring one Model as its subject.
- **Execute Command** — accepts a declared command and its supplied parameters; returns that command's result or operation outcome. Its purpose need not concern one Model.

### Data

The internal file that provides every Database Action. It resolves the requested Instance and Engine, calls the matching Engine Action, and standardizes returned data when required.

### Engine

The internal directory containing one file for every Engine marked for implementation. Each file performs the Database Actions with that Engine's own packages, parameters, and mechanisms.

### Core

The internal directory for shared Database files that support Interface, Data, and Engine without becoming part of the public Database surface.

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

**Rule:** Database Configuration declares every Engine and its engine-specific parameters, every named Instance and its connection parameters, and component Settings such as the default Instance, purpose assignments, secret references, and other shared parameters. Every Instance names one declared Engine, and every configured Instance reference resolves to a declared Instance. Database Preferences identify which Engines are implemented in generated source.

**Why:** One configuration source makes the available storage resources and their selection explicit.

<br>

### Database exposes explicit Interface Operations

**Rule:** Interface publishes the Operations described in this Component. Each applicable Operation receives an imported Entity class or Entity instance directly, never a Model name or identity. List accepts optional filters and optional ordering by field; Count, Sum, Min, and Max accept optional filters. Execute Command may perform a declared database command that does not directly concern one Model. Database documentation gives each published Interface Operation one complete example.

**Why:** An explicit operation catalogue keeps the public data surface stable and understandable.

**Boundary:** Interface receives and returns requests; it does not select an Engine or implement database-specific behavior.

<br>

### Database publishes Interface only

**Rule:** Interface is the only public Database layer. Data, Engine, and Core are internal implementation layers; consumers use Database only through Interface.

**Why:** One public boundary keeps Engine selection, routing, and shared implementation details out of consumers.

**Boundary:** Interface publishes Database Actions; it does not make a consumer responsible for Data routing, Engine-specific storage behavior, or Core implementation.

<br>

### Data routes requests and handles results

**Rule:** Data receives each request from Interface, resolves the requested Instance and its Engine, forwards the Operation to that Engine implementation, and standardizes the returned data when required before returning it to Interface. Data provides one Action for each published Operation.

**Why:** A single Data file keeps selection, translation, and result handling consistent across Engines.

**Boundary:** Data coordinates an Operation; each Engine implementation owns the Engine-specific execution of that Operation.

<br>

### Each Engine implements the published Operations

**Rule:** Every Engine marked for implementation has an implementation isolated from the other Engines. It implements the published Operations with the Engine's own packages, parameters, and mechanisms while preserving the applicable operation request and result standard.

**Why:** Separate Engine implementations make support for each database technology clear and independently maintainable.

**Boundary:** Engine implementations perform storage behavior; the Operation catalogue, routing, and public boundary remain outside them.

<br>

### Database connects Model to Logic

**Rule:** Database independently imports Entity classes only through Model Interface; it does not obtain them through Logic. After all Entity classes are imported, Database uses their SQLModel metadata to create Tables and compare migrations. Database does not create a separate persistence model or duplicate Entity Fields, constraints, relationships, or indexes; it provides its Interface Operations to Logic.

**Why:** This keeps persistence aligned with one authoritative Entity model while allowing Database to build storage independently and giving Logic one consistent data boundary.

**Boundary:** Model owns Entity declarations; Logic owns application behavior; Database owns table creation, migration comparison, and persistence implementation between them.

<br>

### Development provisions the default Database Instance

**Rule:** A successful Develop execution for Database applies the generated migration to the configured default Instance. For file-backed storage, that execution creates the configured database file in the configured Database Directory. Develop verifies that the storage contains every imported Entity table before it reports Database development as complete.

**Why:** A developed Database Component must leave a usable default storage instance, not only source code and a command that could create it later.

**Boundary:** This provisions only the configured default Instance. Other Instances are created only when their own configuration and execution are requested.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Database configuration declares its available resources**

- **Must** — declare every Engine, its parameters, named Instances, and component Settings in Database Configuration.
- **Must** — identify implemented Engines in Database Preferences.
- **Must** — make every Instance name a declared Engine and every configured Instance reference resolve to a declared Instance.

**Database exposes explicit Interface Operations**

- **Must** — publish the Operations described by Interface.
- **Must** — receive an imported Entity class or Entity instance directly, never a Model name or identity.
- **Must** — let List accept optional filters and optional field ordering.
- **Must** — let Count, Sum, Min, and Max accept optional filters.
- **Must** — let Execute Command perform a declared database command that does not directly concern one Model.
- **Must** — give every published Interface Operation one complete documentation example.

**Database publishes Interface only**

- **Must** — publish Database classes and Operations through Interface only.
- **Never** — expose Data, Engine, or Core as a consumer surface.

**Data routes requests and handles results**

- **Must** — route every Interface request to the resolved Instance and Engine.
- **Must** — provide one Data Action for each published Operation.
- **Must** — standardize returned data whenever that Operation requires it.

**Each Engine implements the published Operations**

- **Must** — keep an isolated implementation for every Engine marked for implementation.
- **Must** — implement published Operations with the selected Engine's packages, parameters, and mechanisms.
- **Must** — preserve each Operation's applicable request and result standard.

**Database connects Model to Logic**

- **Must** — independently import Entity classes through Model Interface, never through Logic.
- **Must** — use imported Entity SQLModel metadata for table creation and migration comparison.
- **Never** — create a separate persistence model or duplicate Entity Fields, constraints, relationships, or indexes.
- **Must** — provide Interface Operations to Logic through Interface.

**Development provisions the default Database Instance**

- **Must** — apply the generated migration to the configured default Instance during successful Database development.
- **Must** — create file-backed default storage in the configured Database Directory.
- **Must** — verify every imported Entity table before reporting Database development complete.
