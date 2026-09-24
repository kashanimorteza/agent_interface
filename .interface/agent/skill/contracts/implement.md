# Implement Skill Contract

## What it is

The Core Skill for implementing.

Required. Stable key: `implement`. Skill name: `my-interface-implement`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Execution Log

At the start of every execution, create one Log Entry in State for that execution, including its ID, Skill, and `started_at`. At completion, update that same Log Entry with `completed_at`, `duration`, outcome, report, and any applicable data, Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason. When this Skill coordinates another Core Skill, it supplies its own Log Entry ID as that Skill's `parent_id`; its own execution data includes the unique counts of associated Open Questions and Blockers.

## Outputs

The Skill execution result and status, including the aggregate counts of associated Open Questions and Blockers.

## Source

- `.interface/implementation/operations/implement/implement.md`
- `.interface/implementation/operations/implement/implement.yaml`
