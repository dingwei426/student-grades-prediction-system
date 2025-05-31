import os
import joblib
import pandas as pd
import numpy as np
from app import db
from datetime import datetime
from app.models import Prediction, Subject, Default_Field
from sklearn.impute import KNNImputer
from sqlalchemy.orm import joinedload
import math

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script directory

model_subjects = ['advanced-database', 'ai', 'algo', 'awad', 'cloud-computing', 'coa', 'cybersecurity', 'database', 'design',
                  'dip', 'dm', 'ethics', 'game-engines', 'hcid', 'multimedia', 'network-application', 'network-security', 'ooad', 'os',
                  'parallel-processing', 'prob', 'programming', 'project', 'requirements', 'scc', 'scm', 'se', 'spm', 'sqa',
                  'tcpip-fundamentals', 'tcpip-routing', 'team-project', 'testing', 'wad', 'wireless']

model_subjects_name_mapping = [
    "ADVANCED DATABASE SYSTEMS",                 # advanced-database
    "ARTIFICIAL INTELLIGENCE",                   # ai
    "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS",  # algo
    "ADVANCED WEB APPLICATION DEVELOPMENT",       # awad
    "CLOUD COMPUTING",                            # cloud-computing
    "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",  # coa
    "FUNDAMENTALS OF CYBERSECURITY",              # cybersecurity
    "DATABASE SYSTEM FUNDAMENTALS",               # database
    "SOFTWARE DESIGN",                            # design
    "DIGITAL IMAGE PROCESSING",                   # dip
    "DATA MINING",                                # dm
    "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",  # ethics
    "PROGRAMMING WITH GAME ENGINES",              # game-engines
    "HUMAN COMPUTER INTERACTION DESIGN",          # hcid
    "MULTIMEDIA TECHNOLOGY",                      # multimedia
    "TCP/IP NETWORK APPLICATION DEVELOPMENT",     # network-application
    "NETWORK SECURITY MANAGEMENT",                # network-security
    "OBJECT-ORIENTED APPLICATION DEVELOPMENT",    # ooad
    "OPERATING SYSTEMS",                          # os
    "PARALLEL PROCESSING",                        # parallel-processing
    "PROBABILITY AND STATISTICS FOR COMPUTING",   # prob
    "PROGRAMMING AND PROBLEM SOLVING",            # programming
    "PROJECT",                                     # project
    "SOFTWARE AND REQUIREMENTS",                  # requirements
    "SOFTWARE CONSTRUCTION AND CONFIGURATION",    # scc
    "SERVER CONFIGURATION AND MANAGEMENT",        # scm
    "SOFTWARE ENTREPRENEURSHIP",                  # se
    "SOFTWARE PROJECT MANAGEMENT",                # spm
    "SOFTWARE QUALITY ASSURANCE",                 # sqa
    "TCP/IP NETWORK FUNDAMENTALS",                # tcpip-fundamentals
    "TCP/IP NETWORK ROUTING",                     # tcpip-routing
    "TEAM PROJECT",                               # team-project
    "SOFTWARE TESTING",                           # testing
    "WEB APPLICATION DEVELOPMENT",                # wad
    "WIRELESS APPLICATION DEVELOPMENT"            # wireless
]

subject_cols = ["PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS",
    "TCP/IP NETWORK FUNDAMENTALS", "PROBABILITY AND STATISTICS FOR COMPUTING",
    "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "DATABASE SYSTEM FUNDAMENTALS",
    "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE", "HUMAN COMPUTER INTERACTION DESIGN",
    "OPERATING SYSTEMS", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS",
    "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY", "WEB APPLICATION DEVELOPMENT",
    "SOFTWARE DESIGN", "SOFTWARE TESTING", "SOFTWARE PROJECT MANAGEMENT",
    "SOFTWARE CONSTRUCTION AND CONFIGURATION", "WIRELESS APPLICATION DEVELOPMENT",
    "ADVANCED WEB APPLICATION DEVELOPMENT", "SOFTWARE QUALITY ASSURANCE",
    "SOFTWARE ENTREPRENEURSHIP", "PROJECT"]

