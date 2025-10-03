from flask import Blueprint, jsonify,render_template
from app import db
from app.models import Patient, Visit
# from app.oidc import oidc

bp = Blueprint("routes", __name__)

@bp.route("/")
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
    

# @bp.route("/private")
# @oidc.oidc_auth("default")
# def private():
#     user = oidc.current_user
#     return jsonify({
#         "email": user.userinfo.get("email"),
#         "name": user.userinfo.get("name")
#     })
