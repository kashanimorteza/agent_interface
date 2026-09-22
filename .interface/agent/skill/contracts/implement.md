# Implement Skill Contract

## What it is

The Agent Skill bridge to the Implement Operation Component.

This is the selected, required primary Operation Skill with the stable key `implement`.

## What it does

Exposes the Implement Operation as an Agent Skill through its declared bridge.

## Inputs

An explicit invocation request and an optional phase selection.

## Outputs

The Skill execution result and status.

## Responsibility

Activate only through explicit direct invocation for zero or more phase selections and delegate execution to the Implement Operation.

## Boundaries

- Direct invocation is enabled.
- Coordinator invocation is disabled.
- Autonomous invocation is disabled.
- The skill is required and follows the Implement Component authority.
- Child Operation Skills are invoked only through the Runtime's own Skill mechanism, and each owning Operation Component retains its records and outputs.
- It does not redefine the Implement Operation's behavior, records, or workflow.

## Source

- Skill name: `my-interface-implement`
- Meaning and Understanding: `.interface/implementation/operations/implement/implement.md`
- Current declarations: `.interface/implementation/operations/implement/implement.yaml`
