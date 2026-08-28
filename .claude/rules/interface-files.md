---
paths:
  - ".agent/config/**"
  - ".agent/schema/**"
---

# Working inside the interface

These files are the standard itself, not code. They are read in the order `root.yaml` sets, and each one carries its own write rules in its `policy` section — read that section before editing the file it belongs to.

## Before editing

- Check `policy.agent_may_edit` on the file. `false` means the human owns it (`definition.yaml`, `rules.yaml`); raise an open question in `state.yaml` instead of editing.
- Check `content.active.mode` in `state.yaml`. What may be written where is decided per mode, in `root.yaml` under `content.modes`. Never change the mode yourself.
- `.agent/schema/` and `.agent/project.md` are inputs to the pipeline. They are not edited to make a config file fit.

## Shape

Every file under `config/` follows `schema/file.schema.yaml` — `meta`, `policy`, `read_order`, `content_map`, `content`, in that order. The shape of its `content` comes from that file's own `<name>.schema.yaml`. `root.yaml` has no schema of its own: outer shape only, and its `content.structure` is the item index.

If a change would need a new section or a new field, the shape is what is wrong. That is an open question in `state.yaml`, not a quiet addition.

## Two failures to avoid

- **Inventing.** Anything Phase 1 of `project.md` does not state is written as `to be defined` and raised as an open question. A plausible value in a contract is worse than an admitted gap.
- **Speculative tasks.** Plans live under `content.plans.<item>` in `task.yaml` and stay empty until the human asks for tasks. A task may only name a contract that is frozen.
