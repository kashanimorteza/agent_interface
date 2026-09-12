# FastAPI Standard

> **Conditional implementation standard for the Backend API Interface**
>
> This file does not select FastAPI. Backend Preferences selects the API framework. When FastAPI is selected, every implementation, review, and automation that touches the Backend API Interface MUST apply this standard together with Backend Principles, Development Principles and Preferences, and the current Target.
>
> Backend Principles own architecture and boundaries. This file owns only the FastAPI realization of the API Interface. It never moves Model, Database, or Logic responsibilities into FastAPI.

---

# 1. Scope and authority

FastAPI realizes the Backend API Interface: it receives external requests, validates transport shape, invokes Logic, maps outcomes, serializes approved response data, and publishes the machine-readable API contract.

This standard deliberately excludes:

- domain Model definitions and domain validation, which belong to Model and are consumed through Model Interface;
- ORM mappings, engines, sessions, queries, repositories, migrations, and stored-state constraints, which belong to Database;
- application Behaviour and operation-dependent decisions, which belong to Logic;
- package management, general Python style, formatting, linting, and repository-wide quality choices, which belong to Development; and
- runtime provisioning, secret values, deployment topology, and environment delivery, which belong to Platform.

If this file conflicts with Backend Principles, Backend Principles win. An explicit Target choice may make a stricter or different framework-level choice without weakening a Principle.

---

# 2. Selected technical baseline

Use the concrete stable versions resolved from Backend Preferences and the current project rather than hard-coding a version in this file.

When FastAPI is selected:

- use current supported FastAPI APIs;
- use Pydantic v2 APIs for API request and response schemas;
- use `pydantic-settings` only for typed adaptation of non-secret runtime configuration delivered through the owning configuration boundary;
- use the selected Python and isolated environment from Backend and Development Preferences;
- declare dependencies in `pyproject.toml` and preserve the selected lock file; and
- verify version-sensitive behavior against the installed version or current official documentation.

Do not downgrade the selected stack or introduce compatibility layers merely to reproduce an obsolete tutorial.

---

# 3. Application composition

Create the FastAPI application through one explicit application boundary. Prefer an application factory when tests, configuration, lifespan resources, or deployment composition benefit from isolated application instances.

The application boundary MUST:

- construct FastAPI with explicit metadata resolved from the current Target and package configuration;
- register routers intentionally;
- register exception handlers, middleware, dependencies, and lifespan behavior in visible composition code;
- avoid import-time network access, resource acquisition, migration execution, and hidden global initialization; and
- expose the ASGI application through the package's documented public startup boundary.

Router registration and application composition do not own Behaviour. They connect the API Interface to Logic.

---

# 4. Routers and path operations

Use `APIRouter` to group coherent external capabilities. A router is organized by the public API contract or Target capability, not by Database tables or implementation convenience.

Every path operation MUST:

- declare its HTTP method, path, success status, input shape, output shape, and relevant documented failures explicitly;
- remain thin: decode transport input, obtain API-level dependencies, invoke the corresponding Logic operation, and map the result;
- call Logic rather than Model Interface, Database Interface, Model, Database, ORM, engine, session, or repository objects;
- avoid embedding application rules, transaction ownership, or persistence decisions;
- use stable, unique operation identifiers when generated clients or contract stability requires them; and
- avoid duplicate or ambiguous method-and-path combinations.

Paths, methods, names, tags, and versioning come from the current Target and implementation plan. This standard does not invent them.

---

# 5. Request and response schemas

API schemas are transport contracts owned by API Interface. They are not shared domain Models and are never persistence Models.

- Define explicit, purpose-specific input and output schemas where the public contract differs by operation.
- Derive field meaning and credential markers from Model through the declared Backend boundaries; do not create a competing domain definition.
- Use Pydantic v2 APIs such as `ConfigDict`, `model_validate()`, `model_dump()`, `field_validator`, and `model_validator` when their responsibility is transport-level validation or serialization.
- Do not use Pydantic v1 APIs such as `class Config`, `orm_mode`, `parse_obj()`, `.dict()`, or `.json()` in new code.
- Distinguish omitted input from explicit `null` where partial updates require that difference.
- Declare the response type or `response_model` explicitly so FastAPI validates, documents, serializes, and filters output.
- Do not return internal Logic objects accidentally when they expose fields outside the declared response contract.
- A Credential field may appear only in an appropriate input schema, marked write-only in API documentation when supported. It MUST NOT appear in response schemas or response data.

