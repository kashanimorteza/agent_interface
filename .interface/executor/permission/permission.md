# Agent Permission Definition

Agent Permission is the Executor Component that defines the enforceable boundaries controlling what an Agent may read, change, execute, connect to, or disclose.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Layering](#layering)**
4. **[Authority](#authority)**
5. **[Principles](#principles)**
6. **[Review](#review)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Agent Permission governs what Agent Instances and capabilities may read, change, execute, connect to, or disclose. It defines authorization policy (allow, ask, and deny), sandbox boundaries, trust decisions, authentication, secret handling, and deterministic event-driven Enforced Guarantees.

It owns enforceable access decisions and deterministic boundaries. It does not own Human intent, external account authority, or a capability's functional contract.

### Purpose

Every other Executor Component describes something the Agent can do. This one describes what it may do — and, more importantly, what must happen whether or not the model decides to do it.

Two concerns turn out to be the same concern. Authorization asks whether an action is allowed: which paths are writable, which commands may run, which external systems may be reached, which secrets may be seen. An Enforced Guarantee asks whether a behavior happens without discretion: a check that always runs, a boundary that always blocks, a record that is always written. Both are answers to *the model does not get to decide this*, so both are owned here.

The Component exists because a boundary that depends on good reasoning is not a boundary. An Agent that is merely instructed not to write to the Interface will, under the right prompt, write to the Interface. An Agent that cannot is a different thing entirely.

### How It Works

Access starts closed. The Interface is read-only to every Agent Instance and Skill; operational Config records live outside it, in `.config/` at the project root. Everything beyond that is granted by contract: each capability receives the minimum its declared work requires, deny always wins over allow, and no delegated Agent Instance or lower layer can widen what it was given.

The Executor Module is protected by an explicit Human-only read boundary. Permission enforces that boundary; Agent Native Implement performs the authorized read and produces the Native realization, while every other consumer uses the realized Native artifacts.

Enforced Guarantees cover what authorization alone cannot. A guarantee declares the behavior that must occur and the point at which it occurs; the Agent Native chooses the mechanism — a hook, a deny rule, a sandbox constraint — and the Module never records that choice. A guarantee is deterministic and bounded, carries no authority beyond what its trigger permits, and when it cannot run it fails visibly and safely rather than quietly passing.

Secrets are never values in a declaration. A declaration references a credential source; the value stays where the authority that owns it keeps it. Human authorship sits outside all of this: these rules govern Agent execution, not what the Human writes.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Permission** — an enforceable allow, ask, or deny decision for an action or resource.
- **Authorization** — approval from the authority entitled to permit a scoped action.
- **Sandbox** — an enforced execution boundary restricting filesystem, network, or process access.
- **Enforced Guarantee** — a behavior that must happen deterministically, without the model's discretion; realized by the Native through its own mechanism, such as a hook, permission rule, or sandbox rule.
- **Event** — a named observable point in Agent or Tool execution.
- **Blocking Guarantee** — an Enforced Guarantee authorized to prevent or reject the triggering action.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

This Definition carries the portable meaning and mandatory Principles of the Permission Component. Preferences carry current permission selections, rules, protected sources, secret handling, and enforced guarantees. Agent Native Implement reads both and realizes them without changing their scope or authority.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Human owns this Definition and its Preferences. Every Principle in this file is mandatory; Preferences can never override a Principle, and Agent Native Implement is the only reader authorized to realize the Component in an Agent Native.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Interface is read-only

**Rule:** The entire Interface is read-only to every Agent Instance and Skill by default. Privileged, irreversible, destructive, external, or materially scope-expanding actions additionally require the authorization applicable to their impact.

**Why:** New or moved Interface sources remain protected automatically, while operational Config records live outside it in `.config/` at the project root.

**Boundary:** Human authorship is outside Agent execution. Safe read-only inspection remains available within applicable read restrictions.

<br>

### Permission is least-privilege and deny-safe

**Rule:** Every capability receives only the minimum access required by its contract. Deny rules and stricter authorities take precedence; no lower layer or delegated Agent Instance can broaden them.

**Why:** Broad ambient access turns a bounded mistake into a system-wide one.

**Boundary:** A Human may explicitly authorize broader access for a defined scope and duration.

<br>

### Executor Module reads belong only to the explicit Agent Native Implement

**Rule:** Access to Executor Module sources is denied except within the exact prompt created when the Human directly invokes Agent Native Implement. The Agent Native, every Agent Instance, Skill, coordinator, enforcement handler, lifecycle routine, automation, and model-generated action can neither invoke Agent Native Implement nor create, inherit, borrow, or simulate its access grant. Agent Native Implement reads those Human-owned declarations to produce self-contained project-scoped Native realizations. Every other consumer uses only the last realized Native artifacts, and a missing artifact is reported as Native drift rather than resolved from the Executor Module.

**Why:** The Executor Module defines how an Agent Native and its Agent Instances should be constructed; it is not their operational context after Agent Native Implement.

**Boundary:** Reading the canonical Interface file, seeing its Executor Structure, or receiving a Human request to edit an Executor Module declaration does not authorize Agent Native Implement. This restriction does not prevent the Human from reading or editing Human-owned sources; Agent Native Implement requires a separate direct Human invocation of the declared entry point.

<br>

### Secrets never enter project declarations or reports

**Rule:** Credentials, tokens, private keys, and secret values remain in approved external stores or runtime channels and are never committed, copied into project declarations, logged, or exposed in Agent output.

**Why:** Portable Agent profiles must not transport machine or account secrets.

**Boundary:** Non-secret references naming an approved credential source may be declared.

<br>

### Unrelated Human work is preserved

**Rule:** Agent actions preserve unrelated Human changes and data. Destructive operations resolve exact targets and use recoverable mechanisms when practical.

**Why:** Task authority does not imply ownership of everything reachable from the environment.

**Boundary:** Explicitly authorized cleanup may remove confirmed targets and must report what was removed.

<br>

### An Enforced Guarantee is deterministic and bounded

**Rule:** Every Enforced Guarantee declares what it guarantees, the Event it binds to, its allowed effects, its failure policy, and whether it may block; the Native chooses its own mechanics (matcher, handler type, inputs, timeout, exit behavior) without recording them in the Module. Matching the same unchanged event produces the same policy outcome.

**Why:** Enforced Guarantees are used when behavior must occur reliably rather than at model discretion.

**Boundary:** A prompt- or agent-backed handler may reason internally but remains bounded by the guarantee's declaration.

<br>

### Guarantees fail visibly and safely

**Rule:** A guarantee's failure, timeout, malformed output, and denied execution have an explicit fail-open or fail-closed policy and become observable. Security and integrity controls fail closed unless a stricter authority explicitly defines otherwise.

**Why:** A guarantee that fails silently creates the appearance of enforcement without the protection.

**Boundary:** Notification-only guarantees may fail open when their failure cannot alter correctness or security.

<br>

### A guarantee's authority does not expand on trigger

**Rule:** An Event authorizes only the effects declared for its Enforced Guarantee. A trigger never grants broader file, network, external-service, or workflow authority.

**Why:** Automatic execution magnifies hidden scope expansion.

**Boundary:** An Enforced Guarantee may request Human authorization and stop pending that decision.

<br>

<!--------------------------------------------------------------------------------- Review --->
## Review

### Conformance

- Every Principle above is realized in the Agent Native.

### Checks

- Effective allow, ask, and deny rules match their declarations.
- Every required Enforced Guarantee is realized, and its probe and any allow_probe pass; a failed probe means the guarantee is not realized.
- No project declaration contains a credential or secret value.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Interface is read-only**

- **Never** — modify any Interface path
- **Must** — obtain applicable authorization for materially consequential actions

**Permission is least-privilege and deny-safe**

- **Must** — grant every capability only its minimum required access
- **Never** — let a lower layer or delegate broaden a deny boundary

**Executor Module reads belong only to the explicit Agent Native Implement**

- **Must** — reserve every Executor Module read for the exact prompt created by direct Human invocation of Agent Native Implement
- **Never** — let any non-Human mechanism invoke Agent Native Implement or create, inherit, borrow, or simulate its access grant
- **Never** — use Executor Module sources as ordinary Understanding or as a fallback for Runtime drift

**Secrets never enter project declarations or reports**

- **Never** — store or expose secret values in project declarations, logs, or output

**Unrelated Human work is preserved**

- **Must** — preserve unrelated Human work and resolve destructive targets exactly

**An Enforced Guarantee is deterministic and bounded**

- **Must** — declare every Enforced Guarantee's Event, effects, failure policy, and blocking behavior, leaving matcher, handler, and timeout to the Native block

**Guarantees fail visibly and safely**

- **Must** — make a guarantee's failure visible and give it an explicit failure policy
- **Must** — fail closed for security and integrity controls

**A guarantee's authority does not expand on trigger**

- **Never** — let an Event expand a guarantee's authority
