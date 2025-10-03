from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Patient
from datetime import datetime

patient_bp = Blueprint("patients", __name__, url_prefix="/patients")

@patient_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    pagination = Patient.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "patients/index.html",
        patients=pagination.items,
        pagination=pagination
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
