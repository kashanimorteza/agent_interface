# Develop Skill Contract

## What it is

The Core Skill for developing.

Required. Stable key: `develop`. Skill name: `my-interface-develop`.

## Inputs

An invocation request and an optional phase selection.

## Outputs

The Skill execution result and status.

## Responsibility

Activate through direct invocation or `skills.implement`.

## Boundaries

- Direct invocation is enabled.
- Invocation by the declared coordinator is enabled only for `skills.implement`.
- Autonomous invocation is disabled.

## Source

- Understanding starts at: `.interface/implementation/operations/develop/develop.md`
- Context: `.interface/implementation/operations/develop/develop.yaml`
