---
name: my-interface-agent-sync
description: Realize this adapter itself in `self` mode, or translate every other Agent Module declaration through the active Agent Native's own conventions in `module` mode, certifying synchronization only after complete post-change verification.
argument-hint: "<self | module>"
arguments: [mode]
disable-model-invocation: true
---

# Synchronize the Agent Module

This file is the Claude Code adapter for the portable `agent-sync` Skill Contract and the sole Runtime exception permitted to read Agent Module sources. Resolve and read that Contract through Agent Skill Profile only after explicit Human invocation; the Contract is authoritative for behavior and this adapter supplies runtime execution details. This adapter never depends on the prior presence of another vendor's Agent Sync adapter.

## Modes

The invoked mode arrives as `$mode`. Resolve it before any mutation, and when it is empty treat the invocation as mode-less. Accept exactly one mode and no capability selection.

- `self` — realize only this adapter from the current `agent-sync` Skill Contract. Reconcile no other declaration, and never report the complete Module as synchronized from a `self` run.
- `module` — realize every other Agent Module declaration. Before any mutation, re-read the current `agent-sync` Skill Contract and confirm this adapter still matches it. When it does not, mutate nothing, report the exact difference, and stop with the instruction to run `/my-interface-agent-sync self` first.
- no mode supplied — mutate nothing. Report both modes and whether this adapter still matches its current Contract.

The stale-adapter check exists because a running instance cannot load a definition it did not start with. Never claim to have executed a Contract this adapter does not currently implement.

## Progress narration

Report the current phase to the Human as this run moves through it; never hold every announcement until the final report. Print one short line at the start of each phase, in `self` mode and in `module` mode alike, and again at the start of every repeated cycle:

- **Understanding** — reading the current Contract, or in `module` mode the complete Agent Module.
- **Comparison** — comparing that Understanding against the installed native artifact.
- **Reconciliation** — writing or rewriting native configuration.
- **Verification** — re-reading the result and proving conformance.

## Self realization

This is the complete workflow for `self` mode. The Module realization, Reconciliation plan, Reconcile, and Verification sections below apply to `module` mode only. Narrate each phase as described in Progress narration above while performing the steps below.

1. Establish Interface Understanding from `.interface/foundation/interface.md`, then establish Native Runtime Understanding of Claude Code's project Skill mechanism: its file location, frontmatter fields, argument substitution, and invocation controls. This governs which frontmatter and native execution detail the adapter must keep.
2. Read `.interface/agent/skill/contracts/agent-sync.md` in full. This is the only Agent Module source a `self` run needs.
3. Read this file, `.claude/skills/my-interface-agent-sync/SKILL.md`, in full.
4. Compare them section by section. Record every difference of these three kinds:
   - this adapter instructs something the Contract no longer requires;
   - this adapter omits something the Contract requires;
   - this adapter states a rule the Contract has changed.
5. When the comparison finds no difference, report `already synchronized` for this adapter and stop. Mutate nothing.
6. When it finds any difference, rewrite this file so every section carries what the Contract currently requires, keeping the frontmatter fields the Runtime needs and the native execution detail the Contract deliberately leaves to the adapter. Write the whole file; do not patch around a difference.
7. Re-read the written file and prove each recorded difference is gone. A difference that survives the rewrite is reported as `blocked`, never as resolved.
8. Report the outcome as a mapping record naming this Contract, this adapter path, and what re-reading proved.

A `self` run that found a difference and left this file unwritten has failed, not succeeded. Report it as failed.

## Module realization

This is the mandatory per-declaration procedure for `module` mode. Run it once for every declaration the Agent Module enumeration produced, one at a time, in the reconciliation order derived below. No declaration is exempt, and none may be skipped because it looks current. Narrate each phase as described in Progress narration above for every declaration processed.

For each declaration:

1. Read every Agent Module source that declaration owns, in full. For a Skill, that is its portable Contract at `.interface/agent/skill/contracts/<name>.md`.
2. Read the installed native artifact that realizes it, in full. For a Skill, that is `.claude/skills/<native-name>/SKILL.md`. When no artifact exists, record `create` and go to step 4.
3. Compare them section by section and record every difference of these three kinds:
   - the artifact instructs something the declaration no longer requires;
   - the artifact omits something the declaration requires;
   - the artifact states a rule the declaration has changed.
