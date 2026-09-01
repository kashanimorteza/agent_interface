---
name: my-interface-reviewer
description: Review mode — verify the implemented result for the project phase named by the Developer against its current plan, Config, contracts, and rules. Reports evidence and records only authorized review state; never repairs the result.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Review one project phase

Review the implemented result for the project phase named in `$ARGUMENTS`.

## Read before reviewing

1. Read `README.md` to understand Agent Interface, its workflow, and the Reviewer Skill's role. README content is system context only; never use it as a target-project requirement.
2. Read `.interface/root.yaml` and follow its mappings, read order, mode boundaries, and authority references.
3. Read the live State contract before recording any review state.
4. Read the current Task file and its governing Schema completely.
5. Resolve the requested phase from the generated Understanding and its plan, then read every mapped Config file, rule set, contract, and implementation location required to review that phase.

Do not read `.interface/project.md`. Review the result only against the generated Understanding and the plan that downstream development was authorized to execute.

## Phase scope

Exactly one project phase must be named. If it is missing, ambiguous, absent from the Understanding, or has no reviewable plan, stop and ask or use the configured gap mechanism. Do not select a phase or target implicitly and do not carry one over from an earlier run.

Enter review mode only as the live State contract authorizes for this invocation. Review only the requested phase; do not expand into another phase.

## Review

Derive every check from the current Config, Task standard, project Rules, contracts, and task evidence. Re-run the verification required by completed tasks in the context their target Config defines. Check that implementation scope, dependencies, contracts, state, and recorded outcomes satisfy their current authorities.

A finding must name the exact file and section or observable verification result that supports it. Do not create a rule that is absent from Config, and do not turn missing evidence into an invented fact.

Do not reproduce task fields, status values, transition identifiers, Config keys, or validation rules inside this Skill. Read them fresh from the files that own them.

## Write boundary

Repair nothing. Determine every permitted review write from the live Interface map, file policies, Task standard, and State contract. Record only findings and state changes those authorities explicitly allow. Everything else, including product code and plan content, is read-only.

## Completion

Record the run outcome through the live State contract and report findings in evidence-first order. State whether the requested phase passed review, what failed, and the exact blocker or follow-up required. Do not continue into implementation or planning.
