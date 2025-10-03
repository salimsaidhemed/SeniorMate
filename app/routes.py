from flask import Blueprint, jsonify
# from app.oidc import oidc

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    return {"msg": "Daycare App Running"}

# @bp.route("/private")
# @oidc.oidc_auth("default")
# def private():
#     user = oidc.current_user
#     return jsonify({
#         "email": user.userinfo.get("email"),
#         "name": user.userinfo.get("name")
#     })
