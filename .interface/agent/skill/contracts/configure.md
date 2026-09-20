# configure Skill Contract

## Purpose

Realize the Configure Component defined in the Implementation Module.

## Responsibility

This Skill is the Agent-side bridge to the Configure Component in Implementation.

Read the Component sources together:

- Definition and Principles: `.interface/implementation/process/configure/definition.md`
- Preferences: `.interface/implementation/process/configure/preferences.yaml`

These files are the authority for Configure. This Contract does not repeat their content.

## Trigger

Activate when Configure is invoked by the Human or a declared coordinator.

## Inputs

Use the inputs declared by the Configure Component Definition and Preferences.

## Outputs

Use the outputs declared by the Configure Component Definition and Preferences. Do not reproduce them here.

## Required Understanding

Read the Configure Component Definition, Principles, and Preferences before execution.

## Authority

Follow the authority declared by the Configure Component Definition and Preferences.

## Workflow Invariants

- Keep this Skill aligned with the Configure Component sources.

## Verification

Use the verification declared by the Configure Component sources.

## Idempotency

Preserve the behavior declared by the Configure Component sources when invoked repeatedly.

## Stopping Conditions

Stop when the Configure Component sources cannot be read or their declared operation cannot be realized.

## Runtime Realization

Expose the native Configure capability as an adapter to the Configure Component sources. Runtime details remain provider-owned.
