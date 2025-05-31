# import numpy as np
# import pandas as pd
# import random
# from sklearn.impute import KNNImputer
# from sklearn.preprocessing import MinMaxScaler

# # Define all features (Demographic + Core Subjects + Additional Subjects)
# features = [
#     # Demographic attributes (Categorical)
#     "Gender", "Most Comfortable Language", "Location of Secondary School",
#     "Science Stream", "Type of Qualification Completed", "Grades Obtained in Qualification",
#     "Frequency of Working with Classmates", "Academic Year and Trimester",

#     # Numeric attributes
#     "Year of Birth", "English Proficiency", "Interest in Studying Computer",
#     "Average Studying Hours per Week", "CGPA",

#     # Core subjects (Correlated using Pearson)
#     "PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS",
#     "TCP/IP NETWORK FUNDAMENTALS", "PROBABILITY AND STATISTICS FOR COMPUTING",
#     "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "DATABASE SYSTEM FUNDAMENTALS",
#     "WEB APPLICATION DEVELOPMENT", "SOFTWARE DESIGN", "SOFTWARE TESTING",
#     "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",
#     "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",
#     "HUMAN COMPUTER INTERACTION DESIGN", "OPERATING SYSTEMS",
#     "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"
# ]

# categorical_columns = [
#     "Gender", "Most Comfortable Language", "Location of Secondary School",
#     "Science Stream", "Type of Qualification Completed", "Grades Obtained in Qualification",
#     "Frequency of Working with Classmates", "Academic Year and Trimester"]

# numeric_columns = ["Year of Birth", "English Proficiency", "Interest in Studying Computer", "Average Studying Hours per Week"]

# core_subjects = [
#     "PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS",
#     "TCP/IP NETWORK FUNDAMENTALS", "PROBABILITY AND STATISTICS FOR COMPUTING",
#     "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "DATABASE SYSTEM FUNDAMENTALS",
#     "WEB APPLICATION DEVELOPMENT", "SOFTWARE DESIGN", "SOFTWARE TESTING",
#     "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",
#     "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",
#     "HUMAN COMPUTER INTERACTION DESIGN", "OPERATING SYSTEMS",
#     "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"
# ]

# # Additional subjects (Rule-Based Sampling)
# additional_subjects = [
#     "SOFTWARE PROJECT MANAGEMENT", "SOFTWARE CONSTRUCTION AND CONFIGURATION",
#     "WIRELESS APPLICATION DEVELOPMENT", "ADVANCED WEB APPLICATION DEVELOPMENT",
#     "SOFTWARE QUALITY ASSURANCE", "SOFTWARE ENTREPRENEURSHIP", "PROJECT",
#     "MULTIMEDIA TECHNOLOGY", "ARTIFICIAL INTELLIGENCE", "TEAM PROJECT",
#     "PROGRAMMING WITH GAME ENGINES", "ADVANCED DATABASE SYSTEMS", "CLOUD COMPUTING",
#     "DIGITAL IMAGE PROCESSING", "FUNDAMENTALS OF CYBERSECURITY", "PARALLEL PROCESSING", "DATA MINING",
#     "TCP/IP NETWORK ROUTING", "SERVER CONFIGURATION AND MANAGEMENT",
#     "TCP/IP NETWORK APPLICATION DEVELOPMENT", "NETWORK SECURITY MANAGEMENT"
# ]

# # Load dataset
# df_real = pd.read_csv("data/data-1.2.csv")[features]

# # Save original categorical mappings for restoring later
# category_mappings = {}
# for col in categorical_columns:
#     df_real[col] = df_real[col].astype('category')
#     category_mappings[col] = dict(enumerate(df_real[col].cat.categories))  # Store mapping
#     df_real[col] = df_real[col].cat.codes  # Convert to numerical codes

# # Convert grades to numerical values
# grade_mapping = {'A+': 8, 'A': 7, 'A-': 6, 'B+': 5, 'B': 4, 'B-': 3, 'C+': 2, 'C': 1, 'F': 0}
# df_real.replace(grade_mapping, inplace=True)

# # Handle missing values using KNN Imputation
# imputer = KNNImputer(n_neighbors=5)
# df_real_imputed = pd.DataFrame(imputer.fit_transform(df_real), columns=df_real.columns)

# # Compute Pearson Correlation Matrix for core subjects
# corr_matrix = df_real_imputed.corr()

# # Compute Covariance Matrix
# std_devs = df_real_imputed.std().values  
# cov_matrix = np.outer(std_devs, std_devs) * corr_matrix  

# # Generate Synthetic Data Using Multivariate Normal Sampling for Core Subjects
# num_students = 1000
# mean = df_real_imputed.mean().values  # Use mean values from real data
# synthetic_numeric = np.random.multivariate_normal(mean, cov_matrix, size=num_students)

# # Convert synthetic data back to categorical and numeric values
# synthetic_data = pd.DataFrame(synthetic_numeric, columns=features)

# # --- Apply Quantile Binning for Core Subjects to Ensure Full Grade Range ---
# # We only want this for grade-based subjects; here, we assume core subjects are grade-based.
# grade_labels = ['F', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']

