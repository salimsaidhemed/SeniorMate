from datetime import datetime
from app import db



class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    mr_number = db.Column(db.String(50), unique=True,nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    visits = db.relationship("Visit", back_populates="patient")

class Visit(db.Model):
    __tablename__ = "visits"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    visit_date = db.Column(db.Date, default=datetime.utcnow)
    visit_type = db.Column(db.String(120))   # e.g. "Home Health Aide Note"
    narrative = db.Column(db.Text)

    patient = db.relationship("Patient", back_populates="visits")
    vitals = db.relationship("VitalSigns", back_populates="visit", uselist=False)
    assessments = db.relationship("Assessment", back_populates="visit")
    signature = db.relationship("Signature", back_populates="visit", uselist=False)

class VitalSigns(db.Model):
    __tablename__ = "vital_signs"
    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.id"))
    diet = db.Column(db.String(200))

    visit = db.relationship("Visit", back_populates="vitals")
    bp_measurements = db.relationship("BPMeasurement", back_populates="vital_signs")
    pulse_resp = db.relationship("PulseResp", back_populates="vital_signs", uselist=False)

class BPMeasurement(db.Model):
    __tablename__ = "bp_measurements"
    id = db.Column(db.Integer, primary_key=True)
    vital_id = db.Column(db.Integer, db.ForeignKey("vital_signs.id"))
    position = db.Column(db.String(50)) # lying, sitting, standing
    side = db.Column(db.String(10)) # R or L
    systolic = db.Column(db.String(10))
    diastolic = db.Column(db.String(10))

    vital_signs = db.relationship("VitalSigns", back_populates="bp_measurements")

class PulseResp(db.Model):
    __tablename__ = "pulse_resp"
    id = db.Column(db.Integer, primary_key=True)
    vital_id = db.Column(db.Integer, db.ForeignKey("vital_signs.id"))
    pulse_apical = db.Column(db.String(20))
    pulse_radial = db.Column(db.String(20))
    resp_rate = db.Column(db.String(20))
    temperature = db.Column(db.String(20))

    vital_signs = db.relationship("VitalSigns", back_populates="pulse_resp")

class Assessment(db.Model):
    __tablename__ = "assessments"
    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.id"))
    section = db.Column(db.String(120))   # e.g. "Neuro", "Respiratory", "Pain"
    data = db.Column(db.JSON)             # flexible JSON for fields

    visit = db.relationship("Visit", back_populates="assessments")

class Signature(db.Model):
    __tablename__ = "signatures"
    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.id"))
    signer_name = db.Column(db.String(120))
    signature_date = db.Column(db.Date, default=datetime.utcnow)
    signature_image = db.Column(db.Text)  # base64 string

    visit = db.relationship("Visit", back_populates="signature")
