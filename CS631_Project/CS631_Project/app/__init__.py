from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration for PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cs631_user:cs631@localhost:5432/cs631_personnel_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a strong secret in production
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models here so Alembic can detect them
    from . import models
    
    # Import and register blueprints
    from .views import main_bp
    from .api_hr import hr_bp
    from .api_project import project_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(hr_bp, url_prefix='/api/hr')
    app.register_blueprint(project_bp, url_prefix='/api/project')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .cli import register_commands
    register_commands(app)

    return app