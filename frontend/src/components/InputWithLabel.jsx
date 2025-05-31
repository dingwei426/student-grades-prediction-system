import React from "react";

function InputWithLabel({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
  errorMessage,
}) {
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
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        style={{
          width: "96%",
          padding: "10px",
          borderRadius: "4px",
          border: "1px solid #ccc",
          fontSize: "14px",
        }}
      />
      {errorMessage && (
        <div style={{ color: "red", fontSize: "12px", marginTop: "5px" }}>
          {errorMessage}
        </div>
      )}
    </div>
  );
}

export default InputWithLabel;
