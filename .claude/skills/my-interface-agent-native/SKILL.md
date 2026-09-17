---
name: my-interface-agent-native
description: The Agent Native configuring itself from the Agent Module. Mode 1 realizes this adapter from its Contract, mode 2 realizes every other Agent Module declaration in Claude Code, mode 3 discovers and, after Human approval, installs Prepared and Installed capabilities. Certifies synchronization only after complete post-change verification.
argument-hint: "<1=sync self | 2=sync component | 3=install>"
arguments: [mode]
disable-model-invocation: true
metadata:
  contract: ".interface/agent/skill/contracts/agent-native.md"
---

# Agent Native — sync self · sync component · install

This file is the Claude Code adapter for the portable `agent-native` Skill Contract and the sole Runtime artifact permitted to read Agent Module sources, only within the prompt created by the Human's direct invocation. Resolve and read that Contract through the Agent Skill Preferences after invocation; the Contract is authoritative for behavior and this adapter supplies only Claude Code execution details. It never depends on the prior presence of another vendor's adapter. In Interface prose, *Agent Native* still means the core operational Agent supplied by the Runtime — the one running this Skill; `agent-native` is only this Skill's name.

## Trigger

Activate only on direct Human invocation of `/my-interface-agent-native`, while setting up, repairing, migrating, updating, or auditing an Agent Runtime — or, in mode 3, when the Human requests capability discovery or a declared Prepared or Installed capability is absent from the Runtime. No Agent Native, Agent Instance, Skill, coordinator, Hook, startup or resume routine, automation, or model-generated action may invoke, chain, trigger, or simulate this Skill. A Human request to change Agent Module declarations authorizes only that source change; it is not an invocation of this Skill. Every Agent Module change is dormant desired state until this explicit synchronization completes.

## Modes

The invoked mode arrives as `$mode`. Resolve it before any mutation; accept exactly one mode, and no capability selection in modes 1 and 2.

- `1` (sync self) — run the Realization procedure below on this adapter only — this file and the helper beside it — against the current `agent-native` Contract. Reconcile nothing else, and never report the complete Module as synchronized from a mode 1 run.
- `2` (sync component) — first re-read the current `agent-native` Contract and this file in full and compare them; if they differ, mutate nothing, report the exact difference, and stop with the instruction to run `/my-interface-agent-native 1` first. Otherwise run the Realization procedure on every other declaration, then Verification.
- `3` (install) — run the Install procedure at the end of this file; it reconciles no Constructed Skill and never writes this adapter.
- no mode — mutate nothing; report all three modes and whether this adapter still matches its current Contract.

A running instance cannot load a definition it did not start with, so never claim to have executed a Contract this adapter does not currently implement.

## Progress narration

Print one short line to the Human at the start of each phase — **Understanding**, **Comparison**, **Reconciliation**, **Verification** — in every mode and again at the start of every repeated cycle. Never hold announcements for the final report.

## Understanding

Establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, then read the complete Agent Module beginning with the Agent Module Guide at `.interface/agent/guide.md`, which carries the Agent Structure, and continuing through every current source that Structure names: each Component's `principles.md` and `preferences.yaml`, every Skill Contract under `skill/contracts/`, every Personality definition under `personality/definitions/`, and the prepared-file directory `skill/files/` when present. Discover every declaration, resource, and explicit empty category dynamically on every invocation — never from a hardcoded list or one remembered by the Contract, this adapter, or an earlier run. Consume the Agent Preferences, native project artifacts, and runtime-reported activation state. A matched prepared file only identifies that Skill as Prepared rather than Constructed; an unmatched one is reported and never installed by inference. Treat Principles as mandatory contracts and Preferences as Human-owned desired state; never modify either. Use no Target Understanding (mode 3 excepted) and no other Interface Module.

