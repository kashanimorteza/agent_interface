> Rule `interface-bootstrap` · Scope: **global** — applies to every session and all work in this project, with no path condition. Synchronized Native realization; regenerated only by `/my-interface-agent-native`.

# Agent Interface bootstrap Contract

The Interface structure and Agent Instance realizations are independent of a particular Runtime layout. Native Rules, Skills, Agent Instances, settings, and capabilities are the synchronized Runtime realization consumed by every other operation.

## Entry points

- `.interface/interface.md` is the canonical Interface document and file map, and the single Interface entry point every Skill and supporting Agent Instance starts from.
- The Foundation section files it links — `.interface/foundation/introduction.md`, `terms.md`, `architecture.md`, `understanding.md`, `authority.md`, and `workflow.md` — are part of Interface Understanding and are read together with it before acting.

Establish Interface Understanding from the Interface document and those linked Foundation section files alone. When the active role needs Target meaning, establish Target Understanding from both Target definitions the Interface locates, under the precedence the Interface declares for them. Follow only routes to Target, Implementation, Foundation, Config, and synchronized Runtime resources required by the active role. Current native Rules, role instructions, Skills, settings, and capabilities are the operational Agent contract.

Use the Interface document to locate the current resources required by the active role. Do not assume that a resource exists merely because it existed in an earlier version of the Interface.

Read an authorized located resource before relying on it. Memory, operational records, conversation history, and prior summaries never substitute for current authoritative sources; after a session resume or context compaction, re-establish the Understanding the active role requires before mutating anything.

## Separation

- Do not hardcode or copy Target or Implementation facts into a Skill. Read them from their current authorized owners.
