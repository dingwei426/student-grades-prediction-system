// import React, { useState, useEffect } from "react";
// import "../assets/styles.css";
// import DropdownArrow from "../assets/img/dropdown-arrow.png";

// function EducationalBackgroundDropdown({ onDataChange }) {
//   const [isOpen, setIsOpen] = useState(false);
//   // Initial state with default (first option) values
//   const [educationData, setEducationData] = useState({
//     secondary_school_location: "Johor", // default: first option "Johor"
//     science_stream: "Yes", // default: "Yes"
//     qualification: "UEC", // default: "UEC"
//     qualification_grades: "Mostly A's", // default: "Mostly A's"
//     assignment_working_frequency: "Never", // default: "Never"
//     computer_interest: 1, // default numeric value
//     studyingHours: 1, // default numeric value
//     CGPA: 0, // default numeric value (can be adjusted)
//   });

//   useEffect(() => {
//     onDataChange(educationData);
//   }, [educationData, onDataChange]);

//   const toggleDropdown = () => {
//     setIsOpen(!isOpen);
//   };

//   const handleChange = (e) => {
//     setEducationData({ ...educationData, [e.target.name]: e.target.value });
//   };

//   return (
//     <div className={`dropdown-container ${isOpen ? "open" : "closed"}`}>
//       <div onClick={toggleDropdown} className="dropdown-header">
//         <p>Educational Background</p>
//         <img
//           className={`arrow ${isOpen ? "up" : "down"}`}
//           src={DropdownArrow}
//           alt="dropdown-arrow"
//         />
//       </div>
//       <div className="dropdown-content">
//         <div className="input-field">
//           <label>Secondary School Location</label>
//           <select
//             name="secondary_school_location"
//             value={educationData.secondary_school_location}
//             onChange={handleChange}
//           >
//             {/* Removed "Select..." option */}
//             <option value="Johor">Johor</option>
//             <option value="Kedah">Kedah</option>
//             <option value="Kelantan">Kelantan</option>
//             <option value="Kuala-lumpur">Kuala Lumpur</option>
//             <option value="Labuan">Labuan</option>
//             <option value="Malacca">Malacca</option>
//             <option value="Negeri-sembilan">Negeri Sembilan</option>
//             <option value="Pahang">Pahang</option>
//             <option value="Penang">Penang</option>
//             <option value="Perak">Perak</option>
//             <option value="Perlis">Perlis</option>
//             <option value="Putrajaya">Putrajaya</option>
//             <option value="Sabah">Sabah</option>
//             <option value="Sarawak">Sarawak</option>
//             <option value="Selangor">Selangor</option>
//             <option value="Terengganu">Terengganu</option>
//           </select>
//         </div>

//         <div className="input-field">
//           <label>
//             Are you enrolled in Science stream during high school education?
//           </label>
//           <select
//             name="science_stream"
//             value={educationData.science_stream}
//             onChange={handleChange}
//           >
//             {/* Removed "Select..." option */}
//             <option value="Yes">Yes</option>
//             <option value="No">No</option>
//           </select>
//         </div>

//         <div className="input-field">
//           <label>
//             What is your completed qualification before enrolling in degree?
//           </label>
//           <select
//             name="qualification"
//             value={educationData.qualification}
//             onChange={handleChange}
//           >
//             {/* Default set to UEC */}
//             <option value="UEC">UEC (Unified Examination Certificate)</option>
//             <option value="Foundation Art">Foundation in Art</option>
//             <option value="Foundation Science">Foundation in Science</option>
//             <option value="Diploma">Diploma</option>
//             <option value="A-Level">A-Level</option>
//             <option value="STPM">STPM</option>
//           </select>
//         </div>

//         <div className="input-field">
//           <label>
//             How were your grades in the qualification before enrolling in
//             degree?
//           </label>
//           <select
//             name="qualification_grades"
//             value={educationData.qualification_grades}
//             onChange={handleChange}
//           >
//             {/* Default set to "Mostly A's" */}
//             <option value="Mostly A's">Mostly A's</option>
//             <option value="Mostly B's">Mostly B's</option>
//             <option value="Mostly C's">Mostly C's</option>
//             <option value="Mostly D's">Mostly D's</option>
//             <option value="Mostly E/F's">Mostly E/F's</option>
//             <option value="N/A">N/A</option>
//           </select>
//         </div>

//         <div className="input-field">
//           <label>
//             Do you work with classmates often to prepare assignments?
//           </label>
//           <select
//             name="assignment_working_frequency"
//             value={educationData.assignment_working_frequency}
//             onChange={handleChange}
//           >
//             {/* Default set to "Never" */}
//             <option value="Never">Never</option>
//             <option value="Sometimes">Sometimes</option>
//             <option value="Often">Often</option>
//             <option value="Very-often">Very Often</option>
//           </select>
//         </div>

//         <div className="input-field">
//           <label>Interest in studying computer (1 - 5)</label>
//           <input
//             type="number"
//             name="computer_interest"
//             min="1"
//             max="5"
//             value={educationData.computer_interest}
//             onChange={handleChange}
//           />
//         </div>

//         <div className="input-field">
//           <label>Average studying hours per week (excluding class hours)</label>
//           <input
//             type="number"
//             name="studyingHours"
//             min="1"
//             max="84"
//             value={educationData.studyingHours}
//             onChange={handleChange}
//           />
//         </div>

//         <div className="input-field">
//           <label>CGPA</label>
//           <input
//             type="number"
//             name="CGPA"
//             min="0.0000"
//             max="4.0000"
//             step="0.01"
//             value={educationData.CGPA}
//             onChange={handleChange}
//           />
//         </div>
//       </div>
//     </div>
//   );
// }

