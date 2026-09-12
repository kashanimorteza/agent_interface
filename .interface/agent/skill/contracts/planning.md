# planning Skill Contract

## Purpose

Define complete, bounded, ordered, and verifiable work for Target phases.

## Responsibility

Create or reconcile Plans, Groups, and Tasks from current Target intent and applicable Component authorities. Planning owns what work must achieve and how achievement is observed; it never prescribes implementation or performs downstream operations.

## Trigger

Activate explicitly for zero or more phase selections, or when a coordinator requires a current valid Plan.

## Inputs

Accept zero or more phase positions. Empty input selects every enabled phase. Resolve positions to stable phase identifiers, deduplicate them, and process them in Target order. Consume Target Understanding, applicable Component authorities, current Plan and State, Review Findings, and relevant implementation evidence.

## Outputs

Produce or reconcile only Planning-owned Plan content, Planning aggregate State and History outcomes, conflicts, Blockers or Open Questions permitted by their owners, and a phase-by-phase report.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Read current Plan, State, and Review authorities and Schemas plus every Developer Component applicable to the selected phases.

## Authority

Write only Planning-owned Plan fields and Planning-owned aggregate State and History. Preserve implementation, Review ownership, Target intent, and every field outside Planning authority.

## Workflow Invariants

- Validate the complete input before mutation. Any invalid token prevents the whole planning run and produces the available phase list.
- Build a transient coverage ledger mapping every selected phase requirement, applicable Principle obligation, and unresolved Review Finding to exactly one owning Task or inherited phase context.
- A Plan is incomplete while coverage is missing, duplicated, contradictory, or represented only by a narrower example.
- Preserve valid identities, boundaries, dependencies, wording, progress, and history; prefer stable decomposition over stylistic regeneration.
- Derive new Task boundaries from responsibilities and real dependencies, never document layout or arbitrary batch size.
- Keep planning content implementation-independent and require verification conditions to cover every acceptance clause.
- Process phases independently in Target order unless an owned dependency or Blocker prevents continuation.

## Verification

Validate the complete candidate against the transient coverage ledger, current Plan authorities, and applicable Schemas before writing. Planning is complete only when the selected phase Plan is complete and valid.

## Idempotency

Rebuild from current authorities and reconcile rather than regenerate. Unchanged sources and valid Planning-owned content produce no semantic mutation.

## Stopping Conditions

Stop before mutation on any invalid input. Leave an affected phase incomplete when required intent cannot be resolved safely, coverage cannot be completed, a conflict crosses ownership, or a genuine Blocker applies; continue independent selected phases.

## Runtime Realization

A native adapter exposes optional multi-phase input using the Command mapping, locates all live structures through the Interface, and reports phases, Plan results, changes, conflicts, State, and the supported next step.
