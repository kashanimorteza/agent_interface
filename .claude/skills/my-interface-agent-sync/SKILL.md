---
name: my-interface-agent-sync
description: Realize this adapter itself in `self` mode, or translate every other Agent Module declaration through the active Agent Native's own conventions in `module` mode, certifying synchronization only after complete post-change verification.
argument-hint: "<self | module>"
arguments: [mode]
disable-model-invocation: true
metadata:
  contract: ".interface/agent/skill/contracts/agent-sync.md"
  contract_sha256: "sha256:055a49d54009f1fed515029f2faaf8607e43cb29cabe53a9d57939b0584c0ef5"
  synced_at: "2026-09-17T12:24:58Z"
---

# Synchronize the Agent Module

This file is the Claude Code adapter for the portable `agent-sync` Skill Contract and the sole Runtime exception permitted to read Agent Module sources. Resolve and read that Contract through Agent Skill Profile only after explicit Human invocation; the Contract is authoritative for behavior and this adapter supplies only Claude Code execution details. It never depends on the prior presence of another vendor's Agent Sync adapter.

## Trigger

Activate only on direct Human invocation of `/my-interface-agent-sync`, while setting up, repairing, migrating, updating, or auditing an Agent Runtime. No Agent Native, Agent Instance, Skill, coordinator, Hook, startup or resume routine, automation, or model-generated action may invoke, chain, trigger, or simulate this Skill. A Human request to change Agent Module declarations authorizes only that source change; it is not an invocation of this Skill. Every Agent Module change is dormant desired state until this explicit synchronization completes.

## Modes

The invoked mode arrives as `$mode`. Resolve it before any mutation; accept exactly one mode and no capability selection.

- `self` — run the Realization procedure below on this adapter only, against the current `agent-sync` Contract. Reconcile nothing else, and never report the complete Module as synchronized from a `self` run.
- `module` — first re-read the current `agent-sync` Contract and this file in full and compare them; if they differ, mutate nothing, report the exact difference, and stop with the instruction to run `/my-interface-agent-sync self` first. Otherwise run the Realization procedure on every other declaration.
- no mode — mutate nothing; report both modes and whether this adapter still matches its current Contract.

A running instance cannot load a definition it did not start with, so never claim to have executed a Contract this adapter does not currently implement.

## Progress narration

Print one short line to the Human at the start of each phase — **Understanding**, **Comparison**, **Reconciliation**, **Verification** — in both modes and again at the start of every repeated cycle. Never hold announcements for the final report.

## Understanding

Establish Interface Understanding from `.interface/foundation/interface.md`, then read the complete Agent Module through its declared Agent Structure and current sources, discovering every declaration, resource, and explicit empty category dynamically on every invocation — never from a hardcoded list or one remembered by the Contract, this adapter, or an earlier run. Consume the Agent Profile, portable Skill Contracts, native project artifacts, and runtime-reported activation state. Treat Principles as mandatory contracts and Profiles as Human-owned desired state; never modify either. Use no Target Understanding and no other Interface Module.

Before choosing any realization, establish Native Runtime Understanding from Claude Code's own documentation: project Skill location and frontmatter, `$name` argument substitution, invocation controls (`disable-model-invocation`, `user-invocable`), Rules, settings, permissions, hooks, agents, plugin and MCP enablement, and what each loads only at session start. Never require a project-side realization map or predeclared native path; if Claude Code cannot realize a required declaration, report it `blocked` rather than guessing from a familiar layout. When a declaration carries per-Agent-Native details, use only the Claude Code block as an aid that narrows discovery, ignore other Natives' blocks, and fall back to Claude Code's own documentation when no block exists or it conflicts with the actual mechanism.

## Realization procedure

This is the only permitted way to reach a per-declaration outcome. Apply it to one declaration at a time, none exempted, no shortcut for one that looks current:

