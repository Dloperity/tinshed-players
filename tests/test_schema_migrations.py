import sqlite3

from app import create_app
from app.models import Performance, db


def test_existing_database_gets_nullable_duration_column_without_losing_rows(tmp_path):
    database_path = tmp_path / "legacy.db"
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "CREATE TABLE productions ("
            "id INTEGER PRIMARY KEY, title VARCHAR(200) NOT NULL, created_at DATETIME NOT NULL)"
        )
        connection.execute(
            "CREATE TABLE performances ("
            "id INTEGER PRIMARY KEY, production_id INTEGER NOT NULL, date DATE NOT NULL, "
            "start_time TIME NOT NULL, created_at DATETIME NOT NULL)"
        )
        connection.execute(
            "INSERT INTO productions (id, title, created_at) "
            "VALUES (1, 'Legacy Show', '2026-09-01 00:00:00')"
        )
        connection.execute(
            "INSERT INTO performances (id, production_id, date, start_time, created_at) "
            "VALUES (1, 1, '2026-09-04', '19:30:00', '2026-09-01 00:00:00')"
        )

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )
    with app.app_context():
        performance = db.session.get(Performance, 1)
        assert performance is not None
        assert performance.date.isoformat() == "2026-09-04"
        assert performance.duration_minutes is None