academic_keys = [
    "CGPA", "Average Studying Hours per Week",
    "PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS",
    "TCP/IP NETWORK FUNDAMENTALS", "PROBABILITY AND STATISTICS FOR COMPUTING",
    "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "DATABASE SYSTEM FUNDAMENTALS",
    "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE", "HUMAN COMPUTER INTERACTION DESIGN",
    "OPERATING SYSTEMS", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS",
    "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY", "WEB APPLICATION DEVELOPMENT",
    "SOFTWARE DESIGN", "SOFTWARE TESTING", "SOFTWARE PROJECT MANAGEMENT",
    "SOFTWARE CONSTRUCTION AND CONFIGURATION", "WIRELESS APPLICATION DEVELOPMENT",
    "ADVANCED WEB APPLICATION DEVELOPMENT", "SOFTWARE QUALITY ASSURANCE",
    "SOFTWARE ENTREPRENEURSHIP", "PROJECT"
]


def get_default_field_by_user_id(user_id):
    if not user_id:
        raise ValueError("User ID is required.")

    default_field = Default_Field.query.filter_by(user_id=user_id).first()
    if not default_field:
        return None

    return {
        "id": default_field.id,
        "user_id": default_field.user_id,
        "gender": default_field.gender,
        "yob": default_field.yob,
        "primary_language": default_field.primary_language,
        "english_proficiency": default_field.english_proficiency,
        "year_trimester": default_field.year_trimester,
        "secondary_school_location": default_field.secondary_school_location,
        "science_stream": default_field.science_stream,
        "qualification": default_field.qualification,
        "qualification_grades": default_field.qualification_grades,
        "assignment_working_frequency": default_field.assignment_working_frequency,
        "computer_interest": default_field.computer_interest,
        "average_studying_hour": default_field.average_studying_hour,
        "cgpa": default_field.cgpa,
    }    

def set_default_field(form_data, user_id):
    # Define the exact set of keys expected in the form_data payload.
    expected_keys = {
        "gender",
        "yob",
        "primary_language",
        "english_proficiency",
        "year_trimester",
        "secondary_school_location",
        "science_stream",
        "qualification",
        "qualification_grades",
        "assignment_working_frequency",
        "computer_interest",
        "average_studying_hour",
        "cgpa"
    }

    if not user_id:
        raise ValueError("User ID is required to set default fields.")

    # Clean the form_data: ignore keys with value as None or NaN.
    cleaned_data = {}
    for key, value in form_data.items():
        # Skip keys not in expected_keys (optional)
        if key not in expected_keys:
            continue
        if value is None:
            continue
        if isinstance(value, (int, float)) and math.isnan(value):
            continue
        cleaned_data[key] = value

    # Check if a Default_Field record already exists for this user.
    existing_record = Default_Field.query.filter_by(user_id=user_id).first()
    if existing_record:
        # Update the existing record with new valid values from cleaned_data.
        for key, value in cleaned_data.items():
            setattr(existing_record, key, value)
        db.session.commit()
        return existing_record.id  # Return the ID of the updated record

    # Create a new Default_Field record using the cleaned data.
    new_record = Default_Field(**cleaned_data, user_id=user_id)
    db.session.add(new_record)
    db.session.commit()
    return new_record.id  # Return the ID of the newly created record

def process_data(form_data, model_type):
    # Only keep academic data for imputation
    academic_cleaned_data = {k: (np.nan if v == "" else v) for k, v in form_data.items() if k in academic_keys}

    # Load training data
    # df_dir = os.path.join(script_dir, "dataset", "training-data-1000-4classes.csv")  # Construct the absolute path
    df_dir = os.path.join(script_dir, "dataset", "training-data-1000-4classes.csv")  # Construct the absolute path
    df = pd.read_csv(df_dir)

    if(model_type == "lgbm_4" or model_type == "rf_4"):
        grade_map = {
            "A+": 3, "A": 3, "A-": 3,
            "B+": 2, "B": 2, "B-": 2,
            "C+": 1, "C": 1,
            "F": 0
        }
    else:
        grade_map = {
            "A+": 8, "A": 7, "A-": 6,
            "B+": 5, "B": 4, "B-": 3,
            "C+": 2, "C": 1,
            "F": 0
        }

    # Select only academic columns from training data
    df = df[academic_keys]

    # Apply grade mapping
    df.replace(grade_map, inplace=True)
    df = df.infer_objects(copy=False)

    # Convert input data to DataFrame and apply same mapping
    input_df = pd.DataFrame([academic_cleaned_data])
    input_df.replace(grade_map, inplace=True)
    input_df = input_df.infer_objects(copy=False)

    # Combine training and input data for imputation
    combined_df = pd.concat([df, input_df], ignore_index=True)

    # Perform KNN imputation
    imputer = KNNImputer(n_neighbors=5)
    imputed_array = imputer.fit_transform(combined_df)

    # Get the imputed input row
    imputed_row = imputed_array[-1]
    imputed_df = pd.DataFrame([imputed_row], columns=combined_df.columns)

    # Round imputed grades (exclude CGPA, study hours if present)
    for col in imputed_df.columns:
        if col not in ["CGPA", "Average Studying Hours per Week"]:
            imputed_df[col] = round(imputed_df[col])

    return imputed_df

