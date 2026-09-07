# Development Principles

Development is the Component that defines the project's layered software architecture and the way its independent application layers are composed into one runnable system. It is what makes a set of separate layers into a project: it fixes how boundaries are drawn, how they may talk to each other, how shared capabilities are agreed on, and how the whole thing is configured and brought online. It is an implementation-independent standard and contains no project-specific technology, provider, topology, or execution capability.

The application architecture separates Model, Database, Backend, Frontend, and Platform responsibilities: Model supplies the shared domain representation as an independent package, and Platform is the composition layer that connects the application layers, supplies their operating environment, brings the complete system online, and delivers it to its destination.

## Terms

- **Layer** — one independent application boundary owning its implementation, rules, configuration, and provided interfaces.
- **Package** — an identifiable collection of implementation resources with a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface.
- **Nested Package** — a package inside another package's boundary, with its own responsibility and interface but sharing its parent's installation and runtime where applicable.
- **Declared Interface** — the surface a provider publishes for consumers, whether an import surface, network API, command, or user interface.
- **Connection** — a directed dependency from a consumer to a provider through exactly one declared interface.
- **Platform** — the composition layer owning the operating environment, coordination, startup, networking, runtime configuration delivery, and deployment; also the resolved place the target project runs, such as a host, a container, or a cloud.
- **Runtime Configuration** — the settings a user or environment may change, owned centrally by Platform and delivered to each layer as its own section.
- **Cross-cutting Capability** — a capability that may affect more than one layer, such as testing, logging, error handling, or authentication.

## Relationships

- **Consumes Model, Database, Backend, and Frontend** — their declared responsibilities and public interfaces, referenced when recording composition rather than redefined.
- **Consumed by Model, Database, Backend, and Frontend** — the common package standard, the cross-cutting capability decisions, and the centralized runtime configuration each layer receives.

Technical choices and defaults belong to Development Preferences. Development implementation applies those choices to the current project definition.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every layer is an independent boundary

**Rule:** Each application layer owns its internal implementation, rules, configuration, and provided interfaces. Every application layer is organized as a package, and the same principle applies recursively to each architectural sublayer it contains: a sublayer is a package within its parent's boundary, with its own responsibility and public interface.

**Why:** A layer can evolve or be replaced without requiring consumers to change while its declared interface remains compatible.

**Boundary:** Another layer may depend on what that layer provides, but never on how it is implemented. Ordinary files, classes, and functions do not automatically become separate packages.

<br>

## 2. Communication happens only through declared interfaces

**Rule:** A consumer communicates with another layer only through the interface that the provider declares for that purpose. Shared domain representations are consumed through the Model package interface, Database access happens through the Database interface, and Backend capabilities are consumed through the Backend interface. The same rule applies to every current or future layer.

**Why:** An interface is a promise the provider can keep; anything reached around it is a dependency the provider never agreed to preserve.

**Boundary:** A consumer never reads or modifies another layer's internal storage, implementation, configuration, or private resources directly.

<br>

## 3. Connections are explicit

**Rule:** Every dependency between layers is represented as a directed connection from a consumer to a provider through one declared interface.

**Why:** A system whose dependencies are all written down can be reasoned about, reordered, and replaced one boundary at a time.

**Boundary:** Hidden coupling, undeclared communication, and duplicated ownership are not part of the architecture. A connection describes integration between two boundaries; it does not redefine either boundary or invent an interface that its provider does not own.

<br>

## 4. Platform composes the complete system

**Rule:** Platform owns cross-layer composition: the operating environment, process or service coordination, startup, networking, runtime configuration delivery, and deployment of the complete project. Platform connects layers through their declared interfaces.

**Why:** With composition owned in one place, the system may run on any suitable operating system, local environment, server, container platform, cloud platform, or future destination without changing the ownership of another layer.

**Boundary:** Platform never absorbs the application, presentation, or persistence responsibilities of the layers it composes.

<br>

## 5. Platform owns centralized runtime configuration

