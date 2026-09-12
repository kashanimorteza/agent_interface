# Agent Session Principles

Agent Session is the Component that governs one continuous or resumable period of Agent execution. It defines lifecycle, identity, state continuity, background work, resumption, isolation, and termination behavior.

It owns session lifecycle and transient execution continuity. It does not own project state, authored definitions, or durable Workflow records.

## Terms

- **Session** — one identifiable period of Agent interaction and execution.
- **Resume** — continuation of an existing Session with its available conversation and runtime state.
- **Background Work** — execution that continues without occupying the active interaction path.

## Relationships

- **Consumes Agent Runtime, Agent, Context, Role, and Permission** — hosts an Agent Definition executing with current context and authority.
- **Consumed by Agent Coordination, Hook, Interaction, and Observability** — supplies lifecycle events and execution identity.

Technical session options, persistence, resume policy, isolation, and background behavior belong to Agent Session Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Session state is not authoritative project state

**Rule:** Conversation history, session identifiers, transient tasks, cached context, and background process state never replace authored Interface sources or owned operational records.

**Why:** Sessions can be lost, compacted, forked, or resumed with incomplete state.

**Boundary:** Session state may be used as evidence after it is revalidated against current sources.

<br>

## 2. Resume revalidates before mutation

**Rule:** A resumed, forked, restored, or background Session re-establishes required Context, active scope, permissions, filesystem state, and outstanding work before making new mutations.

**Why:** External state may change while a Session is inactive or isolated.

**Boundary:** Read-only orientation may occur before full mutation readiness is established.

<br>

## 3. Session termination exposes unfinished work

**Rule:** Before a Session claims completion or terminates managed Background Work, it exposes unfinished responsibilities, running work, blockers, and required Human actions. It never abandons authorized work while presenting success.

**Why:** Invisible lifecycle endings make continuation unsafe.

**Boundary:** An explicitly cancelled Session reports cancellation rather than completing its original objective.

<br>

## At a Glance

- **Never** — treat transient Session state as authoritative project state *(1)*
- **Must** — revalidate context, scope, permission, files, and work before resumed mutation *(2)*
- **Must** — expose unfinished and running work before completion or termination *(3)*
- **Never** — abandon unfinished work while reporting success *(3)*
