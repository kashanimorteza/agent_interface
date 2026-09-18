# Development Principles

Development defines the high-level composition through which independent peer Implementation Components form one application system. It owns their shared architectural concepts, configurable Component Profiles, declared dependency graph, centralized technical catalogues, and cross-Component standards.

Development owns composition rather than the internal meaning or implementation behavior of another Component. Each Participating Component remains focused on its own role and receives shared technical and platform selections through its Development Component Profile.

<br>

## Terms

- **Participating Component** — one peer Implementation Component declared by a Component Profile in Development Preferences.
- **Component Profile** — the configurable Development Preferences entry that gives one Participating Component its identity, name, root, type, role, and applicable Language Item, Database Item, and Platform Reference.
- **Application Package** — a Participating Component whose selected Component Type makes it an importable library or executable application boundary.
- **Component Type** — the conceptual form of a Participating Component, such as a library, executable, or guideline.
- **Language Item** — one reusable Development Preferences definition containing a programming language's version, Package Management, conventions, tools, and purpose-specific packages.
- **Package Management** — the language-owned technical definition used to resolve, install, isolate, and lock that language's packages.
- **Database Item** — one reusable Development Preferences definition containing a database technology's version, driver, storage, connection, and naming defaults.
- **Technical Purpose** — a language-level use such as modeling, API delivery, database access, or migration that remains independent of any Component identity.
- **Platform Reference** — the identifier of one Platform-owned Launch Item selected by a Component Profile without copying that Launch Item's definition into Development.
- **Public Interface** — the provider-owned surface intended for consumers, including supported types, functions, APIs, commands, or other entry points.
- **Connection** — one configurable direct dependency from a consumer Component Profile to a provider Component Profile.
- **Runtime Configuration** — runtime settings and secret references owned inside an Application Package boundary.
- **Cross-cutting Capability** — a shared capability whose application to more than one Participating Component requires Development-level coordination.
- **Model Operation** — a named operation that a Model may expose through the composed system, such as create, retrieve, list, search, update, enable, disable, or delete.
- **Application Manifest** — `.interface/foundation/config/application.yaml`, created and reconciled by Configure so Components can exchange current public metadata.

<br>

## Relationships

- **Consumes Platform** — references Platform-owned Launch Items without duplicating their definitions.
- **Consumed by every Participating Component** — provides its Component Profile, Connections, applicable technical items, and shared rules.
- **Publishes Application Manifest** — provides current public Component metadata required by composition and consumption.

<br>

Component Profiles, Language Items, Database Items, Connection entries, publication defaults, and Cross-cutting Capability applicability belong to Development Preferences. Platform Launch Item definitions belong to Platform Preferences. Component-specific conceptual defaults remain in the Preferences of their owning Component, and implementation applies all resolved selections to the current Target.

<br>

Every statement here is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Participating Component has one configurable Component Profile

**Rule:** Development Preferences declares exactly one Component Profile for every Participating Component. Each profile has one canonical identifier and declares its name, repository-relative root, Component Type, high-level role, and any applicable Language Item, Database Item, or Platform Reference. Profile values remain configurable Preferences rather than fixed Principle values. Component roots are unique, do not overlap or nest, and contain the files owned by their Components. Participating Components are peers, and each owns its internal organization below its root.

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

**Boundary:** A provider response creates no reverse Connection, a Connection selects no transport, and a Platform Reference is configuration rather than a runtime dependency Connection.

<br>

## 5. Model operations use one shared contract across Components

**Rule:** Development defines one shared vocabulary for operations that may be exposed by a Model. The default Model Operation set is `create`, `get_by_id`, `list`, `search`, `update`, `enable`, `disable`, and `delete`. Each Model declares the operations applicable to its own fields, relationships, and lifecycle; it may omit an inapplicable operation or add a Model-specific operation. When a Model exposes an operation, the Database, Logic, API, and Presentation Components account for that operation in their own responsibilities and preserve its meaning across their public boundaries.

**Why:** One shared operation contract keeps every participating layer aligned while allowing each Model to have the lifecycle and queries its domain actually requires.

**Boundary:** Development defines operation names, applicability, and cross-Component consistency. It does not prescribe storage statements, service methods, API transport, user-interface controls, or another Component's internal realization.

<br>

## 6. Components publish shared application metadata through the Application Manifest

**Rule:** Configure creates and reconciles `.interface/foundation/config/application.yaml` on every run from the current Development Component Profiles, declared Connections, and each Component's public metadata. When an Implementation Component is generated or configured, it publishes its public composition metadata in the section keyed by its canonical identifier, including `package_name` when it has a package, its repository-relative `path`, `public_entrypoint` when applicable, `public_interface` metadata, and any other non-secret value required by another Component to compose or consume it. Consumers may use the Manifest as the shared application metadata surface while ongoing identity and ownership remain authoritative in Development Preferences and declared Connections. Every declared Implementation Component has a Manifest section, even when that section is empty.

