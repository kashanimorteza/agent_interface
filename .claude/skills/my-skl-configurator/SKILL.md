---

name: my-skl-configurator

description: Generate or update `.agent/config/` from Phase 1 of `.agent/project.md` and the shapes defined in `.agent/schema/` — the agent-oriented representation of the project that the my-skl-planner and my-skl-developer work from. Use when the project definition changes, when config files are missing, outdated, or inconsistent with Phase 1, or when `/my-cmd-configure` is run.

allowed-tools: Read, Write, Edit, Grep, Glob

---

# Generate Config Files

Read and understand `.agent/project.md` completely.

**Only consider Phase 1 of the project. Ignore Phase 2 and Phase 3 entirely. Do not use any information, concepts, parameters, requirements, or development context that belongs to Phase 2 or Phase 3.**

From Phase 1 of `project.md`, identify and understand the project's relevant concepts, parameters, requirements, structure, and context.

Then read the files inside `.agent/schema/` and understand the structure, format, fields, and organization defined by the Schema.

Use the following relationship:

`project.md (Phase 1 only)` → Project Concepts & Parameters

`schema/` → Config Structure & Format

`Project Understanding + Schema` → `config/`

Based on your understanding of the concepts and parameters defined in **Phase 1**, update the existing files inside `.agent/config/` or regenerate them when necessary.

The Config files must reflect the current understanding of **Phase 1** while strictly following the structure and format defined by the corresponding Schema files.

If the existing Config files are incomplete, outdated, or inconsistent with the current Phase 1 content of `project.md`, modify or regenerate them accordingly.

Do not simply copy the Schema into the Config files. Populate and adapt the Schema structure using the concepts and parameters you understand from Phase 1 of `project.md`.

Do not invent project concepts, parameters, requirements, or information that cannot be derived from Phase 1 of `project.md`.

Do not modify `.agent/project.md`.

Do not modify `.agent/schema/`.

Do not perform any planning, implementation, development, testing, refactoring, or other project work.

## What the Config is for

The generated Config is the agent-oriented representation of the project. It is what the `my_skl_planner` Skill plans from and what the `my_skl_developer` Skill builds from — neither of them reads `project.md`. Anything those two need in order to understand how the project is planned and developed has to be in `config/`, expressed in the shape the Schema defines.

## Rules

Rules provide additional constraints for specific agent responsibilities when generating Config files.

Rules do not replace the Schema and do not change the Schema structure.

Apply only the rules that are explicitly defined below.

#### Backend

* API routes do not need to be defined in detailed, route-by-route form inside `backend.yaml`.

## Before starting

Confirm both:

* You have read `.agent/project.md` in full and are using **Phase 1 only**. Phase 2 and Phase 3 contribute nothing — not a concept, not a parameter, not a requirement.

* You have read every file in `.agent/schema/`. `file.schema.yaml` gives the outer shape every interface file follows (meta, policy, read_order, content_map, content); each `<name>.schema.yaml` gives the shape of that file's `content`. `root.yaml` has no schema of its own — outer shape only, and its `content.structure` is the item index.

## While working

* `.agent/project.md` and `.agent/schema/` are inputs. Do not modify either.

* `definition.yaml` and `rules.yaml` carry `agent_may_edit: false`. Regenerating them from `project.md` is the one time they are touched, and only inside this job.

* Do not invent. Anything Phase 1 leaves undefined is written as "to be defined" and raised as an open question in `state.yaml` — never filled with a plausible value.

* Write no tasks. This job produces configuration, not a plan, and `policy.task_creation` in `task.yaml` forbids speculative tasks. Plans stay under `content.plans.<item>`, one per item, and stay empty.

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

Once the Config files correctly represent Phase 1 according to the Schema and applicable Rules, stop. This task is complete.

Report which files changed, and which open questions in `state.yaml` are new or now closed.
