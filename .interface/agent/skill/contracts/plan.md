# Plan Skill Contract

## What it is

The Core Skill for planning.

Required. Stable key: `plan`. Skill name: `my-interface-plan`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs.

## Execution Log

At the start of every execution, create one Log Entry in State for that execution, including its ID, Skill, and `started_at`. At completion, update that same Log Entry with `completed_at`, `duration_ms`, readable `duration`, outcome, report, and any applicable data, Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Outputs

The Skill execution result and status.

## Source

- `.interface/implementation/operations/plan/plan.md`
- `.interface/implementation/operations/plan/plan.yaml`
