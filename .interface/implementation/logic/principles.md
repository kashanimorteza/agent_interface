# Logic Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Understanding](#understanding)**
   - **[Logic](#logic)**
3. **[Terms](#terms)**
4. **[Architecture](#architecture)**
5. **[Relationships](#relationships)**
6. **[Boundaries](#boundaries)**
7. **[Documentation](#documentation)**
8. **[Principles](#principles)**
   - **[Logic is a reusable library](#logic-is-a-reusable-library)**
   - **[Logic owns Behaviour](#logic-owns-behaviour)**
   - **[One Public Interface exposes Logic's Operations](#one-public-interface-exposes-logics-operations)**
   - **[Logic is composed of internal Services, one per Component it talks to](#logic-is-composed-of-internal-services-one-per-component-it-talks-to)**
   - **[Logic reaches another Component only through that Component's Public Interface](#logic-reaches-another-component-only-through-that-components-public-interface)**
   - **[Domain meaning is imported, never restated](#domain-meaning-is-imported-never-restated)**
   - **[External dependencies remain explicit](#external-dependencies-remain-explicit)**
   - **[Runtime configuration stays private](#runtime-configuration-stays-private)**
   - **[Logic verification covers Logic boundaries](#logic-verification-covers-logic-boundaries)**
9. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Logic is the independent Logic Component that implements the Target's application Behaviour as a reusable library. It is the hub of the Implementation: Model, Database, and every consumer — the API today, a command-line entry point or another Component tomorrow — meet through it. A consumer states what it wants done; Logic decides what to read from Model, what to ask of Database or another Component, what to compute, and what to answer.

Logic owns application Behaviour and the rules that depend on an operation and its application context. It does not own domain meaning, persistence, transport, presentation, or process operation.

### Purpose

Every application has reasoning that belongs to no single Domain Definition and to no single stored record: what may be done, in what order, under which conditions, and what the answer is when it cannot be done. That reasoning has to live somewhere. Without a Component that owns it, it settles wherever it was first needed — a rule inside an API handler, a second copy inside a background script, a third inside a screen — and the three drift until the same request gives three different answers depending on which door it came through.

Logic exists so that there is one door. A consumer that wants something done says so and receives an outcome; it does not learn which Components were involved, in what order, or how their answers were combined. That is what makes a second consumer cheap: a command-line entry point, a scheduled job, or another Component arrives without reimplementing anything, because the reasoning was never inside the first consumer to begin with. It is also what makes the Components behind Logic replaceable: when the only route to stored data runs through here, Database can change everything behind its own boundary without Behaviour noticing.

The cost of the alternative is not untidiness, it is disagreement. Behaviour spread across consumers cannot be verified in one place, cannot be changed in one place, and cannot be trusted to mean the same thing twice.

### How It Works

A consumer names an Operation on Logic's Public Interface and gives it what that Operation needs. Logic works out what the request means: which Domain Definitions it concerns, which Components hold the answer, and in what order they have to be asked.

It then carries the work out through its Services. Each Service holds the calls into one Component's Public Interface, so a Service's Action is one call outwards — the Database Service's `create` is a call into Database's Public Interface, and a Service for another Component is the same thing pointed elsewhere. An Operation that needs one Component uses one Service; an Operation that needs several composes their Actions, deciding what to pass from one to the next and what belongs together in a single unit of work.

What comes back is an Application Outcome: the result the consumer asked for, or one of the expected failures that Operation declares. The consumer learns nothing else — not which Components were involved, not which Service performed which step, not how the answers were combined. That is the whole exchange, and it is the same exchange whether the consumer is an API process, a command-line entry point, or another Component.

<br>

## Understanding

How the Human explained this Component, in their own words, and what was decided along the way. The Principles state what holds; this section preserves how they were arrived at. It states no obligation: where this record and a Principle disagree, the Principle is correct.

<br>

### Logic

**What is Logic, in the Human's words?** Logic is the layer of reasoning: the logic, the functionality, the behaviours and the routines of the application are designed here. It is the hub of the Implementation — Model, Database and the consumers turn around it. It is not executable; it is a library.

**Who talks to it?** A consumer states what it wants done and Logic does the rest. The API is one consumer: it runs the server, receives the request and tells Logic. Tomorrow a command-line entry point, or another Component, is a consumer in the same way. Whoever wants to enter or change data for a Model asks Logic, never Database or Model directly.

**What does it talk to?** Logic talks to Model to understand the Domain Definitions and build on them, to Database to reach stored data, and later to further Components — Binance, MT5, Log, Report — each of which will be its own Component.

**How is it reached?** Nobody outside reaches Logic's internal parts. Logic has one Public Interface; it groups its Operations into Categories — Data Entry is one of them — and offers Operations: a consumer names the Operation and gives what it needs — the Model and the data for a data-entry Operation, the instrument and the parameters for opening an MT5 position — and Logic decides what to read from Model, what to ask of another Component, what to do, and what to answer. One Operation may use several internal Services.

**How does it reach the others?** Logic reaches any other Component only through that Component's Public Interface and the Operations it offers — Model for domain meaning, Database for stored data, and every Component that follows. The Service that owns a dependency holds those calls: the Database Service is where the Operations of Database's Public Interface are used, so an Action there is one call into Database. Logic has no other route out, and there are no separate Logic-side interface names for those boundaries.

**What is inside it?** Inside Logic the work is divided into Services, one per Component Logic talks to and named after it: a Database Service for the part of the reasoning that speaks to Database, and later an MT5 Service, a Binance Service, a Log Service, a Report Service. Services are internal — invisible from outside — and each performs Actions.

**Operations and Actions.** An Operation is the larger unit, offered by the Public Interface; an Action is the step a Service performs. Operations are composed of Actions. The Database Service performs create, update, delete, list, count, sum, min, max, truncate and execute command — the last one reaching Database's own capability-restricted command route for work the other Actions cannot express. Enabling and disabling are not Actions of their own: each is the update Action applied to one Field.

**The Data Entry Operations.** The Data Entry Category offers create, list, update, delete, enable, disable, count, sum, min, max and truncate. list carries the reading work: it takes filters — id among them, so reading one record needs no Operation of its own — an order_by field and direction, and a limit. enable sets the Activation Field the Model declares, and disable clears it; they stay two Operations rather than one with a flag, and each is carried out by the update Action. count, sum, min and max each take filters, and sum, min and max also take the field they work on. truncate empties a Model of its records while leaving its structure in place. The names follow REST and data-library convention rather than Interface-invented ones.

**Decisions:**

1. Logic's architecture is the Public Interface with its Categories and Operations, and the internal Services with their Actions. This replaces an earlier structure of a Logic Foundation, one Model Logic unit per Model inheriting from it, and a separate Use Case Logic unit for cross-Model Behaviour. The internal structure of each Service stays deliberately open.
2. That architecture is Logic's own. No named external standard is selected for it — an earlier choice of Hexagonal, with Clean as an alternative, and the policy requiring conformance to it, are not kept.
3. No consumer is named or privileged. Anything can talk to Logic through its Public Interface. An earlier statement that the API Component consumes it is not kept, because it read as a restriction that does not exist.
4. Logic reaches every other Component through that Component's own Public Interface, from the Service that owns the dependency. There are no separate Logic-side names for those boundaries; earlier Model Interface and Database Interface terms are not kept.
5. Public Interface and Operation are meant to become the shared standard of every Implementation Component — Model, Database, API and the rest — declared in Development so documentation can rely on them. Recorded here as the decision that produced it; Development owns the general statement.

**Still open.** Which further Categories and Operations the Public Interface offers, the full Action list of each Service beyond Database, and the internal structure of a Service are not yet decided.

<br>

## Terms

- **Behaviour** — what the application does when a consumer asks for something: the validation, the ordering, and the rules that hold for an operation in its application context rather than for one record on its own.
- **Public Interface** — the only Logic boundary a consumer sees, exposing the Operations Logic performs.
- **Category** — one named grouping of Operations in the Public Interface, gathering the Operations that serve the same kind of work.
- **Operation** — one complete unit of work the Public Interface offers a consumer, named by what the consumer wants done rather than by how it is carried out.
- **Service** — one internal part of Logic, owning the work that concerns one Component Logic talks to. A Service is internal: no consumer reaches it, names it, or depends on it.
- **Action** — one step a Service performs, carried out by calling an Operation of that Component's own Public Interface. Operations are composed of Actions; an Action is never offered directly to a consumer.
- **Application Outcome** — a logical success or expected failure independent of transport and persistence.

<br>

## Architecture

```text
Logic
├── Public Interface        ← the only part a consumer sees
│   └── Category
│       └── Operation
└── Services                ← internal; one per Component Logic talks to
    └── Service
        └── Action
```

The **Public Interface** is Logic's whole outward surface. It organizes what Logic offers into **Categories**, each gathering the Operations that serve one kind of work, and each **Operation** is one complete unit of work stated in the consumer's terms. Nothing else of Logic is visible: the Public Interface names no Service and exposes no Action.

**Services** are the inside of Logic. Each **Service** owns the work that concerns one Component Logic talks to and carries that Component's name, and each **Action** is one step that Service performs by calling an Operation of that Component's own Public Interface. An Operation is carried out by composing Actions, from one Service or several. Services stand beside one another rather than on top of one another, and none of them is reachable, nameable, or dependable from outside.

<br>

## Relationships

- **Consumes Model** — imports authoritative Domain Definitions and their declaration vocabulary through Model's Public Interface.
- **Consumes Database** — reaches persisted data and its transaction boundary through Database's Public Interface.
- **Consumes Development** — takes from it what Logic does not choose for itself: its identity, its technology, and the Connections it is permitted to make.
- **Consumes Platform** — receives the runtime values its configuration contract requires.
- **Consumed by any consumer** — provides the Public Interface through which any Component or entry point carries out the Operations Logic offers; the API is one such consumer, not a privileged one.

<br>

## Boundaries

- **A rule determinable from one Domain Definition's own data** — belongs to Model, because it holds wherever that definition is used, with no operation and no application context to qualify it.
- **A guarantee that requires comparing stored records** — belongs to Database, because only the Component that holds every record can enforce it; Logic would have to read the whole set to imitate it, and would still race with the next writer.
- **The shape of a request or a response on the wire, its status codes and its serialization** — belongs to the consumer that carries it, because it is a property of the transport rather than of the Behaviour underneath.
- **Selecting, provisioning, or operating an external service** — belongs to Development and Platform, because choosing a dependency and running it are decisions about the project and its environment, not about what the application does.
- **Where a value comes from at runtime** — belongs to Platform, because Logic owns the contract that says which values it needs and never the delivery of them.
- **The physical layout of stored data — tables, indexes, migrations, mappings** — belongs to Database, because it is how meaning is stored rather than what the meaning is.

<br>

Logic-owned behavioural defaults and internal realization conventions belong to Logic Preferences. Concrete language, package, framework, and Package Management choices belong to the Logic Component Profile in Development Preferences; API transport and process ownership belong to the API Component. Implementation applies those sources to the current Target.

<br>

## Documentation

Logic's documentation is written for a consumer who will never see inside it. It covers the Public Interface as Development Principle "Every Component has complete, safe, and operational documentation" requires — every Category and its Operations, what each Operation accepts and returns, the Application Outcomes it can produce, and how a consumer imports and calls it — and it stops there. Services and Actions are internal and are not documented for consumers: naming one in the documentation would make it something a consumer could come to rely on, which Principle "Logic is composed of internal Services, one per Component it talks to" forbids. A reader who finishes that documentation can carry out every Operation Logic offers without knowing which Component the work reached or which Service performed it.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## Principles

Every Principle below is mandatory.

<br>

### Logic is a reusable library

**Rule:** Logic owns application Behaviour and exposes it through its Public Interface. It does not start a process, own transport schemas, or depend on a consumer's framework.

**Why:** Behaviour that carries no transport of its own can be reused by any consumer, tested without a running server, and kept while the consumer changes — the API today, a command-line entry point or another Component tomorrow.

**Boundary:** Being a library does not make Logic's internal parts public; consumers use the Public Interface alone. Choosing the language, packages, and framework that realize the library belongs to Development.

<br>

### Logic owns Behaviour

**Rule:** Logic validates domain state, applies operation and application-context rules, and returns Application Outcomes. Behaviour remains independent of transport and storage.

**Why:** One owner for Behaviour keeps the same rule from being written differently in the API, the Database, and the Presentation.

**Boundary:** A rule determinable from a single Domain Definition's own data is an Intrinsic Rule owned by Model; a storage guarantee is owned by Database. Logic does not restate either.

<br>

### One Public Interface exposes Logic's Operations

**Rule:** Logic publishes exactly one Public Interface, and every consumer reaches Logic only through it. That Interface organizes what it offers into Categories, each gathering the Operations that serve one kind of work, and offers Operations: each one a complete unit of work stated in the consumer's terms — what it wants done and with what — never a route into Logic's internal parts. An Operation states what it accepts, what it returns, and which Application Outcomes it can produce.

**Why:** One boundary lets Logic reorganize inside itself without any consumer noticing, and lets a second consumer arrive without a second way in.

**Boundary:** The Public Interface names no Service, and exposes no Action, connection, session, or storage detail. A Category groups Operations and performs no work of its own. Which Categories and Operations exist, and what each Operation does, are declared in Logic Preferences, not fixed here.

<br>

### Logic is composed of internal Services, one per Component it talks to

**Rule:** Inside Logic, work is divided into Services. Each Service owns the work that concerns one Component Logic talks to and is named after it, so the Component a piece of Behaviour depends on is visible from its Service. A Service performs Actions; an Operation is carried out by composing Actions, from one Service or several. Services are internal: no consumer names one, reaches one, or depends on one, and no Service is promoted to the Public Interface.

**Why:** Dividing by the Component on the other side keeps each dependency in one place, so a Component can be added, replaced, or removed without that change spreading through unrelated Behaviour.

**Boundary:** Services sit beside one another, not on top of one another: none is the foundation of another, and one Service never reaches another Component's Service to do its work — the Operation composes them. Which Services exist, and which Actions each one performs, are declared in Logic Preferences.

<br>

### Logic reaches another Component only through that Component's Public Interface

**Rule:** Every route out of Logic runs through the Public Interface of the Component on the other side, and through the Operations that Interface offers. The Service that owns a dependency makes those calls; Logic reaches no Component by another route and holds no part of one that its Public Interface does not publish. Persistence follows the same rule: Logic reaches stored data only through Database's Public Interface, forwards grouped work through Database's transaction boundary, and never exposes engines, sessions, mappings, or schema details.

**Why:** A Component that is only ever reached through its own published surface can change everything behind it without reaching Behaviour, and every dependency Logic has is then visible as a call it is allowed to make.

**Boundary:** Logic decides which operations belong together in one unit of work; the Component on the other side owns what happens inside its own boundary — for Database, commit, rollback, isolation, and retry. What that Component publishes is its own decision, not Logic's.

<br>

### Domain meaning is imported, never restated

**Rule:** Logic imports authoritative Domain Definitions through Model's Public Interface and uses them as Model declares them. It never copies, mirrors, or redefines a Domain Definition, and never re-derives meaning Model already publishes.

**Why:** One definition shared by every Component is what keeps the domain from drifting into several versions of itself.

**Boundary:** Logic may hold a shape of its own for an input or an outcome that has no Domain Definition; it never mirrors one that does.

<br>

### External dependencies remain explicit

**Rule:** Logic consumes only the external services and cross-cutting capabilities selected by Development, through explicit interfaces and only where Behaviour requires them. An external service is reached through the Service that owns that dependency, never from scattered points inside Logic.

**Why:** An implicit dependency on something outside Logic is invisible until it fails or has to be replaced.

**Boundary:** Logic does not select, provision, or operate an external service; Development selects it and Platform operates it. An external service consumed this way is not a Logic Service — Logic Services are internal parts of this Component.

<br>

### Runtime configuration stays private

**Rule:** Logic defines the configuration contract required by its Behaviour and validates required values before use. Runtime values are supplied to Logic by its environment; secrets never enter source, errors, or public interfaces.

**Why:** A contract validated before readiness fails at start with a clear cause rather than mid-operation with an unclear one.

**Boundary:** Logic owns the contract and its validation, never the values, their delivery, or the environment they come from.

<br>

### Logic verification covers Logic boundaries

**Rule:** Verification covers isolated Logic, each Service's calls into the Public Interface it depends on, transaction behaviour, and every Operation the Public Interface offers — its inputs, its result, and each Application Outcome it declares — without requiring a live consumer process.

**Why:** Behaviour that can only be verified through a running API is verified at the wrong boundary and hides which layer actually failed.

**Boundary:** Verification here does not extend to transport, presentation, or deployment; those are verified by the Components that own them. Whether a check persists as a test in this Component follows Development's Cross-cutting Capability applicability.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Logic is a reusable library**

- **Must** — Expose application Behaviour through one public Logic Interface.
- **Never** — Start a process, own a transport schema, or depend on an API framework inside Logic.

**Logic owns Behaviour**

- **Must** — Validate domain state, apply operation and application-context rules, and return Application Outcomes.
- **Never** — Let Behaviour depend on transport or storage, or restate a Model Intrinsic Rule or a Database guarantee.

**One Public Interface exposes Logic's Operations**

- **Must** — Publish exactly one Public Interface and let every consumer reach Logic only through it.
- **Must** — Organize the Public Interface's Operations into Categories, each gathering the Operations that serve one kind of work.
- **Must** — State for every Operation what it accepts, what it returns, and which Application Outcomes it can produce.
- **Never** — Expose a Service, an Action, a connection, a session, or a storage detail through the Public Interface.

**Logic is composed of internal Services, one per Component it talks to**

- **Must** — Divide Logic into internal Services, each owning the work that concerns one Component Logic talks to and named after it.
- **Must** — Carry out an Operation by composing Actions from one Service or several.
- **Never** — Let a consumer name, reach, or depend on a Service, or let one Service do its work through another Component's Service.

**Logic reaches another Component only through that Component's Public Interface**

- **Must** — Reach every other Component only through that Component's Public Interface and its Operations, from the Service that owns the dependency.
- **Must** — Forward grouped persistence work through Database's transaction boundary.
- **Never** — Reach a Component by another route, hold a part of one its Public Interface does not publish, or expose engines, sessions, mappings, or schema details.

**Domain meaning is imported, never restated**

- **Must** — Import authoritative Domain Definitions through Model's Public Interface and use them as Model declares them.
- **Never** — Copy or redefine a Domain Definition inside Logic.

**External dependencies remain explicit**

- **Must** — Consume an external service or cross-cutting capability only when Development selected it and Behaviour requires it, through the Service that owns that dependency.
- **Never** — Select, provision, or operate an external service from Logic.

**Runtime configuration stays private**

- **Must** — Define Logic's configuration contract and validate every required value before use.
- **Never** — Put a secret in source, an error, or a public interface, or take ownership of runtime values.

**Logic verification covers Logic boundaries**

- **Must** — Verify isolated Logic, each Service's calls into its Component's Public Interface, transaction behaviour, and every Operation with its inputs, result, and declared Application Outcomes, without a live consumer process.
- **Never** — Push Logic verification into transport, presentation, or deployment, or persist a check in a Component outside the testing applicability list.
