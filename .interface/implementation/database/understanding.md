# Database Understanding

How the Human explained this Component, in their own words, and what was decided along the way. The Principles state what holds; this file preserves how they were arrived at. It states no obligation: where this record and a Principle disagree, the Principle is correct.

<br>

## Database configuration

**Where does the database information live?** One YAML file holds the database information. Adding a database, or changing a username or password, is one edit in that file and never a change in source. Several Instances live side by side in it, each with its own Engine, connection settings, and credentials, and one of them is the default. Every Instance carries the same keys, and a key that does not apply to its Engine is left empty rather than removed, so moving an Instance to another Engine means filling values in rather than adding keys. The connection credentials and the at-rest encryption key for persisted credential fields are written in that same file.

**Decisions:**

1. The file is `database/database.yaml`, and its shape is the Database Configuration Schema at `.interface/foundation/schema/database.yaml`.
2. Instances are declared side by side, each with its Engine, connection settings, and credentials; `general` is the default.
3. Every Instance carries the same keys — host, port, path, username, password — and an inapplicable key is left empty rather than removed: host and port for a file-backed Engine, path for a server-backed one, username and password for an Engine that does not authenticate.
4. Connection credentials and the at-rest encryption key live in that file. The earlier rule `store_values_in_configuration: false` — no values in the file, environment-variable names instead, secrets delivered by Platform — is removed, because the Human does not agree with it.
5. The configuration file is part of generating the Database Component, not a step after it. Database is not complete without it, and source hardcodes none of its values.
6. How the file is protected — a distinguishing suffix, git exclusion, or another mechanism — is deliberately undecided and is the Human's to settle later. A proposal to fix a `.auth.yml` suffix and exclude the file from version control was set aside for now; no Principle or Preference assumes an answer.
