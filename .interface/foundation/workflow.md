# Workflow

This section defines the Workflow paths used to run Agent Interface.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Define the Project](#define-the-project)**
2. **[Default](#default)**
3. **[Normal](#normal)**
4. **[Detailed](#detailed)**

<br>

<!--------------------------------------------------------------------------------- Define the Project --->
## Define the Project

Define the Target before selecting a Workflow Path:

```text
Human Definition = .interface/target/non-technical.md
Technical Definition = .interface/target/technical.md
```

The Human states the intended outcome in Human Definition, then records its corresponding technical definition without changing that intent.

After the Project is defined, select Default, Normal, or Detailed. The path controls only how much of the Workflow the Human invokes directly; it does not change any operation contract or verification gate.



<br>

<!--------------------------------------------------------------------------------- Default --->
## Default

For the simplest complete run:

```text
/my-interface-implement
```

Implement processes all enabled and ready phases and performs Launch when every required gate is satisfied.



<br>

<!--------------------------------------------------------------------------------- Normal --->
## Normal

For complete orchestration with phase selection:

Run phases separately:

```text
/my-interface-implement 1
/my-interface-implement 2
/my-interface-implement 3
/my-interface-launch
```

Or run several phases together:

```text
/my-interface-implement 1 2 3
/my-interface-launch
```

Launch runs after all required phases are complete.



<br>

<!--------------------------------------------------------------------------------- Detailed --->
## Detailed

For direct control over every operation:

```text
/my-interface-configure
/my-interface-plan 1
/my-interface-develop 1
/my-interface-review 1
If Review is not satisfied: run planning 1, developing 1, reviewer 1 again until it is
Repeat Planning, Developing, and Review for each remaining phase
/my-interface-launch
```

Planning defines the work, Development creates and verifies the implementation, and Review evaluates the resulting Plan coverage and implementation. A phase is reconciled before advancing, and Launch runs only after all required phases satisfy Review.
