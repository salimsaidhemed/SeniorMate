from datetime import UTC, datetime

from sqlalchemy import CheckConstraint

from app.extensions import db


class PatientAssessment(db.Model):
    __tablename__ = "patient_assessments"
    __table_args__ = (
        CheckConstraint(
            "assessment_type IN "
            "('fall_risk', 'nutrition', 'mobility', 'cognitive', 'general')",
            name="ck_patient_assessments_type",
        ),
        CheckConstraint(
            "status IN ('draft', 'completed')",
            name="ck_patient_assessments_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    visit_id = db.Column(
        db.Integer,
        db.ForeignKey("visits.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    assessment_type = db.Column(db.String(50), nullable=False)
    assessment_date = db.Column(db.Date, nullable=False)
    performed_by = db.Column(db.String(200), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    findings = db.Column(db.JSON, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="draft")
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

    patient = db.relationship("Patient", back_populates="assessments")
    visit = db.relationship("Visit", back_populates="assessments")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "visit_id": self.visit_id,
            "assessment_type": self.assessment_type,
            "assessment_date": self.assessment_date.isoformat()
            if self.assessment_date
            else None,
            "performed_by": self.performed_by,
            "summary": self.summary,
            "findings": self.findings,
            "recommendations": self.recommendations,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
