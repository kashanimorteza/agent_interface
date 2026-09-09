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
- **Transaction** — one unit of data operations on a single Instance whose changes are committed together or rolled back together.

## Relationships

- **Consumes Model** — the logical Models, fields, relationships, rules, and initial data that Database maps and enforces.
- **Consumes Development** — the common package standard and the ownership rules under which Database keeps its own settings and secrets.
- **Consumes Platform** — the Bindings the selected Launch delivers to Database's boundary, without Platform taking ownership of them.
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

**Boundary:** Logical Models, fields, relationships, and domain rules remain owned by Model; Database owns only their persistence mapping and enforcement. No other Component makes or changes Database-owned decisions. Database does not own application behaviour, the HTTP API, Frontend, or secrets belonging to other layers. Database owns its private runtime settings and secrets under Development's rules; Platform delivers the Bindings it needs through the selected Launch. Its boundaries remain explicit in the implementation and its public documentation.

<br>

## 6. All data access goes through one generic interface

**Rule:** Consumers use only the generic interface implemented by Database. The interface is generic rather than one access implementation per Model: a caller supplies a Model type or Model instance from the public Model package, selects a supported operation, and supplies any criteria required by that operation. The same interface performs create, read, list, update, delete, and status operations for every persistent Model, and Data Logic uses one Model-driven operation pipeline rather than a separate business-logic implementation for every Model.

The status operation accepts exactly one action: `enable` or `disable`. It is available only when the selected Model declares a `status` field and changes that field to the corresponding enabled or disabled value.

The interface also supports controlled SQL-command execution for cases that cannot be expressed through standard Model operations, using explicit parameters rather than value interpolation. This route is for data operations on the selected Instance and remains subject to Database's persistence constraints and transaction boundaries. It rejects structural changes, which belong exclusively to Migration. Engine-specific SQL must be identified as such and validated for the selected Engine; it carries no promise of portability when the Engine changes.

Controlled SQL preserves the same data protections as the generic operations. Before accepting a command, Database must establish which data it can read or change and how the applicable protections are enforced. Writes preserve Model validation of the resulting data, persistence constraints, and the resolved credential transformations; reads never expose credential storage representations or runtime secrets, including through derived results. Parameterization alone does not establish these guarantees. A command whose effects or results cannot be handled with these protections is rejected before execution. Validation of resulting changes occurs within the same transaction before commit, and failure rolls back the changes. This does not authorize Database to take over application-context rules owned by Backend Logic.

**Why:** Differences between Models come from their resolved fields, relationships, constraints, rules, and storage mappings, so one pipeline serves them all and each new Model costs no new access implementation.

**Boundary:** Consumers never receive the engine connection or access storage outside the published Database interface. Model identity and data are not passed as an untyped Model-name string and unrelated field dictionary. A Model without a `status` field rejects the status operation. The controlled SQL route is the explicit exception to Model-driven access; it stays inside the Database boundary and exposes no connection, ORM mapping, migration implementation, or physical database file. It grants no direct storage access and cannot bypass Migration or manage the transaction independently of the public transaction boundary. Model-specific application Behaviour remains in Backend Logic and never enters Database.

<br>

## 7. Database Instances are explicit and selectable

**Rule:** Every Database Instance has a stable identifier, human-readable name, stated purpose, and one supported Engine binding. Instance identity is distinct from Engine identity: several Instances may use the same Engine while serving different purposes. Database publishes an Instance Registry through its public interface so consumers can discover available Instance identities and select one. Exactly one Instance is the default, and when a consumer does not select an Instance, Database uses that default explicitly and predictably. The number of Instances is derived from the Instance collection and is never maintained as a separate authoritative value.

Database-owned runtime configuration declares the supported Engine catalogue, the Instance catalogue, and the default selection. Each Instance refers to one supported Engine, and the default refers to an existing Instance. The public Registry derives from the configured Instances rather than maintaining a second catalogue in implementation. A consumer can supply an identity obtained from that Registry to select the Instance for an operation or transaction. An omitted selection uses the configured default; an explicit unknown Instance is rejected, never silently redirected to the default.

**Why:** A project outgrows one database, and naming each Instance by purpose lets a consumer choose the right one without learning how any of them connect.

**Boundary:** The registry exposes no raw connection objects and no secret values. Database owns Instance definitions and connection handling; Platform may deliver the Binding that selects an Instance for another layer without taking ownership of it.

