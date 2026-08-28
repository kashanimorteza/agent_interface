---
description: Planning mode — decide what will be built and in what order
---

Planning mode. Read `.agent/config/root.yaml` and follow its `read_order` before anything else.

Check `.agent/config/state.yaml`: `content.active.mode` must be `planning`. If it says otherwise, stop and tell the human — an agent never changes the active mode.

What this mode may write is defined in `root.yaml` under `content.modes.planning`:

- the item files, `backend.yaml` and `frontend.yaml` — their settings and draft contracts, never a frozen contract
- `task.yaml` — the `phases` of a plan only, never `task_schema`, `task_states`, or a plan's `phase_titles`
- `state.yaml` — blockers and open questions, never `active`

Never: any file under an item's `code_path`, a frozen contract, `root.yaml`, `definition.yaml`, `rules.yaml`, or `schema/`.

When writing a task:

- Plans are per item. A task goes under `content.plans.<item>` in `task.yaml` — the plan of the item that owns the code it touches — and never depends on a task sitting under another item. Each item numbers its own phases from P1.
- A task is only ever written against a **frozen** contract. If the contract it needs is a draft or does not exist, the task is not written; the gap is a blocker in `state.yaml`.
- No task is written speculatively. Write tasks for exactly what the human asked for, and no more.
- Every task carries exactly the fields of `task_schema`, including a `verify` command that actually proves its `acceptance`.

$ARGUMENTS
