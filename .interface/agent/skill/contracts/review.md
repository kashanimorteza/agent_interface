# Review Skill Contract

## What it is

The Core Skill for reviewing.

Required. Stable key: `review`. Skill name: `my-interface-review`.

## Inputs

An invocation request and an optional phase selection.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs.

Each selected phase must have a current Plan and a Development result.

## Outputs

The Skill execution result and status.

## Source

- `.interface/implementation/operations/review/review.md`
- `.interface/implementation/operations/review/review.yaml`
