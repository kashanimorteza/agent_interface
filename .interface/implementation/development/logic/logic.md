# Logic Definition

Logic is the Development Component that owns application Behaviour and exposes it through one reusable Interface.

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

Logic is the independent Logic Component that implements the Target's application Behaviour as a reusable library. It is the hub of the Implementation: Model, Database, and every consumer — the API today, a command-line entry point or another Component tomorrow — meet through it. A consumer states what it wants done; Logic decides what to read from Model, what to ask of Database or another Component, what to compute, and what to answer.

Logic owns application Behaviour and the rules that depend on an operation and its application context. It does not own domain meaning, persistence, transport, presentation, or process operation. Whoever wants to enter or change data for a Model asks Logic to do it; Model and Database are never alternate doors for that request.

### Purpose

Every application has reasoning that belongs to no single Domain Definition and to no single stored record: what may be done, in what order, under which conditions, and what the answer is when it cannot be done. That reasoning has to live somewhere. Without a Component that owns it, it settles wherever it was first needed — a rule inside an API handler, a second copy inside a background script, a third inside a screen — and the three drift until the same request gives three different answers depending on which door it came through.

Logic exists so that there is one door. A consumer that wants something done says so and receives an outcome; it does not learn which Components were involved, in what order, or how their answers were combined. That is what makes a second consumer cheap: a command-line entry point, a scheduled job, or another Component arrives without reimplementing anything, because the reasoning was never inside the first consumer to begin with. It is also what makes the Components behind Logic replaceable: when the only route to stored data runs through here, Database can change everything behind its own boundary without Behaviour noticing.

The cost of the alternative is not untidiness, it is disagreement. Behaviour spread across consumers cannot be verified in one place, cannot be changed in one place, and cannot be trusted to mean the same thing twice.

### How It Works

A consumer names an Operation on Logic's Interface and gives it what that Operation needs. Logic works out what the request means: which Domain Definitions it concerns, which Components hold the answer, and in what order they have to be asked.

It then carries the work out through its Services. Each Service holds the calls into one Component's Interface, so a Service's Action is one call outwards — the Database Service's `add` is a call into Database's Interface, and a Service for another Component is the same thing pointed elsewhere. An Operation that needs one Component uses one Service; an Operation that needs several composes their Actions, deciding what to pass from one to the next and what belongs together in a single unit of work.

What comes back is an Application Outcome: the result the consumer asked for, or one of the expected failures that Operation declares. The consumer learns nothing else — not which Components were involved, not which Service performed which step, not how the answers were combined. That is the whole exchange, and it is the same exchange whether the consumer is an API process, a command-line entry point, or another Component.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Behaviour** — what the application does when a consumer asks for something: the validation, the ordering, and the rules that hold for an operation in its application context rather than for one record on its own.
- **Interface** — the only Logic boundary a consumer sees, exposing the Operations Logic performs.
- **Category** — one named grouping of Operations in the Interface, gathering the Operations that serve the same kind of work.
- **Operation** — one complete unit of work the Interface offers a consumer, named by what the consumer wants done rather than by how it is carried out.
- **Service** — one internal part of Logic, owning the work that concerns one Component Logic talks to. A Service is internal: no consumer reaches it, names it, or depends on it.
- **Action** — one step a Service performs, carried out by calling an Operation of that Component's own Interface. Operations are composed of Actions; an Action is never offered directly to a consumer.
- **Application Outcome** — a logical success or expected failure independent of transport and persistence.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Logic
├── Interface
│   └── Category
│       └── Operation
└── Services
    └── Service
        └── Action
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — imports authoritative Domain Definitions and their declaration vocabulary through Model's Interface.
- **Consumes Database** — reaches persisted data and its transaction boundary through Database's Interface.
- **Consumes Development** — takes from it what Logic does not choose for itself: its identity, its technology, and the Connections it is permitted to make.
- **Consumes Platform** — receives the runtime values its configuration contract requires.
- **Consumed by API** — provides the Interface through which API carries out the Operations Logic offers.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **A rule determinable from one Domain Definition's own data** — belongs to Model, because it holds wherever that definition is used, with no operation and no application context to qualify it.
- **A guarantee that requires comparing stored records** — belongs to Database, because only the Component that holds every record can enforce it; Logic would have to read the whole set to imitate it, and would still race with the next writer.
- **The shape of a request or a response on the wire, its status codes and its serialization** — belongs to the consumer that carries it, because it is a property of the transport rather than of the Behaviour underneath.
- **Selecting, provisioning, or operating an external service** — belongs to Development and Platform, because choosing a dependency and running it are decisions about the project and its environment, not about what the application does.
- **Where a value comes from at runtime** — belongs to Platform, because Logic owns the contract that says which values it needs and never the delivery of them.
- **The physical layout of stored data — tables, indexes, migrations, mappings** — belongs to Database, because it is how meaning is stored rather than what the meaning is.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Logic owns application Behaviour, operation composition, and its internal Services. Development supplies the Component's technical selections and Platform supplies runtime values; transport and persistence remain behind their own Component boundaries.

