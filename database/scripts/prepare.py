"""Run prepare on the default Instance through the Database Interface."""

import sys

from database.interface import database_setup

result = database_setup().prepare()
print(f"{result.command} on {result.instance.name}: {result.message}")
sys.exit(0 if result.success else 1)
