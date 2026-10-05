---
name: my-interface-launch
description: Core Skill `launch` — verifies readiness, activates a completed implementation (one Development Component with a runtime, or `complete`/`all`), preserves already healthy parts, and records the observable runtime result, Access Points, and any required Human action. Optional scope; with none, uses the default scope from Launch Preferences.
argument-hint: "[component | complete | all] [parent_id=<id>]"
---

# Launch — Core Skill `launch`

Required Core Skill. Stable key: `launch`. Skill name: `my-interface-launch`.

Synchronized Native realization. The governing authority is the current Launch Operation Definition and Preferences in the Implementation Module; this Skill realizes their meaning and never overrides them.

## Invocation and inputs

- May be invoked directly by the Human or by an Agent.
- Inputs: an invocation request and an optional scope — one Development Component that has a runtime, or `complete` (`all` is an alias). When a coordinating Core Skill invokes it, the request carries `parent_id=<that Skill's Log Entry ID>`.

## Start

1. Apply the loaded Runtime Rules first: `interface-skill-policy`, `interface-bootstrap`, `agent-conduct`, `git-discipline`.
2. Locate through `.interface/interface.md` (Implementation Module → Operations → Launch) and read in full the current Launch Definition and Launch Preferences (last synchronized at `.interface/implementation/operations/launch/launch.md` and `launch.yaml`), plus the State Definition and Schema needed to write records. If they contradict this Skill, follow them and report Runtime drift so the Human can run `/my-interface-agent-native`.
3. Never read, search, or use `.interface/agent/`.

## Workflow

1. **Log Entry.** Create this execution's State Log Entry (see Execution Log). Launch is a recorded event, not a Workflow Mode.
2. **Scope.** Use the supplied scope. With none, use the default scope from the current Launch Preferences and record that decision in the Log Entry.
3. **Understanding and inputs.** Establish current Interface and Target Understanding. Read the Target and Platform selections, Platform Principles and Preferences, operational State, the developed parts, their public interfaces, and the observable runtime state.
4. **Resolve definitions.** Resolve the Environment and the Launch definition from explicit Target decisions before Platform defaults. Never invent a missing definition — an unresolved one stops Launch.
5. **Readiness.** Verify every applicable readiness condition before activation, including that Development is complete for the scope. A readiness failure stops Launch; never alter product Source, Target meaning, or Platform authority to make activation appear ready.
6. **Prepare.** Prepare only the declared project-scoped runtime requirements.
7. **Activate idempotently.** Activate only the selected parts, in dependency order. Preserve every healthy running part and change only runtime elements that do not satisfy the current scope. Deliver bindings through public boundaries without recording or exposing secret values.
8. **Record.** Record startup or preservation outcomes, readiness evidence, Access Points, the observable runtime result, any required Human action, and Log data including Blockers and Open Questions.
9. **Stop** on an unresolved Environment or Launch definition, missing system preparation, failed preparation or prerequisite startup, incomplete Development, failed readiness, or an unsafe binding; report the exact reason.
10. Before finishing, expose any runtime processes left running and any unfinished work.

## Execution Log (mandatory)

- At start, create exactly one Log Entry in the State Config: next project-wide sequential zero-padded `id`, the Skill, `parent_id` when supplied, the event, start time, and an in-progress outcome, following the current State Definition and Schema.
- When work completes, stops, or is blocked, update that same Entry with outcome, report, `data` (scope decision, readiness evidence, startup or preservation outcomes, Access Points), Open Questions, Blockers, and `duration` when timing is known.
- If the State Config is missing or invalid, do not create or repair it; report the stop and the unrecorded Entry as a Blocker in the output.
- Never copy transcripts, secrets, Task histories, or Target content into the Log.

## Boundaries

- Never repairs product Source, changes Target meaning, redefines Platform authority, invents a missing definition, or exposes secrets.
- Never edits `.interface/`. Never commits or pushes.

## Output

The Skill execution result and status: scope used, parts started or preserved, readiness evidence, Access Points, required Human actions, the Log Entry ID, and any Blockers and Open Questions.
