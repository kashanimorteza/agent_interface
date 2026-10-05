# State Definition

State is the Operation Component that records the aggregate operational position of the project.


<br>

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

State records the operational condition of the project: the active Mode, aggregate progress for each Target Phase, and the Log of its execution history.

State never contains Target meaning, implementation instructions, application configuration, product code, or the status and history of individual Tasks.

### Purpose

Work that spans Phases and sessions needs a reliable record of where the project currently stands: which Mode is active, how far each Phase has progressed, and which recorded outcomes still matter. Its Log holds concise records and never replaces the sources.

### How It Works

Each Operation updates its Phase progress and its own Log Entry in State.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Active State** — the current or most recently recorded Workflow Mode, its Phase when applicable, and its recorded provenance.
- **Phase State** — aggregate Planning, Development, and Review progress for one stable Target phase identifier, plus its completion time once Development is completed and Review is satisfied.
- **Log Entry** — one record of a Skill execution.
- **Workflow Mode** — the current or most recently recorded operational position of the project.
- **Blocker** — a condition that genuinely prevents safe or valid continuation.
- **Open Question** — a decision recorded for the Human to review later; work continues with the current choice meanwhile.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Target** — uses stable Phase identifiers without copying Phase goals or Target meaning.

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

**Rule:** State retains one Log Entry for every Skill execution. Its `id` is the next project-wide sequential number, zero-padded to at least three digits (`001`, `002`, …); the Skill and timestamps remain separate fields. Common fields are optional and include identity, Skill, parent, Phase, event, outcome, timing, token usage, Open Questions, Blockers, and report. Execution-specific values belong under that Entry's `data`, which may be a nested mapping or list. The Log preserves every Entry: in progress, completed, stopped, and blocked.

**Why:** Active records show the present while the Log preserves how the project reached it.

**Boundary:** The Log never copies Task histories, command transcripts, secrets, or Target content. Detailed Task history remains in the Plan Config and its Task Logs.

<br>

### Duration is readable

**Rule:** When an execution duration can be determined, State records it in `duration`. A duration below one minute is written as `<seconds> seconds`; a duration of one minute or more is written as `<minutes>:<seconds>`, with seconds zero-padded to two digits.

**Why:** One readable value makes the Log immediately understandable without duplicating the same duration.

**Boundary:** State does not invent a duration when start or completion time is unknown; `duration` remains absent or null in that case.

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

**Duration is readable**

- **Must** — record a readable `duration` when execution timing is available
- **Must** — format durations below one minute as seconds and longer durations as `minutes:seconds`

**The Log preserves Blockers and Open Questions**

- **Must** — retain their presence as part of the project's recorded position
