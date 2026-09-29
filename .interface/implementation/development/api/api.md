# API Definition

API is the executable Development Component that serves modular Groups through one network boundary.

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

API provides one running network boundary for a collection of modular Groups. It owns the shared API process, its configuration, the registration of Groups, the base URL, and the runtime documentation paths. Each Group owns the capabilities served beneath its own URL segment.

API Definition and Preferences describe only the shared API. A Group has its own Definition and Preferences under the Groups directory, and API references that pair without copying the Group's internal structure or capabilities.

### Purpose

Different capability areas need independent structures while clients need one address from which to reach them. API supplies that common address and lifecycle. A Group may change its Items and Actions without turning the root API into another definition of those capabilities.

Without this boundary, every Group would need to create and operate its own API process, repeat the same network configuration, and choose a separate public address. API keeps those concerns together while leaving every capability with its owning Group.

### How It Works

Bootstrap reads `config.yaml`, creates the running API, resolves the referenced Groups, and registers each Group beneath the URL segment formed from that Group's configured name. It then serves all registered Groups through the configured network address.

The base URL is derived from the configured transport protocol, host, port, and optional key. The optional key appears immediately before the Group name. No version segment is inserted into the URL. After the Group segment, the owning Group determines the paths for its Items, Actions, and parameters.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **API Group** — one modular capability area registered beneath its configured name in the shared API URL.
- **Group Reference** — the Definition and Preferences paths through which API discovers one Group without copying it.
- **Bootstrap** — the single entry point that reads API configuration, creates the API, registers its Groups, and starts serving them.
- **Base URL** — the address derived from transport protocol, host, port, and the optional key before any Group segment is appended.
- **URL Key** — an optional opaque path segment placed between the host and port portion of the Base URL and the Group name; it is not request authentication.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
API
├── bootstrap
├── groups/
│   └── <group>/
├── config.yaml
└── README.md
```

The names shown are defaults selected by API Preferences. Every `<group>` directory contains that Group's independent Definition and Preferences; its internal realization is owned by those files.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

API has no direct dependency on another Component. Any connection beyond the API boundary belongs to the Group that owns it and is declared within that Group.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **The internal source or destination of a capability** — belongs to its Group; root API neither knows nor selects it.
- **Items, Actions, routes, parameters, requests, responses, and failures beneath a Group path** — belong to that Group.
- **The shared process, Base URL, Group registration, configuration, and runtime documentation paths** — belong to root API.
- **An optional URL Key** — changes the Base URL path but does not authenticate a request or authorize a capability.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

API consists of one Bootstrap, a directory of independently defined Groups, one runtime configuration file, and one file-based documentation entry.

### Bootstrap

Bootstrap is the API's single composition and execution point. It reads `config.yaml`, creates the API, registers every referenced Group, and starts serving the resulting boundary. It contains no Group Item, Action, route implementation, or downstream capability.

### Groups

The Groups directory contains the modular capability areas served by API. Root API registers each Group beneath its configured name and does not define what follows that path.

### Entity Group

Entity Group is a referenced API Group.

→ [Definition of Entity Group](groups/entity/entity.md)<br>
→ [Preferences of Entity Group](groups/entity/entity.yaml)

An additional Group follows the same modular rule: it receives its own directory, Definition, and Preferences, and API references it instead of copying its content into root files.

### Configuration

`config.yaml` contains the values used to identify and run the API and follows [API Configuration Structure](../../../foundation/schema/api.yaml). API Preferences supply defaults from which that file may be generated.

### Documentation

`README.md` is the file-based documentation for the API Component. The machine-readable schema and live documentation served by the running API use the separately configured `openapi_url`, `docs_url`, and `redoc_url` paths. None of those runtime paths names or replaces `README.md`.

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

**Rule:** API creates one running boundary and serves every referenced Group through that boundary.
**Why:** Groups need one common address and process without becoming separate API applications.
**Boundary:** Another explicitly declared API is another Component; a Group never creates its own server or process.

<br>

### Groups

#### Groups are independently defined and referenced

**Rule:** Every API Group has its own Definition and Preferences inside its own directory. Root API files contain only a reference to that pair and never copy the Group's Items, Actions, routes, parameters, or defaults.
**Why:** Each Group needs one authoritative contract that can change without duplicating its meaning in root API.
**Boundary:** Root API registers and serves the Group but does not define what the Group provides.

#### Group references are complete and unique

**Rule:** Every Group identity is unique and resolves to exactly one existing Definition and one existing Preferences file under the configured Groups directory. A missing, invalid, stale, or colliding reference stops creation with a clear error.
**Why:** API cannot register a Group whose identity or authority is incomplete or ambiguous.
**Boundary:** API never repairs a reference through an invented path, suffix, number, or silent rename.

#### Group names determine their URL segments

**Rule:** API registers each Group beneath one unique URL segment derived from that Group's configured name. The segment follows the optional URL Key directly, and no version segment is inserted before it.
**Why:** A client can locate a Group from its declared identity without a second routing catalogue.
**Boundary:** The owning Group defines every Item, Action, route, and parameter after its Group segment.

<br>

### Bootstrap

#### Bootstrap only composes and runs API

**Rule:** Bootstrap reads API configuration, creates the API, registers referenced Groups, and starts serving them. It defines no Group capability.
**Why:** One narrow entry point keeps shared execution separate from the capabilities being served.
**Boundary:** Every Item, Action, route, parameter, and connection beyond the API boundary remains inside its owning Group.

<br>

### Documentation

#### File and runtime documentation remain distinct

**Rule:** `README.md` documents the API Component, while `openapi_url`, `docs_url`, and `redoc_url` identify documentation served by the running API.
**Why:** Component setup and usage documentation has a different purpose from the live description of the running routes.
**Boundary:** Runtime documentation presents registered Groups without becoming the Definition or Preferences of any Group.

#### Root documentation references Group documentation

**Rule:** Root documentation introduces every registered Group and refers to its documentation without copying its detailed capabilities.
**Why:** Consumers need one API overview while every Group retains one owner for its details.
**Boundary:** Root documentation never publishes an unregistered Group or private Group content.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**API is one shared boundary**

- **Must** — Serve all referenced Groups through one running API boundary.
- **Never** — Let a Group create a separate server or process.

### Groups

**Groups are independently defined and referenced**

- **Must** — Give each Group its own Definition and Preferences and reference them from root API.
- **Never** — Copy Group-specific content into root API files.

**Group references are complete and unique**

- **Must** — Resolve every unique Group identity to one valid Definition and Preferences pair.
- **Never** — Silently repair a missing, invalid, stale, or colliding reference.

**Group names determine their URL segments**

- **Must** — Register each Group beneath its unique configured name after the optional URL Key.
- **Never** — Insert a version segment or let root API define paths owned by the Group.

### Bootstrap

**Bootstrap only composes and runs API**

- **Must** — Read configuration, create API, register Groups, and start serving them.
- **Never** — Define a Group capability in Bootstrap.

### Documentation

**File and runtime documentation remain distinct**

- **Must** — Keep `README.md` distinct from OpenAPI, interactive docs, and ReDoc runtime paths.
- **Never** — Treat a runtime documentation path as the Component README.

**Root documentation references Group documentation**

- **Must** — Introduce registered Groups and refer to their detailed documentation.
- **Never** — Duplicate Group details or expose an unregistered Group.
