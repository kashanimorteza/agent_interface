# Development Principles

Development defines the high-level composition through which independent peer Developer Components form one application system. It owns their shared architectural concepts, configurable Component Profiles, declared dependency graph, centralized technical catalogues, and cross-Component standards.

Development owns composition rather than the internal meaning or implementation behavior of another Component. Each Participating Component remains focused on its own role and receives shared technical and platform selections through its Development Component Profile.

<br>

## Terms

- **Participating Component** — one peer Developer Component declared by a Component Profile in Development Preferences.
- **Component Profile** — the configurable Development Preferences entry that gives one Participating Component its identity, name, root, type, role, and applicable Language Item, Database Item, and Platform Instance references.
- **Application Package** — a Participating Component whose selected Component Type makes it an importable library or executable application boundary.
- **Component Type** — the conceptual form of a Participating Component, such as a library, executable, or guideline.
- **Language Item** — one reusable Development Preferences definition containing a programming language's version, Package Management, conventions, tools, and role-specific packages.
- **Package Management** — the language-owned technical definition used to resolve, install, isolate, and lock that language's packages.
- **Database Item** — one reusable Development Preferences definition containing a database technology's version, driver, storage, connection, and naming defaults.
- **Package Role** — a named technical responsibility inside a Language Item, such as modeling, API, persistence mapping, or migration, resolved only for the Component role that uses it.
- **Platform Instance Reference** — the identifier of one Platform-owned Instance selected by a Component Profile without copying that Instance's definition into Development.
- **Public Interface** — the provider-owned surface intended for consumers, including supported types, functions, APIs, commands, or other entry points.
- **Connection** — one configurable direct dependency from a consumer Component Profile to a provider Component Profile.
- **Runtime Configuration** — runtime settings and secret references owned inside an Application Package boundary.
- **Cross-cutting Capability** — a shared capability whose application to more than one Participating Component requires Development-level coordination.

<br>

## Relationships

- **Consumes Platform** — references Platform-owned Instances without duplicating their definitions.
- **Consumed by every Participating Component** — provides its Component Profile, Connections, applicable technical items, and shared rules.

<br>

Component Profiles, Language Items, Database Items, Connection entries, publication defaults, and Cross-cutting Capability applicability belong to Development Preferences. Platform Instance and Launch definitions belong to Platform Preferences. Component-specific conceptual defaults remain in the Preferences of their owning Component, and implementation applies all resolved selections to the current Target.

<br>

Every statement here is mandatory. A Developer Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Participating Component has one configurable Component Profile

**Rule:** Development Preferences declares exactly one Component Profile for every Participating Component. Each profile has one canonical identifier and declares its name, repository-relative root, Component Type, high-level role, and any applicable Language Item, Database Item, or Platform Instance reference. Profile values remain configurable Preferences rather than fixed Principle values. Component roots are unique, do not overlap or nest, and contain the files owned by their Components. Participating Components are peers, and each owns its internal organization below its root.

**Why:** One configurable profile gives every Component and Connection a stable resolution point without mixing mutable project defaults into Development philosophy.

**Boundary:** An internal structure, service, tool, or package created inside a Component does not become a Participating Component merely because it has its own files or package boundary.

<br>

## 2. Every Application Package is logically independent

**Rule:** Each Application Package has one cohesive responsibility and owns its internal implementation, Runtime Configuration, and Public Interface. An authorized consumer may install or import a provider Application Package or use another supported public entry point only through a declared Connection and the provider's Public Interface. Such use never transfers logical ownership of provider internals.

**Why:** Logical independence lets an Application Package evolve or be replaced while preserving the explicit dependencies needed to compose a working system.

**Boundary:** Development does not prescribe a Component's internal nesting, source layout, or private implementation structure.

<br>

## 3. Cross-Component use stays behind provider-owned Public Interfaces

**Rule:** Every cross-Component interaction uses a Public Interface owned by the provider. The provider owns the number, shape, and implementation of its public entry points. A Connection identifies only its consumer and provider and never duplicates the provider's interface definition.

**Why:** Consumers depend on a supported contract while providers remain free to change private implementation.

