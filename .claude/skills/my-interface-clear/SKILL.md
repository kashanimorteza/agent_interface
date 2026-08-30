---
name: my-interface-clear
description: Reset the Agent Interface to a clean state — remove the generated files under `.interface/config/` so `my-interface-configurator` can run again from nothing. Use when the human asks to clear, reset, or regenerate the interface from scratch. Clears generated files only; never `project.md`, `schema/`, `root.yaml`, the Skills, or any item's built code.
allowed-tools: Read, Grep, Glob, Bash
---

# Clear the generated interface

This job removes what the agents produced and leaves what the human wrote. After it, `.interface/` holds only its inputs — `project.md`, `schema/`, and `root.yaml` — and `my-interface-configurator` can generate `config/` again from nothing.

Deleting is not reversible outside git. Nothing is removed until the human confirms the list.

## What is cleared

Everything inside `.interface/config/` — the files the pipeline generates:

- `definition.yaml` and `rules.yaml` — the configurator's output
- `backend.yaml` and `frontend.yaml` — the item files, including every draft or frozen contract
- `task.yaml` — the frame and every plan the planner wrote
- `state.yaml` — the active mode and item, the blockers, and the open questions
- and with `task.yaml`, every derived `phase_titles` and its lifecycle — a confirmed stage list does not survive a clear, and the human confirms again after the next planning run

All of it or none of it. A half-cleared `config/` is worse than either — a `task.yaml` naming a blocker that no longer exists in `state.yaml` is a broken interface, not a clean one.

`state.yaml`'s `content.active` is written by the Skill the human invokes, under the transitions in `root.yaml` — `content.state_authority`. This job performs transition **S5**: it does not set `active`, it deletes the file that holds it, and only because the human asked for this job by name and confirmed the list. After it, the next Skill invoked sets the state again from its own invocation — the human never has to write it by hand.

## What is never touched

- `.interface/project.md` — the project definition, and the source the whole pipeline runs from
- `.interface/schema/` — the shapes `config/` is generated against
- `.interface/root.yaml` — the entry point and map of the standard; it is not generated, and without it no agent finds the interface at all
- `.claude/` — the Skills, agents, rules, output styles, and settings
- Any file under an item's `code_path` — `backend/`, `frontend/`, and whatever else the item files name. Built code is not generated state, and this job never deletes it.
- Anything outside `.interface/config/`, without exception

## The job

1. **List.** Read `.interface/config/` and name every file actually present. Assume nothing — a partly cleared project is a normal starting point.
2. **Check for unsaved work.** Run `git status --short .interface/config/`. Uncommitted content there is gone for good once deleted; report it and let the human decide whether to commit first.
3. **Confirm.** Show the human the exact list of files to be deleted and what will survive, then wait for an explicit yes. A yes given for an earlier run is not this run's yes.
4. **Delete.** Remove those files and nothing else. Leave the `.interface/config/` directory itself in place — it is the configurator's target.
5. **Verify.** Confirm `project.md`, `schema/`, and `root.yaml` are present and unchanged, and that nothing under any item's `code_path` was touched.

## Not this job's work

Do not regenerate anything — this Skill clears, and `my-interface-configurator` generates. Do not edit `project.md` or `schema/` to shape what the next generation produces. Do not delete built code, and do not do any mode's work while you are here.

## Report

Say which files were deleted, what remains under `.interface/`, and whether anything uncommitted was lost. Close by naming the next step — run `my-interface-configurator` to generate `config/` again.
