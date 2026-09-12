---
name: my-interface-agent-sync
description: Dynamically reconcile every Agent Component declared by the current Interface with the active project-scoped Agent runtime, materializing authorized missing or drifted capabilities and certifying synchronization only after complete post-change verification.
disable-model-invocation: true
---

# Synchronize the Agent Profile

This file is the Claude Code adapter for the portable `agent-sync` Skill Contract. Resolve and read that Contract through Agent Skill Preferences before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Make the active Agent runtime conform to the complete Agent Profile declared by the Interface. Materialize missing native resources, reconcile drift where ownership is unambiguous, provision already-selected project Extensions and Integrations, and prove that every required capability is usable.

This Skill applies existing Human-owned decisions. It does not discover or select new capabilities; use the capability-installation Skill when the Agent Profile does not already declare the needed choice.

## Understanding

Establish Interface Understanding from the canonical Interface document. Derive the complete current Component inventory from its Agent Structure, then read every discovered Component's Principles, Preferences, and declared resources, including explicit empty categories. Resolve the selected Runtime and its native capability mappings from those sources rather than assuming a particular vendor, directory, command, settings shape, Component list, or mechanism list.

Repeat this discovery on every invocation. A Component or mechanism added to the Agent Module after this adapter was written is part of the run automatically.

Treat Principles as mandatory contracts and Preferences as Human-owned desired state. Never modify either. Inspect current project-scoped runtime artifacts and runtime-reported activation state only after deriving the expected profile.

Before native inspection, validate that Runtime Preferences contain exactly one `component_realization` record for every Component dynamically discovered from the canonical Agent Structure. Reject missing, extra, or duplicate records, unresolved `native_capability_mapping` references, absent realization modes, or absent verification obligations as `blocked`; never infer a mapping from a familiar directory layout.

## Reconciliation plan

Build a complete inventory before changing runtime state:

| Component | Declared desired state | Native destination or provider | Observed state | Proposed action | Authority or blocker |
| --- | --- | --- | --- | --- | --- |

Include every dynamically discovered Agent Component, even when its declared category is empty or already satisfied. Classify each action as `no change`, `create`, `update`, `install`, `enable`, `activation required`, `report only`, or `blocked`. Never silently skip an unknown, new, or unsupported Component or mechanism; report a missing native mapping as blocked.

Use each Component's Realization record to resolve its native mechanisms, authorized write targets, and verification gate. A `runtime-provided` Component is observed rather than materialized unless an exact write target is separately declared. An `explicitly-unused` Component requires no native capability and never authorizes removal of an observed undeclared capability.

Resolve ownership before proposing a write. Preserve compatible native values that the Agent Profile leaves unspecified. Report an undeclared native capability as unmanaged unless it conflicts with a Principle or selected choice; do not remove or disable it automatically.

## Reconcile

Verify that the selected Runtime is available and compatible with the declared Profile. Derive reconciliation order from the current Component Relationships and Runtime mappings, then process every inventory row while preserving its owner's authority. Add required declared sources and install or enable only entries already selected by Human-owned Preferences and only at project scope. Reload or activate changed capabilities when the Runtime supports doing so safely.

A selected desired state is standing project authorization for additive, project-scoped reconciliation of that exact declaration. Still honor runtime permission prompts and stop for Human action when provisioning needs credentials, trust of an external service, broader scope, destructive replacement, an irreversible action, or authority not already expressed by the declaration.

When a required native resource is missing, construct the smallest implementation that faithfully realizes its owning Principle and declared Preference. Point to existing contracts instead of copying Interface policy into multiple runtime files where the Runtime can resolve references. Never invent content for an explicit empty category.

Write only to an exact `write_target` in the affected Component's Realization record and only when its owning declarations otherwise authorize the change. When actual state conflicts with multiple authorities or meaningful Human-authored runtime content would be overwritten, make no write to that resource. Report the conflict and the exact decision needed.

## Verification

After reconciliation, discard pre-change observations, rediscover the complete Agent Component inventory from the canonical Interface, revalidate one-to-one Component Realization coverage, independently re-read every native artifact, and query runtime status where supported. Apply every Component's declared verification obligation. A declaration or file presence alone is insufficient.

Verify at least that:

- every required Role and Skill is discoverable by its intended Role, and each native Skill invocation control matches its declared Human and coordinator Invocation Policy;
- every Custom Command resolves to its declared owner and argument contract;
- effective settings, permissions, rules, and hooks match their owners;
- each selected Extension is installed, project-enabled, and exposes its expected capabilities;
- each selected Integration is project-declared, trusted, connected, and usable, or is truthfully marked as requiring activation; and
- no secret was written to a project artifact.

The second pass must account for every current Component and every required declaration. Repeating this Skill against unchanged declarations and runtime state must produce no mutation; additions or changes to Agent Components and their sources must be detected on the next run without editing this adapter.

## Boundaries

Operate only on project-scoped Agent runtime artifacts selected by the Runtime mapping. Never modify Interface sources, Interface Config, Target code, application dependencies, user- or machine-scoped configuration, credentials, or unrelated Human work. Never discover and adopt a new marketplace, plugin, Skill, MCP server, Agent, or other capability as part of synchronization.

Do not report a capability as synchronized until its required activation and usability checks pass. A pending restart, authentication, trust prompt, missing provider, unsupported project scope, or unavailable runtime is a blocker or `activation required`, not success.

## Report

Report every dynamically discovered Agent Component as `synchronized`, `already synchronized`, `activation required`, `unmanaged`, or `blocked`. For every mutation, identify the owning declaration, native project artifact or provider action, and verification result. List preserved undeclared capabilities separately and state any Human action still required.

Finish with `Agent Profile synchronized` only when the complete second pass proves every required declaration and mechanism is realized, active, and usable. Otherwise report `Agent Profile not fully synchronized` and enumerate every condition preventing the assurance claim.
