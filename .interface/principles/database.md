# Database Principles

Database is the Component that owns the project's complete persistence layer. It turns the logical Models into stored data, keeps the whole storage structure reproducible from the repository, and publishes one generic interface through which every consumer reads and writes without ever meeting the engine behind it. Its philosophy, responsibilities, and boundaries are fixed and independent of any engine, tool, or project.

## Terms

- **Database Interface** — the layer that is the only boundary published to consumers, exposing Model operations and Instance discovery and selection.
- **Data Logic and Mapping** — the layer that implements generic Model operations and resolves how logical Models, fields, relationships, rules, and initial data are physically mapped and enforced.
- **Storage Adapter** — the layer that owns the connection to the selected Engine and performs physical persistence operations.
- **Engine** — the database technology behind the Storage Adapter, chosen late and replaceable.
- **Instance** — one selectable database identity with a stable key, name, purpose, and Engine binding.
- **Instance Registry** — the published catalogue through which consumers discover Instance identities and the default, without receiving connections or secrets.
- **Migration** — one recorded, ordered, reversible change to the storage structure, and the authoritative record of how that structure was reached.
- **At-rest mode** — the resolved persistence transformation applied to a field that is a credential.

## Relationships

- **Consumes Model** — the logical Models, fields, relationships, rules, and initial data that Database maps and enforces.
- **Consumes Development** — the common package standard and the centralized runtime configuration through which Platform delivers connection settings.
- **Consumed by Backend** — the generic data-access interface and Instance Registry, reached only through Backend's Data Access layer.

Technical choices and defaults belong to Database Preferences. Database implementation applies those choices to the current project definition.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Database is an independent package with three internal layers

**Rule:** Database is implemented as an independent package with a documented public interface. Compatible in-process consumers import the public Database gateway and Instance Registry from this package. Database is formed from three distinct internal layers:

- **Database Interface** is the only boundary published to consumers and exposes Model operations plus Instance discovery and selection;
- **Data Logic and Mapping** implements generic Model operations and resolves the physical persistence mapping and enforcement of logical Models, fields, relationships, rules, and initial data; and
- **Storage Adapter** owns the connection to the selected Database Engine and performs physical persistence operations.

The dependency direction is Database Interface → Data Logic and Mapping → Storage Adapter → Database Engine.

**Why:** One published boundary over an ordered internal chain is what lets the engine, the mapping, and the exposed operations each change without the others being rewritten.

**Boundary:** Consumers never import internal adapters, mappings, connections, or configuration implementation. Consumers never bypass Database Interface, and an internal layer never bypasses the layer responsible for the next boundary. Migration is internal Database tooling rather than a runtime application layer: it changes the physical storage structure through the Storage Adapter's resolved technology without becoming part of the public Database Interface.

<br>

## 2. Database is independent of its engine

**Rule:** The physical persistence design owned by Database — its tables, columns, foreign keys, constraints, indexes, and enforcement mechanisms — is derived from the logical Model and described in terms that do not belong to any particular database server. It must be possible to replace the engine without redesigning the domain data.

**Why:** If the engine changes, consumers retain the same data-access behaviour and domain meaning while only internal storage and engine-specific configuration may need to differ.

**Boundary:** The engine is an implementation detail chosen late.

<br>

## 3. The whole Database is defined as code

**Rule:** Everything needed to recreate Database from nothing lives in the repository: its storage schema, history of changes, constraints, indexes, and any declared initial data.

**Why:** This provides reproducibility: a new environment, server, or checkout can rebuild an identical Database without manual structural work.

**Boundary:** Nothing about the Database structure exists only inside a running server, only in someone's memory, or only in a manual step.

<br>

## 4. Storage-schema changes are ordered and reversible

**Rule:** The storage schema never changes without a recorded migration. Each change has a fixed position in an ordered history and can be undone. Migration history is the authoritative record of how the Database reached its current structure.

**Why:** An ordered, reversible history is the only way the current structure can be explained, reproduced, or safely stepped back.

