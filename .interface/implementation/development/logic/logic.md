# Logic Definition

Logic is the Development Component that organizes application Behaviour into modular Services and publishes their Interfaces through one reusable Interface.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Logic is the independent Component that organizes the Target's application Behaviour as a reusable library of Services. Its Services implement the Behaviour; Logic's root Interface only publishes their Interfaces. It is the hub of the Implementation: Model, Database, and every consumer — the API today, a command-line entry point or another Component tomorrow — meet through those Services. A consumer states what it wants done; the owning Service decides what to read from Model, what to ask of Database or another Component, what to compute, and what to answer.

Logic owns application Behaviour and the rules that depend on an operation and its application context. It does not own domain meaning, persistence, transport, presentation, or process operation. Whoever wants to enter or change data for a Model asks Logic to do it; Model and Database are never alternate doors for that request.

### Purpose

Every application has reasoning that belongs to no single Domain Definition and to no single stored record: what may be done, in what order, under which conditions, and what the answer is when it cannot be done. That reasoning has to live somewhere. Without a Component that owns it, it settles wherever it was first needed — a rule inside an API handler, a second copy inside a background script, a third inside a screen — and the three drift until the same request gives three different answers depending on which door it came through.

Logic exists so that there is one door. A consumer that wants something done says so and receives an outcome; it does not learn which Components were involved, in what order, or how their answers were combined. That is what makes a second consumer cheap: a command-line entry point, a scheduled job, or another Component arrives without reimplementing anything, because the reasoning was never inside the first consumer to begin with. It is also what makes the Components behind Logic replaceable: when the only route to stored data runs through here, Database can change everything behind its own boundary without Behaviour noticing.

The cost of the alternative is not untidiness, it is disagreement. Behaviour spread across consumers cannot be verified in one place, cannot be changed in one place, and cannot be trusted to mean the same thing twice.

### How It Works

A consumer names an Operation on Logic's Interface and gives it what that Operation needs. Logic works out what the request means: which Domain Definitions it concerns, which Components hold the answer, and in what order they have to be asked.

It then carries the work out through its Services. Every Service keeps all of its files, including its own Interface, in its own directory. Entity Service and Database Service are the two fixed Services every Logic publishes; additional Services may be configured when the application needs them. Logic's Interface publishes each Service Interface under that Service's name and does nothing else: it neither redefines nor wraps any Service Action.

What comes back is an Application Outcome: the result the consumer asked for, or one of the expected failures that Operation declares. The consumer learns nothing else — not which Components were involved, not which Service performed which step, not how the answers were combined. That is the whole exchange, and it is the same exchange whether the consumer is an API process, a command-line entry point, or another Component.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Behaviour** — what the application does when a consumer asks for something: the validation, the ordering, and the rules that hold for an operation in its application context rather than for one record on its own.
- **Interface** — the root Logic boundary that publishes each configured Service Interface under its Service name without implementing Behaviour or Actions.
- **Operation** — one complete unit of work the Interface offers a consumer, named by what the consumer wants done rather than by how it is carried out.
- **Service** — one modular part of Logic that owns one coherent application responsibility. Its Interface is public through Logic Interface while its implementation remains internal.
- **Service Interface** — the outward gateway inside one Service's directory. It declares and publishes that Service's usable classes and Actions, and Logic Interface exposes it unchanged under the Service name.
- **Service Action** — one function a Service class handles through its Service Interface.
- **Entity Service** — one of Logic's two fixed Services, defined independently in [Entity Service Definition](services/entity/entity.md) and published through its Service Interface.
- **Database Service** — one of Logic's two fixed Services, defined independently in [Database Service Definition](services/database/database.md) and published through its Service Interface.
- **Application Outcome** — a logical success or expected failure independent of transport and persistence.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Logic
├── interface
├── core/
├── services/
│   └── <service>/
├── config.yaml
└── README.md
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — imports the authoritative Entities published through Model's Interface.
- **Consumes Database** — reaches persisted data and its transaction boundary through Database's Interface.
- **Consumes Development** — takes from it what Logic does not choose for itself: its identity, its technology, and the Connections it is permitted to make.
- **Consumes Platform** — receives the runtime values its configuration contract requires.
- **Consumed by API** — provides the Interface through which API carries out the Operations Logic offers.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **A constraint determinable from one Domain Definition's own data** — is declared by Model; Logic applies it when an Operation requires it.
- **A guarantee that requires comparing stored records** — belongs to Database, because only the Component that holds every record can enforce it; Logic would have to read the whole set to imitate it, and would still race with the next writer.
- **The shape of a request or a response on the wire, its status codes and its serialization** — belongs to the consumer that carries it, because it is a property of the transport rather than of the Behaviour underneath.
- **Selecting, provisioning, or operating an external service** — is selected for Logic by Target or Logic Preferences, with Development Defaults when needed; Platform operates it.
- **Where a value comes from at runtime** — belongs to Platform, because Logic owns the contract that says which values it needs and never the delivery of them.
- **The physical layout of stored data — tables, indexes, migrations, mappings** — belongs to Database, because it is how meaning is stored rather than what the meaning is.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Logic owns application Behaviour through its modular Services and their composition. Logic Preferences select Component-specific technical choices, Development supplies shared Defaults, and Platform supplies runtime values; transport and persistence remain behind their own Component boundaries.

