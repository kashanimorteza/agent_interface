---
name: my-interface-reset
description: Reset the generated workflow to its pre-development or pre-planning stage without deleting project code or generated Understanding. Use only when the Developer explicitly chooses development or planning.
argument-hint: "[development|planning]"
disable-model-invocation: true
---

# Reset the project workflow

Reset the generated workflow for the one stage named in `$ARGUMENTS`: `development` or `planning`.

## Bootstrap

Read `.interface/map.yaml`. This is the only Interface path this Skill may assume. Follow its current map to discover the workflow data, governing Schemas, State authority, reset transition, and reset protocol required for this run.

Re-read required sources on every invocation. Do not rely on remembered file shapes, fields, states, transitions, preservation rules, or destinations. Require exactly one supported stage and let the current reset contract decide whether the operation is allowed and what it changes.

## Reset

Validate the complete requested mutation before writing, then apply the current reset protocol atomically. Preserve or clear content exactly as the live authorities specify; do not duplicate those structural rules in this Skill.

Perform only the reset role. Do not interpret, plan, develop, review, clear project data, change product code, modify the human project definition, or invoke the next workflow operation.

Validate the resulting workflow files against their current Schemas. Report the selected stage, affected records, cleared workflow findings, preserved content, and the next available explicit action.
