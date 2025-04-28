import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database base class
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Azure OpenAI configuration
app.config["AZURE_OPENAI_ENDPOINT"] = os.environ.get("AZURE_OPENAI_ENDPOINT", "https://thepromptocrats-hackathon-stg-openai-uaen-01.openai.azure.com/")
app.config["AZURE_OPENAI_KEY"] = os.environ.get("AZURE_OPENAI_KEY")
app.config["AZURE_OPENAI_DEPLOYMENT"] = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
app.config["AZURE_OPENAI_API_VERSION"] = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")

# Standard OpenAI configuration (fallback)
app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
app.config["OPENAI_MODEL"] = os.environ.get("OPENAI_MODEL", "gpt-4o")

# Azure Cosmos DB configuration
app.config["COSMOS_ENDPOINT"] = os.environ.get("COSMOS_ENDPOINT")
app.config["COSMOS_KEY"] = os.environ.get("COSMOS_KEY")
app.config["COSMOS_DATABASE"] = os.environ.get("COSMOS_DATABASE", "internship-simulator")

# Azure AI Search configuration
app.config["AZURE_SEARCH_ENDPOINT"] = os.environ.get("AZURE_SEARCH_ENDPOINT")
app.config["AZURE_SEARCH_KEY"] = os.environ.get("AZURE_SEARCH_KEY")
app.config["AZURE_SEARCH_INDEX"] = os.environ.get("AZURE_SEARCH_INDEX", "internship-resources")

# Azure Function configuration
app.config["AZURE_FUNCTION_ENDPOINT"] = os.environ.get("AZURE_FUNCTION_ENDPOINT")
app.config["AZURE_FUNCTION_KEY"] = os.environ.get("AZURE_FUNCTION_KEY")

# Initialize extensions
db.init_app(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models.models import User
    return User.query.get(int(user_id))

# Import and register API Blueprints
from api.auth import bp as auth_bp
from api.internships import bp as internships_bp
from api.tasks import bp as tasks_bp
from api.supervisor import bp as supervisor_bp

app.register_blueprint(auth_bp)
app.register_blueprint(internships_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(supervisor_bp)

# Startup data initialization
with app.app_context():
    try:
        from models.models import User, UserProfile, Industry, InternshipTrack, Task, Submission, Certificate, AdminUser, Company
        db.create_all()

        from api.init_data import initialize_data
        initialize_data()

        logging.info("Database and initial data setup completed successfully.")
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        logging.warning("Backend started without full database initialization.")
