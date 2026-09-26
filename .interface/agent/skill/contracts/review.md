# Review Skill Contract

## What it is

The Core Skill for reviewing.

Required. Stable key: `review`. Skill name: `my-interface-review`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs.

Each selected phase must have a current Plan and generated Source available for examination. Development need not have completed when Source is available.

## Execution Log

Create one Log Entry in State for every execution, including its ID and Skill. Update that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

## Outputs

The Skill execution result and status.

## Source

- `.interface/implementation/operations/review/review.md`
- `.interface/implementation/operations/review/review.yaml`
