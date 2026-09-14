# Backend Principles

Backend is the independent executable Component that implements the current Target's application Behaviour and publishes the API Interface through which external consumers reach that Behaviour. Its reusable architecture keeps Logic at the center and separates shared Model meaning, persistence, and external communication through explicit boundaries.

These Principles are Target- and technology-independent. A concrete Backend changes when Target Behaviour changes, while its ownership and dependency boundaries remain stable.

## Terms

- **Model Interface** — the Backend boundary through which its internal parts consume the Model Public Interface.
- **Database Interface** — the Backend boundary through which Logic consumes the Database Public Interface.
- **Logic** — the Backend part that owns application Behaviour and operation-dependent rules.
- **API Interface** — the external Backend boundary that receives requests and publishes results.
- **Logic Foundation** — the shared Logic unit that supplies standard Model operations without duplicating them in every Model Logic unit.
- **Model Logic** — one distinct Logic unit for operations and Behaviour centered on one shared Model.
- **Use Case Logic** — a Logic unit that coordinates Behaviour spanning multiple Models or supporting services.
- **Behaviour** — what the application does and the application-context rules under which it does it.
- **Application Outcome** — an explicit successful or expected unsuccessful result produced by Logic independently of transport and persistence representations.
- **Request Context** — validated, non-secret identity and tracing information carried through one request.

## Relationships

- **Consumes Target** — receives Target-specific Behaviour, Model-operation intent, integrations, and externally required capabilities.
- **Consumes Model** — receives shared definitions, validation, relationships, constraints, and Credential markers through Model Interface.
- **Consumes Database** — receives generic persistence operations and transaction capability through Database Interface.
- **Consumes Development** — receives its Component Profile, technical items, Connections, and applicable cross-cutting capabilities.
- **Consumes Platform** — receives environment-specific Runtime Bindings through its selected Launch Item.
- **Consumed through Development-defined Connections** — publishes its API Interface without duplicating consumer identity or internal consumer behaviour.

Backend-owned configurable Behaviour and internal layout conventions belong to Backend Preferences. Concrete language, framework, package, version, Package Management, and quality-tool selections belong to Development Preferences. Runtime values and launch mechanisms belong to Platform.

Every statement here is mandatory. A Preference or implementation choice can never override a Principle, and a Target may only add stricter rules, never looser ones.

<br>

## 1. Backend architecture remains stable across Targets and technologies

**Rule:** Backend Principles define reusable responsibilities and dependency directions independent of any Target, language, framework, protocol, package manager, database engine, provider, or deployment topology. A concrete Backend implements the current Target's Behaviour without changing those architectural boundaries.

**Why:** Target Behaviour and technical choices can evolve without redefining Backend ownership.

**Boundary:** Target changes may require Backend implementation changes. Independence applies to this architecture standard, not to the Behaviour implemented by a concrete Backend.

<br>

## 2. Backend has four explicit internal parts

**Rule:** Backend contains API Interface, Logic, Model Interface, and Database Interface as four explicit parts rather than a forced linear layer chain. API Interface invokes Behaviour only through Logic and may consume public Model types through Model Interface. Logic consumes Model through Model Interface and persistence through Database Interface. Database is reachable only through Database Interface.

**Why:** An explicit dependency graph preserves each boundary without inventing a false ordering between peer interfaces.

**Boundary:** Package identity and root path come from Backend's Component Profile in Development Preferences. No internal part becomes a competing Backend package, and no path outside this graph is inferred.

<br>

## 3. Logic owns application Behaviour

**Rule:** Logic implements what the application does and enforces operation- or application-context conditions. It validates the resulting domain state through Model Interface, selects which related persistence operations form one unit, and requests that unit through Database Interface.

**Why:** Behaviour independent of transport and storage remains valid when either realization changes.

**Boundary:** Logic never depends on transport representations, persistence internals, physical storage, or transaction mechanisms. It does not assume a Database transaction covers external services.

<br>

## 4. Standard Model operations come from one Logic Foundation

