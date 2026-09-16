---
name: my-interface-agent-sync
description: Realize this adapter itself in `self` mode, or translate every other Agent Module declaration through the active Agent Native's own conventions in `module` mode, certifying synchronization only after complete post-change verification.
argument-hint: "<self | module>"
arguments: [mode]
disable-model-invocation: true
---

# Synchronize the Agent Module

This file is the Claude Code adapter for the portable `agent-sync` Skill Contract and the sole Runtime exception permitted to read Agent Module sources. Resolve and read that Contract through Agent Skill Profile only after explicit Human invocation; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Modes

The invoked mode arrives as `$mode`. Resolve it before any mutation, and when it is empty treat the invocation as mode-less.

- `self` — realize only this adapter from the current `agent-sync` Skill Contract. Reconcile no other declaration, and never report the complete Module as synchronized from a `self` run.
- `module` — realize every other Agent Module declaration. Before any mutation, re-read the current `agent-sync` Skill Contract and confirm this adapter still matches it. When it does not, mutate nothing, report the exact difference, and stop with the instruction to run `/my-interface-agent-sync self` first.
- no mode supplied — mutate nothing. Report both modes and whether this adapter still matches its current Contract.

The stale-adapter check exists because a running instance cannot load a definition it did not start with. Never claim to have executed a Contract this adapter does not currently implement.

## Role

Understand the complete Agent Module, then make the active Agent Native and its Agent Instances conform to it through the Native Runtime's own documented conventions. Materialize missing native resources, reconcile drift where ownership is unambiguous, provision already-selected project Extensions and Integrations, and prove that every Module declaration is usable.

This Skill applies existing Human-owned decisions. It never runs implicitly, at startup, or through another Skill. It does not discover or select new capabilities; it translates the complete Agent Module into the Native Runtime. Use the capability-installation Skill when the Module does not already declare the needed choice.

## Understanding

Establish Interface Understanding from the canonical Interface document, then read and understand the complete Agent Module through its declared structure and sources. Before choosing a realization, establish Native Runtime Understanding from the selected Agent Native's own documentation, supported capabilities, file conventions, invocation rules, mappings, and limitations. Do not use Target Understanding, and do not use Understanding of any Interface Module other than the Agent Module.

Repeat this discovery on every invocation. A Component or mechanism added to the Agent Module after this adapter was written is part of the run automatically.

Treat Principles as mandatory contracts and Profiles as Human-owned desired state. Never modify either. Inspect current project-scoped runtime artifacts and runtime-reported activation state only after deriving the expected profile.

Do not require a project-side realization map or predeclared native path, format, or capability mapping. Derive those from the Native Runtime. If the Native cannot realize a required Module declaration, report the exact unsupported or ambiguous item as `blocked`; never guess from a familiar directory layout. When a declaration carries optional per-Agent-Native details, use only the block matching Claude Code, treat it as an aid that narrows discovery rather than an authority that overrides Claude Code's own mechanism, ignore blocks declared for other Agent Natives, and fall back to Claude Code's own documentation when no matching block exists or the declared detail conflicts with the actual mechanism.

## Reconciliation plan

Build a complete Agent Module inventory before changing runtime state:

| Module declaration or resource | Declared desired state | Native destination or provider | Observed state | Proposed action | Authority or blocker |
| --- | --- | --- | --- | --- | --- |

Include every dynamically discovered Agent Module declaration and resource, including empty categories and already-satisfied items. Classify each action as `no change`, `create`, `update`, `install`, `enable`, `activation required`, `report only`, or `blocked`. Never silently skip an unknown, new, or unsupported declaration, resource, or mechanism; report an unsupported Native realization as blocked.

Use the Native Runtime's documented mechanisms to resolve native destinations, authorized project scope, and verification gates. A Native-provided or explicitly-unused declaration is observed rather than materialized. Explicitly unused means no capability is required and never authorizes removal of an observed undeclared capability.

Resolve ownership before proposing a write. Preserve compatible native values that the Agent Module leaves unspecified. Report an undeclared native capability as unmanaged unless it conflicts with a Principle or selected choice; do not remove or disable it automatically.

## Reconcile

Verify that the selected Agent Native is available and compatible with the complete Agent Module. Derive reconciliation order from current Module relationships and Native capabilities, then process every inventory row while preserving its owner's authority. Add required declared sources and install or enable only entries already selected by Human-owned Profiles and only at project scope. Reload or activate changed capabilities when the Native Runtime supports doing so safely.

