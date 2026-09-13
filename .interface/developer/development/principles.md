# Development Principles

Development defines the fixed high-level composition through which independent peer Developer Components form one application system. It owns the catalogue of participating Components, their roles and roots, the allowed dependency graph, and the shared rules that make their boundaries work together.

Development owns composition rather than the internal design of Model, Database, Backend, Frontend, or Platform. Each of those Components retains authority over the details inside its boundary.

<br>

## Terms

- **Participating Component** — one of Model, Database, Backend, Frontend, or Platform as a peer Developer Component governed by Development's composition standard.
- **Application Package** — a Developer Component of type `library` or `executable`, with an owned implementation boundary and a Public Interface appropriate to its type.
- **Component Type** — one of `library`, `executable`, or `guideline`: a library is consumed through imports, an executable runs as an application or service, and a guideline defines standards, configuration, instructions, or supporting artifacts without being an Application Package.
- **Public Interface** — the provider-owned surface intended for consumers, including any public classes, types, functions, APIs, commands, or other supported entry points.
- **Connection** — one direct dependency from a consumer Component to a provider Component.
- **Runtime Configuration** — the runtime settings and secret references owned within an Application Package boundary.
- **Cross-cutting Capability** — a shared capability whose application to more than one Component requires Development-level coordination.

<br>

## Relationships

- **Consumes nothing** — Development defines the composition standard without consuming the internal definitions of another Component.
- **Consumed by Model, Database, Backend, Frontend, and Platform** — these Components use Development's catalogue, boundaries, Connections, and shared rules.

<br>

Development publication and Cross-cutting Capability defaults belong to Development Preferences. Internal technical choices belong to the Preferences of the Component that owns them, and implementation applies those choices to the current project definition.

<br>

Every statement here is mandatory. A Developer Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Development fixes the participating Component catalogue

**Rule:** Development composes the following peer Participating Components. Their canonical identifiers, names, repository-relative root paths, types, and high-level roles are fixed; neither a project nor another Component changes them.

| Component | Name | Root path | Type | High-level role |
| --- | --- | --- | --- | --- |
| `model` | `model` | `model` | `library` | Defines the system's shared Models. |
| `database` | `database` | `database` | `library` | Owns persistence and access to stored data. |
| `backend` | `backend` | `backend` | `executable` | Provides server-side application services. |
| `frontend` | `frontend` | `frontend` | `executable` | Provides the user-facing application through Backend services. |
| `platform` | `platform` | `platform` | `guideline` | Defines Environment and Launch standards and their supporting artifacts. |

Each root path identifies the Component's root directory relative to the repository root, never an absolute path or an individual file. Root paths are unique, do not overlap or nest inside one another, and contain the files owned by their Components. Each Component owns the internal organization below its root.

**Why:** One stable catalogue gives every Component and Connection the same identity while preserving physically separate boundaries.

**Boundary:** The catalogue does not make a Participating Component a child of Development; all remain peer Developer Components with independent ownership. Another Participating Component exists only after Development Principles explicitly add it. Internal structures, services, tools, or packages created by a Component do not automatically become Participating Components.

<br>

## 2. Every Application Package is logically independent

**Rule:** Each Application Package has one cohesive responsibility and owns its internal implementation, Runtime Configuration, and Public Interface. A consumer may install or import a provider Application Package, its public classes, types, functions, or other public resources when an authorized Connection identifies that provider. Such use remains limited to the provider's Public Interface and never creates logical ownership of its internals. Each Component may organize additional structures, services, tools, or packages inside its own root as its own Principles and Preferences permit.

**Why:** Logical independence lets an Application Package evolve or be replaced without forbidding the explicit dependencies required to compose a working system.

**Boundary:** Development does not prescribe internal nesting, source layout, dependency-management mechanism, or installation method.

<br>

## 3. Consumers use only provider-owned Public Interfaces

**Rule:** Every cross-Component interaction uses a Public Interface owned by the provider. The provider determines how many public classes, types, functions, APIs, commands, or other entry points it exposes and how they are implemented. A Connection identifies only its consumer and provider; it does not duplicate the provider's interface definition.

