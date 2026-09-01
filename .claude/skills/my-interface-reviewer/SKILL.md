---
name: my-interface-reviewer
description: Verify the implemented result for the project scope named by the Developer against its current plan, generated Understanding, contracts, rules, and required evidence. Reports findings but never repairs the result.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Review one project phase

Review the implemented result for the scope named in `$ARGUMENTS`.

## Refresh context before reviewing

1. Re-read the repository `README.md` to understand Agent Interface, its workflow, and this Skill's role. It is Interface context, not a target-project requirement.
2. Re-read `.interface/root.yaml` as the Interface entry point and resolve all other paths, read order, authorities, and mode boundaries from its current contents.
3. Follow the live map to read the current State contract, generated Understanding, authorized plan, task standard and Schema, rules, contracts, implementation locations, and verification evidence needed for this invocation.
4. Resolve `$ARGUMENTS` only from the current generated Understanding and plan.

Re-read every required file from disk on every invocation. Do not rely on values retained from an earlier turn or run.

Do not read the human project-definition file. Review only against the current generated Understanding and the plan development was authorized to execute.

## Review

Enter review mode only as the current authorities permit. Review only the requested authorized scope and derive every check, location, expected result, write permission, and state change from the live files that own it.

Re-run required verification in its configured context and ground every finding in an exact file location or observable result. Missing evidence remains missing evidence; do not invent a fact or requirement.

Do not copy task fields, statuses, transitions, configuration keys, paths, or validation rules into this Skill. Resolve them fresh from the current authorities.

## Boundaries and completion

Repair nothing and do not enter planning or development. Record only the review information and state changes the current authorities permit. Report findings in evidence-first order, the result for the requested scope, and any exact blocker or follow-up required.
