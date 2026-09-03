---
name: my-interface-reset
description: Reset the generated workflow to its pre-development or pre-planning stage without deleting project code or generated Understanding. Use only when the Developer explicitly chooses development or planning.
argument-hint: "[development|planning]"
disable-model-invocation: true
---

# Reset the project workflow

Rewind all generated Tasks either to the point before development or to the point before planning. Preserve project code, generated Understanding, item configuration, and contracts.

## Developer guidance

- Read `README.md` completely, then resolve the live Interface map and human project-definition file from `.interface/root.yaml`. Read the project definition completely for current project context, followed by the generated Definition, Task file and Schema, and State contract.
- Re-read every required file on each invocation. Do not rely on remembered state or paths.
- Do not interpret or edit the human project definition, item configuration, or target-project code. The project definition provides context but does not alter Reset's mutation scope.
- Perform only this reset role. Do not interpret, plan, develop, review, clear, or invoke another Skill.

## Resolve the invocation

Require exactly one argument: `development` or `planning`. Do not accept a phase id. Refuse missing, additional, ambiguous, or unknown arguments instead of guessing.

Read the live reset transition before changing anything. Validate the complete project-wide mutation first and stop without partial writes if the current State or Task contract does not authorize it. Refuse while any Task is `claimed`; Reset never races active development.

## Reset to development

Require at least one generated Task across the plans. Preserve every Plan, Group, Task definition, dependency, acceptance criterion, verification command, and prior log. Set every Task status—including `done`, `blocked`, `cancelled`, and `superseded`—to the initial status `todo`, remove every Task `blocker` field, and append one dated log entry recording the human-invoked development reset.

Set `content.active.mode` to `planning` and `content.active.phase` to `none`. Record the reset provenance and current date in the remaining active fields. Do not invoke the Tasker or enter a particular phase on its behalf. The existing implementation remains available for later Developer runs to inspect, change where required, and verify again.

## Reset to planning

Require at least one generated Task across the plans. For every phase Plan, replace `groups` with an empty mapping. Preserve each Plan's phase id, title, order, target, and goal-derived `does` value so every entry remains the valid empty shell initially generated for `my-interface-tasker`.

Set `content.active.mode` to `not set` and `content.active.phase` to `none`. Record the reset provenance and current date in the remaining active fields. This is the workflow state before any Plan has been generated.

## Reset State

Preserve State blockers and open questions; Reset never answers, releases, or discards them. Neither reset changes product code, generated Definition, item configuration, contracts, or the phase shells in Task.

## Completion

Validate Task and State against their current Schemas, then report the reset stage, the number of affected Tasks and Plans, what was preserved, and the next explicit Skill invocation now available. Do not run that Skill automatically.