def save_prediction_to_db(form_data, predictions, cgpa, model_type, selected_subjects, input_subjects, user_id):
    selected_subjects = selected_subjects or []
    
    existing_count = Prediction.query.filter_by(user_id=user_id).count()
    prediction_name = f"Prediction {existing_count + 1}"
    
    # Create a joined string for saving in the prediction record.
    # This variable is only used to store the string value in the record.
    if len(selected_subjects) > 0:
        selected_subjects_str = "|".join(selected_subjects)
    else:
        selected_subjects_str = ""
        
    prediction_record = Prediction(
        user_id=user_id,
        date=datetime.now(),
        name=prediction_name,
        gender=form_data.get('gender'),
        yob=form_data.get('yob'),
        primary_language=form_data.get('primary_language'),
        english_proficiency=form_data.get('english_proficiency'),
        year_trimester=form_data.get('year_trimester'),
        secondary_school_location=form_data.get('secondary_school_location'),
        science_stream=form_data.get('science_stream'),
        qualification=form_data.get('qualification'),
        qualification_grades=form_data.get('qualification_grades'),
        assignment_working_frequency=form_data.get('assignment_working_frequency'),
        computer_interest=form_data.get('computer_interest'),
        average_studying_hour=form_data.get("Average Studying Hours per Week"),
        cgpa=form_data.get("CGPA"),
        selected_subjects=selected_subjects_str,  # store the joined string here
        model_used=model_type,  # Specify the model used for prediction
        predicted_cgpa=float(cgpa),
    )

    db.session.add(prediction_record)
    db.session.flush()  # to obtain prediction_record.id for the following loops

    # Track already saved subject names to prevent duplication
    saved_subject_names = set()

    # Save input subjects
    for subject in input_subjects:
        try:
            subject_grade = str(form_data[subject])
        except KeyError:
            subject_grade = ""
        subject_obj = Subject(
            prediction_id=prediction_record.id,
            name=subject,
            is_prediction=False,
            grade=subject_grade
        )
        db.session.add(subject_obj)
        saved_subject_names.add(subject)  # Record the saved subject name

    # Grade mapping based on model type
    if model_type in {"lgbm_4", "rf_4"}:
        grade_map = {
            0: "F",
            1: "C",
            2: "B",
            3: "A"
        }
    else:
        grade_map = {
            0: "F",
            1: "C",
            2: "C+",
            3: "B-",
            4: "B",
            5: "B+",
            6: "A-",
            7: "A",
            8: "A+"
        }

    # Save predicted subjects only if they weren't saved above
    for subject, grade in predictions.items():
        if subject in saved_subject_names:
            continue  # Skip if already saved as input subject
        letter_grade = grade_map.get(grade, "F")
        subject_obj = Subject(
            prediction_id=prediction_record.id,
            name=subject,
            is_prediction=True,
            grade=letter_grade
        )
        db.session.add(subject_obj)
        
    db.session.commit()
    return prediction_record.id

