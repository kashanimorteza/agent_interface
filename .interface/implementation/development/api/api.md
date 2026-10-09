# API Definition

API is the executable Development Component that serves every Group through one network boundary.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

API is the one running network boundary of the application: it serves every Group beneath its own URL segment and has no Endpoint of its own.

### Purpose

Clients need one address for every capability area, while each area keeps its own API surface.

### How It Works

Bootstrap reads the runtime Configuration, creates the API, registers every Group beneath its segment, and starts serving.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Group** — one modular capability area with its own Definition and Preferences, served beneath its own URL segment.
- **Adapter** — the unit of a Group bound to one member of its source, holding the Endpoints of that member's operations.
- **Group Reference** — one stable Group role and the paths of that Group's Definition and Preferences.
- **Bootstrap** — the single runtime entry point of API.
- **Base URL** — the address formed from transport protocol, host, port, and the optional URL Key, before any Group segment.
- **Endpoint** — one HTTP Method, Path, Parameters, and Handler that a Group needs for one of its operations.
- **Parameter** — one operation input placed in Path, Query, or Body.
- **URL Key** — an optional opaque path segment placed before every Group segment; it is not request authentication.
- **Interface contract** — the versioned public surface of API, stated in its Groups section, with its version in API Preferences.
- **Group contract** — the versioned contract, stated in API's Groups section, through which every Group states what it serves.
- **API Configuration Structure** — the versioned structure of API's runtime Configuration.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
API
├── Bootstrap
├── Groups
├── Endpoints
├── Configuration
└── Documentation
```

Every entity below is declared in `architecture` in API Preferences, which also own the language, realization, and documentation choices; these selections realize the responsibilities below without changing them.

<!-------------------------- Bootstrap -->
### Bootstrap

The single composition and execution point of API.

<!-------------------------- Groups -->
### Groups

```text
Groups
└── Entity Group
```

The container of every Group's executable realization. Every Group is served at `<base_url>/<group segment>`, where the Base URL is `<transport_protocol>://<host>:<port>[/<key>]` from the runtime Configuration. API's Interface contract is these needs, with `contract_version` in API Preferences:

1. **Complete** — every Group listed in API Preferences is registered beneath the URL segment of its configured name after the Base URL, changing when the list changes; each Group's name comes from that Group's own Preferences.
2. **Unchanged** — every Group serves its own Endpoints exactly; API adds no Endpoint, wrapper, or behavior to them.
3. **Nothing else** — API has no Endpoint of its own.
4. **One Group contract** — every Group states what it serves through the Group contract below, and API realizes every Group from it the same way.
5. **Versioned** — changing this structure requires raising `contract_version` and a consumer review; a change in the Group list flows through without one.

#### Group contract

The shared contract through which every Group states what it serves, with its version in API Preferences:

- **Group** — the fixed role the Group's Preferences declare, and the configurable name that sets its URL segment.
- **Source** — the one published Interface the Group serves and what it takes from it, found from that Interface's own Preferences.
- **Adapters** — one Adapter for every member of the collection the source publishes, named from its member by the Adapter pattern in the Group's Preferences and bound permanently to it; a caller never supplies it, and a member added or removed adds or removes its Adapter.
- **Endpoints** — one Endpoint for every operation of the Adapter's member; an operation added or removed adds or removes its Endpoint. The Group never states an Endpoint's identity; API derives it.
- **Parameters** — exactly the operation's parameters: the same names, requirements, structures, and defaults, with types the source publishes.
- **Handler** — calls the same operation through the source and returns its result and errors unchanged.

No Handler adds a decision, semantic validation, initialization, wrapper, other call, retry, or alternate path. A Group states no Method, Path, placement, protocol, or technology; API owns every one. A change in what a source publishes flows through without a version change.

#### Entity Group

Entity Service as HTTP.

→ [Definition of Entity Group](groups/entity/entity.md)<br>
→ [Preferences of Entity Group](groups/entity/entity.yaml)

<!-------------------------- Endpoints -->
### Endpoints

The common HTTP rules every Group's Endpoints follow. The operations of each Group's source decide which Endpoints exist; API realizes them by these rules. Every Endpoint is served at `<base_url>/<group segment>/<adapter segment><endpoint path>`.

<!-------------------------- Configuration -->
### Configuration

The runtime values that identify and run the API, in the shape the [API Configuration Structure](../../../foundation/schema/api-configuration.yaml) defines.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Configuration
├── Groups
├── Setup
├── Use
├── Verify
└── Troubleshooting
```

The root documentation, in the file, location, and format API Preferences name. Its sections, in this order:

1. **Overview** — What API is, in one paragraph, with one request example.
2. **Configuration** — Every runtime Configuration value and how the Base URL is formed from it.
3. **Groups** — Every Group beneath its URL segment, with a link to its own documentation; never a copy of its Endpoints.
4. **Setup** — How to install and start API.
5. **Use** — How a client reaches a Group.
6. **Verify** — How to see that every listed Group is served beneath its segment and nothing else is.
7. **Troubleshooting** — Real problems a client can meet and how to fix them.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── api/
│   ├── bootstrap
│   └── groups/
│       └── entity/
├── config
└── README
```

