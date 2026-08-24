# Agent Project Interface — v1.0

A file-based contract between a project and any agent working on it. No runtime, no
database: plain YAML in git, readable by any agent from any vendor.

All paths are relative to this folder — the one containing `root.yaml`.

---

## File layout

```text
root.yaml                              ✓ entry point and protocol
structure.yaml                         ✓ the map — where every layer lives
project.yaml                           ✓ product definition
rules.yaml                             ✓ security and quality rules
state.yaml                             ✓ state layer index
develop/
├── develop.yaml                       ✓ build layer index
├── backend/
│   ├── definition.yaml                ✓ what this item is
│   ├── rules.yaml                     ✓ item-specific rules
│   ├── plan.yaml                      ✓ 12 tasks in 5 groups
│   └── status.yaml                    ✓ task status and reports
├── frontend/
│   ├── definition.yaml                ✓ what this item is
│   ├── rules.yaml                     ✓ item-specific rules
│   ├── plan.yaml                      ✓ 10 tasks in 5 groups
│   └── status.yaml                    ✓ task status and reports
└── shared/
    └── contracts/
        └── api-v1.yaml                ✗ not yet — the backend/frontend interface
history/
├── history.yaml                       ✓ history layer index
├── decisions/                         ✗ empty — filled by the first ADR
└── journal/                           ✗ empty — filled by the first session
stage.yaml                             ✗ not yet — active mode and item
blockers.yaml                          ✗ not yet — open blockers
questions.yaml                         ✗ not yet — queue for the human
counters.yaml                          ✗ not yet — id counters
```

---

## Layers

| Layer | File | Answers | Agent may edit |
| --- | --- | --- | --- |
| 1 | `root.yaml` | How do I behave? | no |
| — | `structure.yaml` | Where is everything? | no |
| 2 | `project.yaml` | What are we building and why? | no |
| 3 | `rules.yaml` | What am I forbidden to do? | no |
| 4 | `develop/develop.yaml` | What items exist and how are they shaped? | no |
| cross | `state.yaml` | Where are we right now? | index no, files yes |
| cross | `history/history.yaml` | Why did we end up here? | index no, files yes |

Each layer defines itself. `root.yaml` holds no content of its own — it points at
`structure.yaml`, which points at every layer index.

---

## Read order

Every session starts here, in exactly this order:

```text
1.  root.yaml                  protocol, modes, write rules
2.  structure.yaml             where the other layers live
3.  state.yaml                 which state files exist and which are writable
4.  state files                active mode and item, human answers, open blockers
5.  project.yaml               what is being built
6.  rules.yaml                 every rule — security overrides everything
7.  develop/develop.yaml       which items exist, task schema, task states
8.  active item                definition.yaml → rules.yaml → plan.yaml
9.  status.yaml                what is done, what remains, what is blocked
```

---

## Inside root.yaml

```text
root.yaml
│
├── meta
│   ├── standard
│   ├── version
│   ├── purpose
│   ├── independence
│   ├── entry_rule
│   ├── on_change_needed
│   ├── agent_may_edit
│   └── updated
│
├── structure
│   ├── path
│   ├── responsibility
│   └── note
│
├── read_order
│   ├── enforcement
│   └── steps                  (9 steps)
│
├── modes
│   ├── active_mode_source
│   ├── switch_rule
│   ├── planning
│   │   ├── purpose
│   │   ├── allowed
│   │   ├── prohibited
│   │   ├── may_write
│   │   └── steps
│   └── development
│       ├── purpose
│       ├── allowed
│       ├── prohibited
│       ├── may_write
│       └── steps
│
└── write_protocol
    ├── task_status_change
    ├── work_details
    ├── session_report
    ├── decision
    ├── blocker
    ├── question_for_human
    ├── new_id
    ├── root_change_needed
    ├── new_item_needed
    ├── rule_change_needed
    └── rule_conflict
```

---

## Inside structure.yaml

```text
structure.yaml
│
├── meta
│   ├── name
│   ├── purpose
│   ├── completeness
│   ├── depth
│   ├── agent_may_edit
│   ├── on_change_needed
│   └── updated
│
├── layers
│   ├── layer_1 … layer_4
│   └── cross_1, cross_2
│
└── map
    ├── root                   layer, path, responsibility, note
    ├── project                layer, path, responsibility, note
    ├── rules                  layer, path, responsibility, note
    ├── develop                layer, path, responsibility, note
    ├── state                  layer, path, responsibility, note
    └── history                layer, path, responsibility, note
```

