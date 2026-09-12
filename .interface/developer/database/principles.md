# Database Standard

> **Authoritative Standard for the Database Component**
>
> This document is the authoritative standard for the project's Database Component.
>
> Every AI agent, developer, reviewer, or automation that creates, changes, validates, or reasons about Database code MUST read and follow this document before making changes.
>
> **Principles override preferences, framework defaults, convenience, and implementation choices.**
>
> A project may add stricter rules, but it must not weaken the rules defined here.

---

# 1. Purpose

Database is the Component that owns the project's complete persistence layer. It turns the logical Models into stored data, keeps the whole storage structure reproducible from the repository, and publishes one generic interface through which every consumer reads and writes without ever meeting the engine behind it. Its philosophy, responsibilities, and boundaries are fixed and independent of any engine, tool, or project.

# Project Independence

Database is reusable across Targets. This standard defines how a Database Component works, not which domain a project contains. Project-specific Model names, fields, relationships, uniqueness rules, initial records, workflows, and platform details belong to the current Target and Model definitions and MUST NOT be copied into this standard.

Examples and implementation choices in this document MUST remain domain-neutral. Changing the Target MUST NOT require changing this standard.

---

# Architectural Foundation

Database is the persistence-specific derivation of the platform-independent logical Model. It adds storage representation, durability, constraints, transactions, and engine integration without redefining the Model's domain meaning.

This standard is aligned with platform-independent and platform-specific modeling ideas. It does not claim full conformance to ISO/IEC 9075, an individual database engine, an ORM, or a migration tool. Those references and tools govern only the concerns within their own authority.

---

# Authority by Concern

| Concern | Authoritative source |
| --- | --- |
| Domain names, fields, relationships, domain rules, and initial data | Current Model and Target definitions |
| Persistence boundaries, ownership, mapping responsibilities, transactions, and storage guarantees | This Database Standard |
| Engine, ORM, migration tool, naming, physical types, and version choices | Database Preferences |
| SQL syntax and engine-specific behaviour | Selected Engine documentation and compatible toolchain |

Database MUST NOT invent a domain Model, field, relationship, rule, or initial record because an engine or ORM makes it convenient. An engine default MUST NOT override an explicit Model definition or this standard.

---

# 2. Core Principles

## 2.1 Terms

- **Database Interface** — the layer that is the only boundary published to consumers, exposing Model operations and Instance discovery and selection.
- **Data Logic and Mapping** — the layer that implements generic Model operations and resolves how logical Models, fields, relationships, rules, and initial data are physically mapped and enforced.
- **Storage Adapter** — the layer that owns the connection to the selected Engine and performs physical persistence operations.
- **Engine** — the database technology behind the Storage Adapter, chosen late and replaceable.
- **Instance** — one selectable database identity with a stable key, name, purpose, and Engine binding.
- **Instance Registry** — the published catalogue through which consumers discover Instance identities and the default, without receiving connections or secrets.
- **Migration** — one recorded, ordered change to the storage structure, with a tested reversal when safe and an explicit recovery path when irreversible; it is part of the authoritative record of how that structure was reached.
- **At-rest mode** — the resolved persistence transformation applied to a field that is a credential.
- **Transaction** — one unit of data operations on a single Instance whose changes are committed together or rolled back together.

## 2.2 Relationships

- **Consumes Model** — the logical Models, fields, relationships, rules, and initial data that Database maps and enforces.
- **Consumes Development** — the common package standard and the ownership rules under which Database keeps its own settings and secrets.
- **Consumes Platform** — the Bindings the selected Launch delivers to Database's boundary, without Platform taking ownership of them.
- **Consumed by Backend** — the generic data-access interface and Instance Registry, reached only through Backend's Data Access layer.

Technical choices and defaults belong to Database Preferences. Database implementation applies those choices to the current project definition.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 2.3 Database is an independent package with three internal layers

**Rule:** Database is implemented as an independent package with a documented public interface. Compatible in-process consumers import the public Database gateway and Instance Registry from this package. Database is formed from three distinct internal layers:

- **Database Interface** is the only boundary published to consumers and exposes Model operations plus Instance discovery and selection;
- **Data Logic and Mapping** implements generic Model operations and resolves the physical persistence mapping and enforcement of logical Models, fields, relationships, rules, and initial data; and
- **Storage Adapter** owns the connection to the selected Database Engine and performs physical persistence operations.

The dependency direction is Database Interface → Data Logic and Mapping → Storage Adapter → Database Engine.

