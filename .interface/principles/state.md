# State Principles

State is the Component that records where the Interface Workflow currently stands. It provides one small shared view of the active working mode, the active phase when one applies, the critical conditions that have stopped progress, and the questions still waiting on a human, so that anyone joining the project can see its current position without reconstructing it.

State does not contain the project definition, implementation plan, application configuration, or product code.

## Terms

- **Workflow** — the ordered path the project follows, from defining the project through planning and implementing its phases.
- **Mode** — the working position the Workflow currently occupies, drawn from a fixed set of values.
- **Active State** — the record of the current mode, its phase when one applies, and the reason, author, and time of the latest update.
- **Phase** — the project stage being acted on, present only when the current work is specific to one stage.
- **Blocker** — a condition that genuinely prevents safe or valid continuation, recorded until it is verified as resolved.
- **Open Question** — a critical decision that cannot safely be made without a human, recorded until the human's answer resolves it.
- **Provenance** — the reason, author, and time recorded with every change to the Active State.

## Relationships

- **Consumed by Task** — a Task references the Blocker records that State owns when it cannot proceed.
- **Consumes no other Component** — State records only its own position, Blockers, and Open Questions.

Technical choices and defaults belong to State Preferences, which currently define none. The exact shape of the generated State configuration belongs to the State Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. State records Workflow position

**Rule:** State records the current or most recently entered Workflow mode and the phase being acted on when the operation is phase-specific.

**Why:** One small shared record answers "where does the Workflow stand" for everyone at once, without any of them reconstructing it.

**Boundary:** State describes what is happening rather than what the project contains. Task progress belongs to the Task Component: State may reference the active phase or a blocking condition, but it never duplicates the status or history of individual Tasks.

<br>

## 2. The Workflow has four modes

**Rule:** State recognizes these modes:

- `not set` — no Workflow operation has yet been recorded;
- `configuring` — project Understanding is being generated or refreshed;
- `planning` — Plans, Groups, and Tasks are being generated or reconciled; and
- `development` — eligible Tasks are being implemented and verified.

The initial mode is `not set`.

**Why:** A fixed, small vocabulary lets every operation and every human name the same situation the same way.

**Boundary:** A phase is absent when the active operation does not act on one specific phase.

<br>

## 3. Modes never make an operation one-time-only

**Rule:** Every Workflow operation is repeatable. Configuring may run after configuring, planning, or development. Planning may run again for an already planned phase. Development may run again for an already developed or partially developed phase. State never rejects an invocation merely because that operation ran before or because the same mode is already active.

**Why:** Real work revisits earlier stages, and each operation is responsible for reconciling its own existing output, preserving information it does not own, and skipping work that is already complete.

**Boundary:** An operation may still reject invalid input or stop for a genuine critical blocker. That decision comes from the operation's own contract and current project Understanding, never from a one-way State lifecycle.

<br>

## 4. Active State is descriptive, not an authorization gate

**Rule:** The active State records the mode, optional phase, reason, provenance, and time of the latest State update. Entering a mode replaces those active values with the current operation's values.

**Why:** State exists to describe the situation, not to police it; permission comes from each operation's own contract.

**Boundary:** No fixed transition graph restricts which mode may follow another. The human may request any applicable Workflow operation from any current mode, including re-entering the same mode.

<br>

## 5. Operations update only the State they own

**Rule:** An operation may record its own active mode and may raise, update, or release blockers and questions encountered during its work.

**Why:** State is shared by everything that touches the project, so a narrow write boundary is what keeps it trustworthy.

**Boundary:** An operation does not rewrite project meaning, Task content, or another Component's owned information through State. A reset may restore active State as part of its explicit reset behaviour, but State does not duplicate the reset algorithm or the files affected by it.

<br>

## 6. Blockers are reserved for critical stoppages

**Rule:** A Blocker records a condition that genuinely prevents safe or valid continuation. Every Blocker states what is blocked, what is missing, why continuation is impossible, who or what can resolve it, and which operation or human raised it. After an authorized operation verifies resolution, the Blocker is removed from the unresolved collection.

**Why:** A Blocker interrupts the human, so the record is only useful while it names a stoppage that is real and currently unresolved.

**Boundary:** Ordinary ambiguity, an unspecified implementation detail, or a decision that can be made through professional judgment is not a Blocker.

<br>

## 7. Open Questions belong to the human

**Rule:** An Open Question records a critical decision that cannot safely be resolved without human input. It explains the decision required, why it matters, and any Blocker it would release. An operation may raise the question and record an answer supplied by the human. The question records who raised it and when; a supplied answer records its value, author, and time. After the answer fully resolves the question, the question is removed from the unresolved collection.

**Why:** Some decisions change project intent, and guessing one produces work the human never asked for.

**Boundary:** An operation never invents the human's answer. Non-critical uncertainty is resolved through professional judgment and does not become an Open Question.

<br>

## 8. State changes retain provenance

**Rule:** Every active-State update records why it occurred, who or which operation recorded it, and when it was recorded.

**Why:** State must remain understandable without reconstructing its latest transition from logs elsewhere.

**Boundary:** Provenance explains the latest update only. The record of individual Task transitions belongs to the Task Component.

<br>

## At a Glance

- **Must** — State records the current or most recent mode, and the phase when the work is phase-specific *(1)*
- **Never** — State duplicates the status or history of individual Tasks *(1)*
- **Must** — the mode is one of `not set`, `configuring`, `planning`, or `development`, starting at `not set` *(2)*
- **Must** — the phase is absent when the current work is not specific to one phase *(2)*
- **Must** — every Workflow operation stays repeatable, and each reconciles its own existing output *(3)*
- **Never** — State rejects an invocation because that operation ran before or its mode is already active *(3)*
- **Must** — entering a mode replaces the active values with the current operation's values *(4)*
- **Never** — a fixed transition graph restricts which mode may follow another *(4)*
- **Must** — an operation records only its own active mode and the blockers and questions it encounters *(5)*
- **Never** — an operation rewrites project meaning, Task content, or another Component's information through State *(5)*
- **Must** — a Blocker states what is blocked, what is missing, why, who can resolve it, and who raised it *(6)*
- **Must** — a Blocker is removed once an authorized operation verifies its resolution *(6)*
- **Never** — ordinary ambiguity or a judgment call becomes a Blocker *(6)*
- **Must** — an Open Question states the decision, why it matters, and any Blocker its answer would release *(7)*
- **Must** — a recorded answer carries its value, author, and time, and the question is removed once resolved *(7)*
- **Never** — an operation invents the human's answer, or raises non-critical uncertainty as an Open Question *(7)*
- **Must** — every active-State update records why, by whom, and when *(8)*
