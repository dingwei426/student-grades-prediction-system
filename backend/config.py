import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

class Config:
    DEBUG = True
    # Database URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    
    # Optional: If you have other configurations like Track Modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    
    # Secret Key for session management
    SECRET_KEY = os.getenv('SECRET_KEY')    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)  # Token expires in 30 minutes
    
    # Mail configuration (for email features)
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT', "587")  # Default to 587 if not specified
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'  # Convert to boolean
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "dingwei0426@gmail.com")  # Default sender!
    
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
    REDIS = os.getenv('REDIS', 'localhost')