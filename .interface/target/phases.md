# Phases

Defines the project's implementation phases. Phases are executed step by step in their defined order, with each phase representing the next intended stage of project development.

<!-------------------------- Phase 1 -->
### Phase 1

```text
id = P1
title = Model
target = Model
is_active = Enabled
readiness = Ready
goal = Implement the independent Model layer and its reusable package from the defined entities, fields, relationships, and rules.
```

<!-------------------------- Phase 2 -->
### Phase 2

```text
id = P2
title = Database
target = Database
is_active = Enabled
readiness = Ready
goal = Implement the database using the shared Model package and insert the defined initial data.
```

<!-------------------------- Phase 3 -->
### Phase 3

```text
id = P3
title = Logic
target = Logic
is_active = Enabled
readiness = Ready
goal = Implement the reusable Logic library for operating on the defined entities.
```

<!-------------------------- Phase 4 -->
### Phase 4

```text
id = P4
title = API
target = API
is_active = Enabled
readiness = Ready
goal = Implement the separate API executable over the Logic library for operating on the defined entities.
```

<!-------------------------- Phase 5 -->
### Phase 5

```text
id = P5
title = Presentation
target = Presentation
is_active = Enabled
readiness = Ready
goal = Implement the Presentation Component as a dashboard with a menu and navigation, in which the records of every defined entity can be listed, searched, filtered, added, edited, enabled, disabled, and deleted.
```

<!-------------------------- Phase 6 -->
### Phase 6

```text
id = P6
title = MetaTrader 5 Platform Module
target = Platform
is_active = Disabled
readiness = Not Designed
goal = Implement the MetaTrader 5 platform module through the common Trading Platform boundary.
```

<!-------------------------- Phase 7 -->
### Phase 7

```text
id = P7
title = Trading Operations
target = Logic
is_active = Disabled
readiness = Not Designed
goal = Implement the execution of the defined trading operations through the selected Trading Platform and Instance.
```