---

## Inside project.yaml — layer 2

```text
project.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── purpose
│   ├── scope_note
│   ├── reason
│   ├── on_change_needed
│   ├── agent_may_edit
│   └── updated
│
├── identity
│   ├── id
│   ├── name
│   └── one_liner
│
├── goals
│
├── non_goals
│   ├── note
│   └── items
│
├── outcomes
│   ├── note
│   └── items
│
├── architecture
│   ├── note
│   ├── shape
│   ├── data
│   ├── boundary
│   └── decided_elsewhere
│
└── constraints
    ├── note
    └── items
```

---

## Inside rules.yaml — layer 3

```text
rules.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── purpose
│   ├── completeness
│   ├── reason
│   ├── on_change_needed
│   ├── item_rules_exception
│   ├── agent_may_edit
│   └── updated
│
├── security                   binding: absolute
│   ├── binding
│   ├── binding_note
│   ├── responsibility
│   ├── items                  (9 prohibitions)
│   └── on_violation
│
├── global                     binding: mandatory
│   ├── binding
│   ├── binding_note
│   ├── responsibility
│   ├── items                  (8 quality rules)
│   └── on_violation
│
├── precedence
│   ├── order                  security → global → item rules
│   ├── on_conflict
│   └── security_conflict
│
└── scope
    ├── applies_to
    ├── item_rules
    └── unwritten
```

---

## Inside develop.yaml — layer 4

```text
develop/develop.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── purpose
│   ├── completeness
│   ├── reason
│   ├── on_change_needed
│   ├── item_files_exception
│   ├── agent_may_edit
│   └── updated
│
├── items
│   ├── backend                enabled, path, prefix, code_path, summary
│   └── frontend               enabled, path, prefix, code_path, summary
│
├── item_files
│   ├── rule
│   └── files                  definition / rules / plan / status
│
├── item_read_order
│
├── task_schema
│   ├── rule
│   └── fields
│       ├── id
│       ├── title
│       ├── goal
│       ├── depends_on
│       ├── needs_contract
│       ├── acceptance
│       ├── verify
│       └── touches
│
├── task_states
│   ├── rule
│   ├── states                 todo / claimed / blocked / done / cancelled / superseded
│   ├── derived_ready
│   ├── done_gate
│   └── claim_protocol
│
├── shared
│   └── contracts
│       ├── path
│       ├── responsibility
│       ├── lifecycle          draft / frozen / deprecated
│       └── change_rule
│
└── boundaries
    ├── code_isolation
    ├── cross_item_link
    └── contract_change
```

---

## Inside state.yaml — cross-cutting

```text
state.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── purpose
│   ├── write_mode             overwrite
│   ├── history_rule
│   ├── index_agent_may_edit   false
│   ├── index_on_change_needed
│   ├── files_agent_may_edit   true
│   └── updated
│
├── files
│   ├── stage                  agent_may_edit: false — the mode is the agent's boundary
│   ├── blockers               agent_may_edit: true
│   ├── questions              agent_may_edit: true
│   └── counters               agent_may_edit: true
│
├── read_order
│   ├── enforcement
│   └── steps                  stage → questions → blockers → counters
│
└── rules
    ├── single_source
    ├── task_status_exception
    ├── answered_question
    ├── resolved_blocker
    └── no_silent_change
```

---

## Inside history.yaml — cross-cutting

```text
history/history.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── purpose
│   ├── write_mode             append-only
│   ├── immutability
│   ├── index_agent_may_edit   false
│   ├── index_on_change_needed
│   ├── files_agent_may_edit   true
│   └── updated
│
├── records
│   ├── decisions              ADR-0001-<slug>.yaml
│   │   ├── path
│   │   ├── responsibility
│   │   ├── file_pattern
│   │   ├── id_source
│   │   ├── when_to_write
│   │   └── fields             id, title, date, context, decision,
│   │                          alternatives, consequences, status, superseded_by
│   └── journal                <YYYY-MM-DD>-<seq>-<item>.yaml
│       ├── path
│       ├── responsibility
│       ├── file_pattern
│       ├── when_to_write
│       └── fields             date, mode, item, tasks_touched, decisions_made,
│                              blockers_opened, blockers_resolved, questions_asked,
│                              unfinished, next
│
└── rules
    ├── append_only
    ├── no_deletion
    ├── supersede_not_edit
    ├── session_mandatory
    ├── handoff
    ├── no_state_here
    └── id_before_write
```

