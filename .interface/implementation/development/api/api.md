# API Definition

API is the executable Development Component that serves generated Groups through one network boundary.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

API provides one running network boundary for modular Groups. It owns the shared API process, runtime configuration, Group registration, and Base URL. Each Group owns the Adapters, Endpoints, Handlers, Parameters, requests, responses, and connections served beneath its URL segment.

Root API has no Adapter, Endpoint, or Handler of its own. It references the independent Definition and Preferences of every known Group for generation, then serves only the Group realizations that were generated and enabled. Root API never copies or redefines a Group's API surface.

### Purpose

Different capability areas need independent API structures while clients need one network address from which to reach them. API supplies that common address and running process while leaving every exposed capability with its owning Group.

### How It Works

During generation, each Group Reference resolves one Group Definition and Preferences pair. The Group's own eligibility rules determine whether its executable realization is generated. Root API uses those references only as generation sources; conceptual MD and YAML files are never copied into the executable API.

At runtime, Bootstrap reads `config.yaml`, creates the API, imports and registers every generated and enabled Group, and starts serving them through the configured network address. Bootstrap does not read Group Definition or Preferences files at runtime.

The Base URL is derived from the configured transport protocol, host, port, and optional URL Key. The optional URL Key appears immediately before the Group segment. The Group name determines that segment, and the Group owns everything that follows it.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **API Group** — one modular capability area that may be generated and registered beneath its configured name in the shared API URL.
- **Group Reference** — one stable Group role and the Definition and Preferences paths used to resolve that Group during generation.
- **Generated Group** — the executable realization created when a referenced Group's eligibility rules are satisfied.
- **Bootstrap** — the single runtime entry point that reads API configuration, creates the API, registers generated Groups, and starts serving them.
- **Base URL** — the address derived from transport protocol, host, port, and the optional URL Key before any Group segment is appended.
- **URL Key** — an optional opaque path segment placed between the host and port portion of the Base URL and the Group name; it is not request authentication.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
API
├── bootstrap
├── groups/
│   └── <group>/
└── config.yaml
```

The names shown are defaults selected by API Preferences. Root API owns only Bootstrap, the Groups container, and Configuration. Each generated `<group>` directory is an executable Group realization whose internal structure is governed by that Group's Definition and Preferences. Conceptual Definition and Preferences files remain in `.interface` and are not copied into this structure.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

API has no direct dependency on another Component. Any connection beyond the API boundary belongs to the Group that owns it and is declared within that Group.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **The shared process, Base URL, Group registration, and runtime configuration** — belong to Root API.
- **Adapters, Endpoints, Handlers, Parameters, requests, responses, failures, and connections beneath a Group segment** — belong to that Group; Root API only registers and serves them.
- **Group eligibility and internal realization** — belong to each Group's Definition and Preferences; a Reference alone never forces generation or registration.
- **An optional URL Key** — changes the Base URL path but does not authenticate a request or authorize a capability.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

API consists of one Bootstrap, one directory containing generated Groups, and one runtime Configuration file.

### Bootstrap

Bootstrap is the API's single composition and execution point. It reads `config.yaml`, creates the API, imports and registers every generated and enabled Group, and starts serving the resulting boundary. It contains no Adapter, Endpoint, Handler, Group capability, or downstream connection.

### Groups

The Groups directory contains executable realizations produced from independently defined API Groups. Root API provides the container and registers each generated Group beneath the URL segment derived from its configured name. The owning Group determines the contents of its directory and everything exposed after its Group segment.

### Entity Group

Entity Group is a known API Group Reference.

→ [Definition of Entity Group](groups/entity/entity.md)<br>
→ [Preferences of Entity Group](groups/entity/entity.yaml)

An additional Group follows the same modular rule: it receives its own Definition and Preferences, is referenced from API Preferences by its stable role, and is generated and registered only when its own eligibility rules are satisfied.

### Configuration

`config.yaml` contains the values used to identify and run the API and follows [API Configuration Structure](../../../foundation/schema/api.yaml). API Preferences supply defaults from which that file may be generated. Bootstrap reads this runtime file but never reads conceptual Group files.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

API Definition Principles are mandatory for the shared API boundary. API Preferences provide configurable defaults for unstated API choices. Each Group Definition and Preferences govern that Group without weakening the shared API Principles. Explicit compatible project meaning takes precedence over defaults.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### API is one shared boundary

**Rule:** API creates one running boundary and serves every generated and enabled Group through that boundary.
**Why:** Groups need one common address and process without becoming separate API applications.
**Boundary:** Another explicitly declared API is another Component; a Group never creates its own server or process.

#### Root API owns no Group capability

**Rule:** Root API defines no Adapter, Endpoint, Handler, Parameter contract, request, response, or downstream connection. It registers and serves only the executable API surface owned by generated Groups.
**Why:** Group capabilities need one authoritative owner and must not be duplicated in the shared boundary.
**Boundary:** Shared process and network concerns remain Root API responsibilities even though all served capabilities belong to Groups.

<br>

### Groups

#### Groups are independently defined and referenced

**Rule:** Every known API Group has its own Definition and Preferences. Root API Preferences contain only a Group Reference to that pair and never copy the Group's Adapters, Endpoints, Handlers, Parameters, defaults, or internal structure.
**Why:** Each Group needs one authoritative contract that can change without duplicating its meaning in Root API.
**Boundary:** Group Definition and Preferences are generation sources and are never copied into the executable API or read by Bootstrap at runtime.

#### Group roles bind references to Group identities

**Rule:** Every Group Reference key matches the fixed `role` declared by that Group's Preferences. The configurable Group `name` determines its public identity and URL segment without changing the stable Reference role.
**Why:** A stable role can resolve the correct Group while its public name remains configurable.
**Boundary:** Renaming a Group never changes its Reference key, Definition path, Preferences path, or responsibility.

#### Group references are complete and generation is conditional

**Rule:** Every Group Reference resolves to exactly one existing Definition and one existing Preferences file. Generation follows the eligibility rules owned by that Group, and Bootstrap registers only Group realizations that were actually generated and enabled.
**Why:** A known Group must have complete authority while an ineligible Group must not appear in the running API.
**Boundary:** A missing, stale, invalid, or ambiguous Reference stops generation with a clear error; a valid Reference alone never forces Group generation.

#### Group names determine valid and unique URL segments

**Rule:** Every generated Group is registered beneath one valid URL segment derived from its configured name. After declared normalization, every generated Group segment is unique.
**Why:** A client can locate a Group from its public identity without a second routing catalogue or an ambiguous address.
**Boundary:** An invalid or colliding segment stops generation with a clear error; API never adds a suffix, number, or silent rename.

<br>

### Bootstrap

#### Bootstrap only composes and runs API

**Rule:** Bootstrap reads runtime Configuration, creates the API, imports and registers generated and enabled Groups, and starts serving them. It defines no Group capability and reads no conceptual Definition or Preferences file at runtime.
**Why:** One narrow entry point keeps shared execution separate from generation sources and the capabilities being served.
**Boundary:** Every Adapter, Endpoint, Handler, Parameter, and connection beyond the API boundary remains inside its owning Group.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**API is one shared boundary**

- **Must** — Serve all generated and enabled Groups through one running API boundary.
- **Never** — Let a Group create a separate server or process.

**Root API owns no Group capability**

- **Must** — Register and serve the API surface owned by generated Groups.
- **Never** — Define an Adapter, Endpoint, Handler, Parameter contract, request, response, or downstream connection in Root API.

### Groups

**Groups are independently defined and referenced**

- **Must** — Give each Group its own Definition and Preferences and reference them from Root API.
- **Never** — Copy Group-specific content into Root API or the executable API structure.

**Group roles bind references to Group identities**

- **Must** — Match every Reference key to the Group's fixed role and use its configurable name for public identity.
- **Never** — Change a stable Reference because the public Group name changes.

**Group references are complete and generation is conditional**

- **Must** — Resolve every Reference and register only Group realizations that are generated and enabled.
- **Never** — Force generation merely because a valid Reference exists.

**Group names determine valid and unique URL segments**

- **Must** — Validate every generated Group segment after normalization.
- **Never** — Silently repair an invalid or colliding segment.

### Bootstrap

**Bootstrap only composes and runs API**

- **Must** — Read runtime Configuration, create API, register generated Groups, and start serving them.
- **Never** — Define a Group capability or read conceptual Definition and Preferences files at runtime.
