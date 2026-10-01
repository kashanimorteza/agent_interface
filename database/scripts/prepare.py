"""Manual entry point: run Prepare through the Interface."""

from database.interface import Database

if __name__ == "__main__":
    print(Database().prepare())