4. When no difference is recorded, classify the row `☑️ already synchronized` and go to step 7. When any difference is recorded, rewrite the whole artifact so every section carries what the declaration currently requires, keeping the frontmatter fields the Runtime needs and the native execution detail the declaration deliberately leaves to the adapter. Write the whole file; do not patch around a difference.
5. Re-read the written artifact and prove each recorded difference is gone.
6. Report as `❌ blocked` any difference that survived the rewrite. Never report it as resolved.
7. Record this declaration's mapping row naming the sources read, the artifact path, the Native mechanism and verification gate, and what re-reading proved.

Then run the Verification pass below across the whole Module.

Never claim `no change` or `☑️ already synchronized` for a declaration from anything other than a comparison performed in this run against both files read in full. The artifact's presence, its frontmatter fields, its modification time, its apparent recency, and the absence of a remembered edit are not evidence of conformance. A run that leaves any declaration unread, or classifies one as unchanged without that recorded comparison, has not realized the Module and fails verification: report `Agent Module not fully synchronized` and name every declaration that was not examined this way.

## Role

Understand the complete Agent Module, then make the active Agent Native and its Agent Instances conform to it through the Native Runtime's own documented conventions. Materialize missing native resources, reconcile drift where ownership is unambiguous, provision already-selected project Extensions and Integrations, and prove that every Module declaration is usable.

This Skill applies existing Human-owned decisions. It never runs implicitly, at startup, or through another Skill. It does not discover or select new capabilities; it translates the complete Agent Module into the Native Runtime. When the Module does not already declare a needed capability choice, report that gap and instruct the Human to declare it and run `/my-interface-skill-installer`; never select or adopt a new capability here.

## Trigger

Activate only on direct Human invocation of `/my-interface-agent-sync`, while setting up, repairing, migrating, updating, or auditing an Agent Runtime. No Agent Native, Agent Instance, Skill, coordinator, Hook, startup or resume routine, automation, or model-generated action may invoke, chain, trigger, or simulate this Skill. A Human request to change Agent Module declarations authorizes only that source change; it is not an Agent Sync invocation unless the Human separately invokes this entry point. Treat every Agent Module change as dormant desired state until this explicit synchronization completes — never trigger it from another Skill, a startup or resume routine, or ordinary Interface Understanding.

## Understanding

Establish Interface Understanding from the canonical Interface document, then read and understand the complete Agent Module through its declared Agent Structure and current sources, without limiting the set of declarations read. Consume its Agent Profile, explicit empty categories, portable Skill Contracts, optional prepared Markdown Skill files matched by declared stable key, native project artifacts, and runtime-reported activation state. Before choosing a realization, establish Native Runtime Understanding from the selected Agent Native's own documentation, supported capabilities, file conventions, invocation rules, mappings, and limitations. Do not use Target Understanding, and do not use Understanding of any Interface Module other than the Agent Module.

Discover declarations without a hardcoded component or category list, and repeat this discovery on every invocation. Never rely on a list remembered by the Contract, this adapter, or an earlier run. A Component, category, or mechanism added to the Agent Module after this adapter was written is part of the run automatically.

Treat Principles as mandatory contracts and Profiles as Human-owned desired state. Never modify either. Inspect current project-scoped runtime artifacts and runtime-reported activation state only after deriving the expected profile.

Do not require a project-side realization map or predeclared native path, format, or capability mapping, and never ask the Module to describe the Native Runtime in advance. Derive those from the Native Runtime. If the Native cannot realize a required Module declaration, report the exact unsupported or ambiguous item as `blocked`; never guess from a familiar directory layout. When a declaration carries optional per-Agent-Native details, use only the block matching Claude Code, treat it as an aid that narrows discovery rather than an authority that overrides Claude Code's own mechanism, ignore blocks declared for other Agent Natives, and fall back to Claude Code's own documentation when no matching block exists or the declared detail conflicts with the actual mechanism.

