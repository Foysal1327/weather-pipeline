import os

# Superset refuses to start with the insecure default key
SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

# Superset's own metadata (users, dashboards, charts), kept separate from weather_db
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://superset:superset@superset-db:5432/superset"