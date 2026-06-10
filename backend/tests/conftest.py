from io import BytesIO

import pytest

from app import create_app
from app.config import Config
from app.extensions import db


class TestConfig(Config):
    TESTING = True
    AUTH_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"
    CORS_ORIGINS = ["http://localhost:5173"]
    MEDICAL_RECORD_MAX_FILE_SIZE = 1024 * 1024
    PATIENT_PHOTO_MAX_FILE_SIZE = 512 * 1024
    BRANDING_LOGO_MAX_FILE_SIZE = 256 * 1024


class FakeMedicalRecordStorage:
    bucket = "test-medical-records"

    def __init__(self):
        self.objects = {}

    def upload(self, object_key, stream, length, content_type):
        self.objects[object_key] = {
            "content": stream.read(length),
            "content_type": content_type,
        }

    def open(self, object_key):
        if object_key not in self.objects:
            raise FileNotFoundError(object_key)
        return BytesIO(self.objects[object_key]["content"])

    def delete(self, object_key):
        self.objects.pop(object_key, None)


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    storage = FakeMedicalRecordStorage()
    app.extensions["medical_record_storage"] = storage
    app.extensions["patient_photo_storage"] = storage
    app.extensions["branding_logo_storage"] = storage

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def medical_record_storage(app):
    return app.extensions["medical_record_storage"]


@pytest.fixture()
def patient_photo_storage(app):
    return app.extensions["patient_photo_storage"]


@pytest.fixture()
def branding_logo_storage(app):
    return app.extensions["branding_logo_storage"]
