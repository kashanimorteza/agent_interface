---
description: Review mode — read the result and report; repair nothing
---

Review mode. Read `agent/config/root.yaml` and follow its `read_order` before anything else.

Nothing is repaired in this mode. You may write exactly two things:

- `state.yaml` — blockers and open questions only, never `active`
- `task.yaml` — the `status`, `blocker`, and `log` fields of a task, only to mark it blocked and record what was found

Everything else is read-only, code under an item's `code_path` included.

What to check:

- Does each `done` task's `verify` still pass when re-run from the item's `verify_cwd`? A task marked done whose verify fails goes back to `blocked`, with what you found in its log.
- Does the code touch only the paths its task listed in `touches`?
- Does the built surface still match the contract version the task named in `needs_contract`?
- Does anything violate `rules.yaml`? Security overrides everything — report a security finding first.

Report what you found to the human. Do not fix it.

$ARGUMENTS
