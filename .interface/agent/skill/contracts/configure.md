# Configure Skill Contract

## What it is

The Agent Skill bridge to the Configure Operation Component.

This is a required primary Operation Skill with the stable key `configure`.

## What it does

Exposes the Configure Operation as an Agent Skill through its declared bridge.

## Inputs

An invocation request.

## Outputs

The Skill execution result and status.

## Responsibility

Activate through a direct invocation or `skills.implement` and delegate execution to the Configure Operation.

## Boundaries

- Direct invocation is enabled.
- Invocation by the declared coordinator is enabled only for `skills.implement`.
- Autonomous invocation is disabled.
- The skill is required and follows the Configure Component authority.
- It does not redefine the Configure Operation's behavior, records, or workflow.

## Source

- Skill name: `my-interface-configure`
- Meaning and Understanding: `.interface/implementation/operations/configure/configure.md`
- Current declarations: `.interface/implementation/operations/configure/configure.yaml`
