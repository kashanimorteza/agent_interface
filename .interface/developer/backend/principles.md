# Backend Standard

> **Authoritative Standard for the Backend Component**
>
> This document is the authoritative standard for the project's Backend Component.
>
> Every implementer, reviewer, or automation that creates, changes, validates, or reasons about Backend code MUST read and follow this document before making changes.
>
> **Principles override preferences, framework defaults, convenience, and implementation choices.**
>
> A project may add stricter rules, but it must not weaken the rules defined here.

---

# 1. Purpose

Backend is an independent package that executes application Behaviour and publishes the application's API Interface. It turns shared domain meaning into what the application does, enforces rules that depend on application context, and exposes the result as the contract used by external consumers.

Backend owns:

- application Behaviour;
- the route from Behaviour to persistence; and
- the external API Interface contract.

Backend does not own domain-model meaning, physical persistence, user-interface presentation, or cross-layer composition.

---

# Project Independence

Backend is reusable across Targets. This standard defines how a Backend Component works, not which domain, Behaviour, Model set, API Interface operation, provider, or deployment topology a particular Target contains.

Its architecture is independent of language, framework, protocol, package manager, database engine, and project. Target-specific Behaviour, Model operations, integrations, and externally exposed capabilities belong to the current Target definition and MUST NOT be copied into this standard.

Technical selections populate the architecture through Backend Preferences without changing its ownership boundaries or dependency direction. Changing the Target MUST NOT require changing this standard.

---

# Architectural Foundation

Backend is an independent package with Logic at its center and three boundary layers around it:

1. Model Interface is Logic's only route to the shared Model package.
2. Database Interface is Logic's only route to the public Database interface.
3. Logic implements application Behaviour and Model-specific logic.
4. API Interface is the external boundary through which consumers reach Logic.

```text
Model package ── Model Interface ──┐
                                   ├── Logic ── API Interface ── External consumers
Database ─────── Database Interface┘
```

The architecture separates domain access, persistence access, Behaviour, and external communication so each boundary can change without redefining the others.

---

# Authority by Concern

| Concern | Authoritative source |
| --- | --- |
| Domain Models, fields, relationships, credential markers, and rules determined from Model data | Model Standard and current Target Model definition |
| Target-specific application Behaviour and externally required capabilities | Current Target definition |
| Backend layers, interface boundaries, Behaviour ownership, dependency direction, and transaction coordination | This Backend Standard |
| Language, environment, API framework, standard operations, and technical defaults | Backend Preferences |
| Persistence operations, transaction mechanism, constraints over stored state, and credential storage mode | Database Standard and Database public interface |
| Package conventions, cross-cutting capabilities, and supporting-service scope | Development Standard and Development Preferences |
| Runtime Bindings delivered to Backend | Platform and the selected Launch definition |

Backend MUST apply each source only within its authority. It MUST NOT invent domain meaning, persistence semantics, or cross-layer ownership because a framework makes doing so convenient.

---

# 2. Core Principles

## 2.1 Terms

- **Model Interface** — the layer through which Logic consumes shared logical Model definitions and validation.
- **Database Interface** — the layer through which Logic consumes the public Database interface.
- **Logic** — the layer that implements application Behaviour and Model-specific logic.
- **API Interface** — the layer through which external consumers invoke Logic and receive results.
- **Model Logic** — the logical unit inside Logic that belongs to one shared Model and carries its operations and Behaviour.
- **Behaviour** — what the application does and the rules under which it does it, independent of how it is requested or stored.
- **Credential** — a Model field marked as secret, accepted as input but never returned across the API Interface boundary.

## 2.2 Relationships

- **Consumes Model** — the shared logical Model definitions reached only through Model Interface.
- **Consumes Database** — the generic data-access interface reached only through Database Interface.
- **Consumes Development** — the common package standard, ownership rules for Backend settings and private secrets, and the cross-cutting capabilities selected for the Target.
- **Consumes Platform** — the Bindings the selected Launch delivers to Backend's boundary.
- **Consumed by Frontend** — the public API Interface through which the user interface reaches application data and capabilities.

Technical choices and defaults belong to Backend Preferences. Backend implementation applies those choices to the current Target definition.

## 2.3 Backend has Logic and three boundary interfaces

