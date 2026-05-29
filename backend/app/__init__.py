from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger, swag_from
from sqlalchemy import text

from app.config import Config
from app.extensions import db, migrate
from app.models import Patient as Patient
from app.routes.patients import patients_bp
from app.swagger import health_spec, swagger_config, swagger_template


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    Swagger(app, config=swagger_config, template=swagger_template)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(patients_bp)

    @app.get("/api/health")
    @swag_from(health_spec)
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
