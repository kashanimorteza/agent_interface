# Implement Skill Contract

## What it is

The Core Skill for implementing.

Required. Stable key: `implement`. Skill name: `my-interface-implement`.

## Inputs

An invocation request and an optional phase selection.

## Outputs

The Skill execution result and status.

## Responsibility

Activate only through direct invocation.

## Boundaries

- Direct invocation is enabled.
- Coordinator invocation is disabled.
- Autonomous invocation is disabled.
- It may invoke `skills.configure`, `skills.plan`, `skills.develop`, and `skills.review`.

## Source

- Understanding starts at: `.interface/implementation/operations/implement/implement.md`
- Context: `.interface/implementation/operations/implement/implement.yaml`