The root of this tree is the Component directory; it and the package directory take their names from `settings` in API Preferences. Each Group has its own directory under `groups/`, named in `settings` of that Group's Preferences.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Everything inside a Group and beneath its URL segment** — is not API's, because that Group's own Definition and Preferences govern it.
- **Request authentication and capability authorization** — are not API's, because the URL Key only changes the path.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for API. API Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning retains its authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### API is one shared boundary with no capability of its own

**Rule:** API creates one running boundary and serves every Group through it. It defines no Endpoint, Handler, Parameter, request, response, or connection of its own.
**Why:** Groups need one common address and process, and every capability needs one owner.
**Boundary:** A Group never creates its own server or process; shared process and network concerns stay with API.

#### API always serves its interactive documentation

**Rule:** When the selected API package can publish interactive documentation of the served Endpoints, API always enables it, with one section per Group and, within it, one section per Adapter holding all of that Adapter's Endpoints.
**Why:** Every client can discover and try every Endpoint without reading source.
**Boundary:** The documentation shows only what the Groups serve.

#### URL Key follows its setting

**Rule:** When the key setting is on, a random URL-safe key of the configured length is generated once, written into the runtime Configuration, and kept on every later generation. When it is off, the Base URL has no key segment.
**Why:** An Endpoint need not sit at a bare, guessable address, and a kept key never moves the address under its clients.
**Boundary:** The URL Key only changes the path; it never authenticates a request or authorizes a capability.

<br>

### Bootstrap

#### Bootstrap only composes and runs API

**Rule:** Bootstrap reads the runtime Configuration, creates the API, registers every Group, and starts serving. It defines no Group capability and reads no Definition or Preferences file at runtime.
**Why:** One narrow entry point keeps execution separate from generation sources and from the capabilities it serves.
**Boundary:** Everything served beneath a Group segment stays inside its Group.

<br>

### Groups

#### API Interface conforms to the Interface contract

**Rule:** Every realization of API's public surface conforms to the versioned Interface contract, which fixes the Base URL, every Group registration, and what API never serves.
**Why:** Every client depends on one exact address structure instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires raising `contract_version`.

#### Public identities are valid and unique

**Rule:** Every Group segment, derived from the Group's configured name, every Adapter segment, and every Method-and-Path combination is valid and unique across API.
**Why:** A client finds every Group and operation without an ambiguous address.
**Boundary:** An invalid or colliding segment stops generation with a clear error; nothing is renamed silently.

#### Every Group is referenced by its role and governed by its own files

**Rule:** Every Group has its own Definition and Preferences. API Preferences hold only a Group Reference, keyed by the fixed role that Group's Preferences declare, and the Reference resolves to exactly one existing Definition and one existing Preferences file. The Group's configurable name sets its public identity without changing its role.
**Why:** Each Group has one authoritative contract that changes without being copied into API, and renaming never breaks its Reference.
**Boundary:** A missing, stale, or ambiguous Reference stops generation with a clear error. Group files are generation sources only and are never copied into the executable API.

<br>

### Endpoints

#### Endpoint identity derives from the operation

**Rule:** Every Endpoint takes its Method from the operation's leading verb by the configured verb table, `POST` otherwise, and the Path `/<operation>`, or `/<operation>/{id}` when the operation takes an `id`; nothing is listed or mapped by hand.
**Why:** Endpoints follow the operations a Group needs every time API is generated, so a change in them never leaves a stale list.
**Boundary:** Only the configured verb table sets a Method; an unlisted verb always uses `POST`, and no Method is chosen any other way.

#### Endpoint Parameters are placed by one rule

**Rule:** `id` uses Path; every other simple Parameter uses Query for `GET` and `DELETE`, and Body for `POST`, `PUT`, and `PATCH`. A `GET` or `DELETE` operation with a Parameter that Query cannot carry uses `POST` instead.
**Why:** Inputs sit predictably in every request of every Group.
**Boundary:** Placement never changes a Parameter's name, requirement, structure, meaning, or default.

#### Non-simple Parameters travel by one rule

**Rule:** A Parameter whose type is a published class travels as a JSON object of its fields and is built from that class; a reference to a field of the bound class travels as the field's name and resolves to it, an unknown name failing with the source's invalid-input error; every other value type the source publishes travels in the form the value table in API Preferences gives it.
**Why:** Every client sends non-simple values the same way in every Group.
**Boundary:** This conversion is part of serving and happens before the Handler runs; the Handler still only calls its Action, and the value's meaning never changes.

#### Action errors map to HTTP by one table