**Rule:** Configuration that a user or operating environment may change remains outside package implementation. Platform owns the centralized configuration boundary: it loads and validates the current settings, resolves environment-specific values, and supplies each application layer with the section that belongs to it. Each layer receives only its own settings and the declared references needed for its connections. Cross-layer choices, such as the Database Instance assigned to Backend, are composition settings owned by Platform rather than constants embedded in either package. Secret values remain outside general configuration and source-controlled package files; central configuration may carry a reference to a secret, while its value is resolved from the authorized runtime source and delivered only to the boundary that owns it.

**Why:** Settings that cross layers belong to whoever composes them, otherwise each package encodes assumptions about the others and the system can only be reconfigured by editing code.

**Boundary:** A package never reads another package's configuration section, discovers another package's internals, or changes source code merely to select a different compatible provider or Instance. The concrete configuration files, formats, section names, override precedence, and delivery mechanism are technical choices resolved from the project definition and Development Preferences, then implemented by Platform.

<br>

## 6. Development records composition, not internal implementation

**Rule:** Development identifies the participating application layers, their public responsibilities and interfaces, the connections between them, and the Platform configuration that makes the complete project runnable. It also defines the common package standard and records package identities, parent relationships, ownership, and integration boundaries.

**Why:** Composition is the one view no single layer can hold, and it is the only thing Development needs to own in order to make the layers work as one system.

**Boundary:** Internal technologies, third-party dependencies, detailed source layout, domain-model implementation, API implementation, user-interface implementation, and persistence implementation remain owned by their respective layers. The package map references those owning definitions rather than independently redefining their technology choices, operations, or domain meaning.

<br>

## 7. The architecture remains project-independent

**Rule:** Development defines a reusable layered standard.

**Why:** A standard that survives its first project is what makes the same architecture usable for the next one.

**Boundary:** Project-specific choices populate that standard but never change its separation of ownership, interface-only communication, explicit connections, or Platform responsibility.

<br>

## 8. Cross-cutting capabilities are coordinated by Development

**Rule:** Capabilities that may affect more than one application layer are coordinated by Development rather than owned as an isolated default by Model, Backend, Frontend, or Database. Examples include testing, logging, error handling, and authentication. Development records whether each capability is enabled, which layers it applies to, and the shared integration expectations that keep those layers compatible.

**Why:** A capability that several layers must agree on becomes incompatible the moment each layer decides it alone.

**Boundary:** Each affected layer still owns its internal implementation and consumes the capability through an explicit boundary.

<br>

## 9. A package is an encapsulated implementation boundary

**Rule:** A package is an identifiable collection of implementation resources with a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface. This definition is independent of a programming language or package manager. A package may be an importable library, a runnable application, or a nested module supported by its implementation technology. Package identity follows responsibility.

**Why:** Nested packages may share their parent's installation, dependency management, and runtime while preserving their own logical boundaries, so the standard describes a boundary rather than a distribution mechanism.

**Boundary:** A package's internal details remain private to that boundary. Being a package does not require public registry publication, a separate process, or an independently installable distribution. Naming conventions and prefixes are supplied by Development Preferences and resolved consistently with the selected ecosystem. A generic name does not imply that the package's implementation or domain data is reusable across unrelated projects.

<br>

## 10. Package interfaces define how consumers use a boundary

**Rule:** Each package explicitly identifies what it exposes and what it consumes. Its public interface may be an import surface, network API, command, user interface, or another appropriate mechanism. A package with no external consumer records that fact instead of inventing an interface.

**Why:** Stating the intended surface is what turns a collection of resources into something another boundary can safely depend on.

**Boundary:** Consumers use only the interface intended for them; they do not depend on private files or implementation details. A nested package's interface is available only to its declared consumers within the permitted boundary. Nesting alone does not expose its internals to consumers of the parent; the parent explicitly provides or delegates any capabilities it makes available outside itself. The owning architecture still determines permitted dependency directions.

<br>

## 11. Every package documents its use

