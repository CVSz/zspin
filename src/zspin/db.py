from __future__ import annotations

import os

import psycopg2
from psycopg2.extensions import connection


def get_conn() -> connection:
    """Create a PostgreSQL connection from environment variables."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "zspin"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "postgres"),
    )