---

## Inside an item — the same four files for every item

```text
develop/<item>/
│
├── definition.yaml            what this item is
│   ├── meta                   item, layer, purpose, agent_may_edit,
│   │                          editable_in_mode, on_change_needed, updated
│   ├── responsibility
│   ├── code_path
│   ├── tech
│   ├── code_layout
│   ├── contracts              produces / consumes, contract_path, rule
│   ├── boundaries             owns, does_not_own, interface
│   └── out_of_scope
│
├── rules.yaml                 item-specific rules — may only tighten
│   ├── meta                   item, layer, purpose, relation_to_global,
│   │                          agent_may_edit, editable_in_mode, updated
│   └── <rule groups>          backend: code, database, security, test, contract
│                              frontend: code, ui, auth, contract, test
│
├── plan.yaml                  task definitions — never status
│   ├── meta                   item, layer, purpose, schema_source,
│   │                          no_status_here, agent_may_edit,
│   │                          editable_in_mode, change_in_development, updated
│   └── groups
│       └── <group>            id, title, goal
│           └── tasks
│               └── <task>     id, title, goal, depends_on, needs_contract,
│                              acceptance, verify, touches
│
└── status.yaml                task status — never definitions
    ├── meta                   item, layer, purpose, states_source,
    │                          agent_may_edit, editable_in_mode,
    │                          write_rule, updated
    ├── summary                total, done, claimed, blocked, todo (derived)
    ├── tasks
    │   └── <task id>          status + the fields below as work progresses
    ├── entry_schema
    │   ├── rule
    │   └── fields             status, claimed_at, verify_result, done_at,
    │                          notes, blocker, unfinished, superseded_by,
    │                          cancel_reason
    └── example
```

---

## Load-bearing rules

These are the decisions the whole standard rests on. Breaking any one of them
breaks something else downstream.

**A file's content lives in exactly one place.** `root.yaml` holds no map;
`structure.yaml` holds no rules; `rules.yaml` holds no task list. Every layer
defines itself and everything else points at it.

**Definition and status never mix.** `plan.yaml` says what a task is and never
changes; `status.yaml` says where it stands and changes constantly. A task in
`plan.yaml` has no status field.

**No task is done without a passing `verify`.** Acceptance criteria are runnable
commands, not prose. A status of `done` with no `verify_result: pass` is a lie the
next agent cannot detect.

**`ready` is derived, never stored.** A task is ready when it is `todo` and all of
its `depends_on` are `done`. Storing readiness would create a second source of
truth that drifts from the dependency graph.

**Items never depend on each other's tasks.** Cross-item coupling goes through
`needs_contract` and a versioned contract in `shared/contracts/`. This turns an
N×M dependency web into two checkpoints: draft and frozen.

**An agent never moves its own boundary.** `root.yaml`, `structure.yaml`,
`project.yaml`, `rules.yaml`, `develop.yaml`, and `stage.yaml` are human-only. An
agent that needs one changed records a proposal in `questions.yaml` and waits.

**State is overwritten, history is appended.** `state.yaml` answers "where are we
now" and keeps nothing; `history/` answers "why did we get here" and deletes
nothing. Mixing the two destroys both.

**Every session ends with a journal entry.** Without it the session is incomplete.
Unfinished work must record its exact stopping point so the next agent resumes
instead of redoing or breaking things.

---

## Still to build

| File | Purpose |
| --- | --- |
| `stage.yaml` | Active mode and active item — human-written |
| `blockers.yaml` | Open blockers |
| `questions.yaml` | Question and proposal queue for the human |
| `counters.yaml` | Id counters — BE, FE, ADR, BLK, Q |
| `develop/shared/contracts/api-v1.yaml` | The backend/frontend interface both items reference |
