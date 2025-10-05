from flask import Blueprint, render_template, request, redirect, url_for, flash,send_file
from app import db
from app.models import Patient
from datetime import datetime
import csv
import io


patient_bp = Blueprint("patients", __name__, url_prefix="/patients")

from sqlalchemy import func
from app.models import Patient, Visit

@patient_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search = request.args.get("search", "", type=str)

    # Build base query
    query = db.session.query(
        Patient,
        func.count(Visit.id).label("visit_count")
    ).outerjoin(Visit).group_by(Patient.id)

    if search:
        query = query.filter(
            (Patient.name.ilike(f"%{search}%")) |
            (Patient.mr_number.ilike(f"%{search}%")) |
            (Patient.gender.ilike(f"%{search}%"))
        )

    pagination = query.order_by(Patient.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Adjust context to pass tuples (Patient, visit_count)
    patients = [
        {"data": patient, "visit_count": visit_count}
        for patient, visit_count in pagination.items
    ]

    print(patients[0])

    return render_template(
        "patients/index.html",
        pagination=pagination,
        patients=patients,
        search=search
    )


@patient_bp.route("/add", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form.get("name")
        mr_number = request.form.get("mr_number")
        gender = request.form.get("gender")
        dob = request.form.get("dob")

        if not name or not mr_number:
            flash("Name and MR# are required", "danger")
            return redirect(url_for("patients.add_patient"))

        # Ensure MR# is unique
        if Patient.query.filter_by(mr_number=mr_number).first():
            flash("MR# already exists, please use a unique ID", "danger")
            return redirect(url_for("patients.add_patient"))

        patient = Patient(
            name=name,
            mr_number=mr_number,
            gender=gender,
            dob=datetime.strptime(dob, "%Y-%m-%d") if dob else None
        )
        

        db.session.add(patient)
        db.session.commit()
        flash("Patient added successfully", "success")
        return redirect(url_for("patients.index"))

    return render_template("patients/add.html")

# Edit Patient
@patient_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        mr_number = request.form.get("mr_number")
        gender = request.form.get("gender")
        dob = request.form.get("dob")

        if not name or not mr_number:
            flash("Name and MR# are required", "danger")
            return redirect(url_for("patients.edit_patient", id=id))

        # Unique MR# validation (exclude current patient)
        existing = Patient.query.filter(Patient.mr_number == mr_number, Patient.id != id).first()
        if existing:
            flash("MR# already exists for another patient", "danger")
            return redirect(url_for("patients.edit_patient", id=id))

        patient.name = name
        patient.mr_number = mr_number
        patient.gender = gender
        patient.dob = datetime.strptime(dob, "%Y-%m-%d") if dob else None

        db.session.commit()
        flash("✏️ Patient updated successfully!", "success")
        return redirect(url_for("patients.index"))

    return render_template("patients/edit.html", patient=patient)


# Delete Patient
@patient_bp.route("/delete/<int:id>", methods=["POST"])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash("🗑️ Patient deleted successfully!", "success")
    return redirect(url_for("patients.index"))

@patient_bp.route("/import", methods=["GET", "POST"])
def import_patients():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("Please upload a CSV file.", "danger")
            return redirect(url_for("patients.import_patients"))

        try:
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(stream)

            required_fields = {"name", "mr_number"}
            if not required_fields.issubset(reader.fieldnames):
                flash("CSV must include 'name' and 'mr_number' columns.", "danger")
                return redirect(url_for("patients.import_patients"))

            added, skipped = 0, 0
            for row in reader:
                name = row.get("name")
                mr_number = row.get("mr_number")
                gender = row.get("gender")
                dob = row.get("dob")

                if not name or not mr_number:
                    skipped += 1
                    continue

                # Ensure MR# is unique
                if Patient.query.filter_by(mr_number=mr_number).first():
                    skipped += 1
                    continue

                patient = Patient(
                    name=name.strip(),
                    mr_number=mr_number.strip(),
                    gender=gender.strip() if gender else None,
                    dob=datetime.strptime(dob, "%Y-%m-%d") if dob else None
                )
                db.session.add(patient)
                added += 1

            db.session.commit()
            flash(f"✅ Import complete: {added} added, {skipped} skipped.", "success")
        except Exception as e:
            flash(f"❌ Import failed: {str(e)}", "danger")

        return redirect(url_for("patients.index"))

    return render_template("patients/import.html")

@patient_bp.route("/export")
def export_csv():
    si = io.StringIO()
    writer = csv.writer(si)

    writer.writerow(["name", "mr_number", "gender", "dob", "created_at"])
    for patient in Patient.query.all():
        writer.writerow([
            patient.name,
            patient.mr_number,
            patient.gender or "",
            patient.dob or "",
            patient.created_at.strftime("%Y-%m-%d %H:%M")
        ])

    output = io.BytesIO()
    output.write(si.getvalue().encode("utf-8"))
    output.seek(0)
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="patients_export.csv"
    )