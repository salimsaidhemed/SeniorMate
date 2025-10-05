from .main import main_bp
from .patients import patient_bp
from .visits import bp as visits_bp
from .api_visits import api
from .assessments import assessment_bp


blueprints = [main_bp, patient_bp, visits_bp,api,assessment_bp]