### Interface

Logic's outward surface. It organizes what Logic offers into Categories, each gathering Operations that serve one kind of work. Each Operation is stated in the consumer's terms. Interface names no Service and exposes no Action.

### Services

Logic's internal layer. Each Service owns the work concerning one Component Logic talks to and carries that Component's name. Each Action calls an Operation of that Component's Interface. An Operation composes Actions from one Service or several; Services are parallel and not reachable, nameable, or dependable from outside.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Logic Definition Principles are mandatory. Logic Preferences provide configurable defaults and conventions for unstated Logic choices, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Logic documentation exposes the Interface only

**Rule:** Logic documentation is written for a consumer who will never see inside it. It covers every Category and Operation in the Interface, what each accepts and returns, the Application Outcomes it can produce, and how a consumer imports and calls it. Services and Actions remain internal and are not documented as consumer dependencies.

**Why:** A reader must be able to carry out every Operation Logic offers without knowing which Component the work reached or which Service performed it.

**Boundary:** This Principle governs consumer-facing Logic documentation; it does not publish Services, Actions, or internal implementation details.

<br>

### Logic is a reusable library

**Rule:** Logic owns application Behaviour and exposes it through its Interface. It does not start a process, own transport schemas, or depend on a consumer's framework.

**Why:** Behaviour that carries no transport of its own can be reused by any consumer, tested without a running server, and kept while the consumer changes — the API today, a command-line entry point or another Component tomorrow.

**Boundary:** Being a library does not make Logic's internal parts public; consumers use the Interface alone. Choosing the language, packages, and framework that realize the library belongs to Development.

<br>

### Logic owns Behaviour

**Rule:** Logic validates domain state, applies operation and application-context rules, including applicable authorization and Target-defined quotas, and returns Application Outcomes. Behaviour remains independent of transport and storage.

**Why:** One owner for Behaviour keeps the same rule from being written differently in the API, the Database, and the Presentation.

**Boundary:** A rule determinable from a single Domain Definition's own data is an Intrinsic Rule owned by Model; a storage guarantee is owned by Database. Logic does not restate either.

<br>

### One Interface exposes Logic's Operations

**Rule:** Logic publishes exactly one Interface, and every consumer reaches Logic only through it. That Interface organizes what it offers into Categories, each gathering the Operations that serve one kind of work, and offers Operations: each one a complete unit of work stated in the consumer's terms — what it wants done and with what — never a route into Logic's internal parts. An Operation states what it accepts, what it returns, and which Application Outcomes it can produce.

**Why:** One boundary lets Logic reorganize inside itself without any consumer noticing, and lets a second consumer arrive without a second way in.

**Boundary:** Interface names no Service, and exposes no Action, connection, session, or storage detail. A Category groups Operations and performs no work of its own. Logic Preferences declare which Operations each Service provides; Interface presents those Operations to consumers.

<br>

### Logic is composed of internal Services, one per Component it talks to

**Rule:** Inside Logic, work is divided into Services. Each Service owns the work that concerns one Component Logic talks to and is named after it, so the Component a piece of Behaviour depends on is visible from its Service. A Service performs Actions; an Operation is carried out by composing Actions, from one Service or several. Services are internal: no consumer names one, reaches one, or depends on one, and no Service is promoted to Interface.

**Why:** Dividing by the Component on the other side keeps each dependency in one place, so a Component can be added, replaced, or removed without that change spreading through unrelated Behaviour.

**Boundary:** Services sit beside one another, not on top of one another: none is the foundation of another, and one Service never reaches another Component's Service to do its work — the Operation composes them. Logic Preferences declare which Services exist and which Operations each one provides.

<br>

### Logic reaches another Component only through that Component's Interface

**Rule:** Every route out of Logic runs through the Interface of the Component on the other side, and through the Operations that Interface offers. The Service that owns a dependency makes those calls; Logic reaches no Component by another route and holds no part of one that its Interface does not publish. Persistence follows the same rule: Logic reaches stored data only through Database's Interface, forwards grouped work through Database's transaction boundary, and never exposes engines, sessions, mappings, or schema details.

**Why:** A Component that is only ever reached through its own published surface can change everything behind it without reaching Behaviour, and every dependency Logic has is then visible as a call it is allowed to make.

**Boundary:** Logic decides which operations belong together in one unit of work; the Component on the other side owns what happens inside its own boundary — for Database, commit, rollback, isolation, and retry. What that Component publishes is its own decision, not Logic's.

<br>

### Domain meaning is imported, never restated

**Rule:** Logic imports authoritative Domain Definitions through Model's Interface and uses them as Model declares them. It never copies, mirrors, or redefines a Domain Definition, and never re-derives meaning Model already publishes.

**Why:** One definition shared by every Component is what keeps the domain from drifting into several versions of itself.