Before choosing any realization, establish Native Runtime Understanding from Claude Code's own documentation: project Skills (`.claude/skills/<name>/SKILL.md`, frontmatter, `$name` argument substitution, `disable-model-invocation`, `user-invocable`), Rules (`.claude/rules/*.md`), agents (`.claude/agents/*.md`), `settings.json` (permissions allow/ask/deny, hooks by event and matcher, enabled plugins and marketplaces, output style), MCP declarations, output-style files, and what each of these loads only at session start. Never require a project-side realization map or predeclared native path, and never infer a destination from a familiar layout. When a declaration carries a `settings.native.claude` block, use it as an aid that narrows discovery — a suggested mechanism, event, matcher, or probe — never as an authority over Claude Code's own mechanism; ignore blocks declared for other Natives; fall back to Claude Code's documentation when no block exists or the block conflicts with the actual mechanism. If Claude Code cannot realize a required declaration exactly, realize it through the nearest Claude Code mechanism, classify it `approximated` with the exact difference stated, and continue; classify it `blocked` only when no Claude Code equivalent exists or a stopping condition applies. The run never stops because one declaration is approximated or blocked.

## Realization procedure

This is the only permitted way to reach a per-declaration outcome. Apply it to one declaration at a time, none exempted, no shortcut for one that looks current:

1. Read every Agent Module source the declaration owns, in full. For a Skill that is its Contract at `.interface/agent/skill/contracts/<name>.md`; for a Rule, Agent Instance, guarantee, Extension, Integration, or setting it is the owning `preferences.yaml` entry and the Principles that govern it.
2. Read the installed native artifact in full. For a Skill that is `.claude/skills/<native-name>/SKILL.md`; for a Rule `.claude/rules/<name>.md`; for an Agent Instance `.claude/agents/<name>.md`; for a guarantee, permission, plugin, or output style the relevant part of `.claude/settings.json` and any hook script. If none exists, record `create` and go to step 4.
3. Compare section by section and record every difference of three kinds: the artifact instructs something the declaration no longer requires; omits something it requires; or states a rule it has changed.
4. No difference → classify `already synchronized` and go to step 7. Any difference → rewrite the whole artifact so every section carries what the declaration currently requires, keeping the frontmatter or keys Claude Code needs and the native detail the declaration leaves to the adapter; never patch around a difference and never invent content for an empty category.
5. Re-read the written artifact and prove each recorded difference is gone.
6. Report `blocked` any difference that survives; never report it resolved.
7. Record the fingerprint of every source read for this declaration — in the artifact's frontmatter `metadata` when it has one, otherwise in the synchronization record only (see Synchronization record).
8. Record the mapping row: sources read, artifact path, Native mechanism, verification gate, and what re-reading proved.

Claim `no change` or `already synchronized` only from this comparison with both files read in full. Presence, frontmatter, modification time, apparent recency, and the absence of a remembered edit are never evidence of conformance. A changed source fingerprint proves staleness and forces step 4; an unchanged one proves nothing. Recorded fingerprints may be consulted first so the report names provably stale artifacts; they never skip, defer, or shorten any declaration's procedure. A mode 1 run that found a difference and left this file unwritten has failed. A run that leaves any declaration unread, or classifies one unchanged without this comparison, reports `Agent Module not fully synchronized` and names every unexamined declaration.

## Module reconciliation (mode 2)

Before changing runtime state, build one inventory row per dynamically discovered declaration and resource, including empty and already-satisfied categories, and classify each as `no change`, `create`, `update`, `install`, `enable`, `approximate`, `activation required`, `report only`, or `blocked`. Never silently skip an unknown, new, or unsupported item: reconcile it when Claude Code supplies an authorized mapping, otherwise report it blocked with the missing mapping.

Verify first that Claude Code is available and compatible with the complete Module, derive dependency-safe order from Module relationships (Runtime and Permission before Skills and Rules; Personality before the Skills that name one), resolve ownership before every write, and preserve each owner's authority throughout. Then process every row through the Realization procedure. Add required declared sources and install or enable only entries already selected by Human-owned Preferences, at project scope only; reload or activate changed capabilities when Claude Code supports doing so safely. Realize only **Constructed** Skills — an Interface-owned Skill built from its portable Contract into the smallest self-contained project Skill; when a core Skill's Preferences name a `personality`, carry that Personality's definition into the native Skill. **Prepared** and **Installed** Skills belong to mode 3: observe and report their condition here, never create, transfer, install, rewrite, or remove them. Already-selected plugins, marketplaces, and MCP declarations from Connection Preferences are still provisioned and verified.

