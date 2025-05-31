import React, { useState, useEffect } from "react";
import "../assets/styles.css";
import DropdownArrow from "../assets/img/dropdown-arrow.png";
import LongButton from "./LongButton";

const predictSubjects = [
  "ADVANCED DATABASE SYSTEMS",
  "ADVANCED WEB APPLICATION DEVELOPMENT",
  "ARTIFICIAL INTELLIGENCE",
  "CLOUD COMPUTING",
  "COMPUTER ETHICS AND PROFESSIONAL RESPONSIBILITY",
  "DATA MINING",
  "DATABASE SYSTEM FUNDAMENTALS",
  "DIGITAL IMAGE PROCESSING",
  "FUNDAMENTALS OF CYBERSECURITY",
  "HUMAN COMPUTER INTERACTION DESIGN",
  "INTRODUCTION TO COMPUTER ORGANISATION AND ARCHITECTURE",
  "MULTIMEDIA TECHNOLOGY",
  "NETWORK SECURITY MANAGEMENT",
  "OBJECT-ORIENTED APPLICATION DEVELOPMENT",
  "OPERATING SYSTEMS",
  "PARALLEL PROCESSING",
  "PROBABILITY AND STATISTICS FOR COMPUTING",
  "PROBLEM SOLVING WITH DATA STRUCTURES AND ALGORITHMS",
  "PROGRAMMING AND PROBLEM SOLVING",
  "PROGRAMMING WITH GAME ENGINES",
  "PROJECT",
  "SERVER CONFIGURATION AND MANAGEMENT",
  "SOFTWARE AND REQUIREMENTS",
  "SOFTWARE CONSTRUCTION AND CONFIGURATION",
  "SOFTWARE DESIGN",
  "SOFTWARE ENTREPRENEURSHIP",
  "SOFTWARE PROJECT MANAGEMENT",
  "SOFTWARE QUALITY ASSURANCE",
  "SOFTWARE TESTING",
  "TCP/IP NETWORK APPLICATION DEVELOPMENT",
  "TCP/IP NETWORK FUNDAMENTALS",
  "TCP/IP NETWORK ROUTING",
  "TEAM PROJECT",
  "WEB APPLICATION DEVELOPMENT",
  "WIRELESS APPLICATION DEVELOPMENT",
];

function PredictSubjectDropdown({ onDataChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedPredictSubjects, setSelectedPredictSubjects] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  // Propagate changes to the parent whenever selectedPredictSubjects update
  useEffect(() => {
    onDataChange(selectedPredictSubjects);
  }, [selectedPredictSubjects, onDataChange]);

  // Toggle selection: add if not selected; remove if already selected.
  const handlePredictSubjectChange = (subject) => {
    setSelectedPredictSubjects((prev) =>
      prev.includes(subject)
        ? prev.filter((item) => item !== subject)
        : [...prev, subject]
    );
  };

  const handleRemovePredictSubject = (subject) => {
    setSelectedPredictSubjects((prev) =>
      prev.filter((item) => item !== subject)
    );
  };

  const filteredPredictSubjects = predictSubjects.filter((subject) =>
    subject.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="dropdown-container">
      <div className="dropdown-header" onClick={() => setIsOpen(!isOpen)}>
        <p>Predict Subject Selection</p>
        <img
          className={`arrow ${isOpen ? "up" : "down"}`}
          src={DropdownArrow}
          alt="dropdown-arrow"
        />
      </div>

      {isOpen && (
        <div className="dropdown-list">
          <input
            type="text"
            placeholder="Search subject..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          {filteredPredictSubjects.length > 0 ? (
            filteredPredictSubjects.map((subject) => (
              <label key={subject} className="subject-option">
                <input
                  type="checkbox"
                  value={subject}
                  checked={selectedPredictSubjects.includes(subject)}
                  onChange={() => handlePredictSubjectChange(subject)}
                />
                {subject}
              </label>
            ))
          ) : (
            <p className="no-results">No subjects found</p>
          )}
        </div>
      )}

      {selectedPredictSubjects.length > 0 && (
        <div className="selected-subjects">
          <h4>Subjects to be Predicted</h4>
          <ol>
            {selectedPredictSubjects.map((subject, index) => (
              <li
                key={subject}
                className="input-field"
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "8px 0",
                }}
              >
                <span className="subject-label">
                  {index + 1}. {subject}
                </span>
                {/* Wrapper div to fix the width and align the button to the right */}
                <div
                  className="button-container"
                  style={{ width: "160px", textAlign: "right" }}
                >
                  <LongButton
                    text="Remove"
                    onClick={() => handleRemovePredictSubject(subject)}
                    isHoveredColor="#e57373"
                    backgroundColor="#e62828"
                  />
                </div>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default PredictSubjectDropdown;
