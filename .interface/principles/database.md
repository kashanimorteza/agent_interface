# Database Principles

Database Principles define the fixed philosophy, responsibilities, and boundaries of the Database Component, independent of any engine, tool, or project.

Technical choices and defaults belong to Database Preferences. The exact shape of the generated Database configuration belongs to the Database Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Database is independent of its engine

The design of Database — its tables, fields, relationships, constraints, and rules — is described in terms that do not belong to any particular database server. The engine is an implementation detail chosen late, and it must be possible to replace it without redesigning the data.

If the engine changes, consumers retain the same data-access behaviour and domain meaning while only internal storage and engine-specific configuration may need to differ.

<br>

## 2. The whole Database is defined as code

Everything needed to recreate Database from nothing lives in the repository: its storage schema, history of changes, constraints, indexes, and any declared initial data. Nothing about the Database structure exists only inside a running server, only in someone's memory, or only in a manual step.

This provides reproducibility: a new environment, server, or checkout can rebuild an identical Database without manual structural work.

<br>

## 3. Storage-schema changes are ordered and reversible

The storage schema never changes without a recorded migration. Each change has a fixed position in an ordered history and can be undone. Migration history is the authoritative record of how the Database reached its current structure.

Application code never creates, alters, or drops database objects directly. Silent startup creation and manual structural patches are excluded because they create storage state that cannot be explained by migration history.

<br>

## 4. Database owns the complete persistence layer

Database alone owns the engine, physical storage, runtime connection, ORM, model-to-storage mappings, storage schema, constraints, indexes, migration history, and the generic data-access interface it publishes. No other Component makes or changes those decisions.

Database does not own application behaviour, the HTTP API, Frontend, or deployment secrets. Its resolved boundaries remain explicit in its generated configuration.

<br>

## 5. All data access goes through one generic interface

Consumers never receive the engine connection and never reach into tables, ORM mappings, migrations, or physical database files. They use only the generic interface implemented by Database.

The interface is generic rather than one access implementation per Model. A caller identifies the Model, selects a supported operation, and supplies the data or criteria required by that operation. The same interface performs create, read, list, update, delete, and status operations for every persistent Model.

The status operation accepts exactly one action: `enable` or `disable`. It is available only when the selected Model declares a `status` field and changes that field to the corresponding enabled or disabled value. A Model without a `status` field rejects the operation.

The interface also supports controlled SQL-command execution for cases that cannot be expressed through standard Model operations. SQL execution stays inside the Database boundary, uses explicit parameters rather than value interpolation, and never exposes the underlying connection.

<br>

## 6. Models become tables and Model rules become constraints — traceably

Every persistent domain Model maps to a table. An explicit storage mapping takes precedence over a derived mapping, and every resolved table records the source Model it implements.

Every Model rule is preserved and represented in the storage schema. A rule with one clear representation is resolved deterministically. A rule with several possible representations is resolved in the way that best preserves its domain meaning. The resulting constraint remains traceable to its source rule; no Model rule is silently dropped.

<br>

## 7. Relationships are explicit and consistently resolved

A relationship between Models is represented explicitly by a foreign-key field. An explicit relationship field or reference always takes precedence over a default, and an existing declared relationship field is reused rather than duplicated.

The foreign key references the related key and uses the same type. Unstated naming, nullability, indexing, and referential actions are resolved through Database Preferences.

When one Model relates to the same target more than once, the relationship roles remain explicit. The resolved storage schema records the foreign-key field, referenced table, and referenced column.

<br>

## 8. Connection secrets stay outside and credential storage stays internal

Connection credentials belong to runtime configuration outside committed files. Runtime connection settings are internal to Database; neither their shape nor secret values are published through the data-access interface.

Fields that are credentials are each resolved to one supported at-rest mode. An explicit mode takes precedence; otherwise Database Preferences supply the default. Database applies the matching persistence transformation without exposing its storage representation to consumers. Encryption keys and other secrets are never written into generated Interface or Database files.

<br>

## 9. Initial data preserves declared meaning

When initial data exists for a Model, seeding becomes part of Database and each record maps to its resolved table. Initial data is never supplied by Database Preferences.

Every seed key names a resolved Model field. Each record satisfies its required relationships and non-nullable fields through a supplied value, a resolved default, or permitted generated behaviour. Records are resolved in dependency order, explicit relationship identifiers are preserved, and seeding is repeatable without duplicating logical records or breaking uniqueness rules.