**Rule:** Backend is implemented as one independent package with its own identity, configuration, documented public boundary, and four internal layers: Model Interface, Database Interface, Logic, and API Interface. Logic owns Behaviour. It consumes Model only through Model Interface, consumes Database only through Database Interface, and is reached by external consumers only through API Interface.

**Why:** Separating all three integration boundaries from Behaviour lets Model, Database, API technology, and Logic evolve without collapsing their responsibilities into one layer.

**Boundary:** No Backend layer bypasses Model Interface, Database Interface, Logic, or API Interface for a responsibility owned by that layer. Package identity and code path are resolved through Backend Preferences; they never change the four-layer architecture or expose an internal layer as an independent competing Backend.

<br>

## 2.4 Logic owns application Behaviour

**Rule:** Logic implements what the application does and the rules under which it does it. It enforces conditions that depend on the operation or application context and uses Model Interface for shared Model definitions and validation. For partial changes, Logic ensures validation considers the resulting domain state, including existing values needed to evaluate applicable rules. Logic communicates with persistence only through Database Interface and with external consumers only through API Interface. Database remains responsible for guaranteeing constraints that depend on stored state.

Logic determines which related data operations must succeed as one unit and requests that unit through Database Interface. It does not implement the underlying transaction mechanism or treat changes to external services as part of a Database transaction.

**Why:** Behaviour expressed without transport or storage detail remains valid when the API technology or Database implementation changes.

**Boundary:** Logic is independent of HTTP, API frameworks, database engines, ORM implementations, physical storage, and transport-specific request or response shapes. It never imports around Model Interface or Database Interface.

<br>

## 2.5 Every Model has a standard Logic surface

**Rule:** Every shared Model receives its own logical unit inside Logic, defined separately from the unit of every other Model. That unit provides a consistent baseline for common Model operations such as create, get, list, update, and delete. Common operations may be implemented in a shared base or helper and reused through inheritance or composition.

Model-specific Behaviour may extend this baseline: one Model may perform validation, calculations, coordination, or other actions that another Model does not. An API Interface request for a Model is handled by the corresponding Model Logic, which may use Model Interface and Database Interface and perform other Behaviour required by that Model.

The operations selected in Backend Preferences are offered only where the shared Model supports them. When status is selected, it is available only for a Model declaring the corresponding field, and its actions follow the public Database interface. A status request passes through the corresponding Model Logic and Database Interface; it never creates a missing field or bypasses Model-specific Behaviour.

**Why:** Each Model retains its own unit even when it currently uses only the common baseline, so its operations and Behaviour can later be extended independently without changing another Model's Logic.

**Boundary:** A definition shared by several Models does not satisfy this separation. A shared registry may import and connect the units without defining them itself. Model-specific additions remain inside that Model's Logic and never weaken the common interface expected across Models. API Interface never substitutes direct persistence for Model Logic.

<br>

## 2.6 Database Interface is the only Backend route to Database

**Rule:** Database Interface translates data operations requested by Logic into calls to the generic interface published by Database, then translates the results back into logical data.

When Logic requests a group of related operations, Database Interface connects that group to the public Database transaction boundary on one resolved Instance. Every participating operation uses the same boundary, and Database Interface propagates its outcome without committing individual operations independently. Database retains ownership of commit, rollback, and connection cleanup.

**Why:** One translation point means the Database implementation can change without Logic being rewritten, and every persistence call remains visible in one place.

**Boundary:** Database Interface contains no application Behaviour and does not decide which operations belong together. It never owns or directly reaches into the database engine, connection, ORM, tables, schema, or migrations. Transaction access exposes none of those internals to Logic or API Interface and implies no atomicity across Instances or external services. API Interface and Logic never bypass Database Interface to access Database.

<br>

## 2.7 API Interface is Logic's external boundary

**Rule:** API Interface receives external requests, validates their transport-level shape, invokes Logic, and converts Logic results into external responses. API Interface owns only communication concerns such as request decoding, transport-level validation, response serialization, protocol handling, and mapping logical outcomes to API responses.

**Why:** Keeping the boundary thin means application Behaviour can be reached through any transport, and a protocol change never becomes a Behaviour change.

