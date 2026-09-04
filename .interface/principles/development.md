# Development Principles

This document is the personality of the development layer — the part of the Interface that says how the project's selected technical items are connected, run, and deployed. It is written for the Agent that generates `config/development.yaml` and for the Developer who wants to know what that file is allowed to decide.

The exact shape of `config/development.yaml` lives in the schema (`.interface/schema/development.yaml`). There is no preferences file for this layer: development has no technical defaults of its own, because every technology it mentions belongs to an item.

Every statement here is mandatory.

<br>

## 1. Development connects items; it does not define them

Project identity, intended outcomes, and each phase's target belong to `definition.yaml`. Domain models belong to `model.yaml`. Each technical item owns its own internal configuration. Development owns only how the selected items are connected, run, and deployed.

Each component's mapped generated configuration remains the source of truth for its internal technology, responsibility, boundaries, contracts, paths, and implementation details. Development summarizes and connects those values without redefining them.

<br>

## 2. The layer is project-independent

The development schema describes a general technical-development layer and contains no project-specific components, providers, platforms, or topology. Every generated value is resolved for the current project at generation time.

<br>

## 3. Components are selected, not assumed

Components are selected dynamically from the item types currently mapped by `map.yaml`. Every target named by a project phase must resolve to a selected component; additional components are selected only when the project Understanding requires them. The existence of an item schema does not by itself add that component to the project.

<br>

## 4. A connection only carries a contract one of its endpoints owns

Every connection is derived from the contracts produced and consumed by the selected components. A connection cannot create a contract that neither endpoint owns.

<br>

## 5. Runtime and deployment choices are resolved and recorded

The generation operation resolves unspecified runtime and deployment choices using the active agent integration's decision policy. Explicit project constraints are preserved, and consequential agent-selected choices are recorded in `development.yaml`.

<br>

## 6. When development disagrees with an item, the item wins

Component summaries and connections must agree with their owning item configurations. When they differ, the owning item configuration governs and `development.yaml` is reconciled rather than treated as a competing authority.
