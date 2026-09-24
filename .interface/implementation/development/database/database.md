# Database Definition

Database is the Development Component that persists Model data and provides standard data operations to Logic.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Layering](#layering)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

Database configuration declares supported Engines and their parameters, named Instances, component Settings, and public Operations. Public Interface receives an operation request from Logic and passes it to Mapping. Mapping resolves the Instance and Engine, may standardize the returned data, and gives the result back to Public Interface. Each declared Engine has one implementation file under `engine/`.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Engine** — a supported database technology and its implementation.
- **Instance** — a named database connection and storage identity using one Engine.
- **Settings** — component-wide choices such as the default Instance, purpose-to-Instance assignments, and secret references.
- **Model Operation** — a public operation that works with one Model, such as add, update, list, delete, enable, disable, or get by ID.
- **Custom Operation** — a public operation with its own request and result shape, such as a report.
- **Public Interface** — the boundary through which Logic requests configured Operations.
- **Mapping** — the internal layer that routes a request to its Instance and Engine and standardizes its result when needed.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Database
├── database.yaml             ← Engines, Instances, Settings, and Operations
├── Public Interface          ← receives operation requests from Logic
├── Mapping                   ← routes requests and standardizes results
└── engine/                   ← one implementation file per declared Engine
    ├── sqlite
    ├── postgresql
    ├── mysql
    └── mssql
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — persists the Models and their declared data shapes.
- **Provides to Logic** — exposes configured Operations through its Public Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

1. `database.yaml` declares Engines, Instances, Settings, and Operations.
2. Public Interface receives an operation request from Logic and passes it to Mapping.
3. Mapping resolves the requested Instance and Engine, then standardizes the result when needed.
4. The selected Engine implementation performs the requested operation.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

- **Definition** defines the Database Component's responsibilities and layers.
- **Preferences** define its implementation layout and conventions.
- **Configuration** contains the current Engines, Instances, Settings, and Operations.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

1. **Configuration declares resources.** Every Instance names a declared Engine. Settings select the default Instance, named assignments, secrets, and other component-wide parameters.
2. **Public operations are explicit.** Public Interface exposes only the Operations declared in `database.yaml`. Model Operations use the Model-operation standard; Custom Operations define their own standard.
3. **Mapping owns routing and result handling.** It selects the requested Instance and Engine, forwards the request, and standardizes the result when needed before returning it through Public Interface.
4. **Engines are isolated.** Each declared Engine has one implementation file under `engine/` and implements the published Operations for that Engine.
5. **Database connects Model to Logic.** It persists Model data and serves Logic through its Public Interface.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

- `database.yaml` is the runtime configuration for Engines, Instances, Settings, and Operations.
- Public Interface receives requests from Logic.
- Mapping selects the target Instance and Engine and may standardize results.
- `engine/` holds one implementation file for every supported Engine.
- Operations are either Model Operations or Custom Operations.
- Database consumes Model and provides its operations to Logic.
