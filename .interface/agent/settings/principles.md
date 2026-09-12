# Agent Settings Principles

Agent Settings is the Component that declares how Agent configuration sources are scoped, combined, selected, and reconciled. It makes the effective configuration explainable without turning runtime files into a second source of project intent.

It owns configuration source precedence and reconciliation. It does not own the choices governed by other Agent Components.

## Terms

- **Configuration Source** — one location or invocation layer that contributes Agent settings.
- **Effective Setting** — the value produced after all applicable sources and merge rules are resolved.
- **Reconciliation** — comparison of declared choices with observed runtime configuration.

## Relationships

- **Consumes every Agent Component** — receives the choices each Component owns.
- **Consumed by Agent Runtime** — provides the configuration that the runtime applies.
- **Consumed by Agent Observability** — provides expected values for diagnostics.

Technical source scopes, merge behavior, and native locations belong to Agent Settings Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every effective setting has an explainable source

**Rule:** Configuration sources, their scopes, precedence, and merge behavior are explicit. Every Effective Setting can be traced to the sources that produced it.

**Why:** Hidden precedence makes identical project files behave differently without an actionable explanation.

**Boundary:** This Component explains resolution but does not override a stricter authority owned elsewhere.

<br>

## 2. Reconciliation preserves ownership

**Rule:** Reconciliation compares current declarations with actual runtime state, reports drift, and changes only the runtime artifacts it is authorized to manage. Resolved runtime state is never written back as a new human-owned decision.

**Why:** Synchronization must not convert observations into policy.

**Boundary:** A runtime-provided default may be observed without being adopted as a project Preference.

<br>

## 3. Empty configuration categories are explicit

**Rule:** Every supported configuration category exists in the Agent Profile even when it currently contains no entries. Empty means declared and unused, not unknown or forgotten.

**Why:** A complete profile distinguishes absence from omission.

**Boundary:** Explicit emptiness does not require activating or configuring the category.

<br>

## 4. Project capabilities travel with the project

**Rule:** Every project-specific Agent, Role, Skill, Command, Rule, Tool declaration, Hook, Integration, Extension, interaction choice, permission policy, and required configuration is stored in or declared by the project so a compatible Agent Runtime can reconstruct the same Agent Profile. Secret values and machine credentials never travel in that declaration.

**Why:** Agent behavior must not depend on undocumented user configuration or one machine's hidden state.

**Boundary:** A project declaration may reference runtime- or user-provided infrastructure without claiming to own or transport it.

<br>

## 5. Every required capability has one owner and a provable status

**Rule:** Every required Agent responsibility maps to one owning Component and one reachable Capability Contract. Its availability status is established from current runtime observation; missing, duplicate, contradictory, unreachable, inactive, or unverified mappings remain explicit and never become available by assumption.

**Why:** A complete catalog is useful only when responsibility and actual usability are unambiguous.

**Boundary:** Several capabilities may collaborate when exactly one contract remains accountable for the required responsibility.

<br>

## At a Glance

- **Must** — make source scope, precedence, merge behavior, and effective origin explicit *(1)*
- **Must** — reconcile declarations with runtime state without changing ownership *(2)*
- **Never** — turn an observed runtime value into a human-owned decision *(2)*
- **Must** — represent every supported configuration category, including empty ones *(3)*
- **Must** — store or declare every project-specific Agent capability and policy at project scope *(4)*
- **Never** — store secret values or machine credentials in the portable declaration *(4)*
- **Must** — map every required responsibility to one owner and one reachable Capability Contract *(5)*
- **Never** — infer availability from a missing, conflicting, inactive, or unverified mapping *(5)*
