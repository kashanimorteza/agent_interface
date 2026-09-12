# Agent Role Principles

Agent Role is the Component that defines the execution responsibilities available within an Agent Profile, including the primary role and specialized delegated roles. It gives each role a stable contract independent of the runtime that hosts it.

It owns role responsibilities and boundaries. It does not own Agent identities, native definitions, capability configuration, workflow content, runtime configuration, or coordination state.

## Terms

- **Agent Role** — one bounded execution responsibility with defined authority, inputs, outputs, and stopping conditions.
- **Primary Role** — the role accountable to the Human for the active request.
- **Specialized Role** — a role delegated a focused responsibility within the parent's authority.

## Relationships

- **Consumes Agent Context, Skill, Tool, and Permission** — receives knowledge, workflow, capabilities, and authority needed to act.
- **Consumed by Agent** — supplies responsibilities that executable Agent Definitions realize.
- **Consumed by Agent Coordination** — supplies the responsibility boundaries preserved during delegation and teams.
- **Consumed by Agent Observability** — supplies the contract against which role outcomes are reported.

Technical Role catalogs and primary Role selection belong to Agent Role Preferences. Agent identities, native definitions, models, tools, Skills, and per-Agent configuration belong to Agent Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Agent Role has one bounded responsibility

**Rule:** Every Agent Role declares one responsibility, scope, authority, required inputs, expected outputs, and stopping conditions. A role never performs an adjacent responsibility or acquires authority merely because it discovers additional work.

**Why:** Bounded roles make behavior predictable and delegation reviewable.

**Boundary:** One role may coordinate several capabilities when coordination is its declared responsibility.

<br>

## 2. Role ownership is unambiguous

**Rule:** Each required responsibility maps to one primary Agent Role. Missing, duplicate, contradictory, or unreachable role ownership is invalid.

**Why:** Shared primary ownership makes accountability disappear.

**Boundary:** Supporting roles may contribute evidence without becoming co-owners of the final claim.

<br>

## 3. The Primary Role remains accountable

**Rule:** The Primary Role remains accountable for integrating delegated results, resolving conflicts, preserving the Human's scope, and making the final outcome claim.

**Why:** Delegation must not leave the Human responsible for assembling unverified fragments.

**Boundary:** Accountability does not grant the Primary Role authority excluded by the active request or policy.

<br>

## 4. The primary execution role owns the requested outcome

**Rule:** The architecture requires one primary execution role whose purpose is accountable request completion, whose responsibility is to establish required Understanding, activate and coordinate applicable capabilities, preserve authority, and report an evidence-backed outcome, and whose task coverage is the complete authorized request.

**Why:** The Human needs one role accountable for the integrated result even when work is delegated.

**Boundary:** The primary execution role gains no authority beyond the request, applicable Permissions, and owning Component contracts.

<br>

## 5. `interface-reader` reports without changing the observed state

**Rule:** The architecture requires the `interface-reader` specialized role whose purpose is current Interface status reporting, whose responsibility is to derive Workflow position, phase progress, plans, implementation, launch, blockers, questions, and Findings from current authorities and records, and whose task coverage is read-only observation and explanation.

**Why:** Status is trustworthy only when the reporter cannot change what it is observing.

**Boundary:** `interface-reader` never writes files, executes project work, repairs discrepancies, or invents missing facts.

<br>

## At a Glance

- **Must** — give every Agent Role one complete bounded contract *(1)*
- **Never** — let discovered work expand a role's authority *(1)*
- **Must** — assign each required responsibility one primary owner *(2)*
- **Never** — accept missing, duplicate, contradictory, or unreachable ownership *(2)*
- **Must** — keep the Primary Role accountable for integration and the final claim *(3)*
- **Must** — provide one primary execution role accountable for the authorized request *(4)*
- **Never** — let primary accountability expand authority *(4)*
- **Must** — provide `interface-reader` for read-only current status reporting *(5)*
- **Never** — let `interface-reader` mutate, execute, repair, or invent project state *(5)*
