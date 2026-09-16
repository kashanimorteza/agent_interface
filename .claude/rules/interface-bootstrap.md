# Agent Interface bootstrap

The Interface structure and Agent Instance realizations are independent of a particular Runtime layout. Agent Module declarations are Human-owned blueprints that only explicit `/my-interface-agent-sync` may read. Native Rules, Skills, Agent Instances, settings, and capabilities are the synchronized Runtime realization consumed by every other operation.

## Entry points

- `.interface/foundation/interface.md` is the canonical Interface document and file map, and the single Interface entry point every Skill and supporting Agent Instance starts from.

Establish Interface Understanding from the Interface document alone. Unless the Human explicitly invoked `/my-interface-agent-sync`, never enter, read, search, resolve, or use `.interface/agent/` or any Agent Module source—even when the Interface file lists it. Follow only routes to Target, Implementation, Foundation, Config, and synchronized Runtime resources required by the active role. Current native Rules, role instructions, Skills, settings, and capabilities are the operational Agent contract.

Use the Interface document to locate the current resources required by the active role. Do not assume that a resource exists merely because it existed in an earlier version of the Interface.

Read an authorized located resource before relying on it. Agent Module changes are deliberately excluded and have no Runtime effect until the Human explicitly runs Agent Sync.

## Separation

- Do not hardcode or copy Target or Implementation facts into a Skill. Read them from their current authorized owners. Runtime-specific Agent Native and Agent Instance behavior is different: Agent Sync intentionally materializes it into self-contained native artifacts so ordinary Skills do not revisit Agent Module sources.
- Every native `my-interface-*` Skill except Agent Sync is a synchronized, self-contained Runtime realization. It must never resolve its portable Contract, invocation mapping, external capability, Rule, or Role through `.interface/agent/`. Runtime artifacts may reference other synchronized Runtime artifacts.
- Only explicit `/my-interface-agent-sync` may compare Runtime artifacts with Agent Module authorities and repair drift. Other Skills report a missing or unusable Runtime capability; they do not inspect the Agent Module or invoke Agent Sync automatically.
