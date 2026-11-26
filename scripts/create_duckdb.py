"""Create the local DuckDB database used by the data pipeline."""

import argparse
from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = PROJECT_ROOT / "data" / "northwind.duckdb"


def create_database(database: Path = DEFAULT_DATABASE) -> Path:
    database = database.expanduser().resolve()
    database.parent.mkdir(parents=True, exist_ok=True)

    connection = duckdb.connect(str(database))
    try:
        connection.execute("CREATE SCHEMA IF NOT EXISTS raw")
    finally:
        connection.close()

    return database


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help=f"Database file to create (default: {DEFAULT_DATABASE})",
    )
    args = parser.parse_args()

    database = create_database(args.database)
    print(f"DuckDB database ready: {database}")


if __name__ == "__main__":
    main()
