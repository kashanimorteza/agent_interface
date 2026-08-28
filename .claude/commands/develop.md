---
description: Development mode — implement the tasks planning defined
---

Development mode. Read `.agent/config/root.yaml` and follow its `read_order` before anything else.

Check `.agent/config/state.yaml`: `content.active.mode` must be `development`, and `content.active.item` names the item you are on. If either disagrees with what you were asked to do, stop and tell the human.

Take a task from `content.plans.<active item>` in `task.yaml`. A task is ready when its `status` is `todo` and every id in its `depends_on` is `done` — `ready` is not a stored status. Never take a task from another item's plan.

The loop:

1. Set the task's `status` to `claimed` and write `task.yaml` immediately, before any other work — so no second agent takes the same task.
2. Write only files under the active item's `code_path`, and only the paths listed in that task's `touches`.
3. Run the task's `verify` from the item's `verify_cwd`. Its passing is the gate — the code being written is not.
4. On a pass, set `status: done` and append a dated entry to `log`. On a blocker, set `status: blocked`, name the blocker id, state what is missing in `state.yaml`, and stop.

In this mode `status`, `blocker`, and `log` are the only fields of a task you may change. Everything else is the plan, and changing it takes a reason written into that task's log plus the human's approval. Never invent your way past a missing contract or a missing decision. `log` is append-only — a past entry is never rewritten.

$ARGUMENTS
