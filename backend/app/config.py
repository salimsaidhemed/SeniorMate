import os


class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "change-me-local-only")
    DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://seniormate:change-me-local-only@localhost:5432/seniormate",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "local-access-key")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "change-me-local-only")
    MINIO_BUCKET = os.getenv("MINIO_BUCKET", "seniormate-medical-records")
    MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"
    MEDICAL_RECORD_MAX_FILE_SIZE = int(
        os.getenv("MEDICAL_RECORD_MAX_FILE_SIZE", str(10 * 1024 * 1024))
    )
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
