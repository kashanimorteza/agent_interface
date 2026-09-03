---
name: my-interface-reset
description: Reset one generated project phase to planning or development readiness without deleting project code or generated Understanding. Use only when the Developer explicitly names the phase and destination stage.
argument-hint: "[phase-id] [planning|development]"
disable-model-invocation: true
---

# Reset one project phase

Rewind the workflow state of exactly one project phase so its plan can be generated again or its existing tasks can be developed again. Preserve project code, generated Understanding, contracts, and every other phase.

## Developer guidance

- Read `README.md` completely, then resolve the live Interface map, generated Definition, Task file and Schema, and State contract from `.interface/root.yaml`.
- Re-read every required file on each invocation. Do not rely on remembered state or paths.
- Do not read or edit the human project definition, item configuration, target-project code, or another phase's active plan.
- Perform only this reset role. Do not interpret, plan, develop, review, clear, or invoke another Skill.

## Resolve the invocation

Require exactly one phase id followed by exactly one destination stage: `planning` or `development`. The phase must exist in `definition.yaml` and have a matching entry in `task.yaml`. Refuse missing, additional, ambiguous, or unknown arguments instead of guessing.

Read the live reset transition before changing anything. Validate the entire selected mutation first and stop without partial writes if the current State or Task contract does not authorize it. A phase containing a `claimed` or `blocked` task is not reset; report that live work or blocker first.

## Reset to development

Require a non-empty active plan whose phase is complete under the live Task rules. Preserve the plan's identity, groups, task definitions, dependencies, acceptance criteria, verification commands, and prior logs. For every task whose status is `done`, set the status to `todo`, keep `cancelled` and `superseded` unchanged, ensure no blocker field is present, and append one dated log entry recording the human-invoked reset to development.

Do not alter product code. The existing implementation remains available for the next `my-interface-developer` run to inspect, change where required, and verify again.

## Reset to planning

Require a non-empty active plan. Copy the complete current phase plan, including every task and log, into the next immutable history entry for that phase under `content.plan_history`. History keys are `R1`, `R2`, and so on within each phase; choose one greater than the greatest existing numeric suffix, starting with `R1`. Then replace only the active plan's `groups` with an empty mapping. Preserve its phase id, title, order, target, and goal-derived `does` value so the active entry remains a valid generated phase shell for `my-interface-tasker`.

Do not alter product code. Do not rewrite or remove an earlier history entry.

## Reset State

After the Task mutation succeeds, set `content.active.mode` to `not set`, `content.active.phase` to `none`, and record the selected phase, destination stage, invocation provenance, and current date in the remaining active fields exactly as the live reset transition requires. Do not enter planning or development on behalf of another Skill.

Preserve blockers and open questions; Reset never answers, releases, or discards them. Preserve all generated item configuration and every phase other than the one explicitly selected.

## Completion

Validate Task and State against their current Schemas, then report the phase reset, its destination stage, what was preserved, and the next explicit Skill invocation now available. Do not run that Skill automatically.
