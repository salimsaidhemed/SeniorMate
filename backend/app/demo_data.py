from datetime import UTC, date, datetime, time, timedelta
from io import BytesIO

import click
from flask import current_app

from app.extensions import db
from app.models import (
    AideNote,
    MedicalRecord,
    NurseNote,
    Patient,
    PatientAssessment,
    Visit,
)
from app.storage import PrivateObjectStorageError, get_medical_record_storage


DEMO_PATIENTS = (
    ("Maya", "Henderson", "1942-03-14", "female", "Hypertension and osteoarthritis"),
    ("Arthur", "Bennett", "1938-11-02", "male", "Type 2 diabetes and reduced mobility"),
    ("Elena", "Morales", "1946-07-21", "female", "Chronic obstructive pulmonary disease"),
    ("Samuel", "Brooks", "1940-01-09", "male", "Congestive heart failure"),
    ("Nora", "Patel", "1951-05-18", "female", "Early cognitive impairment"),
    ("George", "Kim", "1936-09-27", "male", "Post-stroke weakness"),
    ("Lillian", "Foster", "1944-12-06", "female", "Osteoporosis and fall risk"),
    ("Henry", "Wallace", "1948-04-30", "male", "Parkinsonian symptoms"),
    ("Rosa", "Martinez", "1939-08-12", "female", "Diabetes and peripheral neuropathy"),
    ("Edward", "Clarke", "1943-02-25", "male", "Coronary artery disease"),
    ("Grace", "Nguyen", "1950-10-16", "female", "Chronic kidney disease"),
    ("Walter", "Reed", "1937-06-03", "male", "Arthritis and chronic pain"),
    ("Irene", "Sullivan", "1945-01-29", "female", "Macular degeneration"),
    ("Frank", "Douglas", "1941-07-08", "male", "Hypertension and balance concerns"),
    ("Teresa", "Ramirez", "1949-03-19", "female", "Recovery after hip replacement"),
    ("Leonard", "Price", "1935-12-11", "male", "Mild dementia"),
    ("June", "Carter", "1947-05-05", "female", "Asthma and limited endurance"),
    ("Raymond", "Owens", "1942-09-23", "male", "Diabetes and wound monitoring"),
    ("Dolores", "Evans", "1938-04-17", "female", "Heart failure and edema"),
    ("Albert", "Turner", "1946-11-28", "male", "Post-operative rehabilitation"),
    ("Beatrice", "Coleman", "1940-06-15", "female", "Nutrition and weight monitoring"),
    ("Victor", "Hayes", "1952-02-04", "male", "Multiple sclerosis"),
    ("Marian", "Perry", "1943-08-31", "female", "Anxiety and medication support"),
    ("Louis", "Ward", "1939-10-20", "male", "Respiratory monitoring"),
)

AIDE_NAMES = ("Avery Johnson", "Jordan Lee", "Morgan Davis", "Casey Brown")
NURSE_NAMES = ("Taylor Morgan, RN", "Riley Chen, RN", "Jamie Patel, LPN")
VISIT_TYPES = (
    "Personal care",
    "Skilled nursing",
    "Medication review",
    "Wellness check",
    "Mobility support",
)
ASSESSMENT_TYPES = ("fall_risk", "nutrition", "mobility", "cognitive", "general")


def _demo_enabled():
    return current_app.config.get("DEMO_DATA_ENABLED", False)


def _require_demo_enabled():
    if current_app.config.get("APP_ENV") == "production":
        raise click.ClickException(
            "Demo data commands are unavailable when APP_ENV=production."
        )
    if not _demo_enabled():
        raise click.ClickException(
            "Demo data is disabled. Set DEMO_DATA_ENABLED=true explicitly "
            "before running this command."
        )


def _pdf_bytes(patient_name):
    message = f"SeniorMate fictional demo care summary for {patient_name}."
    content = f"BT /F1 12 Tf 72 720 Td ({message}) Tj ET".encode("ascii")
    objects = (
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>"
        ),
        b"<< /Length "
        + str(len(content)).encode("ascii")
        + b" >>\nstream\n"
        + content
        + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    )
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for object_number, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_number} 0 obj\n".encode("ascii"))
        pdf.extend(body)
        pdf.extend(b"\nendobj\n")
    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(pdf)


