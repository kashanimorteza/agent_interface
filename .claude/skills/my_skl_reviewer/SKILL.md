---
name: my_skl_reviewer
description: Review mode — re-run what the plan claims is done, check the result against the contracts, `touches`, and `rules.yaml`, and report to the human. Use when the human asks whether the build is sound, or when `/my_cmd_review` is run. Reports only; repairs nothing.
allowed-tools: Read, Grep, Glob, Bash
---

# Review the result

Review mode. Read `.agent/config/root.yaml` and follow its `read_order` before anything else. The Config and the plan inside `task.yaml` are what the result is judged against — `.agent/project.md` is not read here.

Check `.agent/config/state.yaml`: `content.active.mode` must be `review`. If it says otherwise, stop and tell the human — an agent never changes the active mode.

Nothing is repaired in this mode. You may write exactly two things:

- `state.yaml` — blockers and open questions only, never `active`
- `task.yaml` — the `status`, `blocker`, and `log` fields of a task, only to mark it blocked and record what was found

Everything else is read-only, code under an item's `code_path` included.

## What to check

- Does each `done` task's `verify` still pass when re-run from the item's `verify_cwd`? A task marked done whose verify fails goes back to `blocked`, with what you found in its log.
- Does the code touch only the paths its task listed in `touches`?
- Does the built surface still match the contract version the task named in `needs_contract`?
- Does anything violate `rules.yaml`? Security overrides everything — report a security finding first.

## Reporting

- Quote the file and section a finding came from. A claim with no source is not a finding.
- Never state a rule that is not in `rules.yaml`. If you think one is missing, say so as an observation, not as a rule.
- A gap that Phase 1 leaves undefined is an open question in `state.yaml`, never a guess at its answer.

## Not this mode's work

Do not fix what you found — not the code, not the plan, not a contract. Writing tasks belongs to the `my_skl_planner` Skill and implementing them to the `my_skl_developer` Skill. Report to the human and stop.
