from app import db
from datetime import datetime
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    # created_at = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Relationship to Input (one-to-many)
    inputs = db.relationship('Prediction', backref='user', lazy=True)
    default_field = db.relationship('Default_Field', uselist=False, backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'
