import os

from flask import Flask, render_template

from app.models import db
from app.schema_migrations import ensure_performance_duration_column


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///tinshed.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.assignments.routes import bp as assignments_bp
    from app.productions.routes import bp as productions_bp
    from app.volunteers.routes import bp as volunteers_bp
    from app.production_extensions import bp as production_extensions_bp

    app.register_blueprint(volunteers_bp)
    app.register_blueprint(productions_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(production_extensions_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()
        ensure_performance_duration_column(db.engine)

    return app
