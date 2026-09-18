# Logic Principles

Logic is the independent Logic Component that implements the Target's application Behaviour as a reusable library. It is the hub of the Implementation: Model, Database, and every consumer — the API today, a command-line entry point or another Component tomorrow — meet through it. A consumer states what it wants done; Logic decides what to read from Model, what to ask of Database or another Component, what to compute, and what to answer.

Logic owns application Behaviour and the rules that depend on an operation and its application context. It does not own domain meaning, persistence, transport, presentation, or process operation.

<br>

## Terms

- **Logic** — the Logic part that owns application Behaviour and operation-dependent rules.
- **Public Interface** — the only Logic boundary a consumer sees, exposing the Operations Logic performs.
- **Category** — one named grouping of Operations in the Public Interface, gathering the Operations that serve the same kind of work.
- **Operation** — one complete unit of work the Public Interface offers a consumer, named by what the consumer wants done rather than by how it is carried out.
- **Service** — one internal part of Logic, owning the work that concerns one Component Logic talks to. A Service is internal: no consumer reaches it, names it, or depends on it.
- **Action** — one step a Service performs. Operations are composed of Actions; an Action is never offered directly to a consumer.
- **Model Interface** — Logic's boundary onto Model's Public Interface.
- **Database Interface** — Logic's boundary onto Database's Public Interface.
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

**Services** are the inside of Logic. Each **Service** owns the work that concerns one Component Logic talks to and carries that Component's name, and each **Action** is one step that Service performs. An Operation is carried out by composing Actions, from one Service or several. Services stand beside one another rather than on top of one another, and none of them is reachable, nameable, or dependable from outside.

<br>

## Relationships

- **Consumes Model** — imports authoritative Domain Definitions and their declaration vocabulary through Model's Public Interface.
- **Consumes Database** — reaches persisted data and its transaction boundary through Database's public Database Interface.
- **Consumes Development** — uses its Component Profile, shared rules, technical items, Connections, and Platform Reference.
- **Consumes Platform** — receives the runtime values its configuration contract requires.
- **Consumed by API** — provides the Logic Public Interface the API Component publishes over a transport.

<br>

Logic-owned behavioural defaults and internal realization conventions belong to Logic Preferences. Concrete language, package, framework, and Package Management choices belong to the Logic Component Profile in Development Preferences; API transport and process ownership belong to the API Component. Implementation applies those sources to the current Target.

<br>

## Documentation

Logic's documentation is written for a consumer who will never see inside it. It covers the Public Interface as Development Principle 8 requires — every Category and its Operations, what each Operation accepts and returns, the Application Outcomes it can produce, and how a consumer imports and calls it — and it stops there. Services and Actions are internal and are not documented for consumers: naming one in the documentation would make it something a consumer could come to rely on, which Principle 4 forbids. A reader who finishes that documentation can carry out every Operation Logic offers without knowing which Component the work reached or which Service performed it.

<br>

Every statement here is mandatory. A Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Logic is a reusable library

**Rule:** Logic owns application Behaviour and exposes it through its Public Interface. It does not start a process, own transport schemas, or depend on a consumer's framework.

**Why:** Behaviour that carries no transport of its own can be reused by any consumer, tested without a running server, and kept while the consumer changes — the API today, a command-line entry point or another Component tomorrow.

**Boundary:** Being a library does not make Logic's internal parts public; consumers use the Public Interface alone. Choosing the language, packages, and framework that realize the library belongs to Development.

<br>

## 2. Logic owns Behaviour

**Rule:** Logic validates domain state, applies operation and application-context rules, and returns Application Outcomes. Behaviour remains independent of transport and storage.

**Why:** One owner for Behaviour keeps the same rule from being written differently in the API, the Database, and the Presentation.

**Boundary:** A rule determinable from a single Domain Definition's own data is an Intrinsic Rule owned by Model; a storage guarantee is owned by Database. Logic does not restate either.

<br>

## 3. One Public Interface exposes Logic's Operations

**Rule:** Logic publishes exactly one Public Interface, and every consumer reaches Logic only through it. That Interface organizes what it offers into Categories, each gathering the Operations that serve one kind of work, and offers Operations: each one a complete unit of work stated in the consumer's terms — what it wants done and with what — never a route into Logic's internal parts. An Operation states what it accepts, what it returns, and which Application Outcomes it can produce.

**Why:** One boundary lets Logic reorganize inside itself without any consumer noticing, and lets a second consumer arrive without a second way in.

**Boundary:** The Public Interface names no Service, and exposes no Action, connection, session, or storage detail. A Category groups Operations and performs no work of its own. Which Categories and Operations exist, and what each Operation does, are declared in Logic Preferences, not fixed here.

<br>

## 4. Logic is composed of internal Services, one per Component it talks to

**Rule:** Inside Logic, work is divided into Services. Each Service owns the work that concerns one Component Logic talks to and is named after it, so the Component a piece of Behaviour depends on is visible from its Service. A Service performs Actions; an Operation is carried out by composing Actions, from one Service or several. Services are internal: no consumer names one, reaches one, or depends on one, and no Service is promoted to the Public Interface.