def _non_demo_dependencies_exist(patient_ids, visit_ids):
    checks = (
        Visit.query.filter(
            Visit.patient_id.in_(patient_ids),
            Visit.is_demo_data.is_(False),
        ),
        AideNote.query.filter(
            AideNote.patient_id.in_(patient_ids),
            AideNote.is_demo_data.is_(False),
        ),
        NurseNote.query.filter(
            NurseNote.patient_id.in_(patient_ids),
            NurseNote.is_demo_data.is_(False),
        ),
        PatientAssessment.query.filter(
            PatientAssessment.patient_id.in_(patient_ids),
            PatientAssessment.is_demo_data.is_(False),
        ),
        MedicalRecord.query.filter(
            MedicalRecord.patient_id.in_(patient_ids),
            MedicalRecord.is_demo_data.is_(False),
        ),
    )
    if visit_ids:
        checks += (
            AideNote.query.filter(
                AideNote.visit_id.in_(visit_ids),
                AideNote.is_demo_data.is_(False),
            ),
            NurseNote.query.filter(
                NurseNote.visit_id.in_(visit_ids),
                NurseNote.is_demo_data.is_(False),
            ),
            PatientAssessment.query.filter(
                PatientAssessment.visit_id.in_(visit_ids),
                PatientAssessment.is_demo_data.is_(False),
            ),
        )
    return any(query.first() is not None for query in checks)


def clear_demo_records():
    demo_patients = Patient.query.filter_by(is_demo_data=True).all()
    patient_ids = [patient.id for patient in demo_patients]
    visit_ids = [
        visit_id
        for (visit_id,) in db.session.query(Visit.id)
        .filter(Visit.is_demo_data.is_(True))
        .all()
    ]

    if patient_ids and _non_demo_dependencies_exist(patient_ids, visit_ids):
        raise click.ClickException(
            "Demo patients or visits have non-demo dependent records. "
            "Clear or reclassify those records before deleting demo data."
        )

    records = MedicalRecord.query.filter_by(is_demo_data=True).all()
    storage = get_medical_record_storage()
    for record in records:
        storage.delete(record.storage_object_key)

    counts = {
        "medical_records": len(records),
        "assessments": PatientAssessment.query.filter_by(is_demo_data=True).count(),
        "aide_notes": AideNote.query.filter_by(is_demo_data=True).count(),
        "nurse_notes": NurseNote.query.filter_by(is_demo_data=True).count(),
        "visits": Visit.query.filter_by(is_demo_data=True).count(),
        "patients": len(demo_patients),
    }

    MedicalRecord.query.filter_by(is_demo_data=True).delete(
        synchronize_session=False
    )
    PatientAssessment.query.filter_by(is_demo_data=True).delete(
        synchronize_session=False
    )
    AideNote.query.filter_by(is_demo_data=True).delete(synchronize_session=False)
    NurseNote.query.filter_by(is_demo_data=True).delete(synchronize_session=False)
    Visit.query.filter_by(is_demo_data=True).delete(synchronize_session=False)
    Patient.query.filter_by(is_demo_data=True).delete(synchronize_session=False)
    db.session.commit()
    return counts


