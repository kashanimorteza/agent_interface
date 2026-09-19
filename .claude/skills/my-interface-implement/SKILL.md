---
name: my-interface-implement
description: Implement selected Target phases, or every enabled and ready phase when none is specified, by running Configure once only when no phase is specified, then entering each phase through Review first when it already has an implementation or through Planning first when it has none, and repeating the Planning, Developing, and Review cycle while Review records Findings and progress continues, before eligible Launch.
argument-hint: "[phase-number ...]"
disable-model-invocation: true
metadata:
  contract: ".interface/agent/skill/contracts/implement.md"
  contract_sha256: "sha256:0ac23fa7758cd6882f697b27cb8a1add4bd116a1f58cf9f63bbd356c9df916ae"
  preferences: ".interface/agent/skill/preferences.yaml"
  preferences_sha256: "sha256:386052d88bf6225ecc6b2cc35f60fc2e7344a26bce478741efa86371fde6d566"
  synced_at: "2026-09-19T16:31:31Z"
---

# Implement the Target

This file is the self-contained Claude Code realization of the portable `implement` Skill Contract, placed here by Agent Sync as the Human authored it. Follow this file and the synchronized Runtime Rules under `.claude/rules/`; never read or resolve Agent Module sources.

## Invocation

Run only on explicit Human invocation of `/my-interface-implement`. Model, delegated, and automated invocation are disabled (`disable-model-invocation: true`); no Skill, coordinator, Hook, or automation may start this Skill.

## Purpose

Provide one trustworthy sequential path from operational readiness through independently assured implementation and eligible launch.

## Responsibility

Validate phase selection, coordinate Configure once, then execute Planning, Developing, and Review for each phase in Target order. Reconcile Findings through their owning operations and advance only after the current phase is satisfied. Implement performs no product operation of its own.

## Trigger

Activate explicitly for zero or more phase selections when the Human wants complete orchestration rather than operation-by-operation control.

## Inputs

Accept zero or more phase positions. Empty input selects every phase currently enabled and ready. Resolve positions to stable identifiers, validate all tokens before mutation, deduplicate them, and retain Target order. Consume current operation Contracts, Target eligibility, operational records, dependencies, implementation, and Review evidence.

Claude Code input handling: the positions arrive as whitespace-separated positive integers in `$ARGUMENTS` — `1` selects the first phase, `2` the second, and so on. Resolve numbers against current Target phase order and use stable identifiers throughout orchestration. Report disabled or unready selected phases as outside executable scope. For any invalid token, enumerate available phases with number, stable identifier, title, status, and readiness, identify every invalid token, and request a corrected list without running Configure or another operation. If no implementable phase remains, make no changes and report why.

## Outputs

Produce the integrated ordered outcomes of Configure when it ran, and of every per-phase Planning, Developing, Review, and reconciliation cycle; Implementation State and History owned by Implement, including one step-by-step run entry under State's implementation record that lists the selection, whether Configure ran, and for every phase each Planning → Developing → Reviewing cycle with its outcome, the stop reason when the loop stopped, and the Launch decision; withheld phase results; all Blockers and Open Questions; eligible Launch; and a truthful distinction between selected-scope completion and whole-Target completion.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Resolve the synchronized active Runtime implementations for Configure, Planning, Developing, Reviewing, and Launch, their owned records, and their gates. Never enter the Agent Module to resolve them or their Contracts.

Claude Code routes: establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, then Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Resolve the operation Skills through the synchronized Runtime capability catalog (`.claude/rules/interface-agent-capabilities.md`) and the Skills currently discoverable in this Runtime.

## Authority

Coordinate operation Skills directly and write only Implementation State — its status and the step-by-step run log — and its History independently. Every delegated mutation remains under the invoked Skill and owning Component. Never bypass Human approval or combine operation ownership.

## Workflow Invariants

1. Resolve and validate the complete phase selection before any mutation.
   - Invalid input runs no operation.
2. Resolve Configure, Planning, Reviewing, Developing, and Launch through the synchronized Runtime capability catalog and prove that the Runtime permits Implement to invoke each one as the declared coordinator.
   - Never read Agent Module sources.
   - An unavailable or coordinator-incompatible Child Skill blocks the run before mutation.
3. Execute Configure exactly once when the invocation carried no phase selection, then confirm its required readiness before phase work.
   - When the invocation selected specific phases, do not execute Configure.
