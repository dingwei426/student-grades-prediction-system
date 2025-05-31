import React, { useState, useEffect, useCallback } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { getPredictionDetails } from "../services/predictionServices";
import { jwtDecode } from "jwt-decode";
import {
  getAIRecommendation,
  generateAIRecommendation,
} from "../services/aiServices";
import SideNavBar from "../components/SideNavBar";
import PageHeader from "../components/PageHeader";
import PersonalInfoDropdown from "../components/input/PersonalInfoDropdown";
import EducationalBackgroundDropdown from "../components/input/EducationalBackgroundDropdown";
import InputSubjectsDropdown from "../components/input/InputSubjectsDropdown";
import PredictedSubjectsDropdown from "../components/input/PredictedSubjectsDropdown";
import BackIcon from "../assets/img/back.png";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { AiOutlineClose, AiOutlineLoading3Quarters } from "react-icons/ai";
import "../assets/styles.css";

const styles = {
  backArrow: {
    fontSize: 24,
    cursor: "pointer",
    height: 20,
    width: 20,
    marginLeft: 10,
  },
  resultContainer: {
    display: "flex",
    flexDirection: "column",
    margin: "0 15%",
    alignItems: "center",
    width: "80%",
  },
  resultRow: {
    display: "flex",
    justifyContent: "space-between",
    width: "80%",
    padding: 10,
  },
  resultText: { margin: 0, padding: 5 },
  viewInputButton: {
    backgroundColor: "#4caf50",
    color: "#fff",
    border: "none",
    padding: "10px 20px",
    borderRadius: 4,
    cursor: "pointer",
    margin: 20,
  },
  viewInputButtonHover: { backgroundColor: "#388e3c" },
  viewAIButton: {
    backgroundColor: "#1976d2",
    color: "#fff",
    border: "none",
    padding: "10px 20px",
    borderRadius: 4,
    cursor: "pointer",
    margin: 20,
  },
  viewAIButtonHover: { backgroundColor: "#115293" },
  recommendationContainer: {
    width: "80%",
    padding: 20,
    border: "1px solid #ccc",
    borderRadius: 8,
    backgroundColor: "#f9f9f9",
    marginTop: 20,
  },
  recommendationTitle: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 10,
    color: "#1167b1",
  },
  recommendationContent: {
    fontSize: 16,
    lineHeight: 1.5,
    whiteSpace: "pre-wrap",
  },
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0,0,0,0.5)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
  },
  modalContent: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center", // ← CENTER all direct children
    width: "100%",
    maxWidth: 600,
    height: "80vh",
    overflowY: "auto",
    backgroundColor: "#fff",
    borderRadius: 8,
    padding: 24,
    position: "relative",
    boxShadow: "0 2px 10px rgba(0,0,0,0.2)",
  },
  formSection: {
    width: "120%", // your form wrapper
    display: "flex",
    flexDirection: "column",
    alignItems: "center", // ← CENTER the dropdowns inside
    gap: "1rem",
  },

  modalCloseIcon: {
    position: "absolute", // take it out of the normal flow
    top: 16, // distance from the top edge of the modal
    right: 16, // distance from the right edge of the modal
    cursor: "pointer",
    fontSize: 24,
    color: "#666",
  },
};

