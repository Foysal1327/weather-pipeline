Phase-1:
A resilient API client with retries/backoff — because unattended scheduled jobs need to survive transient network blips
Three extraction scripts, each capturing not just the data but the metadata needed for analysis later: extracted_at/fetched_at timestamps and utc_offset_seconds — decisions made now because they're expensive to reconstruct later
A placeholder storage layer (db.py) with a stable function signature — so swapping JSONL for Postgres in Phase 2 won't ripple through the extraction scripts at all. That's the point of separating "get the data" from "store the data.

A few things worth remembering:

./sql:/docker-entrypoint-initdb.d — Postgres's official image auto-executes any .sql files in this folder, but only the very first time the container initializes its data volume. If you change raw_schema.sql later, it won't re-run automatically — you'd need to drop the volume (docker compose down -v) or apply changes manually. Fine for now, worth remembering later.
pgdata named volume — keeps your data across docker compose stop/start. It only gets wiped if you explicitly run down -v.
healthcheck — matters once Airflow depends on this container in Phase 4; it needs to know Postgres is actually ready, not just started.

Key notes here, worth understanding:

ON CONFLICT ... DO UPDATE (upsert) matches the UNIQUE constraints you already defined in raw_schema.sql. 
Re-running extract_current.py five times a day won't create duplicate rows — it'll just refresh the same row if the city/timestamp combo repeats. 
This is what makes extraction idempotent — a core ETL property, especially once Airflow retries failed tasks and might re-run the same extraction twice.
execute_values batches the whole list into a single INSERT statement rather than one round-trip per row — much faster for 500+ records.

Phase 2:
- Containerized Postgres with Docker Compose, isolated from other projects via a distinct host port
- Applied the raw schema via Postgres's auto-init mechanism
- Replaced the placeholder JSONL storage layer with real psycopg2 upserts — without touching any extraction script, because the storage interface was designed up front to be swappable
- Idempotent loads via ON CONFLICT DO UPDATE, matched to unique constraints defined in the schema — a prerequisite for safe retries once Airflow enters the picture

stories from phase 3:

The dbt 2.0 vs Postgres incompatibility, solved by pinning versions
The DST bug: the grain test caught it, and fixing it meant converting with timezone names instead of a per-response offset
Known limitation: New York’s fall-back hour on Nov 1 may produce a duplicate local hour in the raw upsert

phase 4:
Airflow 3 differs from the 2.x tutorials: a different service layout and different imports.
Running dbt in an isolated virtualenv inside the Airflow image avoids dependency conflicts.
Two compose stacks were joined with a shared Docker network.
A service-name alias clash was avoided by renaming a service.