4. Process selected implementable phases strictly in Target order, one complete phase at a time.
5. Choose the phase's entry from current records.
   - When the phase already has an implementation — its State record shows Development completed or a Review record exists for it — enter through Reviewing first: Review judges the existing Plan and implementation against current Understanding, so that a changed Target (new models, changed fields, new requirements) surfaces as Findings before any work is redone.
   - When Review is satisfied, the phase is complete as it stands and no Planning or Developing runs.
   - When the phase has no implementation, enter through Planning.
6. Execute Planning for the current phase — even when a Plan exists — reading any recorded Findings; Planning's reconciliation and idempotency preserve valid current work.
7. Execute Developing for the current phase, including durable checks and its completion gate, reading any recorded Findings.
8. Execute Reviewing after implementation exists.
   - Reviewing invokes nothing; it judges the current Plan and implementation against current Understanding and records every Finding with its owning operation.
   - When Review is not satisfied, rerun the cycle for the same phase: Configure when a Finding names it, then Planning, then Developing, then Reviewing.
   - Continue only while a cycle closes or materially advances at least one Finding.
9. Stop on a repeated unresolved Finding, no observable progress, inconclusive assurance, unmet dependency, failed operation gate, or required Human decision.
10. Advance to the next selected phase only after the current phase has satisfied Plan and Implementation Assurance.
   - An incomplete phase withholds every later phase in this invocation.
11. Launch only when every currently enabled and ready phase—not merely the selected subset—has completed Planning and Development and has satisfied both Review assurances.

Implementation never derives its sequence from a mutable Target workflow. It locates and executes operation Skills directly rather than depending on nested command invocation. No incomplete or missing gate is passed.

Claude Code execution detail: invoke a Child Skill with Claude Code's `Skill` tool, naming its synchronized Skill name (`my-interface-configure`, `my-interface-planning`, `my-interface-developing`, `my-interface-reviewer`, `my-interface-launch`), so that Skill loads and executes its own SKILL.md. This is what "execute", "invoke", and "locate and execute directly" mean throughout this Skill. Never read a Child Skill's SKILL.md and execute its workflow inline, and never delegate one to a forked or subordinate agent that inherits this Skill's context: neither runs that Skill's own definition, so neither is an invocation and neither may be reported as one. If any Child Skill is unavailable or does not permit this coordinator, stop before Configure and report Runtime drift; never inspect Agent Module sources or invoke the Agent Native Skill automatically. Record Implementation State as `in progress` under its owner and open this run's step-by-step entry under State's implementation record, in the shape the current State authorities define, before the first phase; record the phase entry (Review first or Planning first), each cycle and the outcome of each operation in it, the stop reason, and the Launch decision as they occur.

## Verification

- Verify every delegated operation's own success evidence and gate.
- A phase passes only when its current Review record proves both Plan Assurance and Implementation Assurance are satisfied.
- Overall completion additionally requires every currently implementable phase to pass and Launch to complete.

## Idempotency

Repeated invocation reruns the ordered gates against current authorities while each delegated Skill preserves valid completed work and avoids unnecessary mutation. A satisfied unchanged phase may produce no product change but is still revalidated before advancement.

## Stopping Conditions

- Stop before all mutation on invalid input or an empty implementable selection.
- Stop the run on the first selected phase that cannot pass an operation or assurance gate, makes no reconciliation progress, reaches an inconclusive condition, has an unmet dependency, or requires a Human decision.
- Any incomplete implementable phase prevents Launch and overall completion.

Claude Code execution detail: on a stop, record truthful phase and Implementation State, every delegated outcome, Blocker or Open Question, and the exact later phases withheld. After every currently implementable phase is independently satisfied and Launch completes, record Implementation State as `completed`, its completion time, and the outcome History Event. Completion of a selected subset never implies whole-Target completion.

## Runtime Realization

A native adapter exposes optional multi-phase input, resolves operation implementations through synchronized Runtime capabilities, invokes Configure once when no phase was selected and then, for each phase, either Review first when an implementation already exists or Planning first when none does, followed by the Planning → Developing → Review cycle repeated while Review records Findings and progress continues, and reports every operation and reconciliation outcome in execution order without reading Agent Module sources.

In Claude Code this adapter reports the requested and resolved phase selection, the Configure outcome when Configure ran, and for each phase its entry and every Planning, Development, and Review cycle and reconciliation outcome in execution order. Then it reports withheld phases, Blockers and Open Questions, selected-scope completion, whole-Target completion, and the Launch result, keeping selected-scope completion truthfully distinct from whole-Target completion.
