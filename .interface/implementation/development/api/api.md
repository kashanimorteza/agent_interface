# API Definition

API is the executable Development Component that owns the external communication boundary and publishes selected application capabilities through a transport.

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

API is an independent executable Component. It starts its own process, owns the selected external transport, validates transport data, invokes application capabilities through Logic Interface, and maps declared results and failures into public responses. API owns no authoritative application Behaviour or persistence.

Its Architecture and responsibilities remain stable across languages, frameworks, packages, and transports. API Preferences select the concrete realization and configurable Architecture names; Platform supplies runtime bindings.

<br>

### Purpose

A running application needs one owner for everything required to be externally reachable: process startup, protocol handling, request validation, identity establishment, response serialization, safe failure mapping, public documentation, and lifecycle endpoints. These responsibilities describe how the application is reached, not what the application means or permits.

API keeps those concerns outside Logic. A second transport or consumer can therefore be added without moving transport concepts into application Behaviour, and Logic can change behind its published Interface without exposing its implementation to external callers.

<br>

### How It Works

Application Bootstrap creates the selected framework application and wires Core, Routers, Services, middleware, exception mapping, authentication, and lifecycle hooks. A request reaches the matching Router, which owns the route, method, transport inputs and outputs, transport validation, and Request Context.

Router delegates the request to its corresponding API Service. Service prepares the transport-independent input and enters Logic through Logic Interface. It selects the required Logic Service Interface and then calls the capability that Interface publishes; for Entity Service this includes selecting the appropriate Entity Child Service before its Action. API never imports a private Logic implementation.

