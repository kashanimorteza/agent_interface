# skill-installer Skill Contract

## Purpose

Discover and provision additional Agent capabilities through an explicit, auditable Human decision.

## Responsibility

Derive capability needs from current Target and synchronized Runtime evidence, discover compatible project-scoped candidates, preview provenance and impact, provision only approved candidates, and verify Activation. It manages Runtime capabilities, never application dependencies, Target implementation, or Agent Module declarations. Already Human-declared Installed capabilities in the Agent Module are Agent Sync's responsibility to provision and verify during synchronization; Skill Installer instead discovers and provisions capability needs that are not yet declared.

## Trigger

Activate explicitly when the Human requests capability discovery or when a required capability is absent from the synchronized Runtime. Because Agent Module sources are unreadable here, an absent capability may still be an already-declared capability awaiting synchronization; report that possibility together with the need and let the Human choose between explicit Agent Sync and provisioning through this Skill, rather than assuming the need is undeclared.

## Inputs

Accept a requested capability need or derive needs from current Target technologies, frameworks, protocols, services, data sources, activities, Preferences, dependencies, and installed Agent capabilities. An empty explicit request performs complete relevant discovery from current evidence.

## Outputs

Produce an evidence-backed need inventory, candidate comparison, exact provisioning preview, approval request, and final status for every need as installed, updated, already available, activation required, not found, rejected, or blocked.

## Required Understanding

Establish Interface Understanding and Target Understanding. Read applicable Implementation Components, synchronized Runtime capability state, selected defaults, manifests, lockfiles, runtime versions, implementation evidence, and current capability status. Never read Agent Module sources; a candidate that should become part of the portable Agent definition is reported for Human declaration and later explicit Agent Sync.

## Authority

Discovery is read-only. After explicit approval, provision only named candidates at project scope through supported Agent capability mechanisms. Never change application dependencies, Target code, Interface sources, credentials, or user- or machine-scoped state.

## Workflow Invariants

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