A selected desired state is standing project authorization for additive, project-scoped reconciliation of that exact declaration. Still honor runtime permission prompts and stop for Human action when provisioning needs credentials, trust of an external service, broader scope, destructive replacement, an irreversible action, or authority not already expressed by the declaration.

When a required native resource is missing or drifted, construct the smallest implementation that faithfully realizes its owning Principle and declared Profile. Compare an existing adapter's own instruction content against its current Contract, not only its presence or its declared metadata fields. When the Contract no longer matches what the adapter instructs, regenerate that adapter's content rather than classifying it as `no change`. Every non-Sync Skill and Agent Instance must be self-contained or refer only to other synchronized Runtime artifacts; never leave a Runtime instruction that points back into the Agent Module. Never invent content for an explicit empty category.

For each declared capability, resolve its Capability Realization Kind before acting.

- **Prepared** — a declared Skill with an exact matching Markdown file or matching directory under the Skill Profile's declared file convention (`<declared-skill-stable-key>.md` or `<declared-skill-stable-key>/`). Create the selected Runtime's required Skill folder and entrypoint, preserve the prepared source's instruction content and meaning verbatim — for a prepared directory, every file in its tree with internal relative paths intact — and add or adapt only the minimum native metadata needed for discovery and invocation (for Claude Code, YAML frontmatter `name` and `description`). Report a file or directory that does not match exactly one declared Skill instead of installing it by inference, and never rewrite or reinterpret the Human-owned prepared source.
- **Constructed** — an Interface-owned declaration with a portable Contract and no matching prepared file or directory. Build the smallest self-contained native realization from that Contract.
- **Installed** — an externally provided capability declared through Agent Extension or Agent Integration. Observe its actual state, classify it as `no change` when already present and usable, install it additively through the native mechanism named by its owning declaration when absent, and report it as `activation required` or `blocked` when that mechanism is unavailable or demands credentials, external trust, or broader scope. Never build or transfer content for it.

Write only to a project-scoped destination documented by the Native Runtime and authorized by the owning Module declaration. When actual state conflicts with multiple authorities or meaningful Human-authored runtime content would be overwritten, make no write to that resource. Report the conflict and the exact decision needed.

## Verification

After reconciliation, discard pre-change observations, rediscover and re-read the complete Agent Module, independently re-read every native artifact, and query runtime status where supported. Apply every declaration's verification obligation. Audit all non-Sync Runtime instructions and mappings and fail verification if any directs its consumer to enter, read, search, resolve, or use an Agent Module source. A declaration or file presence alone is insufficient.

Verify at least that:

- the selected Agent Native is active, every required Agent Instance is invocable, every required Role and Skill is discoverable by its intended Role, each native Skill invocation control matches its declared Human and coordinator Invocation Policy, and each Skill realized from a portable Contract instructs what that Contract currently requires;
- every Skill materialized from a matched prepared Markdown file or prepared directory exactly preserves that file's or directory tree's instruction content and meaning, including internal relative paths;
- every Custom Command resolves to its declared owner and argument contract;
- effective settings, permissions, rules, and hooks match their owners;
- each selected Extension is installed, project-enabled, and exposes its expected capabilities;
- each selected Integration is project-declared, trusted, connected, and usable, or is truthfully marked as requiring activation; and
- no secret was written to a project artifact.

The second pass must account for every current Agent Module declaration. Repeating this Skill against unchanged declarations and runtime state must produce no mutation; additions or changes anywhere in the Module must be detected on the next run without editing this adapter.

## Boundaries

Operate only on project-scoped Agent Runtime artifacts supported by the selected Agent Native and authorized by the owning Module declarations. Never modify Interface sources, Interface Config, Target code, application dependencies, user- or machine-scoped configuration, credentials, or unrelated Human work. Never discover and adopt a new marketplace, plugin, Skill, MCP server, Agent, or other capability as part of synchronization.

Do not report a capability as synchronized until its required activation and usability checks pass. A pending restart, authentication, trust prompt, missing provider, unsupported project scope, or unavailable runtime is a blocker or `activation required`, not success.

## Report

Report every dynamically discovered Agent Module declaration as `synchronized`, `already synchronized`, `activation required`, `unmanaged`, or `blocked`. For every mutation, identify the owning declaration, native project artifact or provider action, and verification result. List preserved undeclared capabilities separately and state any Human action still required.

State the resolved mode in every report. A `self` run reports only the adapter outcome, and a `module` run blocked by a stale adapter reports that block and the required `self` run, instead of an overall Module status.

Finish with `Agent Module synchronized` only when the complete second pass proves every required declaration and mechanism is realized, active, and usable. Otherwise report `Agent Module not fully synchronized` and enumerate every condition preventing the assurance claim.
