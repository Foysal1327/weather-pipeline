"""
Storage layer for extracted data. PLACEHOLDER: writes to local JSONL
files under data/raw/ so extraction is runnable without Postgres.
Phase 2 will replace the internals of these functions with real
psycopg2 inserts into Postgres raw tables — callers won't need to change.
"""
import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

# RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
DATABASE_URL = os.environ["DATABASE_URL"]


# def _write_jsonl(filename: str, records: list[dict]) -> None:
#     os.makedirs(RAW_DATA_DIR, exist_ok=True)
#     path = os.path.join(RAW_DATA_DIR, filename)
#     with open(path, "a", encoding="utf-8") as f:
#         for record in records:
#             f.write(json.dumps(record) + "\n")
#     print(f"Wrote {len(records)} records to {path}")

def _get_connection():
    return psycopg2.connect(DATABASE_URL)

def _bulk_upsert(table: str, records: list[dict], conflict_cols: list[str]) -> None:
    if not records:
        print(f"No records to write to {table}")
        return

    columns = list(records[0].keys())
    values = [[r[col] for col in columns] for r in records]

    update_cols = [c for c in columns if c not in conflict_cols]
    conflict_clause = ", ".join(conflict_cols)
    update_clause = ", ".join(f"{c} = EXCLUDED.{c}" for c in update_cols)

    query = f"""
        INSERT INTO {table} ({", ".join(columns)})
        VALUES %s
        ON CONFLICT ({conflict_clause})
        DO UPDATE SET {update_clause}
    """

    with _get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, query, values)
        conn.commit()

    print(f"Upserted {len(records)} records into {table}")

def save_current_conditions(records: list[dict]) -> None:
    # _write_jsonl("current_conditions.jsonl", records)
    _bulk_upsert("raw.current_conditions", records, conflict_cols=["city_id", "observed_at"])
    
def save_hourly_forecast(records: list[dict]) -> None:
    # _write_jsonl("hourly_forecast.jsonl", records)
    _bulk_upsert("raw.hourly_forecast", records, conflict_cols=["city_id", "forecast_for", "fetched_at"])
    
def save_historical(records: list[dict]) -> None:
    # _write_jsonl("historical.jsonl", records)
    _bulk_upsert("raw.historical", records, conflict_cols=["city_id", "observed_at"])