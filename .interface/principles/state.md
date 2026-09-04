# State Principles

This document is the personality of the State contract — `config/state.yaml`, the one file that records where the project stands and who is allowed to move it. It is written for every Agent operation that touches State and for the Developer who wants to know why State is guarded the way it is.

The shape of `state.yaml`, and the default State Authority seeded into every newly created copy of it, live in the schema (`.interface/schema/state.yaml`). There is no preferences file for State: State has no technical choices, only authority.

Every statement here is mandatory.

<br>

## 1. State holds state, and nothing else

State is the project-wide state, the State Authority that governs it, and the transition rules — in one file. No project definition, no rule, and no task status lives there. A task's status travels with the task, in `task.yaml`.

<br>

## 2. The live file is the authority, not the schema

`state.yaml` is the source of truth for the State. Its own `content.state_authority` section is the live authority: every field, its owner, the allowed transitions, and which authorized operation may perform each.

The schema defines only the shape of that section and the default that is seeded into every newly created `state.yaml`. Once the file exists, the live copy governs and the schema default is not consulted at runtime. `map.yaml` references the State contract and does not own any of it.

<br>

## 3. The default is always seeded, verbatim, and authorizes its own seeding

A schema section carrying a `default` is always written into `state.yaml` when the file is created — the default is the seed, written verbatim under transition S0. No newly generated `state.yaml` exists without it; there is no exception.

While no `state.yaml` exists there is no live authority, so the default State Authority in the schema is what authorizes its own seeding: transition S0 is defined inside it.
