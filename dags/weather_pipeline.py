"""
Weather pipeline: extract (3 tasks in parallel) -> dbt deps -> seed -> run -> test.

Every load is idempotent (upserts), so retries and overlapping windows are safe.
"""
from datetime import datetime, timedelta, timezone

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task

DBT_BIN = "/home/airflow/dbt_venv/bin/dbt"
DBT_DIR = "/opt/airflow/dbt_project"
DBT_FLAGS = f"--project-dir {DBT_DIR} --profiles-dir {DBT_DIR}"


@dag(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 10, 1, tzinfo=timezone.utc),
    schedule="0 */6 * * *",          # 00:00, 06:00, 12:00, 18:00 UTC
    catchup=False,
    max_active_runs=1,                # never run two dbt builds at once
    default_args={
        "owner": "foysal",
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
        "retry_exponential_backoff": True,
    },
    tags=["weather", "etl"],
)
def weather_pipeline():
    # Imports sit inside the tasks so the DAG file parses fast and never
    # needs DATABASE_URL at parse time.

    @task
    def extract_current() -> int:
        from extraction.db import save_current_conditions
        from extraction.extract_current import extract_current_conditions

        records = extract_current_conditions()
        save_current_conditions(records)
        return len(records)

    @task
    def extract_forecast() -> int:
        from extraction.db import save_hourly_forecast
        from extraction.extract_forecast import extract_hourly_forecast

        records = extract_hourly_forecast()
        save_hourly_forecast(records)
        return len(records)

    @task
    def extract_historical() -> int:
        from extraction.db import save_historical
        from extraction.extract_historical import extract_historical_for_range

        # Archive data lags ~2 days. Re-fetching a 3-day window each run
        # self-heals missed runs and replaces any not-yet-final values.
        end = datetime.now(timezone.utc).date() - timedelta(days=2)
        start = end - timedelta(days=3)
        records = extract_historical_for_range(start.isoformat(), end.isoformat())
        save_historical(records)
        return len(records)

    dbt_deps = BashOperator(task_id="dbt_deps", bash_command=f"{DBT_BIN} deps {DBT_FLAGS}")
    dbt_seed = BashOperator(task_id="dbt_seed", bash_command=f"{DBT_BIN} seed {DBT_FLAGS}")
    dbt_run = BashOperator(task_id="dbt_run", bash_command=f"{DBT_BIN} run {DBT_FLAGS}")
    dbt_test = BashOperator(task_id="dbt_test", bash_command=f"{DBT_BIN} test {DBT_FLAGS}")

    [extract_current(), extract_forecast(), extract_historical()] >> dbt_deps >> dbt_seed >> dbt_run >> dbt_test


weather_pipeline()