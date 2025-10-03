from datetime import date
from app import create_app, db
from app.models import Patient, Visit, Assessment, Signature

app = create_app()

with app.app_context():
    # Drop + recreate schema (dev only, comment out in production)
    db.drop_all()
    db.create_all()

    # Create a patient
    patient = Patient(
        name="Jane Doe",
        mr_number="MR001",
        gender="F",
        dob=date(1948, 3, 15)
    )
    db.session.add(patient)
    db.session.commit()

    # Create a visit
    visit = Visit(
        patient_id=patient.id,
        visit_type="Nurses Progress Note"
    )
    db.session.add(visit)
    db.session.commit()

    # Create an assessment (store JSON in data column)
    assessment = Assessment(
        visit_id=visit.id,
        section="Pain Assessment",
        data={"location": "Back", "intensity": "6", "management": "Paracetamol"}
    )
    db.session.add(assessment)

    # Add a signature
    signature = Signature(
        visit_id=visit.id,
        signer_name="Nurse Alice",
        signature_date=date.today(),
        signature_image="base64-encoded-placeholder"
    )
    db.session.add(signature)

    db.session.commit()

    print("✅ Seed data inserted successfully")
