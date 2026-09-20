# Implementation Module Guide

This Guide explains the Implementation Module. The Interface and each subject's Definition remain authoritative.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
   - **[Development](#development)**
   - **[Process](#process)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
   - **[Implementation has Development and Process Subsystems](#implementation-has-development-and-process-subsystems)**
   - **[Each subject is defined by one Definition and one Preferences file](#each-subject-is-defined-by-one-definition-and-one-preferences-file)**
   - **[Development and Process retain separate ownership](#development-and-process-retain-separate-ownership)**
9. **[At a Glance](#at-a-glance)**

<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implementation is the reusable programming perspective applied to a Target. It has two distinct Subsystems: Development defines the product being built, and Process controls the work that builds, evaluates, and records it.

### Purpose

This Guide explains the Module's structure and keeps the Human's understanding of its two Subsystems available to later readers.

### How It Works

The Definition is authoritative for mandatory meaning and Principles. Preferences hold current choices. Skills operate under the authority of the relevant subject.

<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation** — the reusable Module that defines how a Target is built and how implementation work is controlled.
- **Development** — the Subsystem that defines the product Components, their composition, and technical realization.
- **Process** — the Subsystem that defines configuration, planning, review, and operational recording.
- **Subsystem** — a major part of Implementation with separate ownership.
- **Component** — a bounded subject within a Subsystem with its own Definition and Preferences.
- **Definition** — the authoritative description of a subject's Understanding, relationships, boundaries, and mandatory Principles.
- **Preference** — a human-owned choice or default used where a higher authority is silent; it never overrides a Principle.
- **Subject** — any Implementation Subsystem or Component described by a Definition and Preferences file.

<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Implementation
└── Subsystems
    ├── Development
    └── Process
```

### Development

Development defines how independent product Components form one application system. It owns their composition, Component Profiles, Connections, shared technical catalogues, and cross-cutting standards.

```yaml
name: Development
definition: .interface/implementation/development/definition.md
preferences: .interface/implementation/development/preferences.yaml
responsibility: The product composition and technical realization of the independent Components that form the Target application.
```

→ [Definition](development/definition.md)<br>
→ [Preferences](development/preferences.yaml)

Model defines shared domain meaning and Domain Definitions. Database owns persistence and the public operations for stored data. Logic owns application Behaviour and exposes it through its Public Interface. API publishes the application's external API through Logic. Presentation presents the application through capabilities published by Logic. Platform defines how completed Development Components are prepared and brought online.

### Process

Process defines how work on Development is configured, planned, reviewed, and recorded. It owns no product Behaviour or Source.

```yaml
name: Process
definition: .interface/implementation/process/definition.md
preferences: .interface/implementation/process/preferences.yaml
responsibility: The configuration, planning, review, and operational recording of Implementation work.
```

→ [Definition](process/definition.md)<br>
→ [Preferences](process/preferences.yaml)

Configure prepares the operational Config records. Plan turns Target phases into bounded, understandable, and verifiable activities. Review establishes whether selected-phase work satisfies its applicable authorities and owns recorded Findings. State records aggregate operational position, progress, outcomes, History, Blockers, and Open Questions. The remaining Process Components coordinate the lifecycle around these responsibilities.

<br><br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target** — applies current Target intent and phase requirements without becoming another Target definition.
- **Consumed by operational Skills** — supplies the Development and Process authorities used while implementation work is performed.
- **Contains Development and Process** — defines the product and operational ownership boundaries used by the Interface.
- **Contains one Definition and one Preferences file per subject** — keeps each subject's meaning separate from its current choices.

<br><br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

Development owns product responsibilities. Process owns configuration, planning, review, and operational records. Neither Subsystem replaces the other.

<br><br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Technical choices and defaults belong to the Preferences file of the subject that owns them. Shared choices that genuinely span Development and Process would belong to a shared Implementation Preferences file. The shape of a generated operational record belongs to its Schema.

No shared Implementation choices are currently declared; Development and Process subjects own their specific choices. Subject Preferences remain human-owned, are read in `selected`, `options`, `settings` order, and never override an explicit Target value or an applicable Definition Principle.

<br><br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Definition and Principles of each subject are authoritative for its meaning and mandatory rules. Preferences never override them. This Guide explains and maps those sources; it does not become a second authority.

<br><br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

The mandatory Principles are stated by the Definition files of the owning subjects and summarized here for the Implementation Module. Those Definitions remain authoritative.

### Implementation has Development and Process Subsystems

**Rule:** Implementation consists of two top-level Subsystems: Development, which governs the product being built, and Process, which governs the work that configures, plans, reviews, and records that build. Neither Subsystem replaces the other.

**Why:** Product architecture and work control require different ownership while still needing one reusable Implementation perspective with explicit Subsystems.

**Boundary:** Development does not own Process records, and Process does not own product Behaviour, Source, or public interfaces.

### Each subject is defined by one Definition and one Preferences file

**Rule:** Every Implementation Subsystem and Component has one `definition.md` and one `preferences.yaml`. The Definition carries its Understanding and mandatory Principles; Preferences carry its choices, defaults, and realization conventions.

**Why:** A stable pair separates what the subject is and must preserve from how it is preferably realized.

**Boundary:** A subject's Preferences never override its Definition, and a child subject does not duplicate the authority of its parent or sibling.

### Development and Process retain separate ownership

**Rule:** Components within Development own product responsibilities, and Components within Process own Configuration, Plan, Review, and State responsibilities. A Skill performs an operation under these owners but does not acquire ownership by writing an authorized record.

**Why:** Explicit ownership keeps product meaning, operational progress, evidence, and workflow records from becoming interchangeable.

**Boundary:** A Component within Process may inspect Development results when its responsibility requires it, but it never changes a Development-owned result directly.

<br><br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

- **Must** — keep product construction in Development and implementation control in Process.
- **Must** — keep each subject's Understanding and mandatory Principles in Definition and its choices in Preferences.
- **Must** — keep choices owned by Development or Process unless a choice genuinely spans both Subsystems.
- **Must** — read each subject's Definition and Preferences through the links above.
- **Never** — let this Guide replace a subject's Definition, Preferences, or Schema.
- **Never** — let Preferences override Definition Principles or let Development and Process replace one another's ownership.
