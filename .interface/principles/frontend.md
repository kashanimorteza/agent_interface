# Frontend Principles

Frontend Principles define the fixed philosophy, responsibilities, and boundaries of the Frontend Component, independent of any language, library, framework, package manager, or project.

Technical choices and defaults belong to Frontend Preferences. The exact shape of the generated Frontend configuration belongs to the Frontend Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. The Backend HTTP API is the Frontend's only door to application data

Frontend reaches application data only through the implemented HTTP API published by Backend and its machine-readable description. It never connects to Database and never imports Backend implementation code.

This keeps Frontend replaceable and Backend accountable: every application-data capability available to Frontend is explicitly provided through the API.

<br>

## 2. Domain Models are shared, never copied

The shared logical domain-model set comes from the Model Component. Frontend configuration and implementation may use it, but they never copy or redefine those Models. There is one logical definition of each Model, and it is not owned by Frontend.
