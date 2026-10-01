"""Manual entry point: run CreateTables through the Interface."""

from database.interface import Database

if __name__ == "__main__":
    print(Database().create_tables())
