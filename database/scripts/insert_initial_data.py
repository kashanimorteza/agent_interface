"""Manual entry point: run InsertInitialData through the Interface."""

from database.interface import Database

if __name__ == "__main__":
    print(Database().insert_initial_data())
