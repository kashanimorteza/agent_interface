# Backend Principles

Backend is the independent Component that implements application Behaviour and publishes the API Interface through which external consumers reach that Behaviour. It keeps Logic at its center and separates access to shared Model meaning, persistence, and external communication through explicit interfaces.

Backend is independent of any Target, language, framework, protocol, package manager, database engine, provider, or deployment topology. It does not own domain-model meaning, physical persistence, user-interface presentation, runtime provisioning, or cross-layer composition.

## Terms

- **Model Interface** — the Backend boundary through which Logic consumes shared Model definitions and validation.
- **Database Interface** — the Backend boundary through which Logic consumes the public Database interface.
- **Logic** — the Backend layer that implements application Behaviour and Model-specific logic.
- **API Interface** — the Backend boundary through which external consumers invoke Logic and receive results.
- **Model Logic** — one distinct logical unit inside Logic that carries the operations and Behaviour belonging to one shared Model.
- **Behaviour** — what the application does and the application-context rules under which it does it, independent of how it is requested or stored.

## Relationships

- **Consumes Target** — receives Target-specific Behaviour, Model-operation intent, integrations, and externally required capabilities without copying them into this standard.
- **Consumes Model** — receives shared domain definitions, validation, relationships, and Credential markers only through Model Interface.
- **Consumes Database** — receives generic persistence operations, stored-state constraints, and transaction capability only through Database Interface.
- **Consumes Development** — receives package conventions, cross-cutting capabilities, supporting-service scope, and ownership rules for configuration and private secrets.
- **Consumes Platform** — receives runtime Bindings through the selected Launch definition.
- **Consumed by Frontend** — provides the public API Interface through which the user interface reaches application data and capabilities.

Technical choices and defaults belong to Backend Preferences. Implementation applies those choices to the current Target without changing Backend ownership or dependency direction.

Every statement here is mandatory. A Developer Preference or implementation choice can never override a Principle, and a Target may only add stricter rules, never looser ones.

<br>

## 1. Backend architecture is Target- and technology-independent

**Rule:** Backend defines a reusable architecture whose responsibilities and dependency direction remain unchanged across Targets, languages, frameworks, protocols, package managers, database engines, providers, and deployment topologies. Target-specific Behaviour, Model operations, integrations, and externally exposed capabilities remain in the current Target definition, and changing the Target never requires changing these Principles.

**Why:** Stable architectural meaning lets different projects and implementations use the same Backend contract without importing one project's details into another.

**Boundary:** Independence does not prevent Preferences or the Target from selecting concrete technologies and capabilities; those selections realize this architecture without redefining it.

<br>

## 2. Backend has Logic and three boundary interfaces

**Rule:** Backend is one independent package with its own identity, configuration, documented public boundary, and four internal layers: Model Interface, Database Interface, Logic, and API Interface. Logic owns Behaviour, consumes Model only through Model Interface, consumes Database only through Database Interface, and is reached by external consumers only through API Interface.

**Why:** Explicit boundaries let domain access, persistence access, Behaviour, and external communication evolve without collapsing into one another.

**Boundary:** No layer bypasses the layer responsible for the next boundary. Package identity and root path come from Development Principles and never expose an internal layer as an independent competing Backend.

<br>

## 3. Logic owns application Behaviour

**Rule:** Logic implements what the application does and enforces conditions that depend on an operation or application context. It uses Model Interface for shared Model definitions and validation, ensures partial changes are validated against the resulting domain state, communicates with persistence only through Database Interface, and is exposed externally only through API Interface. Logic determines which related persistence operations form one unit and requests that unit through Database Interface.

**Why:** Behaviour expressed independently of transport and storage remains valid when API or Database technology changes.

**Boundary:** Logic never depends on transport protocols, API frameworks, database engines, ORM implementations, physical storage, or transport-specific request and response shapes. It does not implement the Database transaction mechanism, assume a Database transaction covers external services, guarantee stored-state constraints, or import around Model Interface or Database Interface.

<br>

## 4. Every shared Model has one distinct Model Logic unit

**Rule:** Each shared Model has its own separately defined Model Logic unit. Each unit offers the common operations selected by Backend Preferences only where its Model supports them. Shared behavior may be reused through a common base or composition, while Model-specific Behaviour extends only the unit of that Model. An activation operation exists only for a Model that declares the corresponding `is_active` field and passes through that Model Logic and Database Interface.

**Why:** A distinct unit gives every Model a stable place for current and future Behaviour without coupling it to another Model's logic.

