# Agent Hook Principles

Agent Hook is the Component that performs deterministic automation at declared lifecycle events. A Hook may observe, validate, block, transform, notify, or trigger a bounded capability independently of the Agent's discretionary reasoning.

It owns event matching, handler order, inputs, effects, and failure behavior. It does not own the workflow it observes or broader authority than the triggering event permits.

## Terms

- **Hook** — an event-bound handler executed when a matching lifecycle event occurs.
- **Event** — a named observable point in Agent or Tool execution.
- **Blocking Hook** — a Hook authorized to prevent or reject the triggering action.

## Relationships

- **Consumes Agent Session, Tool, Integration, and Permission** — reacts to events using authorized handlers.
- **Consumed by Agent Rule and Observability** — enforces guarantees and emits lifecycle evidence.

Technical events, matchers, handlers, timeouts, and native configuration belong to Agent Hook Profile.

Every statement here is mandatory. A Profile can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Hook behavior is deterministic and bounded

**Rule:** Every Hook declares its Event, matcher, handler type, inputs, allowed effects, timeout, exit behavior, and whether it may block. Matching the same unchanged event produces the same policy outcome.

**Why:** Hooks are used when behavior must occur reliably rather than at model discretion.

**Boundary:** A prompt- or agent-backed handler may reason internally but remains bounded by the Hook contract.

<br>

## 2. Hooks fail visibly and safely

**Rule:** Hook failure, timeout, malformed output, and denied execution have an explicit fail-open or fail-closed policy and become observable. Security and integrity controls fail closed unless a stricter authority explicitly defines otherwise.

**Why:** Silent Hook failure creates the appearance of enforcement without the protection.

**Boundary:** Notification-only Hooks may fail open when their failure cannot alter correctness or security.

<br>

## 3. Hook authority does not expand on trigger

**Rule:** An Event authorizes only the effects declared for its Hook. A trigger never grants broader file, network, external-service, or workflow authority.

**Why:** Automatic execution magnifies hidden scope expansion.

**Boundary:** A Hook may request Human authorization and stop pending that decision.

<br>

## At a Glance

- **Must** — declare every Hook's event, matcher, effects, timeout, and blocking behavior *(1)*
- **Must** — make Hook failure visible and give it an explicit failure policy *(2)*
- **Must** — fail closed for security and integrity controls *(2)*
- **Never** — let an Event expand the Hook's authority *(3)*