**Why:** One published boundary over an ordered internal chain is what lets the engine, the mapping, and the exposed operations each change without the others being rewritten.

**Boundary:** Consumers never import internal adapters, mappings, connections, or configuration implementation. Consumers never bypass Database Interface, and an internal layer never bypasses the layer responsible for the next boundary. Migration is internal Database tooling rather than a runtime application layer: it changes the physical storage structure through the Storage Adapter's resolved technology without becoming part of the public Database Interface.

<br>

## 2.4 Database is independent of its engine

**Rule:** The physical persistence design owned by Database — its tables, columns, foreign keys, constraints, indexes, and enforcement mechanisms — is derived from the logical Model. The portable contract and mapping are described independently of any particular database server. Engine-specific extensions are explicit, isolated, and recorded with their portability impact.

**Why:** If the engine changes, consumers retain the same data-access behaviour and domain meaning while only internal storage and engine-specific configuration may need to differ.

**Boundary:** The engine is an implementation detail chosen late.

<br>

## 2.5 The whole Database is defined as code

**Rule:** Everything needed to recreate Database from nothing lives in the repository: its storage schema, history of changes, constraints, indexes, and any declared initial data.

**Why:** This provides reproducibility: a new environment, server, or checkout can rebuild an identical Database without manual structural work.

**Boundary:** Nothing about the Database structure exists only inside a running server, only in someone's memory, or only in a manual step.

<br>

## 2.6 Storage-schema changes are ordered and recoverable

**Rule:** The storage schema never changes without a recorded migration. Each change has a fixed position in an ordered history, and migration history is the authoritative record of how the Database reached its current structure. A migration MUST provide a tested reversal when reversal is semantically safe. A migration that can lose or transform data MAY be irreversible only when it is explicitly marked, protected by an approved backup or recovery procedure, and accompanied by a documented recovery path.

**Why:** An ordered and integrity-checked history is the only way the current structure can be explained, reproduced, and safely recovered.

**Boundary:** Application code never creates, alters, or drops database objects directly. Silent startup creation and manual structural patches are excluded because they create storage state that cannot be explained by migration history. Migration execution verifies ordering, integrity, and schema drift, and coordinates concurrent runners so that a migration cannot be applied twice or partially recorded as complete.

<br>

## 2.7 Database owns the complete persistence layer

**Rule:** Database alone owns supported engine integration, Database Instances, physical storage, runtime connections, ORM, model-to-storage mappings, storage schema, physical constraints, indexes, migration history, and the generic data-access interface it publishes.

**Why:** Persistence decisions interact with each other, so splitting them across Components produces storage that no single Component can reason about.

**Boundary:** Logical Models, fields, relationships, and domain rules remain owned by Model; Database owns only their persistence mapping and enforcement. No other Component makes or changes Database-owned decisions. Database does not own application behaviour, the HTTP API, Frontend, or secrets belonging to other layers. Database owns its private runtime settings and secrets under Development's rules; Platform delivers the Bindings it needs through the selected Launch. Its boundaries remain explicit in the implementation and its public documentation.

<br>

## 2.8 All data access goes through one generic interface

**Rule:** Consumers use only the generic interface implemented by Database. The interface is generic rather than one access implementation per Model: a caller supplies an imported public Model type or Model instance from the public Model package, selects a supported operation, and supplies any criteria required by that operation. The same interface performs create, read, list, update, delete, and status operations for every persistent Model, and Data Logic uses one Model-driven operation pipeline rather than a separate business-logic implementation for every Model. Public Database operations MUST NOT require a Model name encoded as a string or resolve a Model through an untyped string registry; Model identity is carried by the imported type or instance.

The status operation accepts exactly one action: `enable` or `disable`. It is available only when the selected Model declares a `status` field and changes that field to the corresponding enabled or disabled value.

The interface MAY also support controlled SQL-command execution for cases that cannot be expressed through standard Model operations, using explicit parameters rather than value interpolation. This route is capability-restricted, separately observable, and only for data operations on the selected Instance. It remains subject to Database's persistence constraints and transaction boundaries. It rejects structural changes, privilege changes, connection administration, and migration operations, which belong exclusively to Migration or private runtime administration. Engine-specific SQL must be identified as such and validated for the selected Engine; it carries no promise of portability when the Engine changes.

