"""Load CSV files from a directory into DuckDB's raw schema."""

import argparse
import re
from pathlib import Path

import duckdb

from create_duckdb import DEFAULT_DATABASE, PROJECT_ROOT, create_database


DEFAULT_SOURCE_DIR = PROJECT_ROOT / "data" / "raw"
TABLE_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def load_raw_files(
    source_dir: Path = DEFAULT_SOURCE_DIR,
    database: Path = DEFAULT_DATABASE,
) -> dict[str, int]:
    source_dir = source_dir.expanduser().resolve()
    if not source_dir.is_dir():
        raise FileNotFoundError(f"CSV source directory does not exist: {source_dir}")

    csv_files = sorted(source_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {source_dir}")

    for csv_file in csv_files:
        if not TABLE_NAME_PATTERN.fullmatch(csv_file.stem):
            raise ValueError(f"CSV filename cannot be used as a table name: {csv_file.name}")

    database = create_database(database)
    connection = duckdb.connect(str(database))
    row_counts: dict[str, int] = {}
    try:
        connection.execute("BEGIN TRANSACTION")
        for csv_file in csv_files:
            table_name = csv_file.stem
            csv_path = str(csv_file).replace("'", "''")
            connection.execute(
                f"""
                CREATE OR REPLACE TABLE raw."{table_name}" AS
                SELECT * FROM read_csv_auto('{csv_path}', header = true, all_varchar = true)
                """
            )
            row_counts[table_name] = connection.execute(
                f'SELECT COUNT(*) FROM raw."{table_name}"'
            ).fetchone()[0]
        connection.execute("COMMIT")
    except Exception:
        connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()

    return row_counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help=f"Directory containing CSV files (default: {DEFAULT_SOURCE_DIR})",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help=f"DuckDB database file (default: {DEFAULT_DATABASE})",
    )
    args = parser.parse_args()

    row_counts = load_raw_files(args.source_dir, args.database)
    for table_name, row_count in row_counts.items():
        print(f"Loaded raw.{table_name}: {row_count} rows")


if __name__ == "__main__":
    main()