**Rule:** Every shared Model has one distinct Model Logic file. Each Model Logic receives the standard operations selected by Backend Preferences from one Logic Foundation and implements only additional Model-specific Behaviour. An operation is exposed only when the Model and Target support it.

The standard operation vocabulary is create, get-by-identifier, list, update, delete, enable, and disable. Enable and disable are available only for a Model that declares `is_active`. Delete means actual removal and is available only when the Target explicitly permits deletion.

**Why:** Shared operations remain consistent without repeated CRUD implementations, while every Model retains a clear extension point.

**Boundary:** Logic Foundation contains no Model-specific Behaviour. Its concrete reuse mechanism, name, and file layout belong to Backend Preferences.

<br>

## 5. Use Case Logic owns cross-Model Behaviour

**Rule:** Behaviour spanning multiple Models or supporting services belongs to a distinct Use Case Logic unit inside Logic. It coordinates the required Model Logic units and selects transaction boundaries without forcing the Behaviour into an unrelated Model Logic unit.

**Why:** Multi-Model workflows remain cohesive and do not distort single-Model ownership.

**Boundary:** Use Case Logic is not a fifth Backend part, does not bypass Model Interface or Database Interface, and does not absorb Behaviour that belongs cleanly to one Model Logic unit.

<br>

## 6. Database Interface is Backend's only route to persistence

**Rule:** Database Interface translates persistence requests from Logic into calls to Database's Public Interface and returns logical results. It carries related operation groups through one resolved Database Instance's transaction boundary without independently committing their members.

**Why:** One persistence boundary keeps Database replaceable and prevents hidden data access.

**Boundary:** Database Interface contains no application Behaviour and never owns or exposes an engine, connection, mapping, schema, migration, commit, rollback, or cleanup mechanism. API Interface and Logic never bypass it to access Database.

<br>

## 7. API Interface is the only external Behaviour boundary

**Rule:** API Interface receives external requests, validates transport shape, obtains applicable public Model types through Model Interface, invokes Logic, and maps Application Outcomes to approved external responses. It owns request decoding, external schema realization, response serialization, API versioning, and transport-level outcome mapping.

**Why:** A thin external boundary keeps application Behaviour independent of communication details.

**Boundary:** API Interface contains no application Behaviour and never accesses Database directly. It may use Model types and derive transport-only input or output schemas where shapes differ, but never creates a competing Domain Definition or treats valid transport shape as a valid resulting domain state.

<br>

## 8. Model Interface is Backend's route to shared Model meaning

**Rule:** Model Interface imports the authoritative definitions exposed by Model's Public Interface and makes the required public types available to Logic and API Interface. API Interface may use them for input, output, schema, and serialization needs; Logic uses them for domain meaning and validation.

**Why:** One Model boundary prevents Backend parts from copying or redefining the domain.

**Boundary:** Model Interface contains no application, persistence, or transport Behaviour and never exposes private Model implementation. Access to Model types never authorizes API Interface to bypass Logic for an operation.

<br>

## 9. API Interface exposes Target capabilities, not only generic operations

**Rule:** Logic implements every Backend-targeted capability required by the Target, and API Interface exposes each capability intended for external consumers. The public API is never limited to generic Model operations when Target Behaviour requires more.

**Why:** Backend exists to implement application Behaviour, not merely persistence access.

**Boundary:** Capability resolution does not itself select a framework, protocol, endpoint path, method, name, or file layout. Ownership of each configurable choice remains with its declared source.

<br>

## 10. API Interface owns its machine-readable contract

**Rule:** When enabled by Backend Preferences, API Interface publishes and keeps current a machine-readable description of its operations, input shapes, output shapes, versions, and relevant outcomes.

**Why:** The boundary publishing the external contract is responsible for describing it accurately.

**Boundary:** README documentation does not replace the API contract, and the API contract does not restate Backend Principles.

<br>

## 11. Credential fields are write-only at API Interface

**Rule:** A Field marked as a Credential by Model is accepted only by input operations that require it. Its metadata may appear as write-only input documentation, but its value is excluded from every response, example, error, diagnostic, trace, log, or recorded output.

