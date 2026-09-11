# Agent Context Principles

Agent Context is the Component that establishes the current information available to an Agent Role. It governs persistent instructions, loaded project knowledge, memory, imports, and context preservation across runtime lifecycle events.

It owns context composition and freshness. It does not own the meaning of Target, Developer, or Agent sources and never replaces those authorities with remembered summaries.

## Terms

- **Context** — the information currently available to an Agent Role for reasoning and action.
- **Persistent Instruction** — project or organizational guidance loaded across sessions.
- **Memory** — retained supporting knowledge that may help future work but is not authoritative intent.

## Relationships

- **Consumes Target, Developer, and Agent Modules** — loads current authoritative sources as required by the active role.
- **Consumes Agent Rule** — loads applicable persistent and scoped instructions.
- **Consumed by Agent Role, Skill, and Session** — supplies the current information they use.

Technical loading sources, memory behavior, imports, and limits belong to Agent Context Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every action begins from current Understanding

**Rule:** An Agent Role establishes current Interface Understanding before acting and current Target Understanding whenever its responsibility requires it. Memory, operational records, conversation history, and prior summaries never substitute for current authoritative sources.

**Why:** Long-lived or resumed sessions otherwise act on stale assumptions.

**Boundary:** A role reads only the context necessary for its bounded responsibility.

<br>

## 2. Context distinguishes authority from assistance

**Rule:** Every context source retains its authority class and origin. Persistent instructions and Memory may guide execution but never override Principles, explicit project decisions, or current owned records.

**Why:** Loading information together must not flatten its precedence.

**Boundary:** Context ordering may affect presentation but not declared authority.

<br>

## 3. Context lifecycle preserves required instructions

**Rule:** Session start, resume, compaction, delegation, and isolation preserve or reload every instruction required by the receiving role. Missing required context is reported before dependent work proceeds.

**Why:** A lifecycle transition must not silently weaken the execution contract.

**Boundary:** Supporting material may be loaded lazily when no current action depends on it.

<br>

## At a Glance

- **Must** — establish current Interface and role-required Target Understanding before acting *(1)*
- **Never** — substitute memory or prior summaries for current authorities *(1)*
- **Must** — retain each context source's origin and authority *(2)*
- **Never** — let instructions or Memory override owned sources *(2)*
- **Must** — preserve or reload required context across lifecycle transitions *(3)*
