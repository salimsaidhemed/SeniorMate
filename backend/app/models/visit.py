from datetime import UTC, datetime

from sqlalchemy import CheckConstraint

from app.extensions import db


class Visit(db.Model):
    __tablename__ = "visits"
    __table_args__ = (
        CheckConstraint("staff_role IN ('aide', 'nurse')", name="ck_visits_staff_role"),
        CheckConstraint(
            "status IN ('scheduled', 'completed', 'cancelled')",
            name="ck_visits_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    visit_date = db.Column(db.Date, nullable=False)
    visit_type = db.Column(db.String(100), nullable=False)
    staff_name = db.Column(db.String(200), nullable=True)
    staff_role = db.Column(db.String(50), nullable=True)
    time_in = db.Column(db.Time, nullable=True)
    time_out = db.Column(db.Time, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="scheduled")
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

    patient = db.relationship("Patient", back_populates="visits")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "visit_date": self.visit_date.isoformat() if self.visit_date else None,
            "visit_type": self.visit_type,
            "staff_name": self.staff_name,
            "staff_role": self.staff_role,
            "time_in": self.time_in.isoformat(timespec="minutes")
            if self.time_in
            else None,
            "time_out": self.time_out.isoformat(timespec="minutes")
            if self.time_out
            else None,
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
