# Database Principles

Database Principles define the fixed philosophy, responsibilities, and boundaries of the Database Component, independent of any engine, tool, or project.

Technical choices and defaults belong to Database Preferences. Database implementation applies those choices to the current project definition.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Database is an independent package with three internal layers

Database is implemented as an independent package with a documented public interface. Compatible in-process consumers import the public Database gateway and Instance Registry from this package; they never import its internal adapters, mappings, connections, or configuration implementation.

Database is formed from three distinct internal layers:

- **Database Interface** is the only boundary published to consumers and exposes Model operations plus Instance discovery and selection;
- **Data Logic and Mapping** implements generic Model operations and resolves the physical persistence mapping and enforcement of logical Models, fields, relationships, rules, and initial data; and
- **Storage Adapter** owns the connection to the selected Database Engine and performs physical persistence operations.

The dependency direction is Database Interface → Data Logic and Mapping → Storage Adapter → Database Engine. Consumers never bypass Database Interface, and an internal layer never bypasses the layer responsible for the next boundary.

Migration is internal Database tooling rather than a runtime application layer. It changes the physical storage structure through the Storage Adapter's resolved technology without becoming part of the public Database Interface.

<br>

## 2. Database is independent of its engine

The physical persistence design owned by Database — its tables, columns, foreign keys, constraints, indexes, and enforcement mechanisms — is derived from the logical Model and described in terms that do not belong to any particular database server. The engine is an implementation detail chosen late, and it must be possible to replace it without redesigning the domain data.

If the engine changes, consumers retain the same data-access behaviour and domain meaning while only internal storage and engine-specific configuration may need to differ.

<br>

## 3. The whole Database is defined as code

Everything needed to recreate Database from nothing lives in the repository: its storage schema, history of changes, constraints, indexes, and any declared initial data. Nothing about the Database structure exists only inside a running server, only in someone's memory, or only in a manual step.

This provides reproducibility: a new environment, server, or checkout can rebuild an identical Database without manual structural work.

<br>

## 4. Storage-schema changes are ordered and reversible

The storage schema never changes without a recorded migration. Each change has a fixed position in an ordered history and can be undone. Migration history is the authoritative record of how the Database reached its current structure.

Application code never creates, alters, or drops database objects directly. Silent startup creation and manual structural patches are excluded because they create storage state that cannot be explained by migration history.

<br>

## 5. Database owns the complete persistence layer

Database alone owns supported engine integration, Database Instances, physical storage, runtime connections, ORM, model-to-storage mappings, storage schema, physical constraints, indexes, migration history, and the generic data-access interface it publishes. Logical Models, fields, relationships, and domain rules remain owned by Model; Database owns only their persistence mapping and enforcement. No other Component makes or changes Database-owned decisions.

Database does not own application behaviour, the HTTP API, Frontend, or deployment secrets. Its boundaries remain explicit in the implementation and its public documentation.

<br>

## 6. All data access goes through one generic interface

Consumers never receive the engine connection and never reach into tables, ORM mappings, migrations, or physical database files. They use only the generic interface implemented by Database.

The interface is generic rather than one access implementation per Model. A caller supplies a Model type or Model instance from the public Model package, selects a supported operation, and supplies any criteria required by that operation. Model identity and data are not passed as an untyped Model-name string and unrelated field dictionary. The same interface performs create, read, list, update, delete, and status operations for every persistent Model.

Data Logic uses one Model-driven operation pipeline rather than a separate business-logic implementation for every Model. Differences between Models come from their resolved fields, relationships, constraints, rules, and storage mappings. Model-specific application Behaviour remains in Backend Logic and never enters Database.

The status operation accepts exactly one action: `enable` or `disable`. It is available only when the selected Model declares a `status` field and changes that field to the corresponding enabled or disabled value. A Model without a `status` field rejects the operation.

The interface also supports controlled SQL-command execution for cases that cannot be expressed through standard Model operations. SQL execution stays inside the Database boundary, uses explicit parameters rather than value interpolation, and never exposes the underlying connection.

<br>

## 7. Database Instances are explicit and selectable

Every Database Instance has a stable identifier, human-readable name, stated purpose, and one supported Engine binding. Instance identity is distinct from Engine identity: several Instances may use the same Engine while serving different purposes.

Database publishes an Instance Registry through its public interface so consumers can discover available Instance identities and select one without receiving raw connection objects or secret values. Exactly one Instance is the default. When a consumer does not select an Instance, Database uses that default explicitly and predictably.

The number of Instances is derived from the Instance collection and is never maintained as a separate authoritative value. Database owns Instance definitions and connection handling; Platform may select or bind an Instance for another layer without taking ownership of it.

<br>

## 8. Models become tables and Model rules become constraints — traceably

Every persistent domain Model maps to a table. An explicit storage mapping takes precedence over a derived mapping, and every resolved table records the source Model it implements.

Every Model rule is preserved and represented in the storage schema. A rule with one clear representation is resolved deterministically. A rule with several possible representations is resolved in the way that best preserves its domain meaning. The resulting constraint remains traceable to its source rule; no Model rule is silently dropped.

<br>

## 9. Relationships are explicit and consistently resolved

A relationship between Models is represented explicitly by a foreign-key field. An explicit relationship field or reference always takes precedence over a default, and an existing declared relationship field is reused rather than duplicated.

The foreign key references the related key and uses the same type. Unstated naming, nullability, indexing, and referential actions are resolved through Database Preferences.

When one Model relates to the same target more than once, the relationship roles remain explicit. The resolved storage schema records the foreign-key field, referenced table, and referenced column.

<br>

## 10. Connection secrets stay outside and credential storage stays internal

Connection credentials belong to runtime configuration outside committed files. Runtime connection settings are internal to Database; neither their shape nor secret values are published through the data-access interface.

Fields that are credentials are each resolved to one supported at-rest mode. An explicit mode takes precedence; otherwise Database Preferences supply the default. Database applies the matching persistence transformation without exposing its storage representation to consumers. Encryption keys and other secrets are never written into generated Interface or Database files.

<br>

## 11. Initial data preserves declared meaning

When initial data exists for a Model, seeding becomes part of Database and each record maps to its resolved table. Initial data is never supplied by Database Preferences.

Every seed key names a resolved Model field. Each record satisfies its required relationships and non-nullable fields through a supplied value, a resolved default, or permitted generated behaviour. Records are resolved in dependency order, explicit relationship identifiers are preserved, and seeding is repeatable without duplicating logical records or breaking uniqueness rules.
