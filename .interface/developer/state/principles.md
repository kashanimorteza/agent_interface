# State Principles

State records the operational condition of the Interface Workflow: the active mode, aggregate progress for each Target phase, end-to-end implementation, runtime launch, critical stoppages, and Workflow history.

State never contains Target meaning, implementation instructions, application configuration, product code, or the status and history of individual Tasks.

## Terms

- **Active State** — the current or most recently entered Workflow mode, its phase when applicable, and update provenance.
- **Phase State** — aggregate Planning, Development, and Review progress for one stable Target phase identifier.
- **Implementation State** — progress of the current end-to-end Implement run across phases that are presently implementable.
- **Launch State** — runtime condition, selected Environment and Launch method, and verified access points.
- **History Event** — one append-only record of a Workflow operation and its outcome.
- **Blocker** — a condition that genuinely prevents safe or valid continuation.
- **Open Question** — a critical decision that cannot safely be made without a human.

## Relationships

- **Consumes Target phase identity** — uses stable phase identifiers without copying phase goals or Target meaning.
- **Consumes operation outcomes** — each operation records only the aggregate State and history its role owns.
- **Consumed by operations and reporting** — enables work to resume without reconstructing operational progress.

Technical choices and defaults belong to State Preferences, which currently define none. The exact shape and initial values of State Config belong to the State Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a Target may only add stricter rules, never looser ones.

<br>

## 1. State records the active Workflow position

**Rule:** State records the current or most recently entered Workflow mode and the phase being acted on when the operation is phase-specific.

**Why:** Anyone joining the work can immediately see its current operational position.

**Boundary:** Active State is descriptive, not an authorization gate, and never prevents an operation merely because it ran before.

<br>

## 2. The Workflow has four modes

**Rule:** State recognizes `not set`, `configuring`, `planning`, and `development`. The initial mode is `not set`; the active phase is null when work is not phase-specific.

**Why:** A stable vocabulary aligns every operation without imposing a one-way lifecycle.

**Boundary:** Review, Launch, Implement, and Reset update their own State records and History without inventing additional active modes.

<br>

## 3. Every Target phase has aggregate operational State

**Rule:** State keeps one Phase State for every stable Target phase identifier. Planning and Development use `not started`, `in progress`, or `completed`. Review uses `not started`, `in progress`, `satisfied`, `not satisfied`, or `inconclusive`.

**Why:** Target stays human-owned while operations can record where every phase stands.

**Boundary:** Phase State never copies a phase title, goal, target, readiness, or enabled status. It never duplicates individual Task status, evidence, or history.

<br>

## 4. Phase records reconcile without erasing progress

**Rule:** Configure creates missing Phase State records from stable Target phase identifiers and preserves existing records. New records begin with every operation at `not started`. A removed Target phase is not silently deleted when its State carries meaningful progress or provenance; the conflict is reported. A record that still contains only initialization defaults may be removed during synchronization.

**Why:** Target phases can evolve without making recorded work disappear.

**Boundary:** Synchronization establishes identity only; it does not interpret phase meaning or decide implementability.

<br>

## 5. Operations update only their aggregate phase field

**Rule:** Planning updates Planning progress, Development updates Development progress, and Review updates Review progress for the active phase. Each records provenance and appends a History Event.

**Why:** Narrow ownership prevents one operation from overstating another's work.

**Boundary:** One operation's completion never implies another operation's completion.

<br>

## 6. Implementation State represents end-to-end orchestration

**Rule:** Implement records `not started`, `in progress`, `completed`, or `blocked`, with start, completion, and update provenance. `completed` means Configure succeeded, every phase implementable at that invocation was planned and developed, and Launch succeeded.

**Why:** End-to-end orchestration needs one truthful overall result in addition to per-phase progress.

**Boundary:** Disabled, unready, and future phases are never marked complete. A later Target change can make additional phases implementable.

<br>

## 7. Launch State records the observable runtime result

**Rule:** Launch State records `not launched`, `launching`, `launched`, `failed`, or `stopped`, together with the Environment, Launch method, provenance, and verified access points. Each access point has a name, kind, and address.

**Why:** A successful launch is useful only when people and systems know how to reach it.

**Boundary:** State stores no credentials, shared secrets, or private configuration values.

<br>

## 8. History is append-only operational evidence

**Rule:** Every operation that changes State appends a History Event containing a stable identifier, operation, optional phase, event, outcome, recorder, and time.

**Why:** Active records show the present while History explains how the Workflow reached it.

**Boundary:** History never copies Task histories, review Findings, command transcripts, secrets, or Target content.

<br>

## 9. Workflow operations remain repeatable

**Rule:** Configure, Planning, Development, Review, Launch, Implement, and Reset may run again. Each reconciles records it owns, preserves information outside its authority, and records the new outcome truthfully.

**Why:** Real projects revisit earlier work.

**Boundary:** An operation may stop for invalid input, an unmet prerequisite, or a genuine Blocker, but never solely because it ran before.

<br>

## 10. Reset reconciles State with what it removes

**Rule:** A confirmed Reset returns affected phase fields, Implementation State, and Launch State to values consistent with outputs that remain, and appends a reset History Event whenever State itself is preserved.

**Why:** State must not claim removed plans, implementation, review evidence, or runtime still exists.

**Boundary:** A Configure reset removes State Config itself and cannot append to that removed record.

<br>

## 11. Blockers are critical stoppages

**Rule:** A Blocker records what cannot continue, what is missing, why continuation is impossible, who can resolve it, and who raised it. It is removed only after verified resolution and authorized reconciliation of current references.

**Why:** A Blocker must identify a real, current stoppage.

**Boundary:** Ordinary ambiguity or a choice professional judgment can safely resolve is not a Blocker.

<br>

## 12. Open Questions belong to the human

**Rule:** An Open Question records the decision, why it matters, any Blocker it releases, and provenance. A human answer records its value, author, and time; the question is removed when fully resolved.

**Why:** Some choices materially change intent and cannot safely be guessed.

**Boundary:** An operation never invents a human answer or raises non-critical uncertainty as an Open Question.

<br>

## At a Glance

- **Must** — record the active Workflow position without making it an authorization gate *(1–2)*
- **Must** — keep aggregate Planning, Development, and Review progress by stable phase identifier *(3–5)*
- **Never** — copy Target meaning or individual Task status, evidence, or history into State *(3–4)*
- **Must** — preserve existing progress while reconciling phase identity *(4)*
- **Must** — record truthful Implement progress and exclude disabled or unready phases from completion *(6)*
- **Must** — record Launch status and verified access points without secrets *(7)*
- **Must** — append concise operational History for every State-changing operation *(8)*
- **Must** — keep operations repeatable and make confirmed Reset outcomes agree with State *(9–10)*
- **Must** — reserve Blockers and Open Questions for genuine critical conditions *(11–12)*