## Reconciliation plan

Build a complete Agent Module inventory before changing runtime state:

| Module declaration or resource | Declared desired state | Native destination or provider | Observed state | Proposed action | Authority or blocker |
| --- | --- | --- | --- | --- | --- |

Include every dynamically discovered Agent Module declaration and resource, including empty categories and already-satisfied items. Classify each action as `no change`, `create`, `update`, `install`, `enable`, `activation required`, `report only`, or `blocked`. Never silently skip an unknown, new, or unsupported Component, category, declaration, resource, or mechanism: reconcile it when Claude Code supplies an authorized mapping; otherwise report it as blocked, naming the missing mapping or capability.

Use the Native Runtime's documented mechanisms to resolve native destinations, authorized project scope, and verification gates. A Native-provided or explicitly-unused declaration is observed rather than materialized. Explicitly unused means no capability is required and never authorizes removal of an observed undeclared capability.

Resolve ownership before proposing a write. Preserve compatible native values that the Agent Module leaves unspecified. Report an undeclared native capability as unmanaged unless it conflicts with a Principle or selected choice; do not remove or disable it automatically.

## Reconcile

Verify first that the selected Agent Native is available and compatible with the complete Agent Module. Derive dependency-safe reconciliation order from current Module relationships and Native capabilities, then process every inventory row while preserving its owner's authority. Add required declared sources and install or enable only entries already selected by Human-owned Profiles and only at project scope. Reload or activate changed capabilities when the Native Runtime supports doing so safely. Block an affected item on incompatible Runtime, ambiguous ownership, unsupported project scope, destructive conflict, missing provider, or unavailable authority, and mark pending restart, authentication, or trust as `activation required`; independent items continue reconciling when their dependencies permit.

A selected desired state is standing project authorization only for exact additive, project-scoped reconciliation of that declaration. Still honor runtime permission prompts and stop for Human action when provisioning needs credentials, trust of an external service, broader scope, destructive replacement, an irreversible action, or authority not already expressed by the declaration.

Process each row through the Module realization procedure above; it is the only permitted way to reach a per-declaration outcome, and nothing in this section relaxes it. When a required native resource is missing or drifted, construct the smallest self-contained native realization that completely realizes its portable Contract, owning Principle, and declared Profile without requiring any later Agent Module read. Compare an existing artifact's own instruction content against its current Contract, not only its presence or metadata, and regenerate the content when they no longer match. Every non-Sync Skill and Agent Instance must be self-contained or refer only to other synchronized Runtime artifacts; never leave a Runtime instruction that points back into the Agent Module. Never invent content for an explicit empty category.

Realize only **Constructed** Skills: an Interface-owned Skill defined by a portable Contract is built from that Contract into the smallest self-contained native Claude Code project Skill.

A **Prepared** Skill and an **Installed** Skill are outside this operation. Do not create, transfer, install, rewrite, or remove either one; the Skill Installer operation owns both. Observe them only so the mapping table can state their current Runtime condition. This restriction applies to Skills; already-selected Extensions and Integrations are still provisioned and verified under the rules above.

When any synchronized Runtime instruction, mapping, or Skill realization directs its consumer to enter, read, search, resolve, or use an Agent Module source, treat this as required reconciliation, not merely a verification failure: replace that routing with the corresponding synchronized Runtime Rule, capability, Agent Instance, or Skill realization so no non-Sync consumer depends on an Agent Module source.

Write only to a project-scoped destination documented by the Native Runtime and authorized by the owning Module declaration. When actual state conflicts with multiple authorities or meaningful Human-authored runtime content would be overwritten, or ownership is ambiguous, make no write to that resource. Report the conflict and the exact decision needed.

## Verification

After reconciliation, discard pre-change observations and perform a second complete pass from the canonical Agent Structure: rediscover and re-read the complete Agent Module, independently re-read every native artifact, and query runtime status where supported. Apply every declaration's verification obligation. Audit all non-Sync Runtime instructions and mappings and fail verification if any directs its consumer to enter, read, search, resolve, or use an Agent Module source. A declaration or file presence alone is insufficient, and a write that succeeded is not itself conformance.

