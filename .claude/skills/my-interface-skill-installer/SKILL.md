---
name: my-interface-skill-installer
description: Discover and, after human approval, install project-scoped Agent capabilities relevant to the current Target, including Skills, plugins, MCP integrations, and equivalent supported extensions. Never changes application dependencies or code.
disable-model-invocation: true
---

# Install Agent capabilities

## Role

Identify where the current Target could benefit from an additional Agent capability, search the environment's supported sources for compatible options, and present the findings for human approval before installing anything.

This operation may consider Skills, plugins, MCP integrations, agents, or another extension type supported by the active Agent environment. It equips the Agent; it does not install application runtime dependencies or develop the Target.

Read the shared Agent Interface rules at the start of the operation and follow them throughout, including their project-scope requirement.

## Workflow

### Understand

Establish Interface Understanding from the canonical Interface document, then establish Target Understanding from the Target Technical Definition it locates. Read every applicable Principle and Preference, including selected defaults and applicable alternatives. Use dependency manifests, lockfiles, runtime-version files, existing implementation, and installed Agent capabilities as supporting evidence.

Derive capability needs from current evidence on every run. A technology, framework, platform, protocol, service, data source, development activity, or preferred default may indicate that a relevant Agent capability exists. Do not keep a hardcoded technology or capability list in this Skill.

### Identify

Before searching, turn the current Understanding into a visible inventory of items that may have a useful Skill, plugin, MCP integration, agent, or equivalent extension:

| Item | Evidence | Why an Agent capability may exist | Capability types to search |
| --- | --- | --- | --- |

Every row must cite the Target, Principle, Preference, selected default, dependency, configuration, or implementation evidence that produced it. Keep distinct needs separate even when one candidate may later satisfy several of them. This inventory defines what Discovery searches; it does not authorize installation.

### Discover

For each identified item:

1. Check whether an adequate capability is already available to the Agent.
2. Search every relevant discovery route supported by the current environment for Skills, plugins, MCP integrations, agents, or equivalent extensions.
3. Verify each candidate by its declared purpose, source, included components, permissions, installation scope, and compatibility with the detected technology and version.
4. Prefer authoritative sources: an official source first, then a source maintained by the relevant technology, then a trusted third party.
5. Reject duplicates and options that cannot satisfy the shared project-scope rule.
6. Record a negative result only after the applicable discovery routes have been checked. State where the search was performed instead of claiming broadly that no capability exists.

Discovery is read-only. Adding a catalog, connecting an external service, or changing an installation source is a separate external change and requires approval.

### Preview

After Discovery and before installing or updating anything, present one result row for every identified item:

| Item | Evidence | Capability type | Candidate | Source | Compatibility | Project scope | Included components and permissions | Search result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use **not found** for a need with no verified candidate and identify the discovery routes checked. Use **already available** when the current Agent already has an adequate capability.

After the table, state exactly which candidates are proposed for installation or update and ask the human to approve or reject them. Do not install, update, connect, or add a source before receiving that decision.

### Install

Install or update only the candidates explicitly approved by the human and only through a project-scoped mechanism allowed by the shared rules. Preserve rejected and already adequate capabilities unchanged.

Verify the installed capability, its project location or declaration, its included components and permissions, and its activation state. A capability is not `installed` for reporting purposes until the active Agent can discover and use it in this project:

- verify that an installed Skill is discoverable;
- verify that an installed plugin is project-enabled and its contributed capabilities are loaded; and
- verify that an installed MCP integration is project-declared, trusted, connected, and exposes its expected capabilities.

Complete a supported activation or reload during the installation when possible. When human trust, authentication, restart, or another external activation step remains, report `activation required` and the exact remaining action instead of reporting `installed`. Never place credentials or tokens in a repository-tracked declaration.

If project-scoped installation is unavailable, report the candidate as blocked instead of installing it at user or machine scope.

## Boundaries

Perform only Agent-capability discovery and approved project-scoped installation. Do not perform an Interface Operation or change Interface sources, Target application code, architecture, manifests, lockfiles, or runtime dependencies. Do not remove a compatible capability or install a duplicate.

The operation is idempotent: repeating it against unchanged Target evidence, installed capabilities, and available releases makes no changes.

## Report

Report the final status of every identified item as **installed**, **updated**, **already available**, **activation required**, **not found**, **rejected**, or **blocked**. Include its evidence, capability type, selected candidate and source, compatibility evidence, verified project scope and repository location or declaration, included components and permissions, discovery and usability check, and any remaining activation step.
