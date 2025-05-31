import React, { useEffect, useState, useCallback } from "react";
import {
  predict,
  getDefaultStudentFields,
} from "../services/predictionServices";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import SideNavBar from "../components/SideNavBar";
import PersonalInfoDropdown from "../components/PersonalInfoDropdown";
import EducationalBackgroundDropdown from "../components/EducationalBackgroundDropdown";
import DegreeSubjectDropdown from "../components/DegreeSubjectDropdown";
import PredictSubjectDropdown from "../components/PredictSubjectDropdown";
import PageHeader from "../components/PageHeader";
import LongButton from "../components/LongButton";
import ErrorModal from "../components/ErrorModal";
import "../assets/styles.css";

const Home = () => {
  const [isPredicting, setIsPredicting] = useState(false);
  const [personalInfo, setPersonalInfo] = useState({});
  const [educationBackground, setEducationBackground] = useState({});
  const [degreeSubjects, setDegreeSubjects] = useState([]);
  const [predictSubjects, setPredictSubjects] = useState([]);
  const [selectedModel, setSelectedModel] = useState("rf_9");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const checkExpired = useCallback(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    try {
      const decoded = jwtDecode(token);
      const currentTime = Date.now() / 1000;

      if (decoded.exp < currentTime) {
        window.alert("Your session has expired. Please log in again.");
        localStorage.removeItem("access_token");
        navigate("/login");
      }
    } catch (err) {
      console.error("Token decoding failed:", err);
      window.alert("Invalid session detected. Please log in again.");
      localStorage.removeItem("access_token");
      navigate("/login");
    }
  }, [navigate]);

  useEffect(() => {
    const fetchHomePage = async () => {
      if (!token) {
        navigate("/login"); // Redirect to login if no token
        return;
      }

      try {
        checkExpired();

        const defaultStudentFields = await getDefaultStudentFields(token);

        setPersonalInfo({
          gender: defaultStudentFields.gender || "Female",
          yob: defaultStudentFields.yob || "2000",
          primary_language: defaultStudentFields.primary_language || "English",
          english_proficiency: defaultStudentFields.english_proficiency || 1,
          year_trimester:
            defaultStudentFields.year_trimester || "Year 1 Trimester 1",
        });

        setEducationBackground({
          secondary_school_location:
            defaultStudentFields.secondary_school_location || "Johor",
          science_stream: defaultStudentFields.science_stream
            ? "Yes"
            : "No" || "No",
          qualification: defaultStudentFields.qualification || "UEC",
          qualification_grades:
            defaultStudentFields.qualification_grades || "Mostly A's",
          assignment_working_frequency:
            defaultStudentFields.assignment_working_frequency || "Never",
          computer_interest: defaultStudentFields.computer_interest || 1,
          studyingHours: defaultStudentFields.average_studying_hour || 0,
          CGPA: defaultStudentFields.cgpa || 0.0,
        });
      } catch (err) {
        console.error("Error fetching home page data:", err);
        localStorage.removeItem("access_token");
        navigate("/login");
      }
    };

    fetchHomePage();
  }, [navigate, checkExpired]);

  useEffect(() => {
    setError("");
  }, [degreeSubjects, predictSubjects]);

  const handlePredict = async () => {
    checkExpired();

    setError("");
    setIsPredicting(true);

    // Map collected data to the expected keys and cast numeric fields to numbers.
    const form_data = {
      gender: personalInfo.gender,
      yob: Number(personalInfo.yob),
      primary_language: personalInfo.primary_language,
      english_proficiency: Number(personalInfo.english_proficiency),
      year_trimester: personalInfo.year_trimester,
      secondary_school_location: educationBackground.secondary_school_location,
      science_stream: educationBackground.science_stream === "Yes",
      qualification: educationBackground.qualification,
      qualification_grades: educationBackground.qualification_grades,
      assignment_working_frequency:
        educationBackground.assignment_working_frequency,
      computer_interest: Number(educationBackground.computer_interest),
      "Average Studying Hours per Week": Number(
        educationBackground.studyingHours
      ),
      CGPA: Number(educationBackground.CGPA),
    };

    // Merge each completed subject into form_data as key and grade as value.
    degreeSubjects.forEach(({ subject, grade }) => {
      form_data[subject] = grade;
    });

    // Validate that no field in form_data is undefined.
    for (const key in form_data) {
      if (form_data[key] === undefined) {
        setError(`Field '${key}' is undefined. Please complete the form.`);
        return;
      }
    }

    // Validate subject selections
    const completedSubjectNames = degreeSubjects.map((item) => item.subject);
    const intersection = completedSubjectNames.filter((subject) =>
      predictSubjects.includes(subject)
    );

    if (degreeSubjects.length === 0) {
      setIsPredicting(false);
      setError("Please select at least one completed subject.");
      return;
    }
    if (predictSubjects.length === 0) {
      setIsPredicting(false);
      setError("Please select at least one subject to predict.");
      return;
    }
    if (intersection.length > 0) {
      setIsPredicting(false);
      setError("A subject cannot exist in both Completed and Predicted lists.");
      return;
    }
    const missingGrade = degreeSubjects.find((item) => !item.grade);
    if (missingGrade) {
      setIsPredicting(false);
      setError("Please select a grade for all completed subjects.");
      return;
    }

    // Build final request object
    const requestData = {
      model_type: selectedModel,
      selected_subjects: Array.isArray(predictSubjects)
        ? predictSubjects.map((item) =>
            typeof item === "object" && item.subject ? item.subject : item
          )
        : [],
      form_data,
    };

    console.log("Request Data:", requestData);

    try {
      const prediction_id = await predict(token, requestData);
      navigate("/prediction-details", {
        state: { prediction_id: prediction_id.prediction_id },
      });
    } catch (error) {
      console.error("Error sending prediction request:", error);
      setError("Failed to predict. Please try again.");
    } finally {
      setIsPredicting(false);
    }
  };

  return (
    <div className="flex-container">
      <SideNavBar />
      <div className="content-container">
        <PageHeader
          title="Grades and CGPA Prediction"
          color="#1167b1"
          textAlign="left"
        />
        <ErrorModal message={error} onClose={() => setError("")} />
        <div className="form-container">
          <PersonalInfoDropdown
            initialData={personalInfo}
            onDataChange={setPersonalInfo}
          />
          <hr />
          <EducationalBackgroundDropdown
            initialData={educationBackground}
            onDataChange={setEducationBackground}
          />
          <hr />
          <DegreeSubjectDropdown onDataChange={setDegreeSubjects} />
          <hr />
          <PredictSubjectDropdown onDataChange={setPredictSubjects} />
        </div>
        <div className="button-container">
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            style={{
              padding: "8px 36px",
              borderRadius: "8px",
              border: "1px solid #ccc",
              fontSize: "1rem",
              height: "40px",
              textAlign: "center",
              textAlignLast: "center",
            }}
          >
            {/* <option value="lgbm_4">LightGBM - (A, B, C, F)</option> */}
            {/* <option value="rf_4">Random Forest - (A, B, C, F)</option> */}
            <option value="lgbm_9">LightGBM (Optimized for speed)</option>
            <option value="rf_9">Random Forest (Optimized for accuracy)</option>
          </select>
          <LongButton text="Predict" onClick={handlePredict} />
        </div>
      </div>
      {/* loading cover */}
      {isPredicting && (
        <div className="loading-overlay">
          <div className="spinner" />
        </div>
      )}
    </div>
  );
};

export default Home;