**Why:** Preventing every outbound representation closes common disclosure paths.

**Boundary:** Backend reads Credential meaning from Model and never infers it from a Field name or redefines Database's at-rest protection. Documentation uses non-secret placeholders only.

<br>

## 12. Error handling preserves application meaning without leaking internals

**Rule:** Logic represents expected failures as explicit Application Outcomes. API Interface maps those outcomes to its external contract and converts unexpected failures into safe generic responses with a Request Context reference. Internal exceptions, stack traces, persistence details, and secrets never cross the API boundary.

**Why:** Stable outcomes keep consumers independent of implementation failures while preserving diagnostic traceability.

**Boundary:** API Interface never passes through raw framework, supporting-service, or Database errors. Error mapping never hides a successful or expected domain outcome.

<br>

## 13. Authentication and authorization have separate owners

**Rule:** When Authentication applies, API Interface validates or receives the requester identity and establishes a Request Context. Logic decides whether that identity is authorized for an operation. Database persists required facts but never decides application authorization.

**Why:** Identity establishment and business permission decisions occur at the boundaries with the necessary context.

**Boundary:** Authentication technology is selected outside Backend Principles. Authorization is never inferred from transport validity or delegated to persistence.

<br>

## 14. Lists are bounded and query capabilities are explicit

**Rule:** Every list operation applies the pagination policy selected by Backend Preferences. Filtering and sorting accept only explicitly supported Fields and preserve authorization, Model meaning, and stable result ordering.

**Why:** Bounded predictable queries protect availability and make client navigation reliable.

**Boundary:** API query parameters never become direct storage commands, and consumers cannot select private Fields or persistence expressions.

<br>

## 15. Retries and repeated writes are controlled

**Rule:** Every external or persistence interaction has a finite timeout. Automatic retry is bounded and permitted only when the operation is safe or idempotent. Target-selected sensitive write operations use an idempotency identity whose result is recorded atomically so a repeated request does not repeat the effect.

**Why:** Controlled repetition prevents transient failures from becoming duplicated business effects or exhausted resources.

**Boundary:** Backend never retries indefinitely, assumes a non-idempotent operation is safe, or reimplements Database-owned transaction and conflict mechanisms.

<br>

## 16. Supporting services remain behind explicit interfaces

**Rule:** Logic consumes only the supporting services and cross-cutting capabilities selected by Development, through explicit interfaces and only where Behaviour requires them.

**Why:** Optional capabilities remain replaceable and do not couple unrelated Logic units.

**Boundary:** A supporting service never becomes a mandatory Backend part or bypasses Model Interface, Database Interface, or API Interface.

<br>

## 17. Runtime configuration preserves ownership and secrecy

**Rule:** Backend defines and validates the contract of the Runtime Configuration it requires. Platform supplies environment-specific Runtime Bindings. Required values are validated before readiness, and private values remain absent from source, Preferences, documentation, errors, and observability output.

**Why:** One validated contract allows environments to change without changing Backend code or exposing secrets.

**Boundary:** Backend does not own launch mechanisms or environment-specific values, and Platform does not redefine Backend configuration meaning.

<br>

## 18. Startup, readiness, and shutdown are explicit

**Rule:** Backend distinguishes process health from readiness. It reports readiness only after required configuration and dependencies are usable, stops accepting new work during shutdown, and allows active work to complete or be cancelled within the Platform-provided shutdown boundary.

**Why:** Explicit lifecycle signals prevent traffic from reaching an unready or terminating application.

**Boundary:** Health and readiness reveal no secrets or private connection details. Database owns cleanup of its resources, while Platform owns process signals and launch deadlines.

<br>

## 19. Observability correlates operations without exposing data

**Rule:** Every request carries a Request Context with a non-secret request identifier. Backend records applicable operational events and safe error context using that identifier, and propagates it to supporting services when supported.

**Why:** Correlation makes distributed investigation possible without embedding user data in identifiers.

**Boundary:** A request identifier contains no Credential, personal data, authorization decision, or other sensitive meaning. Observability never changes an Application Outcome.

<br>

