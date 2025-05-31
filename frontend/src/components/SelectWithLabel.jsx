import React, { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa"; // import icons

function InputWithLabel({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
  errorMessage,
  min,
  max,
  step,
}) {
  const [showPassword, setShowPassword] = useState(false);

  // Determine the input type for password fields
  const inputType =
    type === "password" ? (showPassword ? "text" : "password") : type;

  return (
    <div style={{ marginBottom: "15px" }}>
      <label
        style={{
          display: "block",
          marginBottom: "5px",
          fontSize: "14px",
          color: "#03254c",
        }}
      >
        {label}
      </label>
      <div style={{ position: "relative" }}>
        <input
          type={inputType}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          min={min}
          max={max}
          step={step}
          style={{
            width: "100%",
            padding: "10px",
            paddingRight: type === "password" ? "40px" : "10px", // extra space for icon if password
            borderRadius: "4px",
            border: "1px solid #ccc",
            fontSize: "14px",
            boxSizing: "border-box",
          }}
        />
        {type === "password" && (
          <button
            type="button"
            onClick={() => setShowPassword((prev) => !prev)}
            style={{
              position: "absolute",
              right: "10px",
              top: "50%",
              transform: "translateY(-50%)",
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: "0",
              outline: "none",
            }}
          >
            {showPassword ? (
              <FaEyeSlash style={{ fontSize: "18px", color: "#555" }} />
            ) : (
              <FaEye style={{ fontSize: "18px", color: "#555" }} />
            )}
          </button>
        )}
      </div>
      {errorMessage && (
        <div style={{ color: "red", fontSize: "12px", marginTop: "5px" }}>
          {errorMessage}
        </div>
      )}
    </div>
  );
}

// SelectWithLabel Component for select dropdowns
function SelectWithLabel({ label, value, onChange, options, errorMessage }) {
  return (
    <div style={{ marginBottom: "15px" }}>
      <label
        style={{
          display: "block",
          marginBottom: "5px",
          fontSize: "14px",
          color: "#03254c",
        }}
      >
        {label}
      </label>
      <select
        value={value}
        onChange={onChange}
        style={{
          width: "100%", // Consistent width with input
          padding: "10px",
          borderRadius: "4px",
          border: "1px solid #ccc",
          fontSize: "14px",
          boxSizing: "border-box",
        }}
      >
        {options.map((option, index) => (
          <option key={index} value={option}>
            {option}
          </option>
        ))}
      </select>
      {errorMessage && (
        <div style={{ color: "red", fontSize: "12px", marginTop: "5px" }}>
          {errorMessage}
        </div>
      )}
    </div>
  );
}

export { InputWithLabel, SelectWithLabel };
