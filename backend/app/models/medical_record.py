from datetime import UTC, datetime

from app.extensions import db


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    record_type = db.Column(db.String(100), nullable=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_mime_type = db.Column(db.String(150), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)
    storage_bucket = db.Column(db.String(255), nullable=False)
    storage_object_key = db.Column(db.String(1024), nullable=False, unique=True)
    uploaded_by = db.Column(db.String(200), nullable=True)
    uploaded_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    is_demo_data = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        index=True,
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    patient = db.relationship("Patient", back_populates="medical_records")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "title": self.title,
            "description": self.description,
            "record_type": self.record_type,
            "file_name": self.file_name,
            "file_mime_type": self.file_mime_type,
            "file_size": self.file_size,
            "storage_bucket": self.storage_bucket,
            "storage_object_key": self.storage_object_key,
            "uploaded_by": self.uploaded_by,
            "uploaded_at": self.uploaded_at.isoformat()
            if self.uploaded_at
            else None,
            "is_demo_data": self.is_demo_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