# for col in core_subjects:
#     try:
#         # Use qcut to create 9 quantile bins ensuring each grade is represented
#         synthetic_data[col] = pd.qcut(synthetic_data[col], q=len(grade_labels), labels=grade_labels)
#     except ValueError:
#         # If qcut fails due to insufficient unique values, default to 'C'
#         synthetic_data[col] = 'C'
        
# # Convert categorical features back to their original categories
# for col in categorical_columns:
#     unique_values = category_mappings[col]
#     synthetic_data[col] = synthetic_data[col].round().clip(0, len(unique_values) - 1).astype(int)
#     synthetic_data[col] = synthetic_data[col].map(unique_values)

# # Convert numeric grades back to letter grades for core subjects
# # reverse_grade_mapping = {v: k for k, v in grade_mapping.items()}
# # for col in features:
# #     if col in grade_mapping.values():
# #         synthetic_data[col] = synthetic_data[col].round().clip(0, 8).map(reverse_grade_mapping)

# synthetic_data[numeric_columns] = synthetic_data[numeric_columns].round().astype(int)

# scaler = MinMaxScaler(feature_range=(1999, 2005))
# synthetic_data["Year of Birth"] = scaler.fit_transform(synthetic_data[["Year of Birth"]])
# synthetic_data["Year of Birth"] = synthetic_data["Year of Birth"].round(0).astype(int)

# # ---- ADDITIONAL SUBJECTS: RULE-BASED SAMPLING ----
# additional_subjects_map = {
#     "SOFTWARE PROJECT MANAGEMENT": ["SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
#     "SOFTWARE CONSTRUCTION AND CONFIGURATION": ["PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
#     "WIRELESS APPLICATION DEVELOPMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
#     "ADVANCED WEB APPLICATION DEVELOPMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
#     "SOFTWARE QUALITY ASSURANCE": ["SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
#     "SOFTWARE ENTREPRENEURSHIP": ["SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
#     "PROJECT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS", "SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "SOFTWARE TESTING"],
#     "MULTIMEDIA TECHNOLOGY": ["SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
#     "ARTIFICIAL INTELLIGENCE": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
#     "TEAM PROJECT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
#     "PROGRAMMING WITH GAME ENGINES": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "WEB APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
#     "ADVANCED DATABASE SYSTEMS": ["DATABASE SYSTEM FUNDAMENTALS", "PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
#     "CLOUD COMPUTING": ["DATABASE SYSTEM FUNDAMENTALS", "PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT"],
#     "DIGITAL IMAGE PROCESSING": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "WEB APPLICATION DEVELOPMENT"],
#     "FUNDAMENTALS OF CYBERSECURITY": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
#     "PARALLEL PROCESSING": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT",  "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
#     "DATA MINING": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT",  "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
#     "TCP/IP NETWORK ROUTING": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
#     "SERVER CONFIGURATION AND MANAGEMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
#     "TCP/IP NETWORK APPLICATION DEVELOPMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
#     "NETWORK SECURITY MANAGEMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
# }

# grade_probability = {
#     "A+": {"A+": 0.55, "A": 0.25, "A-": 0.12, "B+": 0.05, "B": 0.02, "B-": 0.01, "C+": 0.00, "C": 0.00, "F": 0.00},
#     "A":  {"A+": 0.30, "A": 0.35, "A-": 0.18, "B+": 0.10, "B": 0.05, "B-": 0.02, "C+": 0.00, "C": 0.00, "F": 0.00},
#     "A-": {"A+": 0.15, "A": 0.30, "A-": 0.25, "B+": 0.18, "B": 0.07, "B-": 0.03, "C+": 0.02, "C": 0.00, "F": 0.00},
#     "B+": {"A+": 0.05, "A": 0.12, "A-": 0.18, "B+": 0.30, "B": 0.22, "B-": 0.08, "C+": 0.03, "C": 0.02, "F": 0.00},
#     "B":  {"A+": 0.02, "A": 0.05, "A-": 0.12, "B+": 0.22, "B": 0.35, "B-": 0.15, "C+": 0.07, "C": 0.02, "F": 0.00},
#     "B-": {"A+": 0.00, "A": 0.02, "A-": 0.05, "B+": 0.12, "B": 0.25, "B-": 0.28, "C+": 0.15, "C": 0.10, "F": 0.03},
#     "C+": {"A+": 0.00, "A": 0.00, "A-": 0.02, "B+": 0.05, "B": 0.10, "B-": 0.20, "C+": 0.30, "C": 0.20, "F": 0.08},
#     "C":  {"A+": 0.00, "A": 0.00, "A-": 0.00, "B+": 0.02, "B": 0.07, "B-": 0.15, "C+": 0.28, "C": 0.35, "F": 0.13},
#     "F":  {"A+": 0.00, "A": 0.00, "A-": 0.00, "B+": 0.01, "B": 0.03, "B-": 0.08, "C+": 0.15, "C": 0.30, "F": 0.43}
# }

# def assign_additional_subject(influencing_grades):
#     """
#     Assigns an additional subject's grade based on multiple core subjects' grades.
#     The probabilities are averaged across influencing subjects.
#     """
#     aggregate_probs = {grade: 0 for grade in grade_probability["A+"]}
    
