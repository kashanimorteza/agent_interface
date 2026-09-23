<!-- Rule `interface-bootstrap` · scope: global (loaded for all work) · synchronized Runtime realization of a Human-owned Rule contract; edit the source and re-run /my-interface-agent-native instead of editing this file. -->

# Agent Interface bootstrap Contract

The Interface structure and Agent Instance realizations are independent of a particular Runtime layout. Agent Module declarations are Human-owned blueprints that only the explicitly invoked Agent Native Sync may read, strictly within the exact prompt created by its own direct Human invocation. Native Rules, Skills, Agent Instances, settings, and capabilities are the synchronized Runtime realization consumed by every other operation.

## Entry points

- `.interface/interface.md` is the canonical Interface document and file map, and the single Interface entry point every Skill and supporting Agent Instance starts from.
- The Foundation section files it links — `.interface/foundation/introduction.md`, `terms.md`, `architecture.md`, `understanding.md`, `authority.md`, and `workflow.md` — are part of Interface Understanding and are read together with it before acting.

Establish Interface Understanding from the Interface document and those linked Foundation section files alone. When the active role needs Target meaning, establish Target Understanding from both Target definitions the Interface locates, under the precedence the Interface declares for them. Unless the Human explicitly invoked Agent Native Sync, never enter, read, search, resolve, or use `.interface/agent/` or any Agent Module source — even when the Interface file lists it. Follow only routes to Target, Implementation, Foundation, Config, and synchronized Runtime resources required by the active role. Current native Rules, role instructions, Skills, settings, and capabilities are the operational Agent contract.

Use the Interface document to locate the current resources required by the active role. Do not assume that a resource exists merely because it existed in an earlier version of the Interface.

Read an authorized located resource before relying on it. Memory, operational records, conversation history, and prior summaries never substitute for current authoritative sources; after a session resume or context compaction, re-establish the Understanding the active role requires before mutating anything. Agent Module changes are deliberately excluded and have no Native effect until the Human explicitly runs Agent Native Sync.

## Separation

- Do not hardcode or copy Target or Implementation facts into a Skill. Read them from their current authorized owners. Runtime-specific Agent Native and Agent Instance behavior is different: Agent Sync intentionally materializes it into self-contained native artifacts so ordinary Skills do not revisit Agent Module sources.
- Every synchronized Interface-owned Skill is a self-contained Runtime realization. It must never resolve its invocation mapping, external capability, Rule, or Role through `.interface/agent/`. Runtime artifacts may reference other synchronized Runtime artifacts.
- Only the explicitly invoked Agent Native Sync may compare Native artifacts with Agent Module authorities and repair drift. Every other Skill reports a missing or unusable Native capability; none of them inspect the Agent Module or invoke Agent Native Sync automatically.
