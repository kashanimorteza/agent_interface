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

Database is the Development Component that persists Model data and publishes data Operations to Logic. Its layers are Interface, Mapping, and Engine.

### Purpose

Database keeps persistence knowledge in one Component. Without that separation, Engine selection, storage behavior, and data-operation handling spread into Logic and become inconsistent.

### How It Works

Logic sends an Operation request through Interface. Mapping resolves the applicable Instance and Engine, passes the request to that Engine, standardizes the result when needed, and returns it through Interface.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Engine** — a supported database technology and its implementation.
- **Instance** — a named database connection and storage identity using one Engine.
- **Database Configuration** — the declared Engines, Instances, and Settings available to Database.
- **Settings** — component-wide choices such as the default Instance, purpose-to-Instance assignments, and secret references.
- **Interface** — the public boundary through which Logic requests Database Operations.
- **Operation** — one public Database action published through Interface.
- **Execute Command** — an Operation that executes a declared database command whose purpose does not directly concern one Model.
- **Mapping** — the public layer that routes a request to its Instance and Engine and standardizes its result when needed.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Database
├── Interface
├── Mapping
└── Engine
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

The public layer that receives Operation requests from Logic and returns their results. Operations use an imported Entity class or Entity instance directly, as appropriate; they never select data by a Model name or identity.

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

### Mapping

The public layer that resolves and handles requests: it resolves the requested Instance and Engine, routes the Operation, and standardizes returned data when required.

### Engine

The public layer that performs storage behaviour for each Engine-specific implementation.

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

**Rule:** Database Configuration declares every supported Engine, its engine-specific parameters, every named Instance and its connection parameters, and component Settings such as the default Instance, purpose assignments, secret references, and other shared parameters. Every Instance names one declared Engine, and every configured Instance reference resolves to a declared Instance.

**Why:** One configuration source makes the available storage resources and their selection explicit.

<br>

### Database exposes explicit Interface Operations

**Rule:** Interface publishes the Operations described in this Component. Each applicable Operation receives an imported Entity class or Entity instance directly, never a Model name or identity. List accepts optional filters and optional ordering by field; Count, Sum, Min, and Max accept optional filters. Execute Command may perform a declared database command that does not directly concern one Model. Database documentation gives each published Interface Operation one complete example.

**Why:** An explicit operation catalogue keeps the public data surface stable and understandable.

**Boundary:** Interface receives and returns requests; it does not select an Engine or implement database-specific behavior.

<br>

### Database publishes all of its classes

**Rule:** Interface, Mapping, and Engine classes are public. Interface is the standard entry point for Database Operations, while a consumer with a declared Connection may use any public Database class when needed.

**Why:** Every Database class remains available without obscuring the standard operation boundary.

**Boundary:** Public access does not make a consumer responsible for routing or Engine-specific storage behavior.

<br>

### Mapping routes requests and handles results

**Rule:** Mapping receives each request from Interface, resolves the requested Instance and its Engine, forwards the Operation to that Engine implementation, and standardizes the returned data when required before returning it to Interface. Mapping provides one mapping action for each published Operation.

**Why:** A single routing layer keeps selection, translation, and result handling consistent across Engines.

**Boundary:** Mapping coordinates an operation; each Engine implementation owns the Engine-specific execution of that operation.

<br>

### Each Engine implements the published Operations

**Rule:** Every declared Engine has an implementation isolated from the other Engines. It implements the published Operations with the Engine's own packages, parameters, and mechanisms while preserving the applicable operation request and result standard.

**Why:** Separate Engine implementations make support for each database technology clear and independently maintainable.

**Boundary:** Engine implementations perform storage behavior; the Operation catalogue, routing, and public boundary remain outside them.

<br>

### Database connects Model to Logic

**Rule:** Database imports Entity classes only through Model Interface. After all Entity classes are imported, Database uses SQLModel metadata to create Tables and compare migrations. Database does not create a separate persistence model or duplicate Entity Fields, constraints, relationships, or indexes; it provides its Interface Operations to Logic.

**Why:** This keeps persistence aligned with one authoritative Entity model while giving Logic one consistent data boundary.

**Boundary:** Model owns Entity declarations; Logic owns application behavior; Database owns table creation, migration comparison, and persistence implementation between them.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Database configuration declares its available resources**

- **Must** — declare every supported Engine, its parameters, named Instances, and component Settings in Database Configuration.
- **Must** — make every Instance name a declared Engine and every configured Instance reference resolve to a declared Instance.

**Database exposes explicit Interface Operations**

- **Must** — publish the Operations described by Interface.
- **Must** — receive an imported Entity class or Entity instance directly, never a Model name or identity.
- **Must** — let List accept optional filters and optional field ordering.
- **Must** — let Count, Sum, Min, and Max accept optional filters.
- **Must** — let Execute Command perform a declared database command that does not directly concern one Model.
- **Must** — give every published Interface Operation one complete documentation example.

**Database publishes all of its classes**

- **Must** — keep Interface, Mapping, and Engine classes public.
- **Must** — retain Interface as the standard entry point for Database Operations while allowing a declared consumer to use any public Database class when needed.

**Mapping routes requests and handles results**

- **Must** — route every Interface request to the resolved Instance and Engine.
- **Must** — provide one Mapping function for each published Operation.
- **Must** — standardize returned data whenever that Operation requires it.

**Each Engine implements the published Operations**

- **Must** — keep an isolated implementation for every declared Engine.
- **Must** — implement published Operations with the selected Engine's packages, parameters, and mechanisms.
- **Must** — preserve each Operation's applicable request and result standard.

**Database connects Model to Logic**

- **Must** — import Entity classes through Model Interface and use SQLModel metadata for table creation and migration comparison.
- **Never** — create a separate persistence model or duplicate Entity Fields, constraints, relationships, or indexes.
- **Must** — provide Interface Operations to Logic through Interface.
