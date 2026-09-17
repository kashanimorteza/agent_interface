---
name: my-interface-skill-installer
description: Discover and, after human approval, install project-scoped Agent capabilities relevant to the current Target, including Skills, plugins, MCP integrations, and equivalent supported extensions. Never changes application dependencies or code.
disable-model-invocation: true
metadata:
  contract: ".interface/agent/skill/contracts/skill-installer.md"
  contract_sha256: "sha256:290d21586f5b3f035b8ec08b4451586eb89cf38089c70821bd248bde4b1cdab2"
  synced_at: "2026-09-17T12:24:58Z"
---

# Install Agent capabilities

This file is the self-contained Claude Code realization of the portable `skill-installer` contract synchronized by Agent Sync. Together with Agent Sync, it is one of the two Runtime exceptions permitted to read Agent Module sources, and only strictly within the exact prompt created by this Skill's own direct Human invocation. Follow this adapter and synchronized Runtime rules.

## Role

Materialize every capability the Agent Module declares as Prepared or Installed, and separately discover and provision additional Agent capabilities the current Target could use — always through an explicit, auditable Human decision.

This operation may consider Skills, plugins, MCP integrations, agents, or another extension type supported by the active Agent environment. It equips the Agent; it does not install application runtime dependencies or develop the Target. Agent Sync builds only Constructed Skills — those defined completely by a portable Skill Contract — and never materializes a Prepared or Installed capability. This Skill owns both of those kinds instead: it transfers a declared Prepared capability's content into the Runtime unchanged, and it provisions a declared Installed capability through its owning provider declaration. It also discovers and, after approval, provisions capability needs the Module does not yet declare.

Read the shared Agent Interface rules at the start of the operation and follow them throughout, including their project-scope requirement.

## Trigger

Activate only through explicit Human invocation of `/my-interface-skill-installer` — when the Human requests capability discovery, when a capability the Agent Module declares as Prepared or Installed is not present and usable in the Runtime, or when a required capability is absent from the synchronized Runtime. No Agent Native, Agent Instance, Skill, coordinator, Hook, startup or resume routine, automation, or model-generated action may invoke, chain, trigger, or simulate this Skill.

## Workflow

### Understand

Establish Interface Understanding from the canonical Interface document, then establish Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Read every applicable Implementation Principle and Preference together with synchronized Runtime capabilities and rules, including selected defaults and applicable alternatives. Use dependency manifests, lockfiles, runtime-version files, existing implementation, and installed Agent capabilities as supporting evidence.

Read the complete Agent Module — every Component's Principles and Profile, every Skill Contract, and the prepared-file directory at `.interface/agent/skill/files/` — so every declared capability and its Capability Realization Kind (Constructed, Prepared, or Installed) is known. This read is authorized only inside this Skill's own direct Human invocation and is never carried into, or repeated from, another operation. Never modify an Agent Module source: a candidate that should become part of the portable Agent definition is reported for Human declaration rather than written here, and repairing drift in a Rule, Skill, or other Runtime artifact realized from a Skill Contract remains Agent Sync's job alone.

Derive undeclared capability needs from current evidence on every run. A technology, framework, platform, protocol, service, data source, development activity, or preferred default may indicate that a relevant Agent capability exists. Do not keep a hardcoded technology or capability list in this Skill.

### Identify

Turn the current Module declarations and current Understanding into a visible inventory:

| Item | Capability Realization Kind | Evidence | Why an Agent capability may exist | Capability types to search |
| --- | --- | --- | --- | --- |

Every declared Prepared or Installed capability in the Agent Skill Profile is already an identified item; every undeclared item must cite the Target, Principle, Preference, selected default, dependency, configuration, or implementation evidence that produced it. When the Human's invocation names a specific capability need, include it as its own identified item; an empty or unspecific request instead performs complete relevant discovery from current evidence. Keep distinct needs separate even when one candidate may later satisfy several of them. This inventory defines what Discovery searches; it does not authorize installation or transfer.

### Discover

For each identified item:

