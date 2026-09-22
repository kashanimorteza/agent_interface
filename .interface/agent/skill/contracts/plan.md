# Plan Skill Contract

## What it is

The Agent Skill bridge to the Plan Operation Component.

This is a required primary Operation Skill with the stable key `plan`.

## What it does

Exposes the Plan Operation as an Agent Skill through its declared bridge.

## Inputs

An invocation request and an optional phase selection.

## Outputs

The Skill execution result and status.

## Responsibility

Activate explicitly for zero or more phase selections, or when `skills.implement` invokes the Skill, and delegate execution to the Plan Operation.

## Boundaries

- Direct invocation is enabled.
- Invocation by the declared coordinator is enabled only for `skills.implement`.
- Autonomous invocation is disabled.
- The skill is required and follows the Plan Component authority.
- It does not redefine the Plan Operation's behavior, records, or workflow.

## Source

- Skill name: `my-interface-plan`
- Meaning and Understanding: `.interface/implementation/operations/plan/plan.md`
- Current declarations: `.interface/implementation/operations/plan/plan.yaml`
