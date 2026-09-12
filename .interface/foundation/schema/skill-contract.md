# Skill Contract Structure

A Skill Contract is the portable, runtime-independent behavioral definition of one Interface-owned Agent Skill. One Contract exists for every `my-interface-*` Skill declared by Agent Skill Profile at `.interface/agent/skill/contracts/<interface-owned-skill>.md`.

The Contract is Human-owned. Agents read it and may realize it through a selected Runtime, but never edit it during execution. A native Skill implementation is an adapter and cannot override the Contract.

## Required structure

Every Skill Contract contains these sections in this order:

1. **Title** — `# <name> Skill Contract`.
2. **Purpose** — the outcome for which the Skill exists.
3. **Responsibility** — the single responsibility it owns and adjacent work it excludes.
4. **Trigger** — explicit and implicit activation conditions.
5. **Inputs** — accepted Human input and required source inputs, including empty-input behavior.
6. **Outputs** — produced records, artifacts, state transitions, and report obligations.
7. **Required Understanding** — Interface Understanding, Target Understanding when applicable, and role-specific authorities that must be current.
8. **Authority** — exact read, write, execution, provisioning, and delegation boundaries.
9. **Workflow Invariants** — Skill-specific ordering and behavioral conditions that every runtime realization preserves. These state required outcomes and gates, not vendor commands or file formats.
10. **Verification** — observable evidence required before success may be reported.
11. **Idempotency** — what a repeated invocation preserves or reconciles.
12. **Stopping Conditions** — invalid input, missing authority, unmet gates, approval points, conflicts, or external activation that stop or limit execution.
13. **Runtime Realization** — what a native adapter must expose and which implementation details remain provider-owned.

## Content rules

- The Contract contains no Target facts, resolved project state, credentials, concrete provider commands, or vendor-specific storage layout.
- A fixed sequence is included only when changing that sequence changes the Skill's meaning, safety, independence, or completion claim.
- Inputs name semantic values. Command syntax and aliases remain owned by Agent Command Profile.
- Source formats, status vocabularies, and storage shapes remain owned by their Components and Schemas; the Contract points to those owners rather than copying them.
- External framework, package, extension, built-in, user, and managed Skills remain provider-owned resources declared in Skill Profile. They follow applicable Agent Principles and the active Role but do not receive Interface-owned Skill Contracts.
- Every obligation appears once. Shared obligations remain in Agent Skill Principles or another owning Component and are referenced, not copied.
