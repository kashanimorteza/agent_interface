# launch Skill Contract

## Purpose

Bring the completed Target online and prove that it is reachable.

## Responsibility

Verify the selected Environment, start and connect completed parts through the selected Launch definition, verify readiness, and record usable Access Points. Configure owns Environment preparation and Development owns product repair.

## Trigger

Activate explicitly or after end-to-end orchestration establishes every current launch prerequisite.

## Inputs

Accept no phase selection. Consume Target and Platform selections, Platform authorities, State, developed parts and public interfaces, and observable runtime state.

## Outputs

Produce runtime startup or preservation outcomes, readiness evidence, Launch State and History, verified Access Points, and Blockers or Open Questions under their owners.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Read Platform Principles and Preferences, operational State, and public boundaries of developed parts.

## Authority

Control only project runtime startup, connection, readiness, and shutdown actions required by the selected Launch. Write Launch-owned State and History. Never prepare the Environment, repair code, or redefine a part's internals.

## Workflow Invariants

- Resolve Environment and Launch from explicit Target decisions first and Platform defaults second; never invent a missing definition.
- Require Development completion for every phase currently enabled and ready. Review is an additional prerequisite only when Target, Platform, or the invoking coordinator requires it.
- Mark Launch as launching before mutation and record the final truthful state afterward.
- Verify Environment preparation before startup without performing preparation.
- Follow declared dependency order and stop dependent startup after a failed prerequisite.
- Preserve a running part that already satisfies readiness.
- Deliver required bindings through public boundaries without recording secrets.
- Report only independently verified Access Points.

## Verification

Observe readiness for every launched or preserved part and verify the composed result and every reported Access Point.

## Idempotency

Repeated Launch preserves healthy running parts and changes only runtime elements that do not satisfy the current selected Launch.

## Stopping Conditions

Stop when Environment or Launch is unresolved or incompatible, preparation is unverified, required Development is incomplete, a prerequisite startup fails, readiness fails, or a required binding cannot be delivered safely.

## Runtime Realization

A native adapter resolves concrete startup, shutdown, process, service, and health-check mechanisms from Platform and Runtime mappings and reports selections, environment verification, per-part startup, readiness, Access Points, and unresolved conditions.
