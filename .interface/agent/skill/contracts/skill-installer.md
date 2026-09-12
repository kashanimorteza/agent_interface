# skill-installer Skill Contract

## Purpose

Discover and provision additional Agent capabilities through an explicit, auditable Human decision.

## Responsibility

Derive capability needs from current Target and Agent evidence, discover compatible project-scoped candidates, preview provenance and impact, provision only approved candidates, and verify Activation. It manages Agent capabilities, never application dependencies or Target implementation.

## Trigger

Activate explicitly when the Human requests capability discovery or when a required capability is absent and no Human-owned selection already identifies what Agent Sync should realize.

## Inputs

Accept a requested capability need or derive needs from current Target technologies, frameworks, protocols, services, data sources, activities, Preferences, dependencies, and installed Agent capabilities. An empty explicit request performs complete relevant discovery from current evidence.

## Outputs

Produce an evidence-backed need inventory, candidate comparison, exact provisioning preview, approval request, and final status for every need as installed, updated, already available, activation required, not found, rejected, or blocked.

## Required Understanding

Establish Interface Understanding and Target Understanding. Read applicable Agent and Developer Components, selected defaults, manifests, lockfiles, runtime versions, implementation evidence, and current capability status.

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
