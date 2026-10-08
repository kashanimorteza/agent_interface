"""Insert the Initial Data on the default Instance."""

from database import database_error, database_setup

try:
    result = database_setup().insert_initial_data()
except database_error.DatabaseError as error:
    raise SystemExit(f"insert_initial_data failed: {error}") from None
print(f"{result.command}: {result.message}")
