from app import db

class Default_Field(db.Model):
    __tablename__ = 'default_field'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
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

    def __repr__(self):
        return f"<Default_Field {self.id} for user {self.user_id}>"
