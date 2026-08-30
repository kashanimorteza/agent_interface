---
name: my-interface-reviewer
description: Review mode — re-run what the plan claims is done, check the result against the contracts, `touches`, and `rules.yaml`, and report to the human. Invoked as `/my-interface-reviewer` or with an item. Owns review mode and enters it itself; no manual editing of `state.yaml` is needed first. Reports only; repairs nothing.
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Review the result

Review mode. Read `.interface/root.yaml` and follow its `read_order` before anything else — `content.state_authority` is the authority over every state change below. The Config and the plan inside `task.yaml` are what the result is judged against — `.interface/project.md` is not read here.

## Entering review mode

This Skill owns review mode and enters it itself — transition **S3**. The human's invocation is the decision; you record it.

1. **Resolve the item.** The one named in the invocation; failing that, the one already in `content.active.item`; failing that, the single enabled item. Where more than one is enabled and none is named or active, stop and ask.
2. **Write `active`.** Set `mode` to `review`, `item` to the resolved item, `mode_reason` to the invocation, `set_by` to `my-interface-reviewer, on the human's invocation`, and `set_at` to today.
3. **Where the human set `active` by hand** and it disagrees with the invocation, stop and ask — you never overwrite what the human wrote.

You may set the mode to `review` and to nothing else, and only on an invocation of this Skill.

Nothing is repaired in this mode. You may write exactly two things:

- `state.yaml` — `content.active` under transitions S3 and S4, and blockers and open questions under S7 and S8. Never an answer to a question
- `task.yaml` — the `status`, `blocker`, and `log` fields of a task, only to mark it blocked and record what was found

`Edit` exists for exactly those two files and for nothing else. Everything else is read-only, code under an item's `code_path` included.

## What to check

- Does each `done` task's `verify` still pass when re-run from the item's `verify_cwd`? A task marked done whose verify fails goes back to `blocked`, with what you found in its log.
- Does the code touch only the paths its task listed in `touches`?
- Does the built surface still match the contract version the task named in `needs_contract`?
- Does anything violate `rules.yaml`? Security overrides everything — report a security finding first.
- Do the state checks in `root.yaml` under `content.state_authority.validation` all hold? A state change that matches no transition, an `active.set_by` naming a Skill that may not write that field, or a `phase_titles` altered after the human confirmed it is a finding — reported, never repaired.

## Reporting

- Quote the file and section a finding came from. A claim with no source is not a finding.
- Never state a rule that is not in `rules.yaml`. If you think one is missing, say so as an observation, not as a rule.
- A gap that Phase 1 leaves undefined is an open question in `state.yaml`, never a guess at its answer.

## Not this mode's work

Do not fix what you found — not the code, not the plan, not a contract, not a state field another Skill wrote wrongly. Writing tasks belongs to the `my-interface-planner` Skill and implementing them to the `my-interface-developer` Skill. Do not enter or set another Skill's mode. Report to the human and stop.

## Ending the run

Record what the run concluded — transition **S4**: rewrite `content.active.mode_reason` to what was reviewed and what was found, and update `set_at`. Leave `mode` and `item` as they are.
