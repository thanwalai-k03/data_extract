"""Run a SQL query against the local DuckDB database."""

import argparse
import csv
import sys
from pathlib import Path

import duckdb

from create_duckdb import DEFAULT_DATABASE


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help=f"DuckDB database file (default: {DEFAULT_DATABASE})",
    )
    parser.add_argument(
        "sql",
        nargs="*",
        help="SQL statement; if omitted, SQL is read from standard input",
    )
    args = parser.parse_args()

    sql = " ".join(args.sql) if args.sql else sys.stdin.read()
    if not sql.strip():
        parser.error("Provide a SQL statement or pipe one through standard input.")

    database = args.database.expanduser().resolve()
    if not database.is_file():
        raise FileNotFoundError(
            f"DuckDB database does not exist: {database}. "
            "Run scripts/data_extract.py first."
        )

    connection = duckdb.connect(str(database), read_only=True)
    try:
        result = connection.execute(sql)
        if not result.description:
            print("Query executed (no result set).")
            return

        writer = csv.writer(sys.stdout)
        writer.writerow(column[0] for column in result.description)
        writer.writerows(result.fetchall())
    finally:
        connection.close()


if __name__ == "__main__":
    main()
