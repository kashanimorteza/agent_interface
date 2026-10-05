from database.interface import Database


def main() -> None:
    result = Database().insert_initial_data()
    print(f"{result.command}: {result.message}")


if __name__ == "__main__":
    main()