## 20. Rate limits preserve the correct ownership boundary

**Rule:** Platform owns infrastructure request-rate enforcement. Logic owns Target-defined business quotas and eligibility limits. API Interface maps either outcome to the public contract, while Database only persists facts needed by Logic.

**Why:** Network protection and business policy require different context and evolve independently.

**Boundary:** Database never becomes the application permission authority, and Platform never defines a business quota.

<br>

## 21. Backend verification covers every boundary

**Rule:** Backend verification includes isolated Logic tests, Model Interface and Database Interface contract tests, API contract and outcome tests, enabled security capability tests, transaction and idempotency behaviour, and consistency between the machine-readable API description and the implemented API.

**Why:** Boundary-focused verification detects drift without coupling every test to a live external system.

**Boundary:** Unit tests do not require a live Database or external service. Test doubles preserve the applicable public contract and never redefine it.

<br>

## 22. Backend exposes one minimal Public Interface

**Rule:** External consumers reach Backend Behaviour only through API Interface. Platform starts Backend only through its official executable entry point, and verification uses only the supported application construction surface. Internal Logic units, adapters, Runtime Configuration values, and private resources remain private.

**Why:** A minimal public surface allows internal organization to change without creating hidden consumers.

**Boundary:** No Component imports Backend internals without a declared Development Connection and an explicitly published contract.

<br>

## 23. Backend decisions preserve meaning and boundaries before convenience

**Rule:** When more than one realization is valid, decisions preserve, in order: Target Behaviour and Model meaning; Logic ownership and the four Backend parts; declared Public Interfaces and Connections; complete resulting-state validation; transaction and Credential protections; applicable Preferences; and the simplest maintainable realization.

**Why:** A stable priority order prevents local convenience from weakening architecture.

**Boundary:** This order resolves only choices left open by higher authorities and never expands scope or weakens another Component's ownership.

<br>

## At a Glance

- **Must** — keep Backend Principles stable while concrete Backend implementation follows the current Target. *(1)*
- **Must** — preserve the explicit dependency graph among API Interface, Logic, Model Interface, and Database Interface. *(2)*
- **Never** — access Database outside Database Interface or execute API operations outside Logic. *(2, 6–8)*
- **Must** — keep application Behaviour and operation-dependent validation in Logic. *(3)*
- **Must** — give every shared Model one Model Logic file backed by the shared Logic Foundation. *(4)*
- **Must** — expose create, get-by-identifier, list, update, delete, enable, and disable only where supported. *(4)*
- **Never** — duplicate standard operations or place Model-specific Behaviour in Logic Foundation. *(4)*
- **Must** — place cross-Model workflows in Use Case Logic within Logic. *(5)*
- **Must** — let API Interface use public Model types without creating competing Domain Definitions. *(7–8)*
- **Must** — expose all externally required Target Behaviour and keep the machine-readable API contract current. *(9–10)*
- **Never** — expose a Credential value through any outbound or recorded surface. *(11)*
- **Must** — represent expected failures explicitly and prevent implementation details from crossing API Interface. *(12)*
- **Must** — establish identity at API Interface and decide application authorization in Logic when Authentication applies. *(13)*
- **Must** — keep list operations bounded and filtering and sorting allowlisted. *(14)*
- **Must** — apply finite timeouts, bounded safe retries, and Target-selected idempotency. *(15)*
- **Must** — consume optional supporting services through explicit interfaces. *(16)*
- **Must** — validate Backend configuration while receiving environment values from Platform. *(17)*
- **Must** — distinguish health, readiness, startup, and controlled shutdown. *(18)*
- **Must** — correlate safe operational records through a non-secret request identifier. *(19)*
- **Must** — keep infrastructure rate limits in Platform and business quotas in Logic. *(20)*
- **Must** — verify Logic, interfaces, API outcomes, security, transactions, idempotency, and API-description consistency. *(21)*
- **Must** — expose only API Interface, the official executable entry point, and supported construction surface. *(22)*
- **Must** — preserve Target meaning and Component boundaries before implementation convenience. *(23)*
