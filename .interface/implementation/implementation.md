# Implementation Module Guide

Implementation is the Module that defines how a Target is built and how that work is configured, planned, reviewed, and recorded.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Subsystems](#subsystems)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implementation is the reusable programming perspective applied to a Target. It has two distinct Subsystems: Development defines the product being built, and Operations controls the work that builds, evaluates, and records it.

### Purpose

This Guide explains the Module's structure and keeps the Human's understanding of its two Subsystems available to later readers.

### How It Works

The Definition is authoritative for mandatory meaning and Principles. Preferences hold current choices. Skills operate under the authority of the relevant subject.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation** — the reusable Module that defines how a Target is built and how implementation work is controlled.
- **Development** — the Subsystem that defines the product Components, their composition, and technical realization.
- **Operations** — the Subsystem that defines configuration, planning, development, review, implementation, launch, reset, coordination, and operational recording.
- **Subsystem** — a major part of Implementation with separate ownership.
- **Component** — a bounded subject within a Subsystem with its own Definition and Preferences.
- **Definition** — the authoritative description of a subject's Understanding, relationships, boundaries, and mandatory Principles.
- **Preference** — a human-owned choice or default used where a higher authority is silent; it never overrides a Principle.
- **Subject** — any Implementation Subsystem or Component described by a Definition and Preferences file.

<br>

<!--------------------------------------------------------------------------------- Subsystems --->
## Subsystems

```text
Subsystems
├── Development
└── Operations
```

The Implementation Module has two Subsystems: Development and Operations. Their Components are defined inside their respective Subsystem Definitions and are not expanded in this Module-level map.

### Development

Development defines how independent product Components form one application system. It owns their composition, Component Profiles, Connections, shared technical catalogues, and cross-cutting standards.

Responsibility: The product composition and technical realization of the independent Components that form the Target application.

→ [Definition of Development](development/development.md)<br>
→ [Preferences of Development](development/development.yaml)

Model defines shared domain meaning and Domain Definitions. Database owns persistence and the public operations for stored data. Logic owns application Behaviour and exposes it through its Public Interface. API publishes the application's external API through Logic. Presentation presents the application through capabilities published by Logic. Platform defines how completed Development Components are prepared and brought online.

### Operations

Operations defines how work on Development is configured, planned, developed, reviewed, implemented, launched, reset, coordinated, and recorded. It owns no product Behaviour or Source.

Responsibility: The configuration, planning, review, and operational recording of Implementation work.

→ [Definition of Operations](operations/operations.md)<br>
→ [Preferences of Operations](operations/operations.yaml)

Configure prepares the operational Config records. Plan turns Target phases into bounded, understandable, and verifiable activities. Develop performs authorized implementation work. Review establishes whether selected-phase work satisfies its applicable authorities and owns recorded Findings. Implement coordinates the workflow, Launch activates a completed implementation, Reset reconciles an authorized scope, and State records aggregate operational position, progress, outcomes, History, Blockers, and Open Questions. The remaining Operation Components coordinate the lifecycle around these responsibilities.

These Operation Components realize the Implementation-owned Operations. Agent Native Sync remains a Foundation operation because it synchronizes the Agent Module into the selected Agent Native rather than performing Implementation work.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target** — applies current Target intent and phase requirements without becoming another Target definition.
- **Consumed by operational Skills** — supplies the Development and Operations authorities used while implementation work is performed.
- **Contains Development and Operations** — defines the product and operational ownership boundaries used by the Interface.
- **Contains one Definition and one Preferences file per subject** — keeps each subject's meaning separate from its current choices.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

Development owns product responsibilities. Operations owns configuration, planning, development, review, implementation, launch, reset, coordination, and operational records. Neither Subsystem replaces the other.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Technical choices and defaults belong to the Preferences file of the subject that owns them. Shared choices that genuinely span Development and Operations would belong to a shared Implementation Preferences file. The shape of a generated operational record belongs to its Schema.

No shared Implementation choices are currently declared; Development and Operations subjects own their specific choices. Subject Preferences remain human-owned, are read in `selected`, `options`, `settings` order, and never override an explicit Target value or an applicable Definition Principle.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Definition and Principles of each subject are authoritative for its meaning and mandatory rules. Preferences never override them. This Guide explains and maps those sources; it does not become a second authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

The mandatory Principles are stated by the Definition files of the owning subjects and summarized here for the Implementation Module. Those Definitions remain authoritative.

### Implementation has Development and Operations Subsystems

**Rule:** Implementation consists of two top-level Subsystems: Development, which governs the product being built, and Operations, which governs the work that configures, plans, develops, reviews, implements, launches, resets, coordinates, and records that build. Neither Subsystem replaces the other.

**Why:** Product architecture and work control require different ownership while still needing one reusable Implementation perspective with explicit Subsystems.

**Boundary:** Development does not own Operations records, and Operations does not own product Behaviour, Source, or public interfaces.

### Each subject is defined by one Definition and one Preferences file

**Rule:** Every Implementation Subsystem and Component has one `<subject>.md` and one `<subject>.yaml`. The Markdown file carries its Understanding and mandatory Principles; the YAML file carries its choices, defaults, and realization conventions.

**Why:** A stable pair separates what the subject is and must preserve from how it is preferably realized.

**Boundary:** A subject's Preferences never override its Definition, and a child subject does not duplicate the authority of its parent or sibling.

### Development and Operations retain separate ownership

**Rule:** Components within Development own product responsibilities, and Components within Operations own Configure, Plan, Develop, Review, Implement, Launch, Reset, and State responsibilities. A Skill performs an operation under these owners but does not acquire ownership by writing an authorized record.

**Why:** Explicit ownership keeps product meaning, operational progress, evidence, and workflow records from becoming interchangeable.

**Boundary:** A Component within Operations may inspect Development results when its responsibility requires it, but it never changes a Development-owned result directly.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

- **Must** — keep product construction in Development and implementation control in Operations.
- **Must** — keep each subject's Understanding and mandatory Principles in Definition and its choices in Preferences.
- **Must** — keep choices owned by Development or Operations unless a choice genuinely spans both Subsystems.
- **Must** — read each subject's Definition and Preferences through the links above.
- **Never** — let this Guide replace a subject's Definition, Preferences, or Schema.
- **Never** — let Preferences override Definition Principles or let Development and Operations replace one another's ownership.
