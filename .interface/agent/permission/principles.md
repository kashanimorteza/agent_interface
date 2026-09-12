# Agent Permission Principles

Agent Permission is the Component that governs what Agent Roles and capabilities may read, change, execute, connect to, or disclose. It combines authorization policy, sandbox boundaries, trust decisions, and secret handling.

It owns enforceable access decisions. It does not own Human intent, external account authority, or a capability's functional contract.

## Terms

- **Permission** — an enforceable allow, ask, or deny decision for an action or resource.
- **Authorization** — approval from the authority entitled to permit a scoped action.
- **Sandbox** — an enforced execution boundary restricting filesystem, network, or process access.

## Relationships

- **Consumes Human authorization and Agent Role scope** — derives the maximum permitted action boundary.
- **Consumed by every executing Agent Component** — constrains all reads, mutations, execution, and connections.
- **Consumed by Agent Hook and Observability** — supplies enforceable decisions and auditable outcomes.

Technical modes, permission rules, sandbox settings, trust policy, and credential references belong to Agent Permission Profile.

Every statement here is mandatory. A Profile can never override a Principle, and a project may only add stricter rules, never looser ones.

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

## 3. Secrets never enter project declarations or reports

**Rule:** Credentials, tokens, private keys, and secret values remain in approved external stores or runtime channels and are never committed, copied into project declarations, logged, or exposed in Agent output.

**Why:** Portable Agent profiles must not transport machine or account secrets.

**Boundary:** Non-secret references naming an approved credential source may be declared.

<br>

## 4. Unrelated Human work is preserved

**Rule:** Agent actions preserve unrelated Human changes and data. Destructive operations resolve exact targets and use recoverable mechanisms when practical.

**Why:** Task authority does not imply ownership of everything reachable from the environment.

**Boundary:** Explicitly authorized cleanup may remove confirmed targets and must report what was removed.

<br>

## At a Glance

- **Never** — modify any Interface path outside the operational Config boundary *(1)*
- **Must** — restrict Config writes to the exact records owned by the active Skill's responsibility *(1)*
- **Must** — obtain applicable authorization for materially consequential actions *(1)*
- **Must** — grant every capability only its minimum required access *(2)*
- **Never** — let a lower layer or delegate broaden a deny boundary *(2)*
- **Never** — store or expose secret values in project declarations, logs, or output *(3)*
- **Must** — preserve unrelated Human work and resolve destructive targets exactly *(4)*
