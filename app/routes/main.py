from flask import Blueprint, render_template
from app.models import Patient, Visit
from app import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    total_patients = db.session.query(Patient).count()
    total_visits = db.session.query(Visit).count()
    recent_visits = (
        Visit.query.order_by(Visit.visit_date.desc().nullslast())
        .limit(5)
        .all()
    )

    return render_template(
        "index.html",
        total_patients=total_patients,
        total_visits=total_visits,
        recent_visits=recent_visits,
    )
