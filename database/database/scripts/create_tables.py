from database.interface import Database


def main() -> None:
    result = Database().create_tables()
    print(f"{result.command}: {result.message}")


if __name__ == "__main__":
    main()
