# Development Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
   - **[Decisions](#decisions)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Every Participating Component has one configurable Component Profile](#every-participating-component-has-one-configurable-component-profile)**
   - **[Every Application Package is logically independent](#every-application-package-is-logically-independent)**
   - **[Cross-Component use stays behind provider-owned Public Interfaces](#cross-component-use-stays-behind-provider-owned-public-interfaces)**
   - **[The declared Connection graph is direct, explicit, and acyclic](#the-declared-connection-graph-is-direct-explicit-and-acyclic)**
   - **[Components publish shared application metadata through the Application Manifest](#components-publish-shared-application-metadata-through-the-application-manifest)**
   - **[Cross-cutting Capabilities are activated through applicability](#cross-cutting-capabilities-are-activated-through-applicability)**
   - **[Every Component has complete, safe, and operational documentation](#every-component-has-complete-safe-and-operational-documentation)**
   - **[Unstated Development decisions follow one precedence order](#unstated-development-decisions-follow-one-precedence-order)**
   - **[Runtime Configuration ownership remains inside its boundary](#runtime-configuration-ownership-remains-inside-its-boundary)**
   - **[Public Interface changes propagate through direct consumers](#public-interface-changes-propagate-through-direct-consumers)**
   - **[Development centralizes reusable technical items](#development-centralizes-reusable-technical-items)**
   - **[Every Component offers its work as Operations on one Public Interface](#every-component-offers-its-work-as-operations-on-one-public-interface)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Development defines the high-level composition through which independent peer Implementation Components form one application system. It owns their shared architectural concepts, configurable Component Profiles, declared dependency graph, centralized technical catalogues, and cross-Component standards.

Development owns composition rather than the internal meaning or implementation behavior of another Component. Each Participating Component remains focused on its own role and receives shared technical and platform selections through its Development Component Profile.

### Purpose

Software is built from parts, and the parts have to agree on things none of them owns alone: where each one lives, what it is allowed to reach, which language and packages it uses, how it presents itself to the others, and what it must publish about itself. Someone has to hold those agreements. Without a Component that does, each part settles them privately — one picks its own dependency versions, another reaches into a neighbour's internals because it was convenient, a third invents its own way of being called — and the system stops being one system.

Development exists to hold them. It owns composition: the profile of every Participating Component, the graph of who may depend on whom, the catalogues of languages and databases every Component draws from, and the standards every Component honours — one Public Interface offering Operations, one documentation shape, one precedence order when the project is silent. Each Component then concentrates on its own responsibility and receives the shared decisions rather than making them again.

The cost of the alternative is drift that is invisible until it is expensive: two Components on incompatible versions of the same package, a dependency cycle nobody declared, a consumer bound to a provider's private internals, a Component nobody can use because it documents nothing. None of those is one Component's fault, which is exactly why one Component has to own them.

### How It Works

A Component Profile is the unit Development works in. Each Participating Component has exactly one: its identity, its root in the repository, its type, its role, and the technical and Platform references that apply to it. Reading that profile tells the Component everything the composition decides on its behalf.

The technical choices behind those references live in Development's own catalogues rather than in the Components. A Language Item holds a language's version, package management, conventions, tools, and packages grouped by Technical Purpose; a Database Item holds a database technology's version, driver, and defaults. A Component Profile names the items that apply to it, and the Component resolves what it needs from there — so two Components on the same language are on the same version by construction, not by coincidence.

Dependencies are declared, not discovered. A Connection names one consumer and one provider, and that declaration is the whole permission: what flows across it is the provider's Public Interface and its Operations, never its internals. The graph of those Connections stays direct and acyclic, so the composition can always be read as an order.

What every Component owes the others is fixed by Development's standards rather than negotiated per Component: one Public Interface offering Operations that state what they accept and return, one README that explains that Interface, public metadata published through the Application Manifest, and a stated precedence order for the decisions the Target leaves open. Development supplies the shape; each Component fills it with its own content.

### Decisions

**Documentation**

1. Documentation is a Development concern: every new Component starts from Development, and there it learns how to document itself; each Component's Preferences names where its documentation lives, and each Component fulfils that through its own mechanism, measured by whether a reader understands how the Component works.
2. An earlier statement that the README also explains a Component's classes and objects is not kept: the Principle now scopes the README to the Public Interface and excludes internal structure — parts, services, layers, classes — as documenting the wrong thing.
3. The Principles Schema fixes the shape of every Principles file; the shape of a generated documentation file belongs to a Schema or Preferences instead, so the concept stays inside Development. Principle "Every Component has complete, safe, and operational documentation" carries the rule; Development Preferences carry the conventions once for all Components (`settings.documentation`: file, location, order, examples, per-Component fulfilment, secrets, authority), and each Component Profile carries its `documentation` path. Documentation is Development-specific for now; a Foundation-level README Schema is not needed until another Module needs the same shape.
4. After the first Implement run, `model/` and `database/` were generated without a README although the documentation Principle required one — Planning had scoped "applicable obligations" to the phase's own Component, and the phrase "at the root selected by its Component Profile" pointed at a key the Profile did not have. Both are now closed: the Profile has the key, the Principle names it, and the Agent Module's placement rule keeps the obligation from being narrowed in the synchronized Skills.

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
- **Public Interface** — the one provider-owned surface a consumer uses, carrying the Operations that Component offers and nothing else.
- **Operation** — one complete unit of work a Public Interface offers, named by what the consumer wants done rather than by how it is carried out, and stating what it accepts, what it returns, and which outcomes it can produce.
- **Category** — a named grouping of Operations within one Public Interface, used when a Component offers enough Operations that grouping them helps a consumer find the right one.
- **Connection** — one configurable direct dependency from a consumer Component Profile to a provider Component Profile.
- **Runtime Configuration** — runtime settings and secret references owned inside an Application Package boundary.
- **Cross-cutting Capability** — a shared capability whose application to more than one Participating Component requires Development-level coordination.
- **Application Manifest** — `.interface/foundation/config/application.yaml`, created and reconciled by Configure so Components can exchange current public metadata.

<br>

## Relationships

- **Consumes Platform** — references Platform-owned Launch Items without duplicating their definitions.
- **Consumed by every Participating Component** — provides its Component Profile, Connections, applicable technical items, and shared rules.
- **Publishes Application Manifest** — provides current public Component metadata required by composition and consumption.

<br>

Component Profiles, Language Items, Database Items, Connection entries, publication defaults, and Cross-cutting Capability applicability belong to Development Preferences. Platform Launch Item definitions belong to Platform Preferences. Component-specific conceptual defaults remain in the Preferences of their owning Component, and implementation applies all resolved selections to the current Target.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## Principles

Every Principle below is mandatory.

<br>

### Every Participating Component has one configurable Component Profile

**Rule:** Development Preferences declares exactly one Component Profile for every Participating Component. Each profile has one canonical identifier and declares its name, repository-relative root, Component Type, high-level role, and any applicable Language Item, Database Item, or Platform Reference. Profile values remain configurable Preferences rather than fixed Principle values. Component roots are unique, do not overlap or nest, and contain the files owned by their Components. Participating Components are peers, and each owns its internal organization below its root.

**Why:** One configurable profile gives every Component and Connection a stable resolution point without mixing mutable project defaults into Development philosophy.

**Boundary:** An internal structure, service, tool, or package created inside a Component does not become a Participating Component merely because it has its own files or package boundary.

<br>

### Every Application Package is logically independent

**Rule:** Each Application Package has one cohesive responsibility and owns its internal implementation, Runtime Configuration, and Public Interface. An authorized consumer may install or import a provider Application Package or use another supported public entry point only through a declared Connection and the provider's Public Interface. Such use never transfers logical ownership of provider internals.

**Why:** Logical independence lets an Application Package evolve or be replaced while preserving the explicit dependencies needed to compose a working system.

**Boundary:** Development does not prescribe a Component's internal nesting, source layout, or private implementation structure.

<br>

### Cross-Component use stays behind provider-owned Public Interfaces

**Rule:** Every cross-Component interaction uses a Public Interface owned by the provider. The provider owns the number, shape, and implementation of its public entry points. A Connection identifies only its consumer and provider and never duplicates the provider's interface definition.

**Why:** Consumers depend on a supported contract while providers remain free to change private implementation.

**Boundary:** A consumer never reads, changes, or depends on another Component's private implementation, internal storage, private resources, or internal Runtime Configuration. Development defines the interface standard but not a Component's interface contents or implementation method.

<br>

### The declared Connection graph is direct, explicit, and acyclic

**Rule:** Every permitted direct dependency is declared exactly once as a Connection in Development Preferences. Connection direction runs from consumer to provider and represents dependency rather than request-and-response data direction. Connections are direct, non-transitive, and acyclic; an indirect path never grants direct access.

**Why:** One declared directed graph makes dependency ownership visible and prevents hidden, circular, or accidentally inherited coupling.

**Boundary:** A provider response creates no reverse Connection, a Connection selects no transport, and a Platform Reference is configuration rather than a runtime dependency Connection.

<br>

### Components publish shared application metadata through the Application Manifest

**Rule:** Configure creates and reconciles `.interface/foundation/config/application.yaml` on every run from the current Development Component Profiles, declared Connections, and each Component's public metadata. When an Implementation Component is generated or configured, it publishes its public composition metadata in the section keyed by its canonical identifier, including `package_name` when it has a package, its repository-relative `path`, `public_entrypoint` when applicable, `public_interface` metadata, and any other non-secret value required by another Component to compose or consume it. Consumers may use the Manifest as the shared application metadata surface while ongoing identity and ownership remain authoritative in Development Preferences and declared Connections. Every declared Implementation Component has a Manifest section, even when that section is empty.

**Why:** A persistent, reconciled Manifest gives Components one current place to discover the public information needed for composition without reaching into another Component's private files.

**Boundary:** The Application Manifest never contains credentials, secret values, private implementation details, internal storage structure, or undeclared dependencies. It is a shared metadata projection, not the authority for Target meaning, Component ownership, or technical Preferences; Configure reconciles it from those authoritative sources and reports conflicts rather than silently losing meaningful public metadata.

<br>

### Cross-cutting Capabilities are activated through applicability

**Rule:** Development Preferences declares each Cross-cutting Capability with one applicability list. An empty list makes the capability inactive; a non-empty list activates it only for the uniquely listed canonical Component identifiers. Logging, Error Handling, Authentication, and Encryption are active by default for the five application Components (`model`, `database`, `logic`, `api`, and `presentation`). An explicit Target requirement or exclusion overrides that default for the current Target. Each listed Component applies the shared requirement while retaining ownership of its internal realization.

**Why:** One applicability list coordinates shared behavior without transferring implementation ownership to Development.

**Boundary:** Development uses no separate enabled flag for a Cross-cutting Capability. Behavior wholly internal to one Component remains owned by that Component.

<br>

### Every Component has complete, safe, and operational documentation

**Rule:** Every Participating Component is generated with a README at its `path` root, at the file its Component Profile's `documentation` key names. Documentation is part of generating the Component, not a step after it: a Component whose README is missing or stale is not complete. The README moves from the general to the specific — first what the Component is, what it does, and where it sits; then its Public Interface: every Category and every Operation, what each one accepts, what it returns, the outcomes it can produce, and a runnable example of calling it; then setup and configuration; how it is run or used; how to verify it works; and troubleshooting. Each Component fills that order through its own mechanism, and a part that does not apply says so rather than disappearing. Examples use the resolved technical selections so they run as written.

The README exists to explain the Public Interface. It covers that Interface completely — every Category and Operation as Principle "Every Component offers its work as Operations on one Public Interface" defines them, what each Operation takes and returns, and how a consumer imports and calls it — through explanation, runnable code, and a tree of the Interface where that makes it clearer, so that anyone who reads it can work with the Component through its Public Interface without reading its source. It does not explain the Component's internal structure — its parts, its services, its layers, its classes. Those are stated in the Component's Principles and Preferences, and a README that explains them is documenting the wrong thing. Documentation stays consistent with public behavior, and its measure is one: anyone — human or Agent — who reads it understands how the Component works and can use it without inspecting private implementation. The shared conventions of that documentation — file name, order of parts, example policy — are declared once in Development Preferences and apply to every Participating Component.

A README may show safe code and secret-supply mechanisms, but it uses placeholders, environment-variable names, or safe secret references and never includes a usable credential, token, or secret value. Public usage changes update the README.

**Why:** Operational documentation gives each resolved Component one practical usage guide without duplicating its governing philosophy.

**Boundary:** A README never copies or restates Principles and never replaces or overrides Principles, Preferences, the implemented Public Interface, or another authoritative project source.

<br>

### Unstated Development decisions follow one precedence order

**Rule:** When the Target leaves a Development-owned decision unstated, resolution applies Development Principles first, Development Preferences second, and compatible professional judgment last.

**Why:** A short precedence order preserves architecture, applies the Human's defaults, and leaves judgment only for a genuine gap.

**Boundary:** Professional judgment never overrides a Development Principle or an applicable Development Preference. Component-internal conceptual decisions remain governed by that Component's own Principles and Preferences.

<br>

### Runtime Configuration ownership remains inside its boundary

**Rule:** Each Application Package owns the contract and internal representation of its Runtime Configuration. A selected Platform Launch Item may deliver required runtime values through documented inputs. Runtime secret values remain in appropriate secret sources rather than Interface files or documentation.

**Why:** Explicit configuration ownership allows Platform to operate the system without taking ownership of application internals or exposing secrets.

**Boundary:** One Application Package never directly reads or modifies another's internal Runtime Configuration. Platform may coordinate delivery but never redefines the internal contract owned by an Application Package.

<br>

### Public Interface changes propagate through direct consumers

**Rule:** A provider may change private implementation without consumer changes while its Public Interface remains compatible. When a Public Interface changes, every direct consumer in the declared Connection graph is reviewed and, when affected, updated or regenerated and verified. Propagation continues through later Connections only when an affected consumer's own Public Interface also changes.

**Why:** Change follows actual dependencies, keeping consumers correct without rebuilding unrelated Components.

**Boundary:** A private change with no Public Interface effect triggers no consumer work, and a Public Interface change authorizes no change outside the affected dependency path.

<br>

### Development centralizes reusable technical items

**Rule:** Development Preferences defines every Language Item and Database Item once. A Language Item contains its version, Package Management choice, naming and typing conventions, quality tools, and packages grouped by Technical Purpose rather than Component identity. When a Technical Purpose has one package, that package is its default; when it has multiple compatible packages, Development Preferences may mark one with `selected: true` as the default choice. Implementation resolves the selected default only when that purpose is required by the Target and the Component's own conceptual responsibilities. A Database Item contains its version and applicable technical defaults. Each Component Profile references the applicable items, while implementation resolves only the Technical Purposes required by the Target and the Component's own conceptual responsibilities. The same Technical Purpose may be used by any compatible Component. Concrete language, package, database, version, tool, and Package Management selections are never duplicated in a participating Component's own Principles or Preferences.

**Why:** Central technical catalogues preserve all reusable choices in one place while letting Components focus exclusively on their conceptual responsibilities.

**Boundary:** A Component Profile may omit an inapplicable technical reference. A Technical Purpose never restricts its package to a particular Component or transfers conceptual responsibility into the Language Item. Development only references a Platform Launch Item; its definition and all internal parameters remain owned by Platform.


<br>

### Every Component offers its work as Operations on one Public Interface

**Rule:** Every Participating Component publishes exactly one Public Interface and offers its work there as Operations. An Operation is a complete unit of work named in the consumer's terms, and it declares what it accepts, what it returns, and which outcomes it can produce. A Component with enough Operations to need grouping organizes them into Categories; a Category groups and performs no work of its own. What a Component offers is therefore answerable as a list: these Operations, with these inputs and these results.

**Why:** One shape shared by every Component means a consumer learns how to read a Component once rather than once per Component, documentation states what a Component offers in the same terms every time, and a Component can be replaced by anything that offers the same Operations.

**Boundary:** This Principle fixes the shape, never the contents: which Operations a Component offers, what they are called, and what they do belong to that Component's own Principles and Preferences. It does not prescribe how an Operation is realized in code — a function, a method, a command, or a request handler are all realizations the Component and its selected technology decide.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Every Participating Component has one configurable Component Profile**

- **Must** — Declare exactly one configurable Component Profile for every Participating Component.
- **Must** — Give each profile a canonical identifier, name, unique repository-relative root, Component Type, role, and its applicable technical or Platform references.
- **Never** — Fix configurable Component Profile values inside Principles or treat an internal item as a Participating Component.
- **Must** — Keep Participating Components peer-owned and let each own its organization below its non-overlapping root.

**Every Application Package is logically independent**

- **Must** — Keep every Application Package cohesive and responsible for its implementation, Runtime Configuration, and Public Interface.
- **Must** — Limit every authorized cross-package use to a declared Connection and the provider's Public Interface.
- **Never** — Turn provider use into ownership of its internals or let Development prescribe private implementation structure.

**Cross-Component use stays behind provider-owned Public Interfaces**

- **Must** — Route every cross-Component interaction through a provider-owned Public Interface.
- **Must** — Let each provider own its public entry points while each Connection records only consumer and provider.
- **Never** — Access another Component's private implementation, storage, resources, or internal Runtime Configuration.
- **Never** — Let Development define a provider's interface contents or realization method.

**The declared Connection graph is direct, explicit, and acyclic**

- **Must** — Declare every permitted direct dependency exactly once in a direct, non-transitive, acyclic Connection graph.
- **Never** — Infer direct access, reverse dependency, or transport from an indirect path or provider response.
- **Never** — Treat a Platform Reference as a runtime dependency Connection.

**Components publish shared application metadata through the Application Manifest**

- **Must** — Maintain the repository-level Application Manifest from Development Profiles, Connections, and public Component metadata.
- **Must** — Include a Manifest section for every declared Component, even when it is empty.
- **Never** — Put secrets, private implementation details, or undeclared dependencies in the Application Manifest.

**Cross-cutting Capabilities are activated through applicability**

- **Must** — Activate a Cross-cutting Capability only for unique canonical identifiers in its applicability list.
- **Must** — Keep realization of an active Cross-cutting Capability inside each listed Component.
- **Never** — Use a separate enabled flag or apply a Cross-cutting Capability to an unlisted Component.
- **Must** — Apply Logging, Error Handling, Authentication, and Encryption by default to the five application Components: Model, Database, Logic, API, and Presentation.
- **May** — Override a default Cross-cutting Capability explicitly in the Target.

**Every Component has complete, safe, and operational documentation**

- **Must** — Generate a README at each Component's `path` root, named by its Profile's `documentation` key, as part of generating the Component.
- **Must** — Order the README from the general to the specific: overview, the Public Interface with every Category and Operation and a runnable example of each, setup, run, verification, troubleshooting — through each Component's own mechanism, stating explicitly when a part does not apply.
- **Must** — Write it so that anyone who reads it understands how the Component works, with examples that run on the resolved technology.
- **Must** — Explain the Component's Public Interface completely — every Operation's inputs and results, and how a consumer imports and calls it — with examples, and a tree of the Interface where that helps.
- **Never** — Explain a Component's internal structure in its README, or leave a consumer needing it in order to use the Component.
- **Must** — Keep every README consistent with public behavior and update it when public usage changes.
- **Never** — Expose a usable secret in documentation or let a README copy, replace, or override an authoritative source.

**Unstated Development decisions follow one precedence order**

- **Must** — Resolve an unstated Development decision through Principles, Preferences, then compatible professional judgment.
- **Never** — Let judgment override an applicable Principle or Preference.
- **Must** — Leave Component-internal conceptual decisions to that Component's Principles and Preferences.

**Runtime Configuration ownership remains inside its boundary**

- **Must** — Keep each Application Package's Runtime Configuration contract and representation within its boundary.
- **Must** — Let Platform deliver runtime values through documented inputs without redefining an owned contract.
- **Never** — Store runtime secrets in Interface files or documentation or let one package directly modify another's Runtime Configuration.

**Public Interface changes propagate through direct consumers**

- **Must** — Review, update or regenerate when affected, and verify every direct consumer after a Public Interface changes.
- **Must** — Continue propagation only when an affected consumer's own Public Interface changes.
- **Never** — Trigger consumer work for a private compatible change or change Components outside the affected dependency path.

**Development centralizes reusable technical items**

- **Must** — Define each Language Item and Database Item once with its owned configurable technical details.
- **Must** — Group language packages by Technical Purpose and resolve only the purposes applicable to the Target and Component responsibility.
- **May** — Mark one package with `selected: true` when a Technical Purpose has multiple compatible package choices; a single package is the default without a marker.
- **Must** — Allow any compatible Component to use an applicable Technical Purpose.
- **Must** — Omit a technical reference from a Component Profile when that reference is inapplicable.
- **Never** — Group a language package by Component identity or let a Technical Purpose transfer conceptual responsibility.
- **Never** — Duplicate concrete technical selections in a participating Component or copy Platform Launch Item definitions into Development.

**Every Component offers its work as Operations on one Public Interface**

- **Must** — Publish exactly one Public Interface per Component and offer its work there as Operations.
- **Must** — Declare for every Operation what it accepts, what it returns, and which outcomes it can produce.
- **Must** — Group a Component's Operations into Categories when their number makes grouping useful, with the Category grouping only.
- **Never** — Let a consumer reach a Component's work by any route other than an Operation on its Public Interface.