Controlled SQL preserves the same data protections as the generic operations. Before accepting a command, Database must establish which data it can read or change and how the applicable protections are enforced. Identifiers such as table and column names come from an internal allow-list or typed operation definition; user input is never interpolated into SQL structure. Writes preserve Model validation of the resulting data, persistence constraints, and the resolved credential transformations; reads never expose credential storage representations or runtime secrets, including through derived results. Parameterization alone does not establish these guarantees. A command whose effects or results cannot be handled with these protections is rejected before execution. Validation of resulting changes occurs within the same transaction before commit, and failure rolls back the changes. This does not authorize Database to take over application-context rules owned by Backend Logic.

**Why:** Differences between Models come from their resolved fields, relationships, constraints, rules, and storage mappings, so one pipeline serves them all and each new Model costs no new access implementation.

**Boundary:** Consumers never receive the engine connection or access storage outside the published Database interface. Model identity and data are not passed as an untyped Model-name string and unrelated field dictionary. A Model without a `status` field rejects the status operation. The controlled SQL route is the explicit exception to Model-driven access; it stays inside the Database boundary and exposes no connection, ORM mapping, migration implementation, or physical database file. It grants no direct storage access and cannot bypass Migration or manage the transaction independently of the public transaction boundary. Model-specific application Behaviour remains in Backend Logic and never enters Database.

<br>

## 2.9 Database Instances are explicit and selectable

**Rule:** Every Database Instance has a stable identifier, human-readable name, stated purpose, and one supported Engine binding. Instance identity is distinct from Engine identity: several Instances may use the same Engine while serving different purposes. Database publishes an Instance Registry through its public interface so consumers can discover available Instance identities and select one. Exactly one Instance is the default, and when a consumer does not select an Instance, Database uses that default explicitly and predictably. The number of Instances is derived from the Instance collection and is never maintained as a separate authoritative value.

Database-owned runtime configuration declares the supported Engine catalogue, the Instance catalogue, and the default selection. Each Instance refers to one supported Engine, and the default refers to an existing Instance. The public Registry derives from the configured Instances rather than maintaining a second catalogue in implementation. A consumer can supply an identity obtained from that Registry to select the Instance for an operation or transaction. An omitted selection uses the configured default; an explicit unknown Instance is rejected, never silently redirected to the default.

**Why:** A project outgrows one database, and naming each Instance by purpose lets a consumer choose the right one without learning how any of them connect.

**Boundary:** The registry exposes no raw connection objects and no secret values. Database owns Instance definitions and connection handling; Platform may deliver the Binding that selects an Instance for another layer without taking ownership of it.

<br>

## 2.10 Storage mappings and persistence constraints remain traceable to Models

**Rule:** Every persistent domain Model has a traceable storage mapping. A relational implementation commonly maps a persistent Model to a table, but value objects, embedded types, projections, and other non-persistent Models do not become tables merely because they exist in Model. An explicit storage mapping takes precedence over a derived mapping, and every resolved mapping records the source Model it implements. Database guarantees the Model rules that depend on stored state, including uniqueness across records and the existence of referenced records, and maps the resolved Model's storage-relevant field properties into persistence constraints. Enforcement remains traceable to the source Model declaration and applies when changes are committed, including under concurrent access. Database reuses shared Model validation for checks determined from Model data instead of maintaining competing definitions. A persistence rule with one clear representation is resolved deterministically; when several representations are possible, the choice preserves its declared meaning.

**Why:** Persistence guarantees must hold for stored data even when several consumers write concurrently, while keeping a rule's declaration separate from its enforcement prevents duplicate or conflicting ownership.

**Boundary:** Database does not translate application-context or operation-dependent rules into storage constraints or assume responsibility for Backend Logic. Not every Model rule belongs in the storage schema. A rule within Database's persistence responsibility is never silently dropped or weakened; if the selected Engine cannot represent it directly, Database must provide equivalent enforcement within its boundary or report the unsupported requirement.

<br>

## 2.11 Relationships are explicit and consistently resolved

**Rule:** Relationship mappings preserve the cardinality, optionality, and roles resolved by Model, including one-to-one, one-to-many, and many-to-many relationships. The physical representation uses explicit foreign keys and any association storage and constraints needed to preserve that meaning. One-to-one mappings enforce the required uniqueness; one-to-many mappings allow the declared multiplicity; many-to-many mappings represent both sides without reducing either to a single reference. Association storage reuses an explicit association Model when one is declared; a purely physical association does not introduce a new domain Model.

