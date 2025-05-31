from app import db
from datetime import datetime
from sqlalchemy import Text
class Prediction(db.Model):
    __tablename__ = 'prediction'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    yob = db.Column(db.Integer)
    primary_language = db.Column(db.String(50))
    english_proficiency = db.Column(db.Integer)
    year_trimester = db.Column(db.String(50))
    secondary_school_location = db.Column(db.String(100))
    science_stream = db.Column(db.Boolean)
    qualification = db.Column(db.String(100))
    qualification_grades = db.Column(db.String(50))
    assignment_working_frequency = db.Column(db.String(50))
    computer_interest = db.Column(db.Integer)
    average_studying_hour = db.Column(db.Float)
    cgpa = db.Column(db.Float)
    selected_subjects = db.Column(Text)  # Comma-separated list of selected subjects. Example: awad|se|project|......
    model_used = db.Column(db.String(50))  # Ex: lgbm_4, lgbm_9, rf_4, rf_9
    predicted_cgpa = db.Column(db.Float)
    suggestion = db.Column(Text) 
    
    # Relationship to SelectedSubject (one-to-many)
    subjects = db.relationship('Subject', backref='prediction', passive_deletes=True)
    
    def __repr__(self):
        return f"<Prediction {self.id} for user {self.user_id}>"