### Interface

Logic's outward surface. It publishes one unchanged reference to every configured Service Interface under that Service's name. It contains no Action implementation, wrapper, Category, dependency construction, or duplicated symbol from Model, Database, Core, or a Service. A consumer selects the Service Interface and uses the classes and Actions that Interface publishes.

### Core

Logic's shared internal layer. It contains every general file and capability used across Services but owned by no single Service. Core remains private and defines no consumer-facing Action.

### Services

Logic's responsibility layer. Every Service owns one directory containing all of its files, including its Service Interface and implementation files. A Service Interface presents the capabilities that Service publishes. Logic's root Interface publishes that Service Interface, never the Service implementation or its private files. The directory and file names shown in Architecture are defaults selected by Logic Preferences and may be changed there without changing these responsibilities.

Every Logic carries these fixed public Service Interfaces:

- **[Entity Service](services/entity/entity.md)** — the fixed Service for Behaviour concerning Model Entities. Its configurable realization is in [Entity Service Preferences](services/entity/entity.yaml).
- **[Database Service](services/database/database.md)** — the fixed Service for Database capabilities that concern no single Entity. Its configurable realization is in [Database Service Preferences](services/database/database.yaml).

An additional Service follows the same modular rule: it receives its own directory, Interface, Definition, and Preferences, and Logic references it rather than copying its contract here.

### Configuration

`config.yaml` contains Logic's runtime configuration values and Service configuration. Logic reads it through private Core capability; neither consumers nor Service implementations redefine its structure.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Logic Definition Principles are mandatory. Logic Preferences provide configurable defaults and conventions for unstated Logic choices, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the Architecture or Layering category that owns it.

### General

#### Logic is a reusable library

**Rule:** Logic owns application Behaviour and exposes it through its Interface. It does not start a process, own transport schemas, or depend on a consumer's framework.
**Why:** Behaviour that carries no transport of its own can be reused by any consumer, tested without a running server, and kept while the consumer changes — the API today, a command-line entry point or another Component tomorrow.
**Boundary:** Being a library does not make Logic's internal parts public; consumers use the Interface alone. Choosing the language, packages, and framework that realize the library belongs to Development.

<br>

#### Logic owns Behaviour

**Rule:** Logic's Services apply Model-declared constraints when an Operation requires them, apply operation and application-context rules, including applicable authorization and Target-defined quotas, and return Application Outcomes. The root Logic Interface only publishes Service Interfaces and implements none of this Behaviour. Behaviour remains independent of transport and storage.
**Why:** One owner for Behaviour keeps the same rule from being written differently in the API, the Database, and the Presentation.
**Boundary:** Model declares constraints determinable from a single Domain Definition's own data; Database owns storage guarantees. Logic applies Model-declared constraints when an Operation requires them without redefining them, and does not restate Database guarantees.

<br>

### Interface

#### Logic Interface publishes Service Interfaces only

**Rule:** Logic publishes exactly one root Interface, and every consumer reaches Logic through it. The root Interface publishes each configured Service Interface unchanged under its Service name. It defines no Action, wrapper, Category, Behaviour, dependency construction, result transformation, or duplicate export from Model, Database, Core, or a Service. Every Action remains defined and implemented by the Service that owns it and is published through that Service's Interface.
**Why:** One directory of Service gateways lets consumers discover Logic without creating a second implementation of the Services' contracts.
**Boundary:** Logic Interface may name and publish a Service Interface but does not publish the Service implementation. Logic Preferences declare which Services exist; adding or removing a configured Service changes only the set of Service Interfaces the root publishes.

<br>

### Services

#### Logic is composed of modular Services

**Rule:** Inside Logic, work is divided into Services. Each Service owns one coherent application responsibility, keeps all of its files in its own directory, and presents its usable capabilities through its Service Interface. Logic Interface publishes that Service Interface unchanged. Entity Service and Database Service are fixed Services of every Logic; their Interfaces are always published. The Service implementation remains internal.
**Why:** Giving each application responsibility one Service keeps its dependencies and behavior together, so a Service can change without that change spreading through unrelated Behaviour.
**Boundary:** Services sit beside one another, not on top of one another: none is the foundation of another. A Service may use another Service only through that Service's Interface when its Behaviour requires that collaboration. Additional Services may be configured, but they never replace either fixed Service. Each Service's own Definition and Preferences govern its internal contract and realization.

<br>

#### Logic reaches another Component only through that Component's Interface