**Boundary:** Logic may hold a shape of its own for an input or an outcome that has no Domain Definition; it never mirrors one that does.

<br>

### External dependencies remain explicit

**Rule:** Logic consumes only the external services and cross-cutting capabilities selected by Development, through explicit interfaces and only where Behaviour requires them. An external service is reached through the Service that owns that dependency, never from scattered points inside Logic.

**Why:** An implicit dependency on something outside Logic is invisible until it fails or has to be replaced.

**Boundary:** Logic does not select, provision, or operate an external service; Development selects it and Platform operates it. An external service consumed this way is not a Logic Service — Logic Services are internal parts of this Component.

<br>

### Runtime configuration stays private

**Rule:** Logic defines the configuration contract required by its Behaviour and validates required values before use. Runtime values are supplied to Logic by its environment; secrets never enter source, errors, public interfaces, logs, or Application Outcomes.

**Why:** A contract validated before readiness fails at start with a clear cause rather than mid-operation with an unclear one.

**Boundary:** Logic owns the contract and its validation, never the values, their delivery, or the environment they come from.

<br>

### Logic execution remains bounded

**Rule:** Logic uses finite timeouts. It retries only boundedly and only an operation that is safe or idempotent to repeat; it never retries without a limit.

**Why:** An unbounded wait or retry can turn one unavailable dependency into work that never ends or a repeated change whose result cannot be trusted.

**Boundary:** This Principle governs Logic's use of a dependency. It does not transfer retry, transaction, or recovery ownership from the Component whose Interface Logic calls.

<br>

### Logic verification covers Logic boundaries

**Rule:** Verification covers isolated Logic, each Service's calls into the Interface it depends on, transaction behaviour, and every Operation the Interface offers — its inputs, its result, and each Application Outcome it declares — without requiring a live consumer process.

**Why:** Behaviour that can only be verified through a running API is verified at the wrong boundary and hides which layer actually failed.

**Boundary:** Verification here does not extend to transport, presentation, or deployment; those are verified by the Components that own them. Whether a check persists as a test in this Component follows Development's Cross-cutting Capability applicability.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Logic documentation exposes the Interface only**

- **Must** — document every Interface Category and Operation, its inputs, outputs, Application Outcomes, and consumer usage.
- **Never** — document Services or Actions as consumer dependencies.

**Logic is a reusable library**

- **Must** — Expose application Behaviour through one public Logic Interface.
- **Never** — Start a process, own a transport schema, or depend on an API framework inside Logic.

**Logic owns Behaviour**

- **Must** — Validate domain state, apply operation and application-context rules, and return Application Outcomes.
- **Never** — Let Behaviour depend on transport or storage, or restate a Model Intrinsic Rule or a Database guarantee.

**One Interface exposes Logic's Operations**

- **Must** — Publish exactly one Interface and let every consumer reach Logic only through it.
- **Must** — Organize the Interface's Operations into Categories, each gathering the Operations that serve one kind of work.
- **Must** — State for every Operation what it accepts, what it returns, and which Application Outcomes it can produce.
- **Never** — Expose a Service, an Action, a connection, a session, or a storage detail through Interface.

**Logic is composed of internal Services, one per Component it talks to**

- **Must** — Divide Logic into internal Services, each owning the work that concerns one Component Logic talks to and named after it.
- **Must** — Carry out an Operation by composing Actions from one Service or several.
- **Never** — Let a consumer name, reach, or depend on a Service, or let one Service do its work through another Component's Service.

**Logic reaches another Component only through that Component's Interface**

- **Must** — Reach every other Component only through that Component's Interface and its Operations, from the Service that owns the dependency.
- **Must** — Forward grouped persistence work through Database's transaction boundary.
- **Never** — Reach a Component by another route, hold a part of one its Interface does not publish, or expose engines, sessions, mappings, or schema details.

**Domain meaning is imported, never restated**

- **Must** — Import authoritative Domain Definitions through Model's Interface and use them as Model declares them.
- **Never** — Copy or redefine a Domain Definition inside Logic.

**External dependencies remain explicit**

- **Must** — Consume an external service or cross-cutting capability only when Development selected it and Behaviour requires it, through the Service that owns that dependency.
- **Never** — Select, provision, or operate an external service from Logic.

**Runtime configuration stays private**

- **Must** — Define Logic's configuration contract and validate every required value before use.
- **Never** — Put a secret in source, an error, a public interface, a log, or an Application Outcome, or take ownership of runtime values.

**Logic execution remains bounded**

- **Must** — Use finite timeouts and bounded retries only for safe or idempotent operations.
- **Never** — Retry without a limit.

**Logic verification covers Logic boundaries**

- **Must** — Verify isolated Logic, each Service's calls into its Component's Interface, transaction behaviour, and every Operation with its inputs, result, and declared Application Outcomes, without a live consumer process.
- **Never** — Push Logic verification into transport, presentation, or deployment, or persist a check in a Component outside the testing applicability list.
