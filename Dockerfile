FROM apache/airflow:3.3.2

# dbt in an isolated virtualenv: the DAG calls it by path
RUN python -m venv /home/airflow/dbt_venv \
 && /home/airflow/dbt_venv/bin/pip install --no-cache-dir \
      dbt-core==1.12.4 dbt-postgres==1.11.0

# extraction dependencies go into Airflow's own environment.
# Pinning apache-airflow stops pip from upgrading or downgrading Airflow itself.
COPY requirements-airflow.txt /requirements-airflow.txt
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements-airflow.txt