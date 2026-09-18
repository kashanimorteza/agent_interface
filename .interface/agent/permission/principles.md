# Agent Permission Principles

Agent Permission is the Component that governs what Agent Roles and capabilities may read, change, execute, connect to, or disclose. It combines authorization policy, sandbox boundaries, trust decisions, and secret handling.

It owns enforceable access decisions. It does not own Human intent, external account authority, or a capability's functional contract.

On 2026-09-17 the former Hook Component was merged into this Component: a Hook is one native way of guaranteeing a boundary, and the guarantee — a behavior that must happen deterministically, without the model's discretion — is a Permission concern. The Agent Native chooses whether to realize a declared guarantee with a hook, a deny rule, a sandbox, or another mechanism; the Preferences may suggest one per Native. Nothing was dropped; each absorbed Principle keeps its former number in a note.

*Absorbed from the former Agent Hook Component on 2026-09-17 — its introduction, kept verbatim:* Agent Hook is the Component that performs deterministic automation at declared lifecycle events. A Hook may observe, validate, block, transform, notify, or trigger a bounded capability independently of an Agent Native's or Agent Instance's discretionary reasoning.

It owns event matching, handler order, inputs, effects, and failure behavior. It does not own the workflow it observes or broader authority than the triggering event permits.

## Terms

- **Permission** — an enforceable allow, ask, or deny decision for an action or resource.
- **Authorization** — approval from the authority entitled to permit a scoped action.
- **Sandbox** — an enforced execution boundary restricting filesystem, network, or process access.
- **Enforced Guarantee** — a behavior that must happen deterministically, without the model's discretion; realized by the Native through its own mechanism (a hook, a permission rule, a sandbox rule). *(formerly Hook — an event-bound handler executed when a matching lifecycle event occurs)*
- **Event** — a named observable point in Agent or Tool execution.
- **Blocking Guarantee** — an Enforced Guarantee authorized to prevent or reject the triggering action. *(formerly Blocking Hook)*

## Relationships

- **Consumes Human authorization and Agent (formerly Role) scope** — derives the maximum permitted action boundary.
- **Consumed by every executing Agent Component** — constrains all reads, mutations, execution, and connections.
- **Consumed by Agent Permission (formerly Hook) and Rule (formerly Observability)** — supplies enforceable decisions and auditable outcomes.
- **Consumes Agent Rule (formerly Session), Tool, Connection (formerly Integration), and Permission** — reacts to events using authorized handlers.
- **Consumed by Agent Rule (including former Observability)** — enforces guarantees and emits lifecycle evidence.

Technical modes, permission rules, sandbox settings, trust policy, and credential references belong to Agent Permission Preferences.

Technical events, matchers, handlers, timeouts, and native configuration belong to the `native.<agent-native>` block of each Enforced Guarantee in Agent Permission Preferences (formerly Hook Preferences).

Every statement here is mandatory. Preferences can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Interface is read-only except for authorized Config records

**Rule:** The entire Interface is read-only to every Agent Role and Skill by default. Only operational records inside the Interface Config boundary may be changed, and only by a Skill whose declared responsibility and owning Component grant authority over that exact record. Privileged, irreversible, destructive, external, or materially scope-expanding actions additionally require the authorization applicable to their impact.

**Why:** New or moved Interface sources remain protected automatically, while operational workflow records remain maintainable by their authorized owners.

**Boundary:** Human authorship is outside Agent execution. The Config exception grants no write access to any other Interface path, and safe read-only inspection remains available within applicable read restrictions.

<br>

## 2. Permission is least-privilege and deny-safe

**Rule:** Every capability receives only the minimum access required by its contract. Deny rules and stricter authorities take precedence; no lower layer or delegated role can broaden them.

**Why:** Broad ambient access turns a bounded mistake into a system-wide one.

**Boundary:** A Human may explicitly authorize broader access for a defined scope and duration.

<br>

## 3. Agent Module reads belong only to the explicit Agent Native Skill

