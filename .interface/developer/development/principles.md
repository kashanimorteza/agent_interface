# Development Standard

> **Authoritative Standard for the Development Component**
>
> This document is the authoritative standard for the project's Development Component.
>
> Every implementer, reviewer, or automation that creates, changes, validates, or reasons about application composition MUST read and follow this document before making changes.
>
> **Principles override preferences, framework defaults, convenience, and implementation choices.**
>
> A project may add stricter rules, but it must not weaken the rules defined here.

---

# 1. Purpose

Development defines the project's layered software architecture and the way its independent application layers are composed into one system. It fixes how boundaries are drawn, how those boundaries may communicate, and how shared capabilities are coordinated.

Development identifies the participating application layers, their public responsibilities and interfaces, and the directed connections between them. It also defines the common package standard and records package identities, parent relationships, ownership, and integration boundaries.

The application architecture separates Model, Database, Backend, and Frontend responsibilities:

- Model supplies the shared domain representation as an independent package;
- Database owns persistence behind its declared interface;
- Backend owns application behaviour behind its declared interface; and
- Frontend owns presentation behind its declared interface.

Development composes these responsibilities. It does not absorb or redefine them.

---

# Project Independence

Development is a reusable, implementation-independent standard across Targets. It contains no project-specific technology, provider, topology, or execution capability.

Project-specific choices populate this standard but MUST NOT change:

- separation of ownership;
- interface-only communication;
- explicit directed connections; or
- the independence of each package boundary.

Changing the Target MUST NOT require changing this standard. The package map for a Target references the definitions owned by its Components instead of copying their technologies, operations, or domain meaning into Development.

---

# Architectural Foundation

Development treats application architecture as a set of encapsulated package boundaries connected through declared interfaces.

Each layer owns its implementation, rules, runtime configuration, and provided interfaces. Architectural sublayers follow the same rule recursively as nested packages within their parent's boundary. A connection is directed from a consumer to a provider through exactly one declared interface.

This foundation is independent of programming language, package manager, deployment topology, process model, and communication mechanism. An interface may be an import surface, network API, command, user interface, or another mechanism appropriate to its owning Component.

---

# Authority by Concern

| Concern | Authoritative source |
| --- | --- |
| Target-specific layers, requirements, and explicit project choices | Current Target definition |
| Layer ownership, package boundaries, interface-only communication, connections, and cross-cutting coordination | This Development Standard |
| Package conventions and defaults for cross-cutting capabilities | Development Preferences |
| A Component's internal technology, source layout, domain meaning, and public interface | That Component's Principles, Preferences, and Target definition |
| Runtime delivery and execution topology | The owning Platform and Launch definitions |

Development records composition without taking authority away from the source that owns each concern. A Preference can never override a Principle, and a Target may only add stricter rules, never looser ones.

---

# 2. Core Principles

## 2.1 Terms

- **Layer** — one independent application boundary owning its implementation, rules, configuration, and provided interfaces.
- **Package** — an identifiable collection of implementation resources with a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface.
- **Nested Package** — a package inside another package's boundary, with its own responsibility and interface but sharing its parent's installation and runtime where applicable.
- **Declared Interface** — the surface a provider publishes for consumers, whether an import surface, network API, command, user interface, or another appropriate mechanism.
- **Connection** — a directed dependency from a consumer to a provider through exactly one declared interface.
- **Runtime Configuration** — the settings and secrets each layer owns within its own boundary.
- **Cross-cutting Capability** — a capability that may affect more than one layer, such as testing, logging, error handling, or authentication.

## 2.2 Relationships

- **Consumes Model, Database, Backend, and Frontend** — their declared responsibilities and public interfaces, referenced when recording composition rather than redefined.
- **Consumed by Model, Database, Backend, and Frontend** — the common package standard and the cross-cutting capability decisions.

Technical choices and defaults belong to Development Preferences. Development implementation applies those choices to the current Target definition.

