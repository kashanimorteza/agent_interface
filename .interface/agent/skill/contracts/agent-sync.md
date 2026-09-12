# agent-sync Skill Contract

## Purpose

Reconstruct and verify the declared Agent Profile in a compatible project-scoped Runtime.

## Responsibility

Discover every current Agent Component from the canonical Interface, compare each Component's complete declaration with observed native state, reconcile authorized project artifacts and already-selected capabilities, and prove required availability. Agent Sync applies existing Human choices; it never discovers or selects new ones.

## Trigger

Activate explicitly when setting up, repairing, migrating, or auditing an Agent Runtime, and when startup reconciliation is selected by Agent Settings.

## Inputs

Accept no capability selection. Consume the complete Agent Profile, including explicit empty categories, all portable Skill Contracts, the selected Runtime mapping, native project artifacts, and runtime-reported Activation state.

## Outputs

Produce one result for every dynamically discovered Agent Component, project-scoped native resources and additive provisioning authorized by selected declarations, post-change verification, preserved unmanaged capabilities, required Human activation steps, and one truthful overall profile status. A successful overall status certifies that every required declaration is currently realized and usable.

## Required Understanding

Establish Interface Understanding, derive the current Component inventory from the Agent Structure it exposes, and read every discovered Component's Principles, Profile, and declared supporting resources. Read each Interface-owned Skill Contract. Never rely on a Component list remembered by this Contract, a native adapter, or an earlier run. Target Understanding is required only when an Agent declaration explicitly depends on Target-selected context.

## Authority

Modify only project-scoped native Agent artifacts selected by Runtime mapping. Provision only exact Human-selected declarations. Never modify Interface sources or Config, Target code, application dependencies, credentials, user or machine settings, or unrelated Human work.

## Workflow Invariants

- Dynamically enumerate every Agent Component from the current canonical Agent Structure before mutation. A Component or supported mechanism added later is automatically part of the same run without requiring a hardcoded list change.
- Validate the selected Runtime's `component_realization` map against that discovered inventory before observing or changing native state. Every discovered Component must occur exactly once; every listed mechanism must resolve through `native_capability_mapping`; every mode and verification obligation must be explicit. A missing, extra, duplicate, or unresolved record is blocked rather than inferred.
- For every discovered Component, read all sources it declares, derive its complete desired state, identify the Runtime mechanism that realizes it, observe actual state, and record the proposed action and verification gate. Include empty and already-satisfied categories.
- Resolve ownership and classify each item as no change, create, update, install, enable, activation required, report only, or blocked.
- Never silently skip an unknown, new, or unsupported Component, category, or mechanism. Reconcile it when the selected Runtime supplies an authorized mapping; otherwise report it as blocked with the missing mapping or capability.
- Preserve compatible native values left unspecified and report undeclared capabilities as unmanaged unless they conflict; never remove them automatically.
- Verify Runtime compatibility first, derive dependency-safe reconciliation order from current Component Relationships and Runtime mappings, and preserve each Component's ownership throughout execution.
- Treat a selected desired state as standing authorization only for exact additive project-scoped reconciliation. Credentials, external trust, broader scope, destructive replacement, irreversible action, or missing authority still requires Human action.
- Materialize the smallest native adapter that realizes its portable Contract. Never invent content for an empty category or copy authoritative Interface text where a reference is supported.
- Write only to an exact `write_target` declared by the affected Component's Realization record and otherwise authorized by its owning declarations. A runtime-provided or explicitly unused record with no write target is observation-only. Explicitly unused means no capability is required; it never authorizes removal of an observed undeclared capability.
- Preserve meaningful Human-authored runtime content when ownership is ambiguous and report the exact conflict.

## Verification

After reconciliation, discard the pre-change observations and perform a second complete pass from the canonical Agent Structure. Revalidate complete one-to-one Component Realization coverage, re-read every discovered Component source and native artifact, and query current runtime state. Apply each Realization record's verification obligation and prove every required declaration and mechanism is realized and usable, including instantiable Agent Definitions, correct Role and capability assignments, discoverable Skills whose native invocation controls match their declared Human and coordinator Invocation Policies, resolvable Commands, matching effective settings and enforcement, active selected Extensions, usable selected Integrations, and absence of secrets in project artifacts.

The overall result is `synchronized` only when this second pass covers every current Agent Component and every required item passes its own verification gate. Any blocked, missing, conflicting, inactive, unsupported, or unverified required item prevents the success claim, even when all other Components pass.

## Idempotency

After successful reconciliation, a new invocation against unchanged declarations and runtime state produces no mutation. A newly added or changed Agent Component, Principle, Profile, Contract, resource, category, or mechanism is detected from current sources and reconciled on the next invocation.

## Stopping Conditions

Block an affected item on incompatible Runtime, ambiguous ownership, unsupported project scope, destructive conflict, missing provider, or unavailable authority. Mark pending restart, authentication, or trust as activation required. Independent items continue when dependencies permit.

## Runtime Realization

A native adapter uses only mappings declared by Agent Runtime and Settings, dynamically traverses the Agent Structure, and contains no exhaustive Component or mechanism list. It must be bootstrappable from this Contract and the Agent Profile and cannot depend on the previous presence of another vendor's adapter.