**Rule:** Access to Agent Module sources is denied except within the exact prompt created when the Human directly invokes the declared `agent-native` Runtime entry point. The Agent Native, every Agent Instance, Skill, coordinator, enforcement handler, lifecycle routine, automation, and model-generated action can neither invoke the Agent Native Skill nor create, inherit, borrow, or simulate its access grant. In its sync modes the Skill reads those Human-owned declarations to produce self-contained project-scoped Runtime realizations; in its install mode it reads them to resolve which capabilities must be transferred or provisioned. Every other consumer uses only the last synchronized Runtime artifacts, and a missing artifact is reported as Runtime drift rather than resolved from the Agent Module.

**Why:** The Agent Module defines how an Agent Native and its Agent Instances should be constructed; it is not their operational context after synchronization.

**Boundary:** Reading the canonical Interface file, seeing its Agent Structure, or receiving a Human request to edit an Agent Module declaration does not authorize synchronization. This restriction does not prevent the Human from reading or editing Human-owned sources; synchronization requires a separate direct Human invocation of the declared entry point.

<br>

## 4. Secrets never enter project declarations or reports

**Rule:** Credentials, tokens, private keys, and secret values remain in approved external stores or runtime channels and are never committed, copied into project declarations, logged, or exposed in Agent output.

**Why:** Portable Agent profiles must not transport machine or account secrets.

**Boundary:** Non-secret references naming an approved credential source may be declared.

<br>

## 5. Unrelated Human work is preserved

**Rule:** Agent actions preserve unrelated Human changes and data. Destructive operations resolve exact targets and use recoverable mechanisms when practical.

**Why:** Task authority does not imply ownership of everything reachable from the environment.

**Boundary:** Explicitly authorized cleanup may remove confirmed targets and must report what was removed.

<br>

## 6. An Enforced Guarantee is deterministic and bounded

**Rule:** Every Enforced Guarantee declares what it guarantees, the Event it binds to, its allowed effects, its failure policy, and whether it may block; the Native adds its own mechanics (matcher, handler type, inputs, timeout, exit behavior) under `native.<agent-native>`. Matching the same unchanged event produces the same policy outcome.

**Why:** Enforced Guarantees are used when behavior must occur reliably rather than at model discretion.

**Boundary:** A prompt- or agent-backed handler may reason internally but remains bounded by the guarantee's declaration.

*Formerly Agent Hook Principle 1.*

<br>

## 7. Guarantees fail visibly and safely

**Rule:** A guarantee's failure, timeout, malformed output, and denied execution have an explicit fail-open or fail-closed policy and become observable. Security and integrity controls fail closed unless a stricter authority explicitly defines otherwise.

**Why:** A guarantee that fails silently creates the appearance of enforcement without the protection.

**Boundary:** Notification-only guarantees may fail open when their failure cannot alter correctness or security.

*Formerly Agent Hook Principle 2.*

<br>

## 8. A guarantee's authority does not expand on trigger

**Rule:** An Event authorizes only the effects declared for its Enforced Guarantee. A trigger never grants broader file, network, external-service, or workflow authority.

**Why:** Automatic execution magnifies hidden scope expansion.

**Boundary:** An Enforced Guarantee may request Human authorization and stop pending that decision.

*Formerly Agent Hook Principle 3.*

<br>

## At a Glance

- **Never** — modify any Interface path outside the operational Config boundary *(1)*
- **Must** — restrict Config writes to the exact records owned by the active Skill's responsibility *(1)*
- **Must** — obtain applicable authorization for materially consequential actions *(1)*
- **Must** — grant every capability only its minimum required access *(2)*
- **Never** — let a lower layer or delegate broaden a deny boundary *(2)*
- **Must** — reserve every Agent Module read for the exact prompt created by direct Human invocation of `agent-native` *(3)*
- **Never** — let any non-Human mechanism invoke the Agent Native Skill or create, inherit, borrow, or simulate its access grant *(3)*
- **Never** — use Agent Module sources as ordinary Understanding or as a fallback for Runtime drift *(3)*
- **Never** — store or expose secret values in project declarations, logs, or output *(4)*
- **Must** — preserve unrelated Human work and resolve destructive targets exactly *(5)*
- **Must** — declare every Enforced Guarantee's Event, effects, failure policy, and blocking behavior, leaving matcher, handler, and timeout to the Native block *(6)*
- **Must** — make a guarantee's failure visible and give it an explicit failure policy *(7)*
- **Must** — fail closed for security and integrity controls *(7)*
- **Never** — let an Event expand a guarantee's authority *(8)*
