# Skill Contract Structure

A Skill Contract is the portable Agent-side bridge for one Process-backed Interface Skill. One Contract exists for every declared Interface Skill at `.interface/agent/skill/contracts/<interface-owned-skill>.md`.

The Contract is Human-owned. Agents read it and may realize it through a selected Runtime, but never edit it during execution. The owning Process Component Definition and Preferences contain the Process meaning; the Contract points to them and declares the Agent invocation and Runtime boundary. A native Skill implementation is an adapter and cannot override either authority.

## Required structure

Every Process-backed Skill Contract contains these sections in this order:

1. **Title** — `# <name> Skill Contract`.
2. **Purpose** — the Process Component to which the Skill bridges.
3. **Responsibility** — the owning Component and the boundary of the bridge.
4. **Trigger** — Agent-side activation conditions.
5. **Inputs and Outputs** — pointers to the Component-owned inputs and outputs.
6. **Required Understanding and Authority** — the Component sources the Runtime must read and obey.
7. **Runtime Realization** — the invocation and Runtime mechanics the native adapter may provide without changing the Component meaning.

## Content rules

- The Contract contains no Process meaning duplicated from the owning Component, Target facts, resolved project state, credentials, concrete provider commands, or vendor-specific storage layout.
- Inputs name the Component-owned semantic values. Command syntax and aliases remain owned by Agent Command Preferences.
- Source formats, status vocabularies, and storage shapes remain owned by their Components and Schemas; the Contract points to those owners rather than copying them.
- External framework, package, extension, built-in, user, and managed Skills remain provider-owned resources and do not receive Process-backed Contracts.
- Every Process obligation appears once in the owning Component. The bridge references it rather than copying it.
