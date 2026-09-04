# Frontend Principles

This document is the personality of the frontend item: the fixed rules that govern how the frontend is generated, planned, and implemented, whatever language, library, or framework is in play. It is written for the Agent that works on the frontend item and for the Developer who wants to know why the frontend behaves the way it does.

It deliberately names no language, library, framework, package manager, or version. Those are technical choices and live in the preferences file (`.interface/preferences/frontend.yaml`); they may change from project to project without touching a line here. The exact shape of the generated `config/frontend.yaml` lives in the schema (`.interface/schema/frontend.schema.yaml`). The three layers answer different questions: this document answers *why and under what rules*, the preferences answer *with what*, and the schema answers *in what form*.

Every statement here is mandatory. A preference can never override a principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. The backend's HTTP API is the frontend's only door to data

The frontend reaches application data only through the backend's implemented HTTP API and the machine-readable description the backend generates for it. It never connects to the database item, and it never imports backend implementation code.

This is what keeps the frontend replaceable and the backend honest: everything the frontend can do is something the API publicly offers.

<br>

## 2. Domain models are shared, never copied

The shared logical domain-model set comes from `model.yaml`. Frontend configuration and implementation may use it to understand the project, but they never copy or redefine those models. There is one definition of each model, and it is not in the frontend.

<br>

## 3. Packages are chosen from supported profiles, and kept small

Packages selected by an explicit project value or by a supported preference profile are preferred. For an unlisted need inside the authorized scope, the Agent chooses the smallest well-supported compatible package from current evidence and records the consequential choice. It asks only when no safe compatible option can be established.

<br>

## 4. When the project is silent, decide deliberately

An explicit project value always wins. When a frontend technical choice is unstated, the generation operation resolves it from the supported preferences or selects a compatible implementation option, and records the result in the configuration. Downstream operations consume that resolved frontend configuration and never reinterpret the preferences on their own.
