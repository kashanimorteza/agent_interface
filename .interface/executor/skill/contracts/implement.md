# Implement Skill Contract

## What it is

The Core Skill for implementing.

Required. Stable key: `implement`. Skill name: `my-interface-implement`.

## Inputs

An invocation request and an optional phase selection.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Execution Log

When this Skill coordinates another Core Skill, it supplies its own Log Entry ID as that Skill's `parent_id`; its own execution data includes the unique counts of associated Open Questions and Blockers.

## Outputs

The Skill execution result and status, including the aggregate counts of associated Open Questions and Blockers.

## Source

- `.interface/implementation/operations/implement/implement.md`
- `.interface/implementation/operations/implement/implement.yaml`
