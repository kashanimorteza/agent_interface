# skill-installer Skill Contract

## Purpose

Materialize the Prepared and Installed capabilities the Agent Module declares, and discover and provision additional ones, always through an explicit, auditable Human decision.

## Responsibility

Derive capability needs from current Target and synchronized Runtime evidence, discover compatible project-scoped candidates, preview provenance and impact, provision only approved candidates, and verify Activation. It manages Runtime capabilities, never application dependencies, Target implementation, or Agent Module declarations. It owns every capability the Module declares as Prepared or Installed: Prepared content is transferred into the Runtime unchanged, and an Installed capability is provisioned through its owning provider declaration. Agent Sync builds only Constructed Skills and materializes neither kind.

## Trigger

Activate explicitly when the Human requests capability discovery, when a capability the Agent Module declares as Prepared or Installed is not present and usable in the Runtime, or when a required capability is absent from the synchronized Runtime. Never activate through another Skill, coordinator, automation, or model-generated action.

## Inputs

Accept a requested capability need or derive needs from current Target technologies, frameworks, protocols, services, data sources, activities, Preferences, dependencies, and installed Agent capabilities. An empty explicit request performs complete relevant discovery from current evidence.

## Outputs

Produce an evidence-backed need inventory, candidate comparison, exact provisioning preview, approval request, and final status for every need as installed, updated, already available, activation required, not found, rejected, or blocked.

## Required Understanding

Establish Interface Understanding and Target Understanding. Read the complete Agent Module through the exception that permits entry into its sources, so every declared capability and its Capability Realization Kind is known. Read applicable Implementation Components, synchronized Runtime capability state, selected defaults, manifests, lockfiles, runtime versions, implementation evidence, and current capability status. Never modify an Agent Module source; a candidate that should become part of the portable Agent definition is reported for Human declaration rather than written here.

## Authority

Discovery is read-only. After explicit approval, transfer declared Prepared content and provision only named candidates at project scope through supported Agent capability mechanisms. Never change application dependencies, Target code, Interface sources, credentials, or user- or machine-scoped state.

## Workflow Invariants

- Resolve every declared capability's Capability Realization Kind. A Prepared capability is transferred into the selected Runtime unchanged, preserving every file of its source tree and its internal relative paths, adapting only the native metadata required for discovery. An Installed capability is provisioned through the native mechanism its owning provider declaration names. A Constructed capability is never materialized here; it belongs to Agent Sync.
- Treat capability as covering Skills, plugins, MCP servers, and every other provider-supplied Agent capability the selected Runtime supports.
- After the project's packages are installed, use the skill-provisioning mechanism the applicable Language Item declares when one exists, so capabilities bundled by installed packages become discoverable. The absence of a declaration never means no mechanism exists, and a declared mechanism never replaces the environment's own current capability.
- Enumerate distinct capability needs with exact evidence before search.
- Check current availability before discovery and search every relevant route supported by the active Runtime.
- Verify candidate purpose, source, included components, permissions, dependencies, project scope, and version compatibility.
- Prefer an official source, then the technology maintainer, then a trusted third party.
- Reject duplicates and candidates without supported project scope.
- State the routes checked for a negative result.
- Adding a marketplace, trusting or connecting a service, or changing an installation source is provisioning and requires approval.
- Preview one result for every identified need and ask approval for exact candidates before any mutation.
- Verify post-install discovery, enablement, connection, expected capabilities, and usability. File presence or an installation receipt is insufficient.

## Verification

Prove the installed capability is project-declared, active, discoverable, and usable by its intended Role. Report pending authentication, trust, reload, restart, or external activation instead of success.

## Idempotency

Against unchanged evidence and releases, preserve adequate capabilities and perform no duplicate provisioning.

## Stopping Conditions

Stop before provisioning without explicit candidate approval. Block candidates that are incompatible, untrusted, duplicate, unavailable at project scope, or require unauthorized access. Pause for Human trust, authentication, or another external activation step.

## Runtime Realization

A native adapter discovers current provider commands and catalogs through Runtime mappings rather than hardcoding vendors, and presents both the need inventory and candidate-result inventory before installation.
