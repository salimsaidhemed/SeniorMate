from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text

from app.config import Config
from app.extensions import db, migrate


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    db.init_app(app)
    migrate.init_app(app, db)

    @app.get("/api/health")
    def health():
        database = "ok"
        status_code = 200

        try:
            db.session.execute(text("SELECT 1"))
        except Exception:
            database = "unavailable"
            status_code = 503

        return jsonify(
            {
                "service": "seniormate-backend",
                "status": "ok" if status_code == 200 else "degraded",
                "database": database,
                "minio_endpoint": app.config["MINIO_ENDPOINT"],
            }
        ), status_code

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "seniormate-backend",
                "message": "SeniorMate backend is running.",
            }
        )

    return app
