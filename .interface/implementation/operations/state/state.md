# State Definition

State is the Operation Component that records the aggregate operational position, outcomes, stoppages, and history needed to continue the workflow.

Responsibility: The operational position and aggregate progress needed to continue Implementation work.

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

State records the operational condition of the Interface Workflow: the active mode, aggregate progress for each Target phase, and the append-only History of every Skill execution.

State never contains Target meaning, implementation instructions, application configuration, product code, or the status and history of individual Tasks.

### Purpose

Work that spans phases, operations, and sessions needs somewhere to say where it currently stands. Without it, every operation starts by guessing: has this phase been planned, was it reviewed, did the last launch succeed, is there something blocking that nobody has acted on. Guessing from artifacts is unreliable — files exist for many reasons — and asking the Human every time is worse.

State exists to answer that question and only that question. It records the active Workflow position, aggregate progress for each phase, and the History of what happened. Any Skill can read it and know where the Workflow stands and what preceding Skills reported.

It is deliberately thin. State holds no Target meaning, no implementation instruction, no Task-level detail — those have their own owners, and duplicating them here would create a second version of the truth that drifts from the first. Its operation log holds only execution metadata and concise reports: enough to resume with current context, never enough to replace the sources.

### How It Works

An operation begins by reading State: which mode is active, which phase it concerns, and what the aggregate progress of that phase is — planned, developed, reviewed. That is enough to decide what may run next without inspecting artifacts or asking.

Each operation then updates only the field it owns. Planning moves a phase's planning progress, Developing its development progress, Review its review progress; none of them writes another's field, and none of them writes Task-level detail, which belongs to Plan. Phase records reconcile as the Target changes — a new phase appears at its initial values, an existing one keeps the progress it has.

Every Skill invocation records one History item in State. Shared execution metadata goes in the common fields; the Skill's own report and records go under `data`. State is the source of execution history, while Plan remains the source of planned work.

Everything that happened is appended to History rather than overwritten. Each item may record its parent Skill, phase, start and completion times, measurable duration, available token usage, Skills it used, open questions, blockers, outcome, and a concise report. The next Skill reads the latest relevant History items before acting. Skill-specific information is stored in that item's `data` mapping or list.

### Modes

State records the active Mode. Modes describe the current operational position and remain distinct from the behaviour required from the Target.

#### Not Set

State: `not set`.

Responsibility: Represents the initial Workflow position before a Skill action is recorded, or the position restored by Reset.

Inputs: None.

Output: Active State with no selected work scope.

#### Configuring

State: `configuring`.

Responsibility: Create and reconcile the persistent Application Manifest, reconcile operational Config, and synchronize phase State.

Inputs: Operational Schemas, existing Config, and Target phase identities.

Output: Persistent Application Manifest and current operational Config.

#### Planning

State: `planning`.

Responsibility: Create bounded and verifiable Tasks without prescribing implementation.

Inputs: Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, and operational records.

Output: Updated Plan Config.

#### Development

State: `development`.

Responsibility: Implement and verify eligible planned Tasks.

Inputs: Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, Plan, State, and existing implementation.

Output: Verified implementation and updated operational records.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Active State** — the current or most recently entered Workflow mode, its phase when applicable, and update provenance.
- **Phase State** — aggregate Planning, Development, and Review progress for one stable Target phase identifier.
- **History Item** — one append-only record of a Skill execution, its common execution metadata, outcome, and report.
- **Blocker** — a condition that genuinely prevents safe or valid continuation.
- **Open Question** — a critical decision that cannot safely be made without a human.

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target phase identity** — uses stable phase identifiers without copying phase goals or Target meaning.
- **Consumes operation outcomes** — each operation records only the aggregate State and history its role owns.
- **Consumed by operations and reporting** — enables work to resume without reconstructing operational progress.

Technical choices and defaults belong to State Preferences, which currently define none. The exact shape and initial values of State Config belong to the State Schema.

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

<!--------------------------------------------------------------------------------- Layering --->
<!--------------------------------------------------------------------------------- Layering --->
## Layering

State owns aggregate operational records. Individual operations own their detailed records and evidence, while Target and Development remain the authorities for project and product meaning.

<br>

<!--------------------------------------------------------------------------------- Authority --->
<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles in this Definition govern State. State Preferences are empty; the State Schema owns record shape, and operations may update only the fields granted to them.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### State records the active Workflow position

**Rule:** State records the current or most recently entered Workflow mode and the phase being acted on when the operation is phase-specific.

**Why:** Anyone joining the work can immediately see its current operational position.

**Boundary:** Active State is descriptive, not an authorization gate, and never prevents an operation merely because it ran before.

<br>

### The Workflow has four modes

**Rule:** State recognizes `not set`, `configuring`, `planning`, and `development`. The initial mode is `not set`; the active phase is null when work is not phase-specific.

**Why:** A stable vocabulary aligns every operation without imposing a one-way lifecycle.

**Boundary:** Review, Launch, Implement, and Reset update their own State records and History without inventing additional active modes.

<br>

### Every Target phase has aggregate operational State

