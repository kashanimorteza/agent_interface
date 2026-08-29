# agent_interface

This repository is not an application. It carries an **Agent Project Interface** — the standard by which a programmer and an agent communicate about a build. The standard lives in `.interface/`, and `.interface/` is the authority. This file only points at it.

## Entry point

Read `.interface/config/root.yaml` first, then follow its `read_order` exactly — its own words are "Exactly this order — no less, no more". Do not start work from this file, from `README.md`, or from a file named in chat without having read that order.

## This file is not a rulebook

Every rule of this project lives in `.interface/config/rules.yaml`, which states that a rule not in that file is not a rule. Nothing here adds, softens, or restates one. If a rule seems missing or wrong, raise it as an open question in `.interface/config/state.yaml` — never edit `rules.yaml`.

## Never edited

| Path | Why |
|---|---|
| `.interface/project.md` | The source. Phase 1 of it is what the interface is generated from. |
| `.interface/schema/` | The shape of every interface file. An agent never changes the shape of a file. |
| `.interface/config/definition.yaml` | `agent_may_edit: false` — the human owns it. |
| `.interface/config/rules.yaml` | `agent_may_edit: false` — an agent never moves its own boundary. |

`.interface/config/state.yaml` is writable, but `content.active` inside it is not — the human sets the mode and the active item.

## Modes

Exactly one mode is active at a time, named in `.interface/config/state.yaml` under `content.active.mode`. What each mode may write is defined in `root.yaml` under `content.modes` — read it there, not here.

Each command is an entry point only. The standing definition of the job lives in the Skill it names, under `.claude/skills/`.

- `/my_cmd_plan` — planning — `my_skl_planner` Skill
- `/my_cmd_develop` — development — `my_skl_developer` Skill
- `/my_cmd_review` — review — `my_skl_reviewer` Skill
- `/my_cmd_configure` — regenerate `.interface/config/` from Phase 1 of `.interface/project.md` and `.interface/schema/` — `my_skl_configurator` Skill

## Layout

```
.interface/
  project.md      the source — Phase 1 only, never modified
  schema/         the shape of each interface file — never modified
  config/         the interface: root, definition, rules, backend, frontend, task, state
```

Everything outside `.interface/` — `README.md`, `design/`, `.vscode/` — is not part of the standard.

## Scope

Phase 1 only. Phase 2 and Phase 3 of `project.md` are ignored entirely — no concept, parameter, or requirement is taken from them.

## Two habits that fail here

- **Never invent.** Anything Phase 1 does not state becomes an open question in `state.yaml`, never a guess in a contract or a task.
- **Never write a task speculatively.** A plan stays empty until the human asks for tasks, and a task is only ever written against a frozen contract.
