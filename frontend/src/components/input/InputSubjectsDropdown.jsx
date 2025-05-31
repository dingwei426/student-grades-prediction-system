import React, { useState } from "react";
import "../../assets/styles.css";

function DegreeSubjectDropdown({ initialData }) {
  // Set state to the passed initialData; if nothing is passed, default to an empty array.
  const [selectedSubjects] = useState(initialData || []);

  return (
    <div className="dropdown-container">
      <div className="dropdown-header">
        <p>Degree Subject Grades Input</p>
      </div>
      {selectedSubjects.length > 0 ? (
        <div className="selected-subjects">
          <ol>
            {selectedSubjects.map((item, index) => (
              <li
                key={item.subject}
                className="input-field"
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "5px 0",
                }}
              >
                <span
                  className="subject-label"
                  style={{ textAlign: "left", flex: 1 }}
                >
                  {index + 1}. {item.subject}
                </span>
                <span
                  className="subject-grade"
                  style={{ textAlign: "right", marginLeft: "10px" }}
                >
                  Grade: {item.grade}
                </span>
              </li>
            ))}
          </ol>
        </div>
      ) : (
        <p>No subjects provided</p>
      )}
    </div>
  );
}

export default DegreeSubjectDropdown;
