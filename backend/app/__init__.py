from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger, swag_from
from sqlalchemy import text

from app.config import Config
from app.demo_data import register_demo_commands
from app.auth import protect_api_request
from app.extensions import db, migrate
from app.models import AideNote as AideNote
from app.models import MedicalRecord as MedicalRecord
from app.models import NurseNote as NurseNote
from app.models import OrganizationSettings as OrganizationSettings
from app.models import Patient as Patient
from app.models import PatientAssessment as PatientAssessment
from app.models import Visit as Visit
from app.routes.assessments import assessments_bp
from app.routes.admin_users import admin_users_bp
from app.routes.aide_notes import aide_notes_bp
from app.routes.dashboard import dashboard_bp
from app.routes.branding import branding_bp
from app.routes.medical_records import medical_records_bp
from app.routes.nurse_notes import nurse_notes_bp
from app.routes.patients import patients_bp
from app.routes.reports import reports_bp
from app.routes.visits import visits_bp
from app.swagger import health_spec, swagger_config, swagger_template
from app.version import __version__


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    Swagger(app, config=swagger_config, template=swagger_template)

    db.init_app(app)
    migrate.init_app(app, db)
    app.before_request(protect_api_request)
    app.register_blueprint(assessments_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(aide_notes_bp)
    app.register_blueprint(branding_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(medical_records_bp)
    app.register_blueprint(nurse_notes_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(visits_bp)
    register_demo_commands(app)

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
                "version": __version__,
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
                "version": __version__,
                "message": "SeniorMate backend is running.",
            }
        )

    return app
