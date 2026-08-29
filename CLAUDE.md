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
  skills/         the four Agent Skills — one per stage of the workflow — and clear, outside it
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
| `clear` | Removes the generated files under `config/` so the configurator can run again from nothing |

## Modes

Exactly one mode is active at a time, named in `config/state.yaml` under `active.mode`. The human sets it — an agent never changes it. What each mode may write is defined in `root.yaml` under `content.modes`; read it there, not here.

`planning` · `development` · `review`

## Who may write what

Three tiers, and one job outside them. Every file states its own in `policy` — read it there before editing.

**Never written by an agent.** `.interface/project.md` and `.interface/schema/` are inputs. The interface is generated from them, never the reverse.

**Written by the configurator only.** `config/definition.yaml` and `config/rules.yaml` carry `agent_may_edit: false` and `regenerated_by: my-interface-configurator`. They are rewritten when the configurator re-runs against a changed `project.md`, and never as a side effect of planning, development, or review. In those three modes a needed change is an open question in `state.yaml`.

**Written by the working modes.** `config/backend.yaml`, `config/frontend.yaml`, `config/task.yaml` and `config/state.yaml` carry `agent_may_edit: true`, each scoped by its own `policy.rule` and by the active mode. Two limits hold across all of them: `state.yaml`'s `active` is set by the human alone, and a contract is frozen by the human alone.

**Cleared, not written.** The `clear` Skill deletes every file under `config/` — the two the configurator owns included, and `state.yaml`'s `active` with them — and only when the human asks for that job by name. It writes nothing, and never touches `project.md`, `schema/`, `root.yaml`, or an item's `code_path`.

## Scope

Phase 1 of `project.md` only. Later phases contribute nothing — not a concept, not a parameter, not a requirement.

## Two habits that fail here

- **Never invent.** Anything Phase 1 does not state is written as `to be defined` and raised as an open question in `state.yaml` — never a plausible value in a contract or a task.
- **Never write a task speculatively.** A plan stays empty until the human asks for tasks, and a task is only ever written against a frozen contract.
