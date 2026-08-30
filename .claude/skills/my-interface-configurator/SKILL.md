---

name: my-interface-configurator

description: Generate or update `.interface/config/` from Phase 1 of `.interface/project.md` and the shapes defined in `.interface/schema/` — the agent-oriented representation of the project that the my-interface-planner and my-interface-developer work from. Use when the project definition changes, or when config files are missing, outdated, or inconsistent with Phase 1.

allowed-tools: Read, Write, Edit, Grep, Glob

---

# Generate Config Files

Read and understand `.interface/project.md` completely.

**Only consider Phase 1 of the project. Ignore Phase 2 and Phase 3 entirely. Do not use any information, concepts, parameters, requirements, or development context that belongs to Phase 2 or Phase 3.**

From Phase 1 of `project.md`, identify and understand the project's relevant concepts, parameters, requirements, structure, and context.

Then read the files inside `.interface/schema/` and understand the structure, format, fields, and organization defined by the Schema.

Use the following relationship:

`project.md (Phase 1 only)` → Project Concepts & Parameters

`schema/` → Config Structure & Format

`Project Understanding + Schema` → `config/`

Based on your understanding of the concepts and parameters defined in **Phase 1**, update the existing files inside `.interface/config/` or regenerate them when necessary.

The Config files must reflect the current understanding of **Phase 1** while strictly following the structure and format defined by the corresponding Schema files.

If the existing Config files are incomplete, outdated, or inconsistent with the current Phase 1 content of `project.md`, modify or regenerate them accordingly.

Do not simply copy the Schema into the Config files. Populate and adapt the Schema structure using the concepts and parameters you understand from Phase 1 of `project.md`.

Do not invent project concepts, parameters, requirements, or information that cannot be derived from Phase 1 of `project.md`.

Do not modify `.interface/project.md`.

Do not modify `.interface/schema/`.

Do not perform any planning, implementation, development, testing, refactoring, or other project work.

## What the Config is for

The generated Config is the agent-oriented representation of the project. It is what the `my-interface-planner` Skill plans from and what the `my-interface-developer` Skill builds from — neither of them reads `project.md`. Anything those two need in order to understand how the project is planned and developed has to be in `config/`, expressed in the shape the Schema defines.

## Rules

Rules provide additional constraints for specific agent responsibilities when generating Config files.

Rules do not replace the Schema and do not change the Schema structure.

Apply only the rules that are explicitly defined below.

#### Backend

* API routes do not need to be defined in detailed, route-by-route form inside `backend.yaml`.

## Before starting

Confirm both:

* You have read `.interface/project.md` in full and are using **Phase 1 only**. Phase 2 and Phase 3 contribute nothing — not a concept, not a parameter, not a requirement.

* You have read every file in `.interface/schema/`. `file.schema.yaml` gives the outer shape every interface file follows (meta, policy, read_order, content_map, content); each `<name>.schema.yaml` gives the shape of that file's `content`. `root.yaml` has no schema of its own — outer shape only. The item index is `definition.yaml` under `content.architecture.parts`.

## While working

* `.interface/project.md` and `.interface/schema/` are inputs. Do not modify either.

* `definition.yaml` and `rules.yaml` carry `agent_may_edit: false`. Regenerating them from `project.md` is the one time they are touched, and only inside this job.

* This job runs **outside the modes**, and does not enter one. Carry `content.active` in `state.yaml` through a regeneration exactly as you found it — the mode and item a Skill or the human set are runtime state, not something a regeneration decides. Write `active` only when `state.yaml` does not yet exist — transition **S0** — and then as `mode: "not set"`, `item: "none"`, `set_by: "my-interface-configurator, generating state.yaml"`, `set_at` today, and a `mode_reason` saying that the next Skill the human invokes will set the mode. Under S0 you also seed `content.state_authority` **verbatim** from the `default` in `.interface/schema/state.schema.yaml` — no `state.yaml` is ever created without it. A regeneration carries the live `content.state_authority` through untouched, exactly like `active`. Never write `set_by: "the human"` for a value the human did not type. Who may write `active`, and when, is fixed in the State contract — `config/state.yaml` under `content.state_authority`; for a file being created, the schema's default governs its own seeding.

* You may raise blockers and open questions — transitions **S7** and **S8** — and record the human's own answer to a question under `answered_so_far` — dated and in the human's terms. You never answer one yourself, and you never close one by supplying its answer.

* Do not invent. Anything Phase 1 leaves undefined is written as "to be defined" and raised as an open question in `state.yaml` — never filled with a plausible value.

* Write no tasks and no build stages. This job produces configuration, not a plan, and `policy.task_creation` in `task.yaml` forbids speculative tasks. Plans stay under `content.plans.<item>`, one per item, with `phases` empty. An item's `phase_titles` are derived from that item's configuration by `my-interface-planner`, not here — a regeneration carries an existing `phase_titles`, its `phase_titles_lifecycle`, and its `phase_titles_derived_from` through untouched, and writes an empty list with lifecycle `empty` only where the plan is new.

* Do not plan, implement, test, or refactor anything.

* Apply the applicable Rules when generating Config files.

## The task

Your task is only to:

1. Read and understand `project.md`.

2. **Limit your understanding strictly to Phase 1.**

3. Ignore Phase 2 and Phase 3.

4. Understand the structure and format defined by `schema/`.

5. Apply the applicable Rules defined in this Skill.

6. Update or regenerate `config/` based on the Phase 1 project understanding and the Schema.

7. Ensure the resulting Config files follow the Schema and represent the current Phase 1 project understanding.

8. Ensure the runtime state survived: `content.active` and `content.state_authority` in `state.yaml`, and every plan's `phase_titles` with its lifecycle, are as they were before the run unless the file was created by it — and where it was created, that `content.state_authority` equals the schema's default verbatim.

Once the Config files correctly represent Phase 1 according to the Schema and applicable Rules, stop. This task is complete.

Report which files changed, and which open questions in `state.yaml` are new or now closed.
