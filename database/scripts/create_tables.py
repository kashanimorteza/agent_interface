import sys

from database.interface import DatabaseError, Setup

try:
    result = Setup().create_tables()
except DatabaseError as error:
    print("create_tables failed: " + str(error))
    sys.exit(1)

print(
    f"{result.command}: success={result.success} instance={result.instance.name} "
    f"affected={result.affected} - {result.message}"
)
