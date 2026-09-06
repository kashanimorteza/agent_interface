# Development Principles

Development defines the project's layered software architecture and the way its independent application layers are composed into one runnable system. It is an implementation-independent standard and contains no project-specific technology, provider, topology, or execution capability.

The application architecture separates Model, Database, Backend, Frontend, and Platform responsibilities. Model supplies the shared domain representation as an independent package. Platform is the composition layer that connects the application layers, supplies their operating environment, brings the complete system online, and delivers it to its destination.

Every statement here is mandatory.

<br>

## 1. Every layer is an independent boundary

Each application layer owns its internal implementation, rules, configuration, and provided interfaces. Another layer may depend on what that layer provides, but never on how it is implemented.

Every application layer is organized as a package. The same principle applies recursively to each architectural sublayer it contains: a sublayer is a package within its parent's boundary, with its own responsibility and public interface. Ordinary files, classes, and functions do not automatically become separate packages.

A layer can evolve or be replaced without requiring consumers to change while its declared interface remains compatible.

<br>

## 2. Communication happens only through declared interfaces

A consumer communicates with another layer only through the interface that the provider declares for that purpose. It never reads or modifies another layer's internal storage, implementation, configuration, or private resources directly.

Shared domain representations are consumed through the Model package interface. Database access happens through the Database interface. Backend capabilities are consumed through the Backend interface. The same rule applies to every current or future layer.

<br>

## 3. Connections are explicit

Every dependency between layers is represented as a directed connection from a consumer to a provider through one declared interface. Hidden coupling, undeclared communication, and duplicated ownership are not part of the architecture.

A connection describes integration between two boundaries; it does not redefine either boundary or invent an interface that its provider does not own.

<br>

## 4. Platform composes the complete system

Platform owns cross-layer composition: the operating environment, process or service coordination, startup, networking, runtime configuration delivery, and deployment of the complete project.

Platform connects layers through their declared interfaces and never absorbs their application, presentation, or persistence responsibilities. It may run the system on any suitable operating system, local environment, server, container platform, cloud platform, or future destination without changing the ownership of another layer.

<br>

## 5. Platform owns centralized runtime configuration

Configuration that a user or operating environment may change remains outside package implementation. Platform owns the centralized configuration boundary: it loads and validates the current settings, resolves environment-specific values, and supplies each application layer with the section that belongs to it.

Each layer receives only its own settings and the declared references needed for its connections. A package never reads another package's configuration section, discovers another package's internals, or changes source code merely to select a different compatible provider or Instance. Cross-layer choices, such as the Database Instance assigned to Backend, are composition settings owned by Platform rather than constants embedded in either package.

Secret values remain outside general configuration and source-controlled package files. Central configuration may carry a reference to a secret, while its value is resolved from the authorized runtime source and delivered only to the boundary that owns it.

The concrete configuration files, formats, section names, override precedence, and delivery mechanism are technical choices resolved through Development Preferences and represented in generated Development configuration.

<br>

## 6. Development records composition, not internal implementation

Development identifies the participating application layers, their public responsibilities and interfaces, the connections between them, and the Platform configuration that makes the complete project runnable. It also defines the common package standard and records package identities, parent relationships, ownership, and integration boundaries.

Internal technologies, third-party dependencies, detailed source layout, domain-model implementation, API implementation, user-interface implementation, and persistence implementation remain owned by their respective layers. The package map references those owning definitions rather than independently redefining their technology choices, operations, or domain meaning.

<br>

## 7. The architecture remains project-independent

Development defines a reusable layered standard. Project-specific choices populate that standard but never change its separation of ownership, interface-only communication, explicit connections, or Platform responsibility.

<br>

## 8. Cross-cutting capabilities are coordinated by Development

Capabilities that may affect more than one application layer are coordinated by Development rather than owned as an isolated default by Model, Backend, Frontend, or Database. Examples include testing, logging, error handling, and authentication.

Development records whether each capability is enabled, which layers it applies to, and the shared integration expectations that keep those layers compatible. Each affected layer still owns its internal implementation and consumes the capability through an explicit boundary.

<br>

## 9. A package is an encapsulated implementation boundary

A package is an identifiable collection of implementation resources with a cohesive responsibility, explicit dependencies, owned configuration, and a documented public interface. Its internal details remain private to that boundary. This definition is independent of a programming language or package manager.

A package may be an importable library, a runnable application, or a nested module supported by its implementation technology. Being a package does not require public registry publication, a separate process, or an independently installable distribution. Nested packages may share their parent's installation, dependency management, and runtime while preserving their own logical boundaries.

Package identity follows responsibility. Naming conventions and prefixes are supplied by Development Preferences and resolved consistently with the selected ecosystem. A generic name does not imply that the package's implementation or domain data is reusable across unrelated projects.

<br>

## 10. Package interfaces define how consumers use a boundary

Each package explicitly identifies what it exposes and what it consumes. Its public interface may be an import surface, network API, command, user interface, or another appropriate mechanism. Consumers use only the interface intended for them; they do not depend on private files or implementation details. A package with no external consumer records that fact instead of inventing an interface.

A nested package's interface is available only to its declared consumers within the permitted boundary. Nesting alone does not expose its internals to consumers of the parent; the parent explicitly provides or delegates any capabilities it makes available outside itself. The owning architecture still determines permitted dependency directions.

<br>

## 11. Every package documents its use

Each package, including architectural subpackages, carries a README describing its purpose, boundaries, public interface, dependencies, configuration, and concrete usage examples. It explains installation and startup when applicable; a nested package may refer to its parent's setup instructions rather than duplicate them.

The README lets a consumer use the package without inspecting its implementation. It distinguishes supported public operations from internal details and explains how to access the package's interface documentation. It documents configuration names and non-secret examples without recording credentials or other secret values. Documentation remains consistent with the implemented interface.
