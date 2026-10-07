import sys

from database.interface import DatabaseError, Setup

try:
    result = Setup().prepare()
except DatabaseError as error:
    print("prepare failed: " + str(error))
    sys.exit(1)

print(
    f"{result.command}: success={result.success} instance={result.instance.name} "
    f"affected={result.affected} - {result.message}"
)
