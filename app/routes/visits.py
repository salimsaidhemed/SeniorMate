from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Visit, Patient
from datetime import date,datetime

bp = Blueprint("visits", __name__, url_prefix="/visits")

@bp.route("/<int:patient_id>")
def list_visits(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    visits = Visit.query.filter_by(patient_id=patient_id).order_by(Visit.visit_date.desc()).all()
    return render_template("visits/index.html", patient=patient, visits=visits)

@bp.route("/add/<int:patient_id>", methods=["GET", "POST"])
def add_visit(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        visit_date_str = request.form.get("visit_date")
        if visit_date_str:
            visit_date = datetime.strptime(visit_date_str, "%Y-%m-%d").date()
        else:
            visit_date = date.today()

        visit = Visit(
            patient_id=patient.id,
            visit_date=visit_date,
            visit_type=request.form.get("visit_type"),
            narrative=request.form.get("narrative"),
        )
        db.session.add(visit)
        db.session.commit()
        flash("Visit added successfully", "success")
        return redirect(url_for("visits.list_visits", patient_id=patient.id))
    return render_template("visits/add.html", patient=patient,date=date)

@bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_visit(id):
    visit = Visit.query.get_or_404(id)
    if request.method == "POST":
        visit.visit_date = request.form.get("visit_date") or visit.visit_date
        visit.visit_type = request.form.get("visit_type")
        visit.narrative = request.form.get("narrative")
        db.session.commit()
        flash("Visit updated successfully", "success")
        return redirect(url_for("visits.list_visits", patient_id=visit.patient_id))
    return render_template("visits/edit.html", visit=visit,date=date)

@bp.route("/delete/<int:id>", methods=["POST"])
def delete_visit(id):
    visit = Visit.query.get_or_404(id)
    patient_id = visit.patient_id
    db.session.delete(visit)
    db.session.commit()
    flash("Visit deleted successfully", "info")
    return redirect(url_for("visits.list_visits", patient_id=patient_id))

@bp.route("/patient/<int:patient_id>/details")
def visit_details(patient_id):
    """
    Displays the master-detail view for a patient's visits and assessments.
    """
    patient = Patient.query.get_or_404(patient_id)
    return render_template("visits/master_detail.html", patient=patient)
