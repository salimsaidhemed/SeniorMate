import os


basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              f"sqlite:///{os.path.join(basedir, 'senior_mate.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OIDC / Keycloak
    OIDC_CLIENT_SECRETS = os.getenv("OIDC_CLIENT_SECRETS", "client_secrets.json")
    OIDC_SCOPES = ["openid", "profile", "email"]
    OIDC_INTROSPECTION_AUTH_METHOD = "client_secret_post"
