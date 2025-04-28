import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # Needed for url_for to generate with https

# Configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
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

# Initialize the app with extensions
db.init_app(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models.models import User
    return User.query.get(int(user_id))

# Import routes and models
with app.app_context():
    from api import auth, internships, tasks, supervisor
    from models.models import User, UserProfile, Industry, InternshipTrack, Task, Submission, Certificate, AdminUser, Company
    
    # Create tables
    db.create_all()

    # Initialize data if needed
    from api.init_data import initialize_data
    initialize_data()