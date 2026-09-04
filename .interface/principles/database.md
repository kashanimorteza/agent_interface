# Database Principles

This document is the personality of the database item: the fixed convictions that shape every decision about persistent data, whatever engine, tool, or project is in play. It is written for the Agent that generates, plans against, or implements the database item, and for the Developer who wants to know why the database behaves the way it does.

It deliberately names no engine, no migration tool, no version, and no default. Those are technical choices and live in the preferences file (`.interface/preferences/database.yaml`); they may change from project to project without touching a single line here. The exact shape of the generated `config/database.yaml` lives in the schema (`.interface/schema/database.yaml`). The three layers are read together, but each answers a different question: this document answers *why and under what rules*, the preferences answer *with what*, and the schema answers *in what form*.

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

## 4. The database item has one owner, and it owns everything physical

The database item alone decides the engine, the physical storage, the schema, the constraints, the indexes, the migration history, and the contract it publishes. No other item may make or change these decisions.

The other side of ownership is restraint: the database item does not own the backend's ORM behaviour, the API, the frontend, or deployment secrets. Its boundaries are written explicitly in its configuration so that an Agent never infers a responsibility that was not given.

<br>

## 5. Nobody talks to the database directly

Consumers of the database — the backend above all — never reach into tables on their own. They use exactly two things: the frozen database contract, which says what exists and what it means, and credential-free runtime connection information, which says how to reach it. They never infer the schema from migrations or from the physical database files.

Inside a consumer, all access to persistent data goes through a dedicated data-access layer (the *Repository* pattern) rather than being scattered through application logic. Within that layer, reading and writing are separate responsibilities (a light form of *command–query separation*), and each model has its own dedicated access logic, so the behaviour of one model can change without touching another. The database item demands this discipline of its consumers; the consumer implements it.

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

When one model relates to the same target more than once and the roles are not explicit, the Agent records an open question rather than guessing names. Whatever the resolution, the generation operation writes the foreign-key field, the referenced table, and the referenced column explicitly into the contract.

<br>

## 9. Secrets never live in the database layer

Connection credentials belong to runtime configuration outside the repository's committed files. The database contract publishes the shape of a connection, never its secrets.

Fields that are themselves credentials — passwords, API keys — are each resolved to exactly one at-rest mode: plaintext, which stores the original value unchanged; a one-way hash, for values that only need verification and are never recovered; or reversible encryption, for values the application must recover. An explicit project mode for a field always wins; otherwise the default mode comes from the preferences. The database contract owns that resolved mode for each field; the consuming backend owns the matching runtime transformation and never infers or changes the mode. Encryption keys and other secrets are never written into the contract or into database files.

<br>

## 10. Initial data is project content

When the project declares initial data for a model, seeding becomes part of the database item and each record is mapped to its resolved table. Initial data is never supplied by preferences: the Agent may choose safe technical generation behaviour for a required value the project left open, but it never invents project facts.

Every key in a seed record must name a declared field of its model. Before generation, each record must satisfy its required relationship references and every non-nullable field — through an explicit value, a database default, or safe generated behaviour; an open question is raised only when a required project value is critical and no safe generated behaviour exists. Records are resolved in dependency order; a literal relationship id is preserved exactly and must reference an initial or pre-existing target row — it is never renumbered or replaced by an inferred reference. Seeding must be repeatable without creating duplicate logical records or breaking any uniqueness rule.

<br>

## 11. When the project is silent, decide deliberately

An explicit project value always wins. When the project says nothing about a technical choice, the generation operation resolves it from the preferences, or chooses a compatible option and records the choice. Downstream operations consume the resolved configuration and never reinterpret preferences on their own.

A concrete version the project states is preserved exactly. A version left to the preferences is resolved to the latest stable release compatible with the whole selected tool stack, and only that concrete value is written; the word *latest* never appears in a generated configuration. If the current stable version cannot be verified, the best supported compatible version available from current evidence is selected and the choice is recorded. An open question is raised only when the alternatives would materially change domain meaning, security, data integrity, or a frozen contract — ordinary technical decisions are made and recorded, not escalated.
