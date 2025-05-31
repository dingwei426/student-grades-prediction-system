// src/components/ErrorModal.jsx
import React from "react";
import "../assets/styles.css"; // Ensure the styles file is imported
import LongButton from "./LongButton"; // Import the LongButton component
import PageHeader from "./PageHeader";

const ErrorModal = ({ message, onClose }) => {
  // Return nothing if there's no error message
  if (!message) return null;

  return (
    <div className="error-modal-overlay">
      <div className="error-modal">
        {/* <h2>Error</h2> */}
        <PageHeader
          title="Invalid Data Input"
          color="#1167b1"
          textAlign="left"
        />
        <p style={{ color: "#444", marginBottom: "10%" }}>{message}</p>
        {/* A container div to set the width of the button */}
        <div style={{ width: "70%", margin: "0 auto" }}>
          <LongButton text="Close" onClick={onClose} />
        </div>
      </div>
    </div>
  );
};

export default ErrorModal;
