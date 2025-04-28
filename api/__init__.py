# Import all API routes/blueprints here
from app import app
from flask import Blueprint

# Create API blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
internships_bp = Blueprint('internships', __name__, url_prefix='/api/internships')
tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')
supervisor_bp = Blueprint('supervisor', __name__, url_prefix='/api/supervisor')

# Import routes
from . import auth, internships, tasks, supervisor