An explicit relationship field or reference always takes precedence over a default, and an existing declared relationship field is reused rather than duplicated. Each foreign key references the related key and uses the same type. Its nullability preserves the resolved Model field and relationship optionality; Database does not apply a separate logical nullability default. If a physical relationship field is needed where no logical field is declared, its nullability follows the resolved relationship meaning. When one Model relates to the same target more than once, the relationship roles remain explicit, and the resolved storage schema records each foreign-key field, referenced table, and referenced column. A mapping must preserve the complete relationship constraint; foreign-key nullability alone is not proof that every cardinality or participation requirement is enforced.

**Why:** Explicit, recorded connections are what make stored data navigable and enforceable rather than merely conventional.

**Boundary:** Logical field properties and relationship optionality are resolved under the Model Component's rules before storage mapping. Database Preferences supply only unstated physical mapping choices, such as storage naming, indexing, and referential actions, without overriding the resolved Model meaning.

<br>

## 2.12 Connection secrets stay outside and credential storage stays internal

**Rule:** Connection credentials belong to runtime configuration outside committed files. Credential fields are classified before persistence and each resolves to one supported at-rest treatment: passwords and verifiers use an approved one-way password-hashing scheme; secrets that must be recovered use authenticated encryption or a managed secret store; ordinary sensitive data follows its declared protection. An explicit treatment takes precedence, and otherwise Database Preferences supply the default. Database applies the matching persistence transformation.

**Why:** A secret in a committed file is public, and a credential whose at-rest treatment is decided per caller is treated inconsistently.

**Boundary:** Runtime connection settings are internal to Database; neither their shape nor secret values are published through the data-access interface. The storage representation of a credential is never exposed to consumers. Password hashes are never reversible, and encryption keys are never stored beside the ciphertext they protect. Encryption keys and connection secrets belong in Database's private runtime area under Development's rules; they never appear in Interface records, general Database configuration, source-controlled implementation, or distributed artifacts. Platform delivers them as Bindings through the selected Launch, without publishing these values to other layers.

<br>

## 2.13 Initial data preserves declared meaning

**Rule:** When initial data exists for a Model, seeding becomes part of Database and each record maps to its resolved table. Every seed key names a resolved Model field. Each record satisfies its required relationships and non-nullable fields through a supplied value, a resolved default, or permitted generated behaviour. Records are resolved in dependency order, explicit relationship identifiers are preserved, and seeding is repeatable without duplicating logical records or breaking uniqueness rules.

**Why:** Initial records are part of what the project declared, so a rebuilt database is only equivalent if they come back with the same meaning.

**Boundary:** Initial data is never supplied by Database Preferences.

<br>

## 2.14 Related data operations share an explicit transaction boundary

**Rule:** Database publishes a transaction boundary through its generic interface so a consumer can group related data operations on one Instance. Changes in the group are committed together only when the unit succeeds and all applicable persistence constraints hold; a failed or cancelled unit rolls back its changes. Operations participating in the unit do not commit independently. A standalone write outside an explicit group forms its own atomic unit. Database resolves and documents the applicable isolation level, locking or version-check strategy, retry rules for transient conflicts, and idempotency expectations. Database owns commit, rollback, and resource cleanup, and reports the outcome without exposing the underlying connection.

**Why:** Related changes must not leave partially applied data when an operation fails, and the consumer needs to express that relationship without taking ownership of persistence internals.

**Boundary:** The consumer determines which operations belong together as part of its application behaviour; Database provides the persistence guarantee. A transaction belongs to one resolved Instance. Atomicity across different Instances or external services is not implied, and Engine-specific transaction mechanisms remain internal to Database. Deadlock, serialization failure, timeout, and retry outcomes are reported distinctly enough for the consumer to choose a safe response; an automatic retry never silently duplicates a non-idempotent operation.

<br>

## 2.15 Portability and schema integrity are explicit

**Rule:** Every persistence decision is classified as portable contract, portable mapping, or engine-specific extension. Engine-specific types, SQL, indexes, transaction features, and constraints are isolated behind the Storage Adapter and recorded with their compatibility and replacement impact. A Database implementation never presents an engine-specific guarantee as a portable Database guarantee.

Migration history includes an integrity marker for each migration and a verified relationship to the resolved schema. Database detects unexpected schema drift before normal operation or reports it as a blocking state according to the selected operational policy. Concurrent migration runners coordinate through an engine-supported lock or equivalent mechanism, and a failed migration cannot be recorded as successfully applied.

**Why:** Portability is meaningful only when its limits are visible, and reproducibility requires proving that the running structure matches the recorded structure.

**Boundary:** Preferences may select an engine-specific feature, but they cannot silently change the portable contract. Drift detection and migration coordination are Database responsibilities; application code never repairs drift by issuing ad-hoc structural commands.

