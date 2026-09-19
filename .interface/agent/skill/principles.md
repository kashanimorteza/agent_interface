# Agent Skill Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[1. Every Skill has one complete contract](#1-every-skill-has-one-complete-contract)**
   - **[2. Skill availability is proven](#2-skill-availability-is-proven)**
   - **[3. Skill execution is safely repeatable](#3-skill-execution-is-safely-repeatable)**
   - **[4. A prepared file or directory may supply a Skill's native instruction body](#4-a-prepared-file-or-directory-may-supply-a-skills-native-instruction-body)**
   - **[5. Sync places Module content; it translates only where translation serves the Native](#5-sync-places-module-content-it-translates-only-where-translation-serves-the-native)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Skill is the Component that defines the architecture-level requirements for reusable knowledge or workflows an Agent Role can activate. Every declared Skill has exactly one Capability Realization Kind. An Interface-owned Skill is Constructed: its portable Skill Contract defines it completely, and Agent Sync places that Contract's obligations, as written, into the Native's own Skill form, adding only the Native's discovery and invocation mechanics (Principle 5). A declared Skill with a matching prepared Markdown file is Prepared: that file's instruction content is transferred into the Runtime unchanged. Externally provided Skills are Installed: they remain provider-owned capabilities declared by the Agent Preferences and provisioned through Agent Extension or Agent Integration, never built from a Skill Contract.

It owns Skill contracts and activation boundaries. It does not own the project facts, Component policies, or runtime tools it consumes.

### Purpose

An Agent that is told what to do each time repeats the same explanation forever, and every repetition is a chance to say it differently. Work that recurs — planning a phase, reviewing a result, bringing a Target online — needs to exist as a capability the Agent can activate, defined once and identical every time it runs.

Skill exists to define what such a capability must contain before it can be trusted: one complete contract stating its purpose, its inputs, its authority, its verification, and its stopping conditions. A Skill with a partial contract is an instruction that behaves differently depending on who invokes it and when.

It also decides how a Skill becomes real in a Runtime. Some Skills are built from their portable Contract, some are complete files the Human wrote, some come from outside and are merely provisioned. Naming which kind a Skill is settles what Sync does with it, and keeps a Constructed Skill from being quietly replaced by something nobody authored.

### How It Works

Every declared Skill has exactly one Capability Realization Kind, and that Kind decides how it reaches the Runtime. An Interface-owned Skill is Constructed: its portable Contract defines it completely and Agent Sync places those obligations into the Native's own Skill form. A Skill with a matching prepared file is Prepared: that file's content is transferred unchanged. A Skill from an external provider is Installed: provisioned through its own ecosystem, never built here.

A Contract is what makes a Constructed Skill trustworthy. It states the Skill's purpose, what it accepts, what it produces, what authority it has, what it must verify before claiming success, and when it must stop — in portable terms, with no vendor's commands or file layout inside it.

Availability is proven rather than assumed. A Skill counts as available when the intended Role can actually discover and invoke it in the current Runtime; files on disk and installation receipts are not that proof.

Execution is safely repeatable: running a Skill again preserves valid work rather than regenerating over it, and a fingerprint proves that a realization is stale without ever proving that one conforms.

<br>

## Terms

- **Skill** — reusable instructions or knowledge activated explicitly or by relevance.
- **Skill Contract** — the portable definition of an Interface-owned Skill's responsibility, inputs, outputs, authority, checks, and stopping conditions.
- **Prepared Skill File** — an optional Human-authored Markdown instruction body for one declared Skill, materialized by the install mode of the Agent Native Skill into that Skill's native Runtime folder without changing its meaning.
- **Activation** — the state in which a Skill is discoverable and usable by its intended role.
- **Invocation Policy** — whether a Skill may be invoked by the Human, by a declared coordinating Skill, or by both in the selected Runtime.

## Relationships

- **Consumes Agent (formerly Role), Context, Rule, Tool, and Permission** — executes within their contracts.
- **Consumes Implementation Components and Target** — reads current authorities required by its responsibility.
- **Consumed by Agent, Command, and Agent (formerly Coordination)** — provides assignable, invocable, and delegable workflows.

Each Interface-owned Skill's portable behavior belongs to its Skill Contract under the Agent Skill Component. Technical Skill catalogs, external provider Skills, activation choices, and provider resources belong to Agent Skill Preferences; Native implementation mappings are resolved by Agent Sync from the selected Agent Native. Command names and argument forms belong to Agent Command Preferences.

Every statement here is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory, and its number is permanent.

<br>

### 1. Every Skill has one complete contract

**Rule:** Every Interface-owned Skill has exactly one portable Skill Contract, conforming to the Skill Contract Schema, that declares its purpose, responsibility, trigger, inputs, outputs, required Understanding, authority, workflow invariants, verification, idempotency expectation, stopping conditions, and runtime-realization requirements. Principles own rules shared by Skills, the Skill Contract owns Skill-specific behavior independent of a runtime, and a native Skill implementation is a synchronized, self-contained realization that owns only runtime-specific execution details and never overrides or becomes a second authority for its Contract.

**Why:** A Skill must remain focused and current when project definitions change.

**Boundary:** Only `agent-native` reads the portable Contract inside the Agent Module. Every other Interface-owned Skill consumes its synchronized native realization without reading or resolving any Agent Module source. A coordinating Skill Contract may require an exact orchestration sequence when orchestration is its single declared responsibility. An external Skill, including framework and package-provided Skills, remains governed by its synchronized runtime realization and the active Role; it does not receive an Interface-owned Skill Contract.

<br>

### 2. Skill availability is proven

**Rule:** A Skill is available only when its intended Agent Role can discover and invoke it in the current project. A Skill delegated by another Skill is available only when the selected Runtime permits that declared coordinator to invoke it. Core Workflow Skills used by Implement are invocable both directly by the Human and by declared coordinators; top-level or sensitive coordinating Skills remain explicit-Human entry points unless the Skill Preferences state otherwise. A file, installation record, or declaration alone does not prove Activation.

**Why:** Planning around nominal Skills fails when the runtime cannot actually load them.

**Boundary:** Coordinator invocation never expands the delegated Skill's scope, authority, permission requirements, or stopping conditions. Being coordinator-invocable does not authorize unrelated automatic execution. Validation reports an unmet invocation condition before a coordinating workflow mutates state.

<br>

### 3. Skill execution is safely repeatable

**Rule:** Repeating a Skill against unchanged authorities and state preserves valid work and produces no unnecessary mutation. A Skill reconciles current evidence rather than regenerating blindly.

**Why:** Skills are routinely resumed and rerun across sessions.

**Boundary:** Repeatability never authorizes destructive replacement of meaningful work. A native Skill realization may carry a fingerprint of the portable source it was realized from; a changed fingerprint proves staleness and requires reconciliation, and an unchanged fingerprint never proves conformance, which is established only by comparing the current source with the realization in full.

<br>

## Skill-specific behavior

Each Skill's purpose, responsibility, workflow, inputs, outputs, authority, verification, idempotency, stopping conditions, and runtime realization belong only in its own portable Contract. This Principles file defines no Skill-specific workflow or implementation details.

<br>

### 4. A prepared file or directory may supply a Skill's native instruction body

**Rule:** The Agent Skill Preferences declare one optional prepared-file directory and an exact naming convention keyed by declared Skill identity, satisfied either by a single Markdown file or by a directory holding that Skill's complete artifact. When a matching prepared file or directory exists, the install mode of the Agent Native Skill creates the Skill folder and entrypoint required by the selected Agent Native, preserves the prepared content and its meaning - every file of a prepared directory tree, with its internal relative paths intact - and adds or adapts only the minimum native metadata needed for discovery and invocation. When no match exists, Agent Sync realizes the Skill from its portable Contract, provider declaration, and Runtime mapping exactly as before.

**Why:** A complete Human-authored Skill should be reusable without forcing every Skill to have a prepared file or turning Runtime output into its source.

**Boundary:** The presence of a prepared file or directory never declares a new Skill, selects a provider, proves Activation, or authorizes an unmatched artifact to be installed. A prepared file or directory must match exactly one Skill already declared by the Preferences and must conform to that Skill's Contract and applicable Principles. Only Agent Sync reads it; ordinary Runtime Skills consume the synchronized native copy. Agent Sync never rewrites the Human-owned source file or silently changes its semantic instructions.

<br>

### 5. Sync places Module content; it translates only where translation serves the Native

**Rule:** Agent Sync's first job is placement: it takes each declaration as the Human authored it and decides where, in the selected Agent Native's own configuration, that content belongs. The content itself is carried as written. Sync may restate a declaration in the Native's idiom only when doing so makes that concept land better in the Native's own configuration — and then the meaning, scope, and every obligation stay exactly what the Module gives them. A restatement that changes scope ("applicable" to "owning", "every" to "selected", a named Component to a category) is not a translation but a deviation, and is reported as approximated with both wordings side by side, never as synchronized.

**Why:** The Module is written once, general and standard, so that any Agent can work from it; the Human's effort goes into its structure and content alone. After Sync the Human must be able to trust that every concept and rule was carried over unchanged — so that when behavior is wrong, the fault is a rule the Human wrote badly, never a translation the Human never saw.

**Boundary:** Native mechanics — commands, paths, formats, invocation controls, frontmatter — are the Native's own and are always added by Sync; this Principle governs the Module's content, not the wrapper around it. Restating an obligation in the Native's idiom is allowed when its scope is provably unchanged; this Principle does not require copying Contract prose verbatim.

<br>

## At a Glance

- **Must** — give every Interface-owned Skill exactly one complete portable Contract conforming to the Skill Contract Schema *(1)*
- **Must** — keep shared rules in Principles, Skill-specific behavior in its Contract, and runtime execution details in the native implementation *(1)*
- **Must** — make every non-Sync native Skill self-contained so it never resolves a Contract or capability through the Agent Module *(1)*
- **Never** — let a native Skill implementation override or become a second authority for its Contract *(1)*
- **Must** — prove Skill availability through discovery and invocation *(2)*
- **Must** — make every delegated Skill invocable by its declared coordinator and verify the complete invocation chain before orchestration mutates state *(2)*
- **Never** — let coordinator invocation expand a delegated Skill's authority or permit unrelated automatic execution *(2)*
- **Must** — make repeated execution preserve valid work *(3)*
- **Never** — use repeatability to justify destructive regeneration *(3)*
- **Must** — treat a changed source fingerprint as proof of staleness and an unchanged one as no proof of conformance *(3)*
- **Must** — materialize an exact matching prepared Skill file or directory tree into the selected Agent Native's required Skill folder while preserving its instruction meaning and internal relative paths *(4)*
- **Must** — keep the existing Contract- or provider-based realization path when a declared Skill has no prepared file *(4)*
- **Never** — infer a Skill from an unmatched file or directory, treat its presence as proof of Activation, or rewrite the Human-owned prepared source *(4)*
- **Must** — place each Module declaration as the Human authored it, adding only the Native's own mechanics around it *(5)*
- **Must** — restate a declaration in the Native's idiom only where that makes the concept land better in the Native, and only with its scope and obligations unchanged *(5)*
- **Never** — narrow, widen, or re-scope an obligation while realizing it; report such a difference as approximated with both wordings, never as synchronized *(5)*