def generate_prediction(form_data, user_id, model_type, selected_subjects):
    features = ["SOFTWARE AND REQUIREMENTS", "TCP/IP NETWORK FUNDAMENTALS", "PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", 
            "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE", "SOFTWARE DESIGN", "WEB APPLICATION DEVELOPMENT", 
            "OPERATING SYSTEMS", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS", "PROJECT"]
    
    input_subjects = [col for col in model_subjects_name_mapping if col in form_data]
    
    predictions = {}
    input_data = process_data(form_data, model_type)
    
    cgpa_model_dir = os.path.join(script_dir, "predictive-models", "cgpa_model.pkl")  # Construct the absolute path
    cgpa_model = joblib.load(cgpa_model_dir)
    input_for_model = input_data[features]
    cgpa = cgpa_model.predict(input_for_model)
    
    if(model_type == "lgbm_4" or model_type == "lgbm_9"):
        input_data.columns = [col.replace(" ", "_") for col in input_data.columns]

    # Predict each target subject
    for subject in model_subjects:
        model_dir = os.path.join(script_dir, "predictive-models", model_type, (subject+".pkl"))  # Construct the absolute path

        try:
            model = joblib.load(model_dir)
        except FileNotFoundError:
            print(f"⚠️ Model not found for subject: {subject}")
            continue

        expected_features = model.feature_names_in_
        input_for_model = input_data[expected_features]

        pred = model.predict(input_for_model)
        predictions[model_subjects_name_mapping[model_subjects.index(subject)]] = int(pred[0])
    
    prediction_id = save_prediction_to_db(form_data, predictions, cgpa, model_type, selected_subjects, input_subjects, user_id)
    return prediction_id

def get_prediction_list_user_id(user_id):
    # Query predictions with their associated subjects
    predictions = (
        Prediction.query
        .filter_by(user_id=user_id)
        .order_by(Prediction.date.desc())
        .all()
    )

    result = []
    for prediction in predictions:
        pred_data = {
            "prediction_id": prediction.id,
            "date": prediction.date.strftime("%Y-%m-%d %H:%M:%S"),
            "name": prediction.name,
            "predicted_cgpa": prediction.predicted_cgpa,
            "model_used": prediction.model_used,
            "predicted_cgpa": prediction.predicted_cgpa,
        }

        result.append(pred_data)

    return result

def get_prediction_by_id(prediction_id):
    # Fetch the prediction with its related subjects using eager loading
    prediction = (
        Prediction.query
        .options(joinedload(Prediction.subjects))
        .filter_by(id=prediction_id)
        .first()
    )

    if not prediction:
        return None  # Or raise an error / return an appropriate message

    pred_data = {
        "prediction_id": prediction.id,
        "date": prediction.date.strftime("%Y-%m-%d %H:%M:%S"),
        "name": prediction.name,
        "gender": prediction.gender,
        "yob": prediction.yob,
        "primary_language": prediction.primary_language,
        "english_proficiency": prediction.english_proficiency,
        "year_trimester": prediction.year_trimester,
        "secondary_school_location": prediction.secondary_school_location,
        "science_stream": prediction.science_stream,
        "qualification": prediction.qualification,
        "qualification_grades": prediction.qualification_grades,
        "assignment_working_frequency": prediction.assignment_working_frequency,
        "cgpa": prediction.cgpa,
        "computer_interest": prediction.computer_interest,
        "predicted_cgpa": prediction.predicted_cgpa,
        "average_studying_hour": prediction.average_studying_hour,
        "selected_subjects": prediction.selected_subjects.split("|") if prediction.selected_subjects else [],
        "model_used": prediction.model_used,
        "subjects": []
    }

    for subject in prediction.subjects:
        pred_data["subjects"].append({
            "name": subject.name,
            "grade": subject.grade,
            "is_prediction": subject.is_prediction
        })

    return pred_data

def update_prediction_name_service(prediction_id, new_name):
    if not new_name:
        return {"message": "New name is required."}, 400

    prediction = Prediction.query.get(prediction_id)
    if not prediction:
        return {"message": "Prediction not found."}, 404

    prediction.name = new_name
    db.session.commit()

    return {"message": "Prediction name updated successfully.", "new_name": new_name}, 200

def delete_prediction_service(prediction_id):
    prediction = Prediction.query.get(prediction_id)
    if not prediction:
        return {"message": "Prediction not found."}, 404

    db.session.delete(prediction)
    db.session.commit()

    return {"message": "Prediction deleted successfully."}, 200