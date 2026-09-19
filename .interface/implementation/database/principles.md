# Database Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Documentation](#documentation)**
6. **[Principles](#principles)**
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
7. **[At a Glance](#at-a-glance)**
<br>

## Introduction

### Overview

Database owns the Target's complete persistence boundary: it maps Model to durable storage, preserves storage guarantees, and exposes one generic public interface without exposing persistence details.

### Purpose

Database is the one place that sees the complete record set, enforces storage guarantees, records structural change as ordered Migrations, and gives consumers one generic interface. Without it, persistence rules and schema history spread across consumers and become unreliable.

### How It Works

A consumer passes a public Model type or instance and operation to the Database Interface; it never names a table, builds a query, or receives a connection. The request flows through Database Interface, Data Logic and Mapping, and Storage Adapter in that order.

Storage is derived from Model declarations; missing or ambiguous declarations are reported. Migrations apply structure in order, startup verifies integrity and imports Initial Data, and an Instance is ready only after setup succeeds. Runtime Instances, connections, and credentials are configured as Database owns them and are never hardcoded in source.

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

**Database Interface** publishes generic operations and the Instance Registry; it accepts a Model type or instance and never exposes connections, queries, or table names.

**Data Logic and Mapping** derives storage representation and enforcement from Model declarations, including credential treatment and persistence access paths; it reports missing or ambiguous declarations.

**Storage Adapter** owns Engine connections and operations; the Engine remains replaceable behind it.

The layers are ordered, and none bypasses the next boundary.

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

Database documentation covers the public operations, their inputs and outputs, Model naming, the Instance Registry, selection, runnable operation examples, and Transactions. It does not expose internal layers, mappings, Migrations, Engine choice, or configuration; consumers must be able to use persistence without depending on them.

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

**Rule:** Database derives physical persistence from Model, preserving its identity, fields, relationships, constraints, and rules while adding only storage representation, durability, and enforcement. It never invents or weakens domain meaning; unsupported persistence rules are enforced equivalently or reported.

**Why:** Database must preserve Model meaning while making it durable.

**Boundary:** Application behavior stays outside Database; persistence access paths such as indexes belong to Database and cannot change Model meaning.

<br>

### Engine-specific decisions are explicit and isolated

**Rule:** The portable persistence contract remains understandable without its Engine. Each decision is classified as portable contract, portable mapping, or Engine-specific extension; extensions are declared and isolated behind Storage Adapter, while schema drift is detected and reported.

**Why:** Explicit isolation keeps the Engine replaceable.

**Boundary:** Development resolves Engine selection; Preferences may select extensions but cannot change the portable contract, and application code never repairs drift.

<br>

### The complete Database is reproducible from the repository

**Rule:** Everything needed to recreate the Database belongs to the repository: storage structure, migration history, constraints, indexes, and declared initial data.

**Why:** A new environment or checkout can rebuild an equivalent Database without undocumented manual work.

**Boundary:** The repository reproduces structure, history, and declared data; the environment supplies Instances, access, credentials, and keys, and no structure exists only in an unrecorded runtime state.

<br>

### Storage changes use ordered and recoverable Migrations

**Rule:** Storage structure changes only through ordered recorded Migrations. Safe Migrations have tested reversals; data-losing or transforming ones require an explicit marker, approved recovery protection, and a documented recovery path.

**Why:** Ordered history explains, reproduces, and safely recovers the current structure.

**Boundary:** Application code never creates, alters, or drops storage objects directly. Migration execution verifies ordering, integrity, drift, and concurrent-run coordination.

<br>

### Database owns the complete persistence responsibility

**Rule:** Database alone owns how data is stored, reached, constrained, and changed; no other Component stores, queries, alters data, or receives a connection.

**Why:** One owner keeps mapping, constraints, queries, and Migrations coherent.

**Boundary:** Model owns logical meaning; Logic owns application behavior and service orchestration; Presentation owns presentation; Platform operates the result. Database owns only its own private runtime settings and secrets, and it makes no application decision merely because the data passes through it.

<br>

### All data access uses one generic Database Interface

**Rule:** One generic Model-driven Interface serves every persistent Model through create, read, read-by-identifier, list, search, update, delete, aggregate, and truncate operations. It accepts a public Model type or instance and operation criteria, never an untyped Model-name string. A capability-restricted command route may cover unsupported data operations with explicit parameters, protected identifiers, observability, transaction participation, and Engine identification, but never structural, privilege, connection, or Migration work.

**Why:** One generic pipeline preserves a stable boundary without duplicating business logic.

**Boundary:** The Interface offers persistence only: activation is an `update` of the Model Field, consumers receive no connections, controlled commands cannot bypass Model validation or persistence protections, and application behavior remains in Logic.

<br>

### Database Instances are explicit and selectable

**Rule:** Every Database Instance has a stable identifier, human-readable name, stated purpose, and one supported Engine binding. Database publishes an Instance Registry through its public interface. Exactly one Instance is the default; an omitted selection uses it, while an unknown explicit selection is rejected.

The Registry is derived from the configured Instance collection, and the number of Instances is never maintained as a separate authority.

**Why:** Named Instances let consumers choose a database by purpose without learning how it connects.

**Boundary:** The Registry exposes no raw connection objects or secret values. Instances, their connection settings, and their credentials are owned by Database alone and are supplied by no other Component.

<br>

### Every stored structure is traceable to a Model declaration

**Rule:** Every persistent Model has a traceable mapping that records its source declaration; explicit mappings override derived ones. Database enforces storage-relevant identity, generation, uniqueness, composite constraints, references, field properties, relationship cardinality, and optionality, reusing Model validation where applicable. It stores only persistent Models, never infers persistence or declarations, and reports missing or ambiguous mappings.

**Why:** Traceable mappings keep stored data valid and the schema explainable.

**Boundary:** Database maps Model meaning and physical choices only; it does not turn application rules into storage constraints.

<br>

### Credential storage protects values at rest

**Rule:** Environment-supplied connection credentials never enter source and belong only to Database. Persisted credentials are classified before storage and receive approved treatment: one-way verification, authenticated reversible protection or managed storage for recoverable secrets, and declared protection for other sensitive data. Database applies Model's classification and treatment, rejects missing or unsupported treatment, and infers neither from a Field name.

**Why:** Centralized protected treatment prevents credential leaks and inconsistent storage protection.

**Boundary:** Database never exposes credential representations, connection settings, keys, or secret values through its public interface, logs, exports, documentation, or Interface records.

<br>

### Declared Initial Data preserves its meaning

**Rule:** When declared, Initial Data is imported through a reusable configurable mechanism into resolved mappings. Keys name Model Fields, relationships and required fields are satisfied, records follow dependency order, and imports are repeatable without duplicates or uniqueness violations. Setup applies structure, verifies integrity, then imports; the Instance is not ready until import succeeds or is not applicable, and any missing or failed import is a setup failure.

**Why:** Rebuilding the Database must restore the declared initial state with the same meaning.

**Boundary:** Initial data comes from the Target and Model definitions, never from Database Preferences. The physical import mechanism remains an implementation choice.

<br>

### Related operations share an explicit Transaction boundary

**Rule:** Database exposes a Transaction boundary for related operations on one Instance: success commits together, failure or cancellation rolls back, standalone writes are atomic, and Database owns commit, rollback, cleanup, isolation, conflicts, retry, and idempotency without exposing connections.

**Why:** Related changes cannot leave partially applied data when an operation fails.

**Boundary:** The consumer determines which operations belong together. Atomicity across Instances or external services is not implied, and automatic retry never silently duplicates a non-idempotent operation.

<br>

### Persistence security and observability remain bounded

**Rule:** Database applies least privilege, records persistence security outcomes without secrets, and signals connection, Migration, constraint, Transaction, and protected-data events; logs, metrics, traces, backups, exports, and errors follow normal data protection.

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
- **Never** — Infer persistence from a Model's existence, name, or identity field.
- **Must** — Preserve resolved relationship cardinality, optionality, roles, and required physical enforcement.
- **Never** — Let physical mapping defaults override Model meaning.

**Credential storage protects values at rest**

- **Must** — Take connection credentials from the environment and never write one in source.
- **Must** — Apply an approved protected at-rest treatment to every persisted credential field.
- **Must** — Reject a persisted credential whose declared at-rest treatment is missing or unsupported, rather than storing it.
- **Never** — Infer a credential classification or its at-rest treatment from a field name.
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