Verify at least that:

- the selected Agent Native is active, every required Agent Instance Definition is instantiable, and Role and capability assignments are correct;
- every required Skill is discoverable by its intended Role and self-contained, its native invocation control matches its declared Human and coordinator Invocation Policy, and each Skill realized from a portable Contract instructs what that Contract currently requires;
- every Custom Command resolves to its declared owner and argument contract;
- effective settings, permissions, rules, hooks, and their enforcement match their owners;
- each selected Extension is installed, project-enabled, and exposes its expected capabilities;
- each selected Integration is project-declared, trusted, connected, and usable, or is truthfully marked as requiring activation;
- each Prepared and Installed Skill's current Runtime condition is observed and reported, without modification; and
- no secret was written to a project artifact.

The second pass must account for every current Agent Module declaration. Any blocked, missing, conflicting, inactive, unsupported, or unverified required item prevents the success claim, even when every other declaration passes.

When this pass finds a required item unrealized, incompletely realized, or unverified for a reason other than a genuine Stopping Condition, do not stop at reporting it. Return to Understanding, reconcile that item again through Module realization and Reconcile above, and perform a new complete Verification pass, narrating each phase again as you go. Repeat this Understanding-Reconcile-Verify cycle within the same invocation until every required item is realized and verified, or a cycle changes nothing from the previous cycle's outcome — the same items realized, the same items blocked for the same reason. A cycle that only reproduces its own last outcome has converged, not stalled; report that as the final result rather than repeating again.

Repeating this Skill against unchanged declarations and runtime state must produce no mutation; a newly added or changed declaration, Principle, Profile, Contract, resource, category, or mechanism anywhere in the Module must be detected and reconciled on the next run without editing this adapter.

## Boundaries

Operate only on project-scoped Agent Runtime artifacts selected by the Agent Native and authorized by the owning Module declarations. Provision only exact Human-selected declarations. Never modify Interface sources, Interface Config, Target code, application dependencies, user- or machine-scoped configuration, credentials, or unrelated Human work. Never discover and adopt a new marketplace, plugin, Skill, MCP server, Agent, or other capability as part of synchronization.

Do not report a capability as synchronized until its required activation and usability checks pass. A pending restart, authentication, trust prompt, missing provider, unsupported project scope, or unavailable runtime is a blocker or `activation required`, not success.

## Report

Open a `module` report with one mapping table covering every dynamically discovered Agent Module declaration, one row each, in the order they were reconciled:

| | Agent Module declaration | Realized as | Native artifact | Verified |
|---|---|---|---|---|
| ✅ | `agent/skill/contracts/<name>.md` | Claude Code project Skill | `.claude/skills/<native-name>/SKILL.md` | re-read; instructs what the Contract requires |
| ⚠️ | `<declaration>` | `<mechanism>` | `<path or provider>` | activation required: `<what the Human must do>` |
| 🔍 | — | observed only | `<path>` | unmanaged: present in the Runtime, declared nowhere |
| ❌ | `<declaration>` | `<mechanism>` | `<path or provider>` | blocked: `<exact reason>` |

Use `✅` for `synchronized`, `☑️` for `already synchronized`, `⚠️` for `activation required`, `🔍` for `unmanaged`, and `❌` for `blocked`. Every row names the Module declaration it came from, the Native mechanism, and the artifact it was verified against; a row with no named artifact makes no claim. The Verified column reports what re-reading that artifact in the second pass proved, never that a write succeeded.

After the table, detail every non-`✅` row: what it needs, who must act, and what it prevents. List preserved undeclared capabilities separately and state any Human activation step still required.

State the resolved mode in every report. A `self` run, a `module` run blocked by a stale adapter, and a mode-less invocation each report the resolved mode and its outcome — for a stale block, the exact difference and the required `self` run — plus the declarations left unreconciled, instead of an overall Module status.

Finish a complete `module` run with `Agent Module synchronized` only when the complete second pass proves every required declaration and mechanism is realized, active, and usable. Otherwise report `Agent Module not fully synchronized` and enumerate every condition preventing the assurance claim.
