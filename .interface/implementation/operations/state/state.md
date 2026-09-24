# State Definition

State is the Operation Component that records the aggregate operational position of the project.

Responsibility: The current Mode, aggregate Phase progress, and status records needed to show the project's operational position.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Modes](#modes)**
3. **[Terms](#terms)**
4. **[Relationships](#relationships)**
5. **[Layering](#layering)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

State records the operational condition of the project: the active Mode, aggregate progress for each Target Phase, and the Log of its execution history.

State never contains Target meaning, implementation instructions, application configuration, product code, or the status and history of individual Tasks.

### Purpose

Work that spans Phases and sessions needs a reliable record of where the project currently stands: which Mode is active, how far each Phase has progressed, and which recorded outcomes still matter.

State exists to answer that question and only that question. It records the active operational position, aggregate progress for each Phase, and the history of recorded outcomes.

It is deliberately thin. State holds no Target meaning, implementation instruction, or Task-level detail. Its Log holds the common metadata and concise reports needed to preserve the project's recorded position; it never replaces the sources.

### How It Works

State keeps the active Mode, the relevant Phase when applicable, and aggregate Phase progress for planning, development, and review.

A planning occurrence changes a Phase's planning progress; a development occurrence changes its development progress; and a review occurrence changes its review progress. Task status and history remain in the Plan Config and its Task Logs. Phase records reconcile against stable Target Phase identifiers: a new Phase begins with initial values, and an existing Phase preserves recorded progress.

Every executed Skill has one Log Entry in State. Shared execution metadata belongs in common fields; information specific to that execution belongs under `data`. State is the source of execution history, while Plan remains the source of planned work.

The Log preserves every recorded Entry: in progress, completed, stopped, and blocked. Each Entry may record its parent, Phase, start and completion times, measurable duration, available token usage, Skills used, Open Questions, Blockers, outcome, and a concise report. Execution-specific information is stored in that Entry's `data` mapping or list.

<br>

<!---------------------------------------------------------------------------------------- Modes --->
## Modes

State recognizes `not set`, `configuring`, `planning`, `development`, `reviewing`, and `implementing` as active Modes. A Mode identifies the current or most recently recorded operational position only.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Active State** — the current or most recently recorded Workflow Mode, its Phase when applicable, and its recorded provenance.
- **Phase State** — aggregate Planning, Development, and Review progress for one stable Target phase identifier, plus its completion time once Development is completed and Review is satisfied.
- **Log Entry** — one record of a Skill execution. Its project-wide identifier is a sequential, zero-padded number (`001`, `002`, …); it holds known start information while work is in progress, then its completion time, duration, outcome, report, and applicable execution data when work ends.
- **Workflow Mode** — the current or most recently recorded operational position of the project.
- **Blocker** — a condition that genuinely prevents safe or valid continuation.
- **Open Question** — a critical decision that cannot safely be made without a human.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Uses Target Phase identity** — uses stable Phase identifiers without copying Phase goals or Target meaning.

Technical choices and defaults belong to State Preferences, which currently define none. The exact shape and initial values of State Config belong to the State Schema.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

State owns aggregate operational records. Target and Development remain the authorities for project and product meaning, and Plan remains the authority for individual Task records.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles in this Definition govern State. State Preferences are empty, and the State Schema owns record shape and initial values.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### State records the active Workflow position

**Rule:** State records the current or most recently entered Workflow Mode and the Phase being acted on when work is Phase-specific. The active Phase is null when work is not Phase-specific or when coordination spans multiple Phases.

**Why:** Anyone joining the work can immediately see its current operational position.

**Boundary:** Active State is descriptive, not an authorization gate. A completed record leaves its most recently recorded Mode in place; it does not reset State to `not set`.

<br>

### The Workflow has six modes

**Rule:** State recognizes `not set`, `configuring`, `planning`, `development`, `reviewing`, and `implementing`. The initial Mode is `not set`; the active Phase is null when work is not Phase-specific or when coordination spans multiple Phases.

**Why:** A stable vocabulary makes the recorded project position clear without imposing a one-way lifecycle.

**Boundary:** Launch and Reset are recorded events; they do not introduce additional active Modes.

<br>

### Every Target phase has aggregate operational State

**Rule:** State keeps one Phase State for every stable Target Phase identifier. Planning and Development use `not started`, `in progress`, `completed`, or `blocked`. Review uses `not started`, `in progress`, `satisfied`, or `not satisfied`; `not satisfied` identifies an unresolved Review result. State records the Phase's `completed_at` time only when Development is `completed` and Review is `satisfied`.

**Why:** Target stays human-owned while State records where every Phase stands.

**Boundary:** Phase State never copies a Phase title, goal, target, readiness, or enabled status. It never duplicates individual Task status, evidence, or history. New or replacement development work clears `completed_at`.

<br>

### Phase records reconcile without erasing progress

**Rule:** State reconciles Phase records from stable Target Phase identifiers and preserves existing records. New records begin with every progress field at `not started`. A removed Target Phase is not silently deleted when its State carries meaningful progress or provenance; that conflict is recorded. A record that still contains only initialization defaults may be removed during reconciliation.

**Why:** Target phases can evolve without making recorded work disappear.

**Boundary:** Reconciliation establishes identity only; it does not interpret Phase meaning or decide implementability.

<br>

### Phase progress fields change independently

**Rule:** A planning occurrence updates Planning progress, a development occurrence updates Development progress, and a review occurrence updates Review progress for the active Phase. New or replacement development work clears `completed_at` when it reopens a completed Phase.

**Why:** Independent fields prevent one kind of recorded progress from overstating another.

**Boundary:** Completion of one progress field never implies completion of another.

<br>

### The Log preserves operational evidence

**Rule:** State retains one Log Entry for every Skill execution. Its `id` is the next project-wide sequential number, zero-padded to at least three digits (`001`, `002`, …); the Skill and timestamps remain separate fields. Common fields are optional and include identity, Skill, parent, Phase, event, outcome, timing, token usage, Open Questions, Blockers, and report. Execution-specific values belong under that Entry's `data`, which may be a nested mapping or list.

**Why:** Active records show the present while the Log preserves how the project reached it.

**Boundary:** The Log never copies Task histories, command transcripts, secrets, or Target content. Detailed Task history remains in the Plan Config and its Task Logs.

<br>

### The Log preserves Blockers and Open Questions

**Rule:** State preserves Blockers and Open Questions associated with a Log Entry as part of the project's recorded position. Their execution-specific details belong under that Entry's `data`.

**Why:** Current problems and unresolved decisions are part of understanding the project's present condition and history.

**Boundary:** State does not define the shape or content of those execution-specific details.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

The status information State keeps for the project.

**State records the active Workflow position**

- **Must** — record the active Workflow position without making it an authorization gate

**The Workflow has six modes**

- **Must** — use only the six defined Modes for the active project position
- **Must** — keep Launch and Reset as recorded events, not active Modes

**Every Target phase has aggregate operational State**

- **Must** — keep aggregate Planning, Development, and Review progress by stable phase identifier
- **Must** — use `blocked` for blocked Planning or Development and `not satisfied` for a blocked Review
- **Must** — set `completed_at` only when Development is completed and Review is satisfied, and clear it for new or replacement development work
- **Never** — copy Target meaning or individual Task status, evidence, or history into State

**Phase records reconcile without erasing progress**

- **Must** — preserve existing progress while reconciling phase identity

**Phase progress fields change independently**

- **Must** — change only the applicable Planning, Development, or Review field
- **Never** — infer completion of one progress field from another

**The Log preserves operational evidence**

- **Must** — retain one concise Log Entry for every Skill execution
- **Must** — assign each Log Entry the next project-wide sequential, zero-padded identifier
- **Must** — keep execution-specific information only in `data`
- **Never** — copy Task histories, transcripts, secrets, or Target content into the Log

**The Log preserves Blockers and Open Questions**

- **Must** — retain their presence as part of the project's recorded position
