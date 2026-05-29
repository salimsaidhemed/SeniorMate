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
    MINIO_BUCKET = os.getenv("MINIO_BUCKET", "seniormate-local")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