1. Read every Agent Module source the declaration owns, in full. For a Skill that is its Contract at `.interface/agent/skill/contracts/<name>.md`.
2. Read the installed native artifact in full. For a Skill that is `.claude/skills/<native-name>/SKILL.md`. If none exists, record `create` and go to step 4.
3. Compare section by section and record every difference of three kinds: the artifact instructs something the declaration no longer requires; omits something it requires; or states a rule it has changed.
4. No difference → classify `already synchronized` and go to step 7. Any difference → rewrite the whole artifact so every section carries what the declaration currently requires, keeping the frontmatter Claude Code needs and the native detail the declaration leaves to the adapter; never patch around a difference and never invent content for an empty category.
5. Re-read the written artifact and prove each recorded difference is gone.
6. Report `blocked` any difference that survives; never report it resolved.
7. Record the mapping row: sources read, artifact path, Native mechanism, verification gate, and what re-reading proved.

Claim `no change` or `already synchronized` only from this comparison with both files read in full. Presence, frontmatter, modification time, apparent recency, and the absence of a remembered edit are never evidence of conformance. A changed source fingerprint (see Synchronization record) proves staleness and forces step 4; an unchanged one proves nothing. A `self` run that found a difference and left this file unwritten has failed. A run that leaves any declaration unread, or classifies one unchanged without this comparison, reports `Agent Module not fully synchronized` and names every unexamined declaration.

## Module reconciliation

Before changing runtime state, build one inventory row per dynamically discovered declaration and resource, including empty and already-satisfied categories, and classify each as `no change`, `create`, `update`, `install`, `enable`, `activation required`, `report only`, or `blocked`. Never silently skip an unknown, new, or unsupported item: reconcile it when Claude Code supplies an authorized mapping, otherwise report it blocked with the missing mapping.

Verify first that Claude Code is available and compatible with the complete Module, derive dependency-safe order from Module relationships, resolve ownership before every write, and preserve each owner's authority throughout. Then process every row through the Realization procedure. Add required declared sources and install or enable only entries already selected by Human-owned Profiles, at project scope only; reload or activate changed capabilities when Claude Code supports doing so safely. Realize only **Constructed** Skills — an Interface-owned Skill built from its portable Contract into the smallest self-contained project Skill. **Prepared** and **Installed** Skills belong to the Skill Installer: observe and report their condition, never create, transfer, install, rewrite, or remove them. Already-selected Extensions and Integrations are still provisioned and verified.

Explicit Human invocation is standing authorization for every additive, project-scoped write this adapter owns, including rewriting an existing Skill, Rule, setting, or hook: do not pause to ask. Stop for Human action only for credentials, external trust, broader scope, an irreversible action, authority the declaration does not express, or destructive replacement of unrelated or ambiguously-owned Human content — in that last case make no write to that resource and report the exact decision needed. Independent items continue reconciling when their dependencies permit. A Native-provided or explicitly unused declaration is observation-only: explicitly unused means no capability is required and never authorizes removing an observed undeclared capability. Preserve compatible native values the Module leaves unspecified; report an undeclared capability as `unmanaged` and never remove it unless it conflicts with a Principle or selected choice. When any synchronized non-Sync instruction routes its consumer into an Agent Module source, replace that routing with the corresponding synchronized Rule, capability, Agent Instance, or Skill realization; every non-Sync artifact must be self-contained or refer only to other synchronized artifacts.

## Verification

After reconciliation, discard pre-change observations and perform a second complete pass: rediscover and re-read the complete Agent Module, independently re-read every native artifact, and query runtime status where supported. Prove that the Agent Native is active; every required Agent Instance is instantiable with correct Role and capability assignments; every required Skill is discoverable by its Role, self-contained, has invocation controls matching its declared Human and coordinator Invocation Policy, and instructs what its Contract currently requires; every Command resolves to its owner and argument contract; effective settings, permissions, rules, hooks, and enforcement match their owners; each selected Extension is installed and project-enabled; each selected Integration is trusted and usable or truthfully marked `activation required`; each Prepared and Installed Skill's condition is observed without modification; no non-Sync instruction directs its consumer into an Agent Module source; and no secret was written to a project artifact. A write that succeeded is not itself conformance.