export default function PredictionResultPage() {
  const [showInputData, setShowInputData] = useState(false);
  const [showAI, setShowAI] = useState(false);
  const [backArrowOpacity, setBackArrowOpacity] = useState(1);
  const [cgpa, setCgpa] = useState(0);
  const [name, setName] = useState("Prediction Name");
  const [model, setModel] = useState("");
  const [inputSubjects, setInputSubjects] = useState([]);
  const [predictedSubjects, setPredictedSubjects] = useState([]);
  const [personalInfoData, setPersonalInfoData] = useState({});
  const [educationBackgroundData, setEducationBackgroundData] = useState({});
  const [aiRecommendation, setAiRecommendation] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");

  const navigate = useNavigate();
  const { state } = useLocation();
  const predictionId = state?.prediction_id;
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

  // Initial fetch for prediction details & home
  useEffect(() => {
    if (!token) return navigate("/login");
    checkExpired();

    const init = async () => {
      if (!predictionId) return;
      try {
        const { prediction: pred } = await getPredictionDetails(
          token,
          predictionId
        );
        setName(pred.name);
        setCgpa(pred.predicted_cgpa);
        // map model code to label
        const modelMap = {
          rf_4: "Random Forest - (A, B, C, F)",
          lgbm_4: "LightGBM - (A, B, C, F)",
          rf_9: "Random Forest - (A+, A, A-, B+, B, B-, C+, C, F)",
          lgbm_9: "LightGBM - (A+, A, A-, B+ , B, B-, C+, C, F)",
        };
        setModel(modelMap[pred.model_used] || pred.model_used);

        setPersonalInfoData({
          gender: pred.gender,
          yob: pred.yob.toString(),
          primary_language: pred.primary_language,
          english_proficiency: pred.english_proficiency,
          year_trimester: pred.year_trimester,
        });

        setEducationBackgroundData({
          secondary_school_location: pred.secondary_school_location,
          science_stream: pred.science_stream ? "Yes" : "No",
          qualification: pred.qualification,
          qualification_grades: pred.qualification_grades,
          assignment_working_frequency: pred.assignment_working_frequency,
          computer_interest: pred.computer_interest,
          studyingHours: pred.average_studying_hour,
          CGPA: pred.cgpa,
        });

        const allSubs = pred.subjects || [];
        setInputSubjects(
          allSubs
            .filter((s) => !s.is_prediction)
            .map((s) => ({ subject: s.name, grade: s.grade }))
        );
        setPredictedSubjects(
          allSubs
            .filter(
              (s) => s.is_prediction && pred.selected_subjects.includes(s.name)
            )
            .map((s) => ({ subject: s.name, grade: s.grade }))
        );
      } catch (err) {
        console.error("Error loading prediction details:", err);
      }
    };

    init();
  }, [predictionId, navigate, checkExpired]);

  useEffect(() => {
    if (!predictionId || !token) return;
    setAiLoading(true);
    getAIRecommendation(token, predictionId)
      .then((resp) => {
        if (resp && resp.trim()) {
          setAiRecommendation(resp);
        }
      })
      .catch((err) => {
        console.warn("No existing AI suggestion:", err);
      })
      .finally(() => setAiLoading(false));
  }, [predictionId, token]);

  const toggleShowAI = () => {
    setShowAI((v) => !v);
  };

  const handleGenerate = async () => {
    checkExpired();

    setAiError("");
    setAiLoading(true);
    try {
      const resp = await generateAIRecommendation(token, predictionId);
      setAiRecommendation(resp);
      setShowAI(true);
    } catch (err) {
      console.error("AI generation failed:", err);
      setAiError("Failed to generate AI recommendations.");
    } finally {
      setAiLoading(false);
    }
  };

  // const cleanMarkdown = (raw) =>
  //   raw
  //     .replace(/<\s*think\s*>.*?<\s*\/\s*think\s*>/gis, "")
  //     .replace(/<｜end▁of▁sentence｜>/g, "")
  //     .replace(/\n{2,}/g, "\n\n")
  //     .trim();

  return (
    <div className="flex-container">
      <SideNavBar />
      <div className="content-container">
        {/* Header */}
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "flex-start",
            alignItems: "center",
            width: "100%",
            marginBottom: "20px",
          }}
        >
          <img
            src={BackIcon}
            alt="back"
            style={{ ...styles.backArrow, opacity: backArrowOpacity }}
            onClick={() => navigate(-1)}
            onMouseOver={() => setBackArrowOpacity(0.7)}
            onMouseOut={() => setBackArrowOpacity(1)}
          />
          <PageHeader title={name} color="#1167b1" textAlign="left" />
        </div>

        {/* Predicted Grades */}
        <div style={styles.resultContainer}>
          {predictedSubjects.map((r, i) => (
            <div key={i} style={styles.resultRow}>
              <p style={styles.resultText}>{r.subject}</p>
              <p style={styles.resultText}>{r.grade}</p>
            </div>
          ))}
          <hr
            style={{
              width: "80%",
              borderTop: "1px solid #ccc",
              margin: "8px 0",
            }}
          />
          <div style={styles.resultRow}>
            <p style={{ ...styles.resultText }}>Model: {model}</p>
            <p style={{ ...styles.resultText }}>CGPA: {cgpa}</p>
          </div>
        </div>

        {/* INPUT DATA MODAL */}
        {showInputData && (
          <div style={styles.modalOverlay}>
            <div style={styles.modalContent}>
              <AiOutlineClose
                onClick={() => setShowInputData(false)}
                style={styles.modalCloseIcon}
              />

              <h2 style={styles.recommendationTitle}>Input Data</h2>

              <div style={styles.formSection}>
                <PersonalInfoDropdown
                  initialData={personalInfoData}
                  onDataChange={() => {}}
                />
                <EducationalBackgroundDropdown
                  initialData={educationBackgroundData}
                  onDataChange={() => {}}
                />
                <InputSubjectsDropdown initialData={inputSubjects} />
                <PredictedSubjectsDropdown initialData={predictedSubjects} />
              </div>
            </div>
          </div>
        )}

        {/* AI RECOMMENDATIONS PANEL */}
        {showAI && aiRecommendation && (
          <div style={styles.resultContainer}>
            <div
              style={{
                ...styles.recommendationContainer,
                position: "relative",
              }}
            >
              {/* Close icon */}
              <AiOutlineClose
                onClick={() => setShowAI(false)}
                style={{
                  position: "absolute",
                  top: 10,
                  right: 10,
                  cursor: "pointer",
                  fontSize: 24,
                  color: "#666",
                }}
              />

              <h2 style={styles.recommendationTitle}>AI Recommendations</h2>
              {aiError ? (
                <p style={{ color: "red" }}>{aiError}</p>
              ) : (
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h2: ({ node, ...props }) => (
                      <h2 style={styles.recommendationTitle} {...props} />
                    ),
                    p: ({ node, ...props }) => (
                      <p style={{ marginBottom: 0 }} {...props} />
                    ),
                    ul: ({ node, ...props }) => (
                      <ul
                        style={{ paddingLeft: "1.5em", marginBottom: 0 }}
                        {...props}
                      />
                    ),
                    li: ({ node, ...props }) => (
                      <li style={{ marginBottom: 0 }} {...props} />
                    ),
                  }}
                >
                  {/* {cleanMarkdown(aiRecommendation)} */}
                  {aiRecommendation}
                </ReactMarkdown>
              )}
            </div>
          </div>
        )}

        {/* ALL YOUR BUTTONS IN A ROW */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: "1rem",
            flexWrap: "wrap",
            marginTop: "20px",
          }}
        >
          <button
            style={styles.viewInputButton}
            onClick={() => setShowInputData((v) => !v)}
            onMouseOver={(e) =>
              (e.target.style.backgroundColor =
                styles.viewInputButtonHover.backgroundColor)
            }
            onMouseOut={(e) =>
              (e.target.style.backgroundColor =
                styles.viewInputButton.backgroundColor)
            }
          >
            {showInputData ? "Hide Input Data" : "View Input Data"}
          </button>

          <button
            style={{
              ...styles.viewAIButton,
              opacity: aiLoading ? 0.6 : 1,
              cursor: aiLoading ? "not-allowed" : "pointer",
            }}
            onClick={handleGenerate}
            disabled={aiLoading}
            onMouseOver={(e) =>
              !aiLoading &&
              (e.target.style.backgroundColor =
                styles.viewAIButtonHover.backgroundColor)
            }
            onMouseOut={(e) =>
              !aiLoading &&
              (e.target.style.backgroundColor =
                styles.viewAIButton.backgroundColor)
            }
          >
            {aiLoading ? (
              <>
                <AiOutlineLoading3Quarters className="spinner-icon" />
                Generating…
              </>
            ) : aiRecommendation ? (
              "Regenerate Recommendations"
            ) : (
              "Generate Recommendations"
            )}
          </button>

          {aiRecommendation && (
            <button
              style={styles.viewAIButton}
              onClick={toggleShowAI}
              disabled={aiLoading}
              onMouseOver={(e) =>
                (e.target.style.backgroundColor =
                  styles.viewAIButtonHover.backgroundColor)
              }
              onMouseOut={(e) =>
                (e.target.style.backgroundColor =
                  styles.viewAIButton.backgroundColor)
              }
            >
              {showAI ? "Hide Recommendations" : "View Recommendations"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
