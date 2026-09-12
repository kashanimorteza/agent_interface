# agent-sync Skill Contract

## Purpose

Reconstruct and verify the declared Agent Profile in a compatible project-scoped Runtime.

## Responsibility

Compare every Agent Component declaration with observed native state, reconcile authorized project artifacts and already-selected capabilities, and prove required availability. Agent Sync applies existing Human choices; it never discovers or selects new ones.

## Trigger

Activate explicitly when setting up, repairing, migrating, or auditing an Agent Runtime, and when startup reconciliation is selected by Agent Settings.

## Inputs

Accept no capability selection. Consume the complete Agent Profile, including explicit empty categories, all portable Skill Contracts, the selected Runtime mapping, native project artifacts, and runtime-reported Activation state.

## Outputs

Produce a complete component inventory, project-scoped native resources and additive provisioning authorized by selected declarations, post-change verification, preserved unmanaged capabilities, required Human activation steps, and one truthful overall profile status.

## Required Understanding

Establish Interface Understanding and read every Agent Component's Principles and Preferences. Read each declared Skill Contract. Target Understanding is required only when an Agent declaration explicitly depends on Target-selected context.

## Authority

Modify only project-scoped native Agent artifacts selected by Runtime mapping. Provision only exact Human-selected declarations. Never modify Interface sources or Config, Target code, application dependencies, credentials, user or machine settings, or unrelated Human work.

## Workflow Invariants

- Inventory every Agent Component before mutation, including declared empty and already-satisfied categories.
- Resolve ownership and classify each item as no change, create, update, install, enable, activation required, report only, or blocked.
- Preserve compatible native values left unspecified and report undeclared capabilities as unmanaged unless they conflict; never remove them automatically.
- Verify Runtime compatibility first, then reconcile execution boundaries, executable capabilities, and finally Integrations and Extensions in dependency-safe order.
- Treat a selected desired state as standing authorization only for exact additive project-scoped reconciliation. Credentials, external trust, broader scope, destructive replacement, irreversible action, or missing authority still requires Human action.
- Materialize the smallest native adapter that realizes its portable Contract. Never invent content for an empty category or copy authoritative Interface text where a reference is supported.
- Preserve meaningful Human-authored runtime content when ownership is ambiguous and report the exact conflict.

## Verification

Re-read native artifacts and query current runtime state. Prove required Roles and Skills are discoverable, Commands resolve, effective settings and enforcement match, selected Extensions expose expected capabilities, selected Integrations are usable or accurately pending, and no secret entered project artifacts.

## Idempotency

After successful reconciliation, a complete second inventory against unchanged declarations and runtime state produces no mutation.

## Stopping Conditions

Block an affected item on incompatible Runtime, ambiguous ownership, unsupported project scope, destructive conflict, missing provider, or unavailable authority. Mark pending restart, authentication, or trust as activation required. Independent items continue when dependencies permit.

## Runtime Realization

A native adapter uses only mappings declared by Agent Runtime and Settings. It must be bootstrappable from this Contract and the Agent Profile and cannot depend on the previous presence of another vendor's adapter.
