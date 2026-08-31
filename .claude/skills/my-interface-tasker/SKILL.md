---
name: my-interface-tasker
description: Planning mode — turn the generated configuration in `.interface/config/` into a structured task plan for one scope (backend, frontend, or any other item the configuration indexes), written into `task.yaml` in the shape the schema defines. Invoked with the scope, as `/my-interface-tasker backend`. Owns planning mode and enters it itself; no manual editing of `state.yaml` is needed first. Plans only; never implements, and never reads `project.md`.
allowed-tools: Read, Edit, Grep, Glob
---

# Plan the build

Planning mode. The pipeline is `.interface/config/` → this Skill → a structured task plan. Nothing enters from anywhere else.

Read `.interface/root.yaml` first and follow its `read_order`, then `.interface/config/state.yaml` — its own `content.state_authority` is the State Authority over every state change below; read it before writing anything into `state.yaml`. Where `state.yaml` does not exist yet, stop: the `my-interface-interpreter` Skill creates it, seeded with the default authority from `schema/state.schema.yaml`. Then read the configuration. `.interface/project.md` is **not read here** — the `my-interface-interpreter` Skill owns it, and `config/` is the understanding it produced. You form no understanding of the project of your own; where the configuration is silent, the project is silent.

## Entering planning mode

This Skill owns planning mode and enters it itself. The human's invocation *is* the decision — you record it, you do not make it.

1. **Resolve the scope.** The item is the one named in the invocation — `/my-interface-tasker backend` names `backend`. If the invocation names none and exactly one item is `enabled` in the configuration, that is the scope. If it names none and more than one is enabled, **stop and ask the human which item.** Never guess an item, and never carry one over from a previous run.
2. **Check it is plannable.** The item must be indexed under `content.architecture.parts` in `definition.yaml`, hold its own key under `content.plans` in `task.yaml`, and carry `enabled: true`. If not, stop and tell the human — do not adjust the state to fit.
3. **Write `active`** — transition **S1**. Set `content.active.mode` to `planning`, `content.active.item` to the resolved item, `mode_reason` to the invocation that put it there, `set_by` to `my-interface-tasker, on the human's invocation`, and `set_at` to today. Write `state.yaml` before planning anything.
4. **Where the human has already set `active` by hand**, transition S6 stands above you. S6 bites only when what the human wrote *disagrees* with the invocation — another mode, another item; then stop and ask, do not overwrite it, and do not quietly plan the other item. `mode: not set` with `item: none` disagrees with nothing and is the normal resting state: proceed.

You may set the mode to `planning` and to nothing else, and only on an invocation of this Skill. Setting a mode you were not invoked into, or setting one for another Skill to find, is outside this Skill's authority.

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

## The build stages — `phase_titles`

The stages are **derived from the item's own configuration**, by you, and then confirmed by the human. They are not hand-written into a generated file, and they are not invented.

Read `content.plans.<item>.phase_titles_lifecycle` first:

- **`empty`** — derive them. Every title must trace to something the configuration already carries: an entry of the item's `code_layout`, a model or an operation of the contract it produces or consumes, or a goal in `definition.yaml → content.goals`. Order them so a later stage assumes the earlier ones exist. Write `phase_titles`, set `phase_titles_derived_from` to the exact sections you read, and set the lifecycle to `derived`. Then **ask the human to confirm them** — say plainly that they are derived and that a title they disagree with is theirs to change.
- **`derived`** — they are yours to correct if the configuration has moved under them. Say what changed and why, and ask the human to confirm again.
- **`confirmed`** — the human has accepted them. You never change them; a stage you think is missing is an open question in `state.yaml`.

A title with no source in the configuration is an invention — do not write it. If the item's configuration reads `to be defined` where the stages would come from, there is nothing to derive: leave the list empty, name the blocker that stops it, and say so. The frontend is in exactly that position today (B1 / Q1).

A phase's `title` must match its entry in `phase_titles`.

## The shape of a plan

`task.schema.yaml`'s `plans` section is the authority. Three levels, and nothing sits outside them:

- **Phase** — `id` (P1, P2, … in build order), `title`, `does`, `groups`. A later phase assumes the earlier ones are done.
- **Group** — `id` (P1-G1, P1-G2, …), `title`, `does`, `task_count`, `tasks`. One area of work inside a phase.
- **Task** — exactly the fields of `task_schema`, no more and no fewer. A task never sits directly in a phase.

A phase holds groups and a group holds tasks, so no phase is written until tasks may be written. Deriving the stages and writing the plan are two steps, and the first does not force the second.

## Writing a task

- One concrete act per task — the file it creates or the piece it changes, finished in one sitting.
- `depends_on` names tasks of the same item only, and ordering follows it: nothing depends on a task later in the plan.
- `needs_contract` names the contract version the task builds against, and is **omitted when the task needs none**. A task that names a contract is written only against a **frozen** version — if the version it needs is still `draft`, that task is not written and the gap is a blocker in `state.yaml`. A task that needs no contract is not blocked by a draft one.
- `verify` is a runnable command that actually proves `acceptance`, run from the item's `verify_cwd`. What may serve as a verify is governed by `rules.yaml` — where the item's `needs_test` is false, a runtime check stands in for a written test.
- `touches` lists paths relative to the item's `code_path`, and stays inside the `code_layout` that item file defines.
- `status` starts at `todo`; `blocker` and `log` are absent until the task moves.
- No task is written speculatively — `policy.task_creation` in `task.yaml` holds a plan empty until the human asks for tasks. Write what was asked for, and no more.

## What this Skill writes

`root.yaml` under `content.modes.planning` grants planning mode more than this job uses — the item files among them. This Skill writes two files:

- `task.yaml` — the scope's `phase_titles`, `phase_titles_lifecycle` and `phase_titles_derived_from` while the lifecycle is `empty` or `derived`, and the `phases` of that scope's plan. Never `task_schema`, never `task_states`, and never a `phase_titles` the human has confirmed.
- `state.yaml` — `content.active` under transitions **S1** and **S4**, blockers under **S7**, and open questions under **S8**. An answer to a question is never written here; only the human's own answer, recorded as theirs.

The rest of the configuration is input. `definition.yaml`, `rules.yaml`, the item files, `root.yaml`, and `schema/` are read and left as they are — a change any of them needs is an open question in `state.yaml`, not an edit. The grant on the item files stays unused here: this Skill plans, and settling an item's settings or its draft contract is the interpreter's work.

## Ending the run

Record what the run concluded — transition **S4**: rewrite `content.active.mode_reason` to what was planned and what stopped, and update `set_at`. Leave `mode` and `item` as they are; the state reflects where the project stands, and the next invocation moves it.

## Not this mode's work

Do not implement, execute, test, or refactor anything, and do not run a task's `verify` to see whether it would pass — that is the `my-interface-developer` Skill's job. Do not write a file under any item's `code_path`. Do not redesign the architecture the configuration defines, and do not add a requirement it does not carry. Anything the configuration marks `to be defined` stays undefined: it is an open question in `state.yaml`, never a plausible value in a task.

## Report

Say which scope was planned and what state transition you performed, what stages were derived and from which sections of the configuration, what phases and groups were written and how many tasks each holds, and what was **not** planned and why — the blocker or open question that stopped it. Close by asking the human to confirm the derived stages, when the lifecycle is `derived`.
