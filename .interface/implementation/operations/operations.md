# Operations Definition

Operations is the Implementation Subsystem that governs how authorized work is prepared, carried out, checked, activated, reset, and recorded.

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

Operations is the Implementation Subsystem that defines how work on a Target is configured, planned, developed, reviewed, implemented, launched, reset, and recorded. It contains the Configure, Plan, Develop, Review, Implement, Launch, Reset, and State Components while remaining separate from the Development Subsystem that defines the product being built.

### Purpose

Building a product requires more than product architecture. The work also needs a stable way to prepare operational records, divide a phase into verifiable activities, judge the generated result, and preserve progress across runs. Operations gives each of those concerns one owner and one reusable philosophy.

### How It Works

Configuration prepares and reconciles the operational records. Plan turns a selected Target phase into bounded work. Review compares the result of that phase with its applicable authorities and records Findings. State preserves the aggregate operational position and outcomes needed to continue the workflow.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Operation Component** — one Component that owns a distinct part of configuring, planning, reviewing, or recording implementation work.
- **Operational Record** — mutable information produced while the Interface workflow runs, separate from the authorities that define what the work means.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Operations
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

**Agent Skill:** `/my-interface-configure`

Configure initializes and reconciles the four operational Config files and synchronizes phase State. It installs nothing and prepares no Environment: Develop installs the technical requirements of the phase it implements, and Launch prepares the Environment of the selected Launch Item.

A Skill named by an `agent_skills` association reaches the Runtime through its ecosystem's own provisioning mechanism when the environment is prepared, and through Develop when Develop installs the packages that bundle it. Plan, Develop, and every other Operation use such a Skill when it is discoverable and usable, and never install it. The separation exists because a package-provided Skill cannot exist before its package does, and because provisioning one never makes it an Agent Module declaration.

Responsibility: The preparation and structural reconciliation of operational Config and the Application Manifest.

→ [Definition of Configure](configure/configure.md)<br>
→ [Preferences of Configure](configure/configure.yaml)


### Plan

Plan turns Target phases into bounded, understandable, and verifiable activities.

**Agent Skill:** `/my-interface-plan`

Plan converts the current Target and applicable Implementation guidance into bounded, understandable, and verifiable Tasks.

Responsibility: The decomposition of each Target phase into Plans, Groups, and Tasks.

→ [Definition of Plan](plan/plan.md)<br>
→ [Preferences of Plan](plan/plan.yaml)


### Develop

Develop performs the planned implementation work and produces the authorized Development results.

**Agent Skill:** `/my-interface-develop`

Develop implements and verifies eligible Tasks from a valid current Plan. Review evaluates the resulting implementation afterward.

Responsibility: The execution of planned implementation Tasks and production of authorized Development results.

→ [Definition of Develop](develop/develop.md)<br>
→ [Preferences of Develop](develop/develop.yaml)

### Review

Review establishes whether selected-phase work satisfies its applicable authorities and owns the recorded Findings.

**Agent Skill:** `/my-interface-review`

Review assures each selected phase's Plan and existing implementation against current Interface and Target Understanding, recording every misalignment as a Finding owned by Configure, Plan, or Develop, without invoking them or repairing anything. Implement or the Human reruns those Operations and Review until it is satisfied. With no phase input, it reviews every enabled phase.

Responsibility: The assurance of phase Plans and implemented results against their applicable authorities.

→ [Definition of Review](review/review.md)<br>
→ [Preferences of Review](review/review.yaml)


### Implement

Implement coordinates the Operations workflow across Plan, Develop, and Review under the current authorities.

**Agent Skill:** `/my-interface-implement`

Implement executes Configure once when no phase was selected, then processes each selected phase in Target order. It reviews an existing implementation before rework, plans a phase with no implementation, repeats the Plan, Develop, and Review cycle while Findings remain, advances only after the phase is satisfied, and finally performs eligible Launch. With no phase input, it processes every enabled and ready phase.

Responsibility: The coordination of the Operations workflow across planning, development, and review.

→ [Definition of Implement](implement/implement.md)<br>
→ [Preferences of Implement](implement/implement.yaml)


### Launch

Launch brings the completed implementation online and records the observable runtime result.

**Agent Skill:** `/my-interface-launch`

Launch reads the selected Launch definition and its Component Runtime Requirements, starts only the requested scope (or all developed parts for `complete`/`all`), verifies readiness, and reports access points. When no scope is supplied, the Launch Skill asks the Human to choose one.

Responsibility: The controlled activation of the completed implementation and recording of its runtime result.

→ [Definition of Launch](launch/launch.md)<br>
→ [Preferences of Launch](launch/launch.yaml)


### Reset

Reset reconciles operational records and outputs with the selected reset scope while preserving what must remain.

**Agent Skill:** `/my-interface-reset`

Reset resets selected phases; with no phase input it resets every phase with generated work. `config` removes only operational Config files, while `complete` removes those Config files and the implementation outputs of all phases. Emptying or reinitializing a Config file is not removal. Every mode previews its exact impact and requires separate Human confirmation before mutation.

Responsibility: The bounded reconciliation of operational records and outputs after an authorized reset.

→ [Definition of Reset](reset/reset.md)<br>
→ [Preferences of Reset](reset/reset.yaml)


### State

State records aggregate operational position, progress, outcomes, History, Blockers, and Open Questions.

Responsibility: The operational position and aggregate progress needed to continue Implementation work.

→ [Definition of State](state/state.md)<br>
→ [Preferences of State](state/state.yaml)

#### Modes

State records the active Mode. Modes describe the current operational position and remain distinct from the behaviour required from the Target.

##### Not Set

State: `not set`.

Responsibility: Represents the initial Workflow position before a Skill action is recorded, or the position restored by Reset.

Inputs: None.

Output: Active State with no selected work scope.

##### Configuring

State: `configuring`.

Responsibility: Create and reconcile the persistent Application Manifest, reconcile operational Config, and synchronize phase State.

Inputs: Operational Schemas, existing Config, and Target phase identities.

Output: Persistent Application Manifest and current operational Config.

##### Planning

State: `planning`.

Responsibility: Create bounded and verifiable Tasks without prescribing implementation.

Inputs: Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, and operational records.

Output: Updated Plan Config.

##### Development

State: `development`.

Responsibility: Implement and verify eligible planned Tasks.

Inputs: Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, Plan, State, and existing implementation.

Output: Verified implementation and updated operational records.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target** — uses current phase identity and intent without becoming another Target definition.
- **Consumes Development** — applies the product architecture and Component authorities relevant to the work being performed.
- **Consumed by Workflow** — provides the operational concepts and records through which implementation work proceeds and resumes.

<br>

Technical choices and defaults shared by Operations belong to Operations Preferences. Choices owned by Configure, Plan, Review, or State remain in that Component's Preferences. Operational record shapes belong to their Schemas.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Operations owns workflow concerns. Technical choices belong to the Preferences of the Operation Component that owns them; product meaning belongs to Development; project intent belongs to Target; and runtime realization belongs to the selected Agent Native.

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

**Boundary:** Operations may inspect Development results where its Components require them, but inspection never transfers ownership of those results.

<br>

### Each operational concern has one owning Component

**Rule:** Configure owns Config preparation and reconciliation, Plan owns planned activities, Develop owns planned implementation work, Review owns assurance and Findings, Implement owns workflow coordination, Launch owns runtime activation, Reset owns bounded reconciliation, and State owns aggregate operational position and history. No Operation Component writes another's owned content unless the Interface explicitly grants that write under the owning Component's rules.

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