#     for grade in influencing_grades:
#         for key in grade_probability[grade]:
#             aggregate_probs[key] += grade_probability[grade][key]
    
#     # Normalize probabilities
#     total = len(influencing_grades)
#     for key in aggregate_probs:
#         aggregate_probs[key] /= total
    
#     # Perform weighted random sampling
#     return random.choices(list(aggregate_probs.keys()), weights=list(aggregate_probs.values()))[0]

# # Generate additional subject grades
# for subject, base_subjects in additional_subjects_map.items():
#     synthetic_data[subject] = synthetic_data.apply(lambda row: assign_additional_subject(
#         [row[subj] for subj in base_subjects]
#     ), axis=1)
    
# # Calculate CGPA based on all subject grades using credit hours and a GPA mapping
# # Define credit hours for each subject (example values)
# credit_hours = {
#     "PROGRAMMING AND PROBLEM SOLVING": 4,
#     "SOFTWARE AND REQUIREMENTS": 3,
#     "TCP/IP NETWORK FUNDAMENTALS": 3,
#     "PROBABILITY AND STATISTICS FOR COMPUTING": 3,
#     "OBJECT-ORIENTED APPLICATION DEVELOPMENT": 4,
#     "DATABASE SYSTEM FUNDAMENTALS": 3,
#     "WEB APPLICATION DEVELOPMENT": 4,
#     "SOFTWARE DESIGN": 4,
#     "SOFTWARE TESTING": 4,
#     "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY": 3,
#     "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE": 3,
#     "HUMAN COMPUTER INTERACTION DESIGN": 3,
#     "OPERATING SYSTEMS": 3,
#     "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS": 3,
#     "SOFTWARE PROJECT MANAGEMENT": 3,
#     "SOFTWARE CONSTRUCTION AND CONFIGURATION": 3,
#     "WIRELESS APPLICATION DEVELOPMENT": 3,
#     "ADVANCED WEB APPLICATION DEVELOPMENT": 4,
#     "SOFTWARE QUALITY ASSURANCE": 3,
#     "SOFTWARE ENTREPRENEURSHIP": 3,
#     "PROJECT": 9,
#     "MULTIMEDIA TECHNOLOGY": 3,
#     "ARTIFICIAL INTELLIGENCE": 3,
#     "TEAM PROJECT": 3,
#     "PROGRAMMING WITH GAME ENGINES": 3,
#     "ADVANCED DATABASE SYSTEMS": 3,
#     "CLOUD COMPUTING": 3,
#     "DIGITAL IMAGE PROCESSING": 3,
#     "FUNDAMENTALS OF CYBERSECURITY": 3,
#     "PARALLEL PROCESSING": 3,
#     "DATA MINING": 3,
#     "TCP/IP NETWORK ROUTING": 3,
#     "SERVER CONFIGURATION AND MANAGEMENT": 3,
#     "TCP/IP NETWORK APPLICATION DEVELOPMENT": 3,
#     "NETWORK SECURITY MANAGEMENT": 3
# }

# # Define GPA mapping for CGPA calculation (on a 4.0 scale)
# gpa_mapping = {
#     "A+": 4.0,
#     "A": 4.0,
#     "A-": 3.67,
#     "B+": 3.33,
#     "B": 3.0,
#     "B-": 2.67,
#     "C+": 2.33,
#     "C": 2.0,
#     "F": 0.0
# }

# def calculate_cgpa(row, subjects, credit_hours, gpa_mapping):
#     total_points = 0.0
#     total_credits = 0.0
#     for subj in subjects:
#         grade = row[subj]
#         if grade in gpa_mapping:
#             total_points += gpa_mapping[grade] * credit_hours[subj]
#             total_credits += credit_hours[subj]
#     return round(total_points / total_credits, 4) if total_credits != 0 else 0.0

# # Calculate CGPA based on all subjects (core + additional)
# all_subjects_list = core_subjects + additional_subjects
# synthetic_data["CGPA"] = synthetic_data.apply(lambda row: calculate_cgpa(row, all_subjects_list, credit_hours, gpa_mapping), axis=1)

# # Save the synthetic dataset
# synthetic_data.to_csv("training-data-1000.csv", index=False)

# print("✅ Synthetic dataset generated successfully with covariance for core subjects and rule-based sampling for additional subjects!")

# import numpy as np
# import pandas as pd
# import random
# from sklearn.impute import KNNImputer
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Core subjects (generated using Pearson correlation)
# core_subjects = [
#     "PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS",
#     "TCP/IP NETWORK FUNDAMENTALS", "PROBABILITY AND STATISTICS FOR COMPUTING",
#     "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "DATABASE SYSTEM FUNDAMENTALS",
#     "WEB APPLICATION DEVELOPMENT", "SOFTWARE DESIGN", "SOFTWARE TESTING",
#     "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",
#     "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",
#     "HUMAN COMPUTER INTERACTION DESIGN", "OPERATING SYSTEMS",
#     "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"
# ]

