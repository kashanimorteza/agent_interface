# Database Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Understanding](#understanding)**
   - **[Database configuration](#database-configuration)**
3. **[Terms](#terms)**
4. **[Architecture](#architecture)**
5. **[Relationships](#relationships)**
6. **[Documentation](#documentation)**
7. **[Principles](#principles)**
   - **[Database is an independent package with one public boundary](#database-is-an-independent-package-with-one-public-boundary)**
   - **[Database has three ordered internal layers](#database-has-three-ordered-internal-layers)**
   - **[Storage is derived from Model and invents nothing](#storage-is-derived-from-model-and-invents-nothing)**
   - **[Engine-specific decisions are explicit and isolated](#engine-specific-decisions-are-explicit-and-isolated)**
   - **[The complete Database is reproducible from the repository](#the-complete-database-is-reproducible-from-the-repository)**
   - **[Storage changes use ordered and recoverable Migrations](#storage-changes-use-ordered-and-recoverable-migrations)**
   - **[Database owns the complete persistence responsibility](#database-owns-the-complete-persistence-responsibility)**
   - **[All data access uses one generic Database Interface](#all-data-access-uses-one-generic-database-interface)**
   - **[Database Instances are explicit and selectable](#database-instances-are-explicit-and-selectable)**
   - **[Every stored structure is traceable to a Model declaration](#every-stored-structure-is-traceable-to-a-model-declaration)**
   - **[Credential storage protects values at rest](#credential-storage-protects-values-at-rest)**
   - **[Declared Initial Data preserves its meaning](#declared-initial-data-preserves-its-meaning)**
   - **[Related operations share an explicit Transaction boundary](#related-operations-share-an-explicit-transaction-boundary)**
   - **[Persistence security and observability remain bounded](#persistence-security-and-observability-remain-bounded)**
8. **[At a Glance](#at-a-glance)**
<br>

## Introduction

### Overview

Database owns the complete persistence boundary of the Target. It maps the logical Model to durable storage, preserves storage-level guarantees, and exposes one generic public interface through which consumers use persistent data without depending on private persistence details.

Database is independent of any particular storage technology, package, version, or runtime destination. What it does not own is stated in Principle "Database owns the complete persistence responsibility".

### Purpose

Data outlives every process that touches it, and the rules that keep it correct — this record exists once, that reference points at something real, these two changes happen together or not at all — can only be enforced where all the records are. A consumer holds one request at a time and cannot see the set, so a guarantee left to consumers is a guarantee that holds until two of them run at once.

Database exists to be the one place that sees the whole set. It turns the logical Model into durable storage, enforces the guarantees that storage can enforce, records every structural change as an ordered Migration, and hands consumers one generic interface instead of one route per Model. Everything about how that is done — which Engine, which mapping, which indexes, which connection — stays behind that interface.

Without it, persistence would be everywhere and owned by nobody: a query built by hand in one consumer, a schema change applied directly in another, a uniqueness rule checked in code that races the next writer, and no way to rebuild the database from the repository because no ordered history of it exists. Those are not inconveniences; they are how stored data quietly stops being trustworthy.

### How It Works

A consumer names a Model and an operation on the Database Interface. It never names a table, builds a query, or receives a connection: it passes the public Model type or instance and the criteria that operation needs, and one Model-driven pipeline serves every Model rather than one implementation per Model.

Behind that interface the work passes through three ordered layers. The Database Interface receives the request; Data Logic and Mapping resolves how that Model and its declarations are represented and enforced in storage; the Storage Adapter owns the connections to the selected Engine and performs the operation. Dependencies run in that order, and no layer reaches past the one that owns the next boundary.

What the storage looks like is derived from Model rather than decided here. Database reads the declarations Model publishes — identity, field types, optionality, defaults, uniqueness, and relationships with their references and cardinality — and turns them into physical structure and enforcement, adding only what persistence itself requires. A declaration that is missing or ambiguous is reported, never guessed from a name.

Structure changes only through Migrations, in a recorded order, so the current schema can be explained, reproduced from the repository, and recovered. At startup the declared structure is applied, integrity is verified, and declared Initial Data is imported; an Instance is not ready until that completes. Which Instances exist, how each reaches its Engine, and the credentials each uses are Database's to own and never appear in source.

<br>

## Understanding

How the Human explained this Component, in their own words, and what was decided along the way. The Principles state what holds; this section preserves how they were arrived at. It states no obligation: where this record and a Principle disagree, the Principle is correct.

<br>

### Database configuration

**Where does the database information live?** One YAML file holds the database information. Adding a database, or changing a username or password, is one edit in that file and never a change in source. Several Instances live side by side in it, each with its own Engine, connection settings, and credentials, and one of them is the default. Every Instance carries the same keys, and a key that does not apply to its Engine is left empty rather than removed, so moving an Instance to another Engine means filling values in rather than adding keys. The connection credentials and the at-rest encryption key for persisted credential fields are written in that same file.

**Decisions:**

1. The file is `database/database.yaml`, and its shape is the Database Configuration Schema at `.interface/foundation/schema/database.yaml`.
2. Instances are declared side by side, each with its Engine, connection settings, and credentials; `general` is the default.
3. Every Instance carries the same keys — host, port, path, username, password — and an inapplicable key is left empty rather than removed: host and port for a file-backed Engine, path for a server-backed one, username and password for an Engine that does not authenticate.
4. Connection credentials and the at-rest encryption key live in that file. The earlier rule `store_values_in_configuration: false` — no values in the file, environment-variable names instead, secrets delivered by Platform — is removed, because the Human does not agree with it.
5. The configuration file is part of generating the Database Component, not a step after it. Database is not complete without it, and source hardcodes none of its values.
6. How the file is protected — a distinguishing suffix, git exclusion, or another mechanism — is deliberately undecided and is the Human's to settle later. A proposal to fix a `.auth.yml` suffix and exclude the file from version control was set aside for now; no Principle or Preference assumes an answer.

<br>

## Terms

- **Database Interface** — the only Database boundary published to consumers, exposing generic data operations and Instance discovery and selection.
- **Data Logic and Mapping** — the internal layer that resolves how logical Models and their rules are represented and enforced in storage.
- **Storage Adapter** — the internal layer that owns connections to the selected Engine and performs persistence operations.
- **Engine** — the replaceable storage technology behind the Storage Adapter.
- **Instance** — one selectable database identity with a stable key, name, purpose, and Engine binding.
- **Instance Registry** — the public catalogue through which consumers discover Instance identities and the default without receiving connections or secrets.
- **Migration** — one recorded, ordered change to the storage structure, with a tested reversal when safe and an explicit recovery path when irreversible.
- **At-rest Mode** — the resolved persistence transformation applied to a credential field.
- **Transaction** — one unit of data operations on a single Instance whose changes commit together or roll back together.

<br>

## Architecture

```text
Database
├── Database Interface         ← the only part a consumer sees
├── Data Logic and Mapping     ← how a Model becomes storage
└── Storage Adapter            ← the connection to the selected Engine
```

**Database Interface** publishes the generic data operations and the Instance Registry, and it is the only Database boundary a consumer reaches. It accepts a Model type or instance and the criteria an operation needs; it never hands out a connection, a query, or a table name.

**Data Logic and Mapping** resolves how a logical Model and its published declarations are represented and enforced in storage — identity, types, optionality, defaults, uniqueness, relationships, and the at-rest treatment of a credential field, together with the access paths persistence itself needs. It derives that representation from Model rather than deciding domain meaning, and it reports a missing or ambiguous declaration instead of guessing one.

**Storage Adapter** owns the connections to the selected Engine and performs the operations against it. The Engine is replaceable behind it, and nothing above this layer knows which one is in use.

The three layers are ordered: dependencies run from the interface through mapping and logic to the adapter, and no layer bypasses the one that owns the next boundary.

<br>

## Relationships

- **Consumes Model** — maps and enforces the logical Models, fields, relationships, rules, and declared initial data.
- **Consumes Development** — uses the shared package standard, technical catalogues, connections, and ownership rules.
- **Consumes Platform** — receives runtime Bindings delivered to Database's boundary by the selected Launch Item.
- **Consumed by Logic** — provides the generic data-access interface and Instance Registry through Logic's Data Access boundary.

<br>

Database-owned defaults and implementation conventions belong to Database Preferences. Concrete technical selections and the Platform Launch Item reference belong to the Database Component Profile in Development Preferences. Implementation applies those sources to the current Target.

<br>

## Documentation

Database's documentation is written for a consumer who will never open a connection. It covers the one Database Interface as Development's documentation rules require — every operation it offers, what each accepts and returns, and how a consumer names a Model by its imported type — together with the Instance Registry: which Instances exist, which is the default, and how one is selected. It shows a runnable example of each kind of operation and of the Transaction boundary.

It stops at that boundary. The three internal layers, the mapping rules, the Migration history, the Engine in use, and how Database is configured are not explained to consumers: a consumer who learns them would start to depend on them, and the Interface exists so that they do not have to. The reader must finish able to store, read, change, and remove data, and to group related operations in one Transaction, without knowing which Engine holds it or how a Model became a table.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## Principles

Every Principle below is mandatory.

<br>

### Database is an independent package with one public boundary

**Rule:** Database is an independent package with a stable public namespace and documented Database Interface. It imports logical Model types only through the Model Public Interface, does not redefine or privately copy them, and publishes its generic gateway and Instance Registry through its own boundary.

**Why:** One independent package gives persistence one replaceable ownership boundary while allowing authorized consumers to reuse it.

**Boundary:** Consumers never import private adapters, mappings, connections, files, or configuration. Migration is internal Database tooling and is not part of the public runtime interface.

<br>

### Database has three ordered internal layers

**Rule:** Database is formed from three distinct internal layers: Database Interface, Data Logic and Mapping, and Storage Adapter. Dependencies flow from the public interface through mapping and logic to the adapter and selected Engine.

**Why:** An ordered internal chain lets the public operations, mapping rules, and storage technology evolve independently.

**Boundary:** An internal layer never bypasses the layer responsible for the next boundary, and consumers never bypass Database Interface.

<br>

### Storage is derived from Model and invents nothing

**Rule:** Physical persistence is derived from the logical Model and the declarations it publishes. Database preserves Model identity, field meaning, relationships, constraints, and applicable rules, and adds only the storage representation, durability, and enforcement that persistence itself requires. Database never invents a Model, field, relationship, rule, or initial record because storage makes it convenient, and it never weakens one: a persistence rule the selected Engine cannot express directly is enforced equivalently within Database or reported.

**Why:** Consumers need durable data that still means what the Model said it means. A storage layer that may add or reinterpret a definition becomes a second authority on the domain, and the two answers drift apart the first time either changes.

**Boundary:** Application-context and operation-dependent behavior stays outside Database. Database adds what persistence needs — among it the access paths, so an index is Database's decision and never a Model declaration — without that addition changing what any definition means.

<br>

### Engine-specific decisions are explicit and isolated

**Rule:** The portable persistence contract and its mapping remain understandable without knowing which Engine holds the data. Every persistence decision is classified as portable contract, portable mapping, or Engine-specific extension, and an Engine-specific type, command, index, or capability is declared as such and isolated behind the Storage Adapter. Schema integrity is verified against the recorded structure, and drift is reported rather than absorbed.

**Why:** An Engine is replaceable only while the promises made to consumers do not depend on it. An extension that is never marked as one becomes an unwritten requirement that the next Engine cannot meet.

**Boundary:** Engine selection is a technical choice resolved outside this file and never becomes a consumer-facing guarantee unless it is declared as one. A Preference may select an Engine-specific feature; it cannot silently change the portable contract. Application code never repairs drift on its own.

<br>

### The complete Database is reproducible from the repository

**Rule:** Everything needed to recreate the Database belongs to the repository: storage structure, migration history, constraints, indexes, and declared initial data.

**Why:** A new environment or checkout can rebuild an equivalent Database without undocumented manual work.

**Boundary:** This covers the Database's structure, not the access to it. Which Instances a given environment has, how each reaches its Engine, and the credentials and keys it uses are supplied by that environment, and the repository may deliberately not carry them. A fresh checkout reproduces an equivalent structure; connecting to it still requires what that environment supplies. No Database structure exists only in a running server, memory, or an unrecorded manual step.

<br>

### Storage changes use ordered and recoverable Migrations

**Rule:** Storage structure never changes without a recorded Migration in an ordered history. A Migration has a tested reversal when semantically safe. A data-losing or data-transforming Migration may be irreversible only when explicitly marked, protected by an approved recovery procedure, and accompanied by a documented recovery path.

**Why:** Ordered history explains, reproduces, and safely recovers the current structure.

**Boundary:** Application code never creates, alters, or drops storage objects directly. Migration execution verifies ordering, integrity, drift, and concurrent-run coordination.

<br>

### Database owns the complete persistence responsibility

**Rule:** Persistence is owned by Database alone: how data is stored, reached, constrained, and changed over time is its decision to make and its alone. No other Component stores, queries, or alters stored data, and no other Component may be handed a connection through which it could.

**Why:** Persistence decisions interact — a mapping constrains a migration, a constraint constrains a query, an index follows from both — so they need one authority that can reason about them together. Split across Components, each one is reasonable on its own and the set is incoherent.

**Boundary:** Model owns logical meaning; Logic owns application behavior and service orchestration; Presentation owns presentation; Platform operates the result. Database owns only its own private runtime settings and secrets, and it makes no application decision merely because the data passes through it.

<br>

### All data access uses one generic Database Interface

**Rule:** Consumers use one generic Database Interface for every persistent Model. The interface accepts a public Model type or instance, a supported operation, and the criteria required by that operation. It supports create, read, read-by-identifier, list, search, update, and delete operations, the aggregate reads that answer a question about a matching set rather than its records — how many, and the total, smallest, and largest value of one field — and the removal of every record of a Model while its structure stays in place, all through one Model-driven pipeline rather than one implementation per Model.

Public operations never require a Model name encoded as an untyped string or resolve a Model through an untyped string registry. Model identity is carried by the imported type or instance.

The interface may also expose a capability-restricted command route for data operations that cannot be expressed through standard operations. It requires explicit parameters, protected identifiers, separate observability, transaction participation, and explicit Engine identification. It rejects structural changes, privilege changes, connection administration, and Migration operations.

**Why:** One generic pipeline serves every Model while preserving a stable public boundary and preventing duplicate business-logic implementations.

**Boundary:** The interface offers persistence operations and no domain ones: enabling or disabling a record is an `update` of the Field the Model declares for it, not an operation of its own, because a name that carries domain meaning at this boundary makes Database a second place where the domain is decided. Consumers never receive connections or storage access. The command route cannot bypass Model validation, persistence constraints, credential protections, Migrations, or the public transaction boundary. Model-specific application behavior remains in Logic.

<br>

### Database Instances are explicit and selectable

**Rule:** Every Database Instance has a stable identifier, human-readable name, stated purpose, and one supported Engine binding. Database publishes an Instance Registry through its public interface. Exactly one Instance is the default; an omitted selection uses it, while an unknown explicit selection is rejected.

The Registry is derived from the configured Instance collection, and the number of Instances is never maintained as a separate authority.

**Why:** Named Instances let consumers choose a database by purpose without learning how it connects.

**Boundary:** The Registry exposes no raw connection objects or secret values. Instances, their connection settings, and their credentials are owned by Database alone; Platform operates the result without owning or supplying them.

<br>

### Every stored structure is traceable to a Model declaration

**Rule:** Every persistent Model has a traceable storage mapping, and every resolved mapping records the Model it came from and the declaration it rests on. An explicit mapping takes precedence over a derived one. Database enforces the storage-relevant declarations a Model publishes — identity, generated identity, uniqueness, composite constraints, referenced-record existence, and resolved field properties — and reuses Model validation for anything decidable from a single record's own data. A relationship keeps the cardinality and optionality Model resolved, including one-to-one, one-to-many, and many-to-many; physical references, association storage, uniqueness, and referential actions are added only to preserve that meaning, and an explicit reference field is reused rather than duplicated. A Model declared non-persistent never becomes a stored structure. A missing or ambiguous declaration is reported rather than inferred from a name or from documentation.

**Why:** Stored data stays valid under concurrent writes, and every guarantee in the database can be traced back to the meaning that asked for it — which is what makes a schema explainable and a change safe.

**Boundary:** Database does not turn an application-context rule into a storage constraint. Model resolves logical field properties and relationship optionality first; Database Preferences supply only the physical mapping choices Model left unstated and never override Model meaning.

<br>

### Credential storage protects values at rest

**Rule:** Connection credentials are supplied to Database by its environment and are never written in source, and Database is their only owner. Persisted credential fields — a credential the Target stores in a Model — are a separate concern: they are classified before persistence and resolve to an approved at-rest treatment: verification-only credentials use a one-way transformation, recoverable secrets use authenticated protection or a managed secret store, and other sensitive data follows its declared protection.

**Why:** A credential written into source is copied wherever the source goes and outlives every attempt to change it, and inconsistent per-caller treatment of persisted credentials weakens storage protection.

**Boundary:** Database never exposes credential representations, connection settings, keys, or secret values through its public interface, logs, exports, documentation, or Interface records. Platform delivers required secret Bindings without publishing them to other layers.

<br>

### Declared Initial Data preserves its meaning

**Rule:** When initial data exists for a Model, Database imports each declared record through a reusable, configurable mechanism into its resolved storage mapping. The selected implementation determines the mechanism's name, location, and invocation. Every key names a resolved Model field, relationships and required fields are satisfied, records are resolved in dependency order, and importing is repeatable without duplicate logical records or uniqueness violations. The same mechanism may accept later bulk data imports when they follow the same validation, ordering, transaction, and duplicate rules.

Database setup invokes that importer as part of its readiness lifecycle, after pending structural changes are applied and storage integrity is verified. A Database instance is not ready until this import completes successfully, or is explicitly `not applicable` because no Initial Data is declared.

If the Target declares Initial Data, Database is not ready until the structure has been created and the complete Import succeeds. A missing importer, failed import, incomplete record, unresolved relationship, or constraint violation is a Database setup failure and must not be reported as readiness.

**Why:** Rebuilding the Database must restore the declared initial state with the same meaning.

**Boundary:** Initial data comes from the Target and Model definitions, never from Database Preferences. The physical import mechanism remains an implementation choice.

<br>

### Related operations share an explicit Transaction boundary

**Rule:** Database exposes a Transaction boundary through its generic interface so a consumer can group related operations on one Instance. A successful unit commits together; a failed or cancelled unit rolls back, and participating operations do not commit independently. A standalone write forms its own atomic unit. Database owns commit, rollback, cleanup, isolation, conflict handling, retry, and idempotency behavior without exposing the underlying connection.

**Why:** Related changes cannot leave partially applied data when an operation fails.

**Boundary:** The consumer determines which operations belong together. Atomicity across Instances or external services is not implied, and automatic retry never silently duplicates a non-idempotent operation.

<br>

### Persistence security and observability remain bounded

**Rule:** Database applies least privilege to runtime identities, records security-relevant persistence outcomes without secrets, and provides signals for connection failure, Migration failure, constraint violation, Transaction conflict, and protected-data access. Logs, metrics, traces, backups, exports, and error payloads follow the same protection rules as normal reads.

**Why:** A secure schema can still leak through diagnostics, backups, or overpowered identities.

**Boundary:** Database does not own application authorization or business policy, but it enforces its own storage access boundary and never treats observability as an exception to data protection.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Database is an independent package with one public boundary**

- **Must** — Keep Database as an independent package with one documented public boundary.
- **Never** — Let consumers depend on private persistence resources or treat Migration as a public runtime interface.

**Database has three ordered internal layers**

- **Must** — Preserve the order Database Interface → Data Logic and Mapping → Storage Adapter → Engine.
- **Never** — Let an internal layer bypass its next boundary or let consumers bypass Database Interface.

**Storage is derived from Model and invents nothing**

- **Must** — Preserve Model meaning while adding only persistence representation, durability, and enforcement.
- **Never** — Invent domain definitions, rules, records, or application-context behavior in Database.
- **Must** — Decide the access paths, an index among them, in Database; an index is never a Model declaration.

**Engine-specific decisions are explicit and isolated**

- **Must** — Keep the portable contract independent of a particular Engine and isolate extensions.
- **Never** — Present an Engine-specific guarantee as portable without declaring its limits.
- **Must** — Classify portability, isolate Engine-specific extensions, and detect schema drift.
- **Never** — Repair drift with ad-hoc structural commands or hide compatibility impact.

**The complete Database is reproducible from the repository**

- **Must** — Keep the complete reproducible Database structure, history, and initial data in the repository.
- **Never** — Depend on undocumented server state or manual structural work.

**Storage changes use ordered and recoverable Migrations**

- **Must** — Record every storage change as an ordered Migration with safe reversal or explicit recovery.
- **Never** — Change storage objects directly from application code or apply an unverified Migration.

**Database owns the complete persistence responsibility**

- **Must** — Keep every decision about how data is stored, reached, constrained, and changed under Database alone.
- **Never** — Let another Component store, query, or alter stored data, or receive a connection through which it could.
- **Never** — Make an application decision in Database merely because the data passes through it.

**All data access uses one generic Database Interface**

- **Must** — Route all persistent data access through one generic Model-driven Database Interface.
- **Must** — Support the shared `search` operation through the generic Model-driven Database Interface.
- **Must** — Answer an aggregate question about a matching set — how many, total, smallest, largest — in Database rather than by handing the records out to be counted elsewhere.
- **Must** — Offer the removal of every record of a Model while its structure stays in place.
- **Never** — Require untyped Model-name strings, expose connections, or let controlled commands bypass protections.

**Database Instances are explicit and selectable**

- **Must** — Give every Instance a stable identity, publish its Registry, and use exactly one explicit default.
- **Never** — Expose raw connections or secrets through the Registry.

**Every stored structure is traceable to a Model declaration**

- **Must** — Keep every persistent mapping and storage constraint traceable to its source Model.
- **Never** — Turn a non-persistent Model into stored structure or silently weaken a persistence rule.
- **Must** — Preserve resolved relationship cardinality, optionality, roles, and required physical enforcement.
- **Never** — Let physical mapping defaults override Model meaning.

**Credential storage protects values at rest**

- **Must** — Take connection credentials from the environment and never write one in source.
- **Must** — Apply an approved protected at-rest treatment to every persisted credential field.
- **Never** — Expose credential representations, keys, connection settings, or secret values through Database outputs.

**Declared Initial Data preserves its meaning**

- **Must** — Import declared initial data repeatably and preserve its Model meaning.
- **Never** — Source initial data from Database Preferences.

**Related operations share an explicit Transaction boundary**

- **Must** — Provide an explicit Transaction boundary with atomic commit and rollback per Instance.
- **Never** — Imply cross-Instance atomicity or silently duplicate non-idempotent work through retries.

**Persistence security and observability remain bounded**

- **Must** — Apply least privilege, protected observability, and signals for security-relevant persistence outcomes.
- **Never** — Treat logs, backups, exports, or diagnostics as exceptions to data protection or take ownership of application authorization.
