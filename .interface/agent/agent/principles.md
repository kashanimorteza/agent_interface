# Agent Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Every Agent Instance has one complete definition](#every-agent-instance-has-one-complete-definition)**
   - **[Agent Instance and Role remain separate](#agent-instance-and-role-remain-separate)**
   - **[`general` is the General Agent Instance](#general-is-the-general-agent-instance)**
   - **[Specialized Agent Instances remain bounded](#specialized-agent-instances-remain-bounded)**
   - **[Agent Native and Instance availability are proven in the selected Runtime](#agent-native-and-instance-availability-are-proven-in-the-selected-runtime)**
   - **[Every Agent Role has one bounded responsibility](#every-agent-role-has-one-bounded-responsibility)**
   - **[Role ownership is unambiguous](#role-ownership-is-unambiguous)**
   - **[The Primary Role remains accountable](#the-primary-role-remains-accountable)**
   - **[The primary execution role owns the requested outcome](#the-primary-execution-role-owns-the-requested-outcome)**
   - **[`interface-reader` reports without changing the observed state](#interface-reader-reports-without-changing-the-observed-state)**
   - **[Delegation preserves scope and authority](#delegation-preserves-scope-and-authority)**
   - **[Concurrent work has exclusive mutation ownership](#concurrent-work-has-exclusive-mutation-ownership)**
   - **[Runtime coordination state is not project intent](#runtime-coordination-state-is-not-project-intent)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

The `Agent` Component declares the selected Agent Native and the executable Agent Instances it hosts in Agent Preferences. Each Agent Instance realizes an Agent Role through the Agent Native with bounded capabilities and configuration.

It owns Agent Native selection, Agent Instance identity, kind, Role assignment, capability assignment, native realization, and lifecycle defaults. It does not own Role responsibilities, Skill behavior, Runtime implementation, coordination protocol, or Permission policy.

On 2026-09-17 the former Role and Coordination Components were merged into this Component: an Agent Instance, the responsibility it executes, and the way several Instances share work are three answers to one question — which Agents the Human has. Nothing was dropped; each absorbed Principle keeps its former number in a note.

*Absorbed from the former Agent Role Component on 2026-09-17 — its introduction, kept verbatim:* Agent Role is the Component that defines the execution responsibilities available to Agent Instances within Agent Preferences, including the primary role and specialized delegated roles. It gives each role a stable contract independent of the Agent Native that hosts its Instance.

It owns role responsibilities and boundaries. It does not own Agent Instance identities, native realizations, capability configuration, workflow content, runtime configuration, or coordination state.

*Absorbed from the former Agent Coordination Component on 2026-09-17 — its introduction, kept verbatim:* Agent Coordination is the Component that organizes work across multiple Agent Instance Definitions and their Roles, sessions, tasks, and isolated workspaces within an Agent Native. It defines delegation, communication, synchronization, and integration without redefining the Agent Instances or Roles being coordinated.

It owns coordination protocol and conflict boundaries. It does not own role contracts, project Plans, or implementation decisions.

### Purpose

Work gets done by something concrete: an Agent Instance running with a model, a set of tools, a scope, and an authority. But an Instance is not the same thing as a responsibility — one responsibility can be executed by different Instances, and one Instance can be asked to do more than its responsibility allows. Conflating them is how an Agent ends up with authority nobody granted it.

This Component exists to declare both, separately, and to bind them. It says which Agent Native is selected, which Instances exist, what each one is for, which Role it executes, and what it may use. It also owns what happens when several Instances work at once: who may change what, and how their results come back together.

When these are left implicit, the Agent's shape is whatever the Runtime happened to do: a delegated task inherits the parent's full authority, two Instances write the same thing, and no one can say afterwards which Instance produced which change. All three are ownership failures, which is why one Component owns them.

### How It Works

The Human declares Agent Instances. Each one has a complete definition: its identity, its kind — a general Instance or a specialized one — the Role it executes, the capabilities it may use, and the configuration it inherits from the defaults. `general` is the Instance that does ordinary work; a specialized Instance exists because its Role is bounded in a way the general one is not.

Roles are declared beside them and stay separate. A Role is a responsibility with its own scope, authority, inputs, and expected outcome; an Instance is who executes it. That separation is what lets a responsibility be reassigned without rewriting the Agent, and what makes `interface-reader` meaningful: a Role that reports without changing anything, whichever Instance carries it.

When work is delegated, the delegation carries its own bounded objective, scope, authority, and stopping condition — never the parent's. The primary Role stays accountable for the whole request and integrates what comes back.

When several Instances work at once, each holds an exclusive mutation scope, so two of them never write the same thing. What that coordination produces — team membership, task queues, transient state — is runtime state and is never mistaken for project intent.

<br>

## Terms

- **Agent Native** — the core operational Agent supplied by the selected Agent Runtime; it receives the Human's request and hosts or coordinates its Agent Instances.
- **Agent Instance Definition** — one portable declaration of an executable Agent Instance identity and the Role and capabilities it realizes.
- **General Agent Instance** — the primary Agent Instance accountable to the Human for the complete authorized request.
- **Specialized Agent Instance** — an Agent Instance that realizes a bounded supporting Role under delegation or direct invocation.
- **Agent Role** — one bounded execution responsibility with defined authority, inputs, outputs, and stopping conditions.
- **Primary Role** — the role accountable to the Human for the active request.
- **Specialized Role** — a role delegated a focused responsibility within the parent's authority.
- **Delegation** — assignment of a bounded objective from one Agent to another under their declared Roles.
- **Team** — multiple independently executing Agents coordinated toward one authorized outcome.
- **Coordination Record** — transient runtime state used to assign, synchronize, and collect work.

## Relationships

- **Consumes Agent Runtime, Agent (formerly Role), Context, Skill, Tool, Permission, and Rule (formerly Session)** — selects the Agent Native and combines their contracts into executable Agent Instances without redefining them.
- **Consumed by Agent (formerly Coordination)** — supplies the concrete Agent Instances that may be delegated, teamed, or isolated.
- **Consumed by Agent Rule (formerly Observability)** — supplies the declarations against which the Agent Native and every Agent Instance realization are validated.
- **Consumes Agent Context, Skill, Tool, and Permission** — receives knowledge, workflow, capabilities, and authority needed to act.
- **Consumed by Agent** — supplies responsibilities that executable Agent Instance Definitions realize.
- **Consumed by Agent (formerly Coordination)** — supplies the responsibility boundaries preserved during delegation and teams.
- **Consumed by Agent Rule (formerly Observability)** — supplies the contract against which role outcomes are reported.
- **Consumes Agent (formerly Role), Context, Permission, and Rule (formerly Session)** — coordinates eligible Agent Instances while preserving Role, authority, and lifecycle boundaries.
- **Consumed by Agent Rule (formerly Observability)** — provides attribution and coordination outcomes.

Agent Native selection, Agent Instance declarations, primary Instance selection, Role assignments, models, tools, Skills, permissions, memory, isolation, and portable realization requirements belong to Agent Preferences. Native paths, file formats, and runtime-specific mappings are resolved by Agent Sync from the selected Agent Native.

Technical Role catalogs and primary Role selection belong to Agent Preferences (formerly Role Preferences). Agent Instance identities, native realizations, models, tools, Skills, and per-Instance configuration belong to Agent Preferences.

Technical team mechanisms, task systems, messaging, and isolation choices belong to Agent Preferences (formerly Coordination Preferences).

Every Principle in this file is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory.

<br>

### Every Agent Instance has one complete definition

**Rule:** Every required Agent Instance has one stable Agent Instance Definition declaring its identity, kind, assigned Role, native realization, capability assignments, configuration overrides, lifecycle behavior, and availability requirement. The Agent Native realizes that Definition without changing the contracts it references.

**Why:** A named Agent Instance is reproducible only when another Runtime can determine what it is expected to realize.

**Boundary:** Values inherited unchanged from Role, Runtime, or shared defaults are referenced rather than copied into the Agent Instance Definition.

<br>

### Agent Instance and Role remain separate

**Rule:** An Agent Instance Definition states who executes; an Agent Role states the responsibility executed. Every Agent Instance maps to at least one declared Role, and assigning a Role never transfers ownership of the Role contract into the Agent Instance.

**Why:** Several Agent Instances may realize the same Role differently, and one Agent Instance identity may be reconfigured without changing the responsibility itself.

**Boundary:** One Agent Instance may coordinate several Roles only when its assigned primary Role explicitly owns coordination of the complete outcome.

<br>

### `general` is the General Agent Instance

**Rule:** The Agent Preferences requires one General Agent Instance with the stable identity `general`. It realizes the primary execution Role, remains accountable to the Human, activates applicable capabilities, delegates bounded work when useful, integrates delegated evidence, and makes the final outcome claim.

**Why:** Every request needs one concrete accountable Agent Instance even when several Specialized Agent Instances contribute.

**Boundary:** General Agent Instance accountability never broadens request scope, Permission, or Component authority.

<br>

### Specialized Agent Instances remain bounded

**Rule:** Every Specialized Agent Instance maps to a declared supporting Role and receives only the Context, Skills, Tools, Permission, and lifecycle behavior required for that Role. It returns its result and evidence to the accountable General Agent Instance or direct invoker without expanding its own assignment.

**Why:** Multiple Agent Instances improve focus only when their responsibilities and capabilities remain inspectable and limited.

**Boundary:** A Specialized Agent Instance may use professional judgment inside its assigned Role but never becomes the General Agent Instance by delegation.

<br>

### Agent Native and Instance availability are proven in the selected Runtime

**Rule:** The Agent Native is available only when the selected Runtime exposes its core operational Agent. A required Agent Instance is available only when that Agent Native can instantiate or expose its native realization, assign its declared Role and capabilities, and successfully invoke it in the current project. A declaration or native file alone is not proof.

**Why:** Coordination cannot safely depend on an Agent Native or Agent Instance that exists only nominally.

**Boundary:** An incompatible or unavailable Agent Native or Agent Instance is reported explicitly and never approximated with broader authority.

<br>

### Every Agent Role has one bounded responsibility

**Rule:** Every Agent Role declares one responsibility, scope, authority, required inputs, expected outputs, and stopping conditions. A role never performs an adjacent responsibility or acquires authority merely because it discovers additional work.

**Why:** Bounded roles make behavior predictable and delegation reviewable.

**Boundary:** One role may coordinate several capabilities when coordination is its declared responsibility.

*Formerly Agent Role Principle "Every Agent Instance has one complete definition".*

<br>

### Role ownership is unambiguous

**Rule:** Each required responsibility maps to one primary Agent Role. Missing, duplicate, contradictory, or unreachable role ownership is invalid.

**Why:** Shared primary ownership makes accountability disappear.

**Boundary:** Supporting roles may contribute evidence without becoming co-owners of the final claim.

*Formerly Agent Role Principle "Agent Instance and Role remain separate".*

<br>

### The Primary Role remains accountable

**Rule:** The Primary Role remains accountable for integrating delegated results, resolving conflicts, preserving the Human's scope, and making the final outcome claim.

**Why:** Delegation must not leave the Human responsible for assembling unverified fragments.

**Boundary:** Accountability does not grant the Primary Role authority excluded by the active request or policy.

*Formerly Agent Role Principle "`general` is the General Agent Instance".*

<br>

### The primary execution role owns the requested outcome

**Rule:** The architecture requires one primary execution role whose purpose is accountable request completion, whose responsibility is to establish required Understanding, activate and coordinate applicable capabilities, preserve authority, and report an evidence-backed outcome, and whose task coverage is the complete authorized request.

**Why:** The Human needs one role accountable for the integrated result even when work is delegated.

**Boundary:** The primary execution role gains no authority beyond the request, applicable Permissions, and owning Component contracts.

*Formerly Agent Role Principle "Specialized Agent Instances remain bounded".*

<br>

### `interface-reader` reports without changing the observed state

**Rule:** The architecture requires the `interface-reader` specialized role whose purpose is current Interface status reporting, whose responsibility is to derive Workflow position, phase progress, plans, implementation, launch, blockers, questions, and Findings from current authorities and records, and whose task coverage is read-only observation and explanation.

**Why:** Status is trustworthy only when the reporter cannot change what it is observing.

**Boundary:** `interface-reader` never reads Agent Module sources, writes files, executes project work, repairs discrepancies, or invents missing facts. It consumes synchronized Runtime rules for Agent-side behavior.

*Formerly Agent Role Principle "Agent Native and Instance availability are proven in the selected Runtime".*

<br>

### Delegation preserves scope and authority

**Rule:** A delegation carries a bounded objective, minimum necessary context, expected result, evidence requirements, and no authority broader than the parent task permits. Delegation never bypasses ownership or approval.

**Why:** Parallel execution is safe only when every worker's mandate is explicit.

**Boundary:** A delegate may choose ordinary implementation details inside its assigned contract.

*Formerly Agent Coordination Principle "Every Agent Instance has one complete definition".*

<br>

### Concurrent work has exclusive mutation ownership

**Rule:** Concurrent roles receive non-overlapping mutation scopes or an explicit coordination rule for shared records. Conflicting results are reconciled by the accountable parent before integration.

**Why:** Uncoordinated writers create nondeterministic loss and false completion.

**Boundary:** Read-only investigation may overlap freely when it does not mutate shared state.

*Formerly Agent Coordination Principle "Agent Instance and Role remain separate".*

<br>

### Runtime coordination state is not project intent

**Rule:** Team membership, task queues, mailboxes, process identifiers, and other Coordination Records remain runtime state and are never treated as authored Interface definitions.

**Why:** Ephemeral execution mechanics must not become accidental project policy.

**Boundary:** Durable evidence and outcomes may be written to the record that owns them.

*Formerly Agent Coordination Principle "`general` is the General Agent Instance".*

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Every Agent Instance has one complete definition**

- **Must** — select one Agent Native supplied by the selected Agent Runtime
- **Must** — give every required Agent Instance one complete and stable Agent Instance Definition
- **Never** — let the Agent Native change the contracts referenced by an Agent Instance Definition

**Agent Instance and Role remain separate**

- **Must** — map every Agent Instance to a declared Role while keeping Instance identity and Role responsibility separate

**`general` is the General Agent Instance**

- **Must** — provide `general` as the General Agent Instance accountable for the complete authorized outcome
- **Never** — let General Agent Instance accountability broaden scope, Permission, or authority

**Specialized Agent Instances remain bounded**

- **Must** — keep every Specialized Agent Instance bounded to its supporting Role and required capabilities
- **Never** — let delegation turn a Specialized Agent Instance into the General Agent Instance

**Agent Native and Instance availability are proven in the selected Runtime**

- **Must** — prove the Agent Native and every required Agent Instance are usable in the selected Runtime
- **Never** — approximate an unavailable Agent Native or Agent Instance with broader authority

**Every Agent Role has one bounded responsibility**

- **Must** — give every Agent Role one complete bounded contract
- **Never** — let discovered work expand a role's authority

**Role ownership is unambiguous**

- **Must** — assign each required responsibility one primary owner
- **Never** — accept missing, duplicate, contradictory, or unreachable ownership

**The Primary Role remains accountable**

- **Must** — keep the Primary Role accountable for integration and the final claim

**The primary execution role owns the requested outcome**

- **Must** — provide one primary execution role accountable for the authorized request
- **Never** — let primary accountability expand authority

**`interface-reader` reports without changing the observed state**

- **Must** — provide `interface-reader` for read-only current status reporting
- **Never** — let `interface-reader` mutate, execute, repair, or invent project state
- **Never** — let `interface-reader` enter or inspect the Agent Module

**Delegation preserves scope and authority**

- **Must** — delegate bounded objectives, context, outputs, evidence, and authority
- **Never** — use delegation to bypass ownership or approval

**Concurrent work has exclusive mutation ownership**

- **Must** — coordinate mutation scopes and reconcile conflicts before integration

**Runtime coordination state is not project intent**

- **Never** — treat transient coordination state as project intent
