# Task Principles

This document is the personality of the task layer — `config/task.yaml`, the file that defines what a task is and holds the plans that contain tasks. It is written for the planning, development, and review operations and for the Developer who wants to know what a plan may and may not be.

The shape of `task.yaml` — the frame that defines a task and the plans that hold the tasks — lives in the schema (`.interface/schema/task.yaml`). There is no preferences file for tasks: the task layer has no technical choices.

Every statement here is mandatory.

<br>

## 1. The frame is the human's; the plans are the surface

`task_schema` and `task_states` are the frame — fixed by the human. Plans are the surface, and they use the phase → group → task structure.

<br>

## 2. Every plan comes from a project phase

Every plan key and target come from a project phase in `definition.yaml`. The target resolves the item configuration and the code boundary used by its tasks, while `development.yaml` describes the selected components, their connections, runtime, and deployment. A plan never invents a phase or a target.

<br>

## 3. The schema gives shape, not permission

Who may write each part of `task.yaml`, and when, is decided in the State contract under `content.state_authority`, including its working modes and transitions. The Task Schema gives the shape and the invariants, never the permission.

<br>

## 4. Generation creates the frame, never the plan

The generation operation materializes the current `task_schema` and `task_states` frame and creates one Plan shell for every project phase indexed by `definition.yaml`. Each shell copies the phase's id, title, order, and target, derives `does` only from that phase's goal, and begins with an empty `groups` mapping.

Generation never decomposes a phase, creates a Group, or creates a Task. Those are planning decisions and belong only to the planning operation for the phase the human requested.

On regeneration, an existing non-empty Plan for an unchanged phase is preserved. A newly added phase receives an empty Plan shell, and a changed phase whose Plan remains empty may be reconciled to its current Definition. Removing a phase, or changing the identity, order, target, or intended outcome of a phase whose Plan already contains Tasks, is a critical conflict: generation reports it and never silently rewrites or deletes the affected planning content.