# # Additional subjects (dependent on a base subject)
# additional_subjects = ["SOFTWARE PROJECT MANAGEMENT",
#     "SOFTWARE CONSTRUCTION AND CONFIGURATION", "WIRELESS APPLICATION DEVELOPMENT",
#     "ADVANCED WEB APPLICATION DEVELOPMENT", "SOFTWARE QUALITY ASSURANCE",
#     "SOFTWARE ENTREPRENEURSHIP", "PROJECT", "MULTIMEDIA TECHNOLOGY",
#     "ARTIFICIAL INTELLIGENCE", "TEAM PROJECT", "PROGRAMMING WITH GAME ENGINES",
#     "ADVANCED DATABASE SYSTEMS", "CLOUD COMPUTING", "DIGITAL IMAGE PROCESSING",
#     "FUNDAMENTALS OF CYBERSECURITY", "DATA MINING",
#     "TCP/IP NETWORK ROUTING", "SERVER CONFIGURATION AND MANAGEMENT",
#     "TCP/IP NETWORK APPLICATION DEVELOPMENT", "NETWORK SECURITY MANAGEMENT"
# ]

# # Define conditional probability mappings (base subject: "PROGRAMMING AND PROBLEM SOLVING")
# conditional_grade_probabilities = {
#     "A+": {"A+": 0.50, "A": 0.25, "A-": 0.15, "B+": 0.07, "B": 0.03, "B-": 0.00, "C+": 0.00, "C": 0.00, "F": 0.00},
#     "A":  {"A+": 0.30, "A": 0.30, "A-": 0.20, "B+": 0.10, "B": 0.05, "B-": 0.03, "C+": 0.02, "C": 0.00, "F": 0.00},
#     "A-": {"A+": 0.20, "A": 0.30, "A-": 0.20, "B+": 0.15, "B": 0.10, "B-": 0.03, "C+": 0.02, "C": 0.00, "F": 0.00},
#     "B+": {"A+": 0.05, "A": 0.10, "A-": 0.20, "B+": 0.25, "B": 0.20, "B-": 0.10, "C+": 0.05, "C": 0.05, "F": 0.00},
#     "B":  {"A+": 0.00, "A": 0.05, "A-": 0.10, "B+": 0.20, "B": 0.25, "B-": 0.15, "C+": 0.15, "C": 0.10, "F": 0.00},
#     "B-": {"A+": 0.00, "A": 0.00, "A-": 0.05, "B+": 0.10, "B": 0.20, "B-": 0.25, "C+": 0.20, "C": 0.15, "F": 0.05},
#     "C+": {"A+": 0.00, "A": 0.00, "A-": 0.00, "B+": 0.05, "B": 0.10, "B-": 0.20, "C+": 0.25, "C": 0.25, "F": 0.15},
#     "C":  {"A+": 0.00, "A": 0.00, "A-": 0.00, "B+": 0.00, "B": 0.05, "B-": 0.10, "C+": 0.20, "C": 0.30, "F": 0.35},
#     "F":  {"A+": 0.00, "A": 0.00, "A-": 0.00, "B+": 0.00, "B": 0.00, "B-": 0.05, "C+": 0.15, "C": 0.30, "F": 0.50}
# }

# # Load real data and extract core subjects
# df_subjects = pd.read_csv("data/data-1.2.csv")[core_subjects]
# print(df_subjects.isnull().sum())

# # Convert grades to numeric values
# grade_mapping = {'A+': 8, 'A': 7, 'A-': 6, 'B+': 5, 'B': 4, 'B-': 3, 'C+': 2, 'C': 1, 'F': 0}
# df_numeric = df_subjects.map(lambda x: grade_mapping.get(x, None))

# # Apply KNN Imputer to handle missing values
# imputer = KNNImputer(n_neighbors=5)
# df_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_subjects.columns)

# # Convert back to letter grades
# reverse_mapping = {v: k for k, v in grade_mapping.items()}
# df_subjects = df_imputed.map(lambda x: reverse_mapping.get(round(x), 'C'))

# # Compute Pearson correlation matrix
# df_encoded = df_subjects.copy()
# for col in df_encoded.columns:
#     df_encoded[col] = df_encoded[col].astype('category').cat.codes  # Convert to numerical codes
# corr_matrix = df_encoded.corr(method='pearson')

# # Ensure covariance matrix is positive semi-definite
# def nearest_positive_definite(matrix):
#     """Ensure the covariance matrix is positive semi-definite for multivariate sampling."""
#     eigvals, eigvecs = np.linalg.eigh(matrix)
#     eigvals = np.maximum(eigvals, 1e-6)
#     return eigvecs @ np.diag(eigvals) @ eigvecs.T

# # Compute covariance matrix
# std_devs = df_encoded.std().values  
# cov_matrix = np.outer(std_devs, std_devs) * corr_matrix  
# cov_matrix = nearest_positive_definite(cov_matrix)  

# # Generate Synthetic Data for Core Subjects Using Multivariate Normal Sampling
# num_students = 1000
# mean = [4] * len(core_subjects)  # Assume B (4.0) as mean grade
# synthetic_numeric = np.random.multivariate_normal(mean, cov_matrix, size=num_students)

# # Convert numeric scores to grades
# synthetic_data = []
# for i in range(num_students):
#     student = {}
    
#     # Assign core subjects based on correlation
#     for j, subject in enumerate(core_subjects):
#         numeric_grade = np.clip(round(synthetic_numeric[i, j]), 0, 8)  
#         student[subject] = reverse_mapping.get(numeric_grade, 'C')