**Boundary:** A consumer never reads, changes, or depends on another Component's private implementation, internal storage, private resources, or internal Runtime Configuration. Development defines the interface standard but not a Component's interface contents or implementation method.

<br>

## 4. The declared Connection graph is direct, explicit, and acyclic

**Rule:** Every permitted direct dependency is declared exactly once as a Connection in Development Preferences. Connection direction runs from consumer to provider and represents dependency rather than request-and-response data direction. Connections are direct, non-transitive, and acyclic; an indirect path never grants direct access.

**Why:** One declared directed graph makes dependency ownership visible and prevents hidden, circular, or accidentally inherited coupling.

**Boundary:** A provider response creates no reverse Connection, a Connection selects no transport, and a Platform Instance Reference is configuration rather than a runtime dependency Connection.

<br>

## 6. Cross-cutting Capabilities are activated through applicability

**Rule:** Development Preferences declares each Cross-cutting Capability with one applicability list. An empty list makes the capability inactive; a non-empty list activates it only for the uniquely listed canonical Component identifiers. Each listed Component applies the shared requirement while retaining ownership of its internal realization.

**Why:** One applicability list coordinates shared behavior without transferring implementation ownership to Development.

**Boundary:** Development uses no separate enabled flag for a Cross-cutting Capability. Behavior wholly internal to one Component remains owned by that Component.

<br>

## 9. Every Component has complete, safe, and operational documentation

**Rule:** Every Participating Component is generated with a README at the root selected by its Component Profile. The README briefly explains the Component, its actual public surface and structure, setup, installation, configuration, use, run procedure when applicable, verification, troubleshooting, and every active capability relevant to working with it. It uses the resolved technical selections to provide accurate executable examples. Documentation stays consistent with public behavior and enables a human or Agent to understand and use the Component without inspecting private implementation.

A README may show safe code and secret-supply mechanisms, but it uses placeholders, environment-variable names, or safe secret references and never includes a usable credential, token, or secret value. Public usage changes update the README.

**Why:** Operational documentation gives each resolved Component one practical usage guide without duplicating its governing philosophy.

**Boundary:** A README never copies or restates Principles and never replaces or overrides Principles, Preferences, the implemented Public Interface, or another authoritative project source.

<br>

## 10. Unstated Development decisions follow one precedence order

**Rule:** When the Target leaves a Development-owned decision unstated, resolution applies Development Principles first, Development Preferences second, and compatible professional judgment last.

**Why:** A short precedence order preserves architecture, applies the Human's defaults, and leaves judgment only for a genuine gap.

**Boundary:** Professional judgment never overrides a Development Principle or an applicable Development Preference. Component-internal conceptual decisions remain governed by that Component's own Principles and Preferences.

<br>

## 11. Runtime Configuration ownership remains inside its boundary

**Rule:** Each Application Package owns the contract and internal representation of its Runtime Configuration. A selected Platform Instance and Launch may deliver required runtime values through documented inputs. Runtime secret values remain in appropriate secret sources rather than Interface files or documentation.

**Why:** Explicit configuration ownership allows Platform to operate the system without taking ownership of application internals or exposing secrets.

**Boundary:** One Application Package never directly reads or modifies another's internal Runtime Configuration. Platform may coordinate delivery but never redefines the internal contract owned by an Application Package.

<br>

## 12. Public Interface changes propagate through direct consumers

**Rule:** A provider may change private implementation without consumer changes while its Public Interface remains compatible. When a Public Interface changes, every direct consumer in the declared Connection graph is reviewed and, when affected, updated or regenerated and verified. Propagation continues through later Connections only when an affected consumer's own Public Interface also changes.

**Why:** Change follows actual dependencies, keeping consumers correct without rebuilding unrelated Components.

**Boundary:** A private change with no Public Interface effect triggers no consumer work, and a Public Interface change authorizes no change outside the affected dependency path.

<br>

## 13. Development centralizes reusable technical items

