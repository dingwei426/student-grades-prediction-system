from .auth_routes import auth_bp
from .prediction_routes import prediction_bp
from .ai_routes import ai_bp
from .dashboard_routes import dashboard_bp

# If you have more route files in the future, import them here
# Example:
# from .student_routes import student_bp
# from .admin_routes import admin_bp

# Define a list of blueprints for easier registration in `app.py`
blueprints = [auth_bp, prediction_bp, ai_bp, dashboard_bp]
