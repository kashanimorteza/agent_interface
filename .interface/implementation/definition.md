# Implementation Definition

<br><br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Principles](#principles)**
   - **[Implementation has Development and Process parts](#implementation-has-development-and-process-parts)**
   - **[Each subject is defined by one Definition and one Preferences file](#each-subject-is-defined-by-one-definition-and-one-preferences-file)**
   - **[Development and Process retain separate ownership](#development-and-process-retain-separate-ownership)**
   - **[Implementation documentation maps subjects without replacing Definitions](#implementation-documentation-maps-subjects-without-replacing-definitions)**
6. **[At a Glance](#at-a-glance)**





<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implementation defines the reusable philosophy and standards used to build a Target and to control the work that builds it. It is independent of any particular Target or Agent.

Implementation has two parts:

- **Development** defines the product being built, its Components, their composition, and their technical realization.
- **Process** defines how implementation work is configured, planned, reviewed, and recorded.

### Purpose

Building a product requires both a coherent product architecture and a reliable way to control the work that creates it. Keeping these concerns in one Implementation Module makes the programming perspective reusable while keeping product responsibilities distinct from planning, review, configuration, and operational records.

### How It Works

Each subject in Implementation is described by a Definition and a Preferences file. Development supplies the product Components and their shared composition. Process prepares the operational records, turns Target phases into work, evaluates selected results, and records the position needed to continue. Skills perform these operations under the authorities of the relevant subjects.





<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation** — the reusable module that defines how a Target is built and how its implementation work is controlled.
- **Development** — the Implementation part that defines the product Components, their composition, and their technical realization.
- **Process** — the Implementation part that defines configuration, planning, review, and operational recording.
- **Definition** — the authoritative description of a subject's Understanding, relationships, boundaries, and mandatory Principles.
- **Preference** — a human-owned choice or default used where a higher authority is silent; it never overrides a Principle.
- **Subject** — any Implementation Module, part, or Component described by a Definition and Preferences file.




<br><br>
<!--------------------------------------------------------------------------------- Architecture --->

## Architecture

```text
Implementation
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

<br>

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

<br>

Configuration prepares and structurally reconciles operational Config and the Application Manifest. Plan turns Target phases into bounded, understandable, and verifiable activities. Review establishes whether selected-phase work satisfies its applicable authorities and owns recorded Findings. State records aggregate operational position, progress, outcomes, History, Blockers, and Open Questions.




<br><br>
<!--------------------------------------------------------------------------------- Relationships --->

## Relationships

- **Consumes Target** — applies the current Target intent and phase requirements without becoming another Target definition.
- **Consumed by operational Skills** — supplies the Development and Process authorities used while configuring, planning, developing, reviewing, launching, and recording work.
- **Provides Development and Process subjects** — exposes the product and operational ownership boundaries that the rest of the Interface uses.

<br>

Technical choices and defaults belong to the Preferences file of the subject that owns them. Shared choices that genuinely span Development and Process belong to Implementation Preferences. The shape of any generated operational record belongs to its Schema.

Every Principle in this file is mandatory. An Implementation Preference or Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.





<br><br>
<!--------------------------------------------------------------------------------- Principles --->

## Principles

Every Principle below is mandatory.

<br>

### Implementation documentation maps subjects without replacing Definitions

**Rule:** Implementation documentation identifies Development and Process, links each part's Definition and Preferences, and makes clear which responsibilities belong to each part. Subject documentation remains in that subject's Definition and Preferences. Documentation never replaces either.

**Why:** A clear map helps readers reach the authoritative subject files without creating a second explanation that can diverge from them.

**Boundary:** This Principle governs the content and role of the map; it does not require every subject to own a separate documentation section.

<br>

### Implementation has Development and Process parts

**Rule:** Implementation consists of Development, which governs the product being built, and Process, which governs the work that configures, plans, reviews, and records that build. Neither part replaces the other.

**Why:** Product architecture and work control require different ownership while still needing one reusable Implementation perspective.

**Boundary:** Development does not own Process records, and Process does not own product Behaviour, Source, or public interfaces.

<br>

### Each subject is defined by one Definition and one Preferences file

**Rule:** Every Implementation subject has one `definition.md` and one `preferences.yaml`. The Definition carries its Understanding and mandatory Principles; Preferences carry its choices, defaults, and realization conventions.

**Why:** A stable pair separates what the subject is and must preserve from how it is preferably realized.

**Boundary:** A subject's Preferences never override its Definition, and a child subject does not duplicate the authority of its parent or sibling.

<br>

### Development and Process retain separate ownership

**Rule:** Development Components own product responsibilities, and Process Components own Configuration, Plan, Review, and State responsibilities. A Skill performs an operation under these owners but does not acquire ownership by writing an authorized record.

**Why:** Explicit ownership keeps product meaning, operational progress, evidence, and workflow records from becoming interchangeable.

**Boundary:** A Process Component may inspect Development results when its responsibility requires it, but it never changes a Development-owned result directly.





<br><br>
<!--------------------------------------------------------------------------------- At a Glance --->

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Implementation documentation maps subjects without replacing Definitions**

- **Must** — use documentation to identify the parts and link their authoritative Definition and Preferences files; keep subject documentation in that subject's files.
- **Never** — let documentation replace or override a subject's Definition or Preferences.

**Implementation has Development and Process parts**

- **Must** — keep product construction in Development and implementation control in Process.
- **Never** — let either part replace the responsibility of the other.

**Each subject is defined by one Definition and one Preferences file**

- **Must** — keep each subject's Understanding and mandatory Principles in Definition and its choices in Preferences.
- **Never** — let Preferences override Definition or duplicate another subject's authority.

**Development and Process retain separate ownership**

- **Must** — keep product responsibilities in Development and Configuration, Plan, Review, and State responsibilities in Process.
- **Never** — let a Skill acquire ownership merely by performing an operation or writing an authorized record.