Explicit Human invocation is standing authorization for every additive, project-scoped write this adapter owns, including rewriting an existing Skill, Rule, setting, agent, or hook: do not pause to ask. Stop for Human action only for credentials, external trust, broader scope, an irreversible action, authority the declaration does not express, or destructive replacement of unrelated or ambiguously-owned Human content — in that last case make no write to that resource and report the exact decision needed. Independent items continue reconciling when their dependencies permit. A Native-provided or explicitly unused declaration is observation-only: explicitly unused means no capability is required and never authorizes removing an observed undeclared capability. Preserve compatible native values the Module leaves unspecified and report an undeclared capability as `unmanaged`; when one conflicts with a Principle or selected choice, report the exact conflict instead. Never remove either automatically. When any synchronized non-Sync instruction routes its consumer into an Agent Module source, replace that routing with the corresponding synchronized Rule, capability, Agent Instance, or Skill realization; every non-Sync artifact must be self-contained or refer only to other synchronized artifacts.

## Verification (mode 2)

After reconciliation, discard pre-change observations and perform a second complete pass: rediscover and re-read the complete Agent Module, independently re-read every native artifact, and query runtime status where supported. Prove that the Agent Native is active; every required Agent Instance is instantiable with correct Role and capability assignments; every required Skill is discoverable by its Role, self-contained, has invocation controls matching its declared Human and coordinator Invocation Policy, and instructs what its Contract currently requires; every Command resolves to its owner and argument contract; effective settings, permissions, rules, hooks, and enforcement match their owners; each selected plugin is installed and project-enabled; each selected MCP server or service is trusted and usable or truthfully marked `activation required`; each Prepared and Installed Skill's condition is observed without modification; no non-Sync instruction directs its consumer into an Agent Module source; and no secret was written to a project artifact. For every enforced guarantee in the Permission Preferences, run the behavioral probe declared beside it under `native.claude.probe` — perform the action, observe whether Claude Code blocked or permitted it as expected — and record the observation in that guarantee's row; a failed probe makes the guarantee `blocked`, whatever its hook or setting looks like. An approximated item passes its gate when re-reading proves the nearest realization is in place and its stated difference is still accurate. A write that succeeded is not itself conformance; any blocked, missing, conflicting, inactive, unsupported, or unverified required item prevents the success claim, even when every other declaration passes.

When this pass finds a required item unrealized or unverified for a reason other than a genuine stopping condition, return to Understanding, reconcile it again, and run a new complete Verification pass, narrating each phase. Repeat until every required item passes or a cycle reproduces the previous cycle's outcome exactly — that is convergence, reported as final. Repeating this Skill against unchanged declarations and runtime state must produce no mutation; any new or changed Module source is detected and reconciled on the next run without editing this adapter.

## Synchronization record

`scripts/check-stale.py` beside this file is the bounded fingerprint helper: it hashes sources, records fingerprints in frontmatter `metadata` (`stamp`, for Skills) or in the record only (`record`, for every other declaration), and reads or writes `.claude/interface-sync.yaml`. It never compares instruction content and never decides conformance. Step 7 of the Realization procedure is `python3 .claude/skills/my-interface-agent-native/scripts/check-stale.py stamp --mode <mode> --status <status this run proved for it> --note "<evidence>" --only <native-name>` for a Skill, or `... record --mode <mode> --declaration <source#key> --artifact <path> --status <status> --note "<evidence>"` for anything else, so the record holds one entry per declaration: source, fingerprint, artifact, status, mode, and time. The last helper call of a run also passes `--result "<overall result>"`. `check` re-hashes the sources and reports provable staleness; it may run first so the report names stale artifacts, never as a substitute for, or a shortcut through, the Realization procedure.

## Stopping conditions

