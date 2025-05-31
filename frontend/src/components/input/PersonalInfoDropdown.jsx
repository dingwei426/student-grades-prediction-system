import React from "react";
import "../../assets/styles.css";

function PersonalInfoDropdown({ initialData }) {
  return (
    <div className="dropdown-container">
      <div className="dropdown-header">
        <p>Personal Information</p>
      </div>
      <div className="selected-subjects">
        <div className="input-field">
          <label>Gender</label>
          <p>{initialData.gender}</p>
        </div>
        <div className="input-field">
          <label>Year of Birth</label>
          <p>{initialData.yob}</p>
        </div>
        <div className="input-field">
          <label>Primary Language</label>
          <p>{initialData.primary_language}</p>
        </div>
        <div className="input-field">
          <label>English Proficiency (1 - 5)</label>
          <p>{initialData.english_proficiency}</p>
        </div>
        <div className="input-field">
          <label>Academic Year & Trimester</label>
          <p>{initialData.year_trimester}</p>
        </div>
      </div>
    </div>
  );
}

export default PersonalInfoDropdown;