<br>

## 8. Storage mappings and persistence constraints remain traceable to Models

**Rule:** Every persistent domain Model maps to a table. An explicit storage mapping takes precedence over a derived mapping, and every resolved table records the source Model it implements. Database guarantees the Model rules that depend on stored state, including uniqueness across records and the existence of referenced records, and maps the resolved Model's storage-relevant field properties into persistence constraints. Enforcement remains traceable to the source Model declaration and applies when changes are committed, including under concurrent access. Database reuses shared Model validation for checks determined from Model data instead of maintaining competing definitions. A persistence rule with one clear representation is resolved deterministically; when several representations are possible, the choice preserves its declared meaning.

**Why:** Persistence guarantees must hold for stored data even when several consumers write concurrently, while keeping a rule's declaration separate from its enforcement prevents duplicate or conflicting ownership.

**Boundary:** Database does not translate application-context or operation-dependent rules into storage constraints or assume responsibility for Backend Logic. Not every Model rule belongs in the storage schema. A rule within Database's persistence responsibility is never silently dropped or weakened; if the selected Engine cannot represent it directly, Database must provide equivalent enforcement within its boundary or report the unsupported requirement.

<br>

## 9. Relationships are explicit and consistently resolved

**Rule:** Relationship mappings preserve the cardinality, optionality, and roles resolved by Model, including one-to-one, one-to-many, and many-to-many relationships. The physical representation uses explicit foreign keys and any association storage and constraints needed to preserve that meaning. One-to-one mappings enforce the required uniqueness; one-to-many mappings allow the declared multiplicity; many-to-many mappings represent both sides without reducing either to a single reference. Association storage reuses an explicit association Model when one is declared; a purely physical association does not introduce a new domain Model.

An explicit relationship field or reference always takes precedence over a default, and an existing declared relationship field is reused rather than duplicated. Each foreign key references the related key and uses the same type. Its nullability preserves the resolved Model field and relationship optionality; Database does not apply a separate logical nullability default. If a physical relationship field is needed where no logical field is declared, its nullability follows the resolved relationship meaning. When one Model relates to the same target more than once, the relationship roles remain explicit, and the resolved storage schema records each foreign-key field, referenced table, and referenced column. A mapping must preserve the complete relationship constraint; foreign-key nullability alone is not proof that every cardinality or participation requirement is enforced.

**Why:** Explicit, recorded connections are what make stored data navigable and enforceable rather than merely conventional.

**Boundary:** Logical field properties and relationship optionality are resolved under the Model Component's rules before storage mapping. Database Preferences supply only unstated physical mapping choices, such as storage naming, indexing, and referential actions, without overriding the resolved Model meaning.

<br>

## 10. Connection secrets stay outside and credential storage stays internal

**Rule:** Connection credentials belong to runtime configuration outside committed files. Fields that are credentials are each resolved to one supported at-rest mode: an explicit mode takes precedence, and otherwise Database Preferences supply the default. Database applies the matching persistence transformation.

**Why:** A secret in a committed file is public, and a credential whose at-rest treatment is decided per caller is treated inconsistently.

**Boundary:** Runtime connection settings are internal to Database; neither their shape nor secret values are published through the data-access interface. The storage representation of a credential is never exposed to consumers. Encryption keys and connection secrets belong in Database's private runtime area under Development's rules; they never appear in Interface records, general Database configuration, source-controlled implementation, or distributed artifacts. Platform delivers them as Bindings through the selected Launch, without publishing these values to other layers.

<br>

## 11. Initial data preserves declared meaning

**Rule:** When initial data exists for a Model, seeding becomes part of Database and each record maps to its resolved table. Every seed key names a resolved Model field. Each record satisfies its required relationships and non-nullable fields through a supplied value, a resolved default, or permitted generated behaviour. Records are resolved in dependency order, explicit relationship identifiers are preserved, and seeding is repeatable without duplicating logical records or breaking uniqueness rules.

**Why:** Initial records are part of what the project declared, so a rebuilt database is only equivalent if they come back with the same meaning.

**Boundary:** Initial data is never supplied by Database Preferences.

<br>

## 12. Related data operations share an explicit transaction boundary

