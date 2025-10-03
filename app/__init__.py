from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

     # Import models so Alembic sees them
    from app import models
  

   

    # # Setup OIDC + Admin
    # from app.oidc import oidc
    # oidc.init_app(app)

    from app.admin import init_admin
    init_admin(app)

    from app.routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