## 2.3 Every layer is an independent boundary

**Rule:** Each application layer owns its internal implementation, rules, runtime configuration, and provided interfaces. Every application layer is organized as a package. The same principle applies recursively to each architectural sublayer: a sublayer is a nested package within its parent's boundary, with its own cohesive responsibility and public interface.

**Why:** A layer can evolve or be replaced without requiring consumers to change while its declared interface remains compatible.

**Boundary:** Another layer may depend on what the layer provides, but never on how it is implemented. Ordinary files, classes, and functions do not automatically become separate packages.

<br>

## 2.4 Communication happens only through declared interfaces

**Rule:** A consumer communicates with another layer only through the interface that the provider declares for that purpose. Shared domain representations are consumed through the Model package interface, Database access happens through the Database interface, and Backend capabilities are consumed through the Backend interface. The same rule applies to every current or future layer.

**Why:** A declared interface is a promise the provider can preserve; anything reached around it is a dependency the provider never agreed to maintain.

**Boundary:** A consumer never reads or modifies another layer's internal storage, implementation, runtime configuration, or private resources directly.

<br>

## 2.5 Connections are explicit and directed

**Rule:** Every dependency between layers is represented as a directed connection from a consumer to a provider through exactly one declared interface.

**Why:** A system whose dependencies are all written down can be reasoned about, reordered, and replaced one boundary at a time.

**Boundary:** Hidden coupling, undeclared communication, and duplicated ownership are not part of the architecture. A connection describes integration between two boundaries; it does not redefine either boundary or invent an interface that its provider does not own.

<br>

## 2.6 Development records composition, not internal implementation

**Rule:** Development records the participating layers, their public responsibilities and interfaces, their package identities and parent relationships, and the connections between them.

**Why:** Composition is the one view no individual layer can own, and it is the only view Development needs in order to make independent layers work as one system.

**Boundary:** Internal technologies, third-party dependencies, detailed source layout, domain-model implementation, API implementation, user-interface implementation, and persistence implementation remain owned by their respective Components. Development references those owning definitions instead of independently redefining their technology choices, operations, or domain meaning.

<br>

## 2.7 Cross-cutting capabilities are coordinated by Development

**Rule:** Capabilities that may affect more than one application layer are coordinated by Development rather than owned as an isolated default by Model, Database, Backend, or Frontend. Examples include testing, logging, error handling, and authentication. Development records whether each capability is enabled, which layers it applies to, and the shared integration expectations that keep those layers compatible.

**Why:** A capability that several layers must agree on becomes incompatible when each layer decides it alone.

**Boundary:** Each affected layer still owns its internal implementation and consumes the capability through an explicit boundary. A single layer does not acquire ownership of a cross-layer decision merely by implementing part of it.

<br>

## 2.8 A package is an encapsulated implementation boundary

**Rule:** A package is an identifiable collection of implementation resources with a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface. This definition is independent of programming language and package manager. A package may be an importable library, a runnable application, or a nested module supported by its implementation technology. Package identity follows responsibility.

**Why:** Nested packages may share their parent's installation, dependency management, and runtime while preserving their own logical boundaries. The standard therefore defines an encapsulation boundary, not a distribution mechanism.

**Boundary:** A package's internal details remain private. Being a package does not require public registry publication, a separate process, or an independently installable distribution. Naming conventions and prefixes come from Development Preferences and are resolved consistently with the selected ecosystem. A generic name does not imply that the package's implementation or domain data is reusable across unrelated Targets.

<br>

## 2.9 Package interfaces define how consumers use a boundary

**Rule:** Each package explicitly identifies what it exposes and what it consumes. Its public interface may be an import surface, network API, command, user interface, or another appropriate mechanism. A package with no external consumer records that fact instead of inventing an interface.

**Why:** Stating the intended surface is what turns a collection of implementation resources into a boundary another Component can safely depend on.

