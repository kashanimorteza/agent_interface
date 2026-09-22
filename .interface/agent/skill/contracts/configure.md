# Configure Skill Contract

## What it is

The Core Skill for configuring.

Required. Stable key: `configure`. Skill name: `my-interface-configure`.

## Inputs

An invocation request.

## Outputs

The Skill execution result and status.

## Responsibility

Activate through direct invocation or `skills.implement`.

## Boundaries

- Direct invocation is enabled.
- Invocation by the declared coordinator is enabled only for `skills.implement`.
- Autonomous invocation is disabled.

## Source

- Understanding starts at: `.interface/implementation/operations/configure/configure.md`
- Context: `.interface/implementation/operations/configure/configure.yaml`
