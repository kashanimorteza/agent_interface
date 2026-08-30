# agent_interface

This repository is not an application. It carries the **Agent Project Interface** — a standard for how a Developer and an AI Agent communicate about a build. The standard lives in `.interface/`, and `.interface/` is the authority. This file only points at it.

## Entry point

Read `.interface/root.yaml` first. It is the map — the folders and files of the Interface, the Agent Skills, the working modes, and the state authority. Nothing else is a valid starting point: not this file, not `README.md`, not a path named in chat.

Then read what the job needs. `config/rules.yaml` is read in full before any work — a rule that is not in that file is not a rule.

## Layout

```
.interface/
  root.yaml       entry point — the map of the Interface, and the state authority (human-owned)
  project.md      the project definition in natural language — the source
  schema/         the structure and format of every config file
  config/         the project's configuration, generated from project.md against schema/

.claude/
  skills/         the four Agent Skills — one per stage of the workflow — and my-interface-clear, outside it
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

| Skill | Does | Mode it owns |
|---|---|---|
| `my-interface-configurator` | Understands `project.md` and generates the configuration according to the Schemas | none — runs outside the modes |
| `my-interface-planner` | Generates Tasks and plans from the project configuration | `planning` |
| `my-interface-developer` | Executes planned Tasks and implements the required changes | `development` |
| `my-interface-reviewer` | Reviews the implementation against the Tasks and project specifications | `review` |
| `my-interface-clear` | Removes the generated files under `config/` so the configurator can run again from nothing | none — resets the state |

## Modes

Exactly one mode is active at a time, named in `config/state.yaml` under `active.mode`.

**A mode is entered by invoking the Skill that owns it.** The human decides — the invocation *is* the decision — and the Skill records that decision into `state.yaml` as part of its own workflow. `/my-interface-planner backend` names the mode (planning, because that is the Skill invoked) and the item (backend, because the invocation says so); the planner writes both. Nothing has to be hand-edited into `state.yaml` first.

A Skill may write only the mode it owns, only on an invocation of itself, and only an item the configuration indexes. It may not set a mode it was not invoked into, and it may not choose an item — where the invocation leaves the item ambiguous, the Skill stops and asks.

`planning` · `development` · `review`

What each mode may write is in `root.yaml` under `content.modes`. Who may write each field of the state, and on which transition, is in `root.yaml` under `content.state_authority`. Read them there, not here.

## The state authority

`root.yaml → content.state_authority` is the **single source of truth** for the runtime state: every field of `state.yaml`, its owner, the transitions S0–S8, which Skill may perform each, and the validation checks that must always hold. Where a schema, a config `policy`, a `SKILL.md`, or this file appears to say something different, that section governs — the other file is wrong and is corrected, never worked around.

Three tiers:

- **Agent-writable on an authorized transition** — `active.mode`, `active.item`, `active.mode_reason`, `active.set_by`, `active.set_at`; blockers; raising open questions; recording the human's own answer under `answered_so_far`.
- **Human-only** — the *answer* to an open question; freezing or versioning a contract; the content of `definition.yaml` and `rules.yaml` outside a configurator run; `project.md` and `schema/`; a `phase_titles` the human has confirmed; asking for tasks, and asking for a clear.
- **Derived** — `ready` is computed, never stored.

The rule underneath all of it: **an agent records a decision the human has already made, and never makes one.**

## Who may write what

Three tiers, and one job outside them. Every file states its own in `policy` — read it there before editing.

**Never written by an agent.** `.interface/project.md` and `.interface/schema/` are inputs. The interface is generated from them, never the reverse.

**Written by the configurator only.** `config/definition.yaml` and `config/rules.yaml` carry `agent_may_edit: false` and `regenerated_by: my-interface-configurator`. They are rewritten when the configurator re-runs against a changed `project.md`, and never as a side effect of planning, development, or review. In those three modes a needed change is an open question in `state.yaml`. A regeneration carries the runtime state — `active`, and every plan's `phase_titles` — through untouched; it writes `active` only when `state.yaml` does not yet exist (transition S0).

**Written by the working modes.** `config/backend.yaml`, `config/frontend.yaml`, `config/task.yaml` and `config/state.yaml` carry `agent_may_edit: true`, each scoped by its own `policy.rule`, by the active mode, and — for `state.yaml` — by the state authority. Two limits hold across all of them: a contract is frozen by the human alone, and a confirmed `phase_titles` is changed by the human alone.

**Cleared, not written.** The `my-interface-clear` Skill deletes every file under `config/` — the two the configurator owns included — and only when the human asks for that job by name and confirms the list. It writes nothing, and never touches `project.md`, `schema/`, `root.yaml`, or an item's `code_path`.

## Build stages

An item's `phase_titles` in `task.yaml` are **derived, not authored**. `my-interface-planner` derives them from that item's own configuration — its `code_layout`, the contract it produces or consumes, and the goals in `definition.yaml` — where every title traces to something the configuration already carries. The lifecycle runs `empty → derived → confirmed`; once the human confirms, only the human changes them. An item whose configuration reads `to be defined` has nothing to derive from, and its stages stay empty behind the blocker that says so.

## Scope

Phase 1 of `project.md` only. Later phases contribute nothing — not a concept, not a parameter, not a requirement.

## Two habits that fail here

- **Never invent.** Anything Phase 1 does not state is written as `to be defined` and raised as an open question in `state.yaml` — never a plausible value in a contract or a task. Deriving a stage from the configuration is not inventing; writing one the configuration does not carry is.
- **Never write a task speculatively.** A plan stays empty until the human asks for tasks, and a task is only ever written against a frozen contract.
