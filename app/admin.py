from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import db
from app.models import Patient, Visit, VitalSigns, BPMeasurement, PulseResp, Assessment, Signature

def init_admin(app):
    admin = Admin(app, name="SeniorMate Admin", template_mode="bootstrap4")
    
     # Register models
    admin.add_view(SecureModelView(Patient, db.session))
    admin.add_view(ModelView(Visit, db.session))
    admin.add_view(ModelView(VitalSigns, db.session))
    admin.add_view(ModelView(BPMeasurement, db.session))
    admin.add_view(ModelView(PulseResp, db.session))
    admin.add_view(ModelView(Assessment, db.session))
    admin.add_view(ModelView(Signature, db.session))

    return admin

class SecureModelView(ModelView):
    can_create = True
    can_edit = True
    can_delete = False   # prevent accidental deletes
    page_size = 25       # pagination
    column_display_pk = True