// export default EducationalBackgroundDropdown;

import React, { useState, useEffect } from "react";
import "../assets/styles.css";
import DropdownArrow from "../assets/img/dropdown-arrow.png";

function EducationalBackgroundDropdown({ initialData, onDataChange }) {
  const defaultData = {
    secondary_school_location: "Johor",
    science_stream: "No",
    qualification: "UEC",
    qualification_grades: "Mostly A's",
    assignment_working_frequency: "Never",
    computer_interest: 1,
    studyingHours: 0,
    CGPA: 0,
  };

  const [educationData, setEducationData] = useState(
    initialData || defaultData
  );
  const [isOpen, setIsOpen] = useState(false);

  // Update local state when initialData prop changes.
  useEffect(() => {
    if (initialData) {
      setEducationData(initialData);
    }
  }, [initialData]);

  useEffect(() => {
    if (typeof onDataChange === "function") {
      onDataChange(educationData);
    }
  }, [educationData, onDataChange]);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    let newValue = value;

    // Validate CGPA (0 to 4)
    if (name === "CGPA") {
      let cgpa = parseFloat(value);
      if (isNaN(cgpa)) cgpa = 0;
      if (cgpa < 0) cgpa = 0;
      if (cgpa > 4) cgpa = 4;
      newValue = cgpa;
    }

    // Validate computer_interest (0 to 5)
    if (name === "computer_interest") {
      let interest = parseFloat(value);
      if (isNaN(interest)) interest = 0;
      if (interest < 0) interest = 0;
      if (interest > 5) interest = 5;
      newValue = interest;
    }

    setEducationData({ ...educationData, [name]: newValue });
  };

  return (
    <div className={`dropdown-container ${isOpen ? "open" : "closed"}`}>
      <div onClick={toggleDropdown} className="dropdown-header">
        <p>Educational Background</p>
        <img
          className={`arrow ${isOpen ? "up" : "down"}`}
          src={DropdownArrow}
          alt="dropdown-arrow"
        />
      </div>
      <div className="dropdown-content">
        <div className="input-field">
          <label>Secondary School Location</label>
          <select
            name="secondary_school_location"
            value={educationData.secondary_school_location}
            onChange={handleChange}
          >
            <option value="Johor">Johor</option>
            <option value="Kedah">Kedah</option>
            <option value="Kelantan">Kelantan</option>
            <option value="Kuala-lumpur">Kuala Lumpur</option>
            <option value="Labuan">Labuan</option>
            <option value="Malacca">Malacca</option>
            <option value="Negeri-sembilan">Negeri Sembilan</option>
            <option value="Pahang">Pahang</option>
            <option value="Penang">Penang</option>
            <option value="Perak">Perak</option>
            <option value="Perlis">Perlis</option>
            <option value="Putrajaya">Putrajaya</option>
            <option value="Sabah">Sabah</option>
            <option value="Sarawak">Sarawak</option>
            <option value="Selangor">Selangor</option>
            <option value="Terengganu">Terengganu</option>
          </select>
        </div>
        <div className="input-field">
          <label>
            Are you enrolled in Science stream during high school education?
          </label>
          <select
            name="science_stream"
            value={educationData.science_stream}
            onChange={handleChange}
          >
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>
        <div className="input-field">
          <label>
            What is your completed qualification before enrolling in degree?
          </label>
          <select
            name="qualification"
            value={educationData.qualification}
            onChange={handleChange}
          >
            <option value="UEC">UEC</option>
            <option value="Foundation Art">Foundation in Art</option>
            <option value="Foundation Science">Foundation in Science</option>
            <option value="Diploma">Diploma</option>
            <option value="A-Level">A-Level</option>
            <option value="STPM">STPM</option>
          </select>
        </div>
        <div className="input-field">
          <label>
            How were your grades in the qualification before enrolling in
            degree?
          </label>
          <select
            name="qualification_grades"
            value={educationData.qualification_grades}
            onChange={handleChange}
          >
            <option value="Mostly A's">Mostly A's</option>
            <option value="Mostly B's">Mostly B's</option>
            <option value="Mostly C's">Mostly C's</option>
            <option value="Mostly D's">Mostly D's</option>
            <option value="Mostly E/F's">Mostly E/F's</option>
            <option value="N/A">N/A</option>
          </select>
        </div>
        <div className="input-field">
          <label>
            Do you work with classmates often to prepare assignments?
          </label>
          <select
            name="assignment_working_frequency"
            value={educationData.assignment_working_frequency}
            onChange={handleChange}
          >
            <option value="Never">Never</option>
            <option value="Sometimes">Sometimes</option>
            <option value="Often">Often</option>
            <option value="Very-often">Very Often</option>
          </select>
        </div>
        <div className="input-field">
          <label>Interest in studying computer (1 - 5)</label>
          <input
            type="number"
            name="computer_interest"
            min="1"
            max="5"
            value={educationData.computer_interest}
            onChange={handleChange}
          />
        </div>
        <div className="input-field">
          <label>Average studying hours per week (excluding class hours)</label>
          <input
            type="number"
            name="studyingHours"
            min="1"
            max="84"
            value={educationData.studyingHours}
            onChange={handleChange}
          />
        </div>
        <div className="input-field">
          <label>CGPA</label>
          <input
            type="number"
            name="CGPA"
            min="0.0000"
            max="4.0000"
            step="0.01"
            value={educationData.CGPA}
            onChange={handleChange}
          />
        </div>
      </div>
    </div>
  );
}

export default EducationalBackgroundDropdown;
