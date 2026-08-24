# ساختار فایل‌ها — Agent Project Interface (نسخهٔ ۱.۰)

همهٔ مسیرها نسبی‌اند — نسبت به همین پوشه، جایی که `ROOT.yaml` در آن است.

```text
ROOT.yaml                          ✓ ساخته شده
STRUCTURE.yaml                     ✓ ساخته شده
PROJECT.yaml                       ✓ ساخته شده
RULES/
├── RULES.yaml                     ✓ ساخته شده
├── security.yaml                  ✗ هنوز نه
└── global.yaml                    ✗ هنوز نه
DEVELOP/
├── DEVELOP.yaml                   ✓ ساخته شده
├── backend/
│   ├── DEFINITION.yaml            ✗ هنوز نه
│   ├── RULES.yaml                 ✗ هنوز نه
│   ├── PLAN.yaml                  ✗ هنوز نه
│   └── STATUS.yaml                ✗ هنوز نه
├── frontend/                      ✗ همان چهار فایل
└── shared/
    └── contracts/                 ✗ هنوز نه
STATE/
├── STATE.yaml                     ✓ ساخته شده
├── stage.yaml                     ✗ هنوز نه
├── blockers.yaml                  ✗ هنوز نه
├── questions.yaml                 ✗ هنوز نه
└── counters.yaml                  ✗ هنوز نه
HISTORY/
├── HISTORY.yaml                   ✓ ساخته شده
├── decisions/                     ✗ خالی — با اولین ADR پر می‌شود
└── journal/                       ✗ خالی — با اولین جلسه پر می‌شود
```

---

## ساختار درونی ROOT.yaml — Agent Project Interface (نسخهٔ ۱.۰)

```text
ROOT.yaml
│
├── meta
│   ├── standard
│   ├── version
│   ├── purpose
│   ├── independence
│   ├── entry_rule
│   ├── agent_may_edit
│   ├── on_change_needed
│   └── updated
│
├── structure
│   ├── path
│   ├── responsibility
│   └── note
│
├── read_order
│   ├── enforcement
│   └── steps
│       ├── 1. ROOT.yaml
│       ├── 2. STRUCTURE.yaml
│       ├── 3. STATE/STATE.yaml
│       ├── 4. فایل‌های وضعیت
│       ├── 5. PROJECT.yaml
│       ├── 6. RULES/RULES.yaml
│       ├── 7. فایل‌های قاعده
│       ├── 8. DEVELOP/DEVELOP.yaml
│       ├── 9. DEFINITION → RULES → PLAN
│       └── 10. STATUS
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

## ساختار درونی STRUCTURE.yaml — نقشه

```text
STRUCTURE.yaml
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
│   ├── layer_1
│   ├── layer_2
│   ├── layer_3
│   ├── layer_4
│   ├── cross_1
│   └── cross_2
│
└── map
    ├── root
    │   ├── layer
    │   ├── path
    │   ├── responsibility
    │   └── note
    ├── project
    │   ├── layer
    │   ├── path
    │   ├── responsibility
    │   └── note
    ├── rules
    │   ├── layer
    │   ├── path
    │   ├── responsibility
    │   └── note
    ├── develop
    │   ├── layer
    │   ├── path
    │   ├── responsibility
    │   └── note
    ├── state
    │   ├── layer
    │   ├── path
    │   ├── responsibility
    │   └── note
    └── history
        ├── layer
        ├── path
        ├── responsibility
        └── note
```

---

## ساختار درونی PROJECT.yaml — لایهٔ ۲

```text
PROJECT.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── editable_by
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
│
├── outcomes
│
├── architecture
│   ├── shape
│   ├── data
│   ├── boundary
│   └── decided_elsewhere
│
└── constraints
```

---

## ساختار درونی RULES.yaml — لایهٔ ۳

```text
RULES.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── editable_by
│   └── updated
│
├── files
│   ├── security
│   │   ├── path
│   │   ├── responsibility
│   │   └── binding
│   └── global
│       ├── path
│       ├── responsibility
│       └── binding
│
├── read_order
│
├── precedence
│   ├── order
│   ├── on_conflict
│   └── security_conflict
│
└── scope
    ├── applies_to
    ├── item_rules
    └── unwritten
```

---

## ساختار درونی DEVELOP.yaml — لایهٔ ۴

```text
DEVELOP.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── editable_by
│   └── updated
│
├── items
│   ├── backend
│   │   ├── enabled
│   │   ├── path
│   │   ├── prefix
│   │   ├── code_path
│   │   └── summary
│   └── frontend
│       ├── enabled
│       ├── path
│       ├── prefix
│       ├── code_path
│       └── summary
│
├── item_files
│   ├── DEFINITION.yaml
│   ├── RULES.yaml
│   ├── PLAN.yaml
│   └── STATUS.yaml
│
├── item_read_order
│
├── shared
│   └── contracts
│       ├── path
│       └── responsibility
│
└── boundaries
    ├── code_isolation
    ├── cross_item_link
    └── contract_change
```

---

## ساختار درونی STATE.yaml — لایهٔ عرضی

```text
STATE.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── purpose
│   ├── write_mode
│   ├── history_rule
│   ├── index_agent_may_edit
│   ├── index_on_change_needed
│   ├── files_agent_may_edit
│   └── updated
│
├── files
│   ├── stage
│   │   ├── path
│   │   ├── responsibility
│   │   ├── agent_may_edit
│   │   ├── reason
│   │   └── on_change_needed
│   ├── blockers
│   │   ├── path
│   │   ├── responsibility
│   │   ├── agent_may_edit
│   │   └── linked_to
│   ├── questions
│   │   ├── path
│   │   ├── responsibility
│   │   ├── agent_may_edit
│   │   ├── write_rule
│   │   └── answer_rule
│   └── counters
│       ├── path
│       ├── responsibility
│       ├── agent_may_edit
│       ├── write_rule
│       └── uniqueness
│
├── read_order
│   ├── enforcement
│   └── steps
│       ├── stage.yaml
│       ├── questions.yaml
│       ├── blockers.yaml
│       └── counters.yaml
│
└── rules
    ├── single_source
    ├── task_status_exception
    ├── answered_question
    ├── resolved_blocker
    └── no_silent_change
```

---

## ساختار درونی HISTORY.yaml — لایهٔ عرضی

```text
HISTORY.yaml
│
├── meta
│   ├── layer
│   ├── layer_name
│   ├── purpose
│   ├── write_mode
│   ├── immutability
│   ├── index_agent_may_edit
│   ├── index_on_change_needed
│   ├── files_agent_may_edit
│   └── updated
│
├── records
│   ├── decisions
│   │   ├── path
│   │   ├── responsibility
│   │   ├── file_pattern
│   │   ├── id_source
│   │   ├── when_to_write
│   │   └── fields
│   │       ├── id
│   │       ├── title
│   │       ├── date
│   │       ├── context
│   │       ├── decision
│   │       ├── alternatives
│   │       ├── consequences
│   │       ├── status
│   │       └── superseded_by
│   └── journal
│       ├── path
│       ├── responsibility
│       ├── file_pattern
│       ├── when_to_write
│       └── fields
│           ├── date
│           ├── mode
│           ├── item
│           ├── tasks_touched
│           ├── decisions_made
│           ├── blockers_opened
│           ├── blockers_resolved
│           ├── questions_asked
│           ├── unfinished
│           └── next
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
