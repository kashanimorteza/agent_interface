# agent_interface

This repository is not an application. It carries an **Agent Project Interface** — the standard by which a programmer and an agent communicate about a build. The standard lives in `.agent/`, and `.agent/` is the authority. This file only points at it.

## Entry point

Read `.agent/config/root.yaml` first, then follow its `read_order` exactly — its own words are "Exactly this order — no less, no more". Do not start work from this file, from `README.md`, or from a file named in chat without having read that order.

## This file is not a rulebook

Every rule of this project lives in `.agent/config/rules.yaml`, which states that a rule not in that file is not a rule. Nothing here adds, softens, or restates one. If a rule seems missing or wrong, raise it as an open question in `.agent/config/state.yaml` — never edit `rules.yaml`.

## Never edited

| Path | Why |
|---|---|
| `.agent/project.md` | The source. Phase 1 of it is what the interface is generated from. |
| `.agent/schema/` | The shape of every interface file. An agent never changes the shape of a file. |
| `.agent/config/definition.yaml` | `agent_may_edit: false` — the human owns it. |
| `.agent/config/rules.yaml` | `agent_may_edit: false` — an agent never moves its own boundary. |

`.agent/config/state.yaml` is writable, but `content.active` inside it is not — the human sets the mode and the active item.

## Modes

Exactly one mode is active at a time, named in `.agent/config/state.yaml` under `content.active.mode`. What each mode may write is defined in `root.yaml` under `content.modes` — read it there, not here.

Each command is an entry point only. The standing definition of the job lives in the Skill it names, under `.claude/skills/`.

- `/plan` — planning — `my_planner` Skill
- `/develop` — development — `my_developer` Skill
- `/review` — review — `my_reviewer` Skill
- `/configure` — regenerate `.agent/config/` from Phase 1 of `.agent/project.md` and `.agent/schema/` — `my_configurator` Skill

## Layout

```
.agent/
  project.md      the source — Phase 1 only, never modified
  schema/         the shape of each interface file — never modified
  config/         the interface: root, definition, rules, backend, frontend, task, state
```

Everything outside `.agent/` — `README.md`, `design/`, `.vscode/` — is not part of the standard.

## Scope

Phase 1 only. Phase 2 and Phase 3 of `project.md` are ignored entirely — no concept, parameter, or requirement is taken from them.

## Two habits that fail here

- **Never invent.** Anything Phase 1 does not state becomes an open question in `state.yaml`, never a guess in a contract or a task.
- **Never write a task speculatively.** A plan stays empty until the human asks for tasks, and a task is only ever written against a frozen contract.
