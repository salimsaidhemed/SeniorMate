from flask import Blueprint, jsonify, request
from app import db
from app.models import Visit, VisitAssessment
from datetime import datetime

api = Blueprint("api_visits", __name__, url_prefix="/api/visits")

@api.route("/<int:patient_id>", methods=["GET"])
def get_visits(patient_id):
    visits = Visit.query.filter_by(patient_id=patient_id).order_by(Visit.visit_date.desc()).all()
    return jsonify([{
        "id": v.id,
        "visit_date": v.visit_date.strftime("%Y-%m-%d"),
        "visit_type": v.visit_type,
        "narrative": v.narrative
    } for v in visits])

@api.route("/add", methods=["POST"])
def add_visit():
    data = request.json
    visit = Visit(
        patient_id=data["patient_id"],
        visit_date=datetime.strptime(data["visit_date"], "%Y-%m-%d").date(),
        visit_type=data["visit_type"],
        narrative=data.get("narrative", ""),
        created_by=data.get("created_by", "system")
    )
    db.session.add(visit)
    db.session.commit()
    return jsonify({"message": "Visit added", "visit_id": visit.id}), 201

@api.route("/<int:visit_id>/assessments", methods=["GET"])
def get_assessments(visit_id):
    assessments = VisitAssessment.query.filter_by(visit_id=visit_id).all()
    return jsonify([
        {
            "id": a.id,
            # "aide_id": a.aide_id,
            "created_at": a.created_at.strftime("%Y-%m-%d %H:%M"),
            "personal_care": a.personal_care,
            "notes": a.notes
        } for a in assessments
    ])

@api.route("/<int:visit_id>/assessments/add", methods=["POST"])
def add_assessment(visit_id):
    data = request.json
    assessment = VisitAssessment(
        visit_id=visit_id,
        # aide_id=data["aide_id"],
        personal_care=data.get("personal_care", {}),
        nutrition=data.get("nutrition", {}),
        mental_status=data.get("mental_status", {}),
        elimination=data.get("elimination", {}),
        activity=data.get("activity", {}),
        assistive_device=data.get("assistive_device", {}),
        house_keeping=data.get("house_keeping", {}),
        notes=data.get("notes"),
        signature=data.get("signature"),
        time_in=data.get("time_in"),
        time_out=data.get("time_out"),
    )
    db.session.add(assessment)
    db.session.commit()
    return jsonify({"message": "Assessment added", "assessment_id": assessment.id}), 201

