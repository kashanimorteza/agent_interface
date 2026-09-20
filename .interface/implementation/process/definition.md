# Process Definition

Process is the Implementation Subsystem that governs how authorized work is prepared, carried out, checked, activated, reset, and recorded.

<br><br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
   - **[Configure](#configure)**
   - **[Plan](#plan)**
   - **[Develop](#develop)**
   - **[Review](#review)**
   - **[Implement](#implement)**
   - **[Launch](#launch)**
   - **[Reset](#reset)**
   - **[State](#state)**
4. **[Relationships](#relationships)**
5. **[Layering](#layering)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
   - **[Process governs implementation work without becoming product implementation](#process-governs-implementation-work-without-becoming-product-implementation)**
   - **[Each operational concern has one owning Component](#each-operational-concern-has-one-owning-component)**
   - **[Operational records remain separate from their authorities](#operational-records-remain-separate-from-their-authorities)**
8. **[At a Glance](#at-a-glance)**

<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Process is the Implementation Subsystem that defines how work on a Target is configured, planned, developed, reviewed, implemented, launched, reset, and recorded. It contains the Configure, Plan, Develop, Review, Implement, Launch, Reset, and State Components while remaining separate from the Development Subsystem that defines the product being built.

### Purpose

Building a product requires more than product architecture. The work also needs a stable way to prepare operational records, divide a phase into verifiable activities, judge the generated result, and preserve progress across runs. Process gives each of those concerns one owner and one reusable philosophy.

### How It Works

Configuration prepares and reconciles the operational records. Plan turns a selected Target phase into bounded work. Review compares the result of that phase with its applicable authorities and records Findings. State preserves the aggregate operational position and outcomes needed to continue the workflow.

<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Process Component** — one Component that owns a distinct part of configuring, planning, reviewing, or recording implementation work.
- **Operational Record** — mutable information produced while the Interface workflow runs, separate from the authorities that define what the work means.

<br><br>

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

```yaml
name: Configure
definition: .interface/implementation/process/configure/definition.md
preferences: .interface/implementation/process/configure/preferences.yaml
responsibility: The preparation and structural reconciliation of operational Config and the Application Manifest.
```

→ [Definition](configure/definition.md)<br>
→ [Preferences](configure/preferences.yaml)

<br>

### Plan

Plan turns Target phases into bounded, understandable, and verifiable activities.

```yaml
name: Plan
definition: .interface/implementation/process/plan/definition.md
preferences: .interface/implementation/process/plan/preferences.yaml
responsibility: The decomposition of each Target phase into Plans, Groups, and Tasks.
```

→ [Definition](plan/definition.md)<br>
→ [Preferences](plan/preferences.yaml)

<br>

### Develop

Develop performs the planned implementation work and produces the authorized Development results.

```yaml
name: Develop
definition: .interface/implementation/process/develop/definition.md
preferences: .interface/implementation/process/develop/preferences.yaml
responsibility: The execution of planned implementation Tasks and production of authorized Development results.
```

→ [Definition](develop/definition.md)<br>
→ [Preferences](develop/preferences.yaml)

<br>

### Review

Review establishes whether selected-phase work satisfies its applicable authorities and owns the recorded Findings.

```yaml
name: Review
definition: .interface/implementation/process/review/definition.md
preferences: .interface/implementation/process/review/preferences.yaml
responsibility: The assurance of phase Plans and implemented results against their applicable authorities.
```

→ [Definition](review/definition.md)<br>
→ [Preferences](review/preferences.yaml)

<br>

### Implement

Implement coordinates the Process workflow across Plan, Develop, and Review under the current authorities.

```yaml
name: Implement
definition: .interface/implementation/process/implement/definition.md
preferences: .interface/implementation/process/implement/preferences.yaml
responsibility: The coordination of the Process workflow across planning, development, and review.
```

→ [Definition](implement/definition.md)<br>
→ [Preferences](implement/preferences.yaml)

<br>

### Launch

Launch brings the completed implementation online and records the observable runtime result.

```yaml
name: Launch
definition: .interface/implementation/process/launch/definition.md
preferences: .interface/implementation/process/launch/preferences.yaml
responsibility: The controlled activation of the completed implementation and recording of its runtime result.
```

→ [Definition](launch/definition.md)<br>
→ [Preferences](launch/preferences.yaml)

<br>

### Reset

Reset reconciles operational records and outputs with the selected reset scope while preserving what must remain.

```yaml
name: Reset
definition: .interface/implementation/process/reset/definition.md
preferences: .interface/implementation/process/reset/preferences.yaml
responsibility: The bounded reconciliation of operational records and outputs after an authorized reset.
```

→ [Definition](reset/definition.md)<br>
→ [Preferences](reset/preferences.yaml)

<br>

### State

State records aggregate operational position, progress, outcomes, History, Blockers, and Open Questions.

```yaml
name: State
definition: .interface/implementation/process/state/definition.md
preferences: .interface/implementation/process/state/preferences.yaml
responsibility: The operational position and aggregate progress needed to continue Implementation work.
```

→ [Definition](state/definition.md)<br>
→ [Preferences](state/preferences.yaml)

<br><br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target** — uses current phase identity and intent without becoming another Target definition.
- **Consumes Development** — applies the product architecture and Component authorities relevant to the work being performed.
- **Consumed by Workflow** — provides the operational concepts and records through which implementation work proceeds and resumes.

<br>

Technical choices and defaults shared by Process belong to Process Preferences. Choices owned by Configuration, Plan, Review, or State remain in that Component's Preferences. Operational record shapes belong to their Schemas.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br><br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Process owns workflow concerns. Technical choices belong to the Preferences of the Process Component that owns them; product meaning belongs to Development; project intent belongs to Target; and runtime realization belongs to the selected Agent Native.

<br><br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles in this Definition are mandatory. This Definition explains Process and its ownership; Process Preferences supply only defaults and preferences. Target, Development, and the applicable Schemas outrank Process Preferences where they speak to their own concerns.

<br><br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Process governs implementation work without becoming product implementation

**Rule:** Process defines how Target implementation work is configured, planned, reviewed, and recorded. It never owns or implements the product behaviour, source, or public interfaces governed by Development.

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

<br><br>

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
