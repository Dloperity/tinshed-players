"""Small, idempotent schema upgrades for databases created by older app versions."""

from sqlalchemy import inspect, text


def ensure_performance_duration_column(engine):
    """Add the nullable duration column without changing existing performance data."""
    inspector = inspect(engine)
    if "performances" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("performances")}
    if "duration_minutes" in existing_columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE performances ADD COLUMN duration_minutes INTEGER NULL")
        )
