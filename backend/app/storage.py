from urllib.parse import urlparse

from flask import current_app
from minio import Minio
from minio.error import S3Error


class PrivateObjectStorageError(Exception):
    pass


class MinioPrivateObjectStorage:
    def __init__(self, client, bucket):
        self.client = client
        self.bucket = bucket

    def ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except Exception as exc:
            raise PrivateObjectStorageError("Private file storage is unavailable.") from exc

    def upload(self, object_key, stream, length, content_type):
        self.ensure_bucket()
        try:
            self.client.put_object(
                self.bucket,
                object_key,
                stream,
                length,
                content_type=content_type,
            )
        except Exception as exc:
            raise PrivateObjectStorageError("Private file upload failed.") from exc

    def open(self, object_key):
        try:
            return self.client.get_object(self.bucket, object_key)
        except S3Error as exc:
            if exc.code in {"NoSuchKey", "NoSuchObject"}:
                raise FileNotFoundError(object_key) from exc
            raise PrivateObjectStorageError("Private file download failed.") from exc
        except Exception as exc:
            raise PrivateObjectStorageError("Private file download failed.") from exc

    def delete(self, object_key):
        try:
            self.client.remove_object(self.bucket, object_key)
        except S3Error as exc:
            if exc.code not in {"NoSuchKey", "NoSuchObject"}:
                raise PrivateObjectStorageError(
                    "Private file storage cleanup failed."
                ) from exc
        except Exception as exc:
            raise PrivateObjectStorageError(
                "Private file storage cleanup failed."
            ) from exc


def build_minio_storage():
    endpoint = current_app.config["MINIO_ENDPOINT"]
    parsed = urlparse(endpoint)
    minio_endpoint = parsed.netloc or parsed.path
    secure = current_app.config["MINIO_SECURE"]

    client = Minio(
        minio_endpoint,
        access_key=current_app.config["MINIO_ACCESS_KEY"],
        secret_key=current_app.config["MINIO_SECRET_KEY"],
        secure=secure,
    )
    return MinioPrivateObjectStorage(client, current_app.config["MINIO_BUCKET"])


def get_medical_record_storage():
    storage = current_app.extensions.get("medical_record_storage")
    if storage is None:
        storage = build_minio_storage()
        current_app.extensions["medical_record_storage"] = storage
    return storage


def get_patient_photo_storage():
    storage = current_app.extensions.get("patient_photo_storage")
    if storage is None:
        storage = build_minio_storage()
        current_app.extensions["patient_photo_storage"] = storage
    return storage
