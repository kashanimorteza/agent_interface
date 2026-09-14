# API Principles

API is an independent executable Implementation Component. It owns the external communication boundary, starts its own application process, validates transport data, invokes Logic, and publishes the resulting application capabilities. API has no application Behaviour of its own and never accesses Database directly.

These Principles are transport- and framework-independent. Development Preferences selects the concrete API technology, package, and runtime.

## Terms

- **API Interface** — the public boundary that receives requests and publishes responses.
- **Logic Interface** — the public library surface through which API invokes application Behaviour.
- **Transport Schema** — an input or output shape owned by API when it differs from a Domain Definition.
- **Application Outcome** — a logical success or expected failure returned by Logic.
- **Request Context** — validated non-secret identity and tracing information for one request.
- **Application Bootstrap** — the API Composition Root that creates the FastAPI application and wires its public HTTP components.
- **Router** — the API layer that owns the HTTP boundary, including routes, HTTP inputs and outputs, transport validation, and HTTP error mapping.
- **Service** — the API layer between Router and Logic Interface that exposes API operations and coordinates calls without knowing HTTP or FastAPI.

## 1. API is an independent executable

**Rule:** API owns its process, startup, routing, transport schemas, serialization, versioning, and machine-readable contract. Logic remains a library consumed through its Public Interface.

**Boundary:** API does not own application Behaviour, persistence, Model definitions, or Logic internals.

## 2. Application Bootstrap owns API composition

**Rule:** The Application Bootstrap is the API Composition Root. It creates the selected framework application, applies API-level configuration, registers Router modules, installs Middleware and exception handlers, wires Authentication dependencies, configures lifecycle hooks, and exposes the configured application through the selected entrypoint. It contains composition and wiring only; it does not contain business Behaviour or domain-specific operation logic.

**Boundary:** Bootstrap configuration is not a Router or Service responsibility. Runtime values such as host, port, deployment path, allowed origins, and secret references come from Platform Bindings or the API runtime configuration contract and are never hard-coded as application meaning.

## 3. Router owns the HTTP boundary

**Rule:** Router owns URL and route definitions, HTTP methods, path and query parameters, headers, Request handling, HTTP-level validation, Authentication dependencies, HTTP status codes, HTTP error and response mapping, response handling, and OpenAPI metadata. Router delegates API operations to Service and contains no application Behaviour.

**Boundary:** Router never accesses Database directly, imports private Logic implementation, or places business rules in HTTP handlers.

## 4. Service mediates API operations

**Rule:** Service is the API layer between Router and Logic Interface. It exposes API operations and domain-specific API actions, prepares or transforms data at the API boundary, and coordinates calls to Logic through its Public Interface. Service may orchestrate an API-level interaction but does not reimplement authoritative Business Behaviour.

**Boundary:** Service never imports FastAPI, Router modules, Request or Response types, HTTP status codes, Middleware, or other transport-specific concepts. Business rules remain in Logic.

## 5. API consumes explicit Public Interfaces

**Rule:** API consumes Model types through Model's Public Interface for transport schemas and consumes Behaviour only through Logic's Public Interface. It never reaches Database directly.

## 6. API exposes Target capabilities

**Rule:** API publishes every capability selected for external consumers by the Target, including applicable standard Model operations, without reducing the contract to storage CRUD.

## 7. API owns the external contract

**Rule:** API maintains the machine-readable description of operations, input and output shapes, versions, and approved outcomes. Documentation and contract remain consistent with implemented routes.

## 8. Transport validation does not replace domain validation

**Rule:** API validates transport shape and delegates resulting-state and Behaviour validation to Logic. A valid request shape is not itself a valid domain operation.

## 9. Credentials never leave the API boundary

**Rule:** Credential values may be accepted only by required input operations and are excluded from responses, errors, diagnostics, logs, examples, and recorded output.

## 10. Outcomes and failures are mapped safely

**Rule:** API maps explicit Application Outcomes to the public contract. Unexpected failures become safe generic responses with a non-secret request identifier; internal exceptions and persistence details never cross the boundary.

## 11. Identity and authorization remain separate

**Rule:** When enabled, API establishes validated requester identity in Request Context. Logic decides authorization for Behaviour; transport validity never implies permission.

## 12. Queries are bounded and explicit

**Rule:** List, filtering, and sorting parameters are explicitly allowlisted, bounded, and stable. API parameters never become direct storage commands.

## 13. Lifecycle is observable

**Rule:** API distinguishes health from readiness, validates required configuration and dependencies before readiness, and shuts down within the Platform-provided deadline.

## 14. API verification covers the boundary

**Rule:** Verification covers route contracts, schemas, outcomes, credential exclusion, lifecycle, request context, and consistency between the machine-readable description and the running API.