**Rule:** Development Preferences defines every Language Item and Database Item once. A Language Item contains its version, Package Management choice, naming and typing conventions, quality tools, and Package Roles grouped by the Participating Component that uses them. A Database Item contains its version and applicable technical defaults. Each Component Profile references the applicable items and automatically consumes only the package group matching its own canonical Component identifier. Concrete language, package, database, version, tool, and Package Management selections are never duplicated in a participating Component's own Principles or Preferences.

**Why:** Central technical catalogues preserve all reusable choices in one place while letting Components focus exclusively on their conceptual responsibilities.

**Boundary:** A Component Profile may omit an inapplicable technical reference. Development only references a Platform Instance; the Instance and Launch definitions and all their internal parameters remain owned by Platform.

<br>

## At a Glance

- **Must** — Declare exactly one configurable Component Profile for every Participating Component. *(1)*
- **Must** — Give each profile a canonical identifier, name, unique repository-relative root, Component Type, role, and its applicable technical or Platform references. *(1)*
- **Never** — Fix configurable Component Profile values inside Principles or treat an internal item as a Participating Component. *(1)*
- **Must** — Keep Participating Components peer-owned and let each own its organization below its non-overlapping root. *(1)*
- **Must** — Keep every Application Package cohesive and responsible for its implementation, Runtime Configuration, and Public Interface. *(2)*
- **Must** — Limit every authorized cross-package use to a declared Connection and the provider's Public Interface. *(2)*
- **Never** — Turn provider use into ownership of its internals or let Development prescribe private implementation structure. *(2)*
- **Must** — Route every cross-Component interaction through a provider-owned Public Interface. *(3)*
- **Must** — Let each provider own its public entry points while each Connection records only consumer and provider. *(3)*
- **Never** — Access another Component's private implementation, storage, resources, or internal Runtime Configuration. *(3)*
- **Never** — Let Development define a provider's interface contents or realization method. *(3)*
- **Must** — Declare every permitted direct dependency exactly once in a direct, non-transitive, acyclic Connection graph. *(4)*
- **Never** — Infer direct access, reverse dependency, or transport from an indirect path or provider response. *(4)*
- **Never** — Treat a Platform Instance Reference as a runtime dependency Connection. *(4)*
- **Must** — Activate a Cross-cutting Capability only for unique canonical identifiers in its applicability list. *(6)*
- **Must** — Keep realization of an active Cross-cutting Capability inside each listed Component. *(6)*
- **Never** — Use a separate enabled flag or apply a Cross-cutting Capability to an unlisted Component. *(6)*
- **Must** — Generate a root README that explains actual structure, public use, setup, configuration, operation, verification, troubleshooting, and active capabilities with executable resolved-technology examples. *(9)*
- **Must** — Keep every README consistent with public behavior and update it when public usage changes. *(9)*
- **Never** — Expose a usable secret in documentation or let a README copy, replace, or override an authoritative source. *(9)*
- **Must** — Resolve an unstated Development decision through Principles, Preferences, then compatible professional judgment. *(10)*
- **Never** — Let judgment override an applicable Principle or Preference. *(10)*
- **Must** — Leave Component-internal conceptual decisions to that Component's Principles and Preferences. *(10)*
- **Must** — Keep each Application Package's Runtime Configuration contract and representation within its boundary. *(11)*
- **Must** — Let Platform deliver runtime values through documented inputs without redefining an owned contract. *(11)*
- **Never** — Store runtime secrets in Interface files or documentation or let one package directly modify another's Runtime Configuration. *(11)*
- **Must** — Review, update or regenerate when affected, and verify every direct consumer after a Public Interface changes. *(12)*
- **Must** — Continue propagation only when an affected consumer's own Public Interface changes. *(12)*
- **Never** — Trigger consumer work for a private compatible change or change Components outside the affected dependency path. *(12)*
- **Must** — Define each Language Item and Database Item once with its owned configurable technical details. *(13)*
- **Must** — Resolve a Component Profile through applicable item references and only its own role-specific package group. *(13)*
- **Must** — Omit a technical reference from a Component Profile when that reference is inapplicable. *(13)*
- **Never** — Duplicate concrete technical selections in a participating Component or copy Platform Instance or Launch definitions into Development. *(13)*
