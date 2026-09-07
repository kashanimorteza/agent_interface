# Model Principles

Model is the Component and independent application layer that describes the domain entities and concepts from which a project is formed. It provides one shared logical meaning and one reusable implementation boundary for domain data, so that every technical Component works from the same understanding of what the project's data is instead of inventing its own.

Model owns domain representations and validation that can be determined from a Model's own data. It does not own persistence mappings, business behaviour, API transport, user-interface presentation, or deployment.

## Terms

- **Model** — one meaningful entity or concept in the project domain, together with the information, connections, and rules that belong to it.
- **Field** — one piece of information carried by a Model, described by its logical meaning rather than by a storage or transport form.
- **Relationship** — a conceptual connection between two Models, optionally naming the logical field that carries it.
- **Domain Rule** — a constraint on the valid state of a Model, declared by Model and enforced according to the data and operational context needed to evaluate it.
- **Initial Data** — the records a Model must contain when the project begins.
- **Model Package** — the independent package in which the resolved Model set is implemented and published through one public import interface.

## Relationships

- **Consumes Development** — the common package standard, package identity, and naming conventions applied to the Model Package.
- **Consumed by Database** — the logical Models, relationships, and rules that Database maps, enforces, and stores.
- **Consumed by Backend** — the shared domain meaning used by Logic, the Model identity used by Data Access, and the representations derived by API.
- **Consumed by Frontend** — the domain meaning presented to users and preserved across the Backend boundary.

Technical choices and defaults belong to Model Preferences. Model implementation applies those choices to the current project definition.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Models represent domain entities

**Rule:** Each Model represents one meaningful entity or concept in the domain. A Model explains what that entity is, what information belongs to it, how it relates to other entities, and which domain rules govern it.

**Why:** A Model is the project's shared name for a thing the project is about, so every Component that touches that thing reasons about the same subject.

**Boundary:** Models describe the project domain rather than source-code classes, database tables, API resources, forms, pages, or framework objects.

<br>

## 2. Model is an independent shared package

**Rule:** The resolved Model set is implemented as its own package with a documented public import interface. Every resolved Model is exposed through that interface exactly once, using an ecosystem-compatible public symbol without changing its logical identity. Compatible application layers import this package rather than maintaining private copies of the same Models. A consumer that cannot import the package directly uses a representation derived from the same shared Model definitions through its declared layer interface.

**Why:** One importable definition keeps every layer's understanding of a Model identical, and lets the package evolve independently while its public Model interface remains compatible.

**Boundary:** The implementation language and modeling technology of the package are resolved through Model Preferences, while its package identity and general package conventions are coordinated through Development.

<br>

## 3. The logical Model connects persistence and APIs

**Rule:** The Model Component is the shared logical source for Components that need domain data. In particular, it connects the meaning of data persisted by the Database with the meaning of data accepted and exposed by APIs. Backend, Frontend, Database, and other Components may derive technical representations for their own operations. Each included field and relationship remains traceable to the shared definition and preserves its logical meaning. A representation may contain an operation-appropriate subset of fields, such as partial input or an output that excludes credentials. Omitting a field from a representation does not remove it from the Model or weaken the rules governing the resulting domain state.

**Why:** The Database determines how a Model and its declared relationships and rules are physically mapped, enforced, stored, and retrieved, while an API determines how that Model is received, validated for transport, and presented to consumers. Without one logical source between them, the two sides drift into different meanings for the same data.

**Boundary:** Neither side independently redefines the Model's logical fields, relationships, rules, or domain meaning. A technical Component owns the shape of its derived input and output representations and any implementation detail needed within its boundary. Model does not prescribe those transport or presentation shapes, and a partial representation is not a complete domain state.

<br>

## 4. Fields express domain data

**Rule:** Fields describe the information carried by a Model. Their logical type, identity, uniqueness, optionality, default behaviour, credential nature, and meaning may be expressed when applicable. Absence from input, an explicitly null value, and a value awaiting declared generation are distinct. A field required in the resulting domain state need not be supplied by a caller when the operation permits its omission and an applicable default or declared generation supplies it. In a partial update, an omitted field remains unchanged; an explicitly null value is an attempted value change and is valid only when the field permits it. Once required defaults or generation have been resolved, the resulting state must satisfy all applicable Model rules.

**Why:** The field is the level at which domain data acquires meaning, so a Component that reads a field knows what it holds without consulting an implementation.