**Rule:** Database publishes a transaction boundary through its generic interface so a consumer can group related data operations on one Instance. Changes in the group are committed together only when the unit succeeds and all applicable persistence constraints hold; a failed or cancelled unit rolls back its changes. Operations participating in the unit do not commit independently. A standalone write outside an explicit group forms its own atomic unit. Database owns commit, rollback, and resource cleanup, and reports the outcome without exposing the underlying connection.

**Why:** Related changes must not leave partially applied data when an operation fails, and the consumer needs to express that relationship without taking ownership of persistence internals.

**Boundary:** The consumer determines which operations belong together as part of its application behaviour; Database provides the persistence guarantee. A transaction belongs to one resolved Instance. Atomicity across different Instances or external services is not implied, and Engine-specific transaction mechanisms remain internal to Database.

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
- **Must** — Database owns its private runtime settings and secrets under Development, while Platform delivers the Bindings it needs *(5)*
- **Never** — Database owns application behaviour, the HTTP API, Frontend, or another layer's secrets *(5)*
- **Must** — every consumer reaches data through one generic Model-driven interface covering create, read, list, update, delete, and status *(6)*
- **Must** — the status operation accepts only `enable` or `disable`, and only for a Model declaring a `status` field *(6)*
- **Must** — SQL execution uses explicit parameters and stays inside the Database boundary *(6)*
- **Must** — controlled SQL follows the selected Instance's persistence constraints and transaction boundary, with Engine-specific compatibility made explicit *(6)*
- **Must** — controlled SQL preserves Model validation, persistence constraints, credential transformations, and protected output; resulting changes are validated before commit within the same transaction and rolled back on failure *(6)*
- **Never** — a SQL command is accepted when its effects or results cannot be handled with the required data protections; parameterization alone is insufficient *(6)*
- **Never** — the public SQL route performs structural changes or bypasses Migration or transaction ownership *(6)*
- **Never** — a consumer receives the engine connection or accesses storage outside the published Database interface *(6)*
- **Never** — Model identity is passed as an untyped name string with an unrelated field dictionary *(6)*
- **Must** — every Instance has a stable identifier, name, purpose, and Engine binding, and exactly one is the default *(7)*
- **Must** — Database-owned runtime configuration declares supported Engines, Instances, and a valid default; the public Registry derives from those Instances and provides selectable identities for operations and transactions *(7)*
- **Never** — an explicit unknown Instance silently falls back to the default *(7)*
- **Never** — the Instance Registry exposes raw connections or secret values *(7)*
- **Must** — every persistent Model maps to a table that records its source Model, and persistence constraints remain traceable to their logical declarations *(8)*
- **Must** — Database guarantees constraints requiring stored state at commit, including under concurrent access, and reuses shared Model validation *(8)*
- **Never** — Database absorbs application-context validation or silently drops or weakens a required persistence constraint *(8)*
- **Must** — relationship mappings preserve Model cardinality, optionality, and roles through explicit foreign keys and the association storage and constraints they require *(9)*
- **Must** — one-to-one uniqueness, one-to-many multiplicity, and both sides of many-to-many relationships are preserved; an explicit association Model is reused *(9)*
- **Never** — purely physical association storage introduces a domain Model, or foreign-key nullability alone is treated as proof of all relationship constraints *(9)*
- **Must** — each foreign key references the related key with the same type, with roles and physical references recorded explicitly *(9)*
- **Must** — relationship nullability follows the resolved Model meaning; Database defaults cover only unstated physical mapping choices *(9)*
- **Must** — connection credentials live in runtime configuration outside committed files *(10)*
- **Must** — every credential field resolves to one at-rest mode, explicit first, otherwise the Preferences default *(10)*
- **Must** — Database connection secrets and encryption keys reside in its private runtime area under Development's rules *(10)*
- **Never** — connection settings or credential storage representations are exposed through the public interface, or secrets enter Interface records, general configuration, source-controlled implementation, or distributed artifacts *(10)*
- **Must** — declared initial data is seeded in dependency order, repeatably, preserving explicit relationship identifiers *(11)*
- **Never** — initial data is supplied by Database Preferences *(11)*
- **Must** — related data operations on one Instance can share a public transaction boundary that commits or rolls back their changes together *(12)*
- **Must** — standalone writes are atomic, and Database owns commit, rollback, cleanup, and outcome reporting *(12)*
- **Never** — an operation inside a transaction commits independently, or a transaction implies atomicity across Instances or external services *(12)*