1. Check whether an adequate capability is already available to the Agent, matching a declared name against the capability's own name within the Runtime's namespaced identifier rather than requiring an exact string match, so an already-present capability is recognized instead of provisioned again.
2. For a declared Prepared capability, locate its exact matching file or directory under `.interface/agent/skill/files/` by the declared Skill's exact stable key. For a declared Installed capability, resolve its owning provider declaration and any per-Agent-Native identity it names.
3. After the project's packages are installed, use the skill-provisioning mechanism the applicable Language Item declares when one exists, so capabilities bundled by installed packages become discoverable. The absence of a declared mechanism never means none exists, and a declared mechanism never replaces the environment's own current capability.
4. For an undeclared need, search every relevant discovery route supported by the current environment for Skills, plugins, MCP integrations, agents, or equivalent extensions.
5. Verify each candidate by its declared purpose, source, included components, permissions, dependencies, installation scope, and compatibility with the detected technology and version.
6. Prefer authoritative sources: an official source first, then a source maintained by the relevant technology, then a trusted third party.
7. Reject duplicates and options that cannot satisfy the shared project-scope rule.
8. Record a negative result only after the applicable discovery routes have been checked. State where the search was performed instead of claiming broadly that no capability exists.

Discovery is read-only. Adding a catalog, connecting an external service, or changing an installation source is a separate external change and requires approval.

### Preview

After Discovery and before installing, transferring, or updating anything, present one result row for every identified item:

| Item | Capability Realization Kind | Evidence | Capability type | Candidate | Source | Compatibility | Project scope | Included components and permissions | Search result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use **not found** for a need with no verified candidate and identify the discovery routes checked. Use **already available** when the current Agent already has an adequate capability.

Block, and report as **rejected** or **blocked**, a candidate that is incompatible, untrusted, a duplicate, unavailable at project scope, or would require unauthorized access.

After the table, state exactly which candidates are proposed for installation, transfer, or update and ask the human to approve or reject them. Do not install, transfer, update, connect, or add a source before receiving that decision. Adding a marketplace, trusting a service, connecting an external integration, or changing an installation source is itself provisioning and requires this same approval before it happens.

### Install

Materialize or update only the items explicitly approved by the human, and only through a project-scoped mechanism allowed by the shared rules:

- **Prepared** — create the Skill folder and entrypoint required by the selected Agent Native, preserve the prepared content and its meaning exactly as authored — the single Markdown file's instructions, or every file of a prepared directory tree with its internal relative paths intact — and add or adapt only the minimum native metadata needed for discovery and invocation. Never rewrite the Human-owned source file or change its semantic instructions.
- **Installed** — provision through the native mechanism its owning provider declaration names (marketplace, package registry, MCP server, or equivalent).
- **Undeclared** — install or update only through a project-scoped mechanism; a candidate that should become a Module declaration is reported for Human declaration rather than adopted silently.

Preserve rejected and already adequate capabilities unchanged.

Verify the installed capability, its project location or declaration, its included components and permissions, and its activation state. A capability is not `installed` for reporting purposes until the active Agent can discover and use it in this project:

- verify that a Skill — Prepared or newly discovered — is discoverable;
- verify that an installed plugin is project-enabled and its contributed capabilities are loaded; and
- verify that an installed MCP integration is project-declared, trusted, connected, and exposes its expected capabilities.

Complete a supported activation or reload during the installation when possible. When human trust, authentication, restart, or another external activation step remains, report `activation required` and the exact remaining action instead of reporting `installed`. Never place credentials or tokens in a repository-tracked declaration.

If project-scoped installation is unavailable, report the candidate as blocked instead of installing it at user or machine scope.

## Boundaries

Perform only Agent-capability discovery, Prepared and Installed materialization declared by the Module, and approved project-scoped installation of undeclared needs. Do not perform an Interface Operation or change Interface sources, Target application code, architecture, manifests, lockfiles, runtime dependencies, credentials, or user- or machine-scoped state. Do not remove a compatible capability or install a duplicate. Never repair Runtime drift in a Rule, Skill, or other artifact realized from a portable Contract; that reconciliation belongs only to Agent Sync.

The operation is idempotent: repeating it against unchanged Target evidence, Module declarations, installed capabilities, and available releases makes no changes.

## Report

Report the final status of every identified item as **installed**, **updated**, **already available**, **activation required**, **not found**, **rejected**, or **blocked**. Include its Capability Realization Kind, evidence, capability type, selected candidate and source, compatibility evidence, verified project scope and repository location or declaration, included components and permissions, discovery and usability check, and any remaining activation step.
