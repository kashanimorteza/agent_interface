---
name: my-interface-implement
description: Implement selected Target phases, or every enabled and ready phase when none is specified, by running Configure once only when no phase is specified, and then Planning, Developing, and Review sequentially for each phase before eligible Launch.
argument-hint: "[phase-number ...]"
disable-model-invocation: true
metadata:
  contract: ".interface/agent/skill/contracts/implement.md"
  contract_sha256: "sha256:fc43267d5952bfc0274eccfc066fd18acb8c7806657cb23800ab468fcb7a1b20"
  synced_at: "2026-09-17T12:58:42Z"
---

# Implement the Target

This file is the self-contained Claude Code realization of the portable `implement` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Role

Provide one trustworthy sequential path from operational readiness through independently assured implementation and eligible Launch, while preserving the ownership and gates of Configure, Planning, Developing, Reviewing, and Launch. Implement coordinates those Skills, reconciles Findings through their owning operations, and performs no product operation of its own.

Run only on explicit Human invocation of `/my-interface-implement`, when the Human wants complete orchestration rather than operation-by-operation control. The individual operation Skills remain available when the Human wants to work step by step. A successful Implement result means every processed phase passed Planning, Development, and Review in that order.

## Input

Accept zero or more whitespace-separated positive integers from `$ARGUMENTS`: `1` selects the first phase, `2` the second, and so on. Resolve numbers against current Target phase order and use stable identifiers throughout orchestration.

If `$ARGUMENTS` is empty, select every phase the current Target marks both enabled and ready for implementation.

Validate the complete selection before changing any file or invoking any operation. Every token must be a positive integer resolving to an available phase. Deduplicate repeats and retain Target order. Report disabled or unready selected phases as outside executable scope. For any invalid token, enumerate available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without running Configure or another operation.

If no implementable phase remains, make no changes and report why.

## Understanding

Establish Interface Understanding from the canonical Interface document, then Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Without entering the Agent Module, resolve phase eligibility, dependencies, operational records, implementation, Review evidence, and the synchronized Runtime implementations, owned records, and gates of Configure, Planning, Developing, Reviewing, and Launch.

## Workflow

Execute this fixed sequence; never derive it from a mutable Target workflow:

1. Resolve Configure, Planning, Reviewing, Developing, and Launch through the synchronized Runtime capability catalog (`.claude/rules/interface-agent-capabilities.md`) and the Skills currently discoverable in this Runtime. Before mutation, prove that each is discoverable and that its native invocation controls permit invocation by Implement as the declared coordinator. Invoke a Child Skill with Claude Code's `Skill` tool, naming its synchronized Skill name, so that Skill loads and executes its own SKILL.md. This is what "invoke directly" and "do not depend on nested Slash Command invocation" mean throughout this Skill. Never read a Child Skill's SKILL.md and execute its workflow inline, and never delegate one to a forked or subordinate agent that inherits this Skill's context: neither runs that Skill's own definition, so neither is an invocation and neither may be reported as one. If any Child Skill is unavailable or does not permit this coordinator, stop before Configure and report Runtime drift; never inspect Agent Module sources or invoke Agent Sync automatically.
2. Execute Configure exactly once when the invocation carried no phase selection. When the invocation selected specific phases, do not execute Configure. When Configure ran, continue only when its required operational records and Environment preparation pass their gates.
3. Record Implementation State as `in progress` under its owner.
4. Process selected implementable phases strictly in Target order, completing the entire sequence for one phase before touching the next.
5. Invoke Planning for the current phase even when a Plan exists. An existing valid Plan is reconciled idempotently rather than regenerated for style.
6. Invoke Developing for the phase, including its durable checks and completion gate.
7. Invoke Reviewing after implementation exists. Reviewing may coordinate Configure, Planning, or Developing under its own definition when current authorities or evidence require reconciliation, and then re-reviews the resulting state.
8. When Review is not satisfied, route each remaining Finding through its owning Skill — invoke Configure, Planning, or Developing for the Finding that operation owns, within the current phase — and then invoke Reviewing again.
9. Repeat step 8 only while a cycle closes or materially advances at least one Finding. Stop on a repeated unresolved Finding, no observable progress, an inconclusive assurance, an unmet dependency, a failed operation gate, or a required Human decision.
10. Advance to the next selected phase only when the current Review record proves both Plan Assurance and Implementation Assurance satisfied. Otherwise withhold every later phase in this invocation.
11. After all selected phases pass, invoke Launch only if every currently enabled and ready Target phase—not merely the requested subset—has completed Planning and Development and satisfied both Review assurances.

Every operation retains its own write authority. Implement writes only its Implementation State and History, verifies every delegated operation's own success evidence and gate, and never bypasses Human approval or combines operation ownership.

Repeated invocation reruns the same ordered gates against current sources. Planning and Developing preserve valid current output, while Reviewing independently re-establishes assurance. A satisfied unchanged phase may produce no product change but is still revalidated before advancement; never skip a gate merely because an earlier run recorded success.

## Stopping and state

Stop before all mutation on invalid input or an empty implementable selection. Stop the entire run at the first selected phase that cannot pass an operation or assurance gate, makes no reconciliation progress, reaches an inconclusive condition, has an unmet dependency, or requires a Human decision. Record truthful phase and Implementation State, every delegated outcome, Blocker or Open Question, and the exact later phases withheld. An incomplete implementable phase prevents Launch and prevents overall Implementation State from becoming `completed`.

After every currently implementable phase is independently satisfied and Launch completes, record Implementation State as `completed`, its completion time, and the outcome History Event. Completion of a selected subset never implies whole-Target completion.

## Boundaries

Implement coordinates operation roles and performs no product operation itself. It does not define Target, write Plan or Source, perform Review judgment, combine ownership boundaries, bypass a gate, or infer Human approval.

## Report

Report the requested and resolved phase selection, the Configure outcome when Configure ran, and for each phase its Planning, Development, Review, and reconciliation outcomes in execution order. Then report withheld phases, Blockers and Open Questions, selected-scope completion, whole-Target completion, and Launch result.