The called Logic capability returns its declared result or expected failure. API introduces no assumed common Logic result wrapper. Router maps that declared outcome to the external response contract. Unexpected failures become safe generic responses carrying a non-secret request identifier, while credentials and internal details remain inside the boundary.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **API Interface** — the complete external boundary formed by published routes, request and response shapes, authentication requirements, and the machine-readable contract; it is not a root source file.
- **Application Bootstrap** — the root file that creates the selected framework application and composes the API process.
- **Core** — the private directory for shared API files and capabilities owned by no one Router or Service.
- **Router** — one transport-facing module that owns routes, transport schemas, validation, Request Context, and response mapping for a domain area.
- **API Service** — one transport-independent module between a Router and Logic Interface, normally paired with the same domain area.
- **Logic Interface** — the public Logic surface through which API selects a Logic Service Interface and uses its published capabilities.
- **Transport Schema** — an input or output shape owned by API when the external representation differs from a Logic or Model representation.
- **Request Context** — validated non-secret identity and tracing information for one request.
- **External Contract** — the human- and machine-readable description of API's published boundary.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
API
├── application
├── core/
├── router/
│   └── <domain>
├── service/
│   └── <domain>
├── config.yaml
└── README.md
```

The names shown are defaults selected by API Preferences. Changing a name changes the realization path, not the responsibility represented by that member. API Interface is the external transport surface produced by this Architecture, not an additional source file.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Logic** — invokes application capabilities only through Logic Interface and the Service Interfaces it publishes.
- **Consumes Development** — receives shared Defaults and the declared direct Connection to Logic.
- **Consumes Platform** — receives runtime bindings, secret references, and the shutdown deadline its process observes.
- **Consumed by Presentation** — publishes the external contract and capabilities Presentation reaches through its API Access layer.
- **Consumed by other external clients** — serves callers authorized by the Target through the selected transport.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Application Behaviour and authorization decisions** — belong to Logic; API carries validated identity and invokes the applicable Logic capability.
- **Domain meaning** — belongs to Model and is reached through Logic; API may own a Transport Schema without redefining a Domain Definition.
- **Persistence and raw Database access** — belong behind Logic and Storage Service; API never calls Database or Storage Service outside Logic Interface.
- **Transport routes, schemas, authentication, statuses, serialization, and public error shapes** — belong to API.
- **Runtime values and process operation** — belong to Platform; API owns the contract that declares the values it requires and the lifecycle behavior it exposes.
- **User-interface behavior** — belongs to Presentation; API publishes capabilities without deciding how they are displayed.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

API owns the external transport boundary and its process. Its internal dependency direction is Application Bootstrap → Router → API Service → Logic Interface. Core supplies shared private API capabilities without becoming another public layer.

### Application Bootstrap

The configured root application file. It creates the selected framework application, loads validated API configuration, registers Routers, installs middleware and exception handling, wires authentication, configures lifecycle hooks, and exposes the process entrypoint. It contains composition only.

### Core

The private directory for shared API files used across domain Routers or Services but owned by none of them, such as common Request Context support, shared error representation, configuration loading, and lifecycle coordination. Core defines no route or application Behaviour.

### Routers

The transport-facing directory. It contains one Router file per configured or selected domain area. A Router owns routes, Transport Schemas, transport validation, authentication dependencies, status mapping, response serialization, and machine-readable contract metadata. It calls its corresponding API Service and never Logic or Database directly.

### Services

The transport-independent API coordination directory. It contains one API Service file per applicable domain area. Service prepares inputs for Logic, selects a Logic Service Interface and its published capability, and returns that declared result to Router. It imports no Router, framework Request or Response type, transport status, or Database capability.

### Configuration

`config.yaml` is API's generated or supplied runtime configuration file. API declares and validates its contract before readiness. Runtime values and secret delivery remain owned by Platform.

### Documentation

Documentation explains the external API contract for a consumer with no access to API internals. Its filename, location, format, order, and sections are selected by API Preferences. The machine-readable contract remains consistent with the running routes and complements rather than replaces consumer documentation.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

API Definition Principles are mandatory. API Preferences provide configurable defaults and conventions, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the Architecture or Layering category that owns it.

### General

#### API is an independent executable

**Rule:** API owns its process, startup, external transport, serialization, versioning, and external contract. Logic remains a library consumed through Logic Interface.
**Why:** An independently executable boundary can be started, stopped, scaled, or replaced without moving process ownership into Logic.
**Boundary:** API owns no authoritative application Behaviour, Domain Definition, persistence, or private Logic implementation.

#### API exposes Target-selected capabilities

**Rule:** API publishes every capability selected by Target for external consumers without reducing the external contract to storage CRUD.
**Why:** The external contract serves Target intent rather than exposing the shape of persistence and forcing clients to reconstruct application intent.
**Boundary:** Target selects which capabilities are external. API selects only how those capabilities are represented over its transport.

<br>

### Architecture

#### API preserves one structured Architecture

**Rule:** API contains one Application Bootstrap file, one Core directory, one Routers directory, one Services directory, one configuration file, and one Documentation file. Routers and Services contain one corresponding file per applicable domain area. The names are configurable through API Preferences while these responsibilities and ownership locations remain fixed.
**Why:** A stable structure keeps process composition, transport, coordination, shared internals, configuration, and documentation independently understandable.
**Boundary:** Additional private API files belong to Core or the domain directory that owns them; they do not create another public layer or a second Application Bootstrap.

<br>

### Application Bootstrap

#### Application Bootstrap owns API composition

**Rule:** Application Bootstrap creates the selected framework application, loads validated API configuration, registers Router modules, installs middleware and exception handlers, wires authentication, configures lifecycle hooks, and exposes the configured entrypoint. It contains composition and wiring only.
**Why:** One composition root makes the running application readable in one place instead of assembling it through scattered side effects.
**Boundary:** Application Bootstrap contains no route, Transport Schema, domain-specific operation logic, or application Behaviour. Runtime values come from API configuration or Platform Bindings.

<br>

### Core

#### Core contains shared private API capabilities only

**Rule:** A file shared across API domain areas and owned by no one Router or Service belongs in Core. Core remains private, defines no route, and contains no application Behaviour or persistence implementation.
**Why:** Shared API mechanics need one internal home without becoming a public layer or being copied across domains.
**Boundary:** A domain-specific transport concern remains with its Router, and domain-specific API coordination remains with its Service.

<br>

### Routers

#### Router owns the transport boundary

**Rule:** Router owns routes, transport inputs and outputs, Transport Schemas, parameters, headers, Request Context, transport validation, authentication dependencies, status and error mapping, response serialization, and machine-readable contract metadata. Router delegates to API Service and contains no application Behaviour.
**Why:** Confining the protocol to Router keeps everything behind it transport-independent.
**Boundary:** Router imports no private Logic implementation and calls neither Logic Interface nor Database directly.

#### Transport validation does not replace Behaviour validation

**Rule:** Router validates transport shape and rejects malformed requests before invoking Service. Logic validates resulting state, authorization, and application Behaviour; a valid request shape never implies a permitted operation.
**Why:** Shape and meaning are separate checks owned by different boundaries.
**Boundary:** API may enforce its published transport bounds but never copies a Logic rule into Router.

#### Credentials never leave the API boundary

**Rule:** Credential values may be accepted only by operations that require them and are excluded from responses, errors, diagnostics, logs, examples, and recorded output.
**Why:** A credential exposed through any secondary output path is permanently compromised.
**Boundary:** API may pass a required credential inward through the authorized Logic capability but never returns, records, or renders it.

#### Declared results and failures are mapped safely

**Rule:** Router maps each Logic capability's declared result or expected failure to the public contract without assuming a common Logic wrapper. Unexpected failures become safe generic responses with a non-secret request identifier; internal exceptions and persistence details never cross the boundary.
**Why:** Consumers need stable public outcomes without learning internal implementation or failure details.
**Boundary:** An unexpected failure remains a failure and is never reshaped into a successful response.

#### Identity and authorization remain separate

**Rule:** When authentication is enabled, API establishes validated requester identity in Request Context. Logic decides authorization for application Behaviour.
**Why:** Knowing who is asking and deciding what they may do are separate responsibilities.
**Boundary:** Transport validity and authenticated identity never imply permission.

#### Queries are bounded and explicit

**Rule:** List, filtering, ordering, and pagination parameters are explicitly allowlisted, bounded, and stable. API parameters never become direct storage commands.
**Why:** Unbounded or storage-shaped inputs let an external caller control internal load and query construction.
**Boundary:** API bounds its public contract; Logic and Database decide how a valid bounded request is fulfilled.

<br>

### Services

#### API Service mediates between Router and Logic

**Rule:** API Service receives transport-independent input from Router, prepares the call required by the selected Logic capability, and returns that capability's declared result. It selects the required Service Interface from Logic Interface and uses only capabilities that Interface publishes.
**Why:** A mediating layer keeps Router free of application coordination and Logic free of transport concepts.
**Boundary:** API Service imports no Router, framework Request or Response type, status code, middleware, Database Interface, or private Logic implementation and reimplements no authoritative Behaviour.

#### API consumes Logic through Logic Interface only

**Rule:** API reaches application Behaviour only through Logic Interface. It never imports a Logic Service implementation, Logic Core, Model, Database, or Storage Service directly.
**Why:** One public dependency keeps API replaceable and lets Logic change behind its own boundary.
**Boundary:** API may own Transport Schemas and mappings required by its external contract without redefining a Domain Definition or Logic capability.

<br>

### Configuration

#### Runtime configuration remains external and private

**Rule:** API declares and validates every required runtime configuration value before readiness. Platform supplies runtime values and secret references; values are never hard-coded as application meaning or written back into API Preferences.
**Why:** An explicit configuration contract fails clearly before service instead of unpredictably during a request.
**Boundary:** API owns the contract and validation, while Platform owns value delivery and runtime operation.

<br>

### Documentation

#### API documentation describes the external contract only

**Rule:** API documentation addresses an external consumer with access only to the published boundary. It covers every operation, purpose, accepted request, returned response, expected failures, authentication, applicable query controls, and runnable examples.
**Why:** A consumer must be able to use the API without knowing which Logic Service, Database mechanism, or framework serves it.
**Boundary:** Documentation never makes Logic, Database, framework, or private API details consumer dependencies.

#### API owns one consistent external contract

**Rule:** Human documentation, machine-readable contract, and implemented routes describe the same operations, schemas, versions, authentication, and approved outcomes.
**Why:** A contract that differs from the running boundary causes consumers to build against behavior that does not exist.
**Boundary:** API describes its own external representation; the meaning behind a capability remains owned by Logic.

<br>

### Lifecycle

#### API lifecycle is observable

**Rule:** API distinguishes health from readiness, validates required configuration and dependencies before readiness, and shuts down within the Platform-provided deadline.
**Why:** Operators need to distinguish a live process from one ready to serve and need bounded shutdown behavior.
**Boundary:** API reports and observes its own condition; Platform decides what to do with those signals and supplies the deadline.

<br>

### Verification

#### API verification covers the boundary

**Rule:** Verification covers route contracts, Transport Schemas, declared outcomes, credential exclusion, lifecycle, Request Context, and consistency between the machine-readable contract and running routes.
**Why:** The boundary is what external consumers actually rely on.
**Boundary:** API verification does not replace Logic Behaviour verification or Database persistence verification.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**API is an independent executable**

- **Must** — Own the API process, transport, serialization, versioning, and external contract.
- **Never** — Own authoritative Behaviour, Domain Definitions, persistence, or Logic internals.

**API exposes Target-selected capabilities**

- **Must** — Publish every capability Target selects for external consumers.
- **Never** — Reduce the external contract to storage CRUD.

### Architecture

**API preserves one structured Architecture**

- **Must** — Keep one Bootstrap file, Core, Routers, Services, configuration, and Documentation in their configured locations.
- **Never** — Create a second public layer or Bootstrap through an additional private file.

### Application Bootstrap

**Application Bootstrap owns API composition**

- **Must** — Compose and wire the running API in one Application Bootstrap.
- **Never** — Put routes, Transport Schemas, domain operations, or application Behaviour in Bootstrap.

### Core

**Core contains shared private API capabilities only**

- **Must** — Keep shared non-domain API mechanics in private Core.
- **Never** — Define routes, application Behaviour, or persistence in Core.

### Routers

**Router owns the transport boundary**

- **Must** — Keep transport routes, schemas, validation, identity, statuses, serialization, and contract metadata in Router.
- **Never** — Call Logic or Database directly or put application Behaviour in Router.

**Transport validation does not replace Behaviour validation**

- **Must** — Validate transport shape at Router and leave application validity to Logic.
- **Never** — Treat a well-formed request as automatically permitted.

**Credentials never leave the API boundary**

- **Never** — Return, record, log, diagnose, or document a credential value.

**Declared results and failures are mapped safely**

- **Must** — Map declared Logic results and failures without assuming a common wrapper and map unexpected failures to safe generic responses.
- **Never** — Expose internal exceptions or persistence details or reshape a failure as success.

**Identity and authorization remain separate**

- **Must** — Establish validated identity in Request Context when authentication is enabled.
- **Never** — Decide application authorization at the transport boundary.

**Queries are bounded and explicit**

- **Must** — Allowlist and bound public list, filter, order, and pagination parameters.
- **Never** — Turn an API parameter into a direct storage command.

### Services

**API Service mediates between Router and Logic**

- **Must** — Use the selected capability published through Logic Interface and return its declared result to Router.
- **Never** — Import transport concepts, Database, or private Logic implementation into API Service or reimplement Behaviour there.

**API consumes Logic through Logic Interface only**

- **Must** — Reach application Behaviour only through Logic Interface.
- **Never** — Import Logic internals, Model, Database, or Storage Service directly.

### Configuration

**Runtime configuration remains external and private**

- **Must** — Declare and validate required runtime configuration before readiness.
- **Never** — Hard-code runtime values as application meaning or write resolved values into Preferences.

### Documentation

**API documentation describes the external contract only**

- **Must** — Document every external operation, input, response, failure, authentication rule, query control, and runnable example.
- **Never** — Expose internal Logic, Database, framework, or API details as consumer dependencies.

**API owns one consistent external contract**

- **Must** — Keep documentation, machine-readable contract, and running routes consistent.
- **Never** — Describe internal meaning as part of API's external representation.

### Lifecycle

**API lifecycle is observable**

- **Must** — Distinguish health from readiness, validate dependencies before readiness, and honor Platform's shutdown deadline.

### Verification

**API verification covers the boundary**

- **Must** — Verify routes, schemas, outcomes, credential exclusion, lifecycle, Request Context, and contract consistency.
- **Never** — Treat API verification as a substitute for Logic or Database verification.
