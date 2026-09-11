# Agent Coordination Principles

Agent Coordination is the Component that organizes work across multiple Agent Roles, sessions, tasks, and isolated workspaces. It defines delegation, communication, synchronization, and integration without redefining the roles being coordinated.

It owns coordination protocol and conflict boundaries. It does not own role contracts, project Plans, or implementation decisions.

## Terms

- **Delegation** — assignment of a bounded objective from one Agent Role to another.
- **Team** — multiple independently executing Agent Roles coordinated toward one authorized outcome.
- **Coordination Record** — transient runtime state used to assign, synchronize, and collect work.

## Relationships

- **Consumes Agent Role, Context, Permission, and Session** — coordinates eligible roles within current authority and lifecycle.
- **Consumed by Agent Observability** — provides attribution and coordination outcomes.

Technical team mechanisms, task systems, messaging, and isolation choices belong to Agent Coordination Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Delegation preserves scope and authority

**Rule:** A delegation carries a bounded objective, minimum necessary context, expected result, evidence requirements, and no authority broader than the parent task permits. Delegation never bypasses ownership or approval.

**Why:** Parallel execution is safe only when every worker's mandate is explicit.

**Boundary:** A delegate may choose ordinary implementation details inside its assigned contract.

<br>

## 2. Concurrent work has exclusive mutation ownership

**Rule:** Concurrent roles receive non-overlapping mutation scopes or an explicit coordination rule for shared records. Conflicting results are reconciled by the accountable parent before integration.

**Why:** Uncoordinated writers create nondeterministic loss and false completion.

**Boundary:** Read-only investigation may overlap freely when it does not mutate shared state.

<br>

## 3. Runtime coordination state is not project intent

**Rule:** Team membership, task queues, mailboxes, process identifiers, and other Coordination Records remain runtime state and are never treated as authored Interface definitions.

**Why:** Ephemeral execution mechanics must not become accidental project policy.

**Boundary:** Durable evidence and outcomes may be written to the record that owns them.

<br>

## At a Glance

- **Must** — delegate bounded objectives, context, outputs, evidence, and authority *(1)*
- **Never** — use delegation to bypass ownership or approval *(1)*
- **Must** — coordinate mutation scopes and reconcile conflicts before integration *(2)*
- **Never** — treat transient coordination state as project intent *(3)*
