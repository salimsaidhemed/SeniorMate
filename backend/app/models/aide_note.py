from datetime import UTC, datetime

from app.extensions import db


class AideNote(db.Model):
    __tablename__ = "aide_notes"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    visit_id = db.Column(
        db.Integer,
        db.ForeignKey("visits.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    personal_care = db.Column(db.JSON, nullable=True)
    nutrition = db.Column(db.JSON, nullable=True)
    mental_status = db.Column(db.JSON, nullable=True)
    elimination = db.Column(db.JSON, nullable=True)
    activity = db.Column(db.JSON, nullable=True)
    assistive_devices = db.Column(db.JSON, nullable=True)
    housekeeping = db.Column(db.JSON, nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)
    aide_name = db.Column(db.String(200), nullable=False)
    signature_data = db.Column(db.Text, nullable=True)
    signature_date = db.Column(db.Date, nullable=True)
    time_in = db.Column(db.Time, nullable=True)
    time_out = db.Column(db.Time, nullable=True)
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

    patient = db.relationship("Patient", back_populates="aide_notes")
    visit = db.relationship("Visit", back_populates="aide_note")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "visit_id": self.visit_id,
            "personal_care": self.personal_care,
            "nutrition": self.nutrition,
            "mental_status": self.mental_status,
            "elimination": self.elimination,
            "activity": self.activity,
            "assistive_devices": self.assistive_devices,
            "housekeeping": self.housekeeping,
            "additional_notes": self.additional_notes,
            "aide_name": self.aide_name,
            "signature_data": self.signature_data,
            "signature_date": self.signature_date.isoformat()
            if self.signature_date
            else None,
            "time_in": self.time_in.isoformat(timespec="minutes")
            if self.time_in
            else None,
            "time_out": self.time_out.isoformat(timespec="minutes")
            if self.time_out
            else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
