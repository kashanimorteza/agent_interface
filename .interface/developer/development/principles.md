# Development Principles

Development is the Component that defines the project's layered software architecture and the way its independent application layers are composed into one system. It is what makes a set of separate layers into a project: it fixes how boundaries are drawn, how they may talk to each other, and how shared capabilities are agreed on. It is an implementation-independent standard and contains no project-specific technology, provider, topology, or execution capability.

The application architecture separates Model, Database, Backend, and Frontend responsibilities: Model supplies the shared domain representation as an independent package, and the remaining layers own persistence, application behaviour, and presentation behind their declared interfaces.

## Terms

- **Layer** — one independent application boundary owning its implementation, rules, configuration, and provided interfaces.
- **Package** — an identifiable collection of implementation resources with a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface.
- **Nested Package** — a package inside another package's boundary, with its own responsibility and interface but sharing its parent's installation and runtime where applicable.
- **Declared Interface** — the surface a provider publishes for consumers, whether an import surface, network API, command, or user interface.
- **Connection** — a directed dependency from a consumer to a provider through exactly one declared interface.
- **Runtime Configuration** — the settings and secrets each layer owns within its own boundary.
- **Cross-cutting Capability** — a capability that may affect more than one layer, such as testing, logging, error handling, or authentication.

## Relationships

- **Consumes Model, Database, Backend, and Frontend** — their declared responsibilities and public interfaces, referenced when recording composition rather than redefined.
- **Consumed by Model, Database, Backend, and Frontend** — the common package standard and the cross-cutting capability decisions.

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

## 4. Development records composition, not internal implementation

**Rule:** Development identifies the participating application layers, their public responsibilities and interfaces, and the connections between them. It also defines the common package standard and records package identities, parent relationships, ownership, and integration boundaries.

**Why:** Composition is the one view no single layer can hold, and it is the only thing Development needs to own in order to make the layers work as one system.

**Boundary:** Internal technologies, third-party dependencies, detailed source layout, domain-model implementation, API implementation, user-interface implementation, and persistence implementation remain owned by their respective layers. The package map references those owning definitions rather than independently redefining their technology choices, operations, or domain meaning.

<br>

## 5. The architecture remains project-independent

**Rule:** Development defines a reusable layered standard.

**Why:** A standard that survives its first project is what makes the same architecture usable for the next one.

**Boundary:** Project-specific choices populate that standard but never change its separation of ownership, interface-only communication, or explicit connections.

<br>

## 6. Cross-cutting capabilities are coordinated by Development

**Rule:** Capabilities that may affect more than one application layer are coordinated by Development rather than owned as an isolated default by Model, Backend, Frontend, or Database. Examples include testing, logging, error handling, and authentication. Development records whether each capability is enabled, which layers it applies to, and the shared integration expectations that keep those layers compatible.

**Why:** A capability that several layers must agree on becomes incompatible the moment each layer decides it alone.

**Boundary:** Each affected layer still owns its internal implementation and consumes the capability through an explicit boundary.

<br>

## 7. A package is an encapsulated implementation boundary

**Rule:** A package is an identifiable collection of implementation resources with a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface. This definition is independent of a programming language or package manager. A package may be an importable library, a runnable application, or a nested module supported by its implementation technology. Package identity follows responsibility.

**Why:** Nested packages may share their parent's installation, dependency management, and runtime while preserving their own logical boundaries, so the standard describes a boundary rather than a distribution mechanism.

**Boundary:** A package's internal details remain private to that boundary. Being a package does not require public registry publication, a separate process, or an independently installable distribution. Naming conventions and prefixes are supplied by Development Preferences and resolved consistently with the selected ecosystem. A generic name does not imply that the package's implementation or domain data is reusable across unrelated projects.

<br>

## 8. Package interfaces define how consumers use a boundary

**Rule:** Each package explicitly identifies what it exposes and what it consumes. Its public interface may be an import surface, network API, command, user interface, or another appropriate mechanism. A package with no external consumer records that fact instead of inventing an interface.

**Why:** Stating the intended surface is what turns a collection of resources into something another boundary can safely depend on.

**Boundary:** Consumers use only the interface intended for them; they do not depend on private files or implementation details. A nested package's interface is available only to its declared consumers within the permitted boundary. Nesting alone does not expose its internals to consumers of the parent; the parent explicitly provides or delegates any capabilities it makes available outside itself. The owning architecture still determines permitted dependency directions.

<br>

## 9. Every package documents its use

**Rule:** Each package, including architectural subpackages, carries its own public `DOCUMENTATION.md` at the package boundary: what the package is for, where its boundaries lie, what its public interface offers, what it depends on, how it is configured, how it is installed and started when that applies, and how it is used in practice. A nested package may rely on its parent's `DOCUMENTATION.md` for shared setup rather than duplicating it.

**Why:** That description is what lets a consumer use the package without inspecting its implementation.

**Boundary:** The description distinguishes supported public operations from internal details and explains how to reach the package's interface documentation. It documents configuration by name and by non-secret example, and records no credentials or other secret values. It remains consistent with the implemented interface. Component documentation never substitutes for, reads, rewrites, or derives from a repository-root README; its location and required sections are resolved through Development Preferences.

<br>

## At a Glance

- **Must** — every application layer and architectural sublayer is a package owning its implementation, rules, configuration, and interfaces *(1)*
- **Never** — a layer depends on how another layer is implemented *(1)*
- **Never** — ordinary files, classes, or functions automatically become separate packages *(1)*
- **Must** — a consumer reaches another layer only through the interface that layer declares *(2)*
- **Never** — a consumer reads or modifies another layer's internal storage, implementation, configuration, or private resources *(2)*
- **Must** — every dependency between layers is an explicit directed connection through one declared interface *(3)*
- **Never** — hidden coupling, undeclared communication, or duplicated ownership exists in the architecture *(3)*
- **Must** — Development records the layers, their responsibilities and interfaces, and their connections *(4)*
- **Never** — Development redefines the internal technologies, source layout, or domain meaning owned by a layer *(4)*
- **Must** — the layered standard stays reusable across projects *(5)*
- **Never** — project-specific choices change ownership separation, interface-only communication, or explicit connections *(5)*
- **Must** — Development records each cross-cutting capability's enabled state, applicable layers, and shared integration expectations *(6)*
- **Never** — a layer decides a cross-cutting capability alone *(6)*
- **Must** — every package has a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface *(7)*
- **Never** — being a package requires registry publication, a separate process, or an independently installable distribution *(7)*
- **Must** — every package states what it exposes and what it consumes, or records that it has no external consumer *(8)*
- **Never** — nesting alone exposes a package's internals to consumers of its parent *(8)*
- **Must** — every package, including subpackages, carries `DOCUMENTATION.md` at its boundary covering purpose, boundaries, interface, dependencies, configuration, setup, and usage *(9)*
- **Never** — documentation records credentials or other secret values, or drifts from the implemented interface *(9)*
