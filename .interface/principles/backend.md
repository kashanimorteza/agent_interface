# Backend Principles

This document is the personality of the backend item: the fixed rules that govern how the backend is generated, planned, and implemented, whatever language, framework, or project is in play. It is written for the Agent that works on the backend item and for the Developer who wants to know why the backend behaves the way it does.

It deliberately names no language, framework, package, or version. Those are technical choices and live in the preferences file (`.interface/preferences/backend.yaml`); they may change from project to project without touching a line here. The exact shape of the generated `config/backend.yaml` lives in the schema (`.interface/schema/backend.yaml`). The three layers answer different questions: this document answers *why and under what rules*, the preferences answer *with what*, and the schema answers *in what form*.

Every statement here is mandatory. A preference can never override a principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. The backend runs behaviour and publishes the API — it does not own persistence

The backend never owns the database engine, storage, connection, ORM, model mappings, schema, or migrations. It calls the generic data-access interface published by the database item.

This keeps two responsibilities apart. The database item decides how persistent data is represented and accessed; the backend decides how application behaviour uses the database interface. When the backend needs the persistence interface to change, that is a request to the database item, never a change the backend makes itself.

<br>

## 2. Every domain model gets an API, resolved from the shared model set

When the project asks for an API for its domain models without naming the allowed operations, the default set of operations from the preferences is applied to every model currently indexed in `model.yaml`. An explicit project rule for a model replaces the default operations for that model.

Models are resolved dynamically from `model.yaml` at generation time; they are never copied into these principles or into the preferences. Only model-level operation *intent* is resolved here — which operations a model supports. Endpoint paths, HTTP method mappings, payloads, response shapes, and implementation layout are implementation output and are decided when the backend is built, not here.

<br>

## 3. Credentials are write-only and never leave the backend

A field is a credential when, and only when, the shared model configuration explicitly identifies it as one. The backend never guesses credential fields from their names and never re-decides the database-owned at-rest mode.

A credential field is write-only input: it may be accepted when required to create or update the owning model, and that is the only direction it travels. It is never exposed in an API response, in a generated response schema, or in an error payload. Its value is always redacted from application logs, diagnostics, traces, and exception details.

<br>

## 4. Packages are chosen from supported compatibility, never at random

Runtime packages are resolved from the selected language, API framework, and project requirements through an explicitly supported compatibility entry in the preferences when one exists. Database ORM and driver packages belong to the database item and never enter the backend package set. For an unlisted combination, the Agent chooses a well-supported compatible package from current evidence and records the consequential choice. It asks only when no safe compatible stack can be established.

<br>

## 5. Versions are concrete

Every concrete version the project states is preserved exactly. When a preference supplies *latest*, the generation operation resolves it to the latest stable version compatible with the complete selected backend stack and writes only that concrete version into the configuration; the token *latest* never appears in generated config.

If the current stable version cannot be verified, the best supported concrete compatible version available from current evidence is selected and the choice is recorded. An open question is raised only when compatibility or safety cannot be established without a critical human decision.

<br>

## 6. When the project is silent, decide deliberately

An explicit project value always wins. When a backend technical choice is unstated, the generation operation resolves it from the supported preferences or selects a compatible implementation option, and records the result in the configuration. Downstream operations consume that resolved backend configuration and never reinterpret the preferences on their own.
