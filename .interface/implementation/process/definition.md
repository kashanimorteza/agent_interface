# Process Definition

Process is the Implementation Subsystem that governs how authorized work is prepared, carried out, checked, activated, reset, and recorded.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Layering](#layering)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Process is the Implementation Subsystem that defines how work on a Target is configured, planned, developed, reviewed, implemented, launched, reset, and recorded. It contains the Configure, Plan, Develop, Review, Implement, Launch, Reset, and State Components while remaining separate from the Development Subsystem that defines the product being built.

### Purpose

Building a product requires more than product architecture. The work also needs a stable way to prepare operational records, divide a phase into verifiable activities, judge the generated result, and preserve progress across runs. Process gives each of those concerns one owner and one reusable philosophy.

### How It Works

Configuration prepares and reconciles the operational records. Plan turns a selected Target phase into bounded work. Review compares the result of that phase with its applicable authorities and records Findings. State preserves the aggregate operational position and outcomes needed to continue the workflow.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Process Component** — one Component that owns a distinct part of configuring, planning, reviewing, or recording implementation work.
- **Operational Record** — mutable information produced while the Interface workflow runs, separate from the authorities that define what the work means.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Process
└── Components
    ├── Configure
    ├── Plan
    ├── Develop
    ├── Review
    ├── Implement
    ├── Launch
    ├── Reset
    └── State
```

### Configure

Configure prepares and structurally reconciles the operational Config records and maintains the Application Manifest.

Responsibility: The preparation and structural reconciliation of operational Config and the Application Manifest.

→ [Definition of Configure](configure/definition.md)<br>
→ [Preferences of Configure](configure/preferences.yaml)


### Plan

Plan turns Target phases into bounded, understandable, and verifiable activities.

Responsibility: The decomposition of each Target phase into Plans, Groups, and Tasks.

→ [Definition of Plan](plan/definition.md)<br>
→ [Preferences of Plan](plan/preferences.yaml)


### Develop

Develop performs the planned implementation work and produces the authorized Development results.

Responsibility: The execution of planned implementation Tasks and production of authorized Development results.

→ [Definition of Develop](develop/definition.md)<br>
→ [Preferences of Develop](develop/preferences.yaml)

### Review

Review establishes whether selected-phase work satisfies its applicable authorities and owns the recorded Findings.

Responsibility: The assurance of phase Plans and implemented results against their applicable authorities.

→ [Definition of Review](review/definition.md)<br>
→ [Preferences of Review](review/preferences.yaml)


### Implement

Implement coordinates the Process workflow across Plan, Develop, and Review under the current authorities.

Responsibility: The coordination of the Process workflow across planning, development, and review.

→ [Definition of Implement](implement/definition.md)<br>
→ [Preferences of Implement](implement/preferences.yaml)


### Launch

Launch brings the completed implementation online and records the observable runtime result.

Responsibility: The controlled activation of the completed implementation and recording of its runtime result.

→ [Definition of Launch](launch/definition.md)<br>
→ [Preferences of Launch](launch/preferences.yaml)


### Reset

Reset reconciles operational records and outputs with the selected reset scope while preserving what must remain.

Responsibility: The bounded reconciliation of operational records and outputs after an authorized reset.

→ [Definition of Reset](reset/definition.md)<br>
→ [Preferences of Reset](reset/preferences.yaml)


### State

State records aggregate operational position, progress, outcomes, History, Blockers, and Open Questions.

Responsibility: The operational position and aggregate progress needed to continue Implementation work.

→ [Definition of State](state/definition.md)<br>
→ [Preferences of State](state/preferences.yaml)

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target** — uses current phase identity and intent without becoming another Target definition.
- **Consumes Development** — applies the product architecture and Component authorities relevant to the work being performed.
- **Consumed by Workflow** — provides the operational concepts and records through which implementation work proceeds and resumes.

<br>

Technical choices and defaults shared by Process belong to Process Preferences. Choices owned by Configuration, Plan, Review, or State remain in that Component's Preferences. Operational record shapes belong to their Schemas.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Process owns workflow concerns. Technical choices belong to the Preferences of the Process Component that owns them; product meaning belongs to Development; project intent belongs to Target; and runtime realization belongs to the selected Agent Native.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles in this Definition are mandatory. This Definition explains Process and its ownership; Process Preferences supply only defaults and preferences. Target, Development, and the applicable Schemas outrank Process Preferences where they speak to their own concerns.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Process governs implementation work without becoming product implementation

**Rule:** Process defines how Target implementation work is configured, developed, coordinated, reviewed, launched, reset, and recorded. It never owns or implements the product behaviour, source, or public interfaces governed by Development.

**Why:** Separating the way work is controlled from the product being built prevents operational records and workflow mechanics from becoming product architecture.

**Boundary:** Process may inspect Development results where its Components require them, but inspection never transfers ownership of those results.

<br>

### Each operational concern has one owning Component

**Rule:** Configure owns Config preparation and reconciliation, Plan owns planned activities, Develop owns planned implementation work, Review owns assurance and Findings, Implement owns workflow coordination, Launch owns runtime activation, Reset owns bounded reconciliation, and State owns aggregate operational position and history. No Process Component writes another's owned content unless the Interface explicitly grants that write under the owning Component's rules.

**Why:** One owner for each operational concern keeps progress, evidence, and authority consistent across separate runs.

**Boundary:** A Skill may perform work for a Process Component, but the Skill does not become the owner of the record it writes.

<br>

### Operational records remain separate from their authorities

**Rule:** An Operational Record records what happened, what exists, or where work stands. It never redefines Target intent, Development meaning, a Principle, a Preference, or a Schema.

**Why:** A mutable execution record cannot safely serve as the source of the requirements it is meant to track.

**Boundary:** Referencing an authority or recording the result of applying it does not copy ownership of that authority into Process.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Process governs implementation work without becoming product implementation**

- **Must** — Process governs configuration, planning, review, and operational recording.
- **Never** — Process owns or implements Development product behaviour, source, or public interfaces.

**Each operational concern has one owning Component**

- **Must** — Configure, Plan, Develop, Review, Implement, Launch, Reset, and State each retain their declared ownership.
- **Never** — a Process Component writes another's owned content without explicit Interface authority under that owner's rules.

**Operational records remain separate from their authorities**

- **Must** — Operational Records state execution facts and progress.
- **Never** — an Operational Record redefines Target, Development, Principles, Preferences, or Schemas.
