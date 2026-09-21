# Modes

This section defines the operational Modes recorded in State.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Overview](#overview)**
2. **[Not Set](#not-set)**
3. **[Configuring](#configuring)**
4. **[Planning](#planning)**
5. **[Development](#development)**

<br>

<!--------------------------------------------------------------------------------- Overview --->
## Overview

State records the active Mode. Modes describe the current operational position and remain distinct from the behaviour required from the Target.

<br>

<!--------------------------------------------------------------------------------- Not Set --->
## Not Set

State: `not set`.

Responsibility: Represents the initial Workflow position before a Skill action is recorded, or the position restored by Reset.

Inputs: None.

Output: Active State with no selected work scope.

<br>

<!--------------------------------------------------------------------------------- Configuring --->
## Configuring

State: `configuring`.

Responsibility: Create and reconcile the persistent Application Manifest, reconcile operational Config, and synchronize phase State.

Inputs: Operational Schemas, existing Config, and Target phase identities.

Output: Persistent Application Manifest and current operational Config.

<br>

<!--------------------------------------------------------------------------------- Planning --->
## Planning

State: `planning`.

Responsibility: Create bounded and verifiable Tasks without prescribing implementation.

Inputs: Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, and operational records.

Output: Updated Plan Config.

<br>

<!--------------------------------------------------------------------------------- Development --->
## Development

State: `development`.

Responsibility: Implement and verify eligible planned Tasks.

Inputs: Current Target, applicable Implementation Principles and Preferences, synchronized Runtime rules, Plan, State, and existing implementation.

Output: Verified implementation and updated operational records.
