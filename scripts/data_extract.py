"""Run the current and legacy Northwind CSV ingestion pipeline."""

import argparse
from pathlib import Path

from create_duckdb import DEFAULT_DATABASE
from load_raw import DEFAULT_LEGACY_DIR, DEFAULT_SOURCE_DIR, load_raw_files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help=f"Directory containing current CSV files (default: {DEFAULT_SOURCE_DIR})",
    )
    parser.add_argument(
        "--legacy-dir",
        type=Path,
        default=DEFAULT_LEGACY_DIR,
        help=f"Directory containing legacy CSV files (default: {DEFAULT_LEGACY_DIR})",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help=f"DuckDB database file (default: {DEFAULT_DATABASE})",
    )
    args = parser.parse_args()

    row_counts = load_raw_files(args.source_dir, args.database, args.legacy_dir)
    print(f"Loaded data into {args.database.expanduser().resolve()}")
    for table, row_count in row_counts.items():
        print(f"  raw.{table}: {row_count:,} rows")
    print("Done.")


if __name__ == "__main__":
    main()
