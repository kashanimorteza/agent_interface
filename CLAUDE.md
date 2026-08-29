# agent_interface

This repository is not an application. It carries the **Agent Project Interface** — a standard for how a Developer and an AI Agent communicate about a build. The standard lives in `.interface/`, and `.interface/` is the authority. This file only points at it.

## Entry point

Read `.interface/root.yaml` first. It is the map — the folders and files of the Interface, the Agent Skills, and the working modes. Nothing else is a valid starting point: not this file, not `README.md`, not a path named in chat.

Then read what the job needs. `config/rules.yaml` is read in full before any work — a rule that is not in that file is not a rule.

## Layout

```
.interface/
  root.yaml       entry point — the map of the Interface
  project.md      the project definition in natural language — the source
  schema/         the structure and format of every config file
  config/         the project's configuration, generated from project.md against schema/

.claude/
  skills/         the four Agent Skills — one per stage of the workflow
  agents/         interface-reader — read-only reporter of where the build stands
  rules/          what applies when editing the interface files
  output-styles/  every claim cites the file and section it came from
  settings.json   permissions over the interface files
```

`.interface/` is the standard. `.claude/` is how this repository runs it. `README.md` and `design/` are neither.

## The pipeline

`project.md` (natural language) → `schema/` (the shape) → `config/` (the agent's representation)

The Skills plan and build from `config/`. Only the configurator reads `project.md`.

## Agent Skills

Under `.claude/skills/`. The standing definition of each job is its `SKILL.md` — run the Skill, do not paraphrase it.

| Skill | Does |
|---|---|
| `my-interface-configurator` | Understands `project.md` and generates the configuration according to the Schemas |
| `my-interface-planner` | Generates Tasks and plans from the project configuration |
| `my-interface-developer` | Executes planned Tasks and implements the required changes |
| `my-interface-reviewer` | Reviews the implementation against the Tasks and project specifications |

## Modes

Exactly one mode is active at a time, named in `config/state.yaml` under `active.mode`. The human sets it — an agent never changes it. What each mode may write is defined in `root.yaml` under `content.modes`; read it there, not here.

`planning` · `development` · `review`

## Never edited

| Path | Why |
|---|---|
| `.interface/project.md` | The source. The interface is generated from it, never the reverse. |
| `.interface/schema/` | The shape of every config file. An agent never changes the shape of a file. |
| `.interface/config/definition.yaml` | `agent_may_edit: false` — the human owns it. |
| `.interface/config/rules.yaml` | `agent_may_edit: false` — an agent never moves its own boundary. |

`config/state.yaml` is writable, but `active` inside it is not.

## Scope

Phase 1 of `project.md` only. Later phases contribute nothing — not a concept, not a parameter, not a requirement.

## Two habits that fail here

- **Never invent.** Anything Phase 1 does not state is written as `to be defined` and raised as an open question in `state.yaml` — never a plausible value in a contract or a task.
- **Never write a task speculatively.** A plan stays empty until the human asks for tasks, and a task is only ever written against a frozen contract.
