---
name: my-interface-reset
description: Core Skill `reset` — Human-only. Reconciles exactly one explicitly authorized reset scope (explicit phases, all phases with generated work, `config`, or `complete`) after a complete preview and explicit Human confirmation, preserving everything outside that scope.
argument-hint: "[phase-id ...] | config | complete"
disable-model-invocation: true
---

# Reset — Core Skill `reset`

Required Core Skill. Stable key: `reset`. Skill name: `my-interface-reset`.

Native realization. The governing authority is the current Reset Operation Definition and Preferences in the Implementation Module; this Skill realizes their meaning and never overrides them.

## Invocation and inputs

- May be invoked **only directly by the Human**, because Reset acts only on an explicitly authorized scope. Model invocation is disabled. No Agent, Skill, coordinator, or automation may invoke, chain, or simulate it.
- Inputs: an invocation request and **exactly one** scope:
  - one or more explicit phase identifiers;
  - no argument — every phase with generated work;
  - `config`;
  - `complete`.
  Anything else, or more than one scope kind, is refused.

## Start

1. Apply the loaded Runtime Rules first: `interface-skill-policy`, `interface-bootstrap`, `agent-conduct`, `git-discipline`.
2. Locate through `.interface/interface.md` (Implementation Module → Operations → Reset) and read in full the current Reset Definition and Reset Preferences (located, when this Skill was realized, at `.interface/implementation/operations/reset/reset.md` and `reset.yaml`), plus the State Definition and Schema needed to write records. If they contradict this Skill, follow them and report Runtime drift so the Human can run `/my-interface-native-implement`.
3. Never read, search, or use `.interface/executor/`.

## Workflow

1. **Log Entry.** Create this execution's State Log Entry when a valid State Config exists (see Execution Log). Reset is a recorded event, not a Workflow Mode.
2. **Resolve before mutation.** Resolve phase identity, ownership, generated outputs, State, Plan, Review, Config, Platform Launch authorities, Task evidence, and the observable repository state for the selected scope.
3. **Scope meaning.**
   - Explicit phases: remove that phase's Plan, Task content and history, Review and Findings, attributable implementation output, and aggregate progress.
   - No argument: the same for every phase with generated work.
   - `config`: remove the operational Config files without regenerating them.
   - `complete`: the `config` reset combined with the all-phase reset, while preserving the Config container and Environment preparation.
4. **Preview.** Produce a complete preview: every exact target to be removed or reset, every protected target to be preserved, and the runtime parts that would be stopped. Resolve shared paths conservatively. If attribution is unresolved, or the reset is ambiguous or unsafe, refuse and stop without mutation.
5. **Explicit Human confirmation.** Ask the Human to confirm the exact preview and wait. No removal happens before explicit confirmation. This confirmation is required by Reset's Principle; it is not an unstated choice.
6. **Execute the confirmed scope only.** Stop affected runtime parts in dependency order. Remove or reset only the exact confirmed targets, using bounded file removal (exact paths, never broad globs) and recoverable mechanisms where practical. Preserve Interface and Target sources, protected content, unselected phases, and meaningful surviving history.
7. **Verify.** Confirm every previewed target was removed or reset and every protected target is intact.
8. **Record** what was removed and what was retained, and the resulting State.
9. Repeating an already realized reset removes nothing beyond a newly resolved and confirmed preview.

## Execution Log (mandatory)

- Create exactly one Log Entry in the State Config for this execution: next project-wide sequential zero-padded `id`, the Skill, the event, start time, and an in-progress outcome, following the current State Definition and Schema.
- When work completes, stops, or is blocked, update that same Entry with outcome, report, `data` (preview, removed and retained targets, verification), Open Questions, Blockers, and `duration` when timing is known.
- When the confirmed scope removes the State Config itself (`config` or `complete`), the Entry is removed with it: state that explicitly in the output, which then carries the complete execution record. Never recreate a removed Config record.
- If no valid State Config exists, report the unrecorded Entry in the output.
- Never copy transcripts, secrets, Task histories, or Target content into the Log.

## Boundaries

- Changes only records and outputs explicitly included in the confirmed scope. Never changes Target intent, Principles, Preferences, or Development results outside that scope; never edits `.interface/`.
- Never invokes another workflow operation (no other `my-interface-*` Core Skill).
- Git commands that discard or rewrite work (`git reset`, `git restore`, `git checkout`, `git clean`, …) stay under the Human's confirmation prompt; never work around it. Never commits or pushes.

## Output

The Skill execution result and status: the confirmed scope, the preview, every removed and retained target, verification evidence, the resulting State, the Log Entry ID (or the statement that it was removed with the State Config), and any Blockers and Open Questions.
