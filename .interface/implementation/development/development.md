# Development Definition

Development is the Implementation Subsystem that coordinates the Components of one application through shared defaults, direct Connections, documentation standards, and the Application Manifest.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Components](#components)**
4. **[Relationships](#relationships)**
5. **[Layering](#layering)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Development coordinates independent Components into one application. It owns their shared defaults, direct Connections, documentation standards, and the generated Application Manifest. Each Component owns its own meaning, implementation, technical choices, and Public Interface.

### Purpose

Components need one place for the defaults and relationships they genuinely share. Development supplies that common context without duplicating a Component's own configuration.

### How It Works

Each Component resolves its own Preferences first, then uses a Development Default only when its own Preference leaves a shared choice unstated. Components interact only through their Public Interfaces according to the declared Connection graph. The Application Manifest in Config is generated from those public facts.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Component** — one peer part of the Development Subsystem with its own Definition, Preferences, and Public Interface.
- **Development Default** — a shared value a Component may use only when its own Preferences do not select that value.
- **Public Interface** — the Component-owned surface through which another Component uses it; each Component explains its own public contents.
- **Connection** — one direct dependency from a consumer Component to a provider Component.
- **Application Manifest** — the generated Config record that presents the current public composition of the application.
- **Documentation Standard** — the shared rule for how every Component documents its Public Interface and safe usage.

<br>

<!--------------------------------------------------------------------------------- Components --->
## Components

```text
Components
├── Model
├── Database
├── Logic
├── API
├── Presentation
└── Platform
```

```text
Presentation → API → Logic → Database → Model
                     └──────→ Model
```

Each direct connection uses the provider Component's Public Interface.

### Model

Model defines the reusable data library used by Database and Logic.

→ [Definition of Model](model/model.md)<br>
→ [Preferences of Model](model/model.yaml)

### Database

Database realizes storage and exposes its storage capabilities through its Public Interface.

→ [Definition of Database](database/database.md)<br>
→ [Preferences of Database](database/database.yaml)

### Logic

Logic implements application behavior using the Components it connects to.

→ [Definition of Logic](logic/logic.md)<br>
→ [Preferences of Logic](logic/logic.yaml)

### API

API exposes application capabilities through its external Public Interface.

→ [Definition of API](api/api.md)<br>
→ [Preferences of API](api/api.yaml)

### Presentation

Presentation provides the user-facing application through its Public Interface.

→ [Definition of Presentation](presentation/presentation.md)<br>
→ [Preferences of Presentation](presentation/presentation.yaml)

### Platform

Platform provides the runtime and deployment foundation used by the other Components.

→ [Definition of Platform](platform/platform.md)<br>
→ [Preferences of Platform](platform/platform.yaml)

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Components use Development** — receive applicable shared defaults, the Connection graph, and the Documentation Standard.
- **Development uses Components** — derives the Application Manifest from their public composition and declared Connections.
- **Application Manifest is stored in Config** — presents the current public application composition without becoming its source of authority.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Development owns only shared coordination: defaults, Connections, documentation standards, and the Application Manifest. Each Component owns its own content, technical choices, and Public Interface. Platform owns runtime and launch details.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Development Definition Principles are mandatory. A Component's explicit Preference takes precedence over a Development Default. When neither supplies a value, compatible professional judgment applies without overriding Target meaning or an applicable Principle.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Components own their own content and technical choices

**Rule:** Each Component owns its Definition, Preferences, technical selections, implementation, and Public Interface. Development does not duplicate or redefine those details.

**Why:** Ownership stays clear and a Component can change internally without maintaining a second configuration elsewhere.

**Boundary:** Development retains only values that are genuinely shared defaults or relationships across Components.

<br>

### Development Defaults apply only when a Component is silent

**Rule:** A Component's explicit Preference takes precedence over a Development Default. Development supplies a default only when the Component leaves the shared choice unstated.

**Why:** Components can make an intentional local choice while shared defaults avoid repeated configuration.

**Boundary:** A Default never creates, replaces, or changes a Component-owned decision.

<br>

### Cross-Component use stays behind provider-owned Public Interfaces

**Rule:** Every cross-Component interaction uses the provider's Public Interface. Each provider defines and documents the public concepts it offers; a Connection records only consumer and provider.

**Why:** Consumers depend on a supported boundary while providers remain free to change private implementation.

**Boundary:** A consumer never reads, changes, or depends on another Component's private implementation, storage, or resources.

<br>

### The declared Connection graph is direct, explicit, and acyclic

**Rule:** Every permitted direct dependency is declared exactly once as a Connection in Development Preferences. Connection direction runs from consumer to provider, is direct and non-transitive, and forms no cycle.

**Why:** One directed graph makes dependency ownership visible and prevents hidden or circular coupling.

**Boundary:** A provider response creates no reverse Connection, and an indirect path never grants direct access.

<br>

### Components publish shared application metadata through the Application Manifest

**Rule:** The Application Manifest in Config is generated from the Components' non-secret public metadata and the declared Connections. It presents current public composition without becoming authoritative for Component ownership or Target meaning.

**Why:** Components have one current public view of the application without reading private files.

**Boundary:** The Application Manifest never contains credentials, secret values, private implementation details, internal storage structure, or undeclared dependencies.

<br>

### Every Component follows one documentation standard

**Rule:** Every Component documents its Public Interface, configuration, use, verification, and failures according to the Development Documentation Standard. Examples use placeholders or secret references only, never usable credentials, tokens, or secret values.

**Why:** A shared standard makes every Component understandable and safe to use.

**Boundary:** Development defines the documentation standard; each Component owns its documentation content and technology-specific examples.

<br>

### Unstated shared decisions follow one precedence order

**Rule:** Resolve an unstated shared choice in this order: explicit Component Preference, Development Default, then compatible professional judgment.

**Why:** The order preserves Component ownership while supplying shared consistency for genuine gaps.

**Boundary:** Professional judgment never overrides Target meaning, an applicable Principle, or an explicit Preference.

<br>

### Public Interface changes propagate through direct consumers

**Rule:** A provider may change private implementation without consumer changes while its Public Interface remains compatible. When a Public Interface changes, each direct consumer in the declared Connection graph is reviewed and updated or regenerated when affected.

**Why:** Change follows actual dependencies without rebuilding unrelated Components.

**Boundary:** A private change with no Public Interface effect triggers no consumer work, and a public change authorizes no change outside the affected dependency path.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Components own their own content and technical choices**

- **Must** — Keep Component Definition, Preferences, technical choices, implementation, and Public Interface with its owner.
- **Never** — Duplicate or redefine Component-owned details in Development.

**Development Defaults apply only when a Component is silent**

- **Must** — Use an explicit Component Preference before a Development Default.
- **Never** — Let a Default replace a Component-owned decision.

**Cross-Component use stays behind provider-owned Public Interfaces**

- **Must** — Use a provider only through its Public Interface.
- **Never** — Depend on another Component's private resources.

**The declared Connection graph is direct, explicit, and acyclic**

- **Must** — Declare every direct dependency once in Development.
- **Never** — Infer direct access from an indirect path or create a dependency cycle.

**Components publish shared application metadata through the Application Manifest**

- **Must** — Generate the Config Manifest from public Component metadata and Connections.
- **Never** — Put secrets or private implementation detail in the Manifest.

**Every Component follows one documentation standard**

- **Must** — Document each Public Interface, configuration, use, verification, and failures safely.
- **Never** — Include a usable secret in documentation.
