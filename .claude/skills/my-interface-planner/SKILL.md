---
name: my-interface-planner
description: Planning mode — turn the generated configuration in `.interface/config/` into a structured task plan for one scope (backend, frontend, or any other item the configuration indexes), written into `task.yaml` in the shape the schema defines. Use when the human asks for a plan or for tasks. Plans only; never implements, and never reads `project.md`.
allowed-tools: Read, Edit, Grep, Glob
---

# Plan the build

Planning mode. The pipeline is `.interface/config/` → this Skill → a structured task plan. Nothing enters from anywhere else.

Read `.interface/root.yaml` first and follow its `read_order`. Then read the configuration. `.interface/project.md` is **not read here** — the `my-interface-configurator` Skill owns it, and `config/` is the understanding it produced. You form no understanding of the project of your own; where the configuration is silent, the project is silent.

Check `.interface/config/state.yaml`: `content.active.mode` must be `planning`, and `content.active.item` names the scope you are planning. If either disagrees with what you were asked to do, stop and tell the human — an agent never changes the active mode.

## What to read

All of it, in this order — the plan is derived from these files and from nothing else:

1. `definition.yaml` — the product, its goals, and the parts the architecture is divided into. `content.architecture.parts` is the list of scopes that can be planned.
2. `rules.yaml` — the boundaries every task inherits. A rule that is not in this file is not a rule.
3. The scope's item file — `backend.yaml` or `frontend.yaml`: `code_path`, `verify_cwd`, `needs_test`, `code_layout`, `contracts`, `boundaries`, `out_of_scope`.
4. `task.yaml` — `task_schema` and `task_states`, the frame the human fixed, and the plan you write into.
5. `state.yaml` — the blockers and open questions already raised. A task is never written over one.
6. `.interface/schema/task.schema.yaml` — the shape a plan takes, below.

## Scope

One scope per run — an item that `definition.yaml` names under `content.architecture.parts` and that holds its own key under `content.plans` in `task.yaml`. Backend and frontend are what this project indexes today; a scope the configuration does not index cannot be planned.

Each item's plan stands alone: its phases number from P1, its tasks number from T1, and a task never depends on a task under another item. Where an item needs something another item produces, that is a `needs_contract`, not a dependency.

## The shape of a plan

`task.schema.yaml`'s `plans` section is the authority. Three levels, and nothing sits outside them:

- **Phase** — `id` (P1, P2, … in build order), `title`, `does`, `groups`. A later phase assumes the earlier ones are done.
- **Group** — `id` (P1-G1, P1-G2, …), `title`, `does`, `task_count`, `tasks`. One area of work inside a phase.
- **Task** — exactly the fields of `task_schema`, no more and no fewer. A task never sits directly in a phase.

`phase_titles` is part of the frame, fixed by the human — you never write it, and a phase's `title` must match its entry there. If the scope's `phase_titles` is empty, the frame is not set: say so and ask the human for the build stages. Do not invent them, and do not write phases without them.

## Writing a task

- One concrete act per task — the file it creates or the piece it changes, finished in one sitting.
- `depends_on` names tasks of the same item only, and ordering follows it: nothing depends on a task later in the plan.
- `needs_contract` names the contract version the task builds against, and is **omitted when the task needs none**. A task that names a contract is written only against a **frozen** version — if the version it needs is still `draft`, that task is not written and the gap is a blocker in `state.yaml`. A task that needs no contract is not blocked by a draft one.
- `verify` is a runnable command that actually proves `acceptance`, run from the item's `verify_cwd`. What may serve as a verify is governed by `rules.yaml` — where the item's `needs_test` is false, a runtime check stands in for a written test.
- `touches` lists paths relative to the item's `code_path`, and stays inside the `code_layout` that item file defines.
- `status` starts at `todo`; `blocker` and `log` are absent until the task moves.
- No task is written speculatively — `policy.task_creation` in `task.yaml` holds a plan empty until the human asks for tasks. Write what was asked for, and no more.

## What this Skill writes

`root.yaml` under `content.modes.planning` grants planning mode more than this job uses. This Skill writes two things:

- `task.yaml` — the `phases` of the scope's plan. Never `task_schema`, `task_states`, or `phase_titles`.
- `state.yaml` — blockers and open questions. Never `active`.

The rest of the configuration is input. `definition.yaml`, `rules.yaml`, the item files, `root.yaml`, and `schema/` are read and left as they are — a change any of them needs is an open question in `state.yaml`, not an edit.

## Not this mode's work

Do not implement, execute, test, or refactor anything, and do not run a task's `verify` to see whether it would pass — that is the `my-interface-developer` Skill's job. Do not write a file under any item's `code_path`. Do not redesign the architecture the configuration defines, and do not add a requirement it does not carry. Anything the configuration marks `to be defined` stays undefined: it is an open question in `state.yaml`, never a plausible value in a task.

## Report

Say which scope was planned, what phases and groups were written and how many tasks each holds, and what was **not** planned and why — the blocker or open question that stopped it.
