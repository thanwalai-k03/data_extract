# data_extract

## CSV to DuckDB

Create and activate the project virtual environment, then install the dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Put CSV files in `data/raw/`. Run the ingestion pipeline to create
`data/northwind.duckdb` and load each CSV as a table in the `raw` schema:

```bash
python scripts/data_extract.py
```

You can also run the steps separately:

```bash
python scripts/create_duckdb.py
python scripts/load_raw.py
```

Run a query (results are printed as CSV):

```bash
python scripts/query.py "SELECT * FROM raw.orders LIMIT 5"
```

Use `--source-dir` and `--database` to override the default paths. CSV values
are loaded as strings so the raw tables preserve the source data.
