# Understanding

This file carries the Understanding section of the Interface, moved here verbatim from `interface.md` on 2026-09-17. It is part of Interface Understanding: every Skill reads `interface.md` and this file before acting. The Interface file remains the canonical entry point; this file is one of its sections.

<br>

Understanding is the current context an Agent Native or Agent Instance establishes before performing a Skill's role. Interface Understanding is required by every Skill and starts exclusively from this canonical Interface file. For every operation except Agent Sync, the Interface routes the Skill only to applicable Target, Implementation, Foundation, Config, and synchronized Runtime resources; seeing the Agent Structure in the Agent Module Guide never authorizes entry into the Agent Module. Target Understanding is separate and, when the role needs Target meaning, is established from both Human Definition and Technical Definition under Target's declared precedence. Configure uses only the phase identities and Platform selections required for its role; Reset establishes the minimum Target Understanding needed for a phase scope, omits it for Config scope, and uses only phase identity and ownership for Complete scope. Agent Sync alone may follow the Agent Structure into Agent Module sources and does so only after explicit Human invocation.

- **Interface Understanding:** Read `.interface/interface.md` as the Foundation entry point together with the Foundation section files it links — `understanding.md`, `operations.md`, `modes.md`, `authority.md`, and `workflow.md` — then follow only the non-Agent-Module routes they provide for the active role. Agent Sync is the sole explicit exception.
- **Target Understanding:** When required, read both Target definitions located by the Interface. Human Definition provides the Human's stated intent and context; Technical Definition is the primary Target authority and takes precedence wherever they conflict.

```text
Understanding Structure
├── Interface Understanding
│   ├── Interface Foundation Source → .interface/interface.md
│   └── Foundation Section Files   → .interface/foundation/{understanding,operations,modes,authority,workflow}.md
└── Target Understanding
    ├── Human Definition    → .interface/target/non-technical.md
    └── Technical Definition → .interface/target/technical.md
```

Understanding uses these authoritative sources:

- [Interface Foundation Source](../interface.md)
- Foundation Section Files: [Understanding](understanding.md), [Operations](operations.md), [Modes](modes.md), [Authority and Ownership](authority.md), [Workflow](workflow.md)
- [Non-Technical Definition](../target/non-technical.md)
- [Technical Definition](../target/technical.md)

An empty Human Definition contributes no information. Understanding is reconstructed from both current sources under their declared precedence when required and is never copied into Config as a second project definition.