**Boundary:** Field definitions remain independent of a particular programming language, storage engine, API framework, or user-interface technology. Physical columns, transport formats, widgets, and framework-specific declarations belong to their respective Components. The responsible technical Component supplies generated values; Model declares their meaning and requirements without performing persistence or inventing placeholder values to satisfy a required field.

<br>

## 5. Relationships express domain connections

**Rule:** Relationships describe how Models are conceptually connected and, when needed, identify the logical field that carries that connection.

**Why:** A connection between entities is part of what the domain means, so it is stated once with the Models rather than rediscovered by each Component that traverses it.

**Boundary:** The physical realization of a relationship, including database constraints and storage-specific referential behaviour, belongs to the Database Component. API exposure and presentation belong to their respective Components.

<br>

## 6. Domain rules and initial data remain part of the Model

**Rule:** A Model may contain rules that constrain its valid domain state and initial records that must exist when the project begins. Model implements validation determinable from its own data, including field-value constraints and relationships between values within the same Model. Rules requiring application context or an operation's conditions are enforced by Backend Logic using the shared Model rules. Rules requiring stored state, such as uniqueness across records and the existence of a referenced record, are guaranteed by Database. Each rule remains traceable to its Model declaration regardless of where it is enforced. Initial data remains a logical declaration whose insertion and permitted value generation are performed by Database.

**Why:** A rule that limits valid state, and a record that must exist from the start, describe the domain itself rather than any one technology that stores or exposes it.

**Boundary:** Model validation does not query Database, call external services, or implement application operations. Consumer-side checks may provide earlier feedback but do not replace Database's enforcement of persistence constraints. Consumers reuse Model validation rather than maintaining competing copies of the same rules.

<br>

## 7. Field defaults complete unspecified properties

**Rule:** Model Preferences may supply missing properties of fields already present in a Model definition. An explicit Model property always takes precedence over its default, including an explicit false or null value. Defaults are applied separately to each unspecified property, so a partially defined field can be completed without replacing its stated meaning.

**Why:** Completing unstated properties keeps a Model definition short without letting a default silently outrank something the project actually stated.

**Boundary:** A default entry does not introduce a field into a Model or require every entity to contain it. A field-name pattern alone does not define a domain relationship. Technical Components consume the resulting resolved Model rather than independently adding their own common fields.

<br>

## At a Glance

- **Must** — each Model represents one meaningful domain entity or concept and explains its information, connections, and rules *(1)*
- **Never** — a Model describes a source-code class, database table, API resource, form, page, or framework object *(1)*
- **Must** — the resolved Model set is one package with a documented public import interface exposing each Model exactly once *(2)*
- **Must** — compatible layers import the shared package instead of keeping private copies of the same Models *(2)*
- **Must** — derived representations preserve the shared Model identity and the meaning of the fields and relationships they include *(3)*
- **Must** — field subsets follow the operation's needs without weakening the rules governing the resulting domain state *(3)*
- **Never** — a technical Component redefines the identity or meaning of a Model *(3)*
- **Must** — a field expresses its logical type, identity, uniqueness, optionality, default behaviour, credential nature, and meaning when applicable *(4)*
- **Must** — absent input, explicit null, and pending generated values remain distinct; omitted fields in partial updates remain unchanged *(4)*
- **Must** — a required field omitted under the operation's rules is supplied by an applicable default or declared generation before the resulting state is treated as complete *(4)*
- **Never** — a placeholder value substitutes for a required value or its declared generation *(4)*
- **Never** — a field definition depends on a programming language, storage engine, API framework, or user-interface technology *(4)*
- **Must** — a relationship states how Models are connected and, when needed, the logical field that carries it *(5)*
- **Never** — Model resolves the physical realization of a relationship *(5)*
- **Must** — domain rules and initial data remain part of the Model as logical declarations *(6)*
- **Must** — Model validates its own data, Backend Logic enforces context-dependent rules, and Database guarantees constraints requiring stored state *(6)*
- **Must** — consumers reuse Model validation and keep enforcement traceable to its declaration *(6)*
- **Must** — Database inserts initial data and supplies its permitted generated values *(6)*
- **Never** — Model validation queries storage, calls external services, or implements application operations *(6)*
- **Never** — consumer-side checks replace Database's enforcement of persistence constraints *(6)*
- **Must** — an explicit Model property takes precedence over a default, including an explicit false or null *(7)*
- **Never** — a default introduces a field into a Model, and a name pattern alone never defines a relationship *(7)*
