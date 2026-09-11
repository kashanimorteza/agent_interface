# Agent Rule Principles

Agent Rule is the Component that defines persistent behavioral instructions applied across sessions or within a declared path scope. Rules adapt Agent behavior to stable project conventions without becoming enforcement mechanisms or copies of owned Interface sources.

It owns instruction scope, loading conditions, and precedence among Rules. It does not own security enforcement, workflow implementation, or project definitions.

## Terms

- **Agent Rule** — persistent behavioral guidance loaded for all work or a matching scope.
- **Scoped Rule** — an Agent Rule activated only for declared paths or conditions.
- **Rule Conflict** — two applicable instructions that cannot both be satisfied.

## Relationships

- **Consumes Target, Developer, and Agent Modules** — references their authorities without redefining them.
- **Consumed by Agent Context and Skill** — supplies persistent applicable guidance.
- **Consumed by Agent Permission and Hook** — provides behavioral context while those Components supply enforceable controls.

Technical Rule files, scopes, load order, and native locations belong to Agent Rule Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Rules guide behavior without replacing authority

**Rule:** An Agent Rule states stable behavioral guidance concisely and points to the current owner of project facts, structures, choices, and workflows. It never copies or overrides those sources.

**Why:** Always-loaded copies consume context and become stale competing authorities.

**Boundary:** A Rule may state how to locate and apply an authority.

<br>

## 2. Rule scope and conflict are explicit

**Rule:** Every Agent Rule declares whether it is global or scoped and the exact condition under which it applies. Applicable conflicts are reported and resolved by authority and declared precedence, never by arbitrary load order.

**Why:** Silent conditional instructions make Agent behavior unpredictable.

**Boundary:** More specific guidance may refine a broader Rule when both can be satisfied.

<br>

## 3. Security boundaries use enforcement

**Rule:** A behavior that must be guaranteed is enforced by Agent Permission, sandboxing, or an applicable Hook rather than relying only on an Agent Rule.

**Why:** Instructions influence model behavior but do not constitute deterministic enforcement.

**Boundary:** Rules may explain an enforced boundary and how to work within it.

<br>

## At a Glance

- **Must** — keep Rules concise and refer to current owners *(1)*
- **Never** — copy or override project authorities in a Rule *(1)*
- **Must** — declare Rule scope, activation, and conflict resolution *(2)*
- **Never** — resolve conflicts through arbitrary load order *(2)*
- **Must** — place guaranteed boundaries in enforceable mechanisms *(3)*