**Why:** Dividing by the Component on the other side keeps each dependency in one place, so a Component can be added, replaced, or removed without that change spreading through unrelated Behaviour.

**Boundary:** Services sit beside one another, not on top of one another: none is the foundation of another, and one Service never reaches another Component's Service to do its work — the Operation composes them. Which Services exist, and which Actions each one performs, are declared in Logic Preferences.

<br>

## 5. Persistence has one boundary

**Rule:** Database Interface is Logic's only route to persistence and forwards grouped operations through Database's transaction boundary. Logic never exposes engines, sessions, mappings, or schema details.

**Why:** A single persistence boundary lets the Engine, the mapping, and the Database's internals change without reaching Behaviour.

**Boundary:** Logic decides which operations belong together in one unit of work; Database owns commit, rollback, isolation, and retry behaviour within it.

<br>

## 6. Model meaning has one boundary

**Rule:** Model Interface imports authoritative public definitions. Logic never copies or redefines Domain Definitions.

**Why:** One definition shared by every Component is what keeps the domain from drifting into several versions of itself.

**Boundary:** Logic may hold a shape of its own for an input or an outcome that has no Domain Definition; it never mirrors one that does.

<br>

## 7. External dependencies remain explicit

**Rule:** Logic consumes only the external services and cross-cutting capabilities selected by Development, through explicit interfaces and only where Behaviour requires them. An external service is reached through the Service that owns that dependency, never from scattered points inside Logic.

**Why:** An implicit dependency on something outside Logic is invisible until it fails or has to be replaced.

**Boundary:** Logic does not select, provision, or operate an external service; Development selects it and Platform operates it. An external service consumed this way is not a Logic Service — Logic Services are internal parts of this Component.

<br>

## 8. Runtime configuration stays private

**Rule:** Logic defines the configuration contract required by its Logic and validates required values before use. Platform supplies runtime values; secrets never enter source, errors, or public interfaces.

**Why:** A contract validated before readiness fails at start with a clear cause rather than mid-operation with an unclear one.

**Boundary:** Logic owns the contract and its validation, never the values, their delivery, or the environment they come from.

<br>

## 9. Logic verification covers Logic boundaries

**Rule:** Verification covers isolated Logic, Model Interface, Database Interface, transaction behaviour, outcomes, and every public Logic operation without requiring a live API process.

**Why:** Behaviour that can only be verified through a running API is verified at the wrong boundary and hides which layer actually failed.

**Boundary:** Verification here does not extend to transport, presentation, or deployment; those are verified by the Components that own them. Whether a check persists as a test in this Component follows Development's Cross-cutting Capability applicability.

<br>

## At a Glance

- **Must** — Expose application Behaviour through one public Logic Interface. *(1)*
- **Never** — Start a process, own a transport schema, or depend on an API framework inside Logic. *(1)*
- **Must** — Validate domain state, apply operation and application-context rules, and return Application Outcomes. *(2)*
- **Never** — Let Behaviour depend on transport or storage, or restate a Model Intrinsic Rule or a Database guarantee. *(2)*
- **Must** — Publish exactly one Public Interface and let every consumer reach Logic only through it. *(3)*
- **Must** — Organize the Public Interface's Operations into Categories, each gathering the Operations that serve one kind of work. *(3)*
- **Must** — State for every Operation what it accepts, what it returns, and which Application Outcomes it can produce. *(3)*
- **Never** — Expose a Service, an Action, a connection, a session, or a storage detail through the Public Interface. *(3)*
- **Must** — Divide Logic into internal Services, each owning the work that concerns one Component Logic talks to and named after it. *(4)*
- **Must** — Carry out an Operation by composing Actions from one Service or several. *(4)*
- **Never** — Let a consumer name, reach, or depend on a Service, or let one Service do its work through another Component's Service. *(4)*
- **Must** — Reach persistence only through Database Interface, forwarding grouped operations through Database's transaction boundary. *(5)*
- **Never** — Expose engines, sessions, mappings, or schema details through Logic. *(5)*
- **Must** — Import authoritative Domain Definitions through Model Interface. *(6)*
- **Never** — Copy or redefine a Domain Definition inside Logic. *(6)*
- **Must** — Consume an external service or cross-cutting capability only when Development selected it and Behaviour requires it, through the Service that owns that dependency. *(7)*
- **Never** — Select, provision, or operate an external service from Logic. *(7)*
- **Must** — Define Logic's configuration contract and validate every required value before use. *(8)*
- **Never** — Put a secret in source, an error, or a public interface, or take ownership of runtime values. *(8)*
- **Must** — Verify isolated Logic, both Interfaces, transaction behaviour, outcomes, and every public operation without a live API process. *(9)*
- **Never** — Push Logic verification into transport, presentation, or deployment, or persist a check in a Component outside the testing applicability list. *(9)*
