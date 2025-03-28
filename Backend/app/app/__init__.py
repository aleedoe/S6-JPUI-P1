from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models import *
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Load config
    app.config.from_object(Config)

    migrate = Migrate(app, db)

    # Import blueprint    
    from app.routes import register_blueprint_user
    register_blueprint_user(app)
    
    from app.routes import register_blueprint_attendance
    register_blueprint_attendance(app)
    
    from app.routes import register_blueprint_student
    register_blueprint_student(app)

    # Inisialisasi database
    db.init_app(app)

    return app