Transport validation confirms the request shape only. Model and Logic remain responsible for their own validation and Behaviour.

---

# 6. Dependency injection

Use FastAPI dependency injection for API-boundary concerns and for supplying Logic through an explicit interface. Prefer `Annotated` aliases for reusable typed dependencies.

Appropriate dependencies include:

- the Logic capability required by a path operation;
- authentication context and transport-level authorization prerequisites;
- request correlation and other API-scoped context;
- typed, non-secret configuration views; and
- bounded resources genuinely owned by the API Interface.

Dependency injection MUST NOT become a route around the Backend architecture:

- do not inject a Database session, engine, repository, or ORM object into a path operation;
- do not inject Model or Database implementations directly into routers;
- do not hide application Behaviour inside dependency functions; and
- do not create mutable singleton request state without an explicit safe lifecycle.

Override dependencies at the composition boundary for focused API tests.

---

# 7. Asynchronous execution

Use `async def` only when the path operation or dependency awaits asynchronous I/O. Use normal `def` for synchronous work that should run through FastAPI's supported execution behavior.

- Never call blocking I/O directly from an async path.
- Never mark code async merely for appearance.
- Preserve cancellation and cleanup across awaited operations.
- Do not create untracked tasks whose failures or lifetime escape application ownership.
- Do not share request-scoped mutable resources concurrently unless their owner explicitly supports it.

Whether Database is synchronous or asynchronous is hidden behind Logic and Database Interface and does not change router ownership.

---

# 8. Lifespan and resources

Use FastAPI's `lifespan` mechanism for application startup and shutdown behavior in new code. Do not introduce deprecated startup/shutdown event patterns when lifespan provides the supported replacement.

Lifespan may initialize and release application-wide resources delivered to or owned by the Backend boundary. It MUST NOT:

- run Database migrations or silently change a production schema;
- read or embed secret values outside the selected configuration boundary;
- perform import-time initialization indirectly;
- make sub-application lifespan assumptions that FastAPI does not guarantee; or
- acquire resources whose lifecycle belongs to Platform or Database without using their declared interface.

Tests that depend on lifespan behavior MUST execute the application lifespan explicitly.

---

# 9. Errors and HTTP outcomes

Logic reports logical outcomes through transport-independent results or exceptions. API Interface maps them centrally and consistently to HTTP outcomes.

- Use FastAPI/Starlette exception handlers for reusable mappings.
- Reserve `HTTPException` for API-boundary conditions; do not spread it through Logic.
- Distinguish client input failures, authentication failures, authorization failures, not-found outcomes, conflicts, rate limits, and unexpected server failures where the public contract requires it.
- Keep error response shapes stable and documented.
- Never silently swallow an unexpected exception.
- Never expose stack traces, private configuration, credentials, persistence internals, or implementation details in an external response.
- Log unexpected failures through the selected logging capability with protected values redacted.

---

# 10. Authentication, authorization, and transport security

Use FastAPI security and dependency mechanisms to extract and validate transport credentials and construct an authenticated request context. Logic owns application authorization decisions that depend on Target Behaviour or domain state.

- Authentication and authorization requirements MUST be explicit and auditable.
- Protected operations MUST fail closed when identity or required authorization context is unavailable.
- Never log authorization headers, cookies, tokens, passwords, private keys, or Credential values.
- Do not place secret values in source, defaults, OpenAPI examples, URLs, or committed environment files.
- Configure CORS explicitly for known consumers; never use permissive credentials with unrestricted origins.
- Trust forwarded headers, hosts, and proxy metadata only under an explicit deployment configuration.

Do not implement cryptography when an established selected library or identity provider owns the capability.

---

# 11. OpenAPI and public documentation

When Backend Preferences enables API documentation, FastAPI's OpenAPI output is part of the public API Interface contract.

- Keep operation metadata, parameters, request bodies, response schemas, status codes, security requirements, and documented failures consistent with behavior.
- Keep operation identifiers stable and unique when consumers rely on generated clients.
- Separate input and output schemas whenever fields or visibility differ.
- Ensure Credential fields are write-only inputs and absent from every response schema.
- Use non-secret, domain-appropriate examples that do not reveal private implementation data.
- Treat an OpenAPI snapshot or equivalent contract check as durable verification when contract drift can regress.
- Configure interactive documentation exposure deliberately for each environment rather than assuming it is always public.

