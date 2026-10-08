"""Create every Table on the default Instance."""

from database import database_error, database_setup

try:
    result = database_setup().create_tables()
except database_error.DatabaseError as error:
    raise SystemExit(f"create_tables failed: {error}") from None
print(f"{result.command}: {result.message}")