**Boundary:** A shared definition or registry never replaces the distinct Model Logic units. A registry may connect or import them but does not define their Behaviour. No operation invents a missing Model capability, and API Interface never substitutes direct persistence for Model Logic.

<br>

## 5. Database Interface is Backend's only route to persistence

**Rule:** Database Interface translates persistence operations requested by Logic into calls to the generic public interface published by Database and translates results back into logical data. When Logic requests one related operation group, Database Interface carries the group through one resolved Database Instance's public transaction boundary and propagates its outcome without committing individual operations independently.

**Why:** One translation boundary keeps persistence access visible and lets Database implementation change without rewriting Logic.

**Boundary:** Database Interface contains no application Behaviour, never decides which operations belong together, and never owns or reaches into an engine, connection, ORM, table, schema, migration, commit, rollback, or cleanup mechanism. It promises no atomicity across Database Instances or external services. Logic and API Interface never bypass it to access Database.

<br>

## 6. API Interface is Logic's only external boundary

**Rule:** API Interface receives external requests, validates their transport-level shape, invokes the corresponding Logic operation, converts logical outcomes into protocol outcomes, and serializes approved results into external responses. It owns communication concerns including request decoding, transport validation, protocol handling, response serialization, and response mapping.

**Why:** A thin external boundary keeps application Behaviour independent of its transport and makes the public contract explicit.

**Boundary:** API Interface contains no application Behaviour, never calls Model Interface, Database Interface, Model, or Database directly, never duplicates Model validation, and never treats valid transport shape as proof of a valid resulting domain state. Framework, version, protocol, and implementation details come from the current Target and Backend Preferences.

<br>

## 7. Model Interface is Backend's only route to shared Model meaning

**Rule:** Model Interface imports and exposes the shared logical Model definitions required by Logic under Model Principles and Preferences. Logic obtains Model types, meaning, and domain validation only through this boundary. Database Interface receives required Model identities and values from Logic, while API Interface derives external data shapes from Logic's contract without creating a second domain definition.

**Why:** One route to shared Model meaning keeps domain definitions consistent across every Backend layer.

**Boundary:** No other Backend layer imports around Model Interface or copies, redefines, or creates a competing representation of Model meaning. Model Interface contains no application Behaviour, persistence behavior, transport behavior, or private Model implementation.

<br>

## 8. API Interface exposes both Model operations and Target Behaviour

**Rule:** Logic implements Backend-targeted Behaviour from the current Target, and API Interface exposes every declared capability that must be available to external consumers. The public API surface includes supported Model operations and is never limited to generic CRUD when the Target declares additional Behaviour.

**Why:** The value of a Backend lies in the Behaviour its Target requires, not merely in storing and retrieving Models.

**Boundary:** Resolving a capability does not itself select endpoint paths, protocol methods, names, file layout, or framework details. Those are implementation decisions governed by the Target and Backend Preferences.

<br>

## 9. API Interface owns its machine-readable contract

**Rule:** API Interface owns and, when enabled by Backend Preferences, publishes the machine-readable description of its available operations, input shapes, output shapes, and relevant outcomes. That description remains consistent with the implemented external contract.

**Why:** The boundary that publishes an external contract is the only layer able to describe that contract accurately as it changes.

**Boundary:** No other Backend layer owns or generates the public API description. Its enablement, format, and realization are technical choices belonging to Backend Preferences.

<br>

## 10. Credential fields are write-only at API Interface

**Rule:** A field marked as a Credential by Model is accepted through API Interface only when an input operation requires it. Its name, type, requiredness, and write-only nature may appear in input schemas and API documentation, but the field is always excluded from responses and response schemas. Actual Credential values never appear in documentation, examples, errors, diagnostics, traces, logs, or recorded outputs.

**Why:** Preventing every outbound representation closes the most common paths through which a Credential can escape its protected boundary.

**Boundary:** Backend reads the Credential marker from Model Interface and never infers it from a field name. Database owns at-rest protection, and Backend never redefines that storage mode. Documentation may use non-secret placeholders only.

<br>

## 11. Logic consumes supporting services through explicit interfaces

**Rule:** Model Logic may coordinate supporting services and cross-cutting capabilities selected by Development, using explicit interfaces and only within the Model Logic units that need them.

**Why:** Target capabilities remain available to Behaviour without forcing every Model Logic unit to depend on every service.

**Boundary:** A supporting service never becomes a fifth mandatory Backend layer, bypasses Model Interface, Database Interface, or API Interface, or gains a broader application scope merely because one Model Logic unit consumes it.