**Boundary:** Consumers use only the interface intended for them; they do not depend on private files or implementation details. A nested package's interface is available only to its declared consumers within the permitted boundary. Nesting alone does not expose its internals to consumers of the parent. The parent explicitly provides or delegates any capability made available outside itself, and the owning architecture determines permitted dependency directions.

---

# 3. Documentation Standard

Every package, including every architectural subpackage, MUST carry its own public `DOCUMENTATION.md` at the package boundary.

The `DOCUMENTATION.md` MUST explain:

- the package's purpose and boundaries;
- the public interface it offers;
- its dependencies;
- its non-secret configuration;
- installation and startup when applicable; and
- practical usage examples.

A nested package MAY reference its parent's `DOCUMENTATION.md` for shared setup instead of duplicating that material, but it MUST document its own interface and usage locally.

Documentation MUST distinguish supported public operations from internal details and explain how to reach the package's interface documentation. Configuration MUST be documented by name and non-secret example; credentials and other secret values MUST NOT be recorded.

The documentation MUST remain consistent with the implemented interface and MUST let a consumer use the package without inspecting its implementation. Component documentation never substitutes for, reads, rewrites, or derives from a repository-root README. Its location and required sections are resolved through Development Preferences.

---

# 4. Decision Order

When more than one composition or package design is possible, prefer in this order:

1. Preserve the owning Component's responsibility and meaning.
2. Preserve independent package boundaries.
3. Communicate only through provider-declared interfaces.
4. Make every dependency explicit and directed.
5. Keep ownership unique and avoid duplicated responsibility.
6. Preserve compatibility for every enabled cross-cutting capability.
7. Apply the conventions selected by Development Preferences.
8. Prefer the simplest maintainable composition.

---

# 5. At a Glance

## MUST

- Organize every application layer and architectural sublayer as a package that owns its implementation, rules, runtime configuration, and interfaces.
- Route every cross-boundary interaction through an interface declared by the provider.
- Record every dependency as an explicit directed connection through exactly one declared interface.
- Record participating layers, public responsibilities and interfaces, package identities, parent relationships, ownership, and integration boundaries.
- Keep the layered standard reusable across Targets.
- Record each cross-cutting capability's enabled state, applicable layers, and shared integration expectations.
- Give every package a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface.
- State what every package exposes and consumes, or record that it has no external consumer.
- Provide `DOCUMENTATION.md` at every package boundary with purpose, boundaries, interface, dependencies, configuration, applicable setup, and usage.

## SHOULD

- Let package identity follow responsibility.
- Let nested packages share parent installation, dependency management, and runtime where applicable.
- Adapt package naming to the selected ecosystem while keeping the logical role recognizable.
- Reference an owning Component's definition instead of duplicating its internal decisions.

## NEVER

- Depend on how another layer is implemented or access its internal storage, implementation, configuration, or private resources.
- Treat an ordinary file, class, or function as a separate package merely because it exists.
- Introduce hidden coupling, undeclared communication, duplicated ownership, or an interface the provider does not own.
- Let Development redefine a Component's internal technology, source layout, operations, implementation, or domain meaning.
- Let project-specific choices weaken ownership separation, interface-only communication, or explicit connections.
- Let one layer decide a cross-cutting capability alone.
- Require registry publication, a separate process, or an independently installable distribution merely because a boundary is a package.
- Assume nesting exposes a package's internals to consumers of its parent.
- Record credentials or other secret values in documentation, allow documentation to drift from the interface, or use a repository-root README as its source or substitute.

---

# 6. Final Rule

Development defines **how independent application Components are composed without surrendering their ownership**.

When a Development decision is not explicitly covered, preserve each Component's meaning and boundary, communicate only through declared interfaces, make dependencies and ownership explicit, coordinate shared capabilities at the composition level, and apply Development Preferences without redefining an owning Component's internal decisions.

When convenience conflicts with these Development Principles, **the Development Principles win**.