#     # Assign additional subjects based on base subject grade (PROGRAMMING AND PROBLEM SOLVING)
#     base_subject_grade = student["PROGRAMMING AND PROBLEM SOLVING"]
#     base_distribution = conditional_grade_probabilities[base_subject_grade]
#     for subject in additional_subjects:
#         student[subject] = random.choices(list(base_distribution.keys()), weights=list(base_distribution.values()))[0]

#     synthetic_data.append(student)

# # Convert to DataFrame
# synthetic_df = pd.DataFrame(synthetic_data)

# # Save to CSV
# synthetic_df.to_csv("synthetic_student_grades_combined.csv", index=False)

# print("Synthetic dataset generated successfully with core subjects using correlation and additional subjects based on base subject grades!")
#-----------------------------------------------------------------------------------------------------
# import numpy as np
# import pandas as pd
# from sklearn.impute import KNNImputer

# # Define all features (Demographic + Core Subjects + Additional Subjects)
# features = [
#     # Demographic attributes (Categorical)
#     "Gender", "Most Comfortable Language", "Location of Secondary School",
#     "Science Stream", "Type of Qualification Completed", "Grades Obtained in Qualification",
#     "Frequency of Working with Classmates", "Academic Year and Trimester",

#     # Numeric attributes
#     "Year of Birth", "English Proficiency", "Interest in Studying Computer",
#     "Average Studying Hours per Week", "CGPA",

#     # Core subjects (Correlated using Pearson)
#     "PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS",
#     "TCP/IP NETWORK FUNDAMENTALS", "PROBABILITY AND STATISTICS FOR COMPUTING",
#     "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "DATABASE SYSTEM FUNDAMENTALS",
#     "WEB APPLICATION DEVELOPMENT", "SOFTWARE DESIGN", "SOFTWARE TESTING",
#     "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",
#     "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",
#     "HUMAN COMPUTER INTERACTION DESIGN", "OPERATING SYSTEMS",
#     "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS",

#     # Additional subjects (Previously based on rule-based, now included in correlation)
#     "SOFTWARE PROJECT MANAGEMENT", "SOFTWARE CONSTRUCTION AND CONFIGURATION",
#     "WIRELESS APPLICATION DEVELOPMENT", "ADVANCED WEB APPLICATION DEVELOPMENT",
#     "SOFTWARE QUALITY ASSURANCE", "SOFTWARE ENTREPRENEURSHIP", "PROJECT",
#     "MULTIMEDIA TECHNOLOGY", "ARTIFICIAL INTELLIGENCE", "TEAM PROJECT",
#     "PROGRAMMING WITH GAME ENGINES", "ADVANCED DATABASE SYSTEMS", "CLOUD COMPUTING",
#     "DIGITAL IMAGE PROCESSING", "FUNDAMENTALS OF CYBERSECURITY", "DATA MINING",
#     "TCP/IP NETWORK ROUTING", "SERVER CONFIGURATION AND MANAGEMENT",
#     "TCP/IP NETWORK APPLICATION DEVELOPMENT", "NETWORK SECURITY MANAGEMENT"
# ]

# subject_columns = [
#     "PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS",
#     "TCP/IP NETWORK FUNDAMENTALS", "PROBABILITY AND STATISTICS FOR COMPUTING",
#     "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "DATABASE SYSTEM FUNDAMENTALS",
#     "WEB APPLICATION DEVELOPMENT", "SOFTWARE DESIGN", "SOFTWARE TESTING",
#     "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",
#     "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",
#     "HUMAN COMPUTER INTERACTION DESIGN", "OPERATING SYSTEMS",
#     "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS",
#     "SOFTWARE PROJECT MANAGEMENT", "SOFTWARE CONSTRUCTION AND CONFIGURATION",
#     "WIRELESS APPLICATION DEVELOPMENT", "ADVANCED WEB APPLICATION DEVELOPMENT",
#     "SOFTWARE QUALITY ASSURANCE", "SOFTWARE ENTREPRENEURSHIP", "PROJECT",
#     "MULTIMEDIA TECHNOLOGY", "ARTIFICIAL INTELLIGENCE", "TEAM PROJECT",
#     "PROGRAMMING WITH GAME ENGINES", "ADVANCED DATABASE SYSTEMS", "CLOUD COMPUTING",
#     "DIGITAL IMAGE PROCESSING", "FUNDAMENTALS OF CYBERSECURITY", "DATA MINING",
#     "TCP/IP NETWORK ROUTING", "SERVER CONFIGURATION AND MANAGEMENT",
#     "TCP/IP NETWORK APPLICATION DEVELOPMENT", "NETWORK SECURITY MANAGEMENT"
# ]

# # Load dataset
# df_real = pd.read_csv("data/data-1.2.csv")[features]

# # Convert categorical variables to numerical
# categorical_columns = df_real.select_dtypes(include=['object']).columns
# for col in categorical_columns:
#     df_real[col] = df_real[col].astype('category').cat.codes

# # Convert grades to numerical values
# grade_mapping = {'A+': 8, 'A': 7, 'A-': 6, 'B+': 5, 'B': 4, 'B-': 3, 'C+': 2, 'C': 1, 'F': 0}
# df_real.replace(grade_mapping, inplace=True)

