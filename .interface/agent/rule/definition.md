# Agent Rule Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
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
7. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Rule defines persistent behavioral guidance applied across sessions or within a declared scope. It adapts Agent behavior to stable conventions without becoming an enforcement mechanism or a copy of another Component's authority.

It owns Rule scope, loading conditions, precedence, and recurring conduct. It does not own security enforcement, workflow implementation, project definitions, or session records.

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

- **Consumed by Agent** — supplies persistent behavioral guidance to the Agent and its Native realization.
- **Consumes Permission** — explains enforceable boundaries without replacing Permission's guarantees.
- **Consumes Context** — relies on current context loading and scope to determine which Rules apply.

<br>

<br>

## Layering

This Definition carries the portable meaning and mandatory Principles of the Rule Component. Preferences carry current Rule selections, declarations, and Native realization hints. Agent Sync reads both and realizes them without changing their scope or authority.

<br>

## Authority

The Human owns this Definition and its Preferences. Every Principle in this file is mandatory; Preferences can never override a Principle, and Agent Sync is the only reader authorized to realize the Component in an Agent Native.

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

**Rule:** A behavior that must be guaranteed is enforced by Agent Permission, sandboxing, or another applicable Native mechanism rather than relying only on an Agent Rule.

**Why:** Instructions influence model behavior but do not constitute deterministic enforcement.

**Boundary:** Rules may explain an enforced boundary and how to work within it.

<br>

### Presentation preserves technical substance

**Rule:** Output Style may change organization, tone, detail, and format while preserving exact technical meaning, identifiers, commands, paths, code, evidence, warnings, uncertainty, and required decisions.

**Why:** Communication may adapt to a Human without changing the work communicated.

**Boundary:** A style may shorten expression only when no required substance is lost.

<br>

### Interaction keeps work legible

**Rule:** Human-facing roles communicate active scope, material progress, blockers, required decisions, and final outcomes at a frequency and level appropriate to the work. They never fabricate certainty or hide a failed condition behind presentation.

**Why:** The Human must be able to understand and steer ongoing work.

**Boundary:** Routine internal details and hidden reasoning are not progress requirements.

<br>

### Interaction requests only material decisions

**Rule:** An Agent Native or Agent Instance asks the Human only when no safe choice avoids materially changing intent, architecture, security, data integrity, permissions, a declared interface, or an irreversible outcome.

**Why:** Excessive questions prevent autonomous execution while omitted material choices violate ownership.

**Boundary:** Ordinary unstated details within current authority are resolved by professional judgment.

<br>

### Completion is evidence-backed

**Rule:** An Agent Native or Agent Instance reports success only when every requested and contract-required condition has current observable Evidence. Missing or inconclusive Evidence remains explicit and never becomes success by inference.

**Why:** Stable outcomes require repeatable gates rather than confidence or plausible artifacts.

**Boundary:** Evidence proportional to risk is sufficient; redundant checks that cannot increase confidence are unnecessary.

<br>

### Material execution is observable

**Rule:** Active scope, material decisions, mutations, delegation, checks, outcomes, blockers, configuration drift, Capability Status, and required Human actions are attributable and inspectable.

**Why:** Later Humans, Agent Natives, and Agent Instances need to distinguish current fact from assumption and unfinished work.

**Boundary:** Hidden reasoning, secrets, and irrelevant command transcripts are never observability requirements.

<br>

### Health claims use controlled status vocabulary

**Rule:** Capability and configuration health use declared statuses with objective entry conditions. A status changes only when current Observation establishes the new condition.

**Why:** Stable vocabulary makes diagnostics comparable across runtimes and sessions.

**Boundary:** A runtime may expose richer native detail beneath the portable status.

<br>

### Session state is not authoritative project state

**Rule:** Conversation history, session identifiers, transient tasks, cached context, and background process state never replace authored Interface sources or owned operational records.

**Why:** Sessions can be lost, compacted, forked, or resumed with incomplete state.

**Boundary:** Session state may be used as evidence after it is revalidated against current sources.

<br>

### Resume revalidates before mutation

**Rule:** A resumed, forked, restored, or background Session re-establishes required Context, active scope, permissions, filesystem state, and outstanding work before making new mutations.

**Why:** External state may change while a Session is inactive or isolated.

**Boundary:** Read-only orientation may occur before full mutation readiness is established.

<br>

### Session termination exposes unfinished work

**Rule:** Before a Session claims completion or terminates managed Background Work, it exposes unfinished responsibilities, running work, blockers, and required Human actions. It never abandons authorized work while presenting success.

**Why:** Invisible lifecycle endings make continuation unsafe.

**Boundary:** An explicitly cancelled Session reports cancellation rather than completing its original objective.

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