When this pass finds a required item unrealized or unverified for a reason other than a genuine stopping condition, return to Understanding, reconcile it again, and run a new complete Verification pass, narrating each phase. Repeat until every required item passes or a cycle reproduces the previous cycle's outcome exactly — that is convergence, reported as final. Repeating this Skill against unchanged declarations and runtime state must produce no mutation; any new or changed Module source is detected and reconciled on the next run without editing this adapter.

## Synchronization record

`scripts/check-stale.py` beside this file owns the fingerprint mechanism. After reconciliation and before the final report, run `python3 .claude/skills/my-interface-agent-sync/scripts/check-stale.py stamp --mode <mode> --status <status> --result "<overall result>"` (add `--only <native-name>` in `self` mode) so every realized Skill carries `metadata.contract_sha256` in its frontmatter and `.claude/interface-sync.yaml` records one entry per declaration: source, fingerprint, artifact, status, mode, and time. Pass only a status this run actually proved. `check` re-hashes the sources and reports provable staleness; it is a fast gate before Understanding, never a substitute for the Realization procedure.

## Boundaries

Write only to project-scoped Claude Code artifacts authorized by the owning declaration; `.claude/interface-sync.yaml` and the Skill metadata stamp are such artifacts owned by this Skill. Never modify Interface sources, Config, Target code, application dependencies, user- or machine-scoped configuration, credentials, or unrelated Human work. Never discover or adopt a new marketplace, plugin, Skill, MCP server, Agent, or capability; when the Module lacks a needed choice, report the gap and instruct the Human to declare it and run `/my-interface-skill-installer`. A pending restart, authentication, trust prompt, missing provider, or unavailable runtime is `activation required` or `blocked`, never success.

## Report

State the resolved mode in every report. Whenever this run wrote any native artifact — a `self` rewrite of this file or any `create`, `update`, `install`, or `enable` in `module` — classify each written artifact `activation required` and place this notice once, prominently, outside the table, even when everything else succeeded:

> ⚠️ **Restart Claude Code before relying on this.** This session is still running the previous definition of every native artifact this run wrote — Skills, Rules, settings, hooks, agents, and enabled capabilities alike. Fully exit this Claude Code session and start a new one — reopening or continuing this conversation is not enough. Do this before invoking `/my-interface-agent-sync` again or trusting any rewritten artifact's behavior.

Never report a written artifact as usable in the current session while this notice is outstanding.

Open a `module` report with one mapping table, one row per declaration in reconciliation order; a row with no named artifact makes no claim, and the last column reports what re-reading proved, never that a write succeeded:

| | Agent Module declaration | Realized as | Native artifact | Verified |
|---|---|---|---|---|
| ✅ | `agent/skill/contracts/<name>.md` | Claude Code project Skill | `.claude/skills/<native-name>/SKILL.md` | re-read; instructs what the Contract requires |
| ⚠️ | `<declaration>` | `<mechanism>` | `<path or provider>` | activation required: `<Human action>` |
| 🔍 | — | observed only | `<path>` | unmanaged: present, declared nowhere |
| ❌ | `<declaration>` | `<mechanism>` | `<path or provider>` | blocked: `<exact reason>` |

`✅` synchronized · `☑️` already synchronized · `⚠️` activation required · `🔍` unmanaged · `❌` blocked. After the table, detail every non-`✅` row (what it needs, who acts, what it prevents), list preserved unmanaged capabilities, and state any Human activation step. A `self` run, a stale-adapter block, or a mode-less invocation reports its mode, its outcome (for a stale block: the exact difference and the required `self` run), and the declarations left unreconciled — never an overall Module status. Finish a complete `module` run with `Agent Module synchronized` only when the second pass proves every required declaration realized, active, and usable; otherwise `Agent Module not fully synchronized` with every preventing condition enumerated.