**Boundary:** API Interface does not implement application Behaviour and never calls Model Interface, Database Interface, Model, or Database directly. Model owns validation determined from its own data; Logic owns application-context checks and uses Model Interface to coordinate domain validation required by the operation. API Interface neither duplicates those rules nor treats transport validation as proof that the resulting domain state is valid. Its framework, version, protocol, and other technical settings are resolved from the Target definition and Backend Preferences.

<br>

## 2.8 Model Interface is the only Backend route to Model

**Rule:** Model Interface imports and exposes the shared logical Model definitions required by Logic under Model Principles and Preferences. Logic uses Model meaning, types, and domain validation only through this boundary. Database Interface receives the Model identities and values needed for public Database operations from Logic, and API Interface derives external data shapes from Logic's contract without creating a second domain definition.

**Why:** One shared definition keeps the meaning of a Model identical on both sides of the Backend boundary.

**Boundary:** No other Backend layer imports around Model Interface or copies, redefines, or creates a competing representation of Model meaning. Model Interface contains no application Behaviour, persistence behavior, transport behavior, or private Model implementation. HTTP-specific and storage-specific details remain outside Model.

<br>

## 2.9 API Interface serves Model operations and Target Behaviour

**Rule:** Backend is not limited to Model CRUD. Logic implements Backend-targeted Behaviour from the current Target, and API Interface exposes the Behaviour that must be available to external consumers. Model-level API intent and externally exposed Behaviour are resolved from the Target definition under Backend Principles and Preferences.

**Why:** A Target's value usually lies in what it does beyond storing records, so the API Interface surface follows stated Behaviour rather than only the Model list.

**Boundary:** Resolution of Behaviour does not itself fix endpoint paths, HTTP method mappings, file layout, or framework implementation details. Those details are implementation output governed by the applicable sources.

<br>

## 2.10 API Interface documentation belongs to API Interface

**Rule:** The capability to publish a machine-readable API description of available operations and data shapes belongs to the API Interface layer.

**Why:** The layer that defines the external contract is the only layer that can describe it accurately as it changes.

**Boundary:** No other Backend layer owns or generates the public API description. Whether API documentation is enabled, its format, and the tool that produces it are technical choices resolved through Backend Preferences.

<br>

## 2.11 Credentials are write-only at the API Interface boundary

**Rule:** A Model field marked as a Credential is write-only API Interface input. It may be accepted when required to create or update its owning Model. Its input definition—including its name, type, requiredness, and write-only nature—may appear in input schemas and API Interface documentation so a consumer knows how to supply it. The field is excluded from API Interface responses and response schemas.

Actual credential values are never exposed in documentation, examples, error payloads, diagnostics, traces, or recorded outputs. Examples use non-secret placeholders only.

**Why:** A credential that leaves the boundary even once is compromised, and its most likely leak points are easy to overlook.

**Boundary:** Backend reads the Credential marker from the shared Model definition and never guesses Credential fields from their names. Database owns the Credential's at-rest storage mode; Backend does not redefine it.

<br>

## 2.12 Logic may orchestrate resolved supporting services

**Rule:** Model Logic may use Database Interface and may coordinate supporting services or cross-cutting capabilities selected by Development. Such services are consumed through explicit interfaces and used only by the Model Logic that needs them.

**Why:** Capabilities chosen for the whole Target must be usable inside Behaviour without forcing every Model to depend on them.

**Boundary:** A supporting service does not become a fifth mandatory Backend layer and does not bypass Model Interface, Database Interface, or API Interface. Its availability and application scope are resolved outside Backend rather than hard-coded into Model Logic.

---

# 3. Documentation Standard

The Backend package MUST include a public `DOCUMENTATION.md` at its package boundary, as required by the Development Standard.

The `DOCUMENTATION.md` MUST explain:

- Backend's purpose and its Model Interface, Database Interface, Logic, and API Interface boundaries;
- the public API Interface and how external consumers use it;
- how Model Logic and Target Behaviour are organized;
- how Logic reaches Model through Model Interface and Database through Database Interface;
- non-secret configuration and required runtime Bindings;
- installation and startup when applicable; and
- practical usage and failure-handling examples.

The API Interface layer owns any machine-readable API description. When enabled through Backend Preferences, that description MUST remain consistent with the implemented external contract and MUST preserve Credential fields as write-only input excluded from responses and response schemas.

