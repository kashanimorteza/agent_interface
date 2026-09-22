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

Implementation is the reusable programming perspective applied to a Target through two Subsystems: Development defines the product being built, and Operations controls the work that configures, builds, evaluates, activates, and records it. The corresponding Operation Components' Definitions and Preferences are the source for the operational Skills that perform that work.

### Purpose

This Guide explains the Module's structure and keeps the Human's understanding of its two Subsystems available to later readers.

It also maps the Development and Operations Subsystems and their Components so that product authorities, operational Skills, generated records, and State Operation Logs remain connected without duplicating their meaning in the Interface document.

### How It Works

Development supplies the product authorities, and Operations applies them through its owned workflow. Skills act under the relevant subject and record execution in State; a subject-owned Config record keeps detailed results when one exists.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation** — the reusable Module that defines how a Target is built and how implementation work is controlled.
- **Development** — the Subsystem that defines the product Components, their composition, and technical realization.
- **Operations** — the Subsystem that defines configuration, planning, development, review, implementation, launch, reset, coordination, and operational recording.
- **Subsystem** — a major part of Implementation with separate ownership.
- **Component** — a bounded subject within a Subsystem with its own Definition and Preferences.
- **Definition** — the authoritative description of a Subsystem or Component's Understanding, relationships, boundaries, and mandatory Principles.
- **Preference** — a human-owned choice or default used where a higher authority is silent; it never overrides a Principle.
- **Subject** — any Implementation Subsystem or Component described by a Definition and, when it has choices, a Preferences file.

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

Development composes the independent product Components into one application system through shared profiles, connections, technical catalogues, and standards.

Responsibility: The product composition and technical realization of the independent Components that form the Target application.

→ [Definition of Development](development/development.md)<br>
→ [Preferences of Development](development/development.yaml)

### Operations

Operations governs how Development work is configured, planned, developed, reviewed, implemented, launched, reset, coordinated, and recorded without owning product Behaviour or Source.

Responsibility: The configuration, planning, development, review, implementation, launch, reset, coordination, and recording of Implementation work.

→ [Definition of Operations](operations/operations.md)<br>
→ [Preferences of Operations](operations/operations.yaml)

Its Operation Components realize these responsibilities; Agent Native Sync remains a Foundation operation because it synchronizes the Agent Module into the selected Agent Native rather than performing Implementation work.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target** — applies current Target intent and phase requirements without becoming another Target definition.
- **Consumed by operational Skills** — supplies the Development and Operations authorities used while implementation work is performed.
- **Contains Development and Operations** — defines the product and operational ownership boundaries used by the Interface.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

Development owns product responsibilities. Operations owns configuration, planning, development, review, implementation, launch, reset, coordination, and operational records. Neither Subsystem replaces the other.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Technical choices and defaults belong to the Preferences file of the subject that owns them. The shape of a generated operational record belongs to its Schema, while State owns the common Operation Log shape.

Development and Operations subjects own their specific choices. Subject Preferences remain human-owned and are read in `selected`, `options`, `settings` order.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Definition and Principles of each Subsystem or Component are authoritative for its meaning and mandatory rules. Preferences never override them. This Guide explains and maps those sources; it does not become a second authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

The mandatory Principles are stated by the Definition files of the owning subjects and summarized here for the Implementation Module. Those Definitions remain authoritative.

### Implementation has Development and Operations Subsystems

**Rule:** Implementation consists of two top-level Subsystems: Development, which governs the product being built, and Operations, which governs the work that configures, plans, develops, reviews, implements, launches, resets, coordinates, and records that build. Neither Subsystem replaces the other.

**Why:** Product architecture and work control require different ownership while still needing one reusable Implementation perspective with explicit Subsystems.

**Boundary:** Development does not own Operations records, and Operations does not own product Behaviour, Source, or public interfaces.

### Each Subsystem and Component has an explicit source pair

**Rule:** Every Implementation Subsystem and Component has one authoritative Definition and, when it has choices, one Preferences source. The Definition carries its Understanding and mandatory Principles; Preferences carry its choices, defaults, and realization conventions.

**Why:** A stable source pair separates what the subject is and must preserve from how it is preferably realized, while allowing subjects with no choices to keep Preferences empty or absent by design.

**Boundary:** A subject's Preferences never override its Definition, and a child subject does not duplicate the authority of its parent or sibling.

### Operations separate execution logs from detailed records

**Rule:** Every Operation records execution metadata, Skills used, available timing and token measurements, outcome, and a concise report in State. A Component-owned Config record stores detailed operational content when the Operation produces one, such as Plan or Task records. Review Findings and resolutions remain in the State Log Entry's `data`.

**Why:** State provides the shared operational history that later Operations need, while each owned record preserves the detail without turning State into a duplicate of every Component record.

**Boundary:** An Operation Log never replaces a Component-owned record, and a Component-owned record never replaces the Operation Log. State Log `data` may carry Operation-specific content when no separate Config record exists.

### Development and Operations retain separate ownership

**Rule:** Components within Development own product responsibilities, and Components within Operations own Configure, Plan, Develop, Review, Implement, Launch, Reset, and State responsibilities. A Skill performs an operation under these owners but does not acquire ownership by writing an authorized record.

**Why:** Explicit ownership keeps product meaning, operational progress, evidence, and workflow records from becoming interchangeable.

**Boundary:** A Component within Operations may inspect Development results when its responsibility requires it, but it never changes a Development-owned result directly.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

- **Must** — keep product construction in Development and implementation control in Operations.
- **Must** — keep each subject's Understanding and mandatory Principles in Definition and its choices in Preferences.
- **Must** — record every Operation's execution metadata and concise report in State, keeping detailed Config results in their owning records and Operation-specific Log data in State when no separate record exists.
- **Must** — keep choices owned by Development or Operations unless a choice genuinely spans both Subsystems.
- **Must** — read each Subsystem's Definition and Preferences through the links above.
- **Never** — let this Guide replace a subject's Definition, Preferences, or Schema.
- **Never** — let Preferences override Definition Principles or let Development and Operations replace one another's ownership.