# # Handle missing values using KNN Imputation
# imputer = KNNImputer(n_neighbors=5)
# df_real_imputed = pd.DataFrame(imputer.fit_transform(df_real), columns=df_real.columns)

# # Compute Pearson Correlation Matrix
# corr_matrix = df_real_imputed.corr()

# # Fix covariance matrix using nearest positive definite function
# def nearest_positive_definite(matrix):
#     """Ensure the covariance matrix is positive semi-definite for multivariate sampling."""
#     eigvals, eigvecs = np.linalg.eigh(matrix)
#     eigvals = np.maximum(eigvals, 1e-6)
#     return eigvecs @ np.diag(eigvals) @ eigvecs.T

# # Compute Covariance Matrix
# std_devs = df_real_imputed.std().values  
# cov_matrix = np.outer(std_devs, std_devs) * corr_matrix  
# cov_matrix = nearest_positive_definite(cov_matrix)  # Fix non-positive definite issue

# # Generate Synthetic Data Using Multivariate Normal Sampling
# num_students = 1000
# mean = df_real_imputed.mean().values  # Use mean values from real data
# synthetic_numeric = np.random.multivariate_normal(mean, cov_matrix, size=num_students)

# # Convert synthetic data back to categorical and numeric values
# synthetic_data = pd.DataFrame(synthetic_numeric, columns=features)

# # Convert numerical features back to categorical
# for col in categorical_columns:
#     unique_values = df_real[col].astype('category').cat.categories
#     synthetic_data[col] = synthetic_data[col].round().clip(0, len(unique_values) - 1).astype(int)
#     synthetic_data[col] = synthetic_data[col].map(lambda x: unique_values[x])

# # Convert numeric grades back to letter grades
# reverse_grade_mapping = {v: k for k, v in grade_mapping.items()}
# for col in subject_columns:
#     if col in synthetic_data.columns:
#         synthetic_data[col] = synthetic_data[col].round().clip(0, 8).map(reverse_grade_mapping)
        
# # Save the synthetic dataset
# synthetic_data.to_csv("synthetic_student_data_full.csv", index=False)

# print("✅ Synthetic dataset generated successfully using full correlation and covariance!")
#-----------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import random
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler

# Define all features (Demographic + Core Subjects + Additional Subjects)
features = [
    # Demographic attributes (Categorical)
    "Gender", "Most Comfortable Language", "Location of Secondary School",
    "Science Stream", "Type of Qualification Completed", "Grades Obtained in Qualification",
    "Frequency of Working with Classmates", "Academic Year and Trimester",

    # Numeric attributes
    "Year of Birth", "English Proficiency", "Interest in Studying Computer",
    "Average Studying Hours per Week", "CGPA",

    # Core subjects (Correlated using Pearson)
    "PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS",
    "TCP/IP NETWORK FUNDAMENTALS", "PROBABILITY AND STATISTICS FOR COMPUTING",
    "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "DATABASE SYSTEM FUNDAMENTALS",
    "WEB APPLICATION DEVELOPMENT", "SOFTWARE DESIGN", "SOFTWARE TESTING",
    "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",
    "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",
    "HUMAN COMPUTER INTERACTION DESIGN", "OPERATING SYSTEMS",
    "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"
]

# Additional subjects (Rule-Based Sampling)
additional_subjects = [
    "SOFTWARE PROJECT MANAGEMENT", "SOFTWARE CONSTRUCTION AND CONFIGURATION",
    "WIRELESS APPLICATION DEVELOPMENT", "ADVANCED WEB APPLICATION DEVELOPMENT",
    "SOFTWARE QUALITY ASSURANCE", "SOFTWARE ENTREPRENEURSHIP", "PROJECT",
    "MULTIMEDIA TECHNOLOGY", "ARTIFICIAL INTELLIGENCE", "TEAM PROJECT",
    "PROGRAMMING WITH GAME ENGINES", "ADVANCED DATABASE SYSTEMS", "CLOUD COMPUTING",
    "DIGITAL IMAGE PROCESSING", "FUNDAMENTALS OF CYBERSECURITY", "PARALLEL PROCESSING", "DATA MINING",
    "TCP/IP NETWORK ROUTING", "SERVER CONFIGURATION AND MANAGEMENT",
    "TCP/IP NETWORK APPLICATION DEVELOPMENT", "NETWORK SECURITY MANAGEMENT"
]

# Load dataset
df_real = pd.read_csv("real-data.csv")[features]

# Save original categorical mappings for restoring later
categorical_columns = df_real.select_dtypes(include=['object']).columns
category_mappings = {}

# Convert categorical variables to numerical
for col in categorical_columns:
    df_real[col] = df_real[col].astype('category')
    category_mappings[col] = dict(enumerate(df_real[col].cat.categories))  # Store mapping
    df_real[col] = df_real[col].cat.codes  # Convert to numerical codes

# Convert grades to numerical values
grade_mapping = {'A+': 8, 'A': 7, 'A-': 6, 'B+': 5, 'B': 4, 'B-': 3, 'C+': 2, 'C': 1, 'F': 0}
df_real.replace(grade_mapping, inplace=True)

