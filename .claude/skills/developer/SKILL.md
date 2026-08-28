---
name: developer
description: Development mode — take the ready tasks from `.agent/config/task.yaml` and implement them one at a time, under the active item's `code_path`, gated on each task's `verify`. Use when the human asks for a task to be built or continued, or when `/develop` is run. Builds only; never plans.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Execute the plan

Development mode. Read `.agent/config/root.yaml` and follow its `read_order` before anything else. The Config and the plan inside `task.yaml` are what you build from — `.agent/project.md` is not read here.

Check `.agent/config/state.yaml`: `content.active.mode` must be `development`, and `content.active.item` names the item you are on. If either disagrees with what you were asked to do, stop and tell the human.

Take a task from `content.plans.<active item>` in `task.yaml`. A task is ready when its `status` is `todo` and every id in its `depends_on` is `done` — `ready` is not a stored status. Never take a task from another item's plan.

## The loop

Run it once per task, one task at a time:

1. Set the task's `status` to `claimed` and write `task.yaml` immediately, before any other work — so no second agent takes the same task.
2. Write only files under the active item's `code_path`, and only the paths listed in that task's `touches`.
3. Run the task's `verify` from the item's `verify_cwd`. Its passing is the gate — the code being written is not.
4. On a pass, set `status: done` and append a dated entry to `log`. On a blocker, set `status: blocked`, name the blocker id, state what is missing in `state.yaml`, and stop.

Then take the next ready task and start the loop again.

## Rules while building

- In this mode `status`, `blocker`, and `log` are the only fields of a task you may change. Everything else is the plan, and changing it takes a reason written into that task's log plus the human's approval.
- Follow the project's own rules — `rules.yaml` is the authority, and a rule that is not in it is not a rule. The item file gives that item's conventions, `code_path`, and `verify_cwd`.
- Never invent your way past a missing contract or a missing decision. That is a blocker in `state.yaml`, not a guess in the code.
- `log` is append-only — a past entry is never rewritten.

## Not this mode's work

Do not write, renumber, or re-scope tasks, and do not change `task_schema`, `task_states`, or a plan's `phase_titles`. Planning belongs to the `planner` Skill. If the plan is wrong, say so and stop.
