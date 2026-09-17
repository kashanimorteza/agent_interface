# Modes

This file carries the Modes section of the Interface, moved here verbatim from `interface.md` on 2026-09-17. It is part of Interface Understanding: every Skill reads `interface.md` and this file before acting. The Interface file remains the canonical entry point; this file is one of its sections.

<br>

State records the active Mode. Modes describe the current operational position and remain distinct from the behaviour required from the Target.

<!-------------------------- Not Set -->
### Not Set

```text
state = not set
responsibility = Represents the initial Workflow position before a Skill action is recorded, or the position restored by Reset
inputs = none
output = Active State with no selected work scope
```

<!-------------------------- Configuring -->
### Configuring

```text
state = configuring
responsibility = Create and reconcile the persistent Application Manifest, reconcile operational Config, synchronize phase State, resolve technical requirements, and prepare the selected Platform requirements
inputs = Operational Schemas, existing Config, Target phase identities, Implementation Preferences, Platform selections, and Platform authorities
output = Persistent Application Manifest, current operational Config, resolved technical selections, and a prepared selected Platform runtime
```

<!-------------------------- Planning -->
### Planning

```text
state = planning
responsibility = Create bounded and verifiable Tasks without prescribing implementation
inputs = Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, and operational records
output = Updated Plan Config
```

<!-------------------------- Development -->
### Development

```text
state = development
responsibility = Implement and verify eligible planned Tasks
inputs = Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, Plan, State, and existing implementation
output = Verified implementation and updated operational records
```