Documentation and examples MUST NOT expose actual credentials, private configuration, Database internals, or implementation details as public contracts. The package documentation and machine-readable API description MUST be verified for consistency before Backend is reported complete.

---

# 4. Decision Order

When multiple Backend implementations are possible, prefer in this order:

1. Preserve Model meaning and Target Behaviour.
2. Preserve Logic as the Behaviour owner and preserve all three interface boundaries.
3. Keep Behaviour independent of transport and persistence implementation.
4. Route all persistence through the public Database interface.
5. Preserve complete validation of the resulting domain state.
6. Preserve transaction boundaries selected by Logic and implemented by Database.
7. Protect Credentials across every output and diagnostic surface.
8. Apply compatible choices selected by Backend Preferences.
9. Prefer the simplest maintainable implementation.

---

# 5. At a Glance

## MUST

- Implement Backend as one independent package formed from Model Interface, Database Interface, Logic, and API Interface.
- Let Logic implement application Behaviour, enforce operation-dependent conditions, use Model Interface for shared validation, and validate partial changes against the resulting domain state.
- Leave constraints dependent on stored state to Database.
- Let Logic determine related operations that form one unit and request that unit through Database Interface.
- Give every shared Model its own separately defined Logic unit with the supported common-operation baseline.
- Offer selected operations only where the Model supports them; route status through Model Logic and Database Interface only for Models declaring the field.
- Translate Logic's persistence requests through Database Interface into calls on the generic Database interface.
- Carry a Logic-defined operation group through one Instance's public transaction boundary and propagate its outcome while Database owns commit, rollback, and cleanup.
- Let API Interface decode requests, validate transport shape, invoke Logic, serialize results, and expose required Target Behaviour.
- Route all Backend use of shared Model definitions through Model Interface without copying domain meaning.
- Let API Interface own and produce the machine-readable description of its contract.
- Accept Credential fields as input only, preserve their write-only definition, and derive their marker from Model.
- Consume supporting services through explicit interfaces only in the Model Logic that needs them.
- Provide and verify Backend `DOCUMENTATION.md` and, when enabled, consistent machine-readable API Interface documentation.

## SHOULD

- Keep API Interface thin and Logic independent of transport and storage technologies.
- Reuse a common Logic operation baseline through inheritance or composition while keeping one distinct unit per Model.
- Keep persistence translation visible in one Database Interface boundary.
- Use non-secret placeholders in Credential examples.
- Prefer explicit supporting-service interfaces and the smallest necessary application scope.

## NEVER

- Let a layer bypass the layer responsible for the next boundary.
- Let Logic implement Database transaction mechanisms, assume transactions cover external services, or depend on HTTP, API frameworks, database engines, ORM implementations, or physical storage.
- Let a status operation invent a missing field or bypass Model-specific Behaviour.
- Let one shared definition replace the separate Logic units of several Models, or let API Interface substitute direct persistence for Model Logic.
- Let Database Interface independently commit grouped operations, decide application grouping, promise atomicity across Instances or external services, contain Behaviour, or reach into engine, connection, ORM, tables, schema, or migrations.
- Let API Interface duplicate Model validation, treat transport validation as proof of valid domain state, implement Behaviour, or call Database Interface or Database directly.
- Copy, redefine, or create a competing representation of Model meaning.
- Treat resolution of Behaviour as a fixed endpoint path, HTTP method, file layout, or framework detail.
- Let another Backend layer own or generate the public API description.
- Return a Credential field or include it in a response schema; expose an actual value in documentation, examples, errors, diagnostics, traces, or recorded output; guess Credential fields by name; or redefine their at-rest storage mode.
- Let a supporting service become a fifth mandatory Backend layer or bypass one of Logic's three interfaces.

---

# 6. Final Rule

Backend defines **what the application does and how that Behaviour reaches external consumers without coupling it to transport or persistence internals**.

When a Backend decision is not explicitly covered, preserve Model meaning and Target Behaviour, keep Logic responsible for Behaviour, route Model access through Model Interface, persistence through Database Interface, and external communication through API Interface, protect Credentials, and apply Backend Preferences without weakening the four-layer architecture.

When convenience conflicts with these Backend Principles, **the Backend Principles win**.
