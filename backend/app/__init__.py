from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate  # Import Flask-Migrate
from flask_jwt_extended import JWTManager
from config import Config
from dotenv import load_dotenv
import logging
import redis
from flask_session import Session  # Add this import

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()
migrate = Migrate()
sess = Session()

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Initialize Redis for Flask-Session
    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_KEY_PREFIX"] = "session:"
    
    # Setup Redis Connection
    app.config["SESSION_REDIS"] = redis.StrictRedis(
        host="localhost",  # Use "redis" if using Docker
        port=6379,
        db=0,
        decode_responses=True
    )
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    sess.init_app(app)

    # Register blueprints
    from app.routes import blueprints  # Import blueprints from routes/__init__.py
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