**Boundary:** Application code never creates, alters, or drops database objects directly. Silent startup creation and manual structural patches are excluded because they create storage state that cannot be explained by migration history.

<br>

## 5. Database owns the complete persistence layer

**Rule:** Database alone owns supported engine integration, Database Instances, physical storage, runtime connections, ORM, model-to-storage mappings, storage schema, physical constraints, indexes, migration history, and the generic data-access interface it publishes.

**Why:** Persistence decisions interact with each other, so splitting them across Components produces storage that no single Component can reason about.

**Boundary:** Logical Models, fields, relationships, and domain rules remain owned by Model; Database owns only their persistence mapping and enforcement. No other Component makes or changes Database-owned decisions. Database does not own application behaviour, the HTTP API, Frontend, or deployment secrets. Its boundaries remain explicit in the implementation and its public documentation.

<br>

## 6. All data access goes through one generic interface

**Rule:** Consumers use only the generic interface implemented by Database. The interface is generic rather than one access implementation per Model: a caller supplies a Model type or Model instance from the public Model package, selects a supported operation, and supplies any criteria required by that operation. The same interface performs create, read, list, update, delete, and status operations for every persistent Model, and Data Logic uses one Model-driven operation pipeline rather than a separate business-logic implementation for every Model.

The status operation accepts exactly one action: `enable` or `disable`. It is available only when the selected Model declares a `status` field and changes that field to the corresponding enabled or disabled value.

The interface also supports controlled SQL-command execution for cases that cannot be expressed through standard Model operations, using explicit parameters rather than value interpolation.

**Why:** Differences between Models come from their resolved fields, relationships, constraints, rules, and storage mappings, so one pipeline serves them all and each new Model costs no new access implementation.

**Boundary:** Consumers never receive the engine connection and never reach into tables, ORM mappings, migrations, or physical database files. Model identity and data are not passed as an untyped Model-name string and unrelated field dictionary. A Model without a `status` field rejects the status operation. SQL execution stays inside the Database boundary and never exposes the underlying connection. Model-specific application Behaviour remains in Backend Logic and never enters Database.

<br>

## 7. Database Instances are explicit and selectable

**Rule:** Every Database Instance has a stable identifier, human-readable name, stated purpose, and one supported Engine binding. Instance identity is distinct from Engine identity: several Instances may use the same Engine while serving different purposes. Database publishes an Instance Registry through its public interface so consumers can discover available Instance identities and select one. Exactly one Instance is the default, and when a consumer does not select an Instance, Database uses that default explicitly and predictably. The number of Instances is derived from the Instance collection and is never maintained as a separate authoritative value.

**Why:** A project outgrows one database, and naming each Instance by purpose lets a consumer choose the right one without learning how any of them connect.

**Boundary:** The registry exposes no raw connection objects and no secret values. Database owns Instance definitions and connection handling; Platform may select or bind an Instance for another layer without taking ownership of it.

<br>

## 8. Models become tables and Model rules become constraints — traceably

**Rule:** Every persistent domain Model maps to a table. An explicit storage mapping takes precedence over a derived mapping, and every resolved table records the source Model it implements. Every Model rule is preserved and represented in the storage schema: a rule with one clear representation is resolved deterministically, and a rule with several possible representations is resolved in the way that best preserves its domain meaning.

**Why:** A rule that exists only in the domain description is a rule the stored data can violate.

**Boundary:** The resulting constraint remains traceable to its source rule; no Model rule is silently dropped.

<br>

## 9. Relationships are explicit and consistently resolved

**Rule:** A relationship between Models is represented explicitly by a foreign-key field. An explicit relationship field or reference always takes precedence over a default, and an existing declared relationship field is reused rather than duplicated. The foreign key references the related key and uses the same type. When one Model relates to the same target more than once, the relationship roles remain explicit, and the resolved storage schema records the foreign-key field, referenced table, and referenced column.

