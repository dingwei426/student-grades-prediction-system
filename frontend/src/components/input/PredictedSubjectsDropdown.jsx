import React, { useState, useEffect } from "react";
import "../../assets/styles.css";

function PredictSubjectDropdown({ initialData, onDataChange }) {
  // If initialData is provided and its items are objects, map them to subject names.
  let mappedInitial = initialData;
  if (
    initialData &&
    Array.isArray(initialData) &&
    initialData.length > 0 &&
    typeof initialData[0] === "object" &&
    initialData[0].subject
  ) {
    mappedInitial = initialData.map((item) => item.subject);
  }
  const [selectedPredictSubjects, setSelectedPredictSubjects] = useState(
    mappedInitial || []
  );

  useEffect(() => {
    if (typeof onDataChange === "function") {
      onDataChange(selectedPredictSubjects);
    }
  }, [selectedPredictSubjects, onDataChange]);

  return (
    <div className="dropdown-container">
      <div className="dropdown-header">
        <p>Predict Subject Selection</p>
      </div>
      {selectedPredictSubjects.length > 0 && (
        <div className="selected-subjects">
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
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default PredictSubjectDropdown;
