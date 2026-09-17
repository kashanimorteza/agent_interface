# Architecture

This file carries the Architecture section of the Interface, moved here verbatim from `interface.md` on 2026-09-18. It is part of Interface Understanding: every Skill reads `interface.md` and this file before acting. The Interface file remains the canonical entry point; this file is one of its sections.

<br>

The current conceptual architecture is:

```text
Architecture
│
├── Modules
│   ├── Target
│   ├── Implementation
│   └── Agent
├── Foundation Files
├── Understanding
├── Operations
├── Modes
├── Authority and Ownership
└── Workflow
```

Each Module owns one Structure that shows its concepts together with their repository files. Understanding establishes the context used by a Skill, Operations define the actions Skills perform, Foundation Files remain shared resources, Modes record operational position, Authority and Ownership control writes, and Workflow defines execution order.
