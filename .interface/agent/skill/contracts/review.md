# Review Skill Contract

## What it is

The Agent Skill bridge to the Review Operation Component.

This is a required primary Operation Skill with the stable key `review`.

## What it does

Exposes the Review Operation as an Agent Skill through its declared bridge.

## Inputs

An invocation request and an optional phase selection.

## Outputs

The Skill execution result and status.

## Responsibility

Activate explicitly for zero or more phase selections, or when `skills.implement` invokes the Skill, and delegate execution to the Review Operation.

## Boundaries

- Direct invocation is enabled.
- Invocation by the declared coordinator is enabled only for `skills.implement`.
- Autonomous invocation is disabled.
- The skill is required and follows the Review Component authority.
- It does not redefine the Review Operation's behavior, records, or workflow.

## Source

- Skill name: `my-interface-review`
- Meaning and Understanding: `.interface/implementation/operations/review/review.md`
- Current declarations: `.interface/implementation/operations/review/review.yaml`