**Rule:** Every route out of Logic runs through the Interface of the Component on the other side, and through the capabilities that Interface offers. The Service that owns a dependency makes those calls; Logic reaches no Component by another route and holds no part of one that its Interface does not publish.
**Why:** A Component that is only ever reached through its own published surface can change everything behind it without reaching Behaviour, and every dependency Logic has is then visible as a call it is allowed to make.
**Boundary:** The Component on the other side owns what happens inside its own boundary. Logic neither assumes nor restates a capability that Component's Interface does not publish.

<br>

#### Domain meaning is imported, never restated

**Rule:** Logic imports authoritative Domain Definitions through Model's Interface and uses them as Model declares them. It never copies, mirrors, or redefines a Domain Definition, and never re-derives meaning Model already publishes.
**Why:** One definition shared by every Component is what keeps the domain from drifting into several versions of itself.
**Boundary:** Logic may hold a shape of its own for an input or an outcome that has no Domain Definition; it never mirrors one that does.

<br>

#### External dependencies remain explicit

**Rule:** Logic consumes only the external services and cross-cutting capabilities selected by Target or Logic Preferences, using Development Defaults only when needed, through explicit interfaces and only where Behaviour requires them. An external service is reached through the Service that owns that dependency, never from scattered points inside Logic.
**Why:** An implicit dependency on something outside Logic is invisible until it fails or has to be replaced.
**Boundary:** Logic Preferences select a Logic-specific external service; Logic does not provision or operate it, and Platform operates it. An external service consumed this way is not a Logic Service — Logic Services are internal parts of this Component.

<br>

#### Logic execution remains bounded

**Rule:** Logic uses finite timeouts. It retries only boundedly and only an operation that is safe or idempotent to repeat; it never retries without a limit.
**Why:** An unbounded wait or retry can turn one unavailable dependency into work that never ends or a repeated change whose result cannot be trusted.
**Boundary:** This Principle governs Logic's use of a dependency. It does not transfer retry, transaction, or recovery ownership from the Component whose Interface Logic calls.

<br>

### Configuration

#### Runtime configuration stays private

**Rule:** Logic defines the configuration contract required by its Behaviour and validates required values before use. Runtime values are supplied to Logic by its environment; secrets never enter source, errors, public interfaces, logs, or Application Outcomes.
**Why:** A contract validated before readiness fails at start with a clear cause rather than mid-operation with an unclear one.
**Boundary:** Logic owns the contract and its validation, never the values, their delivery, or the environment they come from.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Logic is a reusable library**

- **Must** — Expose application Behaviour through one public Logic Interface.
- **Never** — Start a process, own a transport schema, or depend on an API framework inside Logic.

**Logic owns Behaviour**

- **Must** — Apply Model-declared constraints when an Operation requires them, apply operation and application-context rules, and return Application Outcomes.
- **Never** — Let Behaviour depend on transport or storage, redefine a Model-declared constraint, or restate a Database guarantee.

### Interface

**Logic Interface publishes Service Interfaces only**

- **Must** — publish exactly one root Interface and expose every configured Service Interface unchanged under its Service name.
- **Must** — keep every Action defined and implemented by its owning Service and published through that Service's Interface.
- **Never** — define an Action, wrapper, Category, Behaviour, dependency construction, result transformation, or duplicate dependency symbol in Logic Interface.
- **Never** — expose a Service implementation, connection, session, or storage detail through Logic Interface.

### Services

**Logic is composed of modular Services**

- **Must** — Divide Logic into modular Services, each owning one coherent application responsibility and one directory containing all of its files.
- **Must** — give every Service an outward Service Interface that presents its usable capabilities and is published unchanged by Logic Interface.
- **Must** — include and publish Entity Service and Database Service in every Logic.
- **Never** — let a consumer reach or depend on a Service implementation, or let a Service do its work through another Component's Service.

**Logic reaches another Component only through that Component's Interface**

- **Must** — Reach every other Component only through that Component's Interface and its Operations, from the Service that owns the dependency.
- **Never** — Reach a Component by another route or hold or assume a capability its Interface does not publish.

**Domain meaning is imported, never restated**

- **Must** — Import authoritative Domain Definitions through Model's Interface and use them as Model declares them.
- **Never** — Copy or redefine a Domain Definition inside Logic.

**External dependencies remain explicit**

- **Must** — Consume an external service or cross-cutting capability only when Target or Logic Preferences selected it and Behaviour requires it, through the Service that owns that dependency.
- **Never** — Provision or operate an external service from Logic.

**Logic execution remains bounded**

- **Must** — Use finite timeouts and bounded retries only for safe or idempotent operations.
- **Never** — Retry without a limit.

### Configuration

**Runtime configuration stays private**

- **Must** — Define Logic's configuration contract and validate every required value before use.
- **Never** — Put a secret in source, an error, a public interface, a log, or an Application Outcome, or take ownership of runtime values.
