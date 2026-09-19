# Agent Rule Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Rules guide behavior without replacing authority](#rules-guide-behavior-without-replacing-authority)**
   - **[Rule scope and conflict are explicit](#rule-scope-and-conflict-are-explicit)**
   - **[Security boundaries use enforcement](#security-boundaries-use-enforcement)**
   - **[Presentation preserves technical substance](#presentation-preserves-technical-substance)**
   - **[Interaction keeps work legible](#interaction-keeps-work-legible)**
   - **[Interaction requests only material decisions](#interaction-requests-only-material-decisions)**
   - **[Completion is evidence-backed](#completion-is-evidence-backed)**
   - **[Material execution is observable](#material-execution-is-observable)**
   - **[Health claims use controlled status vocabulary](#health-claims-use-controlled-status-vocabulary)**
   - **[Session state is not authoritative project state](#session-state-is-not-authoritative-project-state)**
   - **[Resume revalidates before mutation](#resume-revalidates-before-mutation)**
   - **[Session termination exposes unfinished work](#session-termination-exposes-unfinished-work)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Rule is the Component that defines persistent behavioral instructions applied across sessions or within a declared path scope. Rules adapt Agent Native and Agent Instance behavior to stable project conventions without becoming enforcement mechanisms or copies of owned Interface sources.

It owns instruction scope, loading conditions, and precedence among Rules. It does not own security enforcement, workflow implementation, or project definitions.

On 2026-09-17 the former Interaction, Observability, and Session Components were merged into this Component: how an Agent presents its work, what counts as evidence of completion, and how a session begins, resumes, and ends are persistent rules of conduct that every Agent Native must honor whether or not it has a native mechanism for each. Nothing was dropped; each absorbed Principle keeps its former number in a note.

*Absorbed from the former Agent Interaction Component on 2026-09-17 — its introduction, kept verbatim:* Agent Interaction is the Component that governs how Agent Native and Agent Instance work is presented to and exchanged with Humans. It covers output style, progress communication, prompts, status presentation, artifacts, and other user-interface behavior.

It owns presentation and interaction contracts. It does not own technical meaning, evidence, permission decisions, or the work being communicated.

*Absorbed from the former Agent Observability Component on 2026-09-17 — its introduction, kept verbatim:* Agent Observability is the Component that makes Agent Native and Agent Instance configuration, execution, capability health, evidence, and outcomes inspectable. It defines diagnostics, status, logs, usage signals, and completion evidence without becoming the authority for the work observed.

It owns observation contracts and health vocabulary. It does not own implementation, project intent, hidden reasoning, or the records maintained by other Components.

*Absorbed from the former Agent Session Component on 2026-09-17 — its introduction, kept verbatim:* Agent Session is the Component that governs one continuous or resumable period of Agent execution. It defines lifecycle, identity, state continuity, background work, resumption, isolation, and termination behavior.

It owns session lifecycle and transient execution continuity. It does not own project state, authored definitions, or durable Workflow records.

### Purpose

Some things an Agent must do are not tied to any one task: never commit without being asked, report progress without narrating everything, claim completion only with evidence, re-establish context after a resume. They apply across sessions and across work, and if they are not written down somewhere persistent, they have to be repeated in every conversation — and they will be forgotten in the one that matters.

Rule exists to hold them. A Rule is a standing instruction that adapts the Agent's behavior to stable conventions: how it presents work, what it counts as done, how it begins and ends a session. It is guidance the Agent carries with it, not enforcement.

The distinction from enforcement is the point. A Rule tells the Agent how to behave; a Permission guarantee makes a behavior impossible. Rules that pretend to enforce create a false sense of safety, and enforcement that pretends to be advice gets argued with. Keeping them in separate Components keeps both honest.

### How It Works

The Human declares Rules, each with its scope — applying everywhere, or only within a declared path — and its complete text in its own definition file. Agent Sync places that content where the selected Native reads standing instructions, adding only that Native's wrapper.

Loading and precedence are explicit: which Rules apply, in what order, and what happens when two of them conflict. A Rule never silently overrides an owned Interface source; where a Rule and an authority disagree, the authority holds.

Beyond the declared Rules, this Component carries the conduct every Agent Native honours whether or not it has a native mechanism for each: presentation that never alters technical substance, progress that is reported without narrating internals, decisions that are asked for only when they are material, completion claimed only with observed evidence, a controlled vocabulary for health, and session conduct — session state is never authoritative, a resume revalidates before it mutates anything, and an ending exposes what is unfinished.

What must be guaranteed rather than followed is not written here: it is declared as an Enforced Guarantee in Permission, and this Component explains the boundary rather than replacing it.

<br>

## Terms

- **Agent Rule** — persistent behavioral guidance loaded for all work or a matching scope.
- **Scoped Rule** — an Agent Rule activated only for declared paths or conditions.
- **Rule Conflict** — two applicable instructions that cannot both be satisfied.
- **Output Style** — a presentation contract controlling organization, tone, and response format.
- **Progress Update** — a concise report of active scope, material movement, or a blocking condition.
- **Artifact** — a rendered or shareable representation of an Agent Native or Agent Instance result.
- **Observation** — a current, attributable fact obtained from an inspectable source or check.
- **Evidence** — an Observation sufficient to support a stated condition or outcome.
- **Capability Status** — the current availability classification of a declared capability.
- **Session** — one identifiable period of Agent interaction and execution.
- **Resume** — continuation of an existing Session with its available conversation and runtime state.
- **Background Work** — execution that continues without occupying the active interaction path.

## Relationships

- **Consumes Target and Implementation Modules during ordinary execution** — Agent Module authorities are consumed only by explicit Agent Sync and realized as Runtime Rules for every other operation.
- **Consumed by Agent Context and Skill** — supplies persistent applicable guidance.
- **Consumed by Agent Permission (including former Hook)** — provides behavioral context while those Components supply enforceable controls.
- **Consumes Agent (formerly Role), Command, Rule (formerly Session and Observability)** — presents actions, progress, state, and outcomes.
- **Consumed by every Human-facing Agent capability** — supplies the selected communication contract.
- **Consumes every Agent Component** — evaluates their declarations and runtime realization.
- **Consumed by Agent (formerly Role), Rule (formerly Interaction and Session)** — supplies diagnostics and evidence-backed outcome claims.
- **Consumes Agent Runtime, Agent, Context, Agent (formerly Role), and Permission** — hosts an Agent Instance executing with current context and authority.
- **Consumed by Agent (formerly Coordination), Permission (formerly Hook), Rule (formerly Interaction and Observability)** — supplies lifecycle events and execution identity.

Technical Rule files, scopes, load order, and native locations belong to Agent Rule Preferences.

Technical styles, status lines, themes, artifact facilities, and interface selections belong to Agent Rule Preferences (formerly Interaction Preferences).

Technical checks, statuses, diagnostics, telemetry, logging, and usage reporting belong to Agent Rule Preferences (formerly Observability Preferences).

Technical session options, persistence, resume policy, isolation, and background behavior belong to Agent Rule Preferences (formerly Session Preferences).

Every Principle in this file is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory.

<br>

### Rules guide behavior without replacing authority

**Rule:** An Agent Rule states stable behavioral guidance concisely and points to the current owner of project facts, structures, choices, and workflows. It never copies or overrides those sources.

**Why:** Always-loaded copies consume context and become stale competing authorities.

**Boundary:** A Rule may state how to locate and apply an authority.

<br>

### Rule scope and conflict are explicit

**Rule:** Every Agent Rule declares whether it is global or scoped and the exact condition under which it applies. Applicable conflicts are reported and resolved by authority and declared precedence, never by arbitrary load order.

**Why:** Silent conditional instructions make Agent behavior unpredictable.

**Boundary:** More specific guidance may refine a broader Rule when both can be satisfied.

<br>

### Security boundaries use enforcement

**Rule:** A behavior that must be guaranteed is enforced by Agent Permission, sandboxing, or an applicable Hook rather than relying only on an Agent Rule.

**Why:** Instructions influence model behavior but do not constitute deterministic enforcement.

**Boundary:** Rules may explain an enforced boundary and how to work within it.

<br>

### Presentation preserves technical substance

**Rule:** Output Style may change organization, tone, detail, and format while preserving exact technical meaning, identifiers, commands, paths, code, evidence, warnings, uncertainty, and required decisions.

**Why:** Communication may adapt to a Human without changing the work communicated.

**Boundary:** A style may shorten expression only when no required substance is lost.

*Formerly Agent Interaction Principle "Rules guide behavior without replacing authority".*

<br>

### Interaction keeps work legible

**Rule:** Human-facing roles communicate active scope, material progress, blockers, required decisions, and final outcomes at a frequency and level appropriate to the work. They never fabricate certainty or hide a failed condition behind presentation.

**Why:** The Human must be able to understand and steer ongoing work.

**Boundary:** Routine internal details and hidden reasoning are not progress requirements.

*Formerly Agent Interaction Principle "Rule scope and conflict are explicit".*

<br>

### Interaction requests only material decisions

**Rule:** An Agent Native or Agent Instance asks the Human only when no safe choice avoids materially changing intent, architecture, security, data integrity, permissions, a declared interface, or an irreversible outcome.

**Why:** Excessive questions prevent autonomous execution while omitted material choices violate ownership.

**Boundary:** Ordinary unstated details within current authority are resolved by professional judgment.

*Formerly Agent Interaction Principle "Security boundaries use enforcement".*

<br>

### Completion is evidence-backed

**Rule:** An Agent Native or Agent Instance reports success only when every requested and contract-required condition has current observable Evidence. Missing or inconclusive Evidence remains explicit and never becomes success by inference.

**Why:** Stable outcomes require repeatable gates rather than confidence or plausible artifacts.

**Boundary:** Evidence proportional to risk is sufficient; redundant checks that cannot increase confidence are unnecessary.

*Formerly Agent Observability Principle "Rules guide behavior without replacing authority".*

<br>

### Material execution is observable

**Rule:** Active scope, material decisions, mutations, delegation, checks, outcomes, blockers, configuration drift, Capability Status, and required Human actions are attributable and inspectable.

**Why:** Later Humans, Agent Natives, and Agent Instances need to distinguish current fact from assumption and unfinished work.

**Boundary:** Hidden reasoning, secrets, and irrelevant command transcripts are never observability requirements.

*Formerly Agent Observability Principle "Rule scope and conflict are explicit".*

<br>

### Health claims use controlled status vocabulary

**Rule:** Capability and configuration health use declared statuses with objective entry conditions. A status changes only when current Observation establishes the new condition.

**Why:** Stable vocabulary makes diagnostics comparable across runtimes and sessions.

**Boundary:** A runtime may expose richer native detail beneath the portable status.

*Formerly Agent Observability Principle "Security boundaries use enforcement".*

<br>

### Session state is not authoritative project state

**Rule:** Conversation history, session identifiers, transient tasks, cached context, and background process state never replace authored Interface sources or owned operational records.

**Why:** Sessions can be lost, compacted, forked, or resumed with incomplete state.

**Boundary:** Session state may be used as evidence after it is revalidated against current sources.

*Formerly Agent Session Principle "Rules guide behavior without replacing authority".*

<br>

### Resume revalidates before mutation

**Rule:** A resumed, forked, restored, or background Session re-establishes required Context, active scope, permissions, filesystem state, and outstanding work before making new mutations.

**Why:** External state may change while a Session is inactive or isolated.

**Boundary:** Read-only orientation may occur before full mutation readiness is established.

*Formerly Agent Session Principle "Rule scope and conflict are explicit".*

<br>

### Session termination exposes unfinished work

**Rule:** Before a Session claims completion or terminates managed Background Work, it exposes unfinished responsibilities, running work, blockers, and required Human actions. It never abandons authorized work while presenting success.

**Why:** Invisible lifecycle endings make continuation unsafe.

**Boundary:** An explicitly cancelled Session reports cancellation rather than completing its original objective.

*Formerly Agent Session Principle "Security boundaries use enforcement".*

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Rules guide behavior without replacing authority**

- **Must** — keep Rules concise and refer to current owners
- **Never** — copy or override project authorities in a Rule

**Rule scope and conflict are explicit**

- **Must** — declare Rule scope, activation, and conflict resolution
- **Never** — resolve conflicts through arbitrary load order

**Security boundaries use enforcement**

- **Must** — place guaranteed boundaries in enforceable mechanisms

**Presentation preserves technical substance**

- **Must** — preserve exact technical substance under every Output Style
- **Never** — let presentation hide evidence, warnings, uncertainty, or decisions

**Interaction keeps work legible**

- **Must** — communicate scope, progress, blockers, decisions, and outcomes appropriately
- **Never** — fabricate certainty or conceal failure

**Interaction requests only material decisions**

- **Must** — ask the Human only for materially consequential unresolved choices

**Completion is evidence-backed**

- **Must** — support every completion claim with current proportional Evidence
- **Never** — infer success from missing or inconclusive Evidence

**Material execution is observable**

- **Must** — make material execution, drift, health, blockers, and Human actions inspectable
- **Never** — expose secrets or require hidden reasoning

**Health claims use controlled status vocabulary**

- **Must** — use declared statuses whose changes are established by Observation

**Session state is not authoritative project state**

- **Never** — treat transient Session state as authoritative project state

**Resume revalidates before mutation**

- **Must** — revalidate context, scope, permission, files, and work before resumed mutation

**Session termination exposes unfinished work**

- **Must** — expose unfinished and running work before completion or termination
- **Never** — abandon unfinished work while reporting success