Block the affected item — and only that item — on an incompatible Runtime, ambiguous ownership, unsupported project scope, destructive conflict, missing provider, or unavailable authority, naming the exact reason. Mark a pending restart, authentication, or trust prompt `activation required`. Independent items continue when their dependencies permit. Stop a mode 2 run before any mutation when this adapter no longer matches its Contract, and report that a mode 1 run is required first.

## Boundaries

Write only to a project-scoped destination that Claude Code documents for the realized declaration and that the owning declaration authorizes, never one inferred from a familiar directory layout; `.claude/interface-sync.yaml`, the Skill metadata stamp, and the helper are such artifacts owned by this Skill. Never modify Interface sources, Config, Target code, application dependencies, user- or machine-scoped configuration, credentials, or unrelated Human work. In modes 1 and 2 never discover or adopt a new marketplace, plugin, Skill, MCP server, Agent, or capability; when the Module lacks a needed choice, report the gap and instruct the Human to declare it and run `/my-interface-agent-native 3`. A pending restart, authentication, trust prompt, missing provider, or unavailable runtime is `activation required` or `blocked`, never success.

## Report (modes 1 and 2)

State the resolved mode in every report. Whenever this run wrote any native artifact — a mode 1 rewrite of this file or any `create`, `update`, `install`, or `enable` in mode 2 — classify each written artifact `activation required` and place this notice once, prominently, visually set apart from the surrounding text as a box, outside the table, even when everything else succeeded:

> ⚠️ **Restart Claude Code before relying on this.** This session is still running the previous definition of every native artifact this run wrote — Skills, Rules, settings, hooks, agents, and enabled capabilities alike. Fully exit this Claude Code session and start a new one — reopening or continuing this conversation is not enough. Do this before invoking `/my-interface-agent-native` again or trusting any rewritten artifact's behavior.

Never report a written artifact as usable in the current session while this notice is outstanding.

Open a mode 2 report with one mapping table, one row per declaration in reconciliation order; a row with no named artifact makes no claim, and the last column reports what re-reading proved — and for a guarantee, what its probe observed — never that a write succeeded:

| | Agent Module declaration | Realized as | Native artifact | Verified |
|---|---|---|---|---|
| ✅ | `agent/skill/contracts/<name>.md` | Claude Code project Skill | `.claude/skills/<native-name>/SKILL.md` | re-read; instructs what the Contract requires |
| ✅ | `agent/permission/preferences.yaml#enforced.<guarantee>` | Claude Code hook | `.claude/settings.json` + `.claude/hooks/<file>` | re-read; probe: `<action>` → `<observed>` (matched) |
| 🟡 | `<declaration>` | `<nearest Claude Code mechanism>` | `<path>` | approximated: `<exact difference from the declaration>` |
| ⚠️ | `<declaration>` | `<mechanism>` | `<path or provider>` | activation required: `<Human action>` |
| 🔍 | — | observed only | `<path>` | unmanaged: present, declared nowhere |
| ❌ | `<declaration>` | `<mechanism>` | `<path or provider>` | blocked: `<exact reason>` |

`✅` synchronized · `☑️` already synchronized · `🟡` approximated · `⚠️` activation required · `🔍` unmanaged · `❌` blocked. After the table, detail every non-`✅` row (what it needs, who acts, what it prevents), list preserved unmanaged capabilities, and state any Human activation step. A mode 1 run, a stale-adapter block, or a mode-less invocation reports its mode, its outcome (for a stale block: the exact difference and the required mode 1 run), and the declarations left unreconciled — never an overall Module status. Finish a complete mode 2 run with `Agent Module synchronized` only when the second pass proves every required declaration realized, active, and usable, listing every approximation beneath it so the Human can judge each one; otherwise `Agent Module not fully synchronized` with every preventing condition enumerated.

## Mode 3 — install

This mode is the former `my-interface-skill-installer` adapter, merged here on 2026-09-17 and kept whole. It runs only when `$mode` is `3`, reads the Agent Module through the same grant as the sync modes, and never reconciles a Constructed Skill or touches this adapter.

This file is the self-contained Claude Code realization of the portable `agent-native` (mode 3) contract synchronized by Agent Sync. Together with Agent Sync, it is one of the two Runtime exceptions permitted to read Agent Module sources, and only strictly within the exact prompt created by this Skill's own direct Human invocation. Follow this adapter and synchronized Runtime rules.

