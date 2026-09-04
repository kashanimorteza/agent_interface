# Definition Principles

This document is the personality of the definition layer — `config/definition.yaml`, the structured form of the project's identity, intended outcomes, and ordered phases. It is written for the interpretation operation that generates it and for the Developer who wants to know what belongs there and what does not.

The shape of `definition.yaml` lives in the schema (`.interface/schema/definition.schema.yaml`). There is no preferences file for definition: it carries project facts, not technical choices.

Every statement here is mandatory.

<br>

## 1. Definition describes the project, never its technology

Definition holds the project's identity, intended outcomes, and ordered project phases — without technical composition or deployment concerns. Technical composition, cross-component connections, runtime, and deployment belong to `development.yaml`. Domain models belong to `model.yaml`.

Each phase's target is part of the human project definition and is preserved here, because choosing which item a phase builds is a project decision, not a technical one.

<br>

## 2. Phases are the units of work

Project phases are the primary units of planning, development, review, and progress. Definition owns each phase's identity, order, target, and intended outcome; every other layer refers to a phase by what definition says about it.
