# Database Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
   - **[Understanding](#understanding)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Principles](#principles)**
   - **[Database is an independent package with one public boundary](#database-is-an-independent-package-with-one-public-boundary)**
   - **[Database has three ordered internal layers](#database-has-three-ordered-internal-layers)**
   - **[Persistence preserves Model meaning without redefining it](#persistence-preserves-model-meaning-without-redefining-it)**
   - **[Database remains independent of its Engine](#database-remains-independent-of-its-engine)**
   - **[The complete Database is reproducible from the repository](#the-complete-database-is-reproducible-from-the-repository)**
   - **[Storage changes use ordered and recoverable Migrations](#storage-changes-use-ordered-and-recoverable-migrations)**
   - **[Database owns the complete persistence responsibility](#database-owns-the-complete-persistence-responsibility)**
   - **[All data access uses one generic Database Interface](#all-data-access-uses-one-generic-database-interface)**
   - **[Database Instances are explicit and selectable](#database-instances-are-explicit-and-selectable)**
   - **[Storage mappings and constraints remain traceable to Models](#storage-mappings-and-constraints-remain-traceable-to-models)**
   - **[Relationship mappings preserve resolved meaning](#relationship-mappings-preserve-resolved-meaning)**
   - **[Credential storage protects values at rest](#credential-storage-protects-values-at-rest)**
   - **[Declared Initial Data preserves its meaning](#declared-initial-data-preserves-its-meaning)**
   - **[Related operations share an explicit Transaction boundary](#related-operations-share-an-explicit-transaction-boundary)**
   - **[Portability and schema integrity remain explicit](#portability-and-schema-integrity-remain-explicit)**
   - **[Persistence security and observability remain bounded](#persistence-security-and-observability-remain-bounded)**
6. **[At a Glance](#at-a-glance)**
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

What the storage looks like is derived from Model rather than decided here. Database reads the declarations Model publishes — identity, field types, nullability, defaults, uniqueness, relationships and their cardinality — and turns them into physical structure and enforcement, adding only what persistence itself requires. A declaration that is missing or ambiguous is reported, never guessed from a name.

Structure changes only through Migrations, in a recorded order, so the current schema can be explained, reproduced from the repository, and recovered. At startup the declared structure is applied, integrity is verified, and declared Initial Data is imported; an Instance is not ready until that completes. Which Instances exist, how each reaches its Engine, and the credentials it uses are read from Database's own runtime configuration file, so adding a database or changing a credential is an edit to that file and not to any source.

### Understanding

#### Database configuration

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

**Data Logic and Mapping** resolves how a logical Model and its published declarations are represented and enforced in storage — identity, types, nullability, defaults, uniqueness, relationships, indexes, and the at-rest treatment of a credential field. It derives that representation from Model rather than deciding domain meaning, and it reports a missing or ambiguous declaration instead of guessing one.

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

Every statement here is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

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

### Persistence preserves Model meaning without redefining it

**Rule:** Physical persistence is derived from the logical Model and the storage-relevant meaning it publishes. Database preserves Model identity, field meaning, relationships, constraints, and applicable rules while adding only storage representation, durability, and enforcement required by persistence.

**Why:** Consumers need durable data that retains the same domain meaning as the source Model.

**Boundary:** Database never invents a Model, field, relationship, rule, or initial record because storage makes it convenient. Application-context and operation-dependent behavior remains outside Database.

<br>

### Database remains independent of its Engine

**Rule:** The portable persistence contract and mapping remain understandable without a particular Engine. Engine-specific extensions are explicit, isolated behind the Storage Adapter, and recorded with their portability impact.

**Why:** An Engine can be replaced without changing consumer behavior or domain meaning.

**Boundary:** Engine selection is a technical Preference resolved outside this Principles file and never becomes a consumer-facing guarantee unless explicitly portable.

<br>

### The complete Database is reproducible from the repository

**Rule:** Everything needed to recreate the Database belongs to the repository: storage structure, migration history, constraints, indexes, and declared initial data.

**Why:** A new environment or checkout can rebuild an equivalent Database without undocumented manual work.

**Boundary:** No Database structure exists only in a running server, memory, or an unrecorded manual step.

<br>

### Storage changes use ordered and recoverable Migrations

**Rule:** Storage structure never changes without a recorded Migration in an ordered history. A Migration has a tested reversal when semantically safe. A data-losing or data-transforming Migration may be irreversible only when explicitly marked, protected by an approved recovery procedure, and accompanied by a documented recovery path.

**Why:** Ordered history explains, reproduces, and safely recovers the current structure.

**Boundary:** Application code never creates, alters, or drops storage objects directly. Migration execution verifies ordering, integrity, drift, and concurrent-run coordination.

<br>

### Database owns the complete persistence responsibility

**Rule:** Database alone owns supported Engine integration, Instances, physical storage, runtime connections, storage mappings, persistence constraints, indexes, Migration history, and the generic data-access interface.

**Why:** Persistence decisions interact and require one authority that can reason about them together.

**Boundary:** Model owns logical meaning; Logic owns application behavior and service orchestration; Presentation owns presentation; Platform operates the result. Database owns only its own private runtime settings and secrets.

<br>

### All data access uses one generic Database Interface

**Rule:** Consumers use one generic Database Interface for every persistent Model. The interface accepts a public Model type or instance, a supported operation, and the criteria required by that operation. It supports create, read, read-by-identifier, list, search, update, delete, and activation operations through one Model-driven pipeline rather than one implementation per Model.

Public operations never require a Model name encoded as an untyped string or resolve a Model through an untyped string registry. Model identity is carried by the imported type or instance.

The activation operation accepts exactly enable or disable, is available only when the selected Model declares the is_active field, and changes that field to the corresponding value.

The interface may also expose a capability-restricted command route for data operations that cannot be expressed through standard operations. It requires explicit parameters, protected identifiers, separate observability, transaction participation, and explicit Engine identification. It rejects structural changes, privilege changes, connection administration, and Migration operations.

**Why:** One generic pipeline serves every Model while preserving a stable public boundary and preventing duplicate business-logic implementations.

**Boundary:** Consumers never receive connections or storage access. The command route cannot bypass Model validation, persistence constraints, credential protections, Migrations, or the public transaction boundary. Model-specific application behavior remains in Logic.

<br>

### Database Instances are explicit and selectable

**Rule:** Every Database Instance has a stable identifier, human-readable name, stated purpose, and one supported Engine binding. Database publishes an Instance Registry through its public interface. Exactly one Instance is the default; an omitted selection uses it, while an unknown explicit selection is rejected.

The Registry is derived from the configured Instance collection, and the number of Instances is never maintained as a separate authority.

**Why:** Named Instances let consumers choose a database by purpose without learning how it connects.

**Boundary:** The Registry exposes no raw connection objects or secret values. Instances, their connection settings, and their credentials come from Database's runtime configuration file; Platform operates the result without owning or supplying them.

<br>

### Storage mappings and constraints remain traceable to Models

**Rule:** Every persistent Model has a traceable storage mapping. An explicit mapping takes precedence over a derived mapping, and every resolved mapping records its source Model and persistence metadata. Non-persistent Models do not become stored structures merely because they exist. Database enforces storage-relevant Model declarations, including primary-key identity, generated identity, uniqueness, referenced-record existence, composite constraints, and resolved field properties, while reusing Model validation for checks determined solely from Model data. A missing or ambiguous declaration is reported rather than inferred from names or documentation.

**Why:** Stored data remains valid under concurrent writes and every guarantee can be traced to its source meaning.

**Boundary:** Database does not translate application-context rules into storage constraints. A persistence rule is never silently weakened; an unsupported requirement is enforced equivalently within Database or reported.

<br>

### Relationship mappings preserve resolved meaning

**Rule:** Relationship mappings preserve the cardinality, optionality, and roles resolved by Model, including one-to-one, one-to-many, and many-to-many relationships. Physical references, association storage, uniqueness, and referential actions are added only as needed to preserve that meaning. An explicit relationship field is reused rather than duplicated.

**Why:** Explicit mapping keeps stored relationships navigable, enforceable, and faithful to the logical Model.

**Boundary:** Model resolves logical field properties and relationship optionality first. Database Preferences supply only unstated physical mapping choices and never override Model meaning.

<br>

### Credential storage protects values at rest

**Rule:** Connection credentials live in Database's runtime configuration file, beside the Instance they belong to, so that adding an Instance or changing a username or password is one edit in one file. Persisted credential fields — a credential the Target stores in a Model — are a separate concern: they are classified before persistence and resolve to an approved at-rest treatment: verification-only credentials use a one-way transformation, recoverable secrets use authenticated protection or a managed secret store, and other sensitive data follows its declared protection.

**Why:** One file holds every connection setting the operator changes, and inconsistent per-caller treatment of persisted credentials weakens storage protection.

**Boundary:** Database never exposes credential representations, connection settings, keys, or secret values through its public interface, logs, exports, documentation, or Interface records. Platform delivers required secret Bindings without publishing them to other layers. The key for an encrypted at-rest treatment is read from that same runtime configuration file. How the file itself is protected — and whether it is committed — is an open decision recorded in this file's Understanding record; this Principle does not decide it.

<br>

### Declared Initial Data preserves its meaning

**Rule:** When initial data exists for a Model, Database imports each declared record through a reusable, configurable mechanism into its resolved storage mapping. The selected implementation determines the mechanism's name, location, and invocation. Every key names a resolved Model field, relationships and non-nullable fields are satisfied, records are resolved in dependency order, and importing is repeatable without duplicate logical records or uniqueness violations. The same mechanism may accept later bulk data imports when they follow the same validation, ordering, transaction, and duplicate rules.

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

### Portability and schema integrity remain explicit

**Rule:** Every persistence decision is classified as portable contract, portable mapping, or Engine-specific extension. Engine-specific types, commands, indexes, transaction features, and constraints remain isolated and recorded with compatibility and replacement impact. Database verifies that the running structure matches the recorded structure.

**Why:** Portability is meaningful only when its limits are visible, and integrity requires detecting drift.

**Boundary:** Preferences may select an Engine-specific feature, but it cannot silently change the portable contract. Application code never repairs drift with ad-hoc structural commands.

<br>

### Persistence security and observability remain bounded

**Rule:** Database applies least privilege to runtime identities, records security-relevant persistence outcomes without secrets, and provides signals for connection failure, Migration failure, constraint violation, Transaction conflict, and protected-data access. Logs, metrics, traces, backups, exports, and error payloads follow the same protection rules as normal reads.

**Why:** A secure schema can still leak through diagnostics, backups, or overpowered identities.

**Boundary:** Database does not own application authorization or business policy, but it enforces its own storage access boundary and never treats observability as an exception to data protection.

<br>

## At a Glance

- **Must** — Keep Database as an independent package with one documented public boundary.
- **Never** — Let consumers depend on private persistence resources or treat Migration as a public runtime interface.
- **Must** — Preserve the order Database Interface → Data Logic and Mapping → Storage Adapter → Engine.
- **Never** — Let an internal layer bypass its next boundary or let consumers bypass Database Interface.
- **Must** — Preserve Model meaning while adding only persistence representation, durability, and enforcement.
- **Never** — Invent domain definitions, rules, records, or application-context behavior in Database.
- **Must** — Keep the portable contract independent of a particular Engine and isolate extensions.
- **Never** — Present an Engine-specific guarantee as portable without declaring its limits.
- **Must** — Keep the complete reproducible Database structure, history, and initial data in the repository.
- **Never** — Depend on undocumented server state or manual structural work.
- **Must** — Record every storage change as an ordered Migration with safe reversal or explicit recovery.
- **Never** — Change storage objects directly from application code or apply an unverified Migration.
- **Must** — Keep all persistence ownership inside Database and all other responsibilities in their owning Components.
- **Must** — Route all persistent data access through one generic Model-driven Database Interface.
- **Must** — Support the shared `search` operation through the generic Model-driven Database Interface when the Model exposes it.
- **Must** — Use is_active with enable or disable for activation when that field exists.
- **Never** — Require untyped Model-name strings, expose connections, or let controlled commands bypass protections.
- **Must** — Give every Instance a stable identity, publish its Registry, and use exactly one explicit default.
- **Never** — Expose raw connections or secrets through the Registry.
- **Must** — Keep every persistent mapping and storage constraint traceable to its source Model.
- **Never** — Turn a non-persistent Model into stored structure or silently weaken a persistence rule.
- **Must** — Preserve resolved relationship cardinality, optionality, roles, and required physical enforcement.
- **Never** — Let physical mapping defaults override Model meaning.
- **Must** — Keep connection credentials in Database's runtime configuration file, beside the Instance that uses them.
- **Must** — Apply an approved protected at-rest treatment to every persisted credential field.
- **Never** — Expose credential representations, keys, connection settings, or secret values through Database outputs.
- **Must** — Import declared initial data repeatably and preserve its Model meaning.
- **Never** — Source initial data from Database Preferences.
- **Must** — Provide an explicit Transaction boundary with atomic commit and rollback per Instance.
- **Never** — Imply cross-Instance atomicity or silently duplicate non-idempotent work through retries.
- **Must** — Classify portability, isolate Engine-specific extensions, and detect schema drift.
- **Never** — Repair drift with ad-hoc structural commands or hide compatibility impact.
- **Must** — Apply least privilege, protected observability, and signals for security-relevant persistence outcomes.
- **Never** — Treat logs, backups, exports, or diagnostics as exceptions to data protection or take ownership of application authorization.