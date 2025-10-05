from flask import render_template, Blueprint
from sqlalchemy import text
from app import db

assessment_bp = Blueprint("assessment_bp", __name__, url_prefix="/assessments")

@assessment_bp.route("/<int:assessment_id>/report")
def assessment_report(assessment_id):
    # --- Flatten JSON sections ---
    section_sql = text("""
    SELECT a.visit_id, 'Personal Care' AS section, j.key, j.value
    FROM visit_assessments AS a, json_each(a.personal_care) AS j WHERE a.id = :assessment_id

    UNION ALL
    SELECT a.visit_id, 'Nutrition' AS section, j.key, j.value
    FROM visit_assessments AS a, json_each(a.nutrition) AS j WHERE a.id = :assessment_id

    UNION ALL
    SELECT a.visit_id, 'Mental Status' AS section, j.key, j.value
    FROM visit_assessments AS a, json_each(a.mental_status) AS j WHERE a.id = :assessment_id

    UNION ALL
    SELECT a.visit_id, 'Elimination' AS section, j.key, j.value
    FROM visit_assessments AS a, json_each(a.elimination) AS j WHERE a.id = :assessment_id

    UNION ALL
    SELECT a.visit_id, 'Activity' AS section, j.key, j.value
    FROM visit_assessments AS a, json_each(a.activity) AS j WHERE a.id = :assessment_id

    UNION ALL
    SELECT a.visit_id, 'Assistive Device' AS section, j.key, j.value
    FROM visit_assessments AS a, json_each(a.assistive_device) AS j WHERE a.id = :assessment_id

    UNION ALL
    SELECT a.visit_id, 'House Keeping' AS section, j.key, j.value
    FROM visit_assessments AS a, json_each(a.house_keeping) AS j WHERE a.id = :assessment_id
    """)

    rows = db.session.execute(section_sql, {"assessment_id": assessment_id}).fetchall()
    sections = {}
    for row in rows:
        sections.setdefault(row.section, []).append({
            "key": row.key,
            "value": row.value
        })

    # --- Metadata ---
    meta_sql = text("""
    SELECT 
        va.visit_id,
        va.created_at,
        va.updated_at,
        va.notes,
        v.patient_id,
        (SELECT name FROM patients WHERE id = v.patient_id) AS patient_name,
        (SELECT mr_number FROM patients WHERE id = v.patient_id) AS mr_number,
        v.visit_date,
        v.visit_type,
        v.narrative
    FROM visit_assessments va
    INNER JOIN visits v ON va.visit_id = v.id
    WHERE va.id = :assessment_id
    """)

    meta = db.session.execute(meta_sql, {"assessment_id": assessment_id}).fetchone()

    if not meta:
        flash("Assessment not found.", "warning")
        return redirect(url_for("patient_bp.index"))

    return render_template(
        "assessments/report.html",
        assessment_id=assessment_id,
        sections=sections,
        meta=meta
    )

@assessment_bp.route("/<int:visit_id>/report/pdf")
def assessment_report_pdf(visit_id):
    html = assessment_report(visit_id).data.decode("utf-8")  # reuse rendered HTML
    pdf = HTML(string=html).write_pdf()
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"inline; filename=assessment_{visit_id}.pdf"},
    )
