# Develop Skill Contract

## What it is

The Agent Skill bridge to the Develop Operation Component.

This is a required primary Operation Skill with the stable key `develop`.

## What it does

Exposes the Develop Operation as an Agent Skill through its declared bridge.

## Inputs

An invocation request and an optional phase selection.

## Outputs

The Skill execution result and status.

## Responsibility

Activate explicitly for zero or more phase selections, or when `skills.implement` invokes the Skill, and delegate execution to the Develop Operation.

## Boundaries

- Direct invocation is enabled.
- Invocation by the declared coordinator is enabled only for `skills.implement`.
- Autonomous invocation is disabled.
- The skill is required and follows the Develop Component authority.
- It does not redefine the Develop Operation's behavior, records, or workflow.

## Source

- Skill name: `my-interface-develop`
- Meaning and Understanding: `.interface/implementation/operations/develop/develop.md`
- Current declarations: `.interface/implementation/operations/develop/develop.yaml`