def seed_demo_records(today=None):
    clear_demo_records()
    current_date = today or date.today()
    storage = get_medical_record_storage()
    uploaded_keys = []
    counts = {
        "patients": 0,
        "visits": 0,
        "aide_notes": 0,
        "nurse_notes": 0,
        "assessments": 0,
        "medical_records": 0,
    }

    try:
        for index, patient_data in enumerate(DEMO_PATIENTS, start=1):
            first_name, last_name, birth_date, gender, diagnosis = patient_data
            patient = Patient(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date.fromisoformat(birth_date),
                gender=gender,
                phone=f"202-555-{1000 + index:04d}",
                email=f"{first_name.lower()}.{last_name.lower()}@example.test",
                address=f"{100 + index} Demo Lane, Sample City, ST 200{index:02d}",
                emergency_contact_name=f"{first_name} Family Contact",
                emergency_contact_phone=f"202-555-{2000 + index:04d}",
                diagnosis_summary=diagnosis,
                status="inactive" if index % 7 == 0 else "active",
                is_demo_data=True,
            )
            db.session.add(patient)
            db.session.flush()
            counts["patients"] += 1

            patient_visits = []
            for visit_number in range(4):
                sequence = (index - 1) * 4 + visit_number
                days_ago = (sequence * 7) % 91
                visit_day = current_date - timedelta(days=days_ago)
                staff_role = "aide" if visit_number % 2 == 0 else "nurse"
                staff_name = (
                    AIDE_NAMES[sequence % len(AIDE_NAMES)]
                    if staff_role == "aide"
                    else NURSE_NAMES[sequence % len(NURSE_NAMES)]
                )
                start_hour = 8 + sequence % 7
                status = (
                    "cancelled"
                    if sequence % 13 == 0
                    else "scheduled"
                    if sequence % 11 == 0
                    else "completed"
                )
                visit = Visit(
                    patient_id=patient.id,
                    visit_date=visit_day,
                    visit_type=VISIT_TYPES[sequence % len(VISIT_TYPES)],
                    staff_name=staff_name,
                    staff_role=staff_role,
                    time_in=time(start_hour, 0),
                    time_out=time(start_hour + 1, 15),
                    notes=(
                        "Fictional demo visit completed with routine safety "
                        "checks and care-plan review."
                    ),
                    status=status,
                    is_demo_data=True,
                )
                db.session.add(visit)
                db.session.flush()
                patient_visits.append(visit)
                counts["visits"] += 1

                note_timestamp = datetime.combine(
                    visit_day,
                    time(start_hour + 1, 30),
                    tzinfo=UTC,
                )
                if status == "completed" and staff_role == "aide":
                    db.session.add(
                        AideNote(
                            patient_id=patient.id,
                            visit_id=visit.id,
                            personal_care={
                                "bathing": True,
                                "grooming": True,
                                "dressing": sequence % 3 != 0,
                            },
                            nutrition={
                                "meal_prepared": True,
                                "meal_percentage": 75 + (sequence % 3) * 10,
                                "fluids_encouraged": True,
                            },
                            mental_status={"alert": True, "confused": False},
                            elimination={"toileting_assistance": sequence % 2 == 0},
                            activity={"ambulation": True, "range_of_motion": True},
                            assistive_devices={
                                "walker": index % 3 == 0,
                                "cane": index % 3 == 1,
                            },
                            housekeeping={"laundry": True, "light_cleaning": True},
                            additional_notes=(
                                "Patient tolerated care well and remained "
                                "comfortable throughout the fictional demo visit."
                            ),
                            aide_name=staff_name,
                            signature_data="Demo signature on file",
                            signature_date=visit_day,
                            time_in=visit.time_in,
                            time_out=visit.time_out,
                            created_at=note_timestamp,
                            updated_at=note_timestamp,
                            is_demo_data=True,
                        )
                    )
                    counts["aide_notes"] += 1
                elif status == "completed" and staff_role == "nurse":
                    systolic = 116 + sequence % 18
                    db.session.add(
                        NurseNote(
                            patient_id=patient.id,
                            visit_id=visit.id,
                            diagnosis=diagnosis,
                            living_arrangements={"setting": "home", "support": True},
                            visit_type={"skilled_nursing": True},
                            vital_signs={
                                "blood_pressure": f"{systolic}/{70 + sequence % 10}",
                                "pulse": 68 + sequence % 12,
                                "temperature_f": 97.8 + (sequence % 4) * 0.2,
                                "oxygen_saturation": 95 + sequence % 4,
                            },
                            diet={"ordered": "heart healthy", "tolerance": "good"},
                            pain_assessment={
                                "score": sequence % 4,
                                "location": "generalized" if sequence % 4 else "none",
                            },
                            respiratory={"effort": "unlabored", "lungs": "clear"},
                            cardiac={"rhythm": "regular", "edema": index % 6 == 0},
                            skin_integrity={"intact": index % 5 != 0},
                            wound_evaluation={
                                "present": index % 5 == 0,
                                "status": "stable" if index % 5 == 0 else "none",
                            },
                            skilled_nursing=(
                                "Medication reconciliation, vital-sign review, "
                                "and fictional care-plan education completed."
                            ),
                            response_to_intervention=(
                                "Patient demonstrated stable response."
                            ),
                            patient_caregiver_understanding={"teach_back": True},
                            narrative=(
                                "Demo clinical narrative: no acute distress; "
                                "continue current plan and routine monitoring."
                            ),
                            signature_data="Demo clinician signature on file",
                            signature_date=visit_day,
                            created_at=note_timestamp,
                            updated_at=note_timestamp,
                            is_demo_data=True,
                        )
                    )
                    counts["nurse_notes"] += 1

            for assessment_number in range(2):
                assessment_type = ASSESSMENT_TYPES[
                    (index + assessment_number) % len(ASSESSMENT_TYPES)
                ]
                assessment_day = current_date - timedelta(
                    days=(index * 3 + assessment_number * 11) % 60
                )
                db.session.add(
                    PatientAssessment(
                        patient_id=patient.id,
                        visit_id=patient_visits[assessment_number].id
                        if assessment_number == 0
                        else None,
                        assessment_type=assessment_type,
                        assessment_date=assessment_day,
                        performed_by=NURSE_NAMES[index % len(NURSE_NAMES)],
                        summary=f"Fictional {assessment_type.replace('_', ' ')} review.",
                        findings={
                            "risk_level": ("moderate" if index % 3 else "high"),
                            "score": 4 + (index + assessment_number) % 7,
                            "demo": True,
                        },
                        recommendations=(
                            "Continue care plan, reinforce safety education, "
                            "and reassess at the next scheduled visit."
                        ),
                        status="completed" if assessment_number == 0 else "draft",
                        is_demo_data=True,
                    )
                )
                counts["assessments"] += 1

            patient_name = f"{first_name} {last_name}"
            pdf = _pdf_bytes(patient_name)
            object_key = f"demo/patients/{patient.id}/care-summary.pdf"
            storage.upload(
                object_key,
                BytesIO(pdf),
                len(pdf),
                "application/pdf",
            )
            uploaded_keys.append(object_key)
            uploaded_at = datetime.combine(
                current_date - timedelta(days=index % 30),
                time(10, 0),
                tzinfo=UTC,
            )
            db.session.add(
                MedicalRecord(
                    patient_id=patient.id,
                    title="Demo care plan summary",
                    description=(
                        "Generated fictional document for SeniorMate demos only."
                    ),
                    record_type="care_plan",
                    file_name="demo-care-summary.pdf",
                    file_mime_type="application/pdf",
                    file_size=len(pdf),
                    storage_bucket=storage.bucket,
                    storage_object_key=object_key,
                    uploaded_by="Demo Data Seeder",
                    uploaded_at=uploaded_at,
                    is_demo_data=True,
                )
            )
            counts["medical_records"] += 1

        db.session.commit()
    except Exception:
        db.session.rollback()
        for object_key in uploaded_keys:
            storage.delete(object_key)
        raise

    return counts


def _format_counts(prefix, counts):
    summary = ", ".join(
        f"{value} {name.replace('_', ' ')}" for name, value in counts.items()
    )
    return f"{prefix}: {summary}."


def register_demo_commands(app):
    @app.cli.command("seed-demo")
    def seed_demo_command():
        """Replace existing demo records with a fresh deterministic dataset."""
        _require_demo_enabled()
        try:
            counts = seed_demo_records()
        except PrivateObjectStorageError as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(_format_counts("Demo data seeded", counts))

    @app.cli.command("clear-demo")
    def clear_demo_command():
        """Delete only records explicitly marked as demo data."""
        _require_demo_enabled()
        try:
            counts = clear_demo_records()
        except PrivateObjectStorageError as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(_format_counts("Demo data cleared", counts))
