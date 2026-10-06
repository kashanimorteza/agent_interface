---
name: my-interface-reset
description: Core Skill for resetting. Previews and, only after explicit Human confirmation, removes or reconciles operational records and generated outputs for exactly one scope (explicit phases, all phases with generated work, config, or complete), preserving everything outside it. Human-invoked only as /my-interface-reset <scope>.
argument-hint: "<phase-id ... | config | complete>  (no argument = all phases with generated work)"
disable-model-invocation: true
---
<!-- managed by /my-interface-native-implement: realized from the Executor Module Skill Contract `reset`; regenerated on every run — do not edit by hand -->

# Reset

The Core Skill for resetting. Required. Stable key: `reset`. Skill name: `my-interface-reset`.

## Inputs

An invocation request and exactly one scope: `$ARGUMENTS` — explicit phases, all phases with generated work (no argument), `config`, or `complete`.

## Invocation

May be invoked only directly by a Human, because Reset acts only on an explicitly authorized scope. Model invocation is disabled for this Skill; no Agent, Skill, or coordinator may invoke it. Reset never invokes another Core Skill; it may use any Provider Skill or other available Skill.

## Authority — read at runtime

Read completely at the start of every run and follow them; this workflow is the Native realization of that understanding and never overrides them.

- `.interface/implementation/operations/reset/reset.md` — Reset's mandatory Principles.
- `.interface/implementation/operations/reset/reset.yaml` — Reset Preferences.

Every Principle in the Definition is mandatory. Reset Preferences can guide only an explicitly authorized scope and can never authorize a destructive scope themselves.

Apply the project Rules (`.claude/rules/`), including Interface protection and preservation of unrelated Human work.

## Workflow

1. Create this execution's State Log Entry (when State exists).
2. Resolve phase identity, ownership, generated outputs, State, Plan, Review, Config, Platform Launch authorities, Task evidence, and observable repository state for the scope.
3. Produce a complete preview of every exact target to remove or reset and every protected target to preserve. Resolve shared paths conservatively; refuse an ambiguous or unsafe reset; unresolved attribution stops mutation.
4. Require explicit Human confirmation of that preview before any mutation.
5. Apply only the confirmed scope:
   - explicit phases → remove each phase's Plan, Task content and history, Review and Findings, attributable implementation output, and aggregate progress; no argument → the same for every phase with generated work;
   - `config` → remove the operational Config files without regenerating them;
   - `complete` → Config reset plus all-phase reset, preserving the Config container and Environment preparation.
6. Stop affected runtime parts in dependency order; use bounded file removal on exact targets only.
7. Verify every previewed and every protected target; record what was removed or retained and the resulting State; complete the Log Entry and report.

Repeating an already realized reset removes nothing beyond a newly resolved and confirmed preview.

## Boundaries

Never alter anything outside the authorized scope. Preserve Interface and Target sources, protected content, unselected phases, and meaningful surviving history. Never change Target intent, Principles, Preferences, or Development results outside the explicit scope. Never remove a target whose attribution is unresolved.

## Execution Log

Every execution creates one Log Entry in State with its `id` and Skill, and updates that same Entry with outcome, report, and any applicable `data` (removed and retained targets), Open Questions, or Blockers when work completes, stops, or is blocked. Follow the State Component (`.interface/implementation/operations/state/state.md`) and State Schema; when the scope removes the State record itself, report the outcome explicitly instead.

## Outputs

The Skill execution result and status.
