# Task states and how to read a plan

Loaded when you need the vocabulary, not on every status report.

## The six states

Written in `task.yaml → content.task_states`, on the `status` field of each task.

| status | meaning |
|---|---|
| `todo` | Defined, not started |
| `claimed` | An agent has taken it and is working on it |
| `blocked` | Stopped — the reason is stated to the human, who decides how to proceed |
| `done` | `verify` was run and passed |
| `cancelled` | No longer needed — the reason is in the task's log |
| `superseded` | Replaced — the successor id is in the task's log |

`ready` is **not** one of them. It is derived: `todo`, and every id in `depends_on` is `done`.

## Gates and protocols

- **done gate** — without a passing `verify` run from the item's `verify_cwd`, no task becomes `done`. Written code is not the gate.
- **claim protocol** — `status` goes to `claimed` and the file is written *before* work starts, so two agents never take the same task.
- **blocked protocol** — set `blocked`, name the blocker id from `state.yaml`, state what is missing, stop. Never invent past a missing contract or decision.
- **log** — append-only. A past entry is never rewritten.

## Reading a plan

Three levels, always: phases → groups → tasks. A task never sits directly in a phase, and nothing sits outside a phase. Ids are scoped to the item: `P1`, then `P1-G1`, then the task's own id.

Cross-item dependencies are forbidden. An item that needs something from another item names the contract version in `needs_contract` instead — that is the whole point of the contract.

## Why a plan is empty

`policy.task_creation` forbids writing a task speculatively, and `policy.coverage_rule` forbids naming a contract that is not frozen. So an empty plan is normal and usually means one of:

- the contract it would need is still a draft (check `backend.yaml → content.contracts`)
- the item's technology is not chosen yet (check the item file for `to be defined`)
- the human has simply not asked for tasks yet

Say which, citing the blocker id. Do not describe an empty plan as an oversight.