The package `README.md` explains how consumers reach and use the API; OpenAPI describes the machine-readable contract. Neither one replaces the current Target or Backend Principles.

---

# 12. Middleware, background work, and streaming

Add middleware only for cross-request HTTP concerns that genuinely apply across the API surface, such as correlation, observability, compression, or explicit CORS policy. Middleware MUST NOT become a hidden Behaviour or persistence layer.

- Order middleware deliberately and test order-sensitive behavior.
- Keep request bodies and sensitive headers out of logs by default.
- Use FastAPI background tasks only for short, in-process work whose loss on process termination is acceptable.
- Route durable, retryable, scheduled, or distributed work through the supporting service selected by Development and coordinated by Logic.
- For streaming responses, define media type, disconnect/cancellation behavior, failure limits, and resource cleanup explicitly.

---

# 13. Testing and verification

Test Logic independently from FastAPI. Test FastAPI at the API Interface boundary.

The API test suite MUST cover, where applicable:

- application creation and router registration;
- request parsing and transport-level validation;
- invocation of the correct Logic capability;
- success response status, headers, body, and schema;
- each declared logical-outcome-to-HTTP mapping;
- authentication and authorization boundaries;
- Credential exclusion from responses, schemas, logs, and errors;
- dependency overrides and isolation between tests;
- lifespan startup, shutdown, and cleanup;
- async behavior using HTTPX with an ASGI transport when asynchronous tests are required; and
- OpenAPI consistency, unique operation identifiers, and documented response contracts.

Tests MUST NOT require a real Database merely to prove router behavior. Use the Logic boundary to isolate API tests; Database integration is verified by the Database owner and Backend integration tests only where the complete interaction must be proven.

Run the selected Development checks for formatting, linting, typing, tests, package installation, and documentation. A FastAPI implementation is incomplete while any applicable check or public-contract verification fails.

---

# 14. Forbidden patterns

When FastAPI is selected, never:

- place application Behaviour in routers, dependencies, middleware, serializers, or exception handlers;
- call Database, ORM, sessions, repositories, or Model directly from API Interface;
- expose persistence objects as accidental API contracts;
- duplicate Model meaning in transport schemas;
- inject Database infrastructure into path operations;
- use Pydantic v1 or deprecated FastAPI patterns in new code;
- mix blocking I/O into async execution;
- use startup as an implicit migration mechanism;
- return undeclared data and assume serialization will protect it;
- expose Credential or secret values through responses, OpenAPI, examples, errors, logs, or traces;
- add framework abstractions, service/repository layers, or compatibility wrappers mechanically; or
- copy a generic FastAPI project tree when it contradicts Backend's four-layer architecture.

---

# 15. Decision order

When several FastAPI realizations are possible, prefer in this order:

1. Preserve Backend's Model Interface, Database Interface, Logic, and API Interface boundaries.
2. Preserve Target Behaviour and the declared public API contract.
3. Protect credentials and prevent excess response data.
4. Use the current supported FastAPI and Pydantic APIs.
5. Keep routers thin and dependencies explicit.
6. Preserve type safety and testability.
7. Prefer the simplest maintainable realization.
8. Add performance or abstraction complexity only with evidence that it is required.

---

# At a Glance

- **Must** — route every request from API Interface to Logic, never directly to Model or Database.
- **Must** — use explicit Pydantic v2 request and response contracts and filter every response through its declared public shape.
- **Must** — use typed `Annotated` dependencies without turning DI into an architectural bypass.
- **Must** — use lifespan for new startup/shutdown resource handling and keep migrations outside application startup.
- **Must** — map logical outcomes centrally, document the API contract, and test the API independently through the Logic boundary.
- **Never** — place ORM, sessions, repositories, migrations, stored-state constraints, or domain meaning in this FastAPI layer.
- **Never** — expose Credential fields or secret values in outputs or documentation.

---

# Reference basis

This standard adapts the supplied Modern Python + FastAPI engineering rules to the Interface's separate Model, Database, Logic, and API ownership. Version-sensitive framework behavior is checked against the official FastAPI documentation, especially its guidance for lifespan, dependencies with `Annotated`, response models, asynchronous tests, and Pydantic v2 migration.