**Why:** A persistent, reconciled Manifest gives Components one current place to discover the public information needed for composition without reaching into another Component's private files.

**Boundary:** The Application Manifest never contains credentials, secret values, private implementation details, internal storage structure, or undeclared dependencies. It is a shared metadata projection, not the authority for Target meaning, Component ownership, or technical Preferences; Configure reconciles it from those authoritative sources and reports conflicts rather than silently losing meaningful public metadata.

<br>

## 7. Cross-cutting Capabilities are activated through applicability

**Rule:** Development Preferences declares each Cross-cutting Capability with one applicability list. An empty list makes the capability inactive; a non-empty list activates it only for the uniquely listed canonical Component identifiers. Logging, Error Handling, Authentication, and Encryption are active by default for the five application Components (`model`, `database`, `logic`, `api`, and `presentation`). An explicit Target requirement or exclusion overrides that default for the current Target. Each listed Component applies the shared requirement while retaining ownership of its internal realization.

**Why:** One applicability list coordinates shared behavior without transferring implementation ownership to Development.

**Boundary:** Development uses no separate enabled flag for a Cross-cutting Capability. Behavior wholly internal to one Component remains owned by that Component.

<br>

## 8. Every Component has complete, safe, and operational documentation

**Rule:** Every Participating Component is generated with a README at its `path` root, at the file its Component Profile's `documentation` key names. Documentation is part of generating the Component, not a step after it: a Component whose README is missing or stale is not complete. The README moves from the general to the specific — first what the Component is, what it does, and where it sits; then its actual public surface and structure, with each main class, object, or module explained; then setup and configuration; how it is run or used; every capability relevant to working with it, each shown with an executable example wherever it can be executed; how to verify it works; and troubleshooting. Each Component fills that order through its own mechanism, and a part that does not apply says so rather than disappearing. Examples use the resolved technical selections so they run as written.

The README's first duty is the Component's Public Interface: it explains that Interface completely — what the Component offers, what each Operation takes and returns, and how a consumer imports and calls it — with explanation, runnable examples, and a tree of the Interface where that makes it clearer. Internal parts are not explained there, and a reader who needs one has been told something the Public Interface should have carried instead. Anyone who reads that section is able to use the Component without reading its source. Documentation stays consistent with public behavior, and its measure is one: anyone — human or Agent — who reads it understands how the Component works and can use it without inspecting private implementation. The shared conventions of that documentation — file name, order of parts, example policy — are declared once in Development Preferences and apply to every Participating Component.

A README may show safe code and secret-supply mechanisms, but it uses placeholders, environment-variable names, or safe secret references and never includes a usable credential, token, or secret value. Public usage changes update the README.

**Why:** Operational documentation gives each resolved Component one practical usage guide without duplicating its governing philosophy.

**Boundary:** A README never copies or restates Principles and never replaces or overrides Principles, Preferences, the implemented Public Interface, or another authoritative project source.

<br>

## 9. Unstated Development decisions follow one precedence order

**Rule:** When the Target leaves a Development-owned decision unstated, resolution applies Development Principles first, Development Preferences second, and compatible professional judgment last.

**Why:** A short precedence order preserves architecture, applies the Human's defaults, and leaves judgment only for a genuine gap.

**Boundary:** Professional judgment never overrides a Development Principle or an applicable Development Preference. Component-internal conceptual decisions remain governed by that Component's own Principles and Preferences.

<br>

## 10. Runtime Configuration ownership remains inside its boundary

**Rule:** Each Application Package owns the contract and internal representation of its Runtime Configuration. A selected Platform Launch Item may deliver required runtime values through documented inputs. Runtime secret values remain in appropriate secret sources rather than Interface files or documentation.

**Why:** Explicit configuration ownership allows Platform to operate the system without taking ownership of application internals or exposing secrets.

**Boundary:** One Application Package never directly reads or modifies another's internal Runtime Configuration. Platform may coordinate delivery but never redefines the internal contract owned by an Application Package.

<br>

## 11. Public Interface changes propagate through direct consumers

**Rule:** A provider may change private implementation without consumer changes while its Public Interface remains compatible. When a Public Interface changes, every direct consumer in the declared Connection graph is reviewed and, when affected, updated or regenerated and verified. Propagation continues through later Connections only when an affected consumer's own Public Interface also changes.

**Why:** Change follows actual dependencies, keeping consumers correct without rebuilding unrelated Components.

**Boundary:** A private change with no Public Interface effect triggers no consumer work, and a Public Interface change authorizes no change outside the affected dependency path.

<br>

## 12. Development centralizes reusable technical items