**Why:** Consumers can safely depend on a supported contract while providers remain free to change private implementation.

**Boundary:** A consumer never reads, changes, or depends on another Component's private implementation, internal storage, private resources, or internal Runtime Configuration. Development defines the interface standard but not the contents or implementation method of a Component's Public Interface.

<br>

## 4. The application dependency graph is fixed, explicit, and acyclic

**Rule:** The application architecture permits exactly these direct Connections:

| Connection | Consumer | Provider |
| --- | --- | --- |
| `frontend_to_backend` | `frontend` | `backend` |
| `backend_to_database` | `backend` | `database` |
| `backend_to_model` | `backend` | `model` |
| `database_to_model` | `database` | `model` |

The direction runs from consumer to provider and represents dependency, not the direction in which request and response data travel. Connections are direct, non-transitive, and acyclic. Every direct use of another Application Package requires its own listed Connection; an indirect path never grants direct access. Platform is a guideline Component and does not participate in the runtime Connection graph.

**Why:** A complete directed graph makes dependency ownership visible and prevents hidden, circular, or accidentally inherited coupling.

**Boundary:** A provider's response to its consumer does not create a reverse Connection. A Connection does not select a transport or limit the provider to one Public Interface.

<br>

## 6. Cross-cutting Capabilities are activated through `applies_to`

**Rule:** The Development Preferences file declares each Cross-cutting Capability with one `applies_to` list. An empty list means the capability is inactive; a non-empty list activates it only for the listed Components. Every entry is a unique canonical Component identifier from the fixed catalogue. Each listed Component applies the shared capability requirement while retaining ownership of its internal implementation.

**Why:** One applicability list gives shared behavior a single coordination point without transferring internal implementation ownership to Development.

**Boundary:** Development does not use a separate `enabled` value. A Component not listed in `applies_to` does not inherit that capability, and behavior that is wholly internal to one Component remains owned there.

<br>

## 9. Every Component has complete, safe, and derived documentation

**Rule:** Every Participating Component is generated with `<component_root>/README.md`. Its README explains the Component's responsibility, supported surface, non-secret configuration, applicable setup and use, and practical executable examples. An Application Package documents its Public Interface, installation and run or usage method, and dependencies derived from the fixed Connection graph. Platform documents its Environment and Launch inputs, outputs, supporting artifacts, and usage. Documentation remains consistent with public behavior and enables a human or Agent to understand and use the Component without inspecting its private implementation.

Documentation may contain code and may demonstrate how an API key or other secret is supplied, but it uses placeholders, environment-variable names, or safe secret references and never contains a real usable credential, token, or secret value. When public usage changes, the README changes with it.

**Why:** A well-documented boundary remains understandable during initial generation and later maintenance without exposing private implementation or sensitive values.

**Boundary:** README files are derived explanations. They may support later Understanding, but they never replace or override Principles, Preferences, the implemented Public Interface, or another authoritative project source.

<br>

## 10. Unstated Development decisions follow one precedence order

**Rule:** When the project leaves a Development-owned decision unstated, the decision applies Development Principles first, Development Preferences second, and professional judgment last.

**Why:** A short precedence order preserves mandatory architecture, uses the Human's defaults, and leaves judgment only for a genuine gap.

**Boundary:** Professional judgment never overrides a Development Principle or an applicable Development Preference. Component-internal decisions remain governed by that Component's own Principles and Preferences.

<br>

## 11. Runtime Configuration ownership remains inside its boundary

**Rule:** Each Application Package owns the contract and internal representation of its Runtime Configuration. Platform owns Environment and Launch configuration and may deliver required runtime values to an Application Package through its documented inputs. Runtime secret values remain in appropriate secret sources rather than Interface files or documentation.

**Why:** Explicit configuration ownership lets Platform launch the system without taking ownership of application internals or exposing secrets.