# Handle missing values using KNN Imputation
imputer = KNNImputer(n_neighbors=5)
df_real_imputed = pd.DataFrame(imputer.fit_transform(df_real), columns=df_real.columns)

# Compute Pearson Correlation Matrix for core subjects
corr_matrix = df_real_imputed.corr()

# Compute Covariance Matrix
std_devs = df_real_imputed.std().values  
cov_matrix = np.outer(std_devs, std_devs) * corr_matrix  

# Generate Synthetic Data Using Multivariate Normal Sampling for Core Subjects
num_students = 1000
mean = df_real_imputed.mean().values  # Use mean values from real data
synthetic_numeric = np.random.multivariate_normal(mean, cov_matrix, size=num_students)

# Convert synthetic data back to categorical and numeric values
synthetic_data = pd.DataFrame(synthetic_numeric, columns=features)

# Convert categorical features back to their original categories
for col in categorical_columns:
    unique_values = category_mappings[col]
    synthetic_data[col] = synthetic_data[col].round().clip(0, len(unique_values) - 1).astype(int)
    synthetic_data[col] = synthetic_data[col].map(unique_values)

# Convert numeric grades back to letter grades for core subjects
reverse_grade_mapping = {v: k for k, v in grade_mapping.items()}
for col in features:
    if col in grade_mapping.values():
        synthetic_data[col] = synthetic_data[col].round().clip(0, 8).map(reverse_grade_mapping)

# Ensure numerical columns like Year of Birth and English Proficiency are integers
numeric_columns = ["Year of Birth", "English Proficiency", "Interest in Studying Computer", "Average Studying Hours per Week"]
synthetic_data[numeric_columns] = synthetic_data[numeric_columns].round().astype(int)

scaler = MinMaxScaler(feature_range=(1999, 2005))
synthetic_data["Year of Birth"] = scaler.fit_transform(synthetic_data[["Year of Birth"]])
synthetic_data["Year of Birth"] = synthetic_data["Year of Birth"].round(0).astype(int)

