"""Run the CSV-to-DuckDB raw ingestion pipeline."""

import argparse
from pathlib import Path

from create_duckdb import DEFAULT_DATABASE
from load_raw import DEFAULT_SOURCE_DIR, load_raw_files


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
    print(f"Loaded {len(row_counts)} CSV file(s) into {args.database.expanduser().resolve()}")
    for table_name, row_count in row_counts.items():
        print(f"  raw.{table_name}: {row_count} rows")


if __name__ == "__main__":
    main()