**Boundary:** One Application Package never directly reads or modifies another's internal Runtime Configuration. Platform may coordinate delivery, but it never redefines the internal configuration contract owned by an Application Package.

<br>

## 12. Public Interface changes propagate through direct consumers

**Rule:** A provider may change its private implementation without requiring consumer changes while its Public Interface remains compatible. When a Public Interface changes, every direct consumer identified by the Connection graph is reviewed and, when affected, regenerated or updated and verified. Propagation continues through later Connections only when an affected consumer's own Public Interface also changes.

**Why:** Change follows the actual dependency graph, keeping consumers correct without rebuilding unrelated Components.

**Boundary:** An internal provider change with no Public Interface effect does not trigger consumer work, and a Public Interface change does not authorize changes outside the affected dependency path.

<br>

## At a Glance

- **Must** — Compose the fixed peer Model, Database, Backend, Frontend, and Platform catalogue with its exact identifiers, names, roots, types, and roles. *(1)*
- **Never** — Let a project or Component override the fixed catalogue. *(1)*
- **Must** — Interpret every Component path as a unique, non-absolute, non-overlapping repository-relative root containing that Component's files, while each Component owns its internal organization below that root. *(1)*
- **Never** — Treat a Participating Component as Development's child or an internal item as a Participating Component unless Development Principles explicitly add it. *(1)*
- **Must** — Keep every Application Package cohesive and responsible for its implementation, Runtime Configuration, and Public Interface. *(2)*
- **Must** — Limit every authorized import or installation dependency to the provider's Public Interface. *(2)*
- **Never** — Turn use of a provider into ownership of or coupling to its internals. *(2)*
- **Never** — Let Development prescribe a Component's internal structure, dependency management, or installation method. *(2)*
- **Must** — Route every cross-Component interaction through a provider-owned Public Interface, while each Connection identifies only its consumer and provider without duplicating the interface definition. *(3)*
- **Must** — Let each provider own the number, shape, and implementation of its Public Interfaces. *(3)*
- **Never** — Access another Component's private implementation, storage, resources, or internal Runtime Configuration. *(3)*
- **Must** — Use only the four fixed direct consumer-to-provider Connections. *(4)*
- **Must** — Treat Connections as direct, non-transitive, acyclic dependencies rather than request-and-response data directions; a provider response creates no reverse Connection, and a Connection selects no transport. *(4)*
- **Never** — Use an unlisted direct dependency or include Platform in the runtime Connection graph. *(4)*
- **Must** — Activate each Cross-cutting Capability only for the unique canonical Component identifiers in its `applies_to` list, while each listed Component retains ownership of its internal implementation. *(6)*
- **Never** — Use a separate `enabled` value or apply a Cross-cutting Capability to an unlisted Component. *(6)*
- **Must** — Generate `<component_root>/README.md` for every Participating Component with the content appropriate to its type. *(9)*
- **Must** — Keep each README consistent with public behavior and sufficient for human or Agent understanding and use. *(9)*
- **Never** — Put a real credential, token, or secret value in documentation. *(9)*
- **Never** — Treat derived README content as a replacement for an authoritative source. *(9)*
- **Must** — Resolve an unstated Development-owned decision through Principles, Preferences, then professional judgment, while Component-internal decisions remain governed by that Component's own Principles and Preferences. *(10)*
- **Never** — Let professional judgment override a Development Principle or applicable Preference. *(10)*
- **Must** — Keep each Application Package's Runtime Configuration contract and representation within its boundary. *(11)*
- **Must** — Let Platform coordinate runtime value delivery through documented Environment and Launch inputs. *(11)*
- **Never** — Store runtime secrets in Interface files or documentation, or let another Component redefine or directly modify owned Runtime Configuration. *(11)*
- **Must** — Review, update or regenerate when affected, and verify every direct consumer after a provider's Public Interface changes. *(12)*
- **Must** — Continue propagation only when an affected consumer's own Public Interface changes. *(12)*
- **Never** — Trigger consumer work for a private change that preserves the Public Interface or change Components outside the affected dependency path. *(12)*
