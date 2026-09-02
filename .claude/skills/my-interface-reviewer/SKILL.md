---
name: my-interface-reviewer
description: Verify the implemented result for the one project phase named by the Developer against its current plan, generated Understanding, target-item Policy, contracts, and required evidence. Reports findings but never repairs the result.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Review one project phase

Review the implemented result for the one project phase named in `$ARGUMENTS`.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine review behavior but cannot expand this Skill's live authority, review scope, or write boundaries.

## Refresh context before reviewing

1. Resolve the one requested phase id in `$ARGUMENTS` from the current generated Understanding and its matching plan. Refuse an omitted, additional, unknown, or unplanned phase rather than choosing one.
2. Resolve that phase's target item from the phase itself, then follow the live map to read the current State contract, task standard and Schema, target-item Policy, configuration, contracts, implementation locations, and verification evidence needed for this invocation.

## Review

Enter review mode only as the current authorities permit. Review only the requested authorized phase and derive every check, location, expected result, write permission, and state change from the live files that own it. Another phase is outside scope even when it targets the same item.

Re-run required verification in its configured context and ground every finding in an exact file location or observable result. Missing evidence remains missing evidence; do not invent a fact or requirement.

Do not copy task fields, statuses, transitions, configuration keys, paths, or validation rules into this Skill. Resolve them fresh from the current authorities.

## Boundaries and completion

Repair nothing and do not enter planning or development. Record only the review information and state changes the current authorities permit. Report findings in evidence-first order, the result for the requested scope, and any exact blocker or follow-up required.
