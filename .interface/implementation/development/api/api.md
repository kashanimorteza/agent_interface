# API Definition

API is the Development Component that owns the external communication boundary and publishes application capabilities through a transport.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Layering](#layering)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

API is an independent executable Implementation Component. It owns the external communication boundary, starts its own application process, validates transport data, invokes Logic, and publishes the resulting application capabilities. API has no application Behaviour of its own.

These Principles are transport- and framework-independent. Development Preferences select the concrete API technology and package; Platform supplies the runtime binding.

### Purpose

A running application has to be reachable from outside itself, and being reachable is a job with its own demands: a process that stays up, a protocol to speak, payloads to parse and validate, statuses to return, credentials to check, errors to render without leaking. None of those demands is about what the application does — they are about how it is reached.

API exists to absorb them so nothing behind it has to. It is the Component that starts a process and speaks a transport, and it does one thing with what it receives: turn it into a call on Logic's Public Interface, and turn the answer back into a response. Because that is all it does, the same application can be reached a second way — another protocol, a command-line entry point — by adding a consumer rather than by rewriting anything.

When the boundary is not owned by one Component, transport leaks inwards: request shapes become domain shapes, status codes become the vocabulary of failure, and the application can only ever be reached the one way it was first built for. Worse, the checks that protect the boundary — validation, authorization, bounded queries — end up half here and half deeper in, which is how something eventually goes unchecked.

### How It Works

A request arrives at the Router, which owns the whole protocol surface: the route, the method, the parameters, the headers. It is validated against the Transport Schema for that endpoint — shape, types, required values, bounds — and rejected there if it does not conform, before anything behind the boundary is touched. When authentication is enabled, identity is established at the same edge and carried in the Request Context.

What survives becomes a call inwards. Router hands the operation to Service, which prepares what the boundary needs to hand over and calls Logic through its Public Interface. API adds no reasoning of its own — it does not decide what may be done, in what order, or under which conditions.

Logic answers with an Application Outcome: the result, or one of the expected failures that Operation declares. Router maps that back onto the transport — a response shaped by API's own schema, a status that corresponds to the outcome, and for an unexpected failure a safe generic response carrying a non-secret request identifier. Credentials and internal detail stop at the boundary in both directions.

Around all of it sits the process: the Application Bootstrap composes and wires it, the machine-readable contract describes exactly what the running routes accept and return, and the lifecycle — health, readiness, shutdown within the Platform deadline — is observable, because a boundary whose state nobody can see is a boundary nobody can operate.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **API Interface** — the public boundary that receives requests and publishes responses.
- **Logic Interface** — the public library surface through which API invokes application Behaviour.
- **Transport Schema** — an input or output shape owned by API when it differs from a Domain Definition.
- **Application Outcome** — a logical success or expected failure returned by Logic.
- **Request Context** — validated non-secret identity and tracing information for one request.
- **Application Bootstrap** — the API Composition Root that creates the selected API framework application and wires its public transport components.
- **Router** — the API layer that owns the selected transport boundary, including routes, transport inputs and outputs, transport validation, and transport error mapping.
- **Service** — the API layer between Router and Logic Interface that exposes API operations and coordinates calls without knowing transport or framework details.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
API
├── Application Bootstrap     ← the Composition Root that starts and wires the process
├── Router                    ← the selected transport boundary: routes, transport shapes, error mapping
└── Service                   ← the layer between Router and Logic, free of transport
```

**Application Bootstrap** creates the application of the selected framework and wires the public transport parts together: it registers Routers, installs middleware and exception handlers, and binds authentication. It owns wiring and nothing else — no route, no transport shape, no application decision.

**Router** owns the selected transport boundary. It declares routes, validates the transport data arriving on them, produces the transport data leaving on them, and maps an Application Outcome to its transport form. It never reasons about the domain and never reaches past Service.

**Service** sits between Router and the Logic Interface. It exposes what API offers as operations and coordinates the calls that fulfil one, without knowing which transport carried the request or which framework is in use. It holds no application Behaviour of its own; that belongs to Logic.

Dependencies run in that order — Bootstrap wires them, Router calls Service, Service calls Logic — and no part reaches past the one that owns the next boundary.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Logic** — invokes application Behaviour through Logic's Public Interface, and reaches the application no other way.
- **Consumes Development** — uses its Component Profile, shared rules, technical items, Connections, and Platform Reference.
- **Consumes Platform** — receives the runtime values its configuration contract requires, and the shutdown deadline it observes.
- **Consumed by external consumers** — publishes the Target's selected capabilities over a transport, to any caller the project authorizes.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

API owns the external transport boundary, its composition, validation, mapping, and lifecycle contract. Development supplies the Component's technical selections and Platform supplies runtime bindings; Logic owns application Behaviour.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

API Definition Principles are mandatory. API Preferences provide configurable boundary defaults and conventions, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### API documentation describes the external contract only

**Rule:** API documentation is written for an external consumer with access to the published boundary and nothing behind it. It covers every published operation, its purpose, accepted shape, return value, failures, authentication, and applicable paging, filtering, ordering, and runnable examples.

**Why:** A reader must be able to use every published operation correctly without knowing which Logic Operation, Service, Database mechanism, or framework served it.

**Boundary:** This Principle governs the external API contract; it does not publish internal Logic, persistence, or framework details.

<br>

### API is an independent executable
**Rule:** API owns its process, startup, routing, transport schemas, serialization, versioning, and machine-readable contract. Logic remains a library consumed through its Public Interface.

**Why:** A boundary that owns its own process can be started, stopped, scaled, and replaced without disturbing the library behind it, and a Logic that owns no process can be reused by a consumer that is not this one.

**Boundary:** API does not own application Behaviour, persistence, or Logic internals.

<br>

### Application Bootstrap owns API composition
**Rule:** The Application Bootstrap is the API Composition Root. It creates the selected API framework application, applies API-level configuration, registers Router modules, installs transport middleware and exception handlers, wires Authentication dependencies, configures lifecycle hooks, and exposes the configured application through the selected entrypoint. It contains composition and wiring only; it does not contain business Behaviour or domain-specific operation logic.

**Why:** One composition root means the shape of the running application is readable in a single place, instead of being assembled from side effects scattered through modules.

**Boundary:** Bootstrap configuration is not a Router or Service responsibility. Runtime values such as host, port, deployment path, allowed origins, and secret references come from Platform Bindings or the API runtime configuration contract and are never hard-coded as application meaning.

<br>

### Router owns the transport boundary
**Rule:** Router owns the selected transport's routes, inputs, parameters, headers where applicable, Request handling, transport-level validation, Authentication dependencies, status and error mapping, response handling, and machine-readable contract metadata. Router delegates API operations to Service and contains no application Behaviour.

**Why:** Confining the protocol to one layer is what lets everything behind it stay transport-independent, and what makes a second transport an addition rather than a rewrite.

**Boundary:** Router imports no private Logic implementation and places no business rules in transport handlers.

<br>

### Service mediates API operations
**Rule:** Service is the API layer between Router and Logic Interface. It exposes API operations and domain-specific API actions, prepares or transforms data at the API boundary, and coordinates calls to Logic through its Public Interface. Service may orchestrate an API-level interaction but does not reimplement authoritative Business Behaviour.

**Why:** A mediating layer keeps Router free of application concerns and Logic free of transport ones, so neither leaks into the other as endpoints multiply.

**Boundary:** Service never imports the selected transport framework, Router modules, Request or Response types, transport status codes, Middleware, or other transport-specific concepts. Business rules remain in Logic.

<br>

### API consumes Logic through its Public Interface
**Rule:** API consumes Behaviour only through Logic's Public Interface.

**Why:** Consuming Logic through its published surface keeps API replaceable and keeps Logic free to change behind its boundary.

**Boundary:** API may hold a Transport Schema of its own where the wire shape differs from the public operation shape.

<br>

### API exposes Target capabilities
**Rule:** API publishes every capability selected for external consumers by the Target without reducing the contract to storage CRUD.

**Why:** The external contract exists to serve what the Target intends, not to expose the shape of storage; reducing it to storage operations forces every consumer to reassemble the intent itself.

**Boundary:** Which capabilities are published is resolved from the Target. API decides how a capability is exposed over the transport, never whether the application has it.

<br>

### API owns the external contract
**Rule:** API maintains the machine-readable description of operations, input and output shapes, versions, and approved outcomes. Documentation and contract remain consistent with implemented routes.

**Why:** A contract that drifts from the running API is worse than none: consumers build against a description that no longer holds and discover the difference in production.

**Boundary:** API owns the description of its own boundary only. The meaning behind an operation belongs to Logic.

<br>

### Transport validation does not replace domain validation
**Rule:** API validates transport shape and delegates resulting-state and Behaviour validation to Logic. A valid request shape is not itself a valid domain operation.

**Why:** Shape and meaning are different checks. A request can be perfectly formed and still be an operation that must not happen, and only the owner of Behaviour can tell.

**Boundary:** API rejects what is malformed at its own edge and never absorbs domain rules to do so; Logic remains the single judge of whether an operation is permitted.

<br>

### Credentials never leave the API boundary
**Rule:** Credential values may be accepted only by required input operations and are excluded from responses, errors, diagnostics, logs, examples, and recorded output.

**Why:** Credentials leak through the paths nobody inspects — an error body, a log line, an example in the generated contract — and one leak is permanent.

**Boundary:** API may accept a credential where an operation requires one and pass it inwards through the authorized route; it never returns, records, or renders one.

<br>

### Outcomes and failures are mapped safely
**Rule:** API maps explicit Application Outcomes to the public contract. Unexpected failures become safe generic responses with a non-secret request identifier; internal exceptions and persistence details never cross the boundary.

**Why:** A consumer needs to distinguish an expected failure from a fault, and neither needs to learn anything about what failed internally.

**Boundary:** The outcomes API may map are the ones Logic declares. An unexpected failure is reported as itself, never reshaped into a successful response.

<br>

### Identity and authorization remain separate
**Rule:** When enabled, API establishes validated requester identity in Request Context. Logic decides authorization for Behaviour; transport validity never implies permission.

**Why:** Knowing who is asking and deciding what they may do are separate questions; answering both at the boundary puts application rules where they cannot see application state.

**Boundary:** API establishes and carries identity; Logic decides authorization. A validated request is evidence of identity alone.

<br>

### Queries are bounded and explicit
**Rule:** List, filtering, and sorting parameters are explicitly allowlisted, bounded, and stable. API parameters never become direct storage commands.

**Why:** Unbounded queries let a caller shape the load on the system, and parameters passed through to storage let a caller shape the query itself.

**Boundary:** API bounds and allowlists what its own contract accepts; how a bounded query is then satisfied belongs to the Components behind it.

<br>

### Lifecycle is observable
**Rule:** API distinguishes health from readiness, validates required configuration and dependencies before readiness, and shuts down within the Platform-provided deadline.

**Why:** An operator needs to know the difference between a process that is alive and one that is ready to serve, and a shutdown that ignores its deadline loses work in flight.

**Boundary:** API reports its own condition; Platform decides what to do with that report and supplies the deadline it observes.

<br>

### API verification covers the boundary
**Rule:** Verification covers route contracts, schemas, outcomes, credential exclusion, lifecycle, request context, and consistency between the machine-readable description and the running API.

**Why:** The boundary is where the outside world meets the system, so what is verified there is what a consumer can actually rely on.

**Boundary:** Verification here covers the boundary alone. Behaviour is verified by Logic and persistence by Database; this verification never substitutes for either.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**API documentation describes the external contract only**

- **Must** — document every published operation, its inputs, outputs, failures, authentication, and applicable query controls with runnable examples.
- **Never** — expose Logic, Service, Database, or framework implementation details as consumer dependencies.

**API is an independent executable**

- **Must** — Own the API process, its startup, routing, schemas, serialization, versioning, and machine-readable contract.
- **Never** — Own application Behaviour, persistence, or Logic internals.

**Application Bootstrap owns API composition**

- **Must** — Compose the running application in one Application Bootstrap that wires and configures only.
- **Never** — Put business Behaviour in composition, or hard-code runtime values as application meaning.

**Router owns the transport boundary**

- **Must** — Keep routes, HTTP inputs and outputs, transport validation, status codes, and error mapping inside Router.
- **Never** — Access Database from Router, import private Logic implementation, or put business rules in handlers.

**Service mediates API operations**

- **Must** — Let Service mediate between Router and Logic, preparing data at the boundary and coordinating calls.
- **Never** — Import transport types or framework concepts into Service, or reimplement Behaviour there.

**API consumes Logic through its Public Interface**

- **Must** — Consume Behaviour only through Logic's Public Interface.

**API exposes Target capabilities**

- **Must** — Publish every capability the Target selects for external consumers.
- **Never** — Reduce the external contract to storage operations.

**API owns the external contract**

- **Must** — Keep the machine-readable contract consistent with the implemented routes.

**Transport validation does not replace domain validation**

- **Must** — Validate transport shape at the boundary and leave state and Behaviour validation to Logic.
- **Never** — Treat a valid request shape as a valid domain operation.

**Credentials never leave the API boundary**

- **Never** — Return, record, or render a credential value anywhere, including errors, logs, diagnostics, and examples.

**Outcomes and failures are mapped safely**

- **Must** — Map declared Application Outcomes to the public contract, and unexpected failures to safe generic responses with a non-secret request identifier.
- **Never** — Let internal exceptions or persistence details cross the boundary.

**Identity and authorization remain separate**

- **Must** — Establish validated identity in Request Context when authentication is enabled.
- **Never** — Decide authorization at the transport boundary or treat transport validity as permission.

**Queries are bounded and explicit**

- **Must** — Allowlist and bound every list, filter, and sort parameter.
- **Never** — Let an API parameter become a direct storage command.

**Lifecycle is observable**

- **Must** — Distinguish health from readiness, validate configuration and dependencies before readiness, and shut down within the Platform deadline.

**API verification covers the boundary**

- **Must** — Verify route contracts, schemas, outcomes, credential exclusion, lifecycle, request context, and contract-to-runtime consistency.
