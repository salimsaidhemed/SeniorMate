import os


class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "change-me-local-only")
    DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://seniormate:change-me-local-only@localhost:5432/seniormate",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_ENABLED = os.getenv("AUTH_ENABLED", "false").lower() == "true"
    KEYCLOAK_ISSUER = os.getenv(
        "KEYCLOAK_ISSUER",
        "http://localhost:8080/realms/seniormate",
    )
    KEYCLOAK_JWKS_URL = os.getenv(
        "KEYCLOAK_JWKS_URL",
        f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs",
    )
    KEYCLOAK_AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE", "seniormate-api")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "local-access-key")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "change-me-local-only")
    MINIO_BUCKET = os.getenv("MINIO_BUCKET", "seniormate-medical-records")
    MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"
    MEDICAL_RECORD_MAX_FILE_SIZE = int(
        os.getenv("MEDICAL_RECORD_MAX_FILE_SIZE", str(10 * 1024 * 1024))
    )
    PATIENT_PHOTO_MAX_FILE_SIZE = int(
        os.getenv("PATIENT_PHOTO_MAX_FILE_SIZE", str(5 * 1024 * 1024))
    )
    BRANDING_LOGO_MAX_FILE_SIZE = int(
        os.getenv("BRANDING_LOGO_MAX_FILE_SIZE", str(2 * 1024 * 1024))
    )
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
