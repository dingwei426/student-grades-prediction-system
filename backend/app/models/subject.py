from app import db

class Subject(db.Model):
    __tablename__ = 'subject'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(
        db.Integer,
        db.ForeignKey('prediction.id', ondelete='CASCADE'),
        nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_prediction = db.Column(db.Boolean, default=False)
    grade = db.Column(db.String(5))  # For example: letter grade or numeric value
    
    def __repr__(self):
        return f"<SelectedSubject Input:{self.prediction_id} Subject:{self.subject_id}>"
