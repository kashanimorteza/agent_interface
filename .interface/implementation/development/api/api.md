# API Definition

API is the Development Component that publishes selected Logic Services as one external HTTP boundary.

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

API is the single external HTTP gateway to the capabilities selected from Logic. It may contain several API Groups while all Groups share one running API, one address, and one lifecycle. Each eligible Logic Service receives exactly one corresponding Group with its own routes and internal boundary.

API describes responsibilities and observable contracts independently of programming language, framework, package, or implementation technique. API Preferences may select a default realization, while the selected package or implementation skill decides its technical mechanics.

### Purpose

Logic may publish several Services, but an external consumer needs a clear and stable way to reach only the capabilities intended for API access. API provides that way without copying Behaviour into transport code or exposing internal Logic, Model, Database, or Storage details.

Each Group keeps one Service's external surface separate from the others. The shared API composes those Groups into one boundary, so adding or removing a Group does not create another server or change the ownership of application Behaviour.

### How It Works

API reads Logic Interface and the settings of its Services. A Service receives an API Group only when both `publish_in_logic_interface` and `generate_api` are `true`. The Group corresponds to that one Service and uses only the Service Interface published through Logic Interface.

Inside a Group, Router receives and returns HTTP data. Adapter translates between that external contract and the corresponding Logic Service Interface. Router calls only its own Adapter, and Adapter calls only its matching Logic Service through Logic Interface.

Each callable Action published by the Service becomes an Endpoint by default. An Action may explicitly set `generate_api: false` in its owning Service to remain outside API. Support exports such as types, enums, constants, and metadata help define the contract but never become Endpoints.