**Why:** Explicit, recorded connections are what make stored data navigable and enforceable rather than merely conventional.

**Boundary:** Unstated naming, nullability, indexing, and referential actions are resolved through Database Preferences.

<br>

## 10. Connection secrets stay outside and credential storage stays internal

**Rule:** Connection credentials belong to runtime configuration outside committed files. Fields that are credentials are each resolved to one supported at-rest mode: an explicit mode takes precedence, and otherwise Database Preferences supply the default. Database applies the matching persistence transformation.

**Why:** A secret in a committed file is public, and a credential whose at-rest treatment is decided per caller is treated inconsistently.

**Boundary:** Runtime connection settings are internal to Database; neither their shape nor secret values are published through the data-access interface. The storage representation of a credential is never exposed to consumers. Encryption keys and other secrets are never written into generated Interface or Database files.

<br>

## 11. Initial data preserves declared meaning

**Rule:** When initial data exists for a Model, seeding becomes part of Database and each record maps to its resolved table. Every seed key names a resolved Model field. Each record satisfies its required relationships and non-nullable fields through a supplied value, a resolved default, or permitted generated behaviour. Records are resolved in dependency order, explicit relationship identifiers are preserved, and seeding is repeatable without duplicating logical records or breaking uniqueness rules.

**Why:** Initial records are part of what the project declared, so a rebuilt database is only equivalent if they come back with the same meaning.

**Boundary:** Initial data is never supplied by Database Preferences.

<br>

## At a Glance

- **Must** — Database is an independent package formed from Database Interface, Data Logic and Mapping, and Storage Adapter, in that dependency direction *(1)*
- **Never** — a consumer imports internal adapters, mappings, connections, or configuration, or bypasses Database Interface *(1)*
- **Never** — migration tooling becomes part of the public Database Interface *(1)*
- **Must** — the physical design is derived from the logical Model and described independently of any database server *(2)*
- **Must** — everything needed to recreate Database from nothing lives in the repository *(3)*
- **Never** — any part of the Database structure exists only in a running server, a memory, or a manual step *(3)*
- **Must** — every storage-schema change is a recorded, ordered, reversible migration *(4)*
- **Never** — application code creates, alters, or drops database objects directly *(4)*
- **Must** — Database alone owns engines, Instances, storage, connections, ORM, mappings, schema, constraints, indexes, migrations, and the published interface *(5)*
- **Never** — Database owns application behaviour, the HTTP API, Frontend, or deployment secrets *(5)*
- **Must** — every consumer reaches data through one generic Model-driven interface covering create, read, list, update, delete, and status *(6)*
- **Must** — the status operation accepts only `enable` or `disable`, and only for a Model declaring a `status` field *(6)*
- **Must** — SQL execution uses explicit parameters and stays inside the Database boundary *(6)*
- **Never** — a consumer receives the engine connection or reaches into tables, ORM mappings, migrations, or database files *(6)*
- **Never** — Model identity is passed as an untyped name string with an unrelated field dictionary *(6)*
- **Must** — every Instance has a stable identifier, name, purpose, and Engine binding, and exactly one is the default *(7)*
- **Never** — the Instance Registry exposes raw connections or secret values *(7)*
- **Must** — every persistent Model maps to a table that records its source Model, and every Model rule is represented in the schema *(8)*
- **Never** — a Model rule is silently dropped or left untraceable to its source *(8)*
- **Must** — a relationship is an explicit foreign key referencing the related key with the same type, with roles kept explicit *(9)*
- **Must** — connection credentials live in runtime configuration outside committed files *(10)*
- **Must** — every credential field resolves to one at-rest mode, explicit first, otherwise the Preferences default *(10)*
- **Never** — connection settings, credential storage representations, or encryption keys are exposed or written into generated files *(10)*
- **Must** — declared initial data is seeded in dependency order, repeatably, preserving explicit relationship identifiers *(11)*
- **Never** — initial data is supplied by Database Preferences *(11)*
