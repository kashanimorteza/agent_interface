"""Create the Tables and insert the Initial Data on the default Instance."""

from database import database_error, database_setup

try:
    result = database_setup().prepare()
except database_error.DatabaseError as error:
    raise SystemExit(f"prepare failed: {error}") from None
print(f"{result.command}: {result.message}")