**Rule:** State keeps one Phase State for every stable Target phase identifier. Planning and Development use `not started`, `in progress`, or `completed`. Review uses `not started`, `in progress`, `plan satisfied`, `satisfied`, `not satisfied`, or `inconclusive`. `plan satisfied` means Plan Assurance passed while no implementation was available for Implementation Assurance; only `satisfied` certifies both an assured Plan and its implemented result.

**Why:** Target stays human-owned while operations can record where every phase stands.

**Boundary:** Phase State never copies a phase title, goal, target, readiness, or enabled status. It never duplicates individual Task status, evidence, or history.

<br>

### Phase records reconcile without erasing progress

**Rule:** Configure creates missing Phase State records from stable Target phase identifiers and preserves existing records. New records begin with every operation at `not started`. A removed Target phase is not silently deleted when its State carries meaningful progress or provenance; the conflict is reported. A record that still contains only initialization defaults may be removed during synchronization.

**Why:** Target phases can evolve without making recorded work disappear.

**Boundary:** Synchronization establishes identity only; it does not interpret phase meaning or decide implementability.

<br>

### Operations update only their aggregate phase field

**Rule:** Planning updates Planning progress, Development updates Development progress, and Review updates Review progress for the active phase. Each records provenance and appends a History Event.

**Why:** Narrow ownership prevents one operation from overstating another's work.

**Boundary:** One operation's completion never implies another operation's completion.

<br>

### Implement results belong to History

**Rule:** Implement records its coordination outcome, selection, child Skill results, and completion condition in one History item's `data`. The active mode and per-phase aggregate fields remain the current State summary.

**Why:** End-to-end orchestration needs one truthful historical result in addition to per-phase progress.

**Boundary:** Disabled, unready, and future phases are never marked complete. A later Target change can make additional phases implementable.

<br>

### Launch results belong to History

**Rule:** Launch records `not launched`, `launching`, `launched`, `failed`, or `stopped`, together with the Environment, Launch method, provenance, and verified access points in its History item's `data`.

**Why:** A successful launch is useful only when people and systems know how to reach it.

**Boundary:** State stores no credentials, shared secrets, or private configuration values.

<br>

### History is append-only operational evidence

**Rule:** Every Skill execution appends one History Item. Common fields are optional and include identity, sequence, Skill, parent, phase, event, outcome, timing, token usage, open questions, blockers, report, and recorder. Skill-specific values belong only under that item’s `data`, which may be a nested mapping or list.

**Why:** Active records show the present while History explains how the Workflow reached it.

**Boundary:** History never copies Task histories, command transcripts, secrets, or Target content. It may preserve concise Review findings and evidence under the Review item's `data`; detailed Task history remains owned by Plan.

<br>

### Workflow operations remain repeatable

**Rule:** Configure, Planning, Development, Review, Launch, Implement, and Reset may run again. Each reconciles records it owns, preserves information outside its authority, and records the new outcome truthfully.

**Why:** Real projects revisit earlier work.

**Boundary:** An operation may stop for invalid input, an unmet prerequisite, or a genuine Blocker, but never solely because it ran before.

<br>

### Reset reconciles State with what it removes

**Rule:** A confirmed phase Reset returns only selected phase fields to values consistent with outputs that remain, preserves unselected phase State, and appends one Reset History Item per selected phase. A confirmed Config or Complete Reset removes State with the other operational Config records.

**Why:** State must not claim removed plans, implementation, review evidence, or runtime still exists.

**Boundary:** Config and Complete Reset remove State Config itself and cannot append to that removed record. Config Reset preserves developed outputs; Complete Reset does not.

<br>

### History records critical Blockers

**Rule:** A History Item records a Blocker when it identifies what cannot continue, what is missing, why continuation is impossible, who can resolve it, and who raised it. The Blocker remains referenced until verified resolution and authorized reconciliation of current references.

**Why:** A Blocker must identify a real, current stoppage.

**Boundary:** Ordinary ambiguity or a choice professional judgment can safely resolve is not a Blocker.

<br>

### History records Open Questions for the Human

**Rule:** A History Item records an Open Question with the decision, why it matters, any Blocker it releases, and provenance. A human answer records its value, author, and time under the relevant History item's `data`.

**Why:** Some choices materially change intent and cannot safely be guessed.

**Boundary:** An operation never invents a human answer or raises non-critical uncertainty as an Open Question.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**State records the active Workflow position**

- **Must** — record the active Workflow position without making it an authorization gate

**Every Target phase has aggregate operational State**

- **Must** — keep aggregate Planning, Development, and Review progress by stable phase identifier
- **Must** — distinguish `plan satisfied` from full Review `satisfied` when implementation is not yet available
- **Never** — copy Target meaning or individual Task status, evidence, or history into State

**Phase records reconcile without erasing progress**

- **Must** — preserve existing progress while reconciling phase identity

**Implement results belong to History**

- **Must** — record truthful Implement results and exclude disabled or unready phases from completion

**Launch results belong to History**

- **Must** — record Launch status and verified access points without secrets

**History is append-only operational evidence**

- **Must** — append concise operational History for every State-changing operation

**Workflow operations remain repeatable**

- **Must** — keep operations repeatable and make confirmed Reset outcomes agree with State

**History records critical Blockers**

- **Must** — reserve Blockers and Open Questions for genuine critical conditions
