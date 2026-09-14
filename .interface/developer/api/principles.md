# API Principles

API is an independent executable Developer Component. It owns the external communication boundary, starts its own application process, validates transport data, invokes Logic, and publishes the resulting application capabilities. API has no application Behaviour of its own and never accesses Database directly.

These Principles are transport- and framework-independent. Development Preferences selects the concrete API technology, package, and runtime.

## Terms

- **API Interface** — the public boundary that receives requests and publishes responses.
- **Logic Interface** — the public library surface through which API invokes application Behaviour.
- **Transport Schema** — an input or output shape owned by API when it differs from a Domain Definition.
- **Application Outcome** — a logical success or expected failure returned by Logic.
- **Request Context** — validated non-secret identity and tracing information for one request.

## 1. API is an independent executable

**Rule:** API owns its process, startup, routing, transport schemas, serialization, versioning, and machine-readable contract. Logic remains a library consumed through its Public Interface.

**Boundary:** API does not own application Behaviour, persistence, Model definitions, or Logic internals.

## 2. API consumes explicit Public Interfaces

**Rule:** API consumes Model types through Model's Public Interface for transport schemas and consumes Behaviour only through Logic's Public Interface. It never reaches Database directly.

## 3. API exposes Target capabilities

**Rule:** API publishes every capability selected for external consumers by the Target, including applicable standard Model operations, without reducing the contract to storage CRUD.

## 4. API owns the external contract

**Rule:** API maintains the machine-readable description of operations, input and output shapes, versions, and approved outcomes. Documentation and contract remain consistent with implemented routes.

## 5. Transport validation does not replace domain validation

**Rule:** API validates transport shape and delegates resulting-state and Behaviour validation to Logic. A valid request shape is not itself a valid domain operation.

## 6. Credentials never leave the API boundary

**Rule:** Credential values may be accepted only by required input operations and are excluded from responses, errors, diagnostics, logs, examples, and recorded output.

## 7. Outcomes and failures are mapped safely

**Rule:** API maps explicit Application Outcomes to the public contract. Unexpected failures become safe generic responses with a non-secret request identifier; internal exceptions and persistence details never cross the boundary.

## 8. Identity and authorization remain separate

**Rule:** When enabled, API establishes validated requester identity in Request Context. Logic decides authorization for Behaviour; transport validity never implies permission.

## 9. Queries are bounded and explicit

**Rule:** List, filtering, and sorting parameters are explicitly allowlisted, bounded, and stable. API parameters never become direct storage commands.

## 10. Lifecycle is observable

**Rule:** API distinguishes health from readiness, validates required configuration and dependencies before readiness, and shuts down within the Platform-provided deadline.

## 11. API verification covers the boundary

**Rule:** Verification covers route contracts, schemas, outcomes, credential exclusion, lifecycle, request context, and consistency between the machine-readable description and the running API.
