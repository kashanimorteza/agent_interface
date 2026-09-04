# Database Principles

This document is the personality of the database item: the fixed convictions that shape every decision about persistent data, whatever engine, tool, or project is in play. It is written for the Agent that generates, plans against, or implements the database item, and for the Developer who wants to know why the database behaves the way it does.

It deliberately names no engine, no migration tool, no version, and no default. Those are technical choices and live in the database Preferences; they may change from project to project without touching a single line here. The exact shape of the generated database configuration lives in the database Schema. The three layers are read together, but each answers a different question: this document answers *why and under what rules*, the Preferences answer *with what*, and the Schema answers *in what form*.

Every statement here is mandatory. A preference can never override a principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. The database is independent of its engine

The design of the database — its tables, fields, relationships, constraints, and rules — is described in terms that do not belong to any particular database server. The engine is an implementation detail chosen late, in the preferences, and it must be possible to replace it without redesigning the data.

This is what is usually called being *database-agnostic*. The practical test is simple: if the engine changed tomorrow, the contract consumers rely on should describe the same tables with the same meaning, and only the engine-specific section of the configuration should differ.

<br>

## 2. The whole database is defined as code

Everything needed to recreate the database from nothing must live in the repository: the schema, its history of changes, its constraints and indexes, and any initial data the project declares. Nothing about the database's structure may exist only inside a running server, only in someone's memory, or only in a manual step.

This is *schema as code*. Its purpose is reproducibility: a new environment, a new server, or a fresh checkout must be able to rebuild an identical database by running what is in the repository, with no hand work.

<br>

## 3. Every change to the schema is an ordered, reversible migration

The schema never changes in place. Each change is expressed as one migration that has a fixed position in an ordered history and that can be undone. The migration history is the authoritative record of how the database came to look the way it does.

Application code never creates, alters, or drops database objects directly. Convenience shortcuts — an ORM that silently creates tables at startup, a script that patches a column by hand — are forbidden, because they produce a database whose state cannot be explained by its migration history.

<br>

## 4. The database item owns the complete persistence layer

The database item alone owns the engine, physical storage, runtime connection, ORM, model-to-storage mappings, schema, constraints, indexes, migration history, and the data-access contract it publishes. No other item may make or change these decisions.

The other side of ownership is restraint: the database item does not own application behaviour, the HTTP API, the frontend, or deployment secrets. Its boundaries are written explicitly in its configuration so that an Agent never infers a responsibility that was not given.

<br>

## 5. All data access goes through one generic interface

Consumers never receive the engine connection and never reach into tables, ORM mappings, migrations, or physical database files. They use only the frozen data-access contract and the interface implemented by the database layer.

The interface is generic rather than one access implementation per model. A caller identifies the model, selects a supported operation, and supplies the data or criteria required by that operation. The same interface performs create, read, list, update, delete, and status operations for every persistent model indexed by the project.

The status operation accepts exactly one action: `enable` or `disable`. It is available only when the selected model declares a `status` field and changes that field to the corresponding enabled or disabled value defined by its field contract. A model without a `status` field rejects the operation; the interface never invents the field or silently turns status into a general update.

The interface also supports controlled SQL-command execution for cases that cannot be expressed through the standard model operations. SQL execution stays inside the database boundary, uses explicit parameters rather than value interpolation, and never exposes the underlying connection to the caller.

<br>

## 6. A published contract is frozen, versioned, and never edited

The contract the database publishes is the promise other items build on. Once frozen it is never modified. A change means a new contract version and migrations that move the database from one version to the next; the old version stays intact for as long as anything depends on it.

The implemented schema and the published contract must match exactly. If they ever differ, the contract is wrong and the discrepancy is reported, never silently absorbed.

<br>

## 7. Models become tables, and model rules become constraints — traceably

Every domain model is persistent and maps to one table unless the project explicitly marks the model as non-persistent or supplies a different mapping. The default table name is derived from the model name by one consistent convention; an explicit project table name always wins. The generation operation writes every resolved table name, and the source model it implements, explicitly into the contract — a reader never has to derive a name.

Every rule declared on a model is preserved in the database and represented in its table's contract. A rule with one clear representation is resolved deterministically — a rule allowing one record per combination of related models becomes a composite unique constraint over those foreign keys. A rule with several possible representations is resolved by whichever preserves the domain meaning best. In both cases the resulting constraint records the source rule, so a reader can always trace a constraint back to the requirement that produced it. No model rule is ever silently dropped.

<br>

## 8. Relationships are explicit, never guessed

A relationship between models is represented by a foreign-key field whose name is derived from the referenced *model*, never from the physical table — `<referenced_model>_id` regardless of whether the table name is singular or plural — or, when the project gives the relationship a role, `<role>_<referenced_model>_id`, such as `source_node_id` and `destination_node_id`. An explicit project field or reference always wins over the derived name. When the project binds a relationship to a field it already declared, that field is the foreign key and no duplicate is invented.

The foreign key references the related table's primary key unless the project names another key, and its type is always exactly the referenced key's type, never chosen independently. Nullability, indexing, and referential actions come from the project when stated and from the preferences when not.

When one model relates to the same target more than once, the relationship roles must be explicit; no role or field name is guessed. The resolved contract always writes the foreign-key field, the referenced table, and the referenced column explicitly.

<br>

## 9. Secrets never live in the database layer

Connection credentials belong to runtime configuration outside the repository's committed files. The database contract publishes the shape of a connection, never its secrets.

Fields that are themselves credentials are each resolved to exactly one supported at-rest mode. An explicit project mode for a field always wins; otherwise the default mode comes from the Preferences. The database contract owns that resolved mode, and the database layer applies the matching persistence transformation without exposing its storage representation to consumers. Encryption keys and other secrets are never written into the contract or into database files.

<br>

## 10. Initial data is project content

When the project declares initial data for a model, seeding becomes part of the database item and each record is mapped to its resolved table. Initial data is never supplied by Preferences, and missing project facts are never invented.

Every key in a seed record must name a declared field of its model. Before generation, each record must satisfy its required relationship references and every non-nullable field through an explicit value, a database default, or safe generated behaviour permitted by the field contract. Records are resolved in dependency order; a literal relationship id is preserved exactly and must reference an initial or pre-existing target row — it is never renumbered or replaced by an inferred reference. Seeding must be repeatable without creating duplicate logical records or breaking any uniqueness rule.

<br>

## 11. Generated versions are concrete

A concrete version stated by the project is preserved exactly. A version supplied as *latest* by the Preferences is resolved to a stable release compatible with the complete selected database tool stack, and only the concrete result is written. The word *latest* never appears in generated database configuration.
