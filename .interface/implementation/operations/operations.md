# Operations Definition

Operations is the Implementation Subsystem that governs how authorized work is prepared, carried out, checked, activated, reset, and recorded.

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

Operations is the Implementation Subsystem that defines how work on a Target is configured, planned, developed, reviewed, implemented, launched, reset, and recorded. It contains the Configure, Plan, Develop, Review, Implement, Launch, Reset, and State Components while remaining separate from the Development Subsystem that defines the product being built.

### Purpose

Building a product requires more than product architecture. The work also needs a stable way to prepare operational records, divide a phase into verifiable activities, judge the generated result, and preserve progress across runs. Operations gives each of those concerns one owner and one reusable philosophy.

### How It Works

Configuration prepares and reconciles the operational records. Plan turns a selected Target phase into bounded work, and Develop executes that work. Review compares the result with its applicable authorities, records Findings, resolves the Findings within its authority, and rechecks the result. Implement coordinates Configure, Plan, Develop, and Review; Launch activates a completed implementation, Reset reconciles its authorized scope, and State preserves the aggregate position and execution outcomes.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Operation Component** — one Component that owns a distinct part of configuring, planning, developing, reviewing, implementing, launching, resetting, or recording implementation work.
- **Operational Record** — mutable information produced while the Interface workflow runs, separate from the authorities that define what the work means.

<br>

<!--------------------------------------------------------------------------------- Components --->
## Components

```text
Components
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

Configure creates Schema-derived Config records.

→ [Definition of Configure](configure/configure.md)<br>
→ [Preferences of Configure](configure/configure.yaml)


### Plan

Plan turns Target phases into verifiable work.

→ [Definition of Plan](plan/plan.md)<br>
→ [Preferences of Plan](plan/plan.yaml)


### Develop

Develop executes authorized planned Tasks.

→ [Definition of Develop](develop/develop.md)<br>
→ [Preferences of Develop](develop/develop.yaml)

### Review

Review checks selected-phase work against its applicable authorities.

→ [Definition of Review](review/review.md)<br>
→ [Preferences of Review](review/review.yaml)


### Implement

Implement coordinates the Operations workflow.

→ [Definition of Implement](implement/implement.md)<br>
→ [Preferences of Implement](implement/implement.yaml)


### Launch

Launch activates the completed implementation.

→ [Definition of Launch](launch/launch.md)<br>
→ [Preferences of Launch](launch/launch.yaml)


### Reset

Reset reconciles authorized records and outputs within its scope.

→ [Definition of Reset](reset/reset.md)<br>
→ [Preferences of Reset](reset/reset.yaml)


### State

State records aggregate operational position and the execution log.

→ [Definition of State](state/state.md)<br>
→ [Preferences of State](state/state.yaml)

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target** — uses current phase identity and intent without becoming another Target definition.
- **Consumes Development** — applies the product architecture and Component authorities relevant to the work being performed.
- **Consumed by Agent** — provides the operational concepts and records used by the corresponding Core Skills.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Operations owns workflow concerns. Technical choices and defaults shared by Operations belong to Operations Preferences; choices owned by an Operation belong to that Component's Preferences, and operational record shapes belong to their Schemas. Product meaning belongs to Development, project intent belongs to Target, and runtime realization belongs to Platform.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles in this Definition are mandatory. This Definition explains Operations and its ownership; Operations Preferences supply only defaults and preferences. Target, Development, and the applicable Schemas outrank Operations Preferences where they speak to their own concerns.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Operations governs implementation work without becoming product implementation

**Rule:** Operations defines how Target implementation work is configured, developed, coordinated, reviewed, launched, reset, and recorded. It never owns or implements the product behaviour, source, or public interfaces governed by Development.

**Why:** Separating the way work is controlled from the product being built prevents operational records and workflow mechanics from becoming product architecture.

**Boundary:** Operations may inspect Development results where its Components require them, but inspection never transfers ownership of those results. Review may change a reviewed Development result or its evidence only to resolve one of its recorded Findings; no other Operation Component acquires that authority.

<br>

### Each operational concern has one owning Component

**Rule:** Configure owns Config preparation and reconciliation, Plan owns planned activities, Develop owns planned implementation work, Review owns Findings, review data, and its resolutions, Implement owns workflow coordination, Launch owns runtime activation, Reset owns bounded reconciliation, and State owns aggregate operational position and the execution log. Shared Config files may contain operational records produced by more than one Component.

**Why:** One owner for each operational concern keeps progress, evidence, and authority consistent across separate runs.

**Boundary:** A Skill may perform work for an Operation Component, but the Skill does not become the owner of the record it writes.

<br>

### Operational records remain separate from their authorities

**Rule:** An Operational Record records what happened, what exists, or where work stands. It never redefines Target intent, Development meaning, a Principle, a Preference, or a Schema.

**Why:** A mutable execution record cannot safely serve as the source of the requirements it is meant to track.

**Boundary:** Referencing an authority or recording the result of applying it does not copy ownership of that authority into Operations.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Operations governs implementation work without becoming product implementation**

- **Must** — Operations governs configuration, planning, development, review, implementation, launch, reset, coordination, and operational recording.
- **Never** — Operations owns or implements Development product behaviour, source, or public interfaces.

**Each operational concern has one owning Component**

- **Must** — Configure, Plan, Develop, Review, Implement, Launch, Reset, and State each retain their declared ownership.
- **Never** — an Operation Component writes another's owned content without explicit Interface authority under that owner's rules.

**Operational records remain separate from their authorities**

- **Must** — Operational Records state execution facts and progress.
- **Never** — an Operational Record redefines Target, Development, Principles, Preferences, or Schemas.