<br>

## 13. Backend decisions preserve meaning and boundaries before convenience

**Rule:** When more than one Backend realization is valid, decisions preserve, in order: Model meaning and Target Behaviour; Logic ownership and all three interface boundaries; independence from transport and persistence implementation; the public Database interface; complete resulting-state validation; transaction grouping selected by Logic and realized by Database; Credential protection; compatible Backend Preferences; and the simplest maintainable implementation.

**Why:** A stable priority order prevents local framework convenience from weakening architectural correctness.

**Boundary:** This order resolves choices that remain open. It never overrides an explicit Target decision, weakens another Component's authority, or authorizes a role to act outside its scope.

<br>

## 14. A required Agent Skill is a Backend completion gate

**Rule:** When the resolved Backend Preference for a selected technology declares an associated Agent Skill with `requirement: required`, Development verifies that exact capability is currently discoverable and usable, invokes it through its synchronized Runtime mechanism before making implementation decisions for that technology, reads its complete primary instructions and every referenced guidance source applicable to the work, and checks every instruction as applied or explicitly not applicable with a reason. Review independently resolves and uses the same current Skill when judging the resulting implementation. Backend work involving that technology is complete only when every applicable Skill instruction is satisfied by observable evidence.

**Why:** Naming a Skill without requiring its complete application proves neither that it influenced the implementation nor that the result follows its current standard.

**Boundary:** A Preference that declares no associated Skill creates no Skill requirement, and no operation invents one. An unavailable required Skill blocks only the affected work and is reported as an Agent capability gap. Skill guidance never selects the technology, expands scope, or overrides Target intent, Backend Principles, resolved Preferences, Plan obligations, Role, or Permission; a conflict follows the shared decision policy.

<br>

## At a Glance

- **Must** — keep Backend architecture independent of Targets and implementation technologies while leaving Target-specific meaning in Target *(1)*
- **Must** — implement Backend as one package containing Logic, Model Interface, Database Interface, and API Interface *(2)*
- **Never** — let a Backend layer bypass the boundary responsible for the next interaction *(2)*
- **Must** — keep application Behaviour and operation-dependent validation in Logic *(3)*
- **Must** — let Logic select related persistence operations as one unit and request that unit through Database Interface *(3)*
- **Never** — couple Logic to transport, persistence implementation, or Database transaction mechanics *(3)*
- **Must** — give every shared Model one distinct Model Logic unit and expose only operations its Model supports *(4)*
- **Never** — let shared helpers, registries, API Interface, or unsupported operations replace Model-specific Logic *(4)*
- **Must** — route all Backend persistence through Database Interface and Database's public transaction boundary *(5)*
- **Never** — put Behaviour or Database internals inside Database Interface or promise unsupported cross-boundary atomicity *(5)*
- **Must** — keep API Interface responsible only for external communication, transport validation, Logic invocation, and response mapping *(6)*
- **Never** — put Behaviour, Model access, Database access, or duplicated domain validation in API Interface *(6)*
- **Must** — route all shared Model meaning and validation used by Logic through Model Interface *(7)*
- **Never** — copy Model meaning or place Behaviour, persistence, transport, or private Model implementation in Model Interface *(7)*
- **Must** — expose supported Model operations and every externally required Target Behaviour through API Interface *(8)*
- **Never** — treat capability resolution as a fixed endpoint, method, name, layout, or framework decision *(8)*
- **Must** — let API Interface own and keep current its enabled machine-readable public contract *(9)*
- **Never** — let another Backend layer own the API description *(9)*
- **Must** — accept Model-marked Credential fields as write-only inputs and exclude them from every output surface *(10)*
- **Never** — infer Credential fields by name, expose their values, or redefine Database's at-rest protection *(10)*
- **Must** — consume selected supporting services through explicit interfaces only where their Behaviour is needed *(11)*
- **Never** — turn a supporting service into a mandatory Backend layer or an interface bypass *(11)*
- **Must** — apply the Backend decision order only to choices left open by higher authorities *(13)*
- **Never** — let framework convenience override Target meaning, Component ownership, or Backend boundaries *(13)*
- **Must** — invoke and completely apply every applicable instruction from a required Agent Skill before completing work on its selected Backend technology *(14)*
- **Must** — make Review independently verify required Agent Skill compliance against observable implementation evidence *(14)*
- **Never** — invent a Skill requirement for a Preference that declares none or let Skill guidance override an owning authority *(14)*
