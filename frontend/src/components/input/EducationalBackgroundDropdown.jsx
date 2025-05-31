// import React from "react";
// import "../../assets/styles.css";

// function EducationalBackgroundDropdown({ initialData }) {
//   const defaultData = {
//     secondary_school_location: "Johor",
//     science_stream: "Yes",
//     qualification: "UEC",
//     qualification_grades: "Mostly A's",
//     assignment_working_frequency: "Never",
//     computer_interest: 1,
//     studyingHours: 1,
//     CGPA: 0,
//   };

//   // Use the initialData if provided; otherwise, use defaultData.
//   const educationData = initialData || defaultData;

//   return (
//     <div className="dropdown-container">
//       {/* Header section */}
//       <div className="dropdown-header">
//         <p>Educational Background</p>
//       </div>
//       {/* Content Section: Display each field */}
//       <div className="dropdown-content">
//         <div className="input-field">
//           <label>Secondary School Location</label>
//           <p>{educationData.secondary_school_location}</p>
//         </div>
//         <div className="input-field">
//           <label>Science Stream Enrolled?</label>
//           <p>{educationData.science_stream}</p>
//         </div>
//         <div className="input-field">
//           <label>Completed Qualification</label>
//           <p>{educationData.qualification}</p>
//         </div>
//         <div className="input-field">
//           <label>Qualification Grades</label>
//           <p>{educationData.qualification_grades}</p>
//         </div>
//         <div className="input-field">
//           <label>Assignment Working Frequency</label>
//           <p>{educationData.assignment_working_frequency}</p>
//         </div>
//         <div className="input-field">
//           <label>Interest in Studying Computer (1 - 5)</label>
//           <p>{educationData.computer_interest}</p>
//         </div>
//         <div className="input-field">
//           <label>Average Studying Hours per Week</label>
//           <p>{educationData.studyingHours}</p>
//         </div>
//         <div className="input-field">
//           <label>CGPA</label>
//           <p>{educationData.CGPA}</p>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default EducationalBackgroundDropdown;

import React from "react";
import "../../assets/styles.css";

function EducationalBackgroundDropdown({ initialData }) {
  const defaultData = {
    secondary_school_location: "Johor",
    science_stream: "Yes",
    qualification: "UEC",
    qualification_grades: "Mostly A's",
    assignment_working_frequency: "Never",
    computer_interest: 1,
    studyingHours: 1,
    CGPA: 0,
  };

  // Use defaultData if initialData is empty
  const educationData =
    initialData && Object.keys(initialData).length > 0
      ? initialData
      : defaultData;

  return (
    <div className="dropdown-container">
      <div className="dropdown-header">
        <p>Educational Background</p>
      </div>
      <div className="selected-subjects">
        <div className="input-field">
          <label>Secondary School Location</label>
          <p>{educationData.secondary_school_location}</p>
        </div>
        <div className="input-field">
          <label>Science Stream Enrolled?</label>
          <p>{educationData.science_stream}</p>
        </div>
        <div className="input-field">
          <label>Completed Qualification</label>
          <p>{educationData.qualification}</p>
        </div>
        <div className="input-field">
          <label>Qualification Grades</label>
          <p>{educationData.qualification_grades}</p>
        </div>
        <div className="input-field">
          <label>Assignment Working Frequency</label>
          <p>{educationData.assignment_working_frequency}</p>
        </div>
        <div className="input-field">
          <label>Interest in Studying Computer (1 - 5)</label>
          <p>{educationData.computer_interest}</p>
        </div>
        <div className="input-field">
          <label>Average Studying Hours per Week</label>
          <p>{educationData.studyingHours}</p>
        </div>
        <div className="input-field">
          <label>CGPA</label>
          <p>{educationData.CGPA}</p>
        </div>
      </div>
    </div>
  );
}

export default EducationalBackgroundDropdown;
