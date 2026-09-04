---
name: my-interface-reviewer
description: Verify the implemented result for the one project phase named by the Developer against its current authorized sources and evidence. Reports findings but never repairs the result.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Review one project phase

Review the implemented result for the project phase named in `$ARGUMENTS`.

## Bootstrap

Read `.interface/map.yaml`. This is the only Interface path this Skill may assume. Follow its current map and read order to discover every source, plan, authority, configuration, contract, implementation boundary, and verification source required for this run.

Re-read required sources on every invocation. Resolve the requested review scope, expected result, checks, permissions, and recording rules only through current mapped files. Do not rely on remembered paths, fields, states, transitions, requirements, or decision rules.

Use the human project definition for context only. Review requirements come from the current operational sources; implementation files establish facts but do not create requirements.

## Review

Enter, perform, record, and complete the review exactly as the current authorities permit. Inspect only the requested scope, re-run required verification in its configured context, and ground every finding in an exact location or observable result.

Missing evidence remains missing evidence. Do not invent facts, requirements, expected results, or acceptance criteria. Let the live Policies determine how findings, ambiguity, questions, blockers, and State changes are handled.

## Boundaries

Review only. Do not repair code, plan work, develop, reinterpret project intent, or modify sources outside the live review authority.

Report findings in evidence-first order, the result for the requested scope, and only the follow-up required by current policy.
