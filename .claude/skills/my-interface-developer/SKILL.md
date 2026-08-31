---
name: my-interface-developer
description: Development mode — take the ready tasks from `.interface/config/task.yaml` and implement them one at a time, under the active item's `code_path`, gated on each task's `verify`. Invoked with the item, as `/my-interface-developer backend`. Owns development mode and enters it itself; no manual editing of `state.yaml` is needed first. Builds only; never plans.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Execute the plan

Development mode. Read `.interface/root.yaml` and follow its `read_order` before anything else, then `.interface/config/state.yaml` — its own `content.state_authority` is the State Authority over every state change below. The Config and the plan inside `task.yaml` are what you build from — `.interface/project.md` is not read here.

## Entering development mode

This Skill owns development mode and enters it itself — transition **S2**. The human's invocation is the decision; you record it.

1. **Resolve the item.** It is the one named in the invocation — `/my-interface-developer backend` names `backend`. If the invocation names none and exactly one item is enabled, that is it. If it names none and more than one is enabled, stop and ask. Never guess an item.
2. **Check it is buildable.** The item must be indexed, enabled, and hold at least one task in `content.plans.<item>.phases`. A mode with nothing to build is not entered: if the plan is empty, stop and say so — planning belongs to `my-interface-tasker`.
3. **Write `active`.** Set `mode` to `development`, `item` to the resolved item, `mode_reason` to the invocation, `set_by` to `my-interface-developer, on the human's invocation`, and `set_at` to today. Write `state.yaml` before touching any code.
4. **Where the human set `active` by hand** and it disagrees with the invocation, stop and ask — transition S6 stands above you, and you never overwrite what the human wrote.

You may set the mode to `development` and to nothing else, and only on an invocation of this Skill.

Take a task from `content.plans.<active item>` in `task.yaml`. A task is ready when its `status` is `todo` and every id in its `depends_on` is `done` — `ready` is not a stored status. Never take a task from another item's plan.

## The loop

Run it once per task, one task at a time:

1. Set the task's `status` to `claimed` and write `task.yaml` immediately, before any other work — so no second agent takes the same task.
2. Write only files under the active item's `code_path`, and only the paths listed in that task's `touches`.
3. Run the task's `verify` from the item's `verify_cwd`. Its passing is the gate — the code being written is not.
4. On a pass, set `status: done` and append a dated entry to `log`. On a blocker, set `status: blocked`, name the blocker id, state what is missing in `state.yaml`, and stop.

Then take the next ready task and start the loop again.

## Ending the run

Record what the run concluded — transition **S4**: rewrite `content.active.mode_reason` to what was built and what stopped, and update `set_at`. Leave `mode` and `item` as they are.

## Rules while building

- In this mode `status`, `blocker`, and `log` are the only fields of a task you may change. Everything else is the plan, and changing it takes a reason written into that task's log plus the human's approval.
- Follow the project's own rules — `rules.yaml` is the authority, and a rule that is not in it is not a rule. The item file gives that item's conventions, `code_path`, and `verify_cwd`.
- Never invent your way past a missing contract or a missing decision. That is a blocker in `state.yaml`, not a guess in the code.
- `log` is append-only — a past entry is never rewritten.
- In `state.yaml` you may write `content.active` under transitions S2 and S4, blockers under S7, and open questions under S8. You never answer a question, and you never freeze a contract.

## Not this mode's work

Do not write, renumber, or re-scope tasks, and do not change `task_schema`, `task_states`, a plan's `phase_titles`, or its `phase_titles_lifecycle`. Planning belongs to the `my-interface-tasker` Skill. Do not enter or set another Skill's mode. If the plan is wrong, say so and stop.
