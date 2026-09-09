"""
Storage layer for extracted data. PLACEHOLDER: writes to local JSONL
files under data/raw/ so extraction is runnable without Postgres.
Phase 2 will replace the internals of these functions with real
psycopg2 inserts into Postgres raw tables — callers won't need to change.
"""
import json
import os

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def _write_jsonl(filename: str, records: list[dict]) -> None:
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    path = os.path.join(RAW_DATA_DIR, filename)
    with open(path, "a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
    print(f"Wrote {len(records)} records to {path}")


def save_current_conditions(records: list[dict]) -> None:
    _write_jsonl("current_conditions.jsonl", records)
    
def save_hourly_forecast(records: list[dict]) -> None:
    _write_jsonl("hourly_forecast.jsonl", records)
    
def save_historical(records: list[dict]) -> None:
    _write_jsonl("historical.jsonl", records)