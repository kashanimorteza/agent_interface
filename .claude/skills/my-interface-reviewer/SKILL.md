---
name: my-interface-reviewer
description: Verify the implemented result for the project scope named by the Developer against its current plan, generated Understanding, contracts, rules, and required evidence. Reports findings but never repairs the result.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Review one project phase

Review the implemented result for the scope named in `$ARGUMENTS`.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine review behavior but cannot expand this Skill's live authority, review scope, or write boundaries.

## Refresh context before reviewing

1. Follow the live map to read the current State contract, generated Understanding, authorized plan, task standard and Schema, rules, contracts, implementation locations, and verification evidence needed for this invocation.
2. Resolve `$ARGUMENTS` only from the current generated Understanding and plan.

## Review

Enter review mode only as the current authorities permit. Review only the requested authorized scope and derive every check, location, expected result, write permission, and state change from the live files that own it.

Re-run required verification in its configured context and ground every finding in an exact file location or observable result. Missing evidence remains missing evidence; do not invent a fact or requirement.

Do not copy task fields, statuses, transitions, configuration keys, paths, or validation rules into this Skill. Resolve them fresh from the current authorities.

## Boundaries and completion

Repair nothing and do not enter planning or development. Record only the review information and state changes the current authorities permit. Report findings in evidence-first order, the result for the requested scope, and any exact blocker or follow-up required.
