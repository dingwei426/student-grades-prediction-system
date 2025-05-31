from app import db
from app.models import Prediction, Subject
from sqlalchemy import func

def get_most_used_model():
    total = db.session.query(func.count(Prediction.id)).scalar()

    result = (
        db.session.query(
            Prediction.model_used,
            func.count(Prediction.model_used).label("model_count")
        )
        .group_by(Prediction.model_used)
        .order_by(func.count(Prediction.model_used).desc())
        .first()
    )

    if result:
        model, count = result
        return {
            "model": model,
            "count": count,
            "percentage": round((count / total) * 100, 2) if total else 0
        }

    return None


def get_primary_language_distribution():
    total = db.session.query(func.count(Prediction.id)).scalar()
    result = db.session.query(
        Prediction.primary_language, func.count(Prediction.primary_language)
    ).group_by(Prediction.primary_language).order_by(func.count(Prediction.primary_language).desc()).first()

    if result:
        language, count = result
        return {
            "language": language,
            "count": count,
            "percentage": round((count / total) * 100, 2) if total else 0
        }

    return None


def get_average_revision_time():
    result = db.session.query(
        func.avg(Prediction.average_studying_hour)
    ).scalar()

    return round(result, 2) if result else 0


def get_cgpa_comparison():
    results = db.session.query(
        Prediction.name,
        Prediction.cgpa,
        Prediction.predicted_cgpa
    ).all()

    return [
        {
            "name": name,
            "actual_cgpa": round(actual, 2) if actual else 0,
            "predicted_cgpa": round(predicted, 2) if predicted else 0
        }
        for name, actual, predicted in results
    ]


def get_subject_grade_distribution(subject_name):
    results = db.session.query(
        Subject.grade, func.count(Subject.grade)
    ).filter(
        Subject.is_prediction == True,
        Subject.name == subject_name
    ).group_by(Subject.grade).all()

    return [
        {"grade": grade, "count": count}
        for grade, count in results
    ]


def get_qualification_type_distribution():
    total = db.session.query(func.count(Prediction.id)).scalar()
    result = (
        db.session.query(
            Prediction.qualification,
            func.count(Prediction.id).label("count")
        )
        .group_by(Prediction.qualification).order_by(func.count(Prediction.qualification).desc()).first()
    )

    if result:
        qualification, count = result
        return {
            "qualification": qualification,
            "count": count,
            "percentage": round((count / total) * 100, 2) if total else 0
        }

    return None