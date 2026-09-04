# State Principles

This document is the personality of the State contract — `config/state.yaml`, the one file that defines the working modes, records where the project stands, and controls who is allowed to move it. It is written for every Agent operation that touches State and for the Developer who wants to know why State is guarded the way it is.

The shape of `state.yaml`, and the default modes and State Authority seeded into every newly created copy of it, live in the Schema. There is no Preferences file for State: State has no technical choices, only workflow authority.

Every statement here is mandatory.

<br>

## 1. State owns workflow modes and runtime state

State contains the fixed working-mode definitions, the project-wide runtime state, the State Authority that governs it, and the transition rules — in one file. It contains no project definition or task status. A task's status travels with the task, in `task.yaml`.

<br>

## 2. The live file is the authority, not the schema

`state.yaml` is the source of truth for the State. Its own `content.state_authority` section is the live authority: the working modes, every field, its owner, the allowed transitions, and which authorized operation may perform each.

The Schema defines only the shape of that section and the default that is seeded into every newly created `state.yaml`. Once the file exists, the live copy governs and the Schema default is not consulted at runtime. `map.yaml` locates the State files and does not define or own their modes or authority.

<br>

## 3. The default is always seeded, verbatim, and authorizes its own seeding

A Schema section carrying a `default` is always written into `state.yaml` when the file is created — the default is the seed, written verbatim under transition S0. This includes the working modes and their permissions. No newly generated `state.yaml` exists without it; there is no exception.

While no `state.yaml` exists there is no live authority, so the default State Authority in the schema is what authorizes its own seeding: transition S0 is defined inside it.
