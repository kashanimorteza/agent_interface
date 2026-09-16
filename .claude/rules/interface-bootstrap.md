# Agent Interface bootstrap

The Interface structure and Agent Instance realizations are independent of a particular Runtime layout. Agent Module declarations are Human-owned blueprints that only explicit `/my-interface-agent-sync` and explicit `/my-interface-skill-installer` may read, each strictly within the exact prompt created by its own direct Human invocation. Native Rules, Skills, Agent Instances, settings, and capabilities are the synchronized Runtime realization consumed by every other operation.

## Entry points

- `.interface/foundation/interface.md` is the canonical Interface document and file map, and the single Interface entry point every Skill and supporting Agent Instance starts from.

Establish Interface Understanding from the Interface document alone. Unless the Human explicitly invoked `/my-interface-agent-sync` or `/my-interface-skill-installer`, never enter, read, search, resolve, or use `.interface/agent/` or any Agent Module source—even when the Interface file lists it. Follow only routes to Target, Implementation, Foundation, Config, and synchronized Runtime resources required by the active role. Current native Rules, role instructions, Skills, settings, and capabilities are the operational Agent contract.

Use the Interface document to locate the current resources required by the active role. Do not assume that a resource exists merely because it existed in an earlier version of the Interface.

Read an authorized located resource before relying on it. Agent Module changes are deliberately excluded and have no Runtime effect until the Human explicitly runs Agent Sync; Skill Installer's Agent Module reads resolve only which Prepared or Installed capabilities to transfer or provision and never repair Runtime drift or serve as a second synchronization path.

## Separation

- Do not hardcode or copy Target or Implementation facts into a Skill. Read them from their current authorized owners. Runtime-specific Agent Native and Agent Instance behavior is different: Agent Sync intentionally materializes it into self-contained native artifacts so ordinary Skills do not revisit Agent Module sources.
- Every native `my-interface-*` Skill except Agent Sync and Skill Installer is a synchronized, self-contained Runtime realization. It must never resolve its portable Contract, invocation mapping, external capability, Rule, or Role through `.interface/agent/`. Runtime artifacts may reference other synchronized Runtime artifacts.
- Only explicit `/my-interface-agent-sync` may compare Runtime artifacts with Agent Module authorities and repair drift. Explicit `/my-interface-skill-installer` may read the Module only to resolve which Prepared and Installed capabilities to materialize; it never repairs drift or reconciles Rules, Skills, or other Runtime artifacts against Module authorities. Every other Skill reports a missing or unusable Runtime capability; none of them inspect the Agent Module or invoke Agent Sync or Skill Installer automatically.
