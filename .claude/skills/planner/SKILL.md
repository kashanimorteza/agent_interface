---
name: planner
description: Planning mode — decide what will be built and in what order, and write tasks into `.agent/config/task.yaml` in the shape `task_schema` defines. Use when the human asks for a plan or for tasks, or when `/plan` is run. Plans only; never implements.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Plan the build

Planning mode. Read `.agent/config/root.yaml` and follow its `read_order` before anything else. The generated Config is your understanding of the project — plan from it, not from `.agent/project.md`, which the `configurator` Skill owns.

Check `.agent/config/state.yaml`: `content.active.mode` must be `planning`. If it says otherwise, stop and tell the human — an agent never changes the active mode.

## What this mode may write

Defined in `root.yaml` under `content.modes.planning`:

- the item files, `backend.yaml` and `frontend.yaml` — their settings and draft contracts, never a frozen contract
- `task.yaml` — the `phases` of a plan only, never `task_schema`, `task_states`, or a plan's `phase_titles`
- `state.yaml` — blockers and open questions, never `active`

Never: any file under an item's `code_path`, a frozen contract, `root.yaml`, `definition.yaml`, `rules.yaml`, or `schema/`.

## Writing a task

Read `task_schema` and `task_states` in `task.yaml` first — they are the frame, fixed by the human, and every task you write takes its shape from them.

- Plans are per item. A task goes under `content.plans.<item>` in `task.yaml` — the plan of the item that owns the code it touches — and never depends on a task sitting under another item. Each item numbers its own phases from P1.
- A task is only ever written against a **frozen** contract. If the contract it needs is a draft or does not exist, the task is not written; the gap is a blocker in `state.yaml`.
- No task is written speculatively. Write tasks for exactly what the human asked for, and no more.
- Every task carries exactly the fields of `task_schema`, including a `verify` command that actually proves its `acceptance`.

## Not this mode's work

Do not implement, test, or refactor anything, and do not run a task's `verify` to see whether it would pass. Executing tasks is the `developer` Skill's job. Planning produces the plan and stops.

Anything Phase 1 leaves undefined stays undefined: write it as an open question in `state.yaml`, never as a plausible value in a contract or a task.