**Rule:** Every error an Endpoint returns is sent as RFC 9457 Problem Details (`application/problem+json`), with `type` set to the error's class name, and with the status the error table in API Preferences sets; an error the table does not name uses `500`.
**Why:** Every client reads every Group's errors the same way, and the error's class reaches it unchanged.
**Boundary:** This mapping is part of serving every Endpoint; it adds no retry, recovery, or other error-handling Behavior.

<br>

### Configuration

#### Every changeable runtime value lives in the runtime Configuration

**Rule:** Every value the API Configuration Structure defines is always written into the runtime Configuration after generation, even when it equals its default, and Bootstrap reads it only from there.
**Why:** An operator finds and changes the API's address and behavior in one file, never in source.
**Boundary:** Source holds no runtime value of its own.

<br>

### Review

#### API conformance covers every API contract

**Rule:** API is conformant only when its Interface contract and the real API match one another, and every observation below holds.
**Why:** A gap here silently hides or misplaces a Group for every client.
**Boundary:** Review reads Group files only to compare; it changes nothing outside API's own files.

#### Review observes API through a fixed set of checks

**Rule:** Review establishes API conformance through these observations, every one of them on every review:
- Every listed Group is registered exactly beneath the URL segment of its name, and nothing else is registered.
- Every Group segment, Adapter segment, and Method-and-Path combination is unique.
- Every Group conforms to the Group contract.
- API serves no Endpoint of its own.
- Every Endpoint's Method follows the verb table, or `POST` when its verb is unlisted, and its Path is `/<operation>`, or `/<operation>/{id}` when it takes an `id`.
- Every Parameter sits in Path, Query, or Body as the placement rule requires.
- Every non-simple Parameter travels in the form the non-simple Parameter rule states, and is converted before its Handler runs.
- Every returned error is RFC 9457 Problem Details with its class name as `type` and the status the error table sets.
- When the key setting is on, the Base URL carries a non-empty URL Key.
- When the package offers interactive documentation, it is served, lists every Endpoint, and has one section per Group and per Adapter.
- The runtime Configuration holds every value the API Configuration Structure defines and follows its rules.
- Bootstrap reads no Definition or Preferences file at runtime.
**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**API is one shared boundary with no capability of its own**

- **Must** — Serve every Group through one running API boundary.
- **Never** — Define an Endpoint, Handler, Parameter, request, response, or connection in API, or let a Group create its own server.

**API always serves its interactive documentation**

- **Must** — Enable the package's interactive documentation whenever the package offers it, sectioned by Group and Adapter.
- **Never** — Show anything in it that the Groups do not serve.

**URL Key follows its setting**

- **Must** — Generate a random URL Key once when the key setting is on, and keep it afterwards.
- **Never** — Regenerate an existing key.

<br>

### Bootstrap

**Bootstrap only composes and runs API**

- **Must** — Read the runtime Configuration, create API, register every Group, and start serving.
- **Never** — Define a Group capability or read Definition or Preferences files at runtime.

<br>

### Groups

**API Interface conforms to the Interface contract**

- **Must** — Conform every realization to the Interface contract.
- **Never** — Serve anything the contract does not list or change its structure without raising `contract_version`.

**Public identities are valid and unique**

- **Must** — Keep every Group segment, Adapter segment, and Method-and-Path combination valid and unique.
- **Never** — Silently repair an invalid or colliding value.

**Every Group is referenced by its role and governed by its own files**

- **Must** — Reference every Group by its fixed role and resolve exactly one Definition and Preferences file.
- **Never** — Copy Group content into API or change a Reference because a Group's name changes.

<br>

### Endpoints

**Endpoint identity derives from the operation**

- **Must** — Give every Endpoint its Method from the verb table, `POST` otherwise, and the Path `/<operation>`, or `/<operation>/{id}` when it takes an `id`.
- **Never** — List or map an Endpoint by hand, or guess a Method.

**Endpoint Parameters are placed by one rule**

- **Must** — Place `id` in Path and every other Parameter in Query or Body by the Method.
- **Never** — Change a Parameter's name, requirement, structure, meaning, or default.

**Non-simple Parameters travel by one rule**

- **Must** — Send every non-simple Parameter in its stated form and convert it before the Handler runs.
- **Never** — Convert a value inside a Handler or change its meaning.

**Action errors map to HTTP by one table**

- **Must** — Return every error as RFC 9457 Problem Details with its class name and the status the table sets.
- **Never** — Add retry, recovery, or other error-handling Behavior through this mapping.

<br>

### Configuration

**Every changeable runtime value lives in the runtime Configuration**

- **Must** — Write every value the API Configuration Structure defines into the runtime Configuration after generation, and read it only from there.
- **Never** — Hold a runtime value in source.

<br>

### Review

**API conformance covers every API contract**

- **Must** — show that the Interface contract and the real API match before API is conformant.
- **Never** — change anything outside API's own files during review.

**Review observes API through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
