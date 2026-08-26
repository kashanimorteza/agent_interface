# Base

                    HUMAN / DEVELOPER
                           │
                           ▼
                  ┌─────────────────┐
                  │ AGENT INTERFACE │
                  │                 │
                  │ Project Intent  │
                  │ Requirements    │
                  │ Rules           │
                  │ Constraints     │
                  │ State           │
                  │ Tasks           │
                  │ Validation      │
                  └────────┬────────┘
                           │
                           ▼
                      AI AGENT
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
            MCP           A2A          Tools
             │             │
             ▼             ▼
        Data / Tools   Other Agents

## Interface

     agent/
     ├── root.yaml            layer 1 — entry point, read protocol, working modes
     ├── definition.yaml      layer 2 — product definition: identity, goals, architecture
     ├── rules.yaml           layer 3 — rules and constraints on agent behavior
     ├── develop.yaml         layer 4 — build layer: items, contracts, plan structure
     ├── task.yaml            layer 5 — task schema, states, plans
     └── state.yaml           layer 6 — current state: active mode, blockers, open questions