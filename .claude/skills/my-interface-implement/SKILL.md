---
name: my-interface-implement
description: Implement selected Target phases, or every enabled and ready phase when none is specified, by running Configure once and then Planning, Plan Review, Developing, and final Review sequentially for each phase before eligible Launch.
argument-hint: "[phase-number ...]"
disable-model-invocation: true
---

# Implement the Target

This file is the Claude Code adapter for the portable `implement` Skill Contract. Resolve and read that Contract through Agent Skill Preferences before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Provide the trustworthy full-path entry point while preserving the ownership and gates of Configure, Planning, Developing, Reviewing, and Launch. Implement coordinates those Skills and performs no product operation of its own.

The individual operation Skills remain available when the Human wants to work step by step. A successful Implement result means every processed phase passed Planning, independent Plan Assurance, Development, and independent final Implementation Assurance in that order.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects the first phase, `2` the second, and so on. Resolve numbers against current Target phase order and use stable identifiers throughout orchestration.

If `$ARGUMENTS` is empty, select every phase the current Target marks both enabled and ready for implementation.

Validate the complete selection before changing any file or invoking any operation. Every token must be a positive integer resolving to an available phase. Deduplicate repeats and retain Target order. Report disabled or unready selected phases as outside executable scope. For any invalid token, enumerate available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without running Configure or another operation.

If no implementable phase remains, make no changes and report why.

## Understanding

Establish Interface Understanding from the canonical Interface document, then Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Resolve phase eligibility and the current implementations, Contracts, records, and stopping conditions for Configure, Planning, Developing, Reviewing, and Launch.

## Workflow

Execute this fixed sequence; do not derive it from a mutable Target workflow:

1. Execute Configure exactly once. Continue only when its required operational records and Environment preparation pass their gates.
2. Record Implementation State as `in progress` under its owner.
3. Process selected implementable phases strictly in Target order, completing the entire sequence for one phase before touching the next.
4. Invoke Planning for the current phase. An existing valid Plan is reconciled idempotently rather than regenerated for style.
5. Invoke Reviewing for the same phase as the Plan gate. Use its `plan_outcome`; do not invoke Development unless Plan Assurance is `satisfied`. Reviewing may coordinate Planning and recheck its result under its own Contract.
6. Invoke Developing for the phase, including its durable verification and completion gate.
7. Invoke Reviewing again. This final pass re-assures the current Plan and performs Implementation Assurance against current Source and evidence.
8. If Plan Findings remain, let Reviewing route them through Planning. If implementation Findings remain, invoke Developing with those recorded Findings, then invoke Reviewing again.
9. Repeat step 8 only while the cycle closes or materially advances at least one Finding. Stop on repetition, no observable progress, an inconclusive assurance, failed dependency or gate, or required Human decision.
10. Advance to the next selected phase only when the current Review proves both `plan_outcome: satisfied` and `implementation_outcome: satisfied`. Otherwise withhold every later phase in this invocation.
11. After all selected phases pass, invoke Launch only if every currently enabled and ready Target phase—not merely the requested subset—has completed Planning and Development and satisfied both Review assurances.

Locate each operation through the current Interface and invoke its implementation directly; do not depend on nested Slash Command invocation. Every operation retains its own write authority. Implement writes only its Implementation State and History.

Repeated invocation runs the same gates against current sources. Planning and Developing preserve valid current output, while Reviewing independently re-establishes assurance. Never skip a gate merely because an earlier run recorded success.

## Stopping and state

Stop the entire run at the first selected phase that cannot pass. Record truthful phase and Implementation State, every delegated outcome, Blocker or Open Question, and the exact later phases withheld. An incomplete phase prevents Launch and prevents overall Implementation State from becoming `completed`.

After every currently implementable phase is independently satisfied and Launch completes, record Implementation State as `completed`, its completion time, and the outcome History Event. Completion of a selected subset never implies whole-Target completion.

## Boundaries

Implement coordinates operation roles and performs no product operation itself. It does not define Target, write Plan or Source, perform Review judgment, combine ownership boundaries, bypass a gate, or infer Human approval.

## Report

Report the requested and resolved phase selection, Configure outcome, and for each phase its Planning, Plan Review, Development, final Review, and reconciliation outcomes in execution order. Then report withheld phases, Blockers and Open Questions, selected-scope completion, whole-Target completion, and Launch result.