**Rule:** Each package, including architectural subpackages, carries its own public description: what the package is for, where its boundaries lie, what its public interface offers, what it depends on, how it is configured, how it is installed and started when that applies, and how it is used in practice. A nested package may rely on its parent's description for shared setup rather than duplicating it.

**Why:** That description is what lets a consumer use the package without inspecting its implementation.

**Boundary:** The description distinguishes supported public operations from internal details and explains how to reach the package's interface documentation. It documents configuration by name and by non-secret example, and records no credentials or other secret values. It remains consistent with the implemented interface. The document that carries it, where it lives, and the sections it contains are technical choices resolved through Development Preferences.

<br>

## 12. Platform is realized with every phase, not after them

**Rule:** Platform has no phase of its own. Each phase that delivers a layer also delivers that layer's part of the composition: its section of the centralized runtime configuration, the process or service that runs it, and its declared connections to the layers already present. The complete system is runnable after every phase, not only after the last.

**Why:** A composition assembled only at the end is assembled against layers that were never run together, and every integration problem surfaces at once at the point where it is most expensive. Composing as each layer arrives keeps the running system one step behind the plan at most.

**Boundary:** This decides when composition happens, not who owns it. Platform still owns the composition and each layer still owns its own implementation; a phase contributes its layer's part under Platform's rules and does not restructure what earlier phases composed. Where the target project runs — a host, a container, a cloud — is a technical choice resolved from the project definition and Development Preferences, and a phase composes for that choice rather than deciding it.

<br>

## At a Glance

- **Must** — every application layer and architectural sublayer is a package owning its implementation, rules, configuration, and interfaces *(1)*
- **Never** — a layer depends on how another layer is implemented *(1)*
- **Never** — ordinary files, classes, or functions automatically become separate packages *(1)*
- **Must** — a consumer reaches another layer only through the interface that layer declares *(2)*
- **Never** — a consumer reads or modifies another layer's internal storage, implementation, configuration, or private resources *(2)*
- **Must** — every dependency between layers is an explicit directed connection through one declared interface *(3)*
- **Never** — hidden coupling, undeclared communication, or duplicated ownership exists in the architecture *(3)*
- **Must** — Platform owns environment, coordination, startup, networking, configuration delivery, and deployment *(4)*
- **Never** — Platform absorbs the application, presentation, or persistence responsibilities of a layer *(4)*
- **Must** — Platform owns central runtime configuration and delivers each layer only its own section and declared references *(5)*
- **Must** — secret values stay outside general configuration and source-controlled files, carried only as references *(5)*
- **Never** — a package reads another package's configuration section or changes source code to select a compatible provider or Instance *(5)*
- **Must** — Development records the layers, their responsibilities and interfaces, their connections, and the Platform configuration *(6)*
- **Never** — Development redefines the internal technologies, source layout, or domain meaning owned by a layer *(6)*
- **Must** — the layered standard stays reusable across projects *(7)*
- **Never** — project-specific choices change ownership separation, interface-only communication, explicit connections, or Platform responsibility *(7)*
- **Must** — Development records each cross-cutting capability's enabled state, applicable layers, and shared integration expectations *(8)*
- **Never** — a layer decides a cross-cutting capability alone *(8)*
- **Must** — every package has a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface *(9)*
- **Never** — being a package requires registry publication, a separate process, or an independently installable distribution *(9)*
- **Must** — every package states what it exposes and what it consumes, or records that it has no external consumer *(10)*
- **Never** — nesting alone exposes a package's internals to consumers of its parent *(10)*
- **Must** — every package, including subpackages, carries a public description covering purpose, boundaries, interface, dependencies, configuration, setup, and usage *(11)*
- **Never** — documentation records credentials or other secret values, or drifts from the implemented interface *(11)*
- **Must** — every phase that delivers a layer also delivers that layer's part of the composition, so the system is runnable after every phase *(12)*
- **Never** — Platform is left to a phase of its own, or a phase restructures what earlier phases composed *(12)*
