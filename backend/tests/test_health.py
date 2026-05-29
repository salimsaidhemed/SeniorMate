from app import create_app
from app.config import Config
from app.extensions import db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"
    CORS_ORIGINS = ["http://localhost:5173"]


def test_create_app():
    app = create_app(TestConfig)

    assert app is not None
    assert app.config["TESTING"] is True


def test_health_endpoint_returns_success():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    response = app.test_client().get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
    assert response.get_json()["database"] == "ok"
