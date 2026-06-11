from datetime import UTC, datetime

from app.extensions import db


class NurseNote(db.Model):
    __tablename__ = "nurse_notes"

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
    diagnosis = db.Column(db.Text, nullable=True)
    living_arrangements = db.Column(db.JSON, nullable=True)
    visit_type = db.Column(db.JSON, nullable=True)
    vital_signs = db.Column(db.JSON, nullable=True)
    diet = db.Column(db.JSON, nullable=True)
    pain_assessment = db.Column(db.JSON, nullable=True)
    sensory = db.Column(db.JSON, nullable=True)
    neuro = db.Column(db.JSON, nullable=True)
    respiratory = db.Column(db.JSON, nullable=True)
    cardiac = db.Column(db.JSON, nullable=True)
    peripheral_circulation = db.Column(db.JSON, nullable=True)
    genitourinary = db.Column(db.JSON, nullable=True)
    gastrointestinal = db.Column(db.JSON, nullable=True)
    endocrine = db.Column(db.JSON, nullable=True)
    skin_integrity = db.Column(db.JSON, nullable=True)
    wound_evaluation = db.Column(db.JSON, nullable=True)
    mental_status = db.Column(db.JSON, nullable=True)
    functional_status = db.Column(db.JSON, nullable=True)
    homebound_status = db.Column(db.JSON, nullable=True)
    skilled_nursing = db.Column(db.Text, nullable=True)
    response_to_intervention = db.Column(db.Text, nullable=True)
    patient_caregiver_understanding = db.Column(db.JSON, nullable=True)
    md_contact = db.Column(db.JSON, nullable=True)
    discharge_planning = db.Column(db.Text, nullable=True)
    patient_feedback = db.Column(db.Text, nullable=True)
    narrative = db.Column(db.Text, nullable=True)
    signature_data = db.Column(db.Text, nullable=True)
    signature_date = db.Column(db.Date, nullable=True)
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

    patient = db.relationship("Patient", back_populates="nurse_notes")
    visit = db.relationship("Visit", back_populates="nurse_note")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "visit_id": self.visit_id,
            "diagnosis": self.diagnosis,
            "living_arrangements": self.living_arrangements,
            "visit_type": self.visit_type,
            "vital_signs": self.vital_signs,
            "diet": self.diet,
            "pain_assessment": self.pain_assessment,
            "sensory": self.sensory,
            "neuro": self.neuro,
            "respiratory": self.respiratory,
            "cardiac": self.cardiac,
            "peripheral_circulation": self.peripheral_circulation,
            "genitourinary": self.genitourinary,
            "gastrointestinal": self.gastrointestinal,
            "endocrine": self.endocrine,
            "skin_integrity": self.skin_integrity,
            "wound_evaluation": self.wound_evaluation,
            "mental_status": self.mental_status,
            "functional_status": self.functional_status,
            "homebound_status": self.homebound_status,
            "skilled_nursing": self.skilled_nursing,
            "response_to_intervention": self.response_to_intervention,
            "patient_caregiver_understanding": self.patient_caregiver_understanding,
            "md_contact": self.md_contact,
            "discharge_planning": self.discharge_planning,
            "patient_feedback": self.patient_feedback,
            "narrative": self.narrative,
            "signature_data": self.signature_data,
            "signature_date": self.signature_date.isoformat()
            if self.signature_date
            else None,
            "is_demo_data": self.is_demo_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
