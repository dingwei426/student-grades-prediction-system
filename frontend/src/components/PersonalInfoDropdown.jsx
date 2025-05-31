// import React, { useState, useEffect } from "react";
// import "../assets/styles.css";
// import DropdownArrow from "../assets/img/dropdown-arrow.png";

// function PersonalInfoDropdown({ onDataChange }) {
//   const [isOpen, setIsOpen] = useState(false);
//   // Initial state with default values from the first option (or a sensible default)
//   const [formData, setFormData] = useState({
//     gender: "Female", // default: first option "Female"
//     yob: "2003", // default year (can be adjusted as needed)
//     primary_language: "English", // default: first option "English"
//     english_proficiency: 1, // default numeric value (lowest value from 1–5)
//     year_trimester: "Year 1 Trimester 1", // default: first option
//   });

//   useEffect(() => {
//     onDataChange(formData);
//   }, [formData, onDataChange]);

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   return (
//     <div className={`dropdown-container ${isOpen ? "open" : "closed"}`}>
//       <div onClick={() => setIsOpen(!isOpen)} className="dropdown-header">
//         <p>Personal Information</p>
//         <img
//           className={`arrow ${isOpen ? "up" : "down"}`}
//           src={DropdownArrow}
//           alt="dropdown-arrow"
//         />
//       </div>
//       <div className="dropdown-content">
//         <div className="input-field">
//           <label>Gender</label>
//           <select name="gender" value={formData.gender} onChange={handleChange}>
//             {/* Removed "Select..." option so default appears */}
//             <option value="Female">Female</option>
//             <option value="Male">Male</option>
//           </select>
//         </div>

//         <div className="input-field">
//           <label>Year of Birth</label>
//           <input
//             type="number"
//             name="yob"
//             min="1900"
//             max="2100"
//             value={formData.yob}
//             onChange={handleChange}
//           />
//         </div>

//         <div className="input-field">
//           <label>Primary Language</label>
//           <select
//             name="primary_language"
//             value={formData.primary_language}
//             onChange={handleChange}
//           >
//             {/* Removed "Select..." option */}
//             <option value="English">English</option>
//             <option value="Chinese">Chinese</option>
//             <option value="Malay">Malay</option>
//             <option value="Other">Others</option>
//           </select>
//         </div>

//         <div className="input-field">
//           <label>English Proficiency (1 - 5)</label>
//           <input
//             type="number"
//             name="english_proficiency"
//             min="1"
//             max="5"
//             value={formData.english_proficiency}
//             onChange={handleChange}
//           />
//         </div>

//         <div className="input-field">
//           <label>Academic Year & Trimester</label>
//           <select
//             name="year_trimester"
//             value={formData.year_trimester}
//             onChange={handleChange}
//           >
//             {/* Removed "Select..." option */}
//             <option value="Year 1 Trimester 1">Year 1, Trimester 1</option>
//             <option value="Year 1 Trimester 2">Year 1, Trimester 2</option>
//             <option value="Year 1 Trimester 3">Year 1, Trimester 3</option>
//             <option value="Year 2 Trimester 1">Year 2, Trimester 1</option>
//             <option value="Year 2 Trimester 2">Year 2, Trimester 2</option>
//             <option value="Year 2 Trimester 3">Year 2, Trimester 3</option>
//             <option value="Year 3 Trimester 1">Year 3, Trimester 1</option>
//             <option value="Year 3 Trimester 2">Year 3, Trimester 2</option>
//             <option value="Year 3 Trimester 3">Year 3, Trimester 3</option>
//             <option value="Alumni">Alumni</option>
//           </select>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default PersonalInfoDropdown;

import React, { useState, useEffect } from "react";
import "../assets/styles.css";
import DropdownArrow from "../assets/img/dropdown-arrow.png";

function PersonalInfoDropdown({ initialData, onDataChange }) {
  const defaultData = {
    gender: "Female",
    yob: "2000",
    primary_language: "English",
    english_proficiency: 1,
    year_trimester: "Year 1 Trimester 1",
  };

  // Initialize state with initialData or defaultData.
  const [formData, setFormData] = useState(initialData || defaultData);
  const [isOpen, setIsOpen] = useState(false);

  // Update local state when initialData prop changes.
  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  useEffect(() => {
    if (typeof onDataChange === "function") {
      onDataChange(formData);
    }
  }, [formData, onDataChange]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    let newValue = value;

    if (name === "english_proficiency") {
      let proficiency = parseFloat(value);

      if (isNaN(proficiency)) proficiency = 0;
      if (proficiency < 0) proficiency = 0;
      if (proficiency > 5) proficiency = 5;

      newValue = proficiency;
    }

    setFormData({ ...formData, [name]: newValue });
  };

  return (
    <div className={`dropdown-container ${isOpen ? "open" : "closed"}`}>
      <div onClick={() => setIsOpen(!isOpen)} className="dropdown-header">
        <p>Personal Information</p>
        <img
          className={`arrow ${isOpen ? "up" : "down"}`}
          src={DropdownArrow}
          alt="dropdown-arrow"
        />
      </div>
      <div className="dropdown-content">
        <div className="input-field">
          <label>Gender</label>
          <select name="gender" value={formData.gender} onChange={handleChange}>
            <option value="Female">Female</option>
            <option value="Male">Male</option>
          </select>
        </div>
        <div className="input-field">
          <label>Year of Birth</label>
          <input
            type="number"
            name="yob"
            min="1900"
            max="2100"
            value={formData.yob}
            onChange={handleChange}
          />
        </div>
        <div className="input-field">
          <label>Primary Language</label>
          <select
            name="primary_language"
            value={formData.primary_language}
            onChange={handleChange}
          >
            <option value="English">English</option>
            <option value="Chinese">Chinese</option>
            <option value="Malay">Malay</option>
            <option value="Other">Others</option>
          </select>
        </div>
        <div className="input-field">
          <label>English Proficiency (1 - 5)</label>
          <input
            type="number"
            name="english_proficiency"
            min="1"
            max="5"
            value={formData.english_proficiency}
            onChange={handleChange}
          />
        </div>
        <div className="input-field">
          <label>Academic Year & Trimester</label>
          <select
            name="year_trimester"
            value={formData.year_trimester}
            onChange={handleChange}
          >
            <option value="Year 1 Trimester 1">Year 1, Trimester 1</option>
            <option value="Year 1 Trimester 2">Year 1, Trimester 2</option>
            <option value="Year 1 Trimester 3">Year 1, Trimester 3</option>
            <option value="Year 2 Trimester 1">Year 2, Trimester 1</option>
            <option value="Year 2 Trimester 2">Year 2, Trimester 2</option>
            <option value="Year 2 Trimester 3">Year 2, Trimester 3</option>
            <option value="Year 3 Trimester 1">Year 3, Trimester 1</option>
            <option value="Year 3 Trimester 2">Year 3, Trimester 2</option>
            <option value="Year 3 Trimester 3">Year 3, Trimester 3</option>
            <option value="Alumni">Alumni</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default PersonalInfoDropdown;
