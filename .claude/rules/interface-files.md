---
paths:
  - ".interface/config/**"
  - ".interface/schema/**"
---

# Working inside the interface

These files are the standard itself, not code. They are read in the order `root.yaml` sets, and each one carries its own write rules in its `policy` section — read that section before editing the file it belongs to.

## Before editing

- Check `policy.agent_may_edit` on the file. `false` (`definition.yaml`, `rules.yaml`) means no mode edits it — but read `policy.regenerated_by` with it: those two are rewritten by `my-interface-configurator` when it re-runs against a changed `project.md`. Outside that job, a needed change is an open question in `state.yaml`, never an edit.
- Check `content.active.mode` in `state.yaml`. What may be written where is decided per mode, in `root.yaml` under `content.modes`.
- Before writing anything into `state.yaml`, read its own `content.state_authority` first. The State Authority lives inside the State contract itself — seeded from the `default` in `schema/state.schema.yaml` when `state.yaml` is created, human-only after that seed, and the single source of truth for every field, its owner, the transitions that exist, and which Skill may perform each. A mode is entered by the Skill that owns it, on the human's invocation of that Skill — never on an agent's own initiative, and never a mode the Skill was not invoked into. Where any file appears to say otherwise, that section governs and the other file is wrong. `root.yaml` references the State contract and does not own it.
- `.interface/schema/` and `.interface/project.md` are inputs to the pipeline. They are not edited to make a config file fit.

## Shape

Every file under `config/` follows `schema/file.schema.yaml` — `meta`, `policy`, `read_order`, `content_map`, `content`, in that order. The shape of its `content` comes from that file's own `<name>.schema.yaml`. `root.yaml` has no schema of its own: outer shape only, and its `content.structure` is the item index.

If a change would need a new section or a new field, the shape is what is wrong. That is an open question in `state.yaml`, not a quiet addition.

## Two failures to avoid

- **Inventing.** Anything Phase 1 of `project.md` does not state is written as `to be defined` and raised as an open question. A plausible value in a contract is worse than an admitted gap.
- **Speculative tasks.** Plans live under `content.plans.<item>` in `task.yaml` and stay empty until the human asks for tasks. A task may only name a contract that is frozen.

An item's `phase_titles` are neither of these: they are derived by `my-interface-planner` from that item's own configuration, every title tracing to something the configuration already carries, and confirmed by the human. Deriving is not inventing; writing a stage the configuration does not carry is.
