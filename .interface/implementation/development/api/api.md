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
- **Group Reference** — one stable Group role and the paths of that Group's Definition and Preferences.
- **Bootstrap** — the single runtime entry point of API.
- **Base URL** — the address formed from transport protocol, host, port, and the optional URL Key, before any Group segment.
- **Endpoint** — one HTTP Method, Path, Parameters, and Handler that a Group needs for one of its operations.
- **Parameter** — one operation input placed in Path, Query, or Body.
- **URL Key** — an optional opaque path segment placed before every Group segment; it is not request authentication.
- **API Interface Schema** — the versioned structure that fixes the exact shape of API's public surface.
- **API Group Interface Schema** — the versioned contract through which every Group states what it serves.
- **API Configuration Structure** — the versioned structure of API's runtime Configuration.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
API
├── Bootstrap       ← the single runtime entry point
├── Groups          ← one directory per Group
└── Configuration   ← the runtime values, in the shape the API Configuration Structure defines
```

API Preferences own its identity, architecture, Group list, Endpoint rules, network, runtime, language and realization, and documentation. The shape of its public surface belongs to the API Interface Schema.

### Bootstrap

The single composition and execution point of API.

### Groups

The container of every Group's executable realization. It meets these needs:

1. **Complete** — every Group listed in API Preferences is registered beneath the URL segment of its configured name after the Base URL, changing when the list changes.
2. **Unchanged** — every Group serves its own Endpoints exactly; API adds no Endpoint, wrapper, or behaviour to them.
3. **Nothing else** — API has no Endpoint of its own.
4. **One Group contract** — every Group states what it serves through the API Group Interface Schema, and API realizes every Group from it the same way.

The exact shape of these needs is fixed by the API Interface Schema, which is built from them. These needs are the reference: when the two differ, the Schema is corrected to match them.

#### Entity Group

Entity Service as HTTP.

→ [Definition of Entity Group](groups/entity/entity.md)<br>
→ [Preferences of Entity Group](groups/entity/entity.yaml)

### Endpoints

The common HTTP rules every Group's Endpoints follow. A Group states which Endpoints it needs; API realizes them by these rules.

### Configuration

The runtime values that identify and run the API, in the shape the [API Configuration Structure](../../../foundation/schema/api-configuration.yaml) defines.

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

### Interface

#### API Interface conforms to the API Interface Schema

**Rule:** Every realization of API's public surface conforms to the versioned API Interface Schema, which fixes the Base URL, every Group registration, and what API never serves.
**Why:** Every client depends on one exact address structure instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires a Schema version change.

#### Public identities are valid and unique

**Rule:** Every Group segment, derived from the Group's configured name, every Adapter segment, and every Method-and-Path combination is valid and unique across API.
**Why:** A client finds every Group and operation without an ambiguous address.
**Boundary:** An invalid or colliding segment stops generation with a clear error; nothing is renamed silently.

### Groups

#### Every Group is referenced by its role and governed by its own files

**Rule:** Every Group has its own Definition and Preferences. API Preferences hold only a Group Reference, keyed by the fixed role that Group's Preferences declare, and the Reference resolves to exactly one existing Definition and one existing Preferences file. The Group's configurable name sets its public identity without changing its role.
**Why:** Each Group has one authoritative contract that changes without being copied into API, and renaming never breaks its Reference.
**Boundary:** A missing, stale, or ambiguous Reference stops generation with a clear error. Group files are generation sources only and are never copied into the executable API.

### Bootstrap

#### Bootstrap only composes and runs API

**Rule:** Bootstrap reads the runtime Configuration, creates the API, registers every Group, and starts serving. It defines no Group capability and reads no Definition or Preferences file at runtime.
**Why:** One narrow entry point keeps execution separate from generation sources and from the capabilities it serves.
**Boundary:** Everything served beneath a Group segment stays inside its Group.

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

**Rule:** A Parameter whose type is a published class travels as a JSON object of its fields and is built from that class; a reference to a field of the bound class travels as the field's name and resolves to it, an unknown name failing with the Invalid Input error; every Filter travels as `{field, operator, value}` and every Order as `{field, direction}`, in Body; a Database Instance travels as its name.
**Why:** Every client sends non-simple values the same way in every Group.
**Boundary:** This conversion is part of serving and happens before the Handler runs; the Handler still only calls its Action, and the value's meaning never changes.

#### Action errors map to HTTP by one table

**Rule:** Every error an Endpoint returns is sent as RFC 9457 Problem Details (`application/problem+json`), with `type` set to the error's class name, and with this status: Invalid Input `422`; Setup `409`; Inactive Instance and Connection Failure `503`; Execution, Declaration Mismatch, Configuration, and every other Database error `500`.
**Why:** Every client reads every Group's errors the same way, and the error's class reaches it unchanged.
**Boundary:** This mapping is part of serving every Endpoint; it adds no retry, recovery, or other error-handling Behaviour.

### Configuration

#### Every changeable runtime value lives in the runtime Configuration

**Rule:** Every value the API Configuration Structure defines is always written into the runtime Configuration after generation, even when it equals its default, and Bootstrap reads it only from there.
**Why:** An operator finds and changes the API's address and behaviour in one file, never in source.
**Boundary:** Source holds no runtime value of its own.

### Review

#### API conformance covers every API contract

**Rule:** API is conformant only when its Groups needs in this Definition, the API Interface Schema, and the real API all match one another, and every observation below holds.
**Why:** A gap here silently hides or misplaces a Group for every client.
**Boundary:** Review reads Group files only to compare; it changes nothing outside API's own files.

#### Review observes API through a fixed set of checks

**Rule:** Review establishes API conformance through these observations, every one of them on every review:
- Every need of the Groups layer and every Endpoints Principle in this Definition appears in the API Interface Schema, and the Schema holds nothing beyond them.
- Every listed Group is registered exactly beneath the URL segment of its name, and nothing else is registered.
- Every Group segment, Adapter segment, and Method-and-Path combination is unique.
- Every Group conforms to the API Group Interface Schema.
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

### Interface

**API Interface conforms to the API Interface Schema**

- **Must** — Conform every realization to the API Interface Schema.
- **Never** — Serve anything the Schema does not list or change its structure without a Schema version change.

**Public identities are valid and unique**

- **Must** — Keep every Group segment, Adapter segment, and Method-and-Path combination valid and unique.
- **Never** — Silently repair an invalid or colliding value.

### Groups

**Every Group is referenced by its role and governed by its own files**

- **Must** — Reference every Group by its fixed role and resolve exactly one Definition and Preferences file.
- **Never** — Copy Group content into API or change a Reference because a Group's name changes.

### Bootstrap

**Bootstrap only composes and runs API**

- **Must** — Read the runtime Configuration, create API, register every Group, and start serving.
- **Never** — Define a Group capability or read Definition or Preferences files at runtime.

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
- **Never** — Add retry, recovery, or other error-handling Behaviour through this mapping.

### Configuration

**Every changeable runtime value lives in the runtime Configuration**

- **Must** — Write every value the API Configuration Structure defines into the runtime Configuration after generation, and read it only from there.
- **Never** — Hold a runtime value in source.

### Review

**API conformance covers every API contract**

- **Must** — show that the Groups needs, the API Interface Schema, and the real API all match before API is conformant.
- **Never** — change anything outside API's own files during review.

**Review observes API through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
