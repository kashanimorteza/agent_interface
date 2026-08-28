---
description: Regenerate .agent/config/ from Phase 1 of .agent/project.md and .agent/schema/
---

Follow `.agent/configure.md` exactly. It is the standing definition of this job — this command adds nothing to it and overrides nothing in it.

Before starting, confirm both:

- You have read `.agent/project.md` in full and are using **Phase 1 only**. Phase 2 and Phase 3 contribute nothing — not a concept, not a parameter, not a requirement.
- You have read every file in `.agent/schema/`. `file.schema.yaml` gives the outer shape every interface file follows (meta, policy, read_order, content_map, content); each `<name>.schema.yaml` gives the shape of that file's `content`. `root.yaml` has no schema of its own — outer shape only, and its `content.structure` is the item index.

While working:

- `.agent/project.md` and `.agent/schema/` are inputs. Do not modify either.
- `definition.yaml` and `rules.yaml` carry `agent_may_edit: false`. Regenerating them from `project.md` is the one time they are touched, and only inside this job.
- Do not invent. Anything Phase 1 leaves undefined is written as "to be defined" and raised as an open question in `state.yaml` — never filled with a plausible value.
- Write no tasks. This job produces configuration, not a plan, and `policy.task_creation` in `task.yaml` forbids speculative tasks. Plans stay under `content.plans.<item>`, one per item, and stay empty.
- Do not plan, implement, test, or refactor anything.

Stop when `.agent/config/` correctly represents Phase 1 according to the schema. Report which files changed, and which open questions in `state.yaml` are new or now closed.