<br>

## 2.16 Persistence security and observability are bounded

**Rule:** Database applies least privilege to runtime identities, records security-relevant persistence outcomes without recording secrets, and provides operational signals for connection failure, migration failure, constraint violation, transaction conflict, and protected-data access. Logs, metrics, traces, backups, exports, and error payloads follow the same credential and sensitive-data protection rules as normal reads.

**Why:** A secure schema can still leak data through diagnostics, backups, or overly powerful runtime identities.

**Boundary:** Database does not own application authorization or business policy, but it does enforce its own storage-level access boundary and never treats observability as an exception to data protection.

<br>

# 3. Documentation Standard

The Database Component MUST include a public `README.md` at its package boundary. The README is a required developer-facing explanation of the completed Database package.

The README MUST explain:

- Database's responsibilities and boundaries;
- the three internal layers and their dependency direction;
- the public Database Interface and Instance Registry;
- Engine selection, runtime configuration, migrations, and transactions;
- the boundary between Database, Model, Backend, Platform, and Development;
- credential protection, controlled SQL, and operational safety rules;
- domain-neutral examples that do not expose project-specific Target information.

The README MUST include complete, runnable, domain-neutral examples showing how a developer uses the public Database package to:

- add or create a record from an imported Model type or instance;
- read one record by its typed identifier, such as an identifier equal to `1`;
- list records with typed criteria, deterministic ordering, and pagination where supported;
- update or edit a record while preserving Model validation and partial-update semantics;
- delete a record and observe the documented constraint or failure result;
- enable or disable a Model that declares a `status` field;
- select an Instance explicitly and use the configured default when selection is omitted;
- group related operations in one transaction and observe commit or rollback;
- handle the public result, validation error, not-found result, constraint failure, and transaction failure.

These examples MUST pass Model types or instances through the public interface. They MUST NOT identify a Model by a string such as `"Entity"`, pass an unrelated untyped field dictionary, expose a connection, or import an internal adapter or ORM object. If controlled SQL is documented, its example MUST show parameterized values, allow-listed structure, transaction usage, and protected results.

The README MUST be generated or updated as part of Database development and verified for existence, completeness, and consistency with the public interface before Database is reported complete.

---

# 4. Decision Order

When multiple persistence implementations are possible, prefer in this order:

1. Preserve the logical Model's meaning.
2. Preserve the Database public contract and component boundary.
3. Enforce the required persistence guarantee under concurrency.
4. Prefer the portable representation.
5. Prefer explicit, traceable migration and mapping decisions.
6. Apply least privilege and protected-data handling.
7. Use the selected Engine's supported capabilities.
8. Add an engine-specific extension only when its impact is recorded and justified.
9. Prefer the simplest maintainable implementation.

---

# 5. At a Glance

## MUST

- Implement Database as an independent package with Interface, Data Logic and Mapping, and Storage Adapter layers.
- Derive persistence mapping from the logical Model without redefining domain meaning.
- Keep schema, migrations, mappings, constraints, and required initial data reproducible from the repository.
- Route consumer data access through the public generic interface and Instance Registry.
- Preserve relationship meaning, persistence constraints, transaction guarantees, and credential protection.
- Verify migration integrity, schema drift, concurrency handling, and least-privilege operation.
- Provide and verify a developer-facing Database README.

## SHOULD

- Prefer portable mappings and standard SQL capabilities.
- Prefer typed Model-driven operations over raw SQL.
- Prefer tested reversals for safe migrations and explicit recovery procedures for irreversible changes.
- Prefer deterministic naming, explicit mapping, observable failures, and idempotent retries.

## NEVER

- Let consumers import connections, adapters, mappings, ORM objects, or secrets.
- Let application code change schema outside Migration.
- Accept uncontrolled SQL, interpolated identifiers, structural commands, or privilege changes through the public interface.
- Expose credential storage representations, secrets, or protected data through results, logs, backups, or errors.
- Invent domain Models, silently weaken persistence guarantees, or redirect an unknown Instance to the default.
- Claim engine-specific behavior is portable without recording its limitation.

# 6. Final Rule

When a Database decision is not explicitly covered, preserve the logical Model's meaning, keep the Database boundary independent of consumers and engine internals, prefer the safest portable representation, and record any consequential engine-specific choice. Never silently invent domain meaning, weaken a persistence guarantee, bypass migration history, or expose a connection, secret, or protected storage representation.