### Role

Materialize every capability the Agent Module declares as Prepared or Installed, and separately discover and provision additional Agent capabilities the current Target could use — always through an explicit, auditable Human decision.

This operation may consider Skills, plugins, MCP integrations, agents, or another extension type supported by the active Agent environment. It equips the Agent; it does not install application runtime dependencies or develop the Target. Agent Sync builds only Constructed Skills — those defined completely by a portable Skill Contract — and never materializes a Prepared or Installed capability. This Skill owns both of those kinds instead: it transfers a declared Prepared capability's content into the Runtime unchanged, and it provisions a declared Installed capability through its owning provider declaration. It also discovers and, after approval, provisions capability needs the Module does not yet declare.

Read the shared Agent Interface rules at the start of the operation and follow them throughout, including their project-scope requirement.

### Trigger

Activate only through explicit Human invocation of `/my-interface-agent-native 3` — when the Human requests capability discovery, when a capability the Agent Module declares as Prepared or Installed is not present and usable in the Runtime, or when a required capability is absent from the synchronized Runtime. No Agent Native, Agent Instance, Skill, coordinator, Hook, startup or resume routine, automation, or model-generated action may invoke, chain, trigger, or simulate this Skill.

### Workflow

### Understand

Establish Interface Understanding from the canonical Interface document, then establish Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Read every applicable Implementation Principle and Preference together with synchronized Runtime capabilities and rules, including selected defaults and applicable alternatives. Use dependency manifests, lockfiles, runtime-version files, existing implementation, and installed Agent capabilities as supporting evidence.

Read the complete Agent Module — every Component's Principles and Preferences, every Skill Contract, and the prepared-file directory at `.interface/agent/skill/files/` — so every declared capability and its Capability Realization Kind (Constructed, Prepared, or Installed) is known. This read is authorized only inside this Skill's own direct Human invocation and is never carried into, or repeated from, another operation. Never modify an Agent Module source: a candidate that should become part of the portable Agent definition is reported for Human declaration rather than written here, and repairing drift in a Rule, Skill, or other Runtime artifact realized from a Skill Contract remains Agent Sync's job alone.

Derive undeclared capability needs from current evidence on every run. A technology, framework, platform, protocol, service, data source, development activity, or preferred default may indicate that a relevant Agent capability exists. Do not keep a hardcoded technology or capability list in this Skill.

### Identify

Turn the current Module declarations and current Understanding into a visible inventory:

| Item | Capability Realization Kind | Evidence | Why an Agent capability may exist | Capability types to search |
| --- | --- | --- | --- | --- |

Every declared Prepared or Installed capability in the Agent Skill Preferences is already an identified item; every undeclared item must cite the Target, Principle, Preference, selected default, dependency, configuration, or implementation evidence that produced it. When the Human's invocation names a specific capability need, include it as its own identified item; an empty or unspecific request instead performs complete relevant discovery from current evidence. Keep distinct needs separate even when one candidate may later satisfy several of them. This inventory defines what Discovery searches; it does not authorize installation or transfer.

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

### Boundaries

Perform only Agent-capability discovery, Prepared and Installed materialization declared by the Module, and approved project-scoped installation of undeclared needs. Do not perform an Interface Operation or change Interface sources, Target application code, architecture, manifests, lockfiles, runtime dependencies, credentials, or user- or machine-scoped state. Do not remove a compatible capability or install a duplicate. Never repair Runtime drift in a Rule, Skill, or other artifact realized from a portable Contract; that reconciliation belongs only to Agent Sync.

The operation is idempotent: repeating it against unchanged Target evidence, Module declarations, installed capabilities, and available releases makes no changes.

### Report

Report the final status of every identified item as **installed**, **updated**, **already available**, **activation required**, **not found**, **rejected**, or **blocked**. Include its Capability Realization Kind, evidence, capability type, selected candidate and source, compatibility evidence, verified project scope and repository location or declaration, included components and permissions, discovery and usability check, and any remaining activation step.