**Rule:** Development Preferences defines every Language Item and Database Item once. A Language Item contains its version, Package Management choice, naming and typing conventions, quality tools, and packages grouped by Technical Purpose rather than Component identity. When a Technical Purpose has one package, that package is its default; when it has multiple compatible packages, Development Preferences may mark one with `selected: true` as the default choice. Implementation resolves the selected default only when that purpose is required by the Target and the Component's own conceptual responsibilities. A Database Item contains its version and applicable technical defaults. Each Component Profile references the applicable items, while implementation resolves only the Technical Purposes required by the Target and the Component's own conceptual responsibilities. The same Technical Purpose may be used by any compatible Component. Concrete language, package, database, version, tool, and Package Management selections are never duplicated in a participating Component's own Principles or Preferences.

**Why:** Central technical catalogues preserve all reusable choices in one place while letting Components focus exclusively on their conceptual responsibilities.

**Boundary:** A Component Profile may omit an inapplicable technical reference. A Technical Purpose never restricts its package to a particular Component or transfers conceptual responsibility into the Language Item. Development only references a Platform Launch Item; its definition and all internal parameters remain owned by Platform.


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
- **Never** — Treat a Platform Reference as a runtime dependency Connection. *(4)*
- **Must** — Use the shared Model Operation vocabulary and preserve the meaning of each exposed operation across Database, Logic, API, and Presentation. *(5)*
- **Must** — Let each Model declare its applicable operations based on its fields, relationships, and lifecycle. *(5)*
- **May** — Omit an inapplicable default operation or add a Model-specific operation. *(5)*
- **Never** — Prescribe a Component's internal implementation from a Model Operation. *(5)*
- **Must** — Maintain the repository-level Application Manifest from Development Profiles, Connections, and public Component metadata. *(6)*
- **Must** — Include a Manifest section for every declared Component, even when it is empty. *(6)*
- **Never** — Put secrets, private implementation details, or undeclared dependencies in the Application Manifest. *(6)*
- **Must** — Activate a Cross-cutting Capability only for unique canonical identifiers in its applicability list. *(7)*
- **Must** — Keep realization of an active Cross-cutting Capability inside each listed Component. *(7)*
- **Never** — Use a separate enabled flag or apply a Cross-cutting Capability to an unlisted Component. *(7)*
- **Must** — Apply Logging, Error Handling, Authentication, and Encryption by default to the five application Components: Model, Database, Logic, API, and Presentation. *(7)*
- **May** — Override a default Cross-cutting Capability explicitly in the Target. *(7)*
- **Must** — Generate a README at each Component's `path` root, named by its Profile's `documentation` key, as part of generating the Component. *(8)*
- **Must** — Order the README from the general to the specific: overview, structure and main objects, setup, run, capabilities with executable examples, verification, troubleshooting — through each Component's own mechanism, stating explicitly when a part does not apply. *(8)*
- **Must** — Write it so that anyone who reads it understands how the Component works, with examples that run on the resolved technology. *(8)*
- **Must** — Explain the Component's Public Interface completely — every Operation's inputs and results, and how a consumer imports and calls it — with examples, and a tree of the Interface where that helps. *(8)*
- **Never** — Explain a Component's internal parts in its README, or leave a consumer needing one in order to use the Component. *(8)*
- **Must** — Keep every README consistent with public behavior and update it when public usage changes. *(8)*
- **Never** — Expose a usable secret in documentation or let a README copy, replace, or override an authoritative source. *(8)*
- **Must** — Resolve an unstated Development decision through Principles, Preferences, then compatible professional judgment. *(9)*
- **Never** — Let judgment override an applicable Principle or Preference. *(9)*
- **Must** — Leave Component-internal conceptual decisions to that Component's Principles and Preferences. *(9)*
- **Must** — Keep each Application Package's Runtime Configuration contract and representation within its boundary. *(10)*
- **Must** — Let Platform deliver runtime values through documented inputs without redefining an owned contract. *(10)*
- **Never** — Store runtime secrets in Interface files or documentation or let one package directly modify another's Runtime Configuration. *(10)*
- **Must** — Review, update or regenerate when affected, and verify every direct consumer after a Public Interface changes. *(11)*
- **Must** — Continue propagation only when an affected consumer's own Public Interface changes. *(11)*
- **Never** — Trigger consumer work for a private compatible change or change Components outside the affected dependency path. *(11)*
- **Must** — Define each Language Item and Database Item once with its owned configurable technical details. *(12)*
- **Must** — Group language packages by Technical Purpose and resolve only the purposes applicable to the Target and Component responsibility. *(12)*
- **May** — Mark one package with `selected: true` when a Technical Purpose has multiple compatible package choices; a single package is the default without a marker. *(12)*
- **Must** — Allow any compatible Component to use an applicable Technical Purpose. *(12)*
- **Must** — Omit a technical reference from a Component Profile when that reference is inapplicable. *(12)*
- **Never** — Group a language package by Component identity or let a Technical Purpose transfer conceptual responsibility. *(12)*
- **Never** — Duplicate concrete technical selections in a participating Component or copy Platform Launch Item definitions into Development. *(12)*