Bootstrap composes all Groups into one running API. Core contains only shared private API capabilities. The external contract, documentation, and running routes describe the same Groups and Endpoints.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **API Group** — the external API surface corresponding to exactly one eligible Logic Service.
- **Eligible Logic Service** — a Service for which both `publish_in_logic_interface` and `generate_api` are `true`.
- **Bootstrap** — the single composition point that assembles and starts the API and registers every Group.
- **Core** — the private home of shared API capabilities owned by no single Group.
- **Router** — the HTTP-facing part of one Group, responsible for its routes and external request and response contract.
- **Adapter** — the transport-independent part of one Group that maps valid external data to its corresponding Logic Service Interface and maps the declared result back.
- **Endpoint** — the public HTTP representation of one API-enabled callable Service Action.
- **Transport Schema** — an external request or response shape owned by API; it is not a copied Domain Entity.
- **Request Context** — non-secret request metadata carried across the API boundary when a capability needs it.
- **External Contract** — the human- and machine-readable description of the API Groups, Endpoints, requests, responses, and failures.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
API
├── bootstrap
├── core/
├── groups/
│   └── <service>/
│       ├── router/
│       └── adapter/
├── config.yaml
└── README.md
```

The names shown are defaults selected by API Preferences. A selected language may realize a small Group compactly and a large Group through several files, but the responsibilities and dependency direction remain unchanged. API Interface is the published HTTP contract and is not a separate root source file.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Logic** — discovers eligible Services and invokes their callable Actions only through Logic Interface.
- **Consumes Development** — receives the shared implementation defaults and the declared connection to Logic.
- **Consumes Platform** — receives the runtime bindings needed to run the API.
- **Consumed by Presentation and external clients** — publishes one external HTTP contract containing every generated Group.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Application Behaviour and application decisions** — belong to Logic; API only represents and carries a request to the owning Service.
- **Domain meaning** — belongs to Model and reaches API through Logic contracts; API never reads Model directly.
- **Persistence** — belongs behind Logic and Database; API never calls Database or Storage Service directly.
- **HTTP routes, external shapes, transport validation, serialization, and public failures** — belong to API.
- **Technical framework mechanics** — belong to the selected package and implementation skill, provided that they preserve this Definition.
- **Runtime values and process operation** — are supplied by Platform; API declares only what its running boundary needs.
- **Authentication** — is not part of the current API contract and is not generated implicitly. A future Target requirement must introduce it explicitly.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

API has one dependency direction: Bootstrap registers Groups; within each Group, Router calls Adapter and Adapter calls the matching Logic Service through Logic Interface. Core may support the API internally but is never another public layer.

### Bootstrap

The single composition and startup point of API. It assembles the selected realization, registers every generated Group, applies shared API concerns, and exposes one running boundary. It contains no Group Action, application Behaviour, or persistence work.

### Core

The private directory for API capabilities shared by several Groups and owned by none of them. A concern that belongs to only one Group remains inside that Group.

### Groups

The directory containing exactly one Group for each eligible Logic Service. A Group is identified by its source Service, keeps its own Router and Adapter, and never calls another Group. If an external capability needs coordination across several Services, that coordination first becomes a Logic Service and API may then create a Group for it.

For Entity Service, there is one Entity Group rather than one Group per Entity. Each Entity Child Service becomes a resource inside that Group, and its API-enabled callable Actions become Endpoints. Router and Adapter may use one file per Entity when the selected realization benefits from that structure.

### Router

The HTTP-facing boundary of one Group. It owns the Group route namespace, methods selected by the API contract, external request and response shapes, transport validation, response production, and public contract metadata. It calls only its Group Adapter.

### Adapter

The transport-independent bridge between one Router and one Logic Service Interface. It maps validated external input to the published Action contract, invokes only the matching Service through Logic Interface, and returns the declared result or failure for Router to represent. It contains neither HTTP mechanics nor application Behaviour.

### Configuration

`config.yaml` contains only runtime values declared by API. Component structure and configurable defaults remain in API Preferences, while Platform supplies environment-specific bindings.

### Documentation

Documentation describes the external contract by Group and Endpoint. Each Group owns the explanation of its own operations, while the root documentation introduces the enabled Groups and presents one combined API boundary.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

API Definition Principles are mandatory. API Preferences provide configurable defaults for unstated API choices. Explicit compatible Target meaning takes precedence over those defaults, while no Preference or package may weaken a Principle.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### API remains independent of its realization

**Rule:** API Definition fixes responsibilities, boundaries, dependency direction, and observable contracts without requiring a programming language, framework, package, decorator, or implementation pattern.
**Why:** The same API Component must remain understandable and implementable across compatible technology choices.
**Boundary:** API Preferences may select defaults, and the selected package or implementation skill may choose mechanics, but neither may change the conceptual contract.

#### API publishes selected Logic capabilities only

**Rule:** API publishes only callable Actions reached through eligible Service Interfaces in Logic Interface. It never imports Logic internals, Model, Database, or Storage Service directly.
**Why:** One public dependency keeps application Behaviour authoritative in Logic and prevents API from becoming another implementation of the application.
**Boundary:** API may own an external representation of a published capability without copying its domain meaning or Behaviour.

<br>

### Groups

#### Group membership comes from Logic Service settings

**Rule:** API creates exactly one Group for each Service whose `publish_in_logic_interface` and `generate_api` settings are both `true`, and no Group for any other Service. `generate_api: true` with root publication disabled is invalid.
**Why:** Logic Service settings remain the single authority for whether a Service is reachable and whether API represents it.
**Boundary:** API Preferences may override API-owned names or contract details but never maintain a second Service catalogue.

#### Each Group corresponds to one Logic Service

**Rule:** Router calls only its own Adapter, and Adapter calls only the Group's corresponding Logic Service Interface through Logic Interface. Groups never call one another.
**Why:** A one-to-one boundary keeps ownership and dependency paths clear.
**Boundary:** Cross-Service orchestration belongs to a Logic Service, which may receive its own Group when eligible.

#### Endpoint membership follows callable Action settings

**Rule:** Every callable Action published by an eligible Service becomes exactly one Endpoint unless that Action explicitly sets `generate_api: false` in its owning Service. Non-callable exports never become Endpoints.
**Why:** Endpoint membership stays aligned with the authoritative Service contract without a second hand-maintained catalogue.
**Boundary:** An API override may change an Endpoint's external representation but never create an Action absent from the Service Interface.

#### Group identities and routes remain unique

**Rule:** Every Group identity, directory, route prefix, and final method-and-path combination is valid and unique after the selected realization's declared normalization. A collision or invalid identity stops generation with a clear error.
**Why:** Silent renaming changes the public contract and makes routing ambiguous.
**Boundary:** API never resolves a conflict by inventing a suffix, number, or hidden rename.

<br>

### Router

#### Router owns HTTP representation only

**Rule:** Router owns its Group's external routes, methods, requests, responses, transport validation, serialization, and public failure representation. It calls its Adapter and contains no application Behaviour.
**Why:** Keeping HTTP at the edge lets Logic and Adapter remain independent of transport.
**Boundary:** Router never calls Logic, another Group, Database, or Storage Service directly.

#### Endpoint methods are explicit

**Rule:** Every Endpoint receives an explicit HTTP method from Target or API Preferences. API never guesses a method from an Action name. A missing method stops generation of that Endpoint with a clear unresolved-choice error.
**Why:** Action names do not reliably determine transport semantics.
**Boundary:** The selected package implements the chosen method but does not choose the public contract silently.

#### External schemas follow published Action contracts

**Rule:** API derives an Endpoint's default request and response shapes from its published Action contract. API defines a distinct Transport Schema only when the external representation must differ. An insufficient Action contract stops Endpoint generation.
**Why:** Derivation avoids copying meaning while still allowing a deliberate external representation.
**Boundary:** Shape validation belongs to API; application validity and Behaviour remain in Logic.

#### Collections remain explicit and bounded

**Rule:** Filtering, ordering, and pagination are available only when an Endpoint contract declares them. Their public values are allowlisted and bounded, and never become direct storage commands.
**Why:** An external caller must not control internal queries or request an unbounded public result.
**Boundary:** The pagination form belongs to the Endpoint contract; Adapter only maps it to the corresponding Logic input.

#### Public outcomes remain faithful and safe

**Rule:** A successful Endpoint returns its declared Action result without an API-wide success envelope. Declared failures remain failures, and unexpected failures become a safe public response carrying a non-secret request identifier.
**Why:** API must preserve the capability contract without exposing internal details or inventing a second result model.
**Boundary:** Exact HTTP representation is selected by the API realization, but it may never expose internal exceptions, persistence details, secrets, or turn a failure into success.

<br>

### Adapter

#### Adapter maps without reimplementing Behaviour

**Rule:** Adapter maps validated external input to the matching published Action, invokes that Action through Logic Interface, and maps its declared result back toward Router. It contains no HTTP mechanics, application decision, or persistence implementation.
**Why:** A narrow Adapter prevents transport and Behaviour from leaking into one another.
**Boundary:** Adapter may perform representation mapping but never changes the meaning, permission, or result of an Action.

<br>

### Bootstrap and Core

#### Bootstrap owns one shared API composition

**Rule:** API has exactly one Bootstrap, one running boundary, and one shared lifecycle. Bootstrap registers every Group and contains composition only; a Group never creates its own server or process.
**Why:** Groups are independent contract areas, not independent applications.
**Boundary:** Runtime bindings come from Platform, and implementation mechanics come from the selected package or skill.

#### Core remains shared and private

**Rule:** A private API capability shared by several Groups and owned by none belongs in Core. Core publishes no Endpoint and contains no application Behaviour.
**Why:** Shared concerns need one internal home without becoming another public layer.
**Boundary:** A Group-specific concern remains in that Group even when a similar concern exists elsewhere.

<br>

### Contract and Documentation

#### API owns one consistent external contract

**Rule:** Running routes, machine-readable contract, and human documentation describe the same Groups, Endpoints, requests, responses, versions, and failures.
**Why:** Consumers must not build against a description that differs from the running boundary.
**Boundary:** The selected package may produce the machine-readable form; API Definition does not prescribe its technical format or default path.

#### Versioning is an external-contract choice

**Rule:** When Target requires versioning, API applies one declared versioning policy across the shared boundary unless Target explicitly gives a Group a different contract. API never infers a versioning strategy.
**Why:** Versioning manages compatibility and must therefore be deliberate and visible.
**Boundary:** API Preferences may provide a default strategy, while the selected package decides only how to realize it.

#### Documentation is organized by Group

**Rule:** Each Group documents its published Endpoints, accepted input, returned output, and failures. Root documentation introduces enabled Groups and presents them as one API.
**Why:** Consumers need both a complete boundary and a clear view of each capability area.
**Boundary:** Documentation exposes no unpublished Service, private API structure, Logic implementation, or Database detail.

<br>

### Lifecycle and Verification

#### Health and readiness always exist

**Rule:** API always exposes distinct health and readiness signals. Health reports that the API is alive; readiness is positive only after required configuration and dependencies are ready. Their paths are configurable, but the signals cannot be disabled.
**Why:** Operators need to distinguish a running process from one able to serve requests.
**Boundary:** The selected package implements the signals, while Platform decides how to use them.

#### Verification covers the published boundary

**Rule:** Verification confirms Group eligibility, one-to-one Group mapping, Endpoint membership, route uniqueness, Router-to-Adapter-to-Logic dependency direction, contract consistency, bounded collection input, safe failures, and lifecycle signals.
**Why:** The published boundary is what external consumers rely on.
**Boundary:** API verification never replaces Logic Behaviour or Database persistence verification.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**API remains independent of its realization**

- **Must** — Preserve the same responsibilities, boundaries, dependency direction, and observable contract across compatible realizations.
- **Never** — Make a language, framework, package, or implementation pattern part of API Definition.

**API publishes selected Logic capabilities only**

- **Must** — Reach API-enabled callable Actions only through eligible Service Interfaces in Logic Interface.
- **Never** — Reimplement Behaviour or access Model, Database, Storage Service, or private Logic directly.

### Groups

**Group membership comes from Logic Service settings**

- **Must** — Create exactly one Group only when both Service settings are true.
- **Never** — Maintain a second Service catalogue or generate a Group for an unpublished Service.

**Each Group corresponds to one Logic Service**

- **Must** — Keep each Router, Adapter, and Logic Service connection inside one Group boundary.
- **Never** — Call between Groups or coordinate several Logic Services inside API.

**Endpoint membership follows callable Action settings**

- **Must** — Create exactly one Endpoint for each API-enabled callable Action.
- **Never** — Turn a support export into an Endpoint or create an Action absent from the Service Interface.

**Group identities and routes remain unique**

- **Must** — Validate Group identities, paths, and final route combinations before realization.
- **Never** — Repair an invalid or colliding value with a silent rename, suffix, or number.

### Router

**Router owns HTTP representation only**

- **Must** — Keep routes, external shapes, transport validation, serialization, and public failures in Router.
- **Never** — Put application Behaviour in Router or call Logic, another Group, Database, or Storage directly.

**Endpoint methods are explicit**

- **Must** — Obtain every Endpoint method from Target or API Preferences.
- **Never** — Guess an HTTP method from an Action name.

**External schemas follow published Action contracts**

- **Must** — Derive default external shapes from the Action contract and define a distinct shape only when needed.
- **Never** — Copy Domain meaning or generate an Endpoint from an insufficient Action contract.

**Collections remain explicit and bounded**

- **Must** — Allow only declared and bounded filtering, ordering, and pagination.
- **Never** — Expose an unbounded result or convert public input directly into a storage command.

**Public outcomes remain faithful and safe**

- **Must** — Return the declared success result directly and represent failures safely.
- **Never** — Add a universal success envelope, expose private failures, or turn a failure into success.

### Adapter

**Adapter maps without reimplementing Behaviour**

- **Must** — Map between Router and the matching Service Action through Logic Interface.
- **Never** — Add HTTP mechanics, application decisions, or persistence work to Adapter.

### Bootstrap and Core

**Bootstrap owns one shared API composition**

- **Must** — Register all Groups through one Bootstrap, running boundary, and lifecycle.
- **Never** — Create a separate server or process for a Group.

**Core remains shared and private**

- **Must** — Keep only shared private API capabilities in Core.
- **Never** — Publish Core or move a Group-specific concern into it.

### Contract and Documentation

**API owns one consistent external contract**

- **Must** — Keep running routes, machine-readable contract, and human documentation consistent.
- **Never** — Let package mechanics silently redefine the external contract.

**Versioning is an external-contract choice**

- **Must** — Apply a declared versioning policy when Target requires versioning.
- **Never** — Infer a versioning strategy or let each Group drift without explicit Target intent.

**Documentation is organized by Group**

- **Must** — Document every generated Group and Endpoint as part of one API boundary.
- **Never** — Expose unpublished Services or private implementation details.

### Lifecycle and Verification

**Health and readiness always exist**

- **Must** — Expose distinct, configurable health and readiness signals.
- **Never** — Disable either signal or report readiness before required configuration and dependencies are ready.

**Verification covers the published boundary**

- **Must** — Verify Group and Endpoint membership, dependency direction, route uniqueness, contract consistency, bounds, safe failures, and lifecycle.
- **Never** — Treat API verification as a replacement for Logic or Database verification.
