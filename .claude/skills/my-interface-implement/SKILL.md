---
name: my-interface-implement
description: "Implement selected project phases, or every enabled and ready phase when none is specified, through Configure, baseline Review, Planning, Development, independent final Review, reconciliation, and eligible Launch."
argument-hint: "[phase-number ...]"
disable-model-invocation: true
---

# Implement the Target

This file is the Claude Code adapter for the portable `implement` Skill Contract. Resolve and read that Contract through Agent Skill Preferences before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Implement an already defined Target end to end through a fixed orchestration sequence. Implement coordinates other operation Skills, while each operation keeps its own role, authority, validation, and reporting rules.

Implement is the trustworthy full-path entry point. A successful result means the selected phases were planned from current authoritative sources, developed under their applicable Component authorities, independently reviewed against those same sources, and reconciled until their Review outcomes were satisfied. The individual Planning, Development, and Review Skills remain available for Humans who choose to run the Workflow one operation at a time.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects the first phase, `2` selects the second phase, and so on. Resolve every number against current Target phase order and use each phase's stable identifier throughout orchestration.

If `$ARGUMENTS` is empty, select every phase the current Target marks both enabled and ready for implementation.

If arguments are present, validate the complete selection before changing any files. Every token must be a positive integer that resolves to an available phase. Deduplicate repeated numbers and process selected phases in Target order regardless of argument order. Report a selected phase that is disabled or not ready as outside the executable scope and leave it unchanged. If any token is invalid, enumerate the available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without beginning any operation.

If the resolved selection contains no implementable phase, make no changes and report why no phase can run.

## Workflow

Establish Interface Understanding from the canonical Interface document. Follow its routes to the shared Skill rules, then establish Target Understanding from the Target Technical Definition it locates. Resolve phase eligibility, the current Skills for Configure, Planning, Development, Review, and Launch, their operational records, and their stopping conditions.

A phase is implementable only when Target marks it both enabled and ready for implementation. Preserve disabled, designing, and not-designed phases unchanged and report them as outside the current run.

Implement does not read, derive, or follow the Interface Workflow. Its sequence is fixed:

1. Execute Configure once.
2. Resolve the selected implementable phases in Target order and establish their applicable Component authorities, operational records, dependencies, and current outputs.
3. For each selected phase that already has a Plan, implementation output, Development progress, or Review evidence, execute an independent baseline Review before Planning. Use its Findings to describe the actual gap between current sources and current output. If the Review is `satisfied`, Planning and Development are already truthfully complete, and their sources have not changed, preserve the current output and move to the next selected phase without regenerating it.
4. For a selected phase with no existing work, skip the empty baseline Review and execute Planning.
5. For existing work that is not satisfied, execute Planning to reconcile the current Plan with authoritative sources and baseline Findings.
6. Confirm that Planning completed successfully and that its coverage validation passed before invoking Development. Never develop from a missing, incomplete, invalid, or stale Plan.
7. Execute Development for the phase, including its durable checks and phase completion gate, then execute an independent final Review.
8. When final Review is `not satisfied`, execute another Planning and Development reconciliation using the recorded Findings, then review again. Continue only while each cycle closes or materially advances at least one Finding. Stop that phase when a cycle repeats an unresolved Finding, makes no observable progress, reaches an inconclusive condition, or requires a Human decision.
9. Do not execute a later phase whose prerequisites depend on an incomplete selected phase. Continue with a later selected phase only when the current authorities establish that it is independent of every incomplete result.
10. Execute Launch only when, after this run, every phase currently enabled and ready for implementation has completed Planning and Development and has a `satisfied` Review outcome. A partial phase selection does not Launch an incomplete Target.

Locate each operation's current Skill through the Interface, read its instructions, and execute them directly; do not depend on nested Slash Command invocation. After Configure makes State available, record Implementation State as `in progress`, set this run's start provenance, and append its State History Event.

Do not pass an incomplete operation or phase gate. A missing, inconclusive, or not-satisfied final Review outcome leaves that phase incomplete. Record truthful phase and Implementation State, append the outcome, and report the stopping condition through its owner. Independent selected phases may continue under step 9, but any incomplete implementable phase prevents Launch and prevents the overall Implementation State from becoming `completed`.

After every currently implementable phase is independently satisfied and Launch completes, record Implementation State as `completed`, its completion time, and the outcome History Event. When the requested selection completes but other implementable phases remain incomplete, record the selected phase outcomes without claiming end-to-end completion.

Repeated invocation reconciles the current Target with existing operational records and implementation according to the individual operation rules; it does not discard completed work merely to repeat the sequence.

## Boundaries

Implement coordinates operation roles and performs no product operation of its own. Its only independent write authority is its Implementation State and History under State. It does not define the Target, replace an operation's judgment, combine ownership boundaries, or bypass required human approval.

## Report

Report the requested and resolved phase selection, eligible and skipped phases, each baseline Review, Planning, Development, final Review, and reconciliation outcome in execution order, dependent work withheld, all Blockers and Open Questions, and the final Implementation and Launch result. Distinguish completion of the selected scope from completion of the whole Target.
