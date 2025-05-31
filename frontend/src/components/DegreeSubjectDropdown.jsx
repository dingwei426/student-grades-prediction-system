import React, { useState, useEffect } from "react";
import "../assets/styles.css";
import DropdownArrow from "../assets/img/dropdown-arrow.png";

const subjects = [
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

function DegreeSubjectDropdown({ onDataChange }) {
  // Change state to store objects: { subject, grade }
  const [isOpen, setIsOpen] = useState(false);
  const [selectedSubjects, setSelectedSubjects] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  // Propagate the list of objects to the parent whenever selectedSubjects update
  useEffect(() => {
    onDataChange(selectedSubjects);
  }, [selectedSubjects, onDataChange]);

  // Toggle a subject's selection: add (with an empty grade) if not present; remove if already selected.
  const handleSubjectChange = (subject) => {
    const found = selectedSubjects.find((item) => item.subject === subject);
    if (found) {
      // Remove the subject from the array
      setSelectedSubjects(
        selectedSubjects.filter((item) => item.subject !== subject)
      );
    } else {
      // Add the subject with an empty grade field
      setSelectedSubjects([...selectedSubjects, { subject, grade: "" }]);
    }
  };

  // Update the grade for a subject that is already selected
  const handleGradeChange = (subject, newGrade) => {
    const updatedSubjects = selectedSubjects.map((item) =>
      item.subject === subject ? { ...item, grade: newGrade } : item
    );
    setSelectedSubjects(updatedSubjects);
  };

  const filteredSubjects = subjects.filter((subject) =>
    subject.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="dropdown-container">
      <div className="dropdown-header" onClick={() => setIsOpen(!isOpen)}>
        <p>Degree Subject Grades Input</p>
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
          {filteredSubjects.length > 0 ? (
            filteredSubjects.map((subject) => (
              <label key={subject} className="subject-option">
                <input
                  type="checkbox"
                  value={subject}
                  checked={selectedSubjects.some(
                    (item) => item.subject === subject
                  )}
                  onChange={() => handleSubjectChange(subject)}
                />
                {subject}
              </label>
            ))
          ) : (
            <p className="no-results">No subjects found</p>
          )}
        </div>
      )}

      {selectedSubjects.length > 0 && (
        <div className="selected-subjects">
          <h4>Subjects Completed</h4>
          <ol>
            {selectedSubjects.map((item, index) => (
              <li key={item.subject} className="input-field">
                <span className="subject-label">
                  {index + 1}. {item.subject}
                </span>
                <select
                  value={item.grade}
                  onChange={(e) =>
                    handleGradeChange(item.subject, e.target.value)
                  }
                  className="grade-select"
                >
                  <option value="" disabled>
                    Select grade
                  </option>
                  <option value="A+">A+</option>
                  <option value="A">A</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B">B</option>
                  <option value="B-">B-</option>
                  <option value="C+">C+</option>
                  <option value="C">C</option>
                  <option value="F">F</option>
                </select>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default DegreeSubjectDropdown;
