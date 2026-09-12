# Agent Tool Principles

Agent Tool is the Component that defines atomic executable capabilities assigned to Agent Definitions for use within their Roles, whether supplied by the runtime or an approved integration. Tools perform bounded actions; Skills compose them into reasoned workflows.

It owns tool identity, action boundaries, inputs, outputs, and availability. It does not own workflow decisions or permission policy.

## Terms

- **Tool** — an atomic callable capability exposed to an Agent Role.
- **Tool Contract** — a Tool's accepted inputs, effects, outputs, failure modes, and permission class.
- **Tool Availability** — verified discoverability and usability in the current runtime and scope.

## Relationships

- **Consumes Agent Runtime, Integration, and Permission** — receives implementations, external capabilities, and execution authority.
- **Consumed by Agent, Role, Skill, and Hook** — provides bounded actions they can invoke.

Technical tool catalogs, mappings, and availability expectations belong to Agent Tool Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Tool has an atomic contract

**Rule:** Every Tool declares its inputs, observable effects, outputs, failure modes, scope, and permission class. A Tool performs one atomic capability and never embeds an undeclared project workflow.

**Why:** Atomic capabilities can be permissioned, composed, and verified independently.

**Boundary:** One call may perform several internal operations when they form one indivisible external action.

<br>

## 2. Tool availability is observed

**Rule:** A Tool is available only when the intended Agent Role can discover and successfully call it in the required scope. Presence in a catalog or provider claim alone is insufficient.

**Why:** A declared Tool may still be disconnected, unauthorized, incompatible, or hidden from a role.

**Boundary:** A non-mutating capability check may substitute for a full action when the real action would be unsafe or irreversible.

<br>

## At a Glance

- **Must** — give every Tool one atomic contract with effects and permission class *(1)*
- **Never** — hide an undeclared project workflow inside a Tool *(1)*
- **Must** — verify Tool availability from the intended role and scope *(2)*
- **Never** — infer availability from a catalog or provider claim *(2)*
