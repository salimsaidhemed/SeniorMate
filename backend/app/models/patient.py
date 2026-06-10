from datetime import UTC, datetime

from sqlalchemy import CheckConstraint

from app.extensions import db


class Patient(db.Model):
    __tablename__ = "patients"
    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive')", name="ck_patients_status"),
    )

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    emergency_contact_name = db.Column(db.String(200), nullable=True)
    emergency_contact_phone = db.Column(db.String(50), nullable=True)
    diagnosis_summary = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="active")
    photo_object_key = db.Column(db.String(1024), nullable=True, unique=True)
    photo_file_name = db.Column(db.String(255), nullable=True)
    photo_mime_type = db.Column(db.String(100), nullable=True)
    photo_file_size = db.Column(db.BigInteger, nullable=True)
    photo_uploaded_at = db.Column(db.DateTime(timezone=True), nullable=True)
    photo_verified = db.Column(db.Boolean, nullable=False, default=False)
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
    visits = db.relationship(
        "Visit",
        back_populates="patient",
        cascade="all, delete-orphan",
    )
    aide_notes = db.relationship(
        "AideNote",
        back_populates="patient",
        cascade="all, delete-orphan",
    )
    nurse_notes = db.relationship(
        "NurseNote",
        back_populates="patient",
        cascade="all, delete-orphan",
    )
    medical_records = db.relationship(
        "MedicalRecord",
        back_populates="patient",
        cascade="all, delete-orphan",
    )
    assessments = db.relationship(
        "PatientAssessment",
        back_populates="patient",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat()
            if self.date_of_birth
            else None,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "diagnosis_summary": self.diagnosis_summary,
            "status": self.status,
            "has_photo": bool(self.photo_object_key),
            "photo_verified": self.photo_verified,
            "photo_file_name": self.photo_file_name,
            "photo_uploaded_at": self.photo_uploaded_at.isoformat()
            if self.photo_uploaded_at
            else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