# ---- ADDITIONAL SUBJECTS: RULE-BASED SAMPLING ----
additional_subjects_map = {
    "SOFTWARE PROJECT MANAGEMENT": ["SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
    "SOFTWARE CONSTRUCTION AND CONFIGURATION": ["PROGRAMMING AND PROBLEM SOLVING", "SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
    "WIRELESS APPLICATION DEVELOPMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
    "ADVANCED WEB APPLICATION DEVELOPMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
    "SOFTWARE QUALITY ASSURANCE": ["SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
    "SOFTWARE ENTREPRENEURSHIP": ["SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
    "PROJECT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS", "SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "SOFTWARE TESTING"],
    "MULTIMEDIA TECHNOLOGY": ["SOFTWARE AND REQUIREMENTS", "SOFTWARE DESIGN", "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY"],
    "ARTIFICIAL INTELLIGENCE": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
    "TEAM PROJECT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
    "PROGRAMMING WITH GAME ENGINES": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "WEB APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
    "ADVANCED DATABASE SYSTEMS": ["DATABASE SYSTEM FUNDAMENTALS", "PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
    "CLOUD COMPUTING": ["DATABASE SYSTEM FUNDAMENTALS", "PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT"],
    "DIGITAL IMAGE PROCESSING": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "WEB APPLICATION DEVELOPMENT"],
    "FUNDAMENTALS OF CYBERSECURITY": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
    "PARALLEL PROCESSING": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT",  "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
    "DATA MINING": ["PROGRAMMING AND PROBLEM SOLVING", "OBJECT-ORIENTED APPLICATION DEVELOPMENT",  "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
    "TCP/IP NETWORK ROUTING": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
    "SERVER CONFIGURATION AND MANAGEMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "OBJECT-ORIENTED APPLICATION DEVELOPMENT", "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS"],
    "TCP/IP NETWORK APPLICATION DEVELOPMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
    "NETWORK SECURITY MANAGEMENT": ["PROGRAMMING AND PROBLEM SOLVING", "TCP/IP NETWORK FUNDAMENTALS", "WEB APPLICATION DEVELOPMENT", "OBJECT-ORIENTED APPLICATION DEVELOPMENT"],
}

grade_probability = {
    "A+": {"A+": 0.55, "A": 0.25, "A-": 0.12, "B+": 0.05, "B": 0.02, "B-": 0.01, "C+": 0.00, "C": 0.00, "F": 0.00},
    "A":  {"A+": 0.30, "A": 0.35, "A-": 0.18, "B+": 0.10, "B": 0.05, "B-": 0.02, "C+": 0.00, "C": 0.00, "F": 0.00},
    "A-": {"A+": 0.15, "A": 0.30, "A-": 0.25, "B+": 0.18, "B": 0.07, "B-": 0.03, "C+": 0.02, "C": 0.00, "F": 0.00},
    "B+": {"A+": 0.05, "A": 0.12, "A-": 0.18, "B+": 0.30, "B": 0.22, "B-": 0.08, "C+": 0.03, "C": 0.02, "F": 0.00},
    "B":  {"A+": 0.02, "A": 0.05, "A-": 0.12, "B+": 0.22, "B": 0.35, "B-": 0.15, "C+": 0.07, "C": 0.02, "F": 0.00},
    "B-": {"A+": 0.00, "A": 0.02, "A-": 0.05, "B+": 0.12, "B": 0.25, "B-": 0.28, "C+": 0.15, "C": 0.10, "F": 0.03},
    "C+": {"A+": 0.00, "A": 0.00, "A-": 0.02, "B+": 0.05, "B": 0.10, "B-": 0.20, "C+": 0.30, "C": 0.20, "F": 0.08},
    "C":  {"A+": 0.00, "A": 0.00, "A-": 0.00, "B+": 0.02, "B": 0.07, "B-": 0.15, "C+": 0.28, "C": 0.35, "F": 0.13},
    "F":  {"A+": 0.00, "A": 0.00, "A-": 0.00, "B+": 0.01, "B": 0.03, "B-": 0.08, "C+": 0.15, "C": 0.30, "F": 0.43}
}

def assign_additional_subject(influencing_grades):
    """
    Assigns an additional subject's grade based on multiple core subjects' grades.
    The probabilities are averaged across influencing subjects.
    """
    aggregate_probs = {grade: 0 for grade in grade_probability["A+"]}
    
    for grade in influencing_grades:
        for key in grade_probability[grade]:
            aggregate_probs[key] += grade_probability[grade][key]
    
    # Normalize probabilities
    total = len(influencing_grades)
    for key in aggregate_probs:
        aggregate_probs[key] /= total
    
    # Perform weighted random sampling
    return random.choices(list(aggregate_probs.keys()), weights=list(aggregate_probs.values()))[0]

# Generate additional subject grades
for subject, base_subjects in additional_subjects_map.items():
    synthetic_data[subject] = synthetic_data.apply(lambda row: assign_additional_subject(
        [row[subj] for subj in base_subjects]
    ), axis=1)

# Calculate CGPA based on all subject grades using credit hours and a GPA mapping
# Define credit hours for each subject (example values)
credit_hours = {
    "PROGRAMMING AND PROBLEM SOLVING": 4,
    "SOFTWARE AND REQUIREMENTS": 3,
    "TCP/IP NETWORK FUNDAMENTALS": 3,
    "PROBABILITY AND STATISTICS FOR COMPUTING": 3,
    "OBJECT-ORIENTED APPLICATION DEVELOPMENT": 4,
    "DATABASE SYSTEM FUNDAMENTALS": 3,
    "WEB APPLICATION DEVELOPMENT": 4,
    "SOFTWARE DESIGN": 4,
    "SOFTWARE TESTING": 4,
    "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY": 3,
    "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE": 3,
    "HUMAN COMPUTER INTERACTION DESIGN": 3,
    "OPERATING SYSTEMS": 3,
    "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS": 3,
    "SOFTWARE PROJECT MANAGEMENT": 3,
    "SOFTWARE CONSTRUCTION AND CONFIGURATION": 3,
    "WIRELESS APPLICATION DEVELOPMENT": 3,
    "ADVANCED WEB APPLICATION DEVELOPMENT": 4,
    "SOFTWARE QUALITY ASSURANCE": 3,
    "SOFTWARE ENTREPRENEURSHIP": 3,
    "PROJECT": 9,
    "MULTIMEDIA TECHNOLOGY": 3,
    "ARTIFICIAL INTELLIGENCE": 3,
    "TEAM PROJECT": 3,
    "PROGRAMMING WITH GAME ENGINES": 3,
    "ADVANCED DATABASE SYSTEMS": 3,
    "CLOUD COMPUTING": 3,
    "DIGITAL IMAGE PROCESSING": 3,
    "FUNDAMENTALS OF CYBERSECURITY": 3,
    "PARALLEL PROCESSING": 3,
    "DATA MINING": 3,
    "TCP/IP NETWORK ROUTING": 3,
    "SERVER CONFIGURATION AND MANAGEMENT": 3,
    "TCP/IP NETWORK APPLICATION DEVELOPMENT": 3,
    "NETWORK SECURITY MANAGEMENT": 3
}

# Define GPA mapping for CGPA calculation (on a 4.0 scale)
gpa_mapping = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.67,
    "B+": 3.33,
    "B": 3.0,
    "B-": 2.67,
    "C+": 2.33,
    "C": 2.0,
    "F": 0.0
}

def calculate_cgpa(row, subjects, credit_hours, gpa_mapping):
    total_points = 0.0
    total_credits = 0.0
    for subj in subjects:
        grade = row[subj]
        if grade in gpa_mapping:
            total_points += gpa_mapping[grade] * credit_hours[subj]
            total_credits += credit_hours[subj]
    return round(total_points / total_credits, 4) if total_credits != 0 else 0.0

# Calculate CGPA based on all subjects (core + additional)
all_subjects_list = credit_hours.keys()
synthetic_data["CGPA"] = synthetic_data.apply(lambda row: calculate_cgpa(row, all_subjects_list, credit_hours, gpa_mapping), axis=1)

# Save the synthetic dataset
synthetic_data.to_csv("training-data-1000.csv", index=False)

print("✅ Synthetic dataset generated successfully with covariance for core subjects and rule-based sampling for additional subjects!")