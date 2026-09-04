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
