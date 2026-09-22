# Plan Skill Contract

## What it is

The Core Skill for planning.

Required. Stable key: `plan`. Skill name: `my-interface-plan`.

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

- Understanding starts at: `.interface/implementation/operations/plan/plan.md`
- Context: `.interface/implementation/operations/plan/plan.yaml`
