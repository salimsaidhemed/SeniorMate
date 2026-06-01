from datetime import UTC, date, datetime

from flasgger import swag_from
from flask import Blueprint
from sqlalchemy import func

from app.extensions import db
from app.models import AideNote, NurseNote, Patient, Visit
from app.swagger import dashboard_stats_spec


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")


def success_response(data, message, status_code=200):
    return {"data": data, "message": message}, status_code


def month_bounds(today=None):
    current = today or datetime.now(UTC).date()
    start = date(current.year, current.month, 1)

    if current.month == 12:
        end = date(current.year + 1, 1, 1)
    else:
        end = date(current.year, current.month + 1, 1)

    return start, end


def start_of_day(day):
    return datetime.combine(day, datetime.min.time(), tzinfo=UTC)


def grouped_counts(model, field, default_label="Not specified"):
    rows = (
        db.session.query(field, func.count(model.id))
        .group_by(field)
        .order_by(func.count(model.id).desc(), field.asc())
        .all()
    )

    return [
        {
            "label": label or default_label,
            "count": count,
        }
        for label, count in rows
    ]


def recent_visit_payload(visit):
    patient_name = None

    if visit.patient:
        patient_name = f"{visit.patient.first_name} {visit.patient.last_name}"

    return {
        "id": visit.id,
        "patient_name": patient_name,
        "visit_date": visit.visit_date.isoformat() if visit.visit_date else None,
        "visit_type": visit.visit_type,
        "staff_role": visit.staff_role,
        "status": visit.status,
    }


@dashboard_bp.get("/dashboard/stats")
@swag_from(dashboard_stats_spec)
def get_dashboard_stats():
    start_of_month, start_of_next_month = month_bounds()

    recent_visits = (
        Visit.query.order_by(Visit.visit_date.desc(), Visit.id.desc()).limit(5).all()
    )

    data = {
        "total_patients": Patient.query.count(),
        "active_patients": Patient.query.filter_by(status="active").count(),
        "inactive_patients": Patient.query.filter_by(status="inactive").count(),
        "total_visits": Visit.query.count(),
        "visits_this_month": Visit.query.filter(
            Visit.visit_date >= start_of_month,
            Visit.visit_date < start_of_next_month,
        ).count(),
        "aide_notes_this_month": AideNote.query.filter(
            AideNote.created_at >= start_of_day(start_of_month),
            AideNote.created_at < start_of_day(start_of_next_month),
        ).count(),
        "nurse_notes_this_month": NurseNote.query.filter(
            NurseNote.created_at >= start_of_day(start_of_month),
            NurseNote.created_at < start_of_day(start_of_next_month),
        ).count(),
        "patients_by_status": grouped_counts(Patient, Patient.status),
        "patients_by_gender": grouped_counts(Patient, Patient.gender),
        "visits_by_type": grouped_counts(Visit, Visit.visit_type),
        "visits_by_status": grouped_counts(Visit, Visit.status),
        "recent_visits": [recent_visit_payload(visit) for visit in recent_visits],
    }

    return success_response(data, "Dashboard stats retrieved successfully")
