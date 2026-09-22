# Review Skill Contract

## What it is

The Core Skill for reviewing.

Required. Stable key: `review`. Skill name: `my-interface-review`.

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

- Understanding starts at: `.interface/implementation/operations/review/review.md`
- Context: `.interface/implementation/operations/review/review.yaml`
