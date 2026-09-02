# Base

                    HUMAN / DEVELOPER
                           │
                           ▼
                  ┌─────────────────┐
                  │ AGENT INTERFACE │
                  │                 │
                  │ Project Intent  │
                  │ Requirements    │
                  │ Item Policies   │
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

     .interface/
     ├── root.yaml                         entry point, map, working modes
     ├── project.md                        human project intent
     ├── schema/
     │   ├── database.schema.yaml          Database shape, Policy, Preferences
     │   ├── backend.schema.yaml           Backend shape, Policy, Preferences
     │   ├── frontend.schema.yaml          Frontend shape, Policy, Preferences
     │   ├── definition.schema.yaml        product and contract graph shape
     │   ├── task.schema.yaml              task frame, states, item plans
     │   ├── state.schema.yaml             state authority and transitions
     │   └── file.schema.yaml              common generated-file envelope
     └── config/
         ├── definition.yaml               generated product Understanding
         ├── database.yaml                 generated Database configuration
         ├── backend.yaml                  generated Backend configuration
         ├── frontend.yaml                 generated Frontend configuration
         ├── task.yaml                     generated plans and task state
         └── state.yaml                    generated runtime state

     Contract direction: Database → Backend → Frontend
