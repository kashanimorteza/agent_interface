---
name: my-interface-agent-sync
description: Reconcile the complete human-declared Agent Profile with the active project-scoped Agent runtime, materializing and verifying missing or drifted roles, skills, commands, rules, tools, hooks, integrations, extensions, interaction choices, permissions, settings, sessions, and observability resources without changing Interface sources or Target code.
disable-model-invocation: true
---

# Synchronize the Agent Profile

## Role

Make the active Agent runtime conform to the complete Agent Profile declared by the Interface. Materialize missing native resources, reconcile drift where ownership is unambiguous, provision already-selected project Extensions and Integrations, and prove that every required capability is usable.

This Skill applies existing Human-owned decisions. It does not discover or select new capabilities; use the capability-installation Skill when the Agent Profile does not already declare the needed choice.

## Understanding

Establish Interface Understanding from the canonical Interface document. Follow its Agent Module route and read every Agent Component's Principles and Preferences, including explicit empty categories. Resolve the selected Runtime and its native capability mappings from those sources rather than assuming a particular vendor, directory, command, or settings shape.

Treat Principles as mandatory contracts and Preferences as Human-owned desired state. Never modify either. Inspect current project-scoped runtime artifacts and runtime-reported activation state only after deriving the expected profile.

## Reconciliation plan

Build a complete inventory before changing runtime state:

| Component | Declared desired state | Native destination or provider | Observed state | Proposed action | Authority or blocker |
| --- | --- | --- | --- | --- | --- |

Include every Agent Component, even when its declared category is empty or already satisfied. Classify each action as `no change`, `create`, `update`, `install`, `enable`, `activation required`, `report only`, or `blocked`.

Resolve ownership before proposing a write. Preserve compatible native values that the Agent Profile leaves unspecified. Report an undeclared native capability as unmanaged unless it conflicts with a Principle or selected choice; do not remove or disable it automatically.

## Reconcile

Apply the inventory in dependency-safe order:

1. Verify that the selected Runtime is available and compatible with the declared profile.
2. Reconcile project-scoped Settings, Permissions, Rules, Hooks, and Interaction choices that establish the execution boundary.
3. Reconcile required Roles, Skills, Commands, Tools, Coordination resources, Session behavior, and Observability resources through the Runtime's declared native mechanisms.
4. Reconcile declared Integrations and Extensions. Add required declared sources, then install or enable only entries selected by the Human-owned Preferences and only at project scope.
5. Reload or activate changed capabilities when the Runtime supports doing so safely, then verify actual discovery and usability.

A selected desired state is standing project authorization for additive, project-scoped reconciliation of that exact declaration. Still honor runtime permission prompts and stop for Human action when provisioning needs credentials, trust of an external service, broader scope, destructive replacement, an irreversible action, or authority not already expressed by the declaration.

When a required native resource is missing, construct the smallest implementation that faithfully realizes its owning Principle and declared Preference. Point to existing contracts instead of copying Interface policy into multiple runtime files where the Runtime can resolve references. Never invent content for an explicit empty category.

When actual state conflicts with multiple authorities or meaningful Human-authored runtime content would be overwritten, make no write to that resource. Report the conflict and the exact decision needed.

## Verification

After reconciliation, independently re-read the native artifacts and query runtime status where supported. A declaration or file presence alone is insufficient.

Verify at least that:

- every required Role and Skill is discoverable by its intended Role;
- every Custom Command resolves to its declared owner and argument contract;
- effective settings, permissions, rules, and hooks match their owners;
- each selected Extension is installed, project-enabled, and exposes its expected capabilities;
- each selected Integration is project-declared, trusted, connected, and usable, or is truthfully marked as requiring activation; and
- no secret was written to a project artifact.

Re-run the complete inventory after changes. Repeating this Skill against unchanged declarations and runtime state must produce no mutation.

## Boundaries

Operate only on project-scoped Agent runtime artifacts selected by the Runtime mapping. Never modify Interface sources, Interface Config, Target code, application dependencies, user- or machine-scoped configuration, credentials, or unrelated Human work. Never discover and adopt a new marketplace, plugin, Skill, MCP server, Agent, or other capability as part of synchronization.

Do not report a capability as synchronized until its required activation and usability checks pass. A pending restart, authentication, trust prompt, missing provider, unsupported project scope, or unavailable runtime is a blocker or `activation required`, not success.

## Report

Report each Agent Component as `synchronized`, `already synchronized`, `activation required`, `unmanaged`, or `blocked`. For every mutation, identify the owning declaration, native project artifact or provider action, and verification result. List preserved undeclared capabilities separately, state any Human action still required, and finish with one truthful overall profile status.
