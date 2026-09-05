# State Principles

State is the Component that records where the Interface Workflow currently stands. It provides a small, shared runtime view of the active working mode, the active phase when one applies, critical blockers, and unresolved human questions.

Every statement here is mandatory. Technical defaults, when any are defined, belong to State Preferences. The exact shape of the generated State configuration belongs to the State Schema.

<br>

## 1. State records Workflow position

State records the current or most recently entered Workflow mode and the phase being acted on when the operation is phase-specific. It describes what is happening; it does not contain the project definition, implementation plan, application configuration, or product code.

Task progress belongs to the Task Component. State may reference the active phase or a blocking condition, but it never duplicates the status or history of individual Tasks.

<br>

## 2. The Workflow has four modes

State recognizes these modes:

- `not set` — no Workflow operation has yet been recorded;
- `configuring` — project Understanding is being generated or refreshed;
- `planning` — Plans, Groups, and Tasks are being generated or reconciled; and
- `development` — eligible Tasks are being implemented and verified.

The initial mode is `not set`. A phase is absent when the active operation does not act on one specific phase.

<br>

## 3. Modes never make an operation one-time-only

Every Workflow operation is repeatable. Configuring may run after configuring, planning, or development. Planning may run again for an already planned phase. Development may run again for an already developed or partially developed phase.

State never rejects an invocation merely because that operation ran before or because the same mode is already active. Each operation is responsible for reconciling its own existing output, preserving information it does not own, and skipping work that is already complete.

An operation may still reject invalid input or stop for a genuine critical blocker. That decision comes from the operation's own contract and current project Understanding, never from a one-way State lifecycle.

<br>

## 4. Active State is descriptive, not an authorization gate

The active State records the mode, optional phase, reason, provenance, and time of the latest State update. Entering a mode replaces those active values with the current operation's values.

No fixed transition graph restricts which mode may follow another. The human may request any applicable Workflow operation from any current mode, including re-entering the same mode.

<br>

## 5. Operations update only the State they own

An operation may record its own active mode and may raise, update, or release blockers and questions encountered during its work. It does not rewrite project meaning, Task content, or another Component's owned information through State.

Reset may restore active State as part of its explicit reset behaviour, but State does not duplicate the reset algorithm or the files affected by it.

<br>

## 6. Blockers are reserved for critical stoppages

A Blocker records a condition that genuinely prevents safe or valid continuation. Ordinary ambiguity, an unspecified implementation detail, or a decision that can be made through professional judgment is not a Blocker.

Every Blocker states what is blocked, what is missing, why continuation is impossible, and who or what can resolve it. A resolved Blocker is removed or marked resolved by an operation authorized to verify its resolution.

<br>

## 7. Open Questions belong to the human

An Open Question records a critical decision that cannot safely be resolved without human input. It explains the decision required, why it matters, and any Blocker it would release.

An operation may raise the question and record an answer supplied by the human. It never invents the human's answer. Non-critical uncertainty is resolved through professional judgment and does not become an Open Question.

<br>

## 8. State changes retain provenance

Every active-State update records why it occurred, who or which operation recorded it, and when it was recorded. State must remain understandable without reconstructing its latest transition from logs elsewhere